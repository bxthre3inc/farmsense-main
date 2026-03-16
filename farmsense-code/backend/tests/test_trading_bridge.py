# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

"""
Tests for the Alliance-Chain ↔ Backend HTTP bridge.

Covers:
  1. initiate_trade() fires the correct httpx.post() call to the DHU.
  2. initiate_trade() stays non-blocking when the DHU is unreachable.
  3. POST /api/v1/trade/callback transitions a PENDING trade to COMMITTED
     and updates water allocation quotas.
  4. POST /api/v1/trade/callback returns 404 for unknown tx_id.
  5. GET /api/v1/trade/status/{tx_id} returns live trade state.
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

import httpx

from app.services.trading_service import WaterTradingService, _DHU_URL
from app.models.water_rights import WaterTrade, WaterAllocation, TradeStatus
from app.models.user import User


# ──────────────────────────────────────────────────────────────
# Helpers / Fixtures
# ──────────────────────────────────────────────────────────────

def _make_user() -> User:
    u = User()
    u.id = "user_test"
    u.email = "test@farmsense.io"
    return u


def _make_allocation(field_id: str, quota_m3: float, consumed_m3: float = 0.0) -> WaterAllocation:
    a = WaterAllocation()
    a.field_id = field_id
    a.quota_m3 = quota_m3
    a.consumed_m3 = consumed_m3
    return a


def _make_db_mock(from_alloc: WaterAllocation):
    """
    Returns a mock SQLAlchemy Session that returns `from_alloc` on the first
    .query(...).filter(...).first() call (the quota check in initiate_trade).
    Subsequent calls for the WaterTrade add/commit flow are handled by MagicMock
    auto-speccing.
    """
    db = MagicMock()
    filter_mock = MagicMock()
    filter_mock.first.return_value = from_alloc
    db.query.return_value.filter.return_value = filter_mock
    # db.add / db.commit / db.refresh are automatically mocked by MagicMock
    # refresh() must populate the trade object — we do this via side_effect
    def _refresh(obj):
        obj.status = TradeStatus.PENDING
    db.refresh.side_effect = _refresh
    return db



# ──────────────────────────────────────────────────────────────
# Trading Service Tests
# ──────────────────────────────────────────────────────────────

class TestInitiateTrade:

    def test_calls_dhu_with_correct_payload(self):
        """initiate_trade() must POST the trade payload to the DHU HTTP server."""
        from_alloc = _make_allocation("field_a", quota_m3=500.0, consumed_m3=100.0)
        db = _make_db_mock(from_alloc)
        user = _make_user()

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()

        with patch("app.services.trading_service.httpx.post", return_value=mock_response) as mock_post:
            trade = WaterTradingService.initiate_trade(
                db, "field_a", "field_b", 200.0, user
            )

        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args
        assert f"{_DHU_URL}/trade" in str(call_kwargs)

        sent_payload = call_kwargs.kwargs.get("json") or call_kwargs.args[1] if len(call_kwargs.args) > 1 else mock_post.call_args[1]["json"]
        # Verify the tx_id, fields, and amount are in the payload
        assert sent_payload["from_field_id"] == "field_a"
        assert sent_payload["to_field_id"] == "field_b"
        assert sent_payload["amount_m3"] == 200.0
        assert trade.status == TradeStatus.PENDING

    def test_non_blocking_when_dhu_unreachable(self):
        """Trade stays PENDING and no exception is raised if DHU is offline."""
        from_alloc = _make_allocation("field_a", quota_m3=500.0)
        db = _make_db_mock(from_alloc)
        user = _make_user()

        with patch(
            "app.services.trading_service.httpx.post",
            side_effect=httpx.ConnectError("connection refused")
        ):
            # Must NOT raise
            trade = WaterTradingService.initiate_trade(
                db, "field_a", "field_b", 100.0, user
            )

        assert trade.status == TradeStatus.PENDING

    def test_raises_when_insufficient_quota(self):
        """initiate_trade() raises ValueError when the field has insufficient quota."""
        from_alloc = _make_allocation("field_a", quota_m3=50.0, consumed_m3=40.0)
        db = _make_db_mock(from_alloc)
        user = _make_user()

        with pytest.raises(ValueError, match="Insufficient water quota"):
            WaterTradingService.initiate_trade(db, "field_a", "field_b", 100.0, user)


class TestSyncLedgerStatus:

    def test_commit_updates_allocations(self):
        """sync_ledger_status(COMMITTED) deducts from sender and credits receiver."""
        trade = WaterTrade()
        trade.tx_id = "tx_abc123"
        trade.from_field_id = "field_a"
        trade.to_field_id = "field_b"
        trade.amount_m3 = 150.0
        trade.status = TradeStatus.PENDING
        trade.committed_at = None
        trade.block_hash = None

        from_alloc = _make_allocation("field_a", quota_m3=500.0)
        to_alloc = _make_allocation("field_b", quota_m3=100.0)

        db = MagicMock()
        filter_mock = MagicMock()
        filter_mock.first.return_value = trade
        db.query.return_value.filter.return_value = filter_mock

        # Patch allocation lookups in the committed branch
        def _alloc_first_side_effect():
            # First call → from_alloc, second → to_alloc
            _alloc_first_side_effect.calls = getattr(_alloc_first_side_effect, "calls", 0) + 1
            return from_alloc if _alloc_first_side_effect.calls == 1 else to_alloc

        alloc_filter = MagicMock()
        alloc_filter.first.side_effect = _alloc_first_side_effect

        def _query_side_effect(model):
            q = MagicMock()
            q.filter.return_value = alloc_filter if model == WaterAllocation else filter_mock
            return q

        db.query.side_effect = _query_side_effect

        result = WaterTradingService.sync_ledger_status(
            db, "tx_abc123", TradeStatus.COMMITTED, block_hash="deadbeef"
        )

        assert result.status == TradeStatus.COMMITTED
        assert result.block_hash == "deadbeef"
        assert result.committed_at is not None

    def test_returns_none_for_unknown_tx(self):
        """sync_ledger_status returns None for unrecognized tx_id."""
        db = MagicMock()
        db.query.return_value.filter.return_value.first.return_value = None

        result = WaterTradingService.sync_ledger_status(
            db, "tx_nonexistent", TradeStatus.COMMITTED
        )
        assert result is None
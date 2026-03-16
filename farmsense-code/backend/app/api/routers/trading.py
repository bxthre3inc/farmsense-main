# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.water_rights import WaterTrade, WaterAllocation, TradeStatus
from app.services.trading_service import WaterTradingService
from pydantic import BaseModel

router = APIRouter()


class TradeInitiateRequest(BaseModel):
    from_field_id: str
    to_field_id: str
    amount_m3: float


class DHUCallbackRequest(BaseModel):
    """JSON body sent by the Go AllianceChain HTTP server on PBFT block finalization."""
    tx_id: str
    status: str          # "COMMITTED" | "FAILED"
    block_hash: str = ""


@router.post("/initiate", tags=["Trading"])
def initiate_water_trade(
    req: TradeInitiateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Starts a water rights transfer between fields and broadcasts it to the DHU AllianceChain."""
    try:
        return WaterTradingService.initiate_trade(
            db, req.from_field_id, req.to_field_id, req.amount_m3, user
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/callback", tags=["Trading"])
def dhu_alliance_chain_callback(
    req: DHUCallbackRequest,
    db: Session = Depends(get_db),
):
    """
    Callback endpoint for the DHU Go AllianceChain service.
    Called automatically after PBFT quorum is reached and a block is finalized.
    Updates the trade status and adjusts water allocation quotas atomically.
    
    > [!CAUTION]
    > **SECURITY VULNERABILITY**: This endpoint currently lacks authentication. 
    > An attacker could spoof a COMMITTED status to artificially inflate their water quota.
    > In production, this MUST be restricted by:
    > 1. MTLS (Mutual TLS) between DHU and Backend.
    > 2. IP Whitelisting (Subnet-level).
    > 3. HMCA/Signature verification of the DHU payload.
    """
    try:
        status = TradeStatus(req.status)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status '{req.status}'. Expected: COMMITTED or FAILED."
        )

    trade = WaterTradingService.sync_ledger_status(
        db, req.tx_id, status, block_hash=req.block_hash
    )
    if trade is None:
        raise HTTPException(
            status_code=404,
            detail=f"Trade '{req.tx_id}' not found in local ledger."
        )

    return {
        "tx_id": trade.tx_id,
        "status": trade.status.value,
        "block_hash": req.block_hash,
        "committed_at": trade.committed_at.isoformat() if trade.committed_at else None,
    }


@router.get("/status/{tx_id}", tags=["Trading"])
def get_trade_status(
    tx_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Retrieve live status of a water rights trade by tx_id."""
    trade = db.query(WaterTrade).filter(WaterTrade.tx_id == tx_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail=f"Trade '{tx_id}' not found.")
    return {
        "tx_id": trade.tx_id,
        "from_field_id": trade.from_field_id,
        "to_field_id": trade.to_field_id,
        "amount_m3": trade.amount_m3,
        "status": trade.status.value,
        "committed_at": trade.committed_at.isoformat() if trade.committed_at else None,
        "created_at": trade.created_at.isoformat() if trade.created_at else None,
    }


@router.get("/ledger", tags=["Trading"])
def get_trading_ledger(
    field_id: str = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Retrieves the history of water rights trades."""
    query = db.query(WaterTrade)
    if field_id:
        query = query.filter(
            (WaterTrade.from_field_id == field_id) |
            (WaterTrade.to_field_id == field_id)
        )
    return query.order_by(WaterTrade.created_at.desc()).all()


@router.get("/allocations", tags=["Trading"])
def get_water_allocations(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Returns current water quotas for all fields."""
    return db.query(WaterAllocation).all()

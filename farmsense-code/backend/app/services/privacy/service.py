# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import hashlib
import uuid
import secrets
from datetime import datetime, timezone
from typing import Optional, Sequence
from .schemas import (
    PrivacyTier, PrivacyConfig, SensorPoint, 
    AnonymizedPoint, PrivacyAuditRecord
)
from .algorithms import add_jitter, snap_to_grid, laplace_noise

class SpatialPrivacyService:
    """Dual-layer spatial privacy service."""

    def apply_privacy(
        self,
        points: Sequence[SensorPoint],
        tier: PrivacyTier = PrivacyTier.RESEARCH,
        config: Optional[PrivacyConfig] = None,
    ) -> tuple[list[AnonymizedPoint], list[PrivacyAuditRecord]]:
        """
        Apply dual-layer privacy transformation to a batch of sensor points.

        Returns
        -------
        (anonymized_points, audit_records)
            anonymized_points — ready for export; suppressed entries have suppressed=True.
            audit_records     — append to immutable audit store.
        """
        cfg = config or TIER_DEFAULTS[tier]
        now = datetime.now(timezone.utc).isoformat()

        # ── Layer 1: Geometric ──────────────────────────────────────────
        stage1: list[tuple[SensorPoint, float, float]] = []
        for p in points:
            lat, lon = add_jitter(p.latitude, p.longitude, cfg.jitter_radius_m)
            lat, lon = snap_to_grid(lat, lon, cfg.grid_snap_m)
            stage1.append((p, lat, lon))

        # ── k-anonymity check ──────────────────────────────────────────
        # Count distinct field_ids per (grid_lat, grid_lon) cell
        cell_field_map: dict[tuple, set] = {}
        for p, lat, lon in stage1:
            cell = (round(lat, 5), round(lon, 5))
            cell_field_map.setdefault(cell, set()).add(p.field_id)

        # ── Layer 2: Contextual + assemble output ──────────────────────
        anon_points: list[AnonymizedPoint] = []
        audit_records: list[PrivacyAuditRecord] = []

        for p, lat, lon in stage1:
            cell = (round(lat, 5), round(lon, 5))
            k_count = len(cell_field_map[cell])
            suppressed = k_count < cfg.k_anonymity_min

            m_s = laplace_noise(p.moisture_surface, sensitivity=5.0, epsilon=cfg.epsilon_moisture)
            m_r = laplace_noise(p.moisture_root,    sensitivity=5.0, epsilon=cfg.epsilon_moisture)
            temp = laplace_noise(p.temperature,      sensitivity=2.0, epsilon=cfg.epsilon_temperature)
            ec   = laplace_noise(p.ec_surface or 0.0, sensitivity=0.5, epsilon=cfg.epsilon_moisture) if p.ec_surface is not None else None
            ph   = laplace_noise(p.ph or 7.0,        sensitivity=0.2, epsilon=cfg.epsilon_moisture) if p.ph is not None else None

            cluster_id = self._opaque_cluster_id(p.field_id if not cfg.strip_field_id else "ANON", lat, lon)
            sensor_tok = self._anon_sensor_token() if cfg.strip_sensor_id else p.sensor_id

            anon_points.append(AnonymizedPoint(
                cluster_id=cluster_id,
                anon_sensor_token=sensor_tok,
                latitude=round(lat, 5),
                longitude=round(lon, 5),
                moisture_surface=round(m_s, 3) if not suppressed else 0.0,
                moisture_root=round(m_r, 3)    if not suppressed else 0.0,
                temperature=round(temp, 2)     if not suppressed else 0.0,
                ec_surface=round(ec, 3) if ec is not None and not suppressed else None,
                ph=round(ph, 2)         if ph is not None and not suppressed else None,
                suppressed=suppressed,
                privacy_tier=cfg.tier.value,
                noise_budget_used={
                    "epsilon_moisture": cfg.epsilon_moisture,
                    "epsilon_temperature": cfg.epsilon_temperature,
                },
            ))

            audit_records.append(PrivacyAuditRecord(
                event_id=str(uuid.uuid4()),
                field_id_hash=hashlib.sha256(p.field_id.encode()).hexdigest()[:16],
                sensor_id_hash=hashlib.sha256(p.sensor_id.encode()).hexdigest()[:16],
                tier_applied=cfg.tier.value,
                jitter_applied_m=cfg.jitter_radius_m,
                laplace_epsilon_moisture=cfg.epsilon_moisture,
                laplace_epsilon_temperature=cfg.epsilon_temperature,
                k_threshold=cfg.k_anonymity_min,
                suppressed=suppressed,
                timestamp=now,
            ))

        return anon_points, audit_records

    def anonymize_aggregate(
        self,
        field_id: str,
        avg_moisture: float,
        avg_temperature: float,
        contributor_count: int,
        tier: PrivacyTier = PrivacyTier.RESEARCH,
    ) -> dict:
        """
        Lightweight anonymization for already-aggregated basin statistics.
        Used by federated learning result broadcast.
        """
        cfg = TIER_DEFAULTS[tier]
        if contributor_count < cfg.k_anonymity_min:
            return {"suppressed": True, "reason": "k-anonymity threshold not met"}

        return {
            "cluster_id": self._opaque_cluster_id(field_id if not cfg.strip_field_id else "ANON", 0.0, 0.0),
            "avg_moisture": round(laplace_noise(avg_moisture, 5.0, cfg.epsilon_moisture), 3),
            "avg_temperature": round(laplace_noise(avg_temperature, 2.0, cfg.epsilon_temperature), 2),
            "contributor_count": contributor_count,
            "suppressed": False,
            "privacy_tier": cfg.tier.value,
        }

    @staticmethod
    def _opaque_cluster_id(field_id: str, grid_lat: float, grid_lon: float) -> str:
        """
        Deterministic but unlinkable cluster identifier.
        Same field + cell = same cluster_id (stable across queries).
        Different field + same cell = different cluster_id.
        Reveals nothing about field identity.
        """
        # Round to 3 decimal places (~100m) to match researchers' grid snap precision
        # This prevents leaking high-fidelity 1m resolution coordinates via the hash digest
        raw = f"{field_id}:{grid_lat:.3f}:{grid_lon:.3f}:FARMSENSE_SALT_V1"
        digest = hashlib.sha256(raw.encode()).hexdigest()[:16]
        return f"clstr_{digest}"

    @staticmethod
    def _anon_sensor_token() -> str:
        """Per-export ephemeral token. Not stable across calls by design."""
        return f"anon_{uuid.uuid4().hex[:12]}"
# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Sequence

class PrivacyTier(str, Enum):
    """
    RESEARCH  – highest precision, basin-level aggregates only, no field IDs.
    PARTNER   – grid-snapped coordinates, k>=3, ε=1.0.
    INTERNAL  – full precision, field IDs intact, for authenticated FarmSense staff.
    RAW       – no anonymization (on-device only, never exported).
    """
    RESEARCH = "research"
    PARTNER  = "partner"
    INTERNAL = "internal"
    RAW      = "raw"


@dataclass
class PrivacyConfig:
    tier: PrivacyTier = PrivacyTier.RESEARCH
    jitter_radius_m: float = 50.0
    grid_snap_m: float = 100.0
    use_bbox_generalization: bool = False # Layer 2 — Contextual
    k_anonymity_min: int = 3               # suppress cell if fewer than k contributors
    epsilon_moisture: float = 0.5          # Laplace ε for moisture readings
    epsilon_temperature: float = 1.0       # Laplace ε for temperature
    strip_field_id: bool = True            # replace field_id with cluster_id
    strip_sensor_id: bool = True           # replace sensor_id with anonymous token


TIER_DEFAULTS: dict[PrivacyTier, PrivacyConfig] = {
    PrivacyTier.RESEARCH: PrivacyConfig(
        tier=PrivacyTier.RESEARCH,
        jitter_radius_m=50.0,
        grid_snap_m=100.0,
        k_anonymity_min=5,
        epsilon_moisture=0.5,
        epsilon_temperature=1.0,
        strip_field_id=True,
        strip_sensor_id=True,
    ),
    PrivacyTier.PARTNER: PrivacyConfig(
        tier=PrivacyTier.PARTNER,
        jitter_radius_m=20.0,
        grid_snap_m=50.0,
        k_anonymity_min=3,
        epsilon_moisture=1.0,
        epsilon_temperature=2.0,
        strip_field_id=True,
        strip_sensor_id=True,
    ),
    PrivacyTier.INTERNAL: PrivacyConfig(
        tier=PrivacyTier.INTERNAL,
        jitter_radius_m=0.0,
        grid_snap_m=1.0,
        k_anonymity_min=1,
        epsilon_moisture=0.0,   # 0 = no noise
        epsilon_temperature=0.0,
        strip_field_id=False,
        strip_sensor_id=False,
    ),
    PrivacyTier.RAW: PrivacyConfig(
        tier=PrivacyTier.RAW,
        jitter_radius_m=0.0,
        grid_snap_m=0.0,
        k_anonymity_min=1,
        epsilon_moisture=0.0,
        epsilon_temperature=0.0,
        strip_field_id=False,
        strip_sensor_id=False,
    ),
}


@dataclass
class SensorPoint:
    """A single sensor observation prior to anonymization."""
    sensor_id: str
    field_id: str
    latitude: float
    longitude: float
    moisture_surface: float
    moisture_root: float
    temperature: float
    ec_surface: Optional[float] = None
    ph: Optional[float] = None
    timestamp: Optional[str] = None


@dataclass
class AnonymizedPoint:
    """A sensor observation after dual-layer privacy transformation."""
    cluster_id: str
    anon_sensor_token: str
    latitude: float
    longitude: float
    moisture_surface: float
    moisture_root: float
    temperature: float
    ec_surface: Optional[float]
    ph: Optional[float]
    suppressed: bool = False
    privacy_tier: str = PrivacyTier.RESEARCH
    noise_budget_used: dict = field(default_factory=dict)


@dataclass
class PrivacyAuditRecord:
    """Immutable audit entry for every anonymization event."""
    event_id: str
    field_id_hash: str
    sensor_id_hash: str
    tier_applied: str
    jitter_applied_m: float
    laplace_epsilon_moisture: float
    laplace_epsilon_temperature: float
    k_threshold: int
    suppressed: bool
    timestamp: str
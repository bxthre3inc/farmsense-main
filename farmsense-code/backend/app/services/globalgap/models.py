# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from dataclasses import dataclass, field
from typing import Optional
from .constants import NCLevel

@dataclass
class ControlPointResult:
    control_point_id: str
    description: str
    score: float                      # 0.0 – 1.0
    level: NCLevel
    evidence: list[str]               # Evidence strings from FarmSense data
    findings: list[str]               # GLOBALG.A.P. auditor-style findings
    corrective_actions: list[str]     # Required before next audit


@dataclass
class GAP_FieldInputs:
    """All FarmSense-derived metrics needed for a GLOBALG.A.P. evaluation."""
    field_id: str
    field_name: str
    farm_name: str
    grower_id: str
    report_period_start: str
    report_period_end: str

    # CB 5.2 — Water source
    water_source_type: str                  # "groundwater", "surface", "municipal", "recycled"
    water_source_documented: bool           # Permit/documentation on file

    # CB 5.3 — Application method
    application_method: str                 # "drip", "sprinkler", "flood", "subsurface"
    application_method_documented: bool

    # CB 5.5 — Water quality
    avg_ec_us_cm: float                     # Electrical conductivity microsiemens/cm
    min_ph: float
    max_ph: float
    microbiological_test_conducted: bool    # At least once per season
    ec_within_threshold: bool               # EC < 2500 µS/cm for GLOBALG.A.P.
    ph_within_threshold: bool               # pH 5.5 – 8.5

    # FV 5.1 — Efficiency
    season_water_applied_m3: float
    prev_season_water_applied_m3: float     # For year-over-year comparison
    documented_efficiency_target: bool       # Written target exists
    efficiency_target_pct: float            # Target reduction vs prev year (%)
    actual_efficiency_gain_pct: float       # What was achieved

    # AG5.2 — Metering
    calibrated_meter_installed: bool
    meter_last_calibration_date: Optional[str]  # ISO date
    monthly_meter_logs: bool               # At least 12 logs in period
    total_metered_volume_m3: float

    # AF1.2 — Site history
    site_risk_assessment_date: Optional[str]   # ISO date
    previous_land_use_documented: bool
    restricted_substances_audit: bool


@dataclass
class GAP_Report:
    report_id: str
    field_id: str
    field_name: str
    farm_name: str
    grower_id: str
    period_start: str
    period_end: str
    generated_at: str
    globalGAP_standard: str = "IFA v6.0 — FV Module"

    control_points: list[ControlPointResult] = field(default_factory=list)
    overall_score: float = 0.0
    certification_status: NCLevel = NCLevel.PASS
    summary_narrative: str = ""
    markdown_report: str = ""
    verifiable_hash: str = ""   # SHA-256 of report data for audit chain
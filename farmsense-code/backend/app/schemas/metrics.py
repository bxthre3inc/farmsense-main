# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from pydantic import BaseModel
from datetime import datetime

class ComplianceReportResponse(BaseModel):
    id: str
    field_id: str
    report_period_start: datetime
    report_period_end: datetime
    total_irrigation_m3: float
    water_use_efficiency: float
    slv_2026_compliant: str
    validation_status: str
    
    class Config:
        from_attributes = True

class ResearchDatasetResponse(BaseModel):
    id: str
    name: str
    size_mb: float
    rows: int
    created_at: datetime
    type: str

class InvestorMetricsResponse(BaseModel):
    total_acreage: float
    enterprise_clients: int
    total_users: int
    arr_usd: float
    growth_pct: float
    retention_rate: float

class GrantImpactResponse(BaseModel):
    grant_id: str
    water_saved_liters: float
    co2_reduced_tons: float
    yield_increase_pct: float
    soil_health_index: float
    funding_disbursed_usd: float

class ComplianceMetricsResponse(BaseModel):
    compliance_rate_pct: float
    critical_violations: int
    audits_this_month: int
    total_fields_monitored: int

class AdminMetricsResponse(BaseModel):
    active_users: int
    system_health_pct: float
    pending_audits: int
    user_growth_pct: float
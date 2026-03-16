# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.api.dependencies import get_current_user, RequireRole
from app.models.user import User, UserRole
from app.models import ComplianceReport

from app.schemas.metrics import ComplianceReportResponse
from app.services.compliance_service import ComplianceService

router = APIRouter()

@router.get("/reports", response_model=list[ComplianceReportResponse], tags=["Compliance"])
def list_compliance_reports(
    field_id: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """List compliance reports with optional filtering"""
    query = db.query(ComplianceReport)
    
    if field_id:
        query = query.filter(ComplianceReport.field_id == field_id)
    if start_date:
        query = query.filter(ComplianceReport.report_period_start >= start_date)
    if end_date:
        query = query.filter(ComplianceReport.report_period_end <= end_date)
    if status:
        query = query.filter(ComplianceReport.validation_status == status)
        
    return query.order_by(ComplianceReport.report_period_end.desc()).limit(100).all()

@router.post("/reports/generate", tags=["Compliance"])
def generate_compliance_report(
    field_id: str,
    period_start: datetime,
    period_end: datetime,
    report_type: str = "monthly",
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Generate SLV 2026 compliance report for a field and time period
    Heavy computation - runs in background
    """
    from app.api.tasks import generate_compliance_report_task
    task_id = f"report_{field_id}_{datetime.utcnow().timestamp()}"
    
    if background_tasks:
        background_tasks.add_task(
            generate_compliance_report_task,
            field_id, period_start, period_end, report_type, db
        )
        return {"status": "accepted", "task_id": task_id, "message": "Report generation started in background"}
    else:
        # Synchronous execution if no background tasks provided
        generate_compliance_report_task(field_id, period_start, period_end, report_type, db)
        return {"status": "completed", "message": "Report generated synchronously"}


@router.get("/audit/field/{field_id}", tags=["Regulatory"], dependencies=[Depends(RequireRole([UserRole.REGULATOR, UserRole.INTERNAL]))])
def get_field_audit_report(
    field_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Generate a non-repudiable Water Court Audit Report (bx3 Standard).
    Consolidates UFI scores, high-res kriging metadata, and AllianceChain proofs.
    Requires REGULATOR or INTERNAL role.
    """
    report = ComplianceService.generate_audit_report(db, field_id, user)
    return report


# ──────────────────────────────────────────────────────────
# GLOBALG.A.P. IFA v6 Compliance Endpoints
# ──────────────────────────────────────────────────────────

from pydantic import BaseModel as PydanticBase
from typing import Optional as Opt


class GAPFieldInputsRequest(PydanticBase):
    """All FarmSense-derived metrics for a GLOBALG.A.P. IFA v6 evaluation."""
    field_id: str
    field_name: str
    farm_name: str
    grower_id: str
    report_period_start: str
    report_period_end: str

    # CB 5.2
    water_source_type: str = "groundwater"
    water_source_documented: bool = False

    # CB 5.3
    application_method: str = "drip"
    application_method_documented: bool = False

    # CB 5.5
    avg_ec_us_cm: float = 1200.0
    min_ph: float = 6.5
    max_ph: float = 7.8
    microbiological_test_conducted: bool = False
    ec_within_threshold: bool = True
    ph_within_threshold: bool = True

    # FV 5.1
    season_water_applied_m3: float = 0.0
    prev_season_water_applied_m3: float = 0.0
    documented_efficiency_target: bool = False
    efficiency_target_pct: float = 10.0
    actual_efficiency_gain_pct: float = 0.0

    # AG 5.2
    calibrated_meter_installed: bool = False
    meter_last_calibration_date: Opt[str] = None
    monthly_meter_logs: bool = False
    total_metered_volume_m3: float = 0.0

    # AF 1.2
    site_risk_assessment_date: Opt[str] = None
    previous_land_use_documented: bool = False
    restricted_substances_audit: bool = False


# In-memory report cache per field (replace with DB in production)
_gap_report_cache: dict[str, dict] = {}


@router.post("/reports/gap/generate", tags=["GLOBALG.A.P."])
def generate_gap_report(
    request: GAPFieldInputsRequest,
    user: User = Depends(get_current_user),
):
    """
    Generate a GLOBALG.A.P. IFA v6 compliance report from FarmSense field data.

    Evaluates 6 control points:
      AF 1.2 — Site History & Risk Assessment
      CB 5.2 — Irrigation Water Source Documentation
      CB 5.3 — Irrigation Application Method
      CB 5.5 — Irrigation Water Quality Monitoring
      FV 5.1 — Water Efficiency Targets & Achievement
      AG 5.2 — Water Metering & Volumetric Reporting

    Returns JSON report + full Markdown narrative ready for submission prep.
    Each report includes a SHA-256 verifiable hash for audit chain integration.
    """
    from app.services.globalgap import gap_engine, GAP_FieldInputs

    inputs = GAP_FieldInputs(
        field_id=request.field_id,
        field_name=request.field_name,
        farm_name=request.farm_name,
        grower_id=request.grower_id,
        report_period_start=request.report_period_start,
        report_period_end=request.report_period_end,
        water_source_type=request.water_source_type,
        water_source_documented=request.water_source_documented,
        application_method=request.application_method,
        application_method_documented=request.application_method_documented,
        avg_ec_us_cm=request.avg_ec_us_cm,
        min_ph=request.min_ph,
        max_ph=request.max_ph,
        microbiological_test_conducted=request.microbiological_test_conducted,
        ec_within_threshold=request.ec_within_threshold,
        ph_within_threshold=request.ph_within_threshold,
        season_water_applied_m3=request.season_water_applied_m3,
        prev_season_water_applied_m3=request.prev_season_water_applied_m3,
        documented_efficiency_target=request.documented_efficiency_target,
        efficiency_target_pct=request.efficiency_target_pct,
        actual_efficiency_gain_pct=request.actual_efficiency_gain_pct,
        calibrated_meter_installed=request.calibrated_meter_installed,
        meter_last_calibration_date=request.meter_last_calibration_date,
        monthly_meter_logs=request.monthly_meter_logs,
        total_metered_volume_m3=request.total_metered_volume_m3,
        site_risk_assessment_date=request.site_risk_assessment_date,
        previous_land_use_documented=request.previous_land_use_documented,
        restricted_substances_audit=request.restricted_substances_audit,
    )

    report = gap_engine.generate(inputs)

    # Cache for quick retrieval
    _gap_report_cache[request.field_id] = {
        "report_id": report.report_id,
        "field_id": report.field_id,
        "field_name": report.field_name,
        "farm_name": report.farm_name,
        "period_start": report.period_start,
        "period_end": report.period_end,
        "generated_at": report.generated_at,
        "globalGAP_standard": report.globalGAP_standard,
        "overall_score": report.overall_score,
        "certification_status": report.certification_status.value,
        "summary_narrative": report.summary_narrative,
        "verifiable_hash": report.verifiable_hash,
        "control_points": [
            {
                "control_point_id": cp.control_point_id,
                "description": cp.description,
                "score": cp.score,
                "level": cp.level.value,
                "evidence": cp.evidence,
                "findings": cp.findings,
                "corrective_actions": cp.corrective_actions,
            }
            for cp in report.control_points
        ],
        "markdown_report": report.markdown_report,
    }

    return _gap_report_cache[request.field_id]


@router.get("/reports/gap/{field_id}/latest", tags=["GLOBALG.A.P."])
def get_latest_gap_report(
    field_id: str,
    user: User = Depends(get_current_user),
):
    """Retrieve the most recently generated GLOBALG.A.P. report for a field."""
    if field_id not in _gap_report_cache:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail=f"No GLOBALG.A.P. report found for field '{field_id}'. Run POST /reports/gap/generate first."
        )
    return _gap_report_cache[field_id]


@router.get("/reports/gap/control-points", tags=["GLOBALG.A.P."])
def list_gap_control_points():
    """
    Returns the full registry of GLOBALG.A.P. IFA v6 control points
    evaluated by FarmSense, with their weights and descriptions.
    Useful for the compliance report UI to explain the scoring model.
    """
    from app.services.globalgap import (
        CONTROL_POINT_DESCRIPTIONS, CONTROL_POINT_WEIGHTS, ControlPointID
    )
    return [
        {
            "id": cp.value,
            "description": CONTROL_POINT_DESCRIPTIONS[cp],
            "weight": CONTROL_POINT_WEIGHTS[cp],
            "module": cp.value.split("_")[0],
        }
        for cp in ControlPointID
    ]

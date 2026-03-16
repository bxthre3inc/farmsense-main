# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from sqlalchemy import Column, String, Float, DateTime, JSON, Index, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .base import Base

class AuditLog(Base):
    """Immutable audit record for decisions made by the system"""
    __tablename__ = 'audit_logs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    decision_type = Column(String(50))
    input_telemetry = Column(JSON)
    rules_applied = Column(JSON)
    deterministic_output = Column(String(500))
    provenance = Column(String(200))
    model_type = Column(String(100))
    integrity_hash = Column(String(64), unique=True, index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class RecalculationLog(Base):
    """Audit log for adaptive recalculation engine"""
    __tablename__ = 'recalculation_logs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    trigger_type = Column(String(50))
    trigger_details = Column(JSON)
    previous_mode = Column(String(20))
    new_mode = Column(String(20))
    mode_reason = Column(String(200))
    moisture_trend = Column(String(20))
    trend_rate = Column(Float)
    next_scheduled = Column(DateTime)
    computation_duration_ms = Column(Integer)
    grid_cells_updated = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class ComplianceReport(Base):
    """SLV 2026 compliance reporting"""
    __tablename__ = 'compliance_reports'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(String(50), nullable=False, index=True)
    report_period_start = Column(DateTime, nullable=False)
    report_period_end = Column(DateTime, nullable=False)
    report_type = Column(String(50))
    total_irrigation_m3 = Column(Float)
    water_use_efficiency = Column(Float)
    allocation_compliance_pct = Column(Float)
    validation_score = Column(Float)
    avg_soil_health_index = Column(Float)
    nutrient_runoff_risk = Column(String(20))
    biodiversity_score = Column(Float)
    data_completeness_pct = Column(Float)
    sensor_uptime_pct = Column(Float)
    validation_status = Column(String(20))
    slv_2026_compliant = Column(String(10))
    violations = Column(JSON)
    corrective_actions = Column(JSON)
    report_hash = Column(String(64))
    signed_by = Column(String(100))
    signature = Column(String(512))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime)

    __table_args__ = (
        Index('idx_field_period', 'field_id', 'report_period_start', 'report_period_end'),
    )


class AnonymizedResearchArchive(Base):
    """Centralized collection for FarmSense platform"""
    __tablename__ = 'research_archive'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    anon_field_hash = Column(String(64), index=True) 
    timestamp = Column(DateTime, nullable=False, index=True)
    avg_moisture = Column(Float)
    avg_temperature = Column(Float)
    total_water_m3 = Column(Float)
    soil_type = Column(String(50))
    region_code = Column(String(20))
    
    created_at = Column(DateTime, default=datetime.utcnow)
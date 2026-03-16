# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum as sqlalchemy_enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid
import enum
from .base import Base

class WaterSourceType(str, enum.Enum):
    DITCH = "ditch"
    RIVER = "river"
    CREEK = "creek"
    WELL = "well"
    RECYCLED = "recycled"

class TradeStatus(str, enum.Enum):
    PENDING = "pending"
    COMMITTED = "committed"
    FAILED = "failed"

class WaterAllocation(Base):
    """Tracks field-level water cubic-meter quotas"""
    __tablename__ = 'water_allocations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(String(50), nullable=False, unique=True, index=True)
    source_type = Column(sqlalchemy_enum(WaterSourceType), default=WaterSourceType.WELL, nullable=False)
    source_name = Column(String(100), nullable=True) # e.g. "Rio Grande", "Lariat Ditch"
    priority = Column(Float, default=1.0) # Lower is higher priority (Seniority)
    quota_m3 = Column(Float, default=0.0)
    consumed_m3 = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class WaterTrade(Base):
    """Immutable log of water rights transfers"""
    __tablename__ = 'water_trades'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tx_id = Column(String(100), unique=True, index=True) # PBFT tx_id
    from_field_id = Column(String(50), nullable=False, index=True)
    to_field_id = Column(String(50), nullable=False, index=True)
    amount_m3 = Column(Float, nullable=False)
    source_type = Column(sqlalchemy_enum(WaterSourceType), nullable=True)
    price_per_m3 = Column(Float, nullable=True) # For tokenized trading
    status = Column(sqlalchemy_enum(TradeStatus), default=TradeStatus.PENDING)
    block_hash = Column(String(255), nullable=True) # PBFT block hash for audit
    committed_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
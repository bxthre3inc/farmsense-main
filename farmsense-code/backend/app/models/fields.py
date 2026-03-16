# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from datetime import datetime, timezone
from .base import Base

class Field(Base):
    """
    Represents a geographic field boundary (AOI - Area of Interest).
    Centric to the FarmSense spatial engine.
    """
    __tablename__ = 'fields'

    field_id = Column(String(50), primary_key=True, index=True)
    farm_id = Column(String(50), nullable=False, index=True)
    field_name = Column(String(200), nullable=False)
    
    # PostGIS Polygon Geometry (SRID 4326 - WGS 84)
    boundary = Column(Geometry('POLYGON', srid=4326), nullable=False)
    
    area_hectares = Column(Float)
    crop_type = Column(String(100))
    planting_date = Column(DateTime)
    harvest_date = Column(DateTime)
    soil_type = Column(String(100))
    irrigation_system = Column(String(50))
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Field(id={self.field_id}, name={self.field_name})>"

# Spatial Index for efficient AOI queries
Index('idx_fields_boundary', Field.boundary, postgresql_using='gist')
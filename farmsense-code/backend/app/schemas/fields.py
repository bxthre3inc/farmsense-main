# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class FieldBase(BaseModel):
    field_id: str
    field_name: str
    farm_id: str
    crop_type: Optional[str] = None
    soil_type: Optional[str] = None
    irrigation_system: Optional[str] = None

class FieldCreate(FieldBase):
    # GeoJSON Polygon Geometry
    # Expects: {"type": "Polygon", "coordinates": [[[lon, lat], ...]]}
    boundary_geojson: Dict[str, Any]

class FieldResponse(FieldBase):
    area_hectares: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
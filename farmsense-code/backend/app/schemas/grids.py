# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ZoneAnalysisRequest(BaseModel):
    geometry: dict = Field(..., description="GeoJSON Polygon geometry dict")

class ZoneAnalysisResponse(BaseModel):
    field_id: str
    Zone_area_sqm: float
    avg_moisture: float
    avg_temperature: float
    avg_stress_index: float
    estimated_water_deficit_mm: float
    intersecting_points_count: int

class SensorReadingResponse(BaseModel):
    id: str
    sensor_id: str
    field_id: str
    timestamp: datetime
    moisture_surface: float
    moisture_root: float
    temp_surface: float
    quality_flag: str
    
    class Config:
        from_attributes = True

class VirtualGridResponse(BaseModel):
    grid_id: str
    field_id: str
    timestamp: datetime
    latitude: float
    longitude: float
    moisture_surface: float
    moisture_root: float
    temperature: float
    water_deficit_mm: float
    stress_index: float
    irrigation_need: str
    confidence: float
    
    class Config:
        from_attributes = True

class FieldAnalyticsResponse(BaseModel):
    field_id: str
    analysis_time: datetime
    avg_moisture: float
    moisture_std: float
    stress_area_pct: float
    irrigation_Zones: List[dict]
    current_mode: str
    next_recalc: datetime
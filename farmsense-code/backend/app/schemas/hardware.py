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

class AerialMultispectralCreate(BaseModel):
    fleet_id: str
    field_id: str
    latitude: float
    longitude: float
    resolution_cm_px: float
    ndvi_avg: float
    ndre_avg: float

class VFAReadingCreate(BaseModel):
    hardware_id: str
    field_id: str
    latitude: float
    longitude: float
    nitrogen_pressure_psi: float
    slot_10_moisture: float
    slot_10_ec: float
    slot_10_temp: float
    slot_18_moisture: float
    slot_25_moisture: float
    slot_25_ec: float
    slot_25_temp: float
    slot_35_moisture: float
    slot_48_moisture: float
    slot_48_ec: float
    battery_voltage: float

class PFAReadingCreate(BaseModel):
    hardware_id: str
    field_id: str
    well_pressure_psi: float
    flow_rate_gpm: float
    pump_status: str
    current_harmonics: Optional[List[float]] = None

class PMTReadingCreate(BaseModel):
    hardware_id: str
    field_id: str
    latitude: float
    longitude: float
    kinematic_angle_deg: float
    span_speed_mph: float
    gps_fix_quality: int

class LRZReadingCreate(BaseModel):
    hardware_id: str
    field_id: str
    latitude: float
    longitude: float
    moisture_surface: float
    moisture_root: float
    temp_surface: float
    battery_voltage: float

class EBKGridCreate(BaseModel):
    hardware_id: str
    field_id: str
    latitude: float
    longitude: float
    attention_mode: str
    grid_resolution_m: int
    grid_rows: int
    grid_cols: int
    moisture_probability_grid: List[List[float]]

class SensorReadingCreate(BaseModel):
    sensor_id: str
    field_id: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    moisture_surface: float = Field(..., ge=0, le=1)
    moisture_root: float = Field(..., ge=0, le=1)
    temp_surface: float
    temp_root: Optional[float] = None
    vertical_profile: Optional[dict] = None
    ec_surface: Optional[float] = None
    ec_root: Optional[float] = None
    ph: Optional[float] = None
    battery_voltage: Optional[float] = None
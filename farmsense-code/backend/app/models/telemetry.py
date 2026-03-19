# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from sqlalchemy import Column, String, Float, DateTime, JSON, Index, ForeignKey, Enum as DBEnum
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
import uuid
from datetime import datetime
from enum import Enum as PyEnum
from .base import Base

class HardwareModel(str, PyEnum):
    LRZ = "LRZ"
    LRZN = "LRZN"
    LRZB = "LRZB"
    VFA = "VFA"
    DHU = "DHU"
    RSS = "RSS"
    PFA = "PFA"
    PMT = "PMT"
    CSA = "CSA"

class HardwareNode(Base):
    """Generic Hardware Node deployment tracker"""
    __tablename__ = 'hardware_nodes'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hardware_id = Column(String(50), nullable=False, unique=True, index=True)
    field_id = Column(String(50), nullable=False, index=True)
    node_type = Column(DBEnum(HardwareModel), nullable=False)
    
    # Hierarchy: LRZ/PFA/PMT/CSA -> VFA -> DHU -> RSS
    parent_hardware_id = Column(String(50), ForeignKey('hardware_nodes.hardware_id'), nullable=True)
    
    # Geospatial 
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    
    status = Column(String(20), default='active') # active, offline, maintenance
    battery_voltage = Column(Float)
    last_active = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class SoilSensorReading(Base):
    """Raw soil sensor readings - 2-depth + vertical profiling"""
    __tablename__ = 'soil_sensor_readings'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id = Column(String(50), nullable=False, index=True)
    field_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    
    # Geospatial
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    
    # Dual-depth readings (inches)
    moisture_surface = Column(Float)  # 0-12in
    moisture_root = Column(Float)     # 12-24in
    temp_surface = Column(Float)
    temp_root = Column(Float)
    
    # Vertical profiling (inches)
    vertical_profile = Column(JSON)  # [{depth_in: 10, moisture: 0.25, temp: 18.5}, ...]
    
    # Salinity and nutrients
    ec_surface = Column(Float)
    ec_root = Column(Float)
    ph = Column(Float)
    
    # Quality flags
    quality_flag = Column(String(20), default='valid')
    battery_voltage = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_sensor_field_time', 'sensor_id', 'field_id', 'timestamp'),
        Index('idx_field_time', 'field_id', 'timestamp'),
        Index('idx_spatial', 'location', postgresql_using='gist'),
    )


class LRZReading(Base):
    """Lateral Root-Zone Scout high-density readings"""
    __tablename__ = 'lrz_readings'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hardware_id = Column(String(50), ForeignKey('hardware_nodes.hardware_id'), nullable=False, index=True)
    field_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    
    dielectric_count = Column(Float)
    ec_count = Column(Float)
    battery_voltage = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class VFAReading(Base):
    """Vertical Field Anchor deep-profile reading"""
    __tablename__ = 'vfa_readings'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hardware_id = Column(String(50), ForeignKey('hardware_nodes.hardware_id'), nullable=False, index=True)
    field_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    
    nitrogen_pressure_psi = Column(Float)
    
    slot_10_moisture = Column(Float)
    slot_10_ec = Column(Float)
    slot_10_temp = Column(Float)
    slot_18_moisture = Column(Float)
    slot_25_moisture = Column(Float)
    slot_25_ec = Column(Float)
    slot_25_temp = Column(Float)
    slot_35_moisture = Column(Float)
    slot_48_moisture = Column(Float)
    slot_48_ec = Column(Float)
    
    battery_voltage = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class PFAReading(Base):
    """Pressure & Flow Anchor reading"""
    __tablename__ = 'pfa_readings'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hardware_id = Column(String(50), ForeignKey('hardware_nodes.hardware_id'), nullable=False, index=True)
    field_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    
    well_pressure_psi = Column(Float)
    flow_rate_gpm = Column(Float)
    pump_status = Column(String(20))
    current_harmonics = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class PMTReading(Base):
    """Pivot Motion Tracker kinematic reading"""
    __tablename__ = 'pmt_readings'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hardware_id = Column(String(50), ForeignKey('hardware_nodes.hardware_id'), nullable=False, index=True)
    field_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    
    kinematic_angle_deg = Column(Float)
    span_speed_mph = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class PumpTelemetry(Base):
    """Pump operational data"""
    __tablename__ = 'pump_telemetry'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pump_id = Column(String(50), nullable=False, index=True)
    field_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    
    status = Column(String(20))
    flow_rate_lpm = Column(Float)
    pressure_bar = Column(Float)
    power_consumption_kw = Column(Float)
    runtime_hours = Column(Float)
    volume_delivered_l = Column(Float)
    cumulative_volume_l = Column(Float)
    anomaly_score = Column(Float)
    anomaly_flag = Column(String(20), default='normal')
    
    created_at = Column(DateTime, default=datetime.utcnow)


class WeatherData(Base):
    """Weather station and forecast data"""
    __tablename__ = 'weather_data'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    station_id = Column(String(50), index=True)
    field_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    data_type = Column(String(20))
    
    temperature_c = Column(Float)
    humidity_pct = Column(Float)
    pressure_hpa = Column(Float)
    wind_speed_ms = Column(Float)
    wind_direction_deg = Column(Float)
    rainfall_mm = Column(Float)
    rainfall_intensity = Column(String(20))
    solar_radiation_wm2 = Column(Float)
    et0_mm = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
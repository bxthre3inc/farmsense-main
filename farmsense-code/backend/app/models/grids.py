# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from sqlalchemy import Column, String, Float, DateTime, JSON, Index, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
import uuid
from datetime import datetime
from .base import Base

class VirtualSensorGrid50m(Base):
    """Edge-computed 50m virtual sensor grid"""
    __tablename__ = 'virtual_sensor_grid_50m'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(String(50), nullable=False, index=True)
    grid_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    grid_cell = Column(Geometry('POLYGON', srid=4326))
    
    moisture_surface = Column(Float)
    moisture_root = Column(Float)
    temperature = Column(Float)
    water_deficit_mm = Column(Float)
    stress_index = Column(Float)
    irrigation_need = Column(String(20))
    computation_mode = Column(String(20))
    source_sensors = Column(JSON)
    confidence = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    physical_probe_value = Column(Float)
    edge_device_id = Column(String(50))
    
    __table_args__ = (
        Index('idx_field_grid_time_50m', 'field_id', 'grid_id', 'timestamp'),
        Index('idx_spatial_50m', 'location', postgresql_using='gist'),
    )


class VirtualSensorGrid20m(Base):
    """Edge-computed 20m virtual sensor grid"""
    __tablename__ = 'virtual_sensor_grid_20m'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(String(50), nullable=False, index=True)
    grid_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    grid_cell = Column(Geometry('POLYGON', srid=4326))
    
    moisture_surface = Column(Float)
    moisture_root = Column(Float)
    temperature = Column(Float)
    water_deficit_mm = Column(Float)
    stress_index = Column(Float)
    irrigation_need = Column(String(20))
    computation_mode = Column(String(20))
    source_sensors = Column(JSON)
    confidence = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    physical_probe_value = Column(Float)
    edge_device_id = Column(String(50))
    
    __table_args__ = (
        Index('idx_field_grid_time', 'field_id', 'grid_id', 'timestamp'),
        Index('idx_spatial_20m', 'location', postgresql_using='gist'),
    )


class VirtualSensorGrid10m(Base):
    """Cloud-computed 10m high-resolution virtual sensor grid"""
    __tablename__ = 'virtual_sensor_grid_10m'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(String(50), nullable=False, index=True)
    grid_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    grid_cell = Column(Geometry('POLYGON', srid=4326))
    
    moisture_surface = Column(Float)
    moisture_root = Column(Float)
    temperature = Column(Float)
    water_deficit_mm = Column(Float)
    stress_index = Column(Float)
    irrigation_need = Column(String(20))
    computation_mode = Column(String(20))
    source_sensors = Column(JSON)
    confidence = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    physical_probe_value = Column(Float)
    edge_device_id = Column(String(50))
    
    __table_args__ = (
        Index('idx_field_grid_time_10m', 'field_id', 'grid_id', 'timestamp'),
        Index('idx_spatial_10m', 'location', postgresql_using='gist'),
    )


class VirtualSensorGrid1m(Base):
    """Cloud-computed 1m high-resolution virtual sensor grid"""
    __tablename__ = 'virtual_sensor_grid_1m'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(String(50), nullable=False, index=True)
    grid_id = Column(String(100), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    
    moisture_surface = Column(Float)
    moisture_root = Column(Float)
    temperature = Column(Float)
    ndvi = Column(Float)
    ndwi = Column(Float)
    confidence_score = Column(Float, default=1.0)
    physical_probe_value = Column(Float)
    edge_device_id = Column(String(50))
    crop_stress_probability = Column(Float)
    yield_forecast_kgha = Column(Float)
    irrigation_priority = Column(Integer)
    kriging_variance = Column(Float)
    prediction_std = Column(Float)
    sentinel_cloud_pct = Column(Float)
    landsat_qa = Column(String(20))
    is_dual_use_enabled = Column(Boolean, default=False)
    jadc2_sync_status = Column(String(20), default='pending')
    
    created_at = Column(DateTime, default=datetime.now)
    
    __table_args__ = (
        Index('idx_field_time_1m', 'field_id', 'timestamp'),
        Index('idx_spatial_1m', 'location', postgresql_using='gist'),
    )
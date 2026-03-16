# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import asyncio
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.websocket import manager
from app.models import VFAReading, PFAReading, PMTReading, LRZReading, VirtualSensorGrid50m, VirtualSensorGrid1m

from app.schemas.hardware import (
    VFAReadingCreate, PFAReadingCreate, PMTReadingCreate,
    LRZReadingCreate, EBKGridCreate, AerialMultispectralCreate,
    SensorReadingCreate
)

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/vfa/payload", tags=["Hardware Ingestion"])
def ingest_vfa_payload(
    payload: VFAReadingCreate,
    db: Session = Depends(get_db)
):
    """Ingests the decrypted/aggregated AES-256 payload from a Vertical Field Anchor (VFA)."""
    vfa_reading = VFAReading(
        hardware_id=payload.hardware_id,
        field_id=payload.field_id,
        timestamp=datetime.utcnow(),
        location=f"POINT({payload.longitude} {payload.latitude})",
        nitrogen_pressure_psi=payload.nitrogen_pressure_psi,
        slot_10_moisture=payload.slot_10_moisture,
        slot_10_ec=payload.slot_10_ec,
        slot_10_temp=payload.slot_10_temp,
        slot_18_moisture=payload.slot_18_moisture,
        slot_25_moisture=payload.slot_25_moisture,
        slot_25_ec=payload.slot_25_ec,
        slot_25_temp=payload.slot_25_temp,
        slot_35_moisture=payload.slot_35_moisture,
        slot_48_moisture=payload.slot_48_moisture,
        slot_48_ec=payload.slot_48_ec,
        battery_voltage=payload.battery_voltage
    )
    db.add(vfa_reading)
    db.commit()
    
    update_payload = {
        "type": "SENSOR_UPDATE",
        "timestamp": datetime.utcnow().isoformat(),
        "field_id": payload.field_id,
        "data": {
            "device": "VFA",
            "hardware_id": payload.hardware_id,
            "moisture_profile": {
                "10cm": payload.slot_10_moisture,
                "25cm": payload.slot_25_moisture,
                "48cm": payload.slot_48_moisture
            }
        }
    }
    asyncio.create_task(manager.broadcast(update_payload))
    return {"status": "success", "id": str(vfa_reading.id)}

@router.post("/pfa/telemetry", tags=["Hardware Ingestion"])
def ingest_pfa_telemetry(
    payload: PFAReadingCreate,
    db: Session = Depends(get_db)
):
    """Ingests real-time pressure and flow data from a Pressure & Flow Anchor (PFA)."""
    pfa_reading = PFAReading(
        hardware_id=payload.hardware_id,
        field_id=payload.field_id,
        timestamp=datetime.utcnow(),
        well_pressure_psi=payload.well_pressure_psi,
        flow_rate_gpm=payload.flow_rate_gpm,
        pump_status=payload.pump_status,
        current_harmonics=payload.current_harmonics
    )
    db.add(pfa_reading)
    db.commit()
    
    update_payload = {
        "type": "PUMP_UPDATE",
        "timestamp": datetime.utcnow().isoformat(),
        "field_id": payload.field_id,
        "data": {
            "device": "PFA",
            "hardware_id": payload.hardware_id,
            "flow_rate_gpm": payload.flow_rate_gpm,
            "pump_status": payload.pump_status
        }
    }
    asyncio.create_task(manager.broadcast(update_payload))
    return {"status": "success", "id": str(pfa_reading.id)}

@router.post("/pmt/kinematics", tags=["Hardware Ingestion"])
def ingest_pmt_kinematics(
    payload: PMTReadingCreate,
    db: Session = Depends(get_db)
):
    """Ingests real-time location and speed data from a Pivot Motion Tracker (PMT)."""
    pmt_reading = PMTReading(
        hardware_id=payload.hardware_id,
        field_id=payload.field_id,
        timestamp=datetime.utcnow(),
        location=f"POINT({payload.longitude} {payload.latitude})",
        kinematic_angle_deg=payload.kinematic_angle_deg,
        span_speed_mph=payload.span_speed_mph
    )
    db.add(pmt_reading)
    db.commit()
    
    update_payload = {
        "type": "SENSOR_UPDATE",
        "timestamp": datetime.utcnow().isoformat(),
        "field_id": payload.field_id,
        "data": {
            "device": "PMT",
            "hardware_id": payload.hardware_id,
            "kinematic_angle_deg": payload.kinematic_angle_deg,
            "span_speed_mph": payload.span_speed_mph
        }
    }
    asyncio.create_task(manager.broadcast(update_payload))
    return {"status": "success", "id": str(pmt_reading.id)}

@router.post("/lrz/reading", tags=["Hardware Ingestion"])
def ingest_lrz_reading(
    payload: LRZReadingCreate,
    db: Session = Depends(get_db)
):
    """Ingests a dumb-chirp reading from a Lateral Root-Zone Scout (LRZ)."""
    lrz_reading = LRZReading(
        hardware_id=payload.hardware_id,
        field_id=payload.field_id,
        timestamp=datetime.utcnow(),
        location=f"POINT({payload.longitude} {payload.latitude})",
        moisture_surface=payload.moisture_surface,
        moisture_root=payload.moisture_root,
        temp_surface=payload.temp_surface,
        battery_voltage=payload.battery_voltage
    )
    db.add(lrz_reading)
    db.commit()
    
    update_payload = {
        "type": "SENSOR_UPDATE",
        "timestamp": datetime.utcnow().isoformat(),
        "field_id": payload.field_id,
        "data": {
            "device": "LRZ",
            "hardware_id": payload.hardware_id,
            "moisture_surface": payload.moisture_surface,
            "moisture_root": payload.moisture_root
        }
    }
    asyncio.create_task(manager.broadcast(update_payload))
    return {"status": "success", "id": str(lrz_reading.id)}

@router.post("/pmt/ebk_grid", tags=["Hardware Ingestion"])
def ingest_pmt_ebk_grid(
    payload: EBKGridCreate,
    db: Session = Depends(get_db)
):
    """Ingests the 50m EBK probability grid calculated autonomously by the PMT Edge-EBK engine."""
    grid_record = VirtualSensorGrid50m(
        grid_id=f"grid_{payload.hardware_id}_{datetime.utcnow().timestamp()}",
        field_id=payload.field_id,
        timestamp=datetime.utcnow(),
        location=f"POINT({payload.longitude} {payload.latitude})",
        moisture_probability_grid=payload.moisture_probability_grid,
        computation_mode=payload.attention_mode
    )
    db.add(grid_record)
    db.commit()
    
    update_payload = {
        "type": "GRID_UPDATE",
        "timestamp": datetime.utcnow().isoformat(),
        "field_id": payload.field_id,
        "data": {
            "device": "PMT-EBK",
            "hardware_id": payload.hardware_id,
            "attention_mode": payload.attention_mode,
            "grid_resolution_m": payload.grid_resolution_m
        }
    }
    asyncio.create_task(manager.broadcast(update_payload))
    return {"status": "success", "grid_id": grid_record.grid_id}

@router.post("/aerial/multispectral", tags=["Hardware Ingestion"])
def ingest_aerial_multispectral(
    payload: AerialMultispectralCreate,
    db: Session = Depends(get_db)
):
    """Ingests drone multispectral orthomosaics serving as Spatial Priors for the 1m Kriging model."""
    logger.info(f"Ingested {payload.resolution_cm_px}cm/px multispectral tile for field {payload.field_id}")
    return {
        "status": "success", 
        "resolution": payload.resolution_cm_px,
        "action": "prior_updated"
    }
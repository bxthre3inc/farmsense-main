# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import logging
import uuid
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.devices import Device, DeviceType

logger = logging.getLogger(__name__)

class ProvisioningService:
    """
    Manages the "Cradle-to-Field" provisioning sequence for FarmSense nodes.
    Transitioning devices from UNPROVISIONED -> FACTORY_READY -> FIELD_ACTIVE.
    """

    # Valid Serial Prefix for bxthre3 inc. hardware
    BX3_SERIAL_PREFIX = "BX3-2026-"

    @staticmethod
    def validate_serial(serial_number: str) -> bool:
        """
        Validates the hardware serial against the authorized manufacturer pattern.
        """
        return serial_number.startswith(ProvisioningService.BX3_SERIAL_PREFIX)

    @staticmethod
    def auto_register_node(
        db: Session, 
        external_id: str, 
        field_id: str, 
        device_type: DeviceType
    ) -> Device:
        """
        Stage 3/4: Auto-registers a device upon first contact if the serial is valid.
        """
        if not ProvisioningService.validate_serial(external_id):
            logger.warning(f"PROVISIONING: Unauthorized hardware ID attempt: {external_id}")
            raise ValueError("Unauthorized Hardware ID")

        # Check if already exists
        existing = db.query(Device).filter(Device.external_id == external_id).first()
        if existing:
            return existing

        # Create new device record
        new_device = Device(
            external_id=external_id,
            field_id=field_id,
            device_type=device_type,
            status="provisioning",
            config={
                "provisioning_stage": "HELO_RECEIVED",
                "provisioned_at": datetime.now(timezone.utc).isoformat()
            },
            created_at=datetime.now(timezone.utc)
        )
        
        db.add(new_device)
        db.commit()
        db.refresh(new_device)
        
        logger.info(f"PROVISIONING: Node {external_id} auto-registered for field {field_id}")
        return new_device

    @staticmethod
    def generate_provisioning_blob(device: Device) -> Dict[str, Any]:
        """
        Stage 4: Generates the "Boom" configuration blob.
        Injects site-specific deep moats (HVS, JADC2, Mesh).
        """
        # 1. HVS Constants (Simulated for SLV Loamy Sand)
        hvs_constants = {
            "decay_constant": 0.08,
            "clay_binding_ratio": 0.12,
            "texture_nonlinearity": True
        }

        # 2. JADC2 Tactical Keys (Simulated)
        jadc2_keys = {
            "signing_key_id": str(uuid.uuid4())[:8],
            "mesh_id": "SLV-Tactical-A",
            "failover_mode": "autonomous"
        }

        # 3. Frequency Hopping Parity
        hop_parity = hashlib.sha256(device.external_id.encode()).hexdigest()[:8]

        config_blob = {
            "device_id": str(device.id),
            "field_id": device.field_id,
            "hvs_parameters": hvs_constants,
            "jadc2_tactical": jadc2_keys,
            "mesh_params": {
                "hop_parity": hop_parity,
                "tx_power_limit_dbm": 5
            },
            "firmware_update_url": "https://ota.bxthre3.com/latest",
            "status": "FIELD_ACTIVE"
        }

        # Update device status
        device.status = "active"
        device.config = config_blob
        
        logger.info(f"PROVISIONING: Configuration blob pushed to {device.external_id}")
        return config_blob
# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

"""
vri_command_center.py — Hierarchical Zoned VRI Orchestrator

Manages the spatial fidelity hierarchy (1m, 10m/20m, 50m) based on 
field context, attention modes, and hardware availability.
"""

import logging
from typing import List, Any, Dict
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.grid_renderer import GridRenderingService
from app.services.adaptive_recalc import AdaptiveRecalculationEngine, AttentionMode
from app.services.vri_hardware_gateway import VRIHardwareGateway
from app.models import VirtualSensorGrid50m, VirtualSensorGrid20m, VirtualSensorGrid1m, RecalculationLog

logger = logging.getLogger(__name__)

class VRICommandCenter:
    @staticmethod
    def get_best_available_resolution(db: Session, field_id: str) -> str:
        """
        Determines the optimal resolution for the current field state.
        BAR (Best Available Resolution) logic.
        """
        # 1. Check current attention mode from the latest RecalculationLog
        latest_log = db.query(RecalculationLog).filter(
            RecalculationLog.field_id == field_id
        ).order_by(RecalculationLog.timestamp.desc()).first()
        
        if not latest_log:
            current_mode = AttentionMode.DORMANT
        else:
            # Map string back to AttentionMode enum
            try:
                current_mode = AttentionMode(latest_log.new_mode)
            except ValueError:
                current_mode = AttentionMode.DORMANT
        
        # 2. Logic for BAR
        # Collapse mode (emergency/high-action) -> Prefers 1m if possible, or 10m/20m
        # Anticipatory mode (pivot moving) -> 20m
        # Dormant mode -> 50m is sufficient
        
        if current_mode == AttentionMode.COLLAPSE:
            return "1m"
        elif current_mode == AttentionMode.ANTICIPATORY:
            return "20m"
        else:
            return "50m"

    @staticmethod
    def fetch_vri_grid(db: Session, field_id: str, requested_res: str = None) -> List[Any]:
        """
        Returns grid data at the Best Available Resolution (BAR).
        """
        if requested_res is None:
            resolution = VRICommandCenter.get_best_available_resolution(db, field_id)
        else:
            resolution = requested_res
            
        logger.info(f"VRICommandCenter: Delivering {resolution} resolution for field {field_id}")
        
        return GridRenderingService.get_or_render_grid(db, field_id, resolution)

    @staticmethod
    def dispatch_prescription(db: Session, field_id: str) -> Dict[str, Any]:
        """
        Fetches the latest high-res 1m grid and dispatches it to the hardware gateway.
        """
        # 1. Fetch the 1m grid with predictive mode (to proactive optimize)
        grid = GridRenderingService.get_or_render_grid(db, field_id, "1m", predictive_mode=True)
        
        # 2. Extract prescriptions (the grid objects now have enriched attributes from phase 2)
        prescriptions = []
        for point in grid:
            prescriptions.append({
                "grid_id": point.grid_id,
                "vri_nozzle_setting": getattr(point, 'vri_nozzle_setting', 1.0)
            })
            
        # 3. Dispatch to Hardware
        hw_response = VRIHardwareGateway.dispatch_commands(field_id, prescriptions)
        
        logger.info(f"VRICommandCenter: Dispatch successful. Hardware Result: {hw_response['status']}")
        return hw_response
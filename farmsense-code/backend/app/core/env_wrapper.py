# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import os
import logging
from enum import Enum
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FarmSenseMode(Enum):
    DEVELOPMENT = "dev"
    PILOT = "pilot"
    PRODUCTION = "prod"

class PlatformEnvironmentWrapper:
    """
    Unified environment wrapper for FarmSense.
    Bridges the gap between local development, pilot-stage field trials,
    and full institutional production.
    """

    def __init__(self, mode: str = None):
        try:
            self.mode = FarmSenseMode(mode or os.getenv("FARMSENSE_MODE", "dev"))
        except ValueError:
            logger.warning(f"Invalid FARMSENSE_MODE '{mode}'. Defaulting to DEVELOPMENT.")
            self.mode = FarmSenseMode.DEVELOPMENT
        
        logger.info(f"PLATFORM WRAPPER: Initialized in {self.mode.value.upper()} mode.")

    def get_service_config(self, service_name: str) -> Dict[str, Any]:
        """
        Returns environment-specific configurations for services.
        """
        config_matrix = {
            "satellite": {
                FarmSenseMode.DEVELOPMENT: {"provider": "Sentinel-Public", "reliability": 0.3},
                FarmSenseMode.PILOT: {"provider": "Sentinel-Public", "reliability": 0.8},
                FarmSenseMode.PRODUCTION: {"provider": "Planet-HighRes", "reliability": 0.98}
            },
            "sensors": {
                FarmSenseMode.DEVELOPMENT: {"stream": "MeshRelay-Geofenced", "audit": False},
                FarmSenseMode.PILOT: {"stream": "MeshRelay-Geofenced", "audit": True},
                FarmSenseMode.PRODUCTION: {"stream": "FullMesh-Institutional", "audit": True}
            },
            "decision_engine": {
                FarmSenseMode.DEVELOPMENT: {"explainability": "Verified", "auto_execute": False},
                FarmSenseMode.PILOT: {"explainability": "Verified", "auto_execute": False},
                FarmSenseMode.PRODUCTION: {"explainability": "Signed", "auto_execute": True}
            }
        }
        return config_matrix.get(service_name, {}).get(self.mode, {})

    def is_pilot(self) -> bool:
        return self.mode == FarmSenseMode.PILOT

    def is_production(self) -> bool:
        return self.mode == FarmSenseMode.PRODUCTION

    def wrap_data_stream(self, data: Any):
        """
        Wraps incoming technical data with environment metadata/safety flags.
        """
        return {
            "payload": data,
            "metadata": {
                "origin_env": self.mode.value,
                "institutional_grade": self.is_production(),
                "pilot_verification": self.is_pilot()
            }
        }

# Global singleton for dependency injection
platform_wrapper = PlatformEnvironmentWrapper()
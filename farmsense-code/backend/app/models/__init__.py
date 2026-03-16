# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from .telemetry import (
    SoilSensorReading, PumpTelemetry, WeatherData,
    HardwareModel, HardwareNode, LRZReading, VFAReading,
    PFAReading, PMTReading
)
from .grids import (
    VirtualSensorGrid50m, VirtualSensorGrid20m,
    VirtualSensorGrid10m, VirtualSensorGrid1m
)
from .audit import (
    AuditLog, RecalculationLog, ComplianceReport,
    AnonymizedResearchArchive
)

__all__ = [
    "SoilSensorReading",
    "PumpTelemetry",
    "WeatherData",
    "HardwareModel",
    "HardwareNode",
    "LRZReading",
    "VFAReading",
    "PFAReading",
    "PMTReading",
    "VirtualSensorGrid50m",
    "VirtualSensorGrid20m",
    "VirtualSensorGrid10m",
    "VirtualSensorGrid1m",
    "AuditLog",
    "RecalculationLog",
    "ComplianceReport",
    "AnonymizedResearchArchive",
]
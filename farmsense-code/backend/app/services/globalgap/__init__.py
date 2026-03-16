# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from .engine import GAPComplianceEngine
from .models import GAP_FieldInputs, GAP_Report, ControlPointResult
from .constants import NCLevel, ControlPointID, CONTROL_POINT_DESCRIPTIONS

gap_engine = GAPComplianceEngine()

__all__ = [
    "GAPComplianceEngine",
    "GAP_FieldInputs",
    "GAP_Report",
    "ControlPointResult",
    "NCLevel",
    "ControlPointID",
    "CONTROL_POINT_DESCRIPTIONS",
    "gap_engine",
]
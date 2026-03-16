# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from enum import Enum

class NCLevel(str, Enum):
    PASS        = "pass"
    MINOR_NC    = "minor_nc"      # Minor non-conformance: corrective action required
    MAJOR_NC    = "major_nc"      # Major: suspension risk
    CRITICAL_NC = "critical_nc"   # Critical: immediate suspension


class ControlPointID(str, Enum):
    AF_1_2 = "AF_1.2"   # Site history & risk assessment
    CB_5_2 = "CB_5.2"   # Irrigation water source documentation
    CB_5_3 = "CB_5.3"   # Application method (drip, flood, etc.)
    CB_5_5 = "CB_5.5"   # Water quality monitoring (EC, pH, microbio)
    FV_5_1 = "FV_5.1"   # Water efficiency targets and achievement
    AG5_2  = "AG_5.2"   # Water metering, volumetric reporting


CONTROL_POINT_DESCRIPTIONS = {
    ControlPointID.AF_1_2: "Site History & Risk Assessment",
    ControlPointID.CB_5_2: "Irrigation Water Source Documentation",
    ControlPointID.CB_5_3: "Irrigation Application Method",
    ControlPointID.CB_5_5: "Irrigation Water Quality Monitoring",
    ControlPointID.FV_5_1: "Water Efficiency Targets & Achievement",
    ControlPointID.AG5_2:  "Water Metering & Volumetric Reporting",
}

# Weights for overall certification score (must sum to 1.0)
CONTROL_POINT_WEIGHTS = {
    ControlPointID.AF_1_2: 0.10,
    ControlPointID.CB_5_2: 0.15,
    ControlPointID.CB_5_3: 0.15,
    ControlPointID.CB_5_5: 0.25,
    ControlPointID.FV_5_1: 0.20,
    ControlPointID.AG5_2:  0.15,
}
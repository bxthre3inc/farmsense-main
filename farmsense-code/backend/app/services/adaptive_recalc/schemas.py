# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class AttentionMode(Enum):
    """Operational modes governed by Fisherman's Attention"""
    DORMANT = "dormant"             # 4 hour intervals
    ANTICIPATORY = "anticipatory"   # 60 minute intervals
    RIPPLE = "ripple"               # 15 minute intervals
    COLLAPSE = "collapse"           # 1 minute intervals


@dataclass
class FieldCondition:
    """Current field state for decision making"""
    field_id: str
    current_mode: AttentionMode
    last_recalc: datetime
    
    # Moisture metrics
    avg_moisture_surface: float
    avg_moisture_root: float
    moisture_std_dev: float
    moisture_trend_1h: float  # % change per hour
    moisture_trend_6h: float
    
    # Environmental
    current_temp: float
    et0_rate: float  # mm/day
    rainfall_last_1h: float
    rainfall_forecast_6h: float
    wind_speed: float
    
    # Operational
    pumps_running: int
    irrigation_active: bool
    sensor_coverage_pct: float
    
    # Events
    sensor_anomalies: List[Dict]
    extreme_weather_alerts: List[Dict]


@dataclass
class RecalcDecision:
    """Output of decision engine"""
    should_recalculate: bool
    new_mode: AttentionMode
    reason: str
    next_scheduled: datetime
    priority: int  # 1-5, higher = more urgent
    trigger_type: str
# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock
from app.services.adaptive_recalc import (
    AdaptiveRecalculationEngine, 
    FieldCondition, 
    AttentionMode, 
    RecalcDecision
)

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def engine(mock_db):
    return AdaptiveRecalculationEngine(mock_db)

@pytest.fixture
def stable_condition():
    return FieldCondition(
        field_id="field_001",
        current_mode=AttentionMode.DORMANT,
        last_recalc=datetime.now(timezone.utc) - timedelta(hours=1),
        avg_moisture_surface=0.30,
        avg_moisture_root=0.30,
        moisture_std_dev=0.02,
        moisture_trend_1h=0.0,
        moisture_trend_6h=0.0,
        current_temp=25.0,
        et0_rate=2.0,
        rainfall_last_1h=0.0,
        rainfall_forecast_6h=0.0,
        wind_speed=2.0,
        pumps_running=0,
        irrigation_active=False,
        sensor_coverage_pct=100.0,
        sensor_anomalies=[],
        extreme_weather_alerts=[]
    )

def test_stable_conditions_no_recalc(engine, stable_condition):
    """Stable conditions should stay in DORMANT mode and not trigger recalc within 4h."""
    decision = engine.evaluate_field(stable_condition)
    assert decision.should_recalculate is False
    assert decision.new_mode == AttentionMode.DORMANT

def test_critical_moisture_drop_triggers_collapse(engine, stable_condition):
    """Rapid moisture drop (>30% in 6h) should trigger immediate COLLAPSE (1 min)."""
    stable_condition.moisture_trend_6h = -35.0
    decision = engine.evaluate_field(stable_condition)
    
    assert decision.should_recalculate is True
    assert decision.new_mode == AttentionMode.COLLAPSE
    assert "Critical moisture drop" in decision.reason
    assert decision.priority == 5

def test_pump_failure_triggers_collapse(engine, stable_condition):
    """Pump stops during active irrigation should trigger COLLAPSE."""
    stable_condition.irrigation_active = True
    stable_condition.pumps_running = 0
    decision = engine.evaluate_field(stable_condition)
    
    assert decision.should_recalculate is True
    assert decision.new_mode == AttentionMode.COLLAPSE
    assert "Pump failure" in decision.reason

def test_rainfall_event_triggers_ripple(engine, stable_condition):
    """Significant rainfall triggers out-of-turn RIPPLE mode (15 min)."""
    stable_condition.rainfall_last_1h = 15.0 # > 10mm threshold
    decision = engine.evaluate_field(stable_condition)
    
    assert decision.should_recalculate is True
    assert decision.new_mode == AttentionMode.RIPPLE
    assert "Rainfall event" in decision.reason

def test_active_irrigation_mode_transition(engine, stable_condition):
    """Active irrigation should transition from DORMANT to ANTICIPATORY/COLLAPSE."""
    stable_condition.irrigation_active = True
    stable_condition.moisture_trend_1h = 2.5 # > 2.0 volatility threshold
    
    # Evaluate mode determination
    mode = engine._determine_mode(stable_condition)
    assert mode in [AttentionMode.ANTICIPATORY, AttentionMode.COLLAPSE]

def test_scheduled_recalc_due(engine, stable_condition):
    """If last_recalc is older than mode interval, should_recalculate should be True."""
    # DORMANT interval is 4h
    stable_condition.last_recalc = datetime.now(timezone.utc) - timedelta(hours=5)
    decision = engine.evaluate_field(stable_condition)
    
    assert decision.should_recalculate is True
    assert decision.trigger_type == 'scheduled'
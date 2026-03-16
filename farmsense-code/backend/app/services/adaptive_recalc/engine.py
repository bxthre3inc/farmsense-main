# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Tuple, Optional
from sqlalchemy.orm import Session
from .schemas import AttentionMode, FieldCondition, RecalcDecision

class AdaptiveRecalculationEngine:
    """
    Judgment-based recalculation engine using trend analysis
    and configurable thresholds
    """
    
    # Configurable thresholds (per crop type, can be overridden)
    DEFAULT_THRESHOLDS = {
        'moisture_stable_band': 0.05,      # ±5% is stable
        'moisture_active_threshold': 0.15,  # >15% = active
        'moisture_critical_threshold': 0.30, # >30% = critical
        'trend_volatile_threshold': 2.0,    # >2%/hr = volatile
        'temp_stress_threshold': 35.0,      # >35°C = heat stress
        'rainfall_event_threshold': 10.0,   # >10mm = significant
        'wind_stress_threshold': 8.0,       # >8 m/s = high wind
        'et0_high_threshold': 8.0,          # >8mm/day = high ET
    }
    
    def __init__(self, db_session: Session, config: Optional[Dict] = None):
        self.db = db_session
        self.thresholds = {**self.DEFAULT_THRESHOLDS, **(config or {})}
    
    def evaluate_field(self, condition: FieldCondition) -> RecalcDecision:
        """
        Main decision logic: determine if and when to recalculate
        """
        critical_check = self._check_critical_events(condition)
        if critical_check:
            return critical_check
        
        oot_check = self._check_out_of_turn_triggers(condition)
        if oot_check:
            return oot_check
        
        new_mode = self._determine_mode(condition)
        
        time_since_last = datetime.now(timezone.utc) - condition.last_recalc
        is_due, next_scheduled = self._is_recalc_due(
            condition.current_mode, 
            new_mode, 
            time_since_last
        )
        
        if is_due:
            reason = self._generate_reason(condition, new_mode)
            return RecalcDecision(
                should_recalculate=True,
                new_mode=new_mode,
                reason=reason,
                next_scheduled=next_scheduled,
                priority=self._calculate_priority(new_mode, condition),
                trigger_type='scheduled'
            )
        
        return RecalcDecision(
            should_recalculate=False,
            new_mode=condition.current_mode,
            reason="Next scheduled recalculation not due",
            next_scheduled=next_scheduled,
            priority=1,
            trigger_type='none'
        )
    
    def _check_critical_events(self, condition: FieldCondition) -> Optional[RecalcDecision]:
        reasons = []
        if condition.moisture_trend_6h < -self.thresholds['moisture_critical_threshold']:
            reasons.append(f"Critical moisture drop: {condition.moisture_trend_6h:.1f}% in 6h")
        if (condition.current_temp > self.thresholds['temp_stress_threshold'] and 
            condition.avg_moisture_surface < 0.20):
            reasons.append(f"Heat stress event: {condition.current_temp}°C with low moisture")
        if condition.irrigation_active and condition.pumps_running == 0:
            reasons.append("Pump failure during active irrigation")
        if condition.sensor_coverage_pct < 50.0:
            reasons.append(f"Low sensor coverage: {condition.sensor_coverage_pct:.1f}%")
        
        if reasons:
            return RecalcDecision(
                should_recalculate=True,
                new_mode=AttentionMode.COLLAPSE,
                reason=" | ".join(reasons),
                next_scheduled=datetime.now(timezone.utc) + timedelta(minutes=1),
                priority=5,
                trigger_type='critical_event'
            )
        return None
    
    def _check_out_of_turn_triggers(self, condition: FieldCondition) -> Optional[RecalcDecision]:
        reasons = []
        if condition.sensor_anomalies:
            reasons.append(f"{len(condition.sensor_anomalies)} sensor anomalies detected")
        if condition.rainfall_last_1h > self.thresholds['rainfall_event_threshold']:
            reasons.append(f"Rainfall event: {condition.rainfall_last_1h:.1f}mm in 1h")
        if condition.extreme_weather_alerts:
            alert_types = [a['type'] for a in condition.extreme_weather_alerts]
            reasons.append(f"Weather alerts: {', '.join(alert_types)}")
        if (condition.et0_rate > self.thresholds['et0_high_threshold'] and 
            condition.irrigation_active):
            reasons.append(f"High ET rate: {condition.et0_rate:.1f}mm/day during irrigation")
        
        if reasons:
            return RecalcDecision(
                should_recalculate=True,
                new_mode=AttentionMode.RIPPLE,
                reason=" | ".join(reasons),
                next_scheduled=datetime.now(timezone.utc) + timedelta(minutes=15),
                priority=4,
                trigger_type='out_of_turn_event'
            )
        return None
    
    def _determine_mode(self, condition: FieldCondition) -> AttentionMode:
        volatility_factors = []
        if abs(condition.moisture_trend_1h) > self.thresholds['trend_volatile_threshold']:
            volatility_factors.append(0.4)
        elif abs(condition.moisture_trend_1h) > self.thresholds['moisture_active_threshold']:
            volatility_factors.append(0.2)
        if condition.moisture_std_dev > 0.15:
            volatility_factors.append(0.3)
        if condition.irrigation_active:
            volatility_factors.append(0.3)
        if condition.et0_rate > self.thresholds['et0_high_threshold']:
            volatility_factors.append(0.2)
        if condition.wind_speed > self.thresholds['wind_stress_threshold']:
            volatility_factors.append(0.2)
        if condition.rainfall_forecast_6h > self.thresholds['rainfall_event_threshold']:
            volatility_factors.append(0.3)
        
        volatility_score = min(sum(volatility_factors), 1.0)
        if volatility_score > 0.7:
            return AttentionMode.COLLAPSE
        elif volatility_score > 0.3:
            return AttentionMode.ANTICIPATORY
        return AttentionMode.DORMANT
    
    def _is_recalc_due(
        self, 
        current_mode: AttentionMode, 
        new_mode: AttentionMode,
        time_since_last: timedelta
    ) -> Tuple[bool, datetime]:
        mode_intervals = {
            AttentionMode.DORMANT: timedelta(hours=4),
            AttentionMode.ANTICIPATORY: timedelta(minutes=60),
            AttentionMode.RIPPLE: timedelta(minutes=15),
            AttentionMode.COLLAPSE: timedelta(minutes=1),
        }
        interval = min(
            mode_intervals.get(current_mode, timedelta(hours=4)),
            mode_intervals.get(new_mode, timedelta(hours=4))
        )
        is_due = time_since_last >= interval
        next_scheduled = datetime.now(timezone.utc) + interval
        return is_due, next_scheduled
    
    def _calculate_priority(self, mode: AttentionMode, condition: FieldCondition) -> int:
        priority_map = {
            AttentionMode.DORMANT: 1,
            AttentionMode.ANTICIPATORY: 2,
            AttentionMode.RIPPLE: 3,
            AttentionMode.COLLAPSE: 5,
        }
        base_priority = priority_map[mode]
        if condition.avg_moisture_surface < 0.15:
            base_priority = min(base_priority + 1, 5)
        return base_priority
    
    def _generate_reason(self, condition: FieldCondition, new_mode: AttentionMode) -> str:
        reasons = [f"Mode: {new_mode.value}"]
        if new_mode == AttentionMode.COLLAPSE:
            reasons.append("High volatility detected")
            if condition.irrigation_active:
                reasons.append("Active irrigation")
        elif new_mode == AttentionMode.ANTICIPATORY:
            if condition.irrigation_active:
                reasons.append("Irrigation in progress")
            reasons.append(f"Moisture trend: {condition.moisture_trend_1h:+.1f}%/h")
        else:
            reasons.append("Stable conditions")
        if condition.et0_rate > 6.0:
            reasons.append(f"ET0: {condition.et0_rate:.1f}mm/day")
        return " | ".join(reasons)
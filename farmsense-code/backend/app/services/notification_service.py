# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.


from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import SoilSensorReading
from enum import Enum

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class NotificationService:
    @staticmethod
    def evaluate_reading(reading: SoilSensorReading, db: Session):
        """Evaluates a sensor reading for potential alerts"""
        # Thresholds (Mock)
        CRITICAL_MOISTURE = 0.10
        WARNING_MOISTURE = 0.18
        
        alerts = []
        
        if reading.moisture_surface < CRITICAL_MOISTURE:
            alerts.append({
                "severity": AlertSeverity.CRITICAL,
                "msg": f"Critical Moisture Level: {reading.moisture_surface*100}% on Sensor {reading.sensor_id}",
                "field_id": reading.field_id
            })
        elif reading.moisture_surface < WARNING_MOISTURE:
            alerts.append({
                "severity": AlertSeverity.WARNING,
                "msg": f"Low Moisture Warning: {reading.moisture_surface*100}% on Sensor {reading.sensor_id}",
                "field_id": reading.field_id
            })
            
        for alert in alerts:
            NotificationService.send_alert(alert)

    @staticmethod
    def send_alert(alert: dict):
        """Simulates sending an alert (email/SMS/In-app)"""
        timestamp = datetime.utcnow().isoformat()
        print(f"[{timestamp}] ALERT [{alert['severity'].value.upper()}] for field {alert['field_id']}: {alert['msg']}")
        # In a real app, this would push to a message queue or Firebase/OneSignal
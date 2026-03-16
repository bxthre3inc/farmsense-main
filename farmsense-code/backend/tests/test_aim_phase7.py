# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.


import unittest
from datetime import datetime, timedelta
from app.services.extended_forecasting_service import ExtendedForecastingService
from app.services.autonomous_irrigation_service import AutonomousIrrigationService

class TestAIMPhase7(unittest.TestCase):
    def setUp(self):
        self.forecast_svc = ExtendedForecastingService()
        self.aim_svc = AutonomousIrrigationService()
        self.mock_profile = [{'depth_in': 10, 'moisture': 0.35}, {'depth_in': 18, 'moisture': 0.38}]

    def test_14d_outlook_generation(self):
        outlook = self.forecast_svc.get_14_day_outlook(self.mock_profile, 0.8, 0.0)
        self.assertEqual(len(outlook), 14)
        # Verify moisture decay
        self.assertLess(outlook[-1]['avg_moisture'], outlook[0]['avg_moisture'])
        # Verify yield impact
        self.assertLess(outlook[-1]['yield_forecast_kgha'], outlook[0]['yield_forecast_kgha'])

    def test_autonomous_fleet_scheduling(self):
        fleet_data = {
            'FIELD_ALPHA': [
                {'moisture_surface': 0.2, 'ndvi': 0.7, 'ndwi': -0.1, 'source_sensors': self.mock_profile}
            ],
            'FIELD_BETA': [
                {'moisture_surface': 0.1, 'ndvi': 0.4, 'ndwi': -0.4, 'source_sensors': self.mock_profile}
            ]
        }
        
        result = self.aim_svc.evaluate_fleet_scheduling(fleet_data)
        dispatches = result['fleet_dispatches']
        
        # Verify both fields are handled
        self.assertIn('FIELD_ALPHA', dispatches)
        self.assertIn('FIELD_BETA', dispatches)
        
        # BETA should be higher priority due to lower moisture/spectral indexes
        self.assertEqual(dispatches['FIELD_BETA']['status'], 'SCHEDULED')
        self.assertGreater(dispatches['FIELD_BETA']['estimated_gallons'], 0)

    def test_quota_throttling(self):
        # Set a very low quota to trigger throttling
        self.aim_svc.GLOBAL_SLV_DAILY_QUOTA_GALLONS = 100
        
        fleet_data = {
            'FIELD_DRY': [{'moisture_surface': 0.1, 'ndvi': 0.4, 'ndwi': -0.4}]
        }
        
        result = self.aim_svc.evaluate_fleet_scheduling(fleet_data)
        self.assertEqual(result['fleet_dispatches']['FIELD_DRY']['status'], 'THROTTLED')
        self.assertIn("Quota Exceeded", result['fleet_dispatches']['FIELD_DRY']['reason'])

if __name__ == '__main__':
    unittest.main()
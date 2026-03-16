# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import unittest
from app.services.autonomous_irrigation_service import AutonomousIrrigationService

class TestMultiSourceWater(unittest.TestCase):
    def setUp(self):
        self.service = AutonomousIrrigationService()
        # Mock grid data for two fields
        self.mock_fleet_data = {
            "FIELD_LARIAT": [
                {"moisture_surface": 0.2, "ndvi": 0.6, "ndwi": 0.0, "computation_mode": "BASE"}
            ],
            "FIELD_WELL_ONLY": [
                {"moisture_surface": 0.2, "ndvi": 0.6, "ndwi": 0.0, "computation_mode": "BASE"}
            ]
        }
        
    def test_source_prioritization(self):
        # Configure allocations: LARIAT uses DITCH (High Priority/Low Num), WELL_ONLY uses WELL (Low Priority/High Num)
        allocations = {
            "FIELD_LARIAT": {
                "source_type": "ditch",
                "source_name": "Lariat Ditch",
                "priority": 1.0 # Senior
            },
            "FIELD_WELL_ONLY": {
                "source_type": "well",
                "source_name": "Deep Aquifer",
                "priority": 5.0 # Junior
            }
        }
        self.service.update_fleet_allocations(allocations)
        
        # Evaluate scheduling
        # Both fields have same stress, so tie-break should go to the Senior Water Right (LARIAT)
        results = self.service.evaluate_fleet_scheduling(self.mock_fleet_data)
        
        dispatches = results['fleet_dispatches']
        self.assertIn("FIELD_LARIAT", dispatches)
        self.assertIn("FIELD_WELL_ONLY", dispatches)
        
        # Verify source tracking in reasons
        self.assertIn("Source: ditch", dispatches['FIELD_LARIAT']['reason'])
        self.assertIn("Source: well", dispatches['FIELD_WELL_ONLY']['reason'])
        
        # If we had a tight quota, LARIAT should be SCHEDULED and WELL_ONLY might be THROTTLED
        # Given both have same stress, if we sort correctly, LARIAT is "more" prioritized
        # The logic sorts by (max_stress, -priority_score) reverse.
        # So (0.3, -1.0) vs (0.3, -5.0) -> (0.3, -1.0) is greater, so LARIAT comes first.
        
if __name__ == '__main__':
    unittest.main()
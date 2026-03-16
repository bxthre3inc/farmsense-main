# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.


import unittest
import numpy as np
from app.services.vri_prescription_service import VRIPrescriptionService

class TestVRIPrescription(unittest.TestCase):
    def setUp(self):
        self.service = VRIPrescriptionService()
        self.grid_data = [
            {'moisture_surface': 0.20, 'lat': 40.0, 'lon': -105.0}, # High deficit
            {'moisture_surface': 0.35, 'lat': 40.1, 'lon': -105.1}, # No deficit
            {'moisture_surface': 0.40, 'lat': 39.9, 'lon': -104.9}  # Surplus
        ]

    def test_prescription_generation(self):
        prescriptions = self.service.generate_prescription(self.grid_data, target_moisture=0.35)
        
        # Point 1 (0.20 moisture) should have a high nozzle setting (adjustment > 1.0)
        self.assertGreater(prescriptions[0]['vri_nozzle_setting'], 1.0)
        
        # Point 2 (0.35 moisture) should have base flow (1.0)
        self.assertAlmostEqual(prescriptions[1]['vri_nozzle_setting'], 1.0)

        # Point 3 (0.40 moisture) should also have base flow (min flow 1.0 in this simple logic)
        # Actually our logic: adjustment = 1.0 + (deficit * 3.0), deficit = max(0, target - current)
        # So it should be 1.0
        self.assertAlmostEqual(prescriptions[2]['vri_nozzle_setting'], 1.0)

    def test_efficiency_gain(self):
        prescriptions = [
            {'vri_nozzle_setting': 0.8},
            {'vri_nozzle_setting': 0.8},
            {'vri_nozzle_setting': 0.8}
        ]
        metrics = self.service.calculate_efficiency_gain(prescriptions)
        
        # (1.0 - 0.8) * 100 = 20% savings
        self.assertAlmostEqual(metrics['estimated_water_savings_pct'], 20.0)

if __name__ == '__main__':
    unittest.main()
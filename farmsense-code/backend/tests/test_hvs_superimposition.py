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
from app.services.hvs_sync_service import HVSSyncService

class TestHVSSync(unittest.TestCase):
    def setUp(self):
        self.svc = HVSSyncService()
        self.mock_vfa = {
            'slot_10_moisture': 0.30,
            'slot_18_moisture': 0.36, # Ratio = 1.2
            'slot_25_moisture': 0.45, # Ratio = 1.5
            'slot_35_moisture': 0.30, # Ratio = 1.0
            'slot_48_moisture': 0.15  # Ratio = 0.5
        }

    def test_same_zone_superimposition(self):
        lrz_reading = {'moisture_surface': 0.20}
        profile = self.svc.superimpose_profile(lrz_reading, self.mock_vfa, "ZONE_A", "ZONE_A")
        
        # 18in should be 0.20 * 1.2 * 1.0 (base) * 0.97 (non-linear modifier for 0.20 surface)
        # Modifier = 0.85 + (0.20/0.25)*0.15 = 0.97
        # Expected: 0.20 * 1.2 * 0.97 = 0.2328
        self.assertAlmostEqual(profile[1]['moisture'], 0.2328)
        self.assertEqual(profile[1]['depth_in'], 18)
        self.assertIn("VFA_ANCHORED", profile[1]['source'])

    def test_cross_zone_offset_superimposition(self):
        lrz_reading = {'moisture_surface': 0.20}
        # ZONE_A to ZONE_B offset for 18in is 0.80
        profile = self.svc.superimpose_profile(lrz_reading, self.mock_vfa, "ZONE_B", "ZONE_A")
        
        # 18in should be 0.20 * 1.2 * 0.80 (offset) * 0.97 (non-linear modifier)
        # Expected: 0.20 * 1.2 * 0.80 * 0.97 = 0.18624
        self.assertAlmostEqual(profile[1]['moisture'], 0.18624)
        self.assertIn("ZONE_A_TO_ZONE_B", profile[1]['source'])

    def test_unit_normalization_indices(self):
        lrz_reading = {'moisture_surface': 0.20}
        profile = self.svc.superimpose_profile(lrz_reading, self.mock_vfa)
        depths = [p['depth_in'] for p in profile]
        self.assertEqual(depths, [10, 18, 25, 35, 48])

if __name__ == '__main__':
    unittest.main()
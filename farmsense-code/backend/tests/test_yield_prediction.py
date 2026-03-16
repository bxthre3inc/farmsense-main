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
from app.services.yield_prediction_service import YieldPredictionService

class TestYieldPrediction(unittest.TestCase):
    def setUp(self):
        self.svc = YieldPredictionService()
        self.mock_profile = [
            {'depth_in': 10, 'moisture': 0.30},
            {'depth_in': 18, 'moisture': 0.32},
            {'depth_in': 25, 'moisture': 0.35}
        ]

    def test_optimal_conditions(self):
        # Optimal moisture (avg 0.32), optimal NDVI (0.85), low stress (ndwi 0)
        result = self.svc.calculate_yield(self.mock_profile, 0.85, 0.0)
        
        # Predicted yield should be near the peak (BASE * GDD_MOD)
        # GDD_MOD at default 1200 / 1500 = 0.8
        self.assertGreater(result['yield_forecast_kgha'], 9000)
        self.assertLess(result['crop_stress_probability'], 0.1)

    def test_drought_stress(self):
        dry_profile = [
            {'depth_in': 10, 'moisture': 0.15},
            {'depth_in': 18, 'moisture': 0.18},
            {'depth_in': 25, 'moisture': 0.20}
        ]
        # Low NDVI, high NDWI (water deficit)
        result = self.svc.calculate_yield(dry_profile, 0.40, -0.2)
        
        self.assertLess(result['yield_forecast_kgha'], 6000)
        self.assertGreater(result['crop_stress_probability'], 0.4)

    def test_batch_prediction(self):
        grid = [
            {'moisture_surface': 0.3, 'ndvi': 0.7, 'ndwi': 0.05, 'computation_mode': 'BASE'},
            {'moisture_surface': 0.1, 'ndvi': 0.3, 'ndwi': -0.3, 'computation_mode': 'BASE'}
        ]
        processed = self.svc.batch_predict_grid(grid)
        self.assertEqual(len(processed), 2)
        self.assertIn('MSF_YIELD', processed[0]['computation_mode'])
        self.assertGreater(processed[0]['yield_forecast_kgha'], processed[1]['yield_forecast_kgha'])

if __name__ == '__main__':
    unittest.main()
# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.


import logging
from typing import List, Dict, Any, Optional
import numpy as np

logger = logging.getLogger(__name__)

class YieldPredictionService:
    """
    Multi-Spectral Fusion (MSF) & Yield Prediction Service.
    Fuses soil moisture (HVS-synced), multispectral trends (NDVI/NDWI), 
    and environmental factors to forecast harvest yield.
    """
    
    def __init__(self):
        # Base yield constants (e.g. for Corn in Colorado)
        self.BASE_YIELD_KG_HA = 12000.0
        self.MOISTURE_OPTIMAL_RANGE = (0.25, 0.35)
        self.NDVI_OPTIMAL = 0.85

    def calculate_yield(
        self, 
        moisture_profile: List[Dict[str, Any]], 
        ndvi: float, 
        ndwi: float,
        growing_degree_days: float = 1200.0
    ) -> Dict[str, Any]:
        """
        Hyper-local yield forecasting algorithm.
        """
        # 1. Soil Moisture Modifier (Root-zone focused)
        # Use average of top 25 inches as the primary yield driver
        root_depths = [p['moisture'] for p in moisture_profile if p['depth_in'] <= 25]
        avg_root_moisture = np.mean(root_depths) if root_depths else 0.2
        
        moisture_mod = 1.0
        if avg_root_moisture < self.MOISTURE_OPTIMAL_RANGE[0]:
            moisture_mod = 0.7 + (avg_root_moisture / self.MOISTURE_OPTIMAL_RANGE[0]) * 0.3
        elif avg_root_moisture > self.MOISTURE_OPTIMAL_RANGE[1]:
            moisture_mod = 0.9 # Minor reduction for saturation
            
        # 2. Spectral (NDVI/NDWI) Modifier
        # NDVI reflects biomass; NDWI reflects current water stress
        spectral_mod = (ndvi / self.NDVI_OPTIMAL) * (1.0 + ndwi)
        spectral_mod = np.clip(spectral_mod, 0.5, 1.2)
        
        # 3. Environmental (GDD) Modifier
        gdd_mod = np.clip(growing_degree_days / 1500.0, 0.8, 1.1)
        
        # Final Calculation
        forecasted_yield = self.BASE_YIELD_KG_HA * moisture_mod * spectral_mod * gdd_mod
        
        # Crop Stress Probability (Non-linear sensitivity to moisture and NDWI deficit)
        moisture_deficit = max(0.0, self.MOISTURE_OPTIMAL_RANGE[0] - avg_root_moisture) / self.MOISTURE_OPTIMAL_RANGE[0]
        spectral_deficit = max(0.0, -ndwi)
        
        # Non-linear scaling: stress increases rapidly as moisture drops
        stress_prob = (moisture_deficit ** 0.5 * 0.75) + (spectral_deficit * 0.25)
        stress_prob = np.clip(stress_prob, 0.0, 1.0)
        
        return {
            "yield_forecast_kgha": float(forecasted_yield),
            "crop_stress_probability": float(stress_prob),
            "modifiers": {
                "moisture": float(moisture_mod),
                "spectral": float(spectral_mod),
                "environmental": float(gdd_mod)
            },
            "timestamp": "2026-03-10T10:45:59Z"
        }

    def batch_predict_grid(self, grid_points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Processes an entire 1m grid for yield forecasting.
        """
        logger.info(f"MSF: Running yield prediction for {len(grid_points)} grid cells.")
        for p in grid_points:
            # Extract profile if available from HVS sync
            profile = p.get('source_sensors', []) # source_sensors stores the vertical_profile in 1m grid
            if not isinstance(profile, list):
                profile = [{"depth_in": 10, "moisture": p.get('moisture_surface', 0.2)}]
            
            # Use current NDVI/NDWI from the grid point
            ndvi = p.get('ndvi', 0.6)
            ndwi = p.get('ndwi', 0.1)
            
            prediction = self.calculate_yield(profile, ndvi, ndwi)
            p['yield_forecast_kgha'] = prediction['yield_forecast_kgha']
            p['crop_stress_probability'] = prediction['crop_stress_probability']
            p['computation_mode'] += "_MSF_YIELD"
            
        return grid_points
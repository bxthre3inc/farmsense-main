# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.services.yield_prediction_service import YieldPredictionService
from app.core.env_wrapper import platform_wrapper

class ExtendedForecastingService:
    """
    Extends forecasting lead times to 14 days for commercial pivot operations.
    Incorporates SLV (San Luis Valley) climatic cycles and non-linear decay.
    """
    
    FORECAST_DAYS = 14
    SLV_EVAPOTRANSPIRATION_BASE = 0.25 # Inches per day (average for SLV growing season)
    
    def __init__(self):
        self.yield_svc = YieldPredictionService()

    def get_14_day_outlook(self, current_profile: List[Dict[str, float]], ndvi: float, ndwi: float) -> List[Dict[str, Any]]:
        """
        Generates a 14-day daily forecast for moisture, yield potential, and stress.
        """
        outlook = []
        base_time = datetime.now()
        
        # Calculate starting metrics
        initial_metrics = self.yield_svc.calculate_yield(current_profile, ndvi, ndwi)
        avg_moisture = np.mean([p['moisture'] for p in current_profile])
        
        for day in range(self.FORECAST_DAYS):
            forecast_time = base_time + timedelta(days=day)
            
            # SLV-Specific Moisture Decay (Non-linear, accelerating under heat)
            # Simulating moisture drop-off without irrigation
            daily_decay = self.SLV_EVAPOTRANSPIRATION_BASE * (1.0 + (day * 0.05)) 
            projected_moisture = max(0.05, avg_moisture - (daily_decay * day / 100.0))
            
            # Adjust spectral modifiers for projected stress
            projected_ndwi = ndwi - (day * 0.02) # Decreasing water index
            projected_ndvi = ndvi * (1.0 - (max(0, 0.3 - projected_moisture) * 2.0)) # NDVI brown-off logic
            
            # Re-run MSF engine for the future state
            # Simulating deep profile shifting proportionally
            projected_profile = [
                {'depth_in': p['depth_in'], 'moisture': p['moisture'] * (projected_moisture / avg_moisture)}
                for p in current_profile
            ]
            
            metrics = self.yield_svc.calculate_yield(projected_profile, projected_ndvi, projected_ndwi)
            
            outlook.append({
                'day': day,
                'date': forecast_time.strftime('%Y-%m-%d'),
                'avg_moisture': round(projected_moisture, 3),
                'yield_forecast_kgha': metrics['yield_forecast_kgha'],
                'crop_stress_probability': metrics['crop_stress_probability'],
                'modifiers': metrics['modifiers']
            })
            
        return outlook

    def batch_extend_grid(self, grid_cells: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Processes a batch of grid cells for long-range outlooks.
        """
        results = []
        for cell in grid_cells:
            # Reconstruct profile from surface if deep profile not provided
            profile = cell.get('source_sensors')
            if not profile or not isinstance(profile, list):
                m_surf = cell.get('moisture_surface', 0.2)
                profile = [
                    {'depth_in': 10, 'moisture': m_surf},
                    {'depth_in': 18, 'moisture': m_surf * 0.9},
                    {'depth_in': 25, 'moisture': m_surf * 0.8}
                ]
            
            outlook = self.get_14_day_outlook(profile, cell.get('ndvi', 0.6), cell.get('ndwi', 0.1))
            
            # Summarize the 14-day risk
            max_stress = max(day['crop_stress_probability'] for day in outlook)
            final_yield = outlook[-1]['yield_forecast_kgha']
            
            cell.update({
                'outlook_14d': outlook,
                'max_stress_risk_14d': max_stress,
                'projected_yield_14d': final_yield,
                'computation_mode': cell.get('computation_mode', 'BASE') + '+AIM_14D'
            })
            results.append(cell)
            
        return results
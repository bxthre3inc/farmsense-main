# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import math
import numpy as np
from typing import List, Dict, Tuple
import sys
import os

# Add common to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from common.spatial.kriging import KrigingBase

class EdgeKrigingEngine(KrigingBase):
    def __init__(self, grid_size: int = 16, resolution_m: float = 50.0):
        super().__init__(resolution_m=resolution_m)
        self.grid_size = grid_size
        
    def compute_50m_grid(
        self, 
        center_lat: float, 
        center_lon: float, 
        sensors: List[Dict[str, float]]
    ) -> List[List[float]]:
        """
        Calculates a grid_size x grid_size moisture probability grid.
        sensors: List of dicts with {'lat': float, 'lon': float, 'moisture': float}
        """
        if not sensors:
            return [[0.0] * self.grid_size for _ in range(self.grid_size)]

        grid = np.zeros((self.grid_size, self.grid_size))
        
        # Use shared spatial logic
        lat_step, lon_step = get_lat_lon_steps(self.resolution, center_lat)
        
        # Grid boundaries
        min_lat = center_lat - (self.grid_size // 2) * lat_step
        min_lon = center_lon - (self.grid_size // 2) * lon_step
        
        for r in range(self.grid_size):
            cell_lat = min_lat + r * lat_step
            for c in range(self.grid_size):
                cell_lon = min_lon + c * lon_step
                
                # Simplified IDW-based Kriging approximation for Edge IQ
                total_weight = 0.0
                weighted_sum = 0.0
                
                for s in sensors:
                    # Euclidean distance in degree-space (sufficient for 16x16 50m grid)
                    d_lat = cell_lat - s['lat']
                    d_lon = cell_lon - s['lon']
                    dist = math.sqrt(d_lat**2 + d_lon**2)
                    
                    if dist < 0.00001: # Avoid division by zero
                        weighted_sum = s['moisture']
                        total_weight = 1.0
                        break
                    
                    weight = 1.0 / (dist ** 2) # Inverse square decay
                    weighted_sum += s['moisture'] * weight
                    total_weight += weight
                
                if total_weight > 0:
                    grid[r, c] = round(weighted_sum / total_weight, 4)
                else:
                    grid[r, c] = 0.0
                    
        return grid.tolist()
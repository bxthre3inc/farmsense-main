import numpy as np
from typing import List, Dict, Any, Tuple
import math

class KrigingBase:
    """
    Base class for spatial interpolation engines (RSS and Edge).
    Adheres to E-DAP standards by standardizing spatial mathematics.
    """
    def __init__(self, resolution_m: float = 50.0):
        self.resolution = resolution_m

    def get_lat_lon_steps(self, center_lat: float) -> Tuple[float, float]:
        """
        Approximate meters to degrees conversion for local field math.
        """
        lat_step = (self.resolution / 111111.0)
        lon_step = (self.resolution / (111111.0 * math.cos(math.radians(center_lat))))
        return lat_step, lon_step

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """Haversine distance simplified for local planar coordinates."""
        return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

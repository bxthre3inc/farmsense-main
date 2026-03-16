import math

def get_lat_lon_steps(resolution_m: float, center_lat: float):
    """
    Approximate meters to degrees conversion for local field math.
    """
    lat_step = (resolution_m / 111111.0)
    lon_step = (resolution_m / (111111.0 * math.cos(math.radians(center_lat))))
    return lat_step, lon_step

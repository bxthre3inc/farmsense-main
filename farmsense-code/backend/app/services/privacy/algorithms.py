# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import secrets
import math

_EARTH_RADIUS_M = 6_371_000.0

def add_jitter(lat: float, lon: float, radius_m: float) -> tuple[float, float]:
    """Uniform random displacement within a circle of `radius_m` metres."""
    if radius_m <= 0:
        return lat, lon

    # Random bearing and distance (rejection-free method)
    angle = secrets.randbelow(360_000) / 1000.0  # degrees, 3 d.p. precision
    distance = math.sqrt(secrets.randbelow(10_000) / 10_000.0) * radius_m

    d_lat = (distance * math.cos(math.radians(angle))) / _EARTH_RADIUS_M
    d_lon = (distance * math.sin(math.radians(angle))) / (
        _EARTH_RADIUS_M * math.cos(math.radians(lat))
    )

    return lat + math.degrees(d_lat), lon + math.degrees(d_lon)


def snap_to_grid(lat: float, lon: float, grid_m: float) -> tuple[float, float]:
    """Snap coordinate to nearest N-metre grid cell centre."""
    if grid_m <= 1.0:
        return lat, lon

    d_lat_per_m = 1.0 / _EARTH_RADIUS_M * (180.0 / math.pi)
    d_lon_per_m = d_lat_per_m / math.cos(math.radians(lat))

    snap_lat = round(lat / (grid_m * d_lat_per_m)) * (grid_m * d_lat_per_m)
    snap_lon = round(lon / (grid_m * d_lon_per_m)) * (grid_m * d_lon_per_m)
    return snap_lat, snap_lon


def laplace_noise(value: float, sensitivity: float, epsilon: float) -> float:
    """Add Laplace-mechanism noise. Returns value unchanged when ε=0."""
    if epsilon <= 0.0 or sensitivity <= 0.0:
        return value
    scale = sensitivity / epsilon
    # numpy-free Laplace variate via uniform inverse CDF
    u = (secrets.randbelow(1_000_000) / 1_000_000.0) - 0.5
    sign = 1.0 if u >= 0 else -1.0
    noise = -scale * sign * math.log(1.0 - 2.0 * abs(u))
    return float(value + noise)
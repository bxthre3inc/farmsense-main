# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

MOISTURE_THRESHOLDS = {
    "critical_low": 0.15,   # vWC - immediate irrigation required
    "low": 0.22,            # vWC - irrigation recommended within 24h
    "optimal_low": 0.28,    # vWC - lower bound of optimal range
    "optimal_high": 0.38,   # vWC - upper bound of optimal range
    "saturated": 0.45,      # vWC - over-irrigation risk
}

NDVI_THRESHOLDS = {
    "stressed": 0.40,       # Below this = severe crop stress
    "marginal": 0.55,       # Moderate stress, investigate
    "healthy": 0.70,        # Nominal vegetative health
    "vigorous": 0.85,       # Peak canopy performance
}

TEMPERATURE_THRESHOLDS = {
    "frost_risk": 2.0,      # °C - frost damage likely
    "cold_stress": 8.0,     # °C - growth retardation
    "optimal_low": 15.0,    # °C - lower optimal
    "optimal_high": 30.0,   # °C - upper optimal
    "heat_stress": 35.0,    # °C - yield reduction begins
}

CROP_MODELS = {
    "potato": {
        "moisture": {"critical_low": 0.25, "low": 0.32, "optimal_high": 0.42},
        "depth_focus": "18-24in (HAPS-Sled)",
        "vaps_focus": "36in",
    },
    "alfalfa": {
        "moisture": {"critical_low": 0.15, "low": 0.20, "optimal_high": 0.38},
        "depth_focus": "24in (HAPS-Deep)",
        "vaps_focus": "48in",
    },
    "barley": {
        "moisture": {"critical_low": 0.12, "low": 0.18, "optimal_high": 0.35},
        "depth_focus": "18in",
        "vaps_focus": "36in",
    },
    "corn": {
        "moisture": {"critical_low": 0.22, "low": 0.28, "optimal_high": 0.45},
        "depth_focus": "24in",
        "vaps_focus": "60in",
    }
}

KNOWN_PEST_SIGNATURES = {
    "colorado_potato_beetle": {
        "color_profile": "orange_striped_black",
        "size_range_mm": (8, 12),
        "severity": "high",
        "action": "Localized targeted spray on affected rows. Consult SLV Extension Office protocol CPB-2026.",
    },
    "aphid_cluster": {
        "color_profile": "green_cluster_underleaf",
        "size_range_mm": (1, 3),
        "severity": "medium",
        "action": "Monitor for 48h. If population exceeds 50/leaf, apply neem oil per SLV organic protocol.",
    },
}
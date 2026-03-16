# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

"""
attention_engine.py — "Fisherman's Attention" State Machine

Governs the adaptive emit frequency of all field sensor nodes. The engine
evaluates real-time physics state and transitions between 4 operational modes,
matching the behavior documented in the PMT Firmware Specification.

The state machine is the software equivalent of the ATSAMD51 FPU's runtime
logic on the physical hardware — this allows the Sensor Emulator to faithfully
replicate the PMT's dynamic bandwidth governance in software.
"""

import logging
import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger("AttentionEngine")


class AttentionMode(str, Enum):
    DORMANT      = "dormant"       # 4-hour grid sweeps; stable conditions
    ANTICIPATORY = "anticipatory"  # 60-minute sweeps; leading indicators rising
    RIPPLE       = "ripple"        # 15-minute sweeps; active anomaly tracking
    COLLAPSE     = "collapse"      # 5-second sweeps; pivot moving or critical event


# Tick interval in real seconds for each mode.
# In the emulator, TIME_MULTIPLIER in main.py scales simulated time.
TICK_INTERVALS_SECONDS = {
    AttentionMode.DORMANT:      14400,   # 4 hours
    AttentionMode.ANTICIPATORY: 3600,    # 60 minutes
    AttentionMode.RIPPLE:       900,     # 15 minutes
    AttentionMode.COLLAPSE:     5,       # 5 seconds
}


@dataclass
class FieldState:
    """Snapshot of the physical conditions used by the attention engine."""
    # Soil hydrology
    moisture_avg: float = 0.30         # Average across all LRZ/VFA nodes (0-1 VWC)
    moisture_std: float = 0.01         # Standard deviation (anomaly signal)
    moisture_delta_1hr: float = 0.0    # Change in moisture over last 1 hour (+ = wetting)

    # Atmosphere
    temperature_c: float = 20.0
    temperature_delta_1hr: float = 0.0  # Rising temp = increased ET demand
    vpd_kpa: float = 0.5               # Vapor Pressure Deficit
    
    # Hardware state
    pivot_moving: bool = False
    pump_on: bool = False
    any_node_faulted: bool = False

    # Edge-EBK derived signals
    anomaly_node_id: Optional[str] = None   # Which LRZ/VFA triggered a trend
    critical_threshold_breached: bool = False


@dataclass
class FocusCollapse:
    """Active Focus Collapse geometry — hyper-computation Zone around an event."""
    epicenter_lat: float = 0.0
    epicenter_lon: float = 0.0
    radius_m: float = 200.0             # Initial collapse radius
    active: bool = False
    triggering_mode: str = "pivot"      # 'pivot' | 'anomaly' | 'fault'


class FishermansAttentionEngine:
    """
    Implements the 4-tier adaptive scaling logic from the PMT Firmware Specification.

    The engine is instantiated per-field. It evaluates a FieldState snapshot
    on every tick and returns the mode that should govern the next emission cycle.
    """

    def __init__(self, field_id: str):
        self.field_id = field_id
        self.mode = AttentionMode.DORMANT
        self.focus = FocusCollapse()
        self._stable_since: float = time.monotonic()
        self._last_mode_change: float = time.monotonic()
        logger.info(f"[{field_id}] AttentionEngine initialized in DORMANT mode.")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def evaluate(self, state: FieldState) -> AttentionMode:
        """
        Evaluate current field state and return the new (or retained) attention mode.
        Also updates the internal Focus Collapse geometry if transitioning to COLLAPSE.
        """
        previous_mode = self.mode
        new_mode = self._compute_mode(state)

        if new_mode != previous_mode:
            logger.info(f"[{self.field_id}] Attention: {previous_mode.value} → {new_mode.value}")
            self._last_mode_change = time.monotonic()

            # If entering COLLAPSE, activate the focus geometry
            if new_mode == AttentionMode.COLLAPSE:
                self.focus.active = True
                self.focus.triggering_mode = "pivot" if state.pivot_moving else "anomaly"
                logger.warning(f"[{self.field_id}] 🎯 FOCUS COLLAPSE activated. Trigger: {self.focus.triggering_mode}")

            # If leaving COLLAPSE towards RIPPLE, deactivate focus and expand to ripple
            elif previous_mode == AttentionMode.COLLAPSE and new_mode == AttentionMode.RIPPLE:
                self.focus.active = False
                logger.info(f"[{self.field_id}] Focus Collapse → Ripple expansion.")

            # If returning to DORMANT, clear anomaly state
            elif new_mode == AttentionMode.DORMANT:
                self.focus.active = False
                self._stable_since = time.monotonic()

        self.mode = new_mode
        return self.mode

    def get_tick_interval_seconds(self, time_multiplier: float = 1.0) -> float:
        """
        Returns the real-world sleep interval for the current mode,
        adjusted for the simulation time multiplier.

        A multiplier > 1.0 compresses simulated time (e.g., multiplier=3600
        makes 1 real second = 1 simulated hour).
        """
        base_interval = TICK_INTERVALS_SECONDS[self.mode]
        return max(0.5, base_interval / time_multiplier)

    def get_ripple_nodes(self, all_node_ids: list[str], anomaly_node_id: Optional[str]) -> list[str]:
        """
        In RIPPLE mode, return the ordered list of nodes to hyper-ping
        (radiating outward from the anomaly epicenter node).
        For simulation: returns all nodes if no epicenter is identified.
        """
        if not anomaly_node_id or anomaly_node_id not in all_node_ids:
            return all_node_ids
        # Put anomaly node first, then the rest
        rest = [n for n in all_node_ids if n != anomaly_node_id]
        return [anomaly_node_id] + rest

    def summary(self) -> dict:
        """Returns the current engine state as a JSON-serializable dict."""
        return {
            "field_id": self.field_id,
            "mode": self.mode.value,
            "tick_interval_seconds": TICK_INTERVALS_SECONDS[self.mode],
            "focus_active": self.focus.active,
            "focus_trigger": self.focus.triggering_mode if self.focus.active else None,
            "seconds_in_current_mode": round(time.monotonic() - self._last_mode_change, 1),
        }

    # ------------------------------------------------------------------
    # Internal state machine
    # ------------------------------------------------------------------

    def _compute_mode(self, s: FieldState) -> AttentionMode:
        """
        Core transition logic. Evaluated top-down; first matching condition wins.
        """
        # ── COLLAPSE triggers (highest priority) ─────────────────────────
        if s.pivot_moving:
            return AttentionMode.COLLAPSE
        if s.critical_threshold_breached:
            return AttentionMode.COLLAPSE
        if s.any_node_faulted:
            return AttentionMode.COLLAPSE

        # ── RIPPLE triggers ───────────────────────────────────────────────
        # 2-sigma spike in moisture std dev signals an active anomaly Zone
        if s.moisture_std > 0.04:
            return AttentionMode.RIPPLE
        if s.anomaly_node_id is not None:
            return AttentionMode.RIPPLE
        if s.pump_on:
            # Pump running is a leading indicator of active state
            return AttentionMode.RIPPLE

        # ── ANTICIPATORY triggers ─────────────────────────────────────────
        # Rising temperature = rising ET demand = narrowing MAD headroom
        if s.temperature_delta_1hr > 2.0:
            return AttentionMode.ANTICIPATORY
        # High VPD = aggressive evapotranspiration
        if s.vpd_kpa > 2.0:
            return AttentionMode.ANTICIPATORY
        # Soil drying quickly (>2% VWC/hr decline)
        if s.moisture_delta_1hr < -0.02:
            return AttentionMode.ANTICIPATORY

        # ── DORMANT (default stable baseline) ────────────────────────────
        # All conditions nominal: high moisture, low temp delta, pivot parked
        return AttentionMode.DORMANT
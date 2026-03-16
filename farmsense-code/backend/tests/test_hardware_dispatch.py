# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.


import unittest
from datetime import datetime
from unittest.mock import MagicMock
from app.api.tasks import evaluate_field_recalculation
from app.services.adaptive_recalc.schemas import AttentionMode, RecalcDecision
from app.models import RecalculationLog

class TestHardwareDispatchFlow(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.field_id = "test_field_999"

    def test_auto_dispatch_on_collapse_mode(self):
        # Mock the engine to return a COLLAPSE decision
        from app.services.adaptive_recalc import AdaptiveRecalculationEngine
        
        # We need to mock the engine's evaluate_field method
        # But evaluate_field_recalculation creates its own engine.
        # So we patch it in the test.
        with unittest.mock.patch('app.api.tasks.AdaptiveRecalculationEngine') as MockEngine:
            engine_instance = MockEngine.return_value
            engine_instance.evaluate_field.return_value = RecalcDecision(
                should_recalculate=True,
                new_mode=AttentionMode.COLLAPSE,
                reason="Volatility detected",
                next_scheduled=datetime.utcnow(),
                priority=5,
                trigger_type="AUTOMATED"
            )
            
            # Mock VRICommandCenter.dispatch_prescription
            with unittest.mock.patch('app.api.tasks.VRICommandCenter.dispatch_prescription') as MockDispatch:
                evaluate_field_recalculation(self.field_id, self.db)
                
                # Check if dispatch was called
                MockDispatch.assert_called_once_with(self.db, self.field_id)
                print("Hardware Dispatch Logic Verified via Mocking")

if __name__ == '__main__':
    unittest.main()
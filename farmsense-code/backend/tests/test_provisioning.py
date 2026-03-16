# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import unittest
from unittest.mock import MagicMock
from app.services.protection.provisioning_service import ProvisioningService
from app.models.devices import Device, DeviceType

class TestProvisioningSequence(unittest.TestCase):
    def setUp(self):
        # Mock DB session
        self.db = MagicMock()
        self.db.query().filter().first.return_value = None # Simulate no device yet

    def test_full_provisioning_sequence(self):
        # Stage 1: Build & ID Allocation (Pattern Check)
        valid_serial = "BX3-2026-SN-001"
        invalid_serial = "FAKE-999"
        self.assertTrue(ProvisioningService.validate_serial(valid_serial))
        self.assertFalse(ProvisioningService.validate_serial(invalid_serial))

        # Stage 3: First Contact (Auto-Registration)
        device = ProvisioningService.auto_register_node(
            self.db, 
            valid_serial, 
            "FIELD_ALFA", 
            DeviceType.VFA
        )
        self.assertEqual(device.external_id, valid_serial)
        self.assertEqual(device.status, "provisioning")
        self.db.add.assert_called()
        self.db.commit.assert_called()

        # Stage 4: "The Boom" (Config Push)
        config = ProvisioningService.generate_provisioning_blob(device)
        self.assertEqual(device.status, "active")
        self.assertIn("hvs_parameters", config)
        self.assertIn("jadc2_tactical", config)
        self.assertEqual(config["status"], "FIELD_ACTIVE")
        self.assertTrue(len(config["jadc2_tactical"]["signing_key_id"]) > 0)

if __name__ == '__main__':
    unittest.main()
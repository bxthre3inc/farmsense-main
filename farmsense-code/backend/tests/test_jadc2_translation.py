# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import unittest
from app.services.jadc2_adapter import JADC2Adapter
import xml.etree.ElementTree as ET

class TestJADC2Adapter(unittest.TestCase):
    def test_to_cot_xml(self):
        grid_point = {
            "field_id": "test-field-001",
            "grid_id": "grid-x1-y1",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "moisture_surface": 0.25,
            "confidence_score": 0.95
        }
        
        cot_xml = JADC2Adapter.to_cot_xml(grid_point)
        self.assertIsNotNone(cot_xml)
        self.assertIn("FS-test-field-001-grid-x1-y1", cot_xml)
        self.assertIn('type="a-f-G-E-O"', cot_xml)
        
        # Parse XML to verify structure
        root = ET.fromstring(cot_xml)
        self.assertEqual(root.tag, "event")
        self.assertEqual(root.get("uid"), "FS-test-field-001-grid-x1-y1")
        
        point = root.find("point")
        self.assertEqual(point.get("lat"), "37.7749")
        self.assertEqual(point.get("lon"), "-122.4194")
        
        detail = root.find("detail")
        env = detail.find("environmental")
        self.assertEqual(env.get("moisture"), "0.25")
        
        lpi = detail.find("lpi_lpd")
        self.assertEqual(lpi.get("fhss_hopping"), "active")

    def test_batch_to_cot(self):
        grid_points = [
            {"field_id": "f1", "grid_id": "g1", "latitude": 10.0, "longitude": 20.0, "moisture_surface": 0.1},
            {"field_id": "f1", "grid_id": "g2", "latitude": 10.1, "longitude": 20.1, "moisture_surface": 0.2}
        ]
        batch_xml = JADC2Adapter.batch_to_cot(grid_points)
        events = batch_xml.strip().split("\n")
        self.assertEqual(len(events), 2)
        self.assertTrue(events[0].startswith("<event"))
        self.assertTrue(events[1].startswith("<event"))

if __name__ == "__main__":
    unittest.main()
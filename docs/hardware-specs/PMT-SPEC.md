---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Device Code: PMT
Full Name: Pivot Motion Tracker
Version: 1.7
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding implementation MUST be reflected here immediately.
> 3. **AI Agent Compliance**: Agents MUST verify current implementation against this document before proposing changes.
> 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

---

# PMT V1.7: Pivot Motion Tracker

## 1. Executive Summary

The PMT (Pivot Motion Tracker) is the primary field-level aggregator and "Field Hub" for FarmSense deployments. Mounted on the center pivot span at 10-15 feet elevation, the PMT receives telemetry from all subordinate sensors (VFA, LRZN, LRZB, PFA), performs edge computation for 50m grid Kriging, executes reflex logic for safety decisions, and relays aggregated data to the District Hub Unit (DHU). The PMT is the critical nexus between low-power field sensors and the district-level infrastructure.

**Primary Role:** Field-level data aggregation and edge computation
**Secondary Role:** Safety reflex logic execution
**Tertiary Role:** Sensor network coordinator
**Deployment Target:** 1 unit per center-pivot system

---

## 2. Functional Requirements

### 2.1 Core Capabilities

| Function | Specification | Priority |
|----------|---------------|----------|
| Field Sensor Aggregation | 34+ nodes (VFA, LRZ, PFA) | P0 |
| Edge Computation | 50m grid Kriging (IDW) | P0 |
| Reflex Logic | Emergency actuation decisions | P0 |
| RTK Positioning | ±5cm accuracy for VRI | P0 |
| Stall Detection | IMU-based, <3g trigger | P0 |
| DHU Communication | 2.4GHz + LTE-M | P0 |
| Sensor Communication | 900MHz CSS LoRa hub | P0 |

### 2.2 Critical Functions

1. **Sensor Aggregation:** Collect 4-hour chirps from all field sensors
2. **Edge-EBK:** Compute 50m Inverse Distance Weighting grid
3. **Reflex Logic:** Emergency pump shutdown authority
4. **Position Tracking:** Real-time pivot angle + GPS
5. **VRI Coordination:** Generate and execute variable-rate worksheets

---

## 3. Hardware Architecture

### 3.1 Mechanical Specifications

| Attribute | Specification |
|-----------|---------------|
| Mounting | Pivot center tower or first span |
| Elevation | 10-15 feet above ground |
| Enclosure | Pelican 1400, IP67 |
| Dimensions | 12" × 10" × 6" |
| Material | Polycarbonate + aluminum heatsink |
| Weight | 8 lbs (enclosure + electronics) |
| Power | 24VAC from pivot panel or solar |
| Antennas | 4×: LoRa, 2.4GHz, LTE, GNSS |
| Operating Temp | -30°C to +70°C |

**Mounting Considerations:**
- Clear line-of-sight to all field sensors
- LoRa coverage radius: 1km+
- Protected from sprinkler spray
- Vibration isolation from tower motion

### 3.2 Compute Subsystem

**MCU: Espressif ESP32-S3-WROOM-1**

| Feature | Specification |
|---------|-------------|
| Core | Xtensa LX7 dual-core @ 240MHz |
| Flash | 16MB (QSPI) |
| RAM | 512KB SRAM + 8MB PSRAM |
| WiFi | 2.4GHz 802.11 b/g/n |
| AI Acceleration | Vector instructions for Kriging |
| Interfaces | SPI × 4, I2C × 2, UART × 3, Ethernet |

**Edge Computation Load:**
| Task | Frequency | Processing Time |
|------|-----------|-----------------|
| IDW Kriging (50m) | Every 4 hours | 150ms |
| Reflex logic | Continuous | <10ms latency |
| Sensor aggregation | Every 4 hours | 50ms |
| VRI worksheet | On-demand | 500ms |

### 3.3 Position Tracking Subsystem

**GNSS: u-blox ZED-F9P with RTK**

| Parameter | Specification |
|-----------|---------------|
| Constellations | GPS, GLONASS, Galileo, BeiDou |
| Bands | L1/L2 multi-band |
| RTK Accuracy | Horizontal: ±2cm, Vertical: ±3cm |
| Update Rate | 10Hz (100ms) |
| Convergence | <30 seconds (with DHU corrections) |

**IMU: Bosch BNO055 9-Axis**

| Parameter | Specification |
|-----------|---------------|
| Accelerometer | ±2g/±4g/±8g/±16g |
| Gyroscope | ±125°/s to ±2000°/s |
| Magnetometer | ±1300µT (x,y), ±2500µT (z) |
| Fusion | On-chip sensor fusion |
| Output | Absolute orientation (quaternion) |
| Update Rate | 100Hz |

**Pivot Angle Calculation:**
```python
def calculate_pivot_angle(gnss_pos, imu_heading, pivot_gps):
    """
    Calculate current pivot rotation angle
    Used for VRI zone mapping and position reporting
    """
    delta_e = gnss_pos.easting - pivot_gps.easting
    delta_n = gnss_pos.northing - pivot_gps.northing
    
    angle_rad = atan2(delta_e, delta_n)
    angle_deg = degrees(angle_rad)
    
    # Normalize to 0-360
    if angle_deg < 0:
        angle_deg += 360
    
    return angle_deg
```

**Stall Detection Algorithm:**
```python
def detect_stall(accel_data, gyro_data, dt):
    """
    Detect pivot stall/impact event via IMU shock detection
    Triggers emergency stop via PFA
    """
    accel_magnitude = sqrt(ax² + ay² + az²)
    
    if accel_magnitude > 3.0:  # 3g threshold
        return True, accel_magnitude
    
    # Also check for stopped rotation (gyro Z axis)
    if gyro_z < 0.1 and expected_moving:
        return True, "rotation_stopped"
    
    return False, None
```

### 3.4 Sensor Communication Hub (LoRa)

**LoRa Concentrator: HopeRF RFM95W × 2 (diversity)**

| Parameter | Specification |
|-----------|---------------|
| Frequency | 915MHz ISM |
| Bandwidth | 125kHz |
| Spreading Factor | SF9-SF12 (adaptive) |
| TX Power | +20dBm (100mW) |
| Sensitivity | -148dBm |
| Channels | 2 (A and B for diversity) |
| Antenna | 3dBi collinear, omni-directional |

**TDMA Network Management:**

| Slot | Duration | Purpose |
|------|----------|---------|
| 0-3s | 3s | LRZB beacon transmissions |
| 3-15s | 12s | LRZN density transmissions |
| 15-20s | 5s | VFA transmissions |
| 20-25s | 5s | PFA transmissions |
| 25-30s | 5s | Contention/random access |

**Network Capacity:**
- Max 50 nodes per PMT (current design: 34)
- Duty cycle: 1% per node (FCC compliant)
- Battery life optimized: 4-hour sleep cycles

### 3.5 Uplink Communication (DHU)

**Primary: 2.4GHz LTU/LTE**

| Parameter | Specification |
|-----------|---------------|
| Technology | Ubiquiti LTU or LTE-M |
| Band | 2.4GHz ISM or Band 2/4/12 |
| Bandwidth | 20MHz (LTU) or 1.4MHz (LTE-M) |
| Range | 10km+ to DHU |
| Data Rate | 10Mbps (LTU) or 1Mbps (LTE-M) |

**Fallback: LTE-M (Cat-M1)**

| Parameter | Specification |
|-----------|---------------|
| Module | Quectel BG96 |
| Bands | B2, B4, B12 (North America) |
| Data Rate | 1Mbps DL / 1Mbps UL |
| Power | 20dBm output |
| Feature | eDRX for power saving |

**Protocol Stack:**
- Physical: 2.4GHz or LTE-M
- Transport: UDP + QUIC (for reliability)
- Application: Protobuf-encoded telemetry bundles
- Security: TLS 1.3 + mutual certificate auth

### 3.6 VRI Control Interface

**Control Valve Outputs:**

| Interface | Type | Purpose |
|-----------|------|---------|
| PWM × 5 | 12V, 5A | Percentage valves (zones) |
| 4-20mA × 2 | Analog | Variable end gun |
| Digital Out × 2 | 24V | On/off end gun |
| Encoder In | A/B quadrature | Position feedback |

**VRI Worksheet Execution:**
```
Worksheet received from DHU/Cloud:
- Start angle, end angle
- Speed preset (FAST/NORMAL/SLOW)
- Zone definitions with percentages

PMT execution:
- Monitor current angle via GNSS
- Interpolate valve position between zones
- Smooth transitions (5-second ramp)
- Log actual vs. commanded to ledger
```

### 3.7 Power Subsystem

**Primary: Pivot Panel 24VAC**

| Parameter | Specification |
|-----------|---------------|
| Input | 24VAC, 5A (from pivot control panel) |
| Conversion | 24VAC → 5VDC (buck converter) |
| Efficiency | 92% |
| Backup | Internal supercap (30-second ride-through) |

**Solar Backup (optional):**

| Component | Specification |
|-----------|---------------|
| Panel | 30W flexible |
| Battery | 20Ah LiFePO₄ |
| Charge Controller | MPPT |
| Autonomy | 3 days |

**Power Budget:**

| Component | Active | Sleep | Average |
|-----------|--------|-------|---------|
| ESP32-S3 | 240mA | 15mA | 180mA |
| ZED-F9P | 68mA | — | 68mA |
| LoRa × 2 | 45mA | — | 15mA |
| LTE-M | 200mA (TX) | 5mA | 25mA |
| **Total** | — | — | **~300mA @ 5V = 1.5W** |

---

## 4. Bill of Materials

| Component | Supplier | Part Number | Unit Cost | Qty | Extended |
|-----------|----------|-------------|-----------|-----|----------|
| MCU | Espressif | ESP32-S3-WROOM-1-N16R8 | $6.50 | 1 | $6.50 |
| GNSS Module | u-blox | ZED-F9P | $68.00 | 1 | $68.00 |
| IMU | Bosch | BNO055 | $12.00 | 1 | $12.00 |
| LoRa Module ×2 | HopeRF | RFM95W-915S2 | $6.50 | 2 | $13.00 |
| LTE-M Module | Quectel | BG96 | $28.00 | 1 | $28.00 |
| SIM Card | Hologram | Global IoT | $5.00 | 1 | $5.00 |
| Enclosure | Pelican | 1400 | $95.00 | 1 | $95.00 |
| Antenna (GNSS) | Taoglas | AGGBP.25B | $18.00 | 1 | $18.00 |
| Antenna (LoRa) | Taoglas | MAG-LP-915 | $24.00 | 2 | $48.00 |
| Antenna (LTE) | Taoglas | GSA.8821 | $12.00 | 1 | $12.00 |
| Power Supply | CUI | VGS-25-5 | $15.00 | 1 | $15.00 |
| PCB | JLCPCB | 6-layer | $45.00 | 1 | $45.00 |
| Connectors/Cable | Various | — | $65.00 | 1 | $65.00 |
| **TOTAL BOM** | | | | | **$430.50** |

**Target Price:** $385/unit at 500+ volume

---

## 5. Software Architecture

### 5.1 Firmware Structure

```
PMT Firmware v2.1.5
├── Core
│   ├── main.cpp              # Initialization
│   ├── scheduler.cpp         # Task scheduling
│   └── power_manager.cpp     # Sleep/wake control
├── Sensors
│   ├── lora_hub.cpp          # LoRa TDMA management
│   ├── gnss.cpp              # ZED-F9P driver
│   └── imu.cpp               # BNO055 driver
├── Compute
│   ├── idw_kriging.cpp       # 50m grid computation
│   ├── reflex_logic.cpp      # Safety decisions
│   └── vri_controller.cpp    # Valve control
├── Comms
│   ├── dhu_link.cpp          # 2.4GHz/LTE uplink
│   ├── protobuf_codec.cpp    # Encoding
│   └── crypto.cpp            # AES/TLS
└── Storage
    ├── sd_cache.cpp          # Black box logging
    └── config.cpp            # EEPROM settings
```

### 5.2 Field State Bundle

**187-Byte Payload (aggregated every 4 hours):**

| Field | Bytes | Description |
|-------|-------|-------------|
| Header | 8 | Timestamp, PMT ID, version |
| Position | 12 | Lat, lon, elevation, angle |
| IMU | 8 | Orientation, stall flags |
| VFA Summary | 24 | 4 depths × VWC + temp |
| LRZ Grid | 64 | 16 nodes × VWC + temp |
| PFA Status | 32 | Flow, depth, pump status |
| VRI | 16 | Current zone, valve positions |
| Ledger | 16 | Hash of last compliance entry |
| CRC | 7 | Fletcher-64 checksum |

---

## 6. Deployment Specifications

### 6.1 Installation Procedure

1. **Mount:** PMT bracket on pivot center tower
2. **Antennas:**
   - GNSS: Clear sky view, magnetic base
   - LoRa: Vertical, 10 feet above ground
   - LTE: Vertical, away from LoRa
   - 2.4GHz: Directional toward DHU (if known)
3. **Power:** Tap 24VAC from pivot panel
4. **VRI:** Connect to valve controller (if equipped)
5. **Commission:**
   - Pair with DHU
   - Calibrate RTK (wait for fix)
   - Register all subordinate sensors
   - Test LoRa coverage to field extremities

**Installation Time:** 1.5 hours

### 6.2 Sensor Registration

**Automatic Discovery:**
- PMT listens for unregistered sensor chirps
- Captures device ID, type, GPS location
- Farmer confirms placement via mobile app
- PMT assigns TDMA slot, updates schedule

**Network Map:**
```json
{
  "pmt_id": "PMT-001-ABC123",
  "sensors": {
    "vfa": ["VFA-1234", "VFA-5678"],
    "lrzb": ["LRZB-A", "LRZB-B", "LRZB-C", "LRZB-D"],
    "lrzn": ["LRZN-01" through "LRZN-12"],
    "pfa": ["PFA-9876"]
  },
  "tdma_schedule": "slot_map_v1.2"
}
```

---

## 7. Telemetry Protocol

### 7.1 PMT → DHU Uplink

**Primary Bundle (4-hour interval, LTE-M):**
- 187-byte Field State Bundle
- Compressed with zlib (typical: 120 bytes)
- Encrypted with AES-256-GCM
- Sent via QUIC over LTE-M

**Emergency Packet (immediate, any available link):**
- Stall detected
- PFA actuation commanded
- Critical sensor failure
- Format: 32 bytes, max priority

### 7.2 DHU → PMT Downlink

**VRI Worksheet Delivery:**
```protobuf
message VRIWorksheet {
  string worksheet_id = 1;
  uint64 valid_until = 2;  // Unix timestamp
  float start_angle = 3;
  float end_angle = 4;
  SpeedPreset base_speed = 5;
  repeated VRIZone zones = 6;
}
```

**Configuration Updates:**
- TDMA schedule modifications
- Sensor registration/deregistration
- Firmware OTA (over 2.4GHz)
- Reflex logic threshold changes

---

## 8. Reflex Logic System

### 8.1 Decision Matrix

| Condition | Source | Threshold | Action | Latency |
|-----------|--------|-----------|--------|---------|
| Stall detected | IMU | >3g shock | Signal PFA stop | <50ms |
| Rotation stopped | IMU + GNSS | No motion 30s | Signal PFA stop | <100ms |
| VFA saturation | VFA | >95% at 36" | Signal PFA stop | <200ms |
| PFA cavitation | PFA | HF signature | Alert farmer | <500ms |
| DHU offline | Link status | 5 min no ACK | Buffer to SD, alert | <1s |

### 8.2 Actuation Authority

**PMT Authority:**
- Recommend stop to PFA (via LoRa)
- Execute VRI stop (direct valve control)
- Alert farmer via DHU/Cloud

**PFA Authority:**
- Direct pump contactor open (highest priority)
- Cannot be overridden by PMT
- Both must agree to restart

---

## 9. Maintenance & Lifecycle

### 9.1 Expected Lifespan

| Component | Lifespan | Replacement |
|-----------|----------|-------------|
| Electronics | 10+ years | Not serviceable |
| GNSS module | 10+ years | Field replaceable |
| Antennas | 15+ years | Weather check |
| Enclosure seals | 5 years | Inspect annually |

### 9.2 Maintenance Schedule

| Interval | Action |
|----------|--------|
| Weekly | Visual inspection, antenna tightness |
| Monthly | Log review, error rate check |
| Quarterly | GNSS accuracy verification |
| Annually | Full diagnostic, seal replacement |

---

## 10. Integration & APIs

### 10.1 Device Registration

```json
{
  "device_type": "PMT",
  "hardware_version": "1.7",
  "firmware_version": "2.1.5",
  "device_id": "PMT-001-ABC123",
  "field_id": "field-550e8400",
  "dhu_id": "DHU-CONEJOS-001",
  "installed_at": "2026-03-19T08:00:00Z",
  "gps_pivot": {
    "lat": 37.456789,
    "lon": -105.987654
  },
  "vri_equipped": true,
  "valve_zones": 5,
  "sensors_managed": 34,
  "warranty_expires": "2031-03-19"
}
```

### 10.2 Real-Time Data

```json
{
  "device_id": "PMT-001-ABC123",
  "timestamp": "2026-03-19T14:30:00Z",
  "position": {
    "lat": 37.456789,
    "lon": -105.987654,
    "elevation_m": 2345.6,
    "pivot_angle": 127.5
  },
  "motion": {
    "moving": true,
    "speed_preset": "NORMAL",
    "completion_pct": 35.4
  },
  "sensors_summary": {
    "vfa_count": 2,
    "lrzn_count": 12,
    "lrzb_count": 4,
    "pfa_online": true
  },
  "vri": {
    "active": true,
    "current_zone": 3,
    "valve_position_pct": 78.5
  },
  "ledger": {
    "last_hash": "a3f7b2c8d9e1f4a5...",
    "uncommitted_events": 0
  }
}
```

---

## 11. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-04-01 | Initial release | Engineering |
| 1.5 | 2025-08-15 | Added LTE-M fallback | Comms |
| 1.6 | 2025-11-20 | Improved stall detection | Software |
| 1.7 | 2026-03-19 | Documentation standard | Documentation |

---

## 12. Related Documentation

- `DHU-SPEC.md` — District hub receiving PMT data
- `LRZN-SPEC.md` — Subordinate soil sensors
- `LRZB-SPEC.md` — Reference soil sensors
- `VFA-SPEC.md` — Deep vertical probes
- `PFA-SPEC.md` — Wellhead flow measurement
- `SFD-SPEC.md` — Deployment configurations

---

*Proprietary IP of bxthre3 inc. — Confidential*
*© 2026 bxthre3 inc. All rights reserved.*

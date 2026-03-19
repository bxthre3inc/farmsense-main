---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Device Code: CSA
Full Name: Corner Swing Arm
Version: 1.0
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding implementation MUST be reflected here immediately.
> 3. **AI Agent Compliance**: Agents MUST verify current implementation against this document before proposing changes.
> 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

---

# CSA V1.0: Corner Swing Arm

## 1. Executive Summary

The CSA (Corner Swing Arm) is a kinematic tracking module specifically designed for center-pivot irrigation systems with corner-swing or linear-move extensions. Mounted on the outer span or end tower of a corner-swing system, the CSA provides extended coverage area tracking, variable-rate irrigation (VRI) control for the swing arm, and compliance monitoring for non-circular field geometries.

**Primary Role:** Corner-swing extension tracking and VRI control
**Secondary Role:** Extended field boundary coverage monitoring
**Deployment Target:** 1 unit per corner-swing system (optional)

---

## 2. Functional Requirements

### 2.1 Core Capabilities

| Function | Specification | Priority |
|----------|---------------|----------|
| Swing Angle Tracking | ±1° accuracy, 0-270° sweep | P0 |
| Extended Span Position | RTK GNSS + kinematic model | P0 |
| VRI Zone Mapping | Variable-rate for swing arm | P1 |
| Coverage Area Calculation | Non-circular polygon | P1 |
| Telemetry | 900MHz CSS LoRa to PMT | P0 |
| Power | Battery + solar (autonomous) | P0 |

### 2.2 Swing Arm Geometry

**Corner-Swing System Topology:**

| Component | Standard Pivot | Corner-Swing Extension |
|-----------|---------------|------------------------|
| Coverage | Circular (126 acres) | Irregular (+15-40 acres) |
| Span Length | 1,300 ft fixed | 1,300 ft + 300-500 ft |
| Motion | Pure rotation | Rotation + linear translation |
| VRI Complexity | 1D (radial zones) | 2D (radial × swing) |
| CSA Role | N/A | Extension tracking + VRI |

**CSA Measurement Requirements:**
- Real-time swing angle (compass relative to pivot)
- Extension span heading (GNSS-derived)
- End gun position (if equipped)
- Actual coverage vs. planned coverage

---

## 3. Hardware Architecture

### 3.1 Mechanical Specifications

| Attribute | Specification |
|-----------|---------------|
| Mounting | Outer span tower or end gun carriage |
| Enclosure | Polycase YH-161208, IP67 |
| Dimensions | 8" × 6" × 4" |
| Material | Polycarbonate + aluminum heatsink |
| Weight | 3.5 lbs |
| Solar Panel | 20W flexible, span-mount |
| Battery | 12Ah LiFePO₄ |
| Operating Temp | -20°C to +60°C |

**Mounting Considerations:**
- Vibration isolation from span motion
- Clear sky view for GNSS
- Protected from sprinkler spray
- Accessible for maintenance

### 3.2 Position Tracking Subsystem

**GNSS: u-blox ZED-F9P with RTK**

| Parameter | Specification |
|-----------|---------------|
| Constellations | GPS, GLONASS, Galileo, BeiDou |
| Bands | L1/L2 multi-band |
| RTK Accuracy | Horizontal: ±2cm, Vertical: ±3cm |
| Update Rate | 10Hz (100ms) |
| Convergence | <30 seconds (with RTK) |
| Base Station | DHU or PMT provides RTK corrections |

**IMU: Bosch BNO055 9-Axis**

| Parameter | Specification |
|-----------|---------------|
| Accelerometer | ±2g/±4g/±8g/±16g |
| Gyroscope | ±125°/s to ±2000°/s |
| Magnetometer | ±1300µT (x,y), ±2500µT (z) |
| Fusion | On-chip sensor fusion |
| Output | Absolute orientation (quaternion) |
| Update Rate | 100Hz |

**Kinematic Model:**
```
Swing Angle (θ) = atan2(E_N, E_E) - Pivot_Heading
Extension Length (L) = sqrt((E_N - P_N)² + (E_E - P_E)²) - Span_Length
Where: E = End tower position, P = Pivot position
```

### 3.3 VRI Control Interface

**Valve Control Output:**

| Interface | Type | Purpose |
|-----------|------|---------|
| PWM × 4 | 12V, 3A | Zone valve control |
| 4-20mA × 2 | Analog | Variable-rate end gun |
| Digital In × 2 | 24V | Pressure switch feedback |
| CAN Bus | J1939 | Integration with existing VRI systems |

**Zone Mapping:**
- Standard pivot: 3-5 radial zones
- Corner-swing: 6-12 radial × angular zones
- CSA coordinates with PMT for unified VRI worksheet

### 3.4 Processing Subsystem

**MCU: Espressif ESP32-S3-WROOM-1**

| Feature | Specification |
|---------|-------------|
| Core | Xtensa LX7 dual-core @ 240MHz |
| Flash | 8MB (QSPI) |
| RAM | 512KB SRAM + 8MB PSRAM |
| WiFi | 2.4GHz 802.11 b/g/n |
| Bluetooth | 5.0 (not used) |
| Interfaces | SPI × 4, I2C × 2, UART × 3, CAN |

**Real-Time Requirements:**
- Position update: 100ms (10Hz)
- VRI valve response: <500ms
- Emergency stop relay: <100ms

### 3.5 Communication Subsystem

**LoRa: HopeRF RFM95W-915S2**

| Parameter | Specification |
|-----------|---------------|
| Frequency | 915MHz ISM |
| Bandwidth | 125kHz |
| Spreading Factor | SF9 |
| TX Power | +17dBm (50mW) |
| Range | 1km+ to PMT |

**CAN Bus:**
- J1939 protocol for valve controllers
- Integration with Valley, Zimmatic, Reinke VRI systems
- Backward compatible with existing installations

### 3.6 Power Subsystem

| Component | Specification |
|-----------|---------------|
| Solar Panel | 20W flexible, monocrystalline |
| Battery | 12Ah LiFePO₄ @ 12.8V = 154Wh |
| Charge Controller | MPPT, 10A |
| Consumption | 2W average, 8W peak |
| Autonomy | 3 days (no solar) |

---

## 4. Bill of Materials

| Component | Supplier | Part Number | Unit Cost | Qty | Extended |
|-----------|----------|-------------|-----------|-----|----------|
| MCU | Espressif | ESP32-S3-WROOM-1 | $4.50 | 1 | $4.50 |
| GNSS Module | u-blox | ZED-F9P | $68.00 | 1 | $68.00 |
| IMU | Bosch | BNO055 | $12.00 | 1 | $12.00 |
| LoRa Module | HopeRF | RFM95W-915S2 | $6.50 | 1 | $6.50 |
| CAN Transceiver | TI | TCAN330 | $2.50 | 1 | $2.50 |
| Enclosure | Polycase | YH-161208 | $45.00 | 1 | $45.00 |
| Solar Panel | Renogy | 20W-flex | $35.00 | 1 | $35.00 |
| Battery | Bioenno | BLF-1212 | $95.00 | 1 | $95.00 |
| Charge Controller | Victron | 75/10 | $65.00 | 1 | $65.00 |
| Antenna (GNSS) | Taoglas | AGGBP.25B | $18.00 | 1 | $18.00 |
| Antenna (LoRa) | Taoglas | SS-Whip | $3.50 | 1 | $3.50 |
| PCB | JLCPCB | 4-layer | $28.00 | 1 | $28.00 |
| Connectors/Cable | Various | — | $45.00 | 1 | $45.00 |
| **TOTAL BOM** | | | | | **$428.00** |

**Target Price:** $385/unit at 500+ volume

---

## 5. Software & Algorithms

### 5.1 Kinematic Fusion

**Complementary Filter:**
```python
def fuse_position(gnss_pos, imu_accel, imu_gyro, dt):
    """
    Fuse GNSS absolute position with IMU high-rate updates
    Provides 100Hz position output from 10Hz GNSS
    """
    # GNSS provides absolute reference
    # IMU provides high-rate interpolation between fixes
    # Outlier rejection for GNSS multipath
    pass
```

### 5.2 Coverage Calculation

**Non-Circular Area:**
```python
def calculate_coverage(pivot_pos, end_tower_pos, swing_angle):
    """
    Calculate actual irrigated area as polygon
    For corner-swing systems with variable geometry
    """
    # Shoelace formula for polygon area
    # Handles concave shapes from field boundaries
    pass
```

---

## 6. Deployment Specifications

### 6.1 Installation

1. **Mount:** Vibration-isolated bracket on outer span
2. **GNSS Antenna:** Clear sky view, magnetic mount
3. **LoRa Antenna:** Vertical, away from metal span
4. **Solar Panel:** South-facing, 30° tilt
5. **Wire:** CAN bus to valve controller (if VRI)
6. **Commission:** Pair with PMT, calibrate swing angle

**Installation Time:** 1 hour

### 6.2 Calibration

**Swing Angle Calibration:**
1. Position swing arm at 0° (aligned with main span)
2. Record magnetometer baseline
3. Position at 90°, 180°, 270°
4. Build lookup table for angle vs. heading
5. Verify against GNSS-derived angle

---

## 7. Telemetry Protocol

### 7.1 Payload Format

```c
typedef struct {
    uint32_t device_id;
    uint32_t timestamp;
    int32_t  lat;              // × 1e7 (degrees)
    int32_t  lon;              // × 1e7 (degrees)
    int16_t  elevation_cm;     // Ellipsoid height
    uint16_t swing_angle;      // × 10 (0-2700 = 0-270°)
    uint16_t extension_ft;   // Distance from last tower
    uint16_t heading;          // × 10 (0-360°)
    uint8_t  gnss_fix_type;    // 0=none, 1=3D, 2=RTK
    uint8_t  vri_zone;         // Active VRI zone
    uint16_t valve_position; // × 100 (0-100%)
    uint16_t battery_voltage;
    int8_t   rssi;
    uint8_t  status_flags;
} csa_payload_t;
```

---

## 8. Integration

### 8.1 Device Registration

```json
{
  "device_type": "CSA",
  "hardware_version": "1.0",
  "device_id": "CSA-ABCD1234",
  "pivot_id": "pmt-corner-001",
  "installed_at": "2026-03-19T10:00:00Z",
  "swing_range_degrees": 270,
  "extension_length_ft": 450,
  "vri_enabled": true,
  "valve_zones": 8
}
```

---

## 9. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-19 | Initial release | Documentation |

---

## 10. Related Documentation

- `PMT-SPEC.md` — Main pivot tracker
- `SFD-SPEC.md` — Corner-swing deployment config
- `VRI-SPEC.md` — Variable-rate irrigation protocol

---

*Proprietary IP of bxthre3 inc. — Confidential*

---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Device Code: LRZN
Full Name: Lateral Root Zone Node
Version: 1.2
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding implementation MUST be reflected here immediately.
> 3. **AI Agent Compliance**: Agents MUST verify current implementation against this document before proposing changes.
> 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

---

# LRZN V1.2: Lateral Root Zone Node

## 1. Executive Summary

The LRZN (Lateral Root Zone Node) is a high-density, low-cost soil moisture sensor designed for spatial coverage and Kriging interpolation support. As the "Basic" tier of the Lateral Root Zone Surveyor family, LRZN units provide volumetric water content (VWC) measurements across the field at a target density of 12 nodes per 126-acre center-pivot field.

**Primary Role:** Spatial density coverage for moisture interpolation
**Secondary Role:** Ground-truth validation points for Kriging algorithms
**Deployment Target:** 12 units per standard field (with 4 LRZB reference units)

---

## 2. Functional Requirements

### 2.1 Core Capabilities

| Function | Specification | Priority |
|----------|---------------|----------|
| VWC Measurement | ±3% accuracy, 0-100% range | P0 |
| Soil Temperature | Not equipped (rely on LRZB for temp) | — |
| Telemetry | 900MHz CSS LoRa to PMT | P0 |
| Battery Life | 4+ years at 4-hour chirp intervals | P0 |
| Installation | Tool-less push-in deployment | P1 |
| Cost Target | <$30 BOM | P1 |

### 2.2 Operational Modes

**DORMANT Mode (Default):**
- Measurement interval: 4 hours
- Power draw: 8µA (sleep)
- Telemetry: Single VWC chirp
- Duration: 90%+ of operational life

**ANTICIPATORY Mode:**
- Trigger: Sunrise, temperature rise >5°C/hour
- Measurement interval: 60 minutes
- Power draw: 15mA
- Purpose: Pre-irrigation baseline capture

**FOCUS RIPPLE Mode:**
- Trigger: Moisture anomaly >5% deviation from expected
- Measurement interval: 15 minutes
- Power draw: 45mA
- Purpose: High-resolution anomaly capture

---

## 3. Hardware Architecture

### 3.1 Mechanical Specifications

| Attribute | Specification |
|-----------|---------------|
| Form Factor | Soil probe with integrated electronics |
| Length | 8" (200mm) insertion depth |
| Diameter | 1.5" (38mm) body |
| Material | UV-stabilized ABS housing |
| Tip | Hardened steel penetration point |
| Seal Rating | IP68 (submersible to 1m) |
| Operating Temp | -40°C to +85°C |
| Weight | 180g (including battery) |

**Installation Method:**
- Push-in manual deployment
- No tools required
- Self-tapping thread engagement
- Antenna protrudes 2" above soil surface

### 3.2 Sensing Subsystem

**Dielectric Measurement Principle:**
- Method: High-frequency capacitive (~100MHz)
- Electrodes: Two planar electrodes embedded in housing wall
- Field projection: Through ABS housing into soil
- Measurement: Dielectric constant (ε) of surrounding soil

**Topp Equation Conversion:**
```
VWC = -5.3×10⁻² + 2.92×10⁻²×ε - 5.5×10⁻⁴×ε² + 4.3×10⁻⁶×ε³
```

**Sensor Specifications:**

| Parameter | Value |
|-----------|-------|
| VWC Range | 0-100% |
| VWC Accuracy | ±3% (factory calibrated) |
| VWC Resolution | 0.1% |
| Temperature Coefficient | ±0.5% / 10°C |
| Response Time | <5 seconds |
| Sensor Depth | 4-8" (adjustable via insertion) |

### 3.3 Processing Subsystem

**MCU: Nordic Semiconductor nRF52840-QIAA**

| Feature | Specification |
|---------|-------------|
| Core | ARM Cortex-M4 @ 64MHz |
| Flash | 1MB |
| RAM | 256KB |
| Bluetooth | 5.2 (not used — disabled for power) |
| ADC | 12-bit SAR, 8 channels |
| Crypto | ARM TrustZone + Cryptocell CC-310 |
| Package | QFN48 |

**PCBA GPIO Pinout:**

| Pin | Function | Direction | Notes |
|-----|----------|-----------|-------|
| P0.02 | ADC0 (dielectric) | Input | VWC measurement |
| P0.04 | LoRa NSS | Output | Chip select |
| P0.05 | LoRa DIO0 | Input | Packet ready interrupt |
| P0.06 | LoRa DIO1 | Input | CAD detect |
| P0.07 | LoRa DIO2 | Input | FHS change |
| P0.28 | SPI SCK | Output | 8MHz max |
| P0.29 | SPI MISO | Input | — |
| P0.30 | SPI MOSI | Output | — |
| P0.31 | Status LED | Output | Red/green bicolor |
| P1.00 | Wake Button | Input | Configuration mode |
| P1.01 | Battery ADC | Input | Voltage monitoring |

### 3.4 Communication Subsystem

**LoRa Module: HopeRF RFM95W-915S2**

| Parameter | Specification |
|-----------|---------------|
| Frequency | 915MHz (ISM band) |
| Modulation | LoRa CSS (Chirp Spread Spectrum) |
| Bandwidth | 125kHz |
| Spreading Factor | SF9 (trade-off: range vs. airtime) |
| Coding Rate | 4/5 |
| TX Power | +14dBm (25mW) |
| Sensitivity | -148dBm @ SF9 |
| Range | 2km+ to PMT in open field |
| Data Rate | 1.2kbps effective |
| Antenna | PCB trace helical, vertical polarization |

**Protocol Stack:**
- Physical: LoRa CSS
- MAC: Custom TDMA (Time Division Multiple Access)
- Network: Proprietary star topology (PMT as hub)
- Application: CBOR-encoded sensor readings
- Security: AES-128-CTR encrypted payloads

### 3.5 Power Subsystem

**Battery: 2× AA Lithium (LiFeS₂)**

| Attribute | Specification |
|-----------|---------------|
| Chemistry | Lithium Iron Disulfide (LiFeS₂) |
| Brand | Energizer Ultimate Lithium |
| Capacity | 3000mAh per cell |
| Voltage | 1.5V nominal (3.0V series) |
| Temperature Range | -40°C to +60°C |
| Self-Discharge | <1% per year |
| Shelf Life | 20 years |

**Power Budget (4-hour interval):**

| Mode | Duration | Current | Energy |
|------|----------|---------|--------|
| Sleep | 3h 59m 50s | 8µA | 114µAh |
| Wake + Measure | 5s | 5mA | 7µAh |
| LoRa TX | 5s | 45mA | 63µAh |
| **Per Cycle** | 4 hours | — | **184µAh** |
| **Annual** | — | — | **403mAh** |
| **Battery Life** | — | — | **~7.4 years** |

**Conservative Rating:** 4+ years (accounts for cold weather, TX retries)

---

## 4. Bill of Materials

| Component | Supplier | Part Number | Unit Cost | Qty | Extended |
|-----------|----------|-------------|-----------|-----|----------|
| MCU | Nordic | nRF52840-QIAA-R | $8.50 | 1 | $8.50 |
| LoRa Module | HopeRF | RFM95W-915S2 | $6.50 | 1 | $6.50 |
| PCB | JLCPCB | 4-layer, 1.6mm | $2.80 | 1 | $2.80 |
| Enclosure (ABS) | Custom mold | UV-stabilized | $3.20 | 1 | $3.20 |
| Antenna | PCB trace | 915MHz helical | $0.50 | 1 | $0.50 |
| Battery contacts | Keystone | 92 | $0.40 | 2 | $0.80 |
| Batteries (AA) | Energizer | L91 | $2.50 | 2 | $5.00 |
| Seals (O-rings) | Parker | NBR-70 | $0.30 | 3 | $0.90 |
| Passives | Various | 0402/0603 | $1.50 | 1 | $1.50 |
| **TOTAL BOM** | | | | | **$29.70** |

**Target Price:** $29.00/unit at 1,000+ volume

---

## 5. Calibration & Accuracy

### 5.1 Factory Calibration

**Two-Point Calibration Process:**
1. **Dry Reference:** Oven-dried soil (0% VWC)
2. **Saturated Reference:** Fully saturated known soil (45% VWC for clay loam)

**Calibration Certificate Includes:**
- Dielectric-to-VWC conversion coefficients
- Temperature compensation lookup table
- Unique device ID and QR code
- Factory calibration date

### 5.2 Field Calibration (Optional)

**Single-Point Field Calibration:**
- Collect sensor reading
- Extract soil sample at same depth
- Gravimetric analysis (oven dry)
- Upload correction factor via PMT
- Improves accuracy to ±2%

---

## 6. Deployment Specifications

### 6.1 Field Placement Pattern

**Standard 126-Acre Center Pivot (16 Total LRZ Units):**

| Ring | Radius (% of span) | Count | Type | Purpose |
|------|-------------------|-------|------|---------|
| Center | 0% | 1 | LRZB | Pivot point reference |
| Inner | 25% | 3 | LRZN | Near-pivot zone |
| Middle | 50% | 4 | LRZB | Mid-field validation |
| Outer | 75% | 8 | LRZN | Edge interpolation |

**Placement Guidelines:**
- Avoid wheel tracks (±3m from tire lines)
- Avoid previous crop rows (residue effects)
- Maintain LoRa line-of-sight to PMT
- Vary depth 4-8" based on root zone depth
- GPS coordinates logged on installation

### 6.2 Installation Procedure

1. **Site Selection:** Mark location with GPS ±10cm
2. **Soil Prep:** Clear surface debris, loosen if compacted
3. **Insertion:** Push vertically to marked depth line
4. **Engagement:** Twist ¼ turn to engage self-tapping threads
5. **Verification:** LED flash confirms LoRa registration
6. **Documentation:** Photo + GPS + depth recorded in app

**Time per Unit:** 2 minutes
**Total Field Installation:** 32 minutes (16 LRZ units)

---

## 7. Telemetry Protocol

### 7.1 Payload Format (CBOR)

```c
typedef struct {
    uint32_t device_id;        // 4 bytes: Unique device ID
    uint32_t timestamp;        // 4 bytes: Unix epoch
    uint16_t vwc;              // 2 bytes: VWC × 100 (0-10000)
    int16_t  temperature;      // 2 bytes: Temp × 10 (optional, if equipped)
    uint16_t battery_mv;       // 2 bytes: Battery millivolts
    int8_t   rssi;             // 1 byte: Last RSSI to PMT
    uint8_t  quality_score;    // 1 byte: 0-100 measurement confidence
    uint8_t  reserved[2];      // 2 bytes: Future expansion
} lrzn_payload_t;              // 18 bytes total
```

### 7.2 Transmission Schedule

| Mode | Interval | Max Retries | Backoff |
|------|----------|-------------|---------|
| DORMANT | 4 hours | 3 | 15 min |
| ANTICIPATORY | 60 min | 3 | 5 min |
| FOCUS RIPPLE | 15 min | 5 | 2 min |

---

## 8. Compliance & Certifications

| Standard | Status | Notes |
|----------|--------|-------|
| FCC Part 15.247 | ✅ | 915MHz ISM operation |
| CE Marking | 🔄 | In progress (EU expansion) |
| IP68 Rating | ✅ | Submersible to 1m |
| RoHS 3 | ✅ | Lead-free, compliant materials |
| WEEE | ✅ | Recycling program included |

---

## 9. Maintenance & Lifecycle

### 9.1 Expected Lifespan

| Component | Lifespan | Replacement |
|-----------|----------|-------------|
| Electronics | 10+ years | Not serviceable |
| Battery | 4-6 years | Field replacement |
| Housing | 15+ years | UV-stabilized ABS |
| Sensor drift | <1% / year | Auto-compensated |

### 9.2 Field Maintenance

**Annual Inspection:**
- Visual housing check
- Antenna orientation
- Battery voltage reading
- Re-install if heaved by frost

**Battery Replacement:**
- Tool: 3mm hex key
- Procedure: Twist open housing, swap AAs, reseal
- Time: 2 minutes
- Disposal: Recycle at RSS Sled Hospital

---

## 10. Integration & APIs

### 10.1 Device Registration

```json
{
  "device_type": "LRZN",
  "hardware_version": "1.2",
  "firmware_version": "2.1.4",
  "device_id": "LRZN-A1B2C3D4",
  "field_id": "field-550e8400",
  "installed_at": "2026-03-19T14:30:00Z",
  "gps_location": {
    "lat": 37.456789,
    "lon": -105.987654
  },
  "depth_inches": 6,
  "calibration_date": "2026-03-19",
  "warranty_expires": "2029-03-19"
}
```

### 10.2 Data Output

```json
{
  "device_id": "LRZN-A1B2C3D4",
  "timestamp": "2026-03-19T14:30:00Z",
  "vwc": 0.234,
  "vwc_percent": 23.4,
  "battery_voltage": 2.95,
  "quality_score": 98,
  "measurement_mode": "DORMANT"
}
```

---

## 11. Revision History

| Version | Date | Changes | Author |
|-----------|------|---------|--------|
| 1.0 | 2025-11-01 | Initial release | Engineering |
| 1.1 | 2026-01-15 | Improved antenna, +1yr battery | RF Team |
| 1.2 | 2026-03-19 | Cost reduction ($35→$29), renamed from LRZ1 | Documentation |

---

## 12. Related Documentation

- `LRZB-SPEC.md` — Reference/beacon variant
- `PMT-SPEC.md` — Field hub receiving LRZN data
- `VFA-SPEC.md` — Deep vertical profile anchor
- `NETWORK-SPEC.md` — LoRa topology and protocols
- `SFD-SPEC.md` — Single Field Deployment configurations

---

*Proprietary IP of bxthre3 inc. — Confidential*
*© 2026 bxthre3 inc. All rights reserved.*

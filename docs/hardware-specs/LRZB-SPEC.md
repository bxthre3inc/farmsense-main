---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Device Code: LRZB
Full Name: Lateral Root Zone Beacon
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

# LRZB V1.2: Lateral Root Zone Beacon

## 1. Executive Summary

The LRZB (Lateral Root Zone Beacon) is a premium soil moisture sensor serving as a calibration anchor and temperature reference point within the Lateral Root Zone Surveyor family. As the "Reference" tier, LRZB units provide both VWC and soil temperature measurements with higher accuracy than LRZN units, enabling temperature-compensated VWC readings and ground-truth validation for Kriging interpolation.

**Primary Role:** Calibration anchor and temperature reference
**Secondary Role:** Ground-truth validation for Kriging algorithms
**Deployment Target:** 4 units per standard field (with 12 LRZN density units)

---

## 2. Functional Requirements

### 2.1 Core Capabilities

| Function | Specification | Priority |
|----------|---------------|----------|
| VWC Measurement | ±2% accuracy, 0-100% range | P0 |
| Soil Temperature | ±0.5°C accuracy, -40°C to +60°C | P0 |
| Temperature Compensation | Auto-correct VWC based on soil temp | P1 |
| Telemetry | 900MHz CSS LoRa to PMT | P0 |
| Battery Life | 4+ years at 4-hour chirp intervals | P0 |
| Cost Target | <$55 BOM | P1 |

### 2.2 LRZB vs LRZN Distinction

| Attribute | LRZB (Reference) | LRZN (Basic) |
|-----------|------------------|--------------|
| **Role** | Calibration anchor | Spatial density |
| **VWC Accuracy** | ±2% | ±3% |
| **Temperature Sensor** | ✅ Yes | ❌ No |
| **Temp Compensation** | ✅ Yes | ❌ No |
| **BOM Cost** | $54.30 | $29.00 |
| **Field Density** | 4 per field | 12 per field |
| **Purpose** | Ground-truth validation | Kriging interpolation |

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
| Weight | 195g (including battery) |

**Installation Method:**
- Push-in manual deployment
- No tools required
- Self-tapping thread engagement
- Antenna protrudes 2" above soil surface
- Identical form factor to LRZN (interchangeable deployment)

### 3.2 Sensing Subsystem

**Dielectric Measurement Principle:**
- Method: High-frequency capacitive (~100MHz)
- Electrodes: Two planar electrodes embedded in housing wall
- Field projection: Through ABS housing into soil
- Measurement: Dielectric constant (ε) of surrounding soil

**Temperature Measurement:**
- Sensor: NTC thermistor (10kΩ @ 25°C)
- Location: Embedded in sensor tip
- Thermal mass: <30 seconds to equilibrium
- Accuracy: ±0.5°C across -40°C to +60°C

**Topp Equation with Temperature Compensation:**
```
VWC_corrected = VWC_raw + α × (T_soil - T_cal)
where α = 0.002 (temperature coefficient)
```

**Sensor Specifications:**

| Parameter | VWC | Temperature |
|-----------|-----|-------------|
| Range | 0-100% | -40°C to +60°C |
| Accuracy | ±2% | ±0.5°C |
| Resolution | 0.1% | 0.1°C |
| Response Time | <5 sec | <30 sec |
| Sensor Depth | 4-8" | Same as VWC |

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
| P0.03 | ADC1 (temperature) | Input | NTC thermistor |
| P0.04 | LoRa NSS | Output | Chip select |
| P0.05 | LoRa DIO0 | Input | Packet ready interrupt |
| P0.06 | LoRa DIO1 | Input | CAD detect |
| P0.07 | LoRa DIO2 | Input | FHS change |
| P0.28 | SPI SCK | Output | 8MHz max |
| P0.29 | SPI MISO | Input | — |
| P0.30 | SPI MOSI | Output | — |
| P0.31 | Status LED | Output | Red/green/blue tricolor |
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

**Beacon Role:**
- LRZB units transmit first in each TDMA slot (priority channel)
- PMT uses LRZB timestamps to synchronize LRZN receptions
- Temperature readings broadcast for LRZN compensation lookup

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
| Sleep | 3h 59m 55s | 10µA | 143µAh |
| Wake + Measure | 8s | 6mA | 13µAh |
| LoRa TX (priority) | 5s | 45mA | 63µAh |
| **Per Cycle** | 4 hours | — | **219µAh** |
| **Annual** | — | — | **480mAh** |
| **Battery Life** | — | — | **~6.2 years** |

**Conservative Rating:** 4+ years (accounts for cold weather, priority TX retries)

---

## 4. Bill of Materials

| Component | Supplier | Part Number | Unit Cost | Qty | Extended |
|-----------|----------|-------------|-----------|-----|----------|
| MCU | Nordic | nRF52840-QIAA-R | $8.50 | 1 | $8.50 |
| LoRa Module | HopeRF | RFM95W-915S2 | $6.50 | 1 | $6.50 |
| PCB | JLCPCB | 4-layer, 1.6mm | $3.20 | 1 | $3.20 |
| Enclosure (ABS) | Custom mold | UV-stabilized | $3.20 | 1 | $3.20 |
| Antenna | PCB trace | 915MHz helical | $0.50 | 1 | $0.50 |
| Battery contacts | Keystone | 92 | $0.40 | 2 | $0.80 |
| Batteries (AA) | Energizer | L91 | $2.50 | 2 | $5.00 |
| NTC Thermistor | Vishay | NTCLE100E3103JB0 | $1.20 | 1 | $1.20 |
| Precision resistors | Vishay | 0.1% 0603 | $0.80 | 4 | $3.20 |
| Seals (O-rings) | Parker | NBR-70 | $0.30 | 3 | $0.90 |
| Passives | Various | 0402/0603 | $2.00 | 1 | $2.00 |
| Calibration fixture | Custom | Lab-grade | $15.00 | amort | $15.00 |
| **TOTAL BOM** | | | | | **$54.30** |

**Target Price:** $54.30/unit at 1,000+ volume

---

## 5. Calibration & Accuracy

### 5.1 Factory Calibration

**Three-Point Calibration Process:**
1. **Dry Reference:** Oven-dried soil (0% VWC, 25°C)
2. **Saturated Reference:** Fully saturated known soil (45% VWC, 25°C)
3. **Temperature Sweep:** Controlled chamber at -10°C, 25°C, 50°C

**Calibration Certificate Includes:**
- Dielectric-to-VWC conversion coefficients
- Temperature compensation lookup table (32-point)
- NTC thermistor beta value
- Unique device ID and QR code
- Factory calibration date and technician

### 5.2 Field Calibration (Recommended)

**Single-Point Field Calibration:**
- Collect sensor reading (VWC + temperature)
- Extract soil sample at same depth
- Gravimetric analysis (oven dry)
- Upload correction factor via PMT
- Improves accuracy to ±1.5%

**Annual Recalibration:**
- Check against gravimetric samples
- Update correction factors
- Document drift rate

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

**LRZB Placement Rationale:**
- **Center LRZB:** Baseline for entire field, unaffected by pivot spray
- **Middle Ring LRZBs:** Validation points at 90° intervals for Kriging
- Temperature compensation source for all 12 LRZN units

### 6.2 Installation Procedure

1. **Site Selection:** Mark location with GPS ±10cm
2. **Soil Prep:** Clear surface debris, loosen if compacted
3. **Insertion:** Push vertically to marked depth line (6-8" recommended)
4. **Engagement:** Twist ¼ turn to engage self-tapping threads
5. **Verification:** LED flash confirms LoRa registration + temp reading
6. **Documentation:** Photo + GPS + depth + initial readings recorded

**Time per Unit:** 2 minutes
**Total LRZB Installation:** 8 minutes (4 LRZB units)

---

## 7. Telemetry Protocol

### 7.1 Payload Format (CBOR)

```c
typedef struct {
    uint32_t device_id;        // 4 bytes: Unique device ID
    uint32_t timestamp;        // 4 bytes: Unix epoch
    uint16_t vwc;              // 2 bytes: VWC × 100 (0-10000)
    int16_t  temperature;      // 2 bytes: Temp × 10 (decidegrees C)
    uint16_t battery_mv;       // 2 bytes: Battery millivolts
    int8_t   rssi;             // 1 byte: Last RSSI to PMT
    uint8_t  quality_score;    // 1 byte: 0-100 measurement confidence
    uint16_t temp_comp_factor; // 2 bytes: Applied correction × 1000
    uint8_t  reserved[2];      // 2 bytes: Future expansion
} lrzb_payload_t;              // 22 bytes total
```

### 7.2 Transmission Schedule

| Mode | Interval | Priority | Max Retries | Backoff |
|------|----------|----------|-------------|---------|
| DORMANT | 4 hours | HIGH | 3 | 15 min |
| ANTICIPATORY | 60 min | HIGH | 3 | 5 min |
| FOCUS RIPPLE | 15 min | HIGH | 5 | 2 min |

**Beacon Synchronization:**
- LRZB transmits at T+0 of each TDMA epoch
- LRZN units synchronize to LRZB transmission
- Temperature broadcast enables LRZN compensation

---

## 8. Temperature Compensation Service

### 8.1 Compensation Algorithm

```python
def compensate_vwc(vwc_raw, soil_temp, calibration_table):
    """
    Apply temperature correction to VWC reading
    Uses factory calibration table for device-specific curve
    """
    temp_idx = int((soil_temp + 40) / 2.8)  # 32-point table
    correction = calibration_table[temp_idx]
    return vwc_raw + (correction / 1000.0)
```

### 8.2 Broadcast Service

**Temperature Broadcast Packet:**
- Broadcast every 4 hours (with regular reading)
- Includes: soil_temp, air_temp (if equipped), timestamp
- Range: All LRZN units within 100m radius
- Purpose: Enable LRZN compensation without temp sensors

---

## 9. Compliance & Certifications

| Standard | Status | Notes |
|----------|--------|-------|
| FCC Part 15.247 | ✅ | 915MHz ISM operation |
| CE Marking | 🔄 | In progress (EU expansion) |
| IP68 Rating | ✅ | Submersible to 1m |
| RoHS 3 | ✅ | Lead-free, compliant materials |
| WEEE | ✅ | Recycling program included |
| NIST Traceable | ✅ | Temp calibration traceable |

---

## 10. Maintenance & Lifecycle

### 10.1 Expected Lifespan

| Component | Lifespan | Replacement |
|-----------|----------|-------------|
| Electronics | 10+ years | Not serviceable |
| NTC Thermistor | 15+ years | Epoxy-encapsulated |
| Battery | 4-6 years | Field replacement |
| Housing | 15+ years | UV-stabilized ABS |
| Sensor drift | <1% / year | Auto-compensated |

### 10.2 Field Maintenance

**Annual Inspection:**
- Visual housing check
- Antenna orientation
- Battery voltage reading
- Temperature accuracy check (ice bath reference)
- Re-install if heaved by frost

**Battery Replacement:**
- Tool: 3mm hex key
- Procedure: Twist open housing, swap AAs, reseal
- Time: 2 minutes
- Post-replacement: Verify temp reading stabilizes

---

## 11. Integration & APIs

### 11.1 Device Registration

```json
{
  "device_type": "LRZB",
  "hardware_version": "1.2",
  "firmware_version": "2.1.4",
  "device_id": "LRZB-E5F6G7H8",
  "field_id": "field-550e8400",
  "installed_at": "2026-03-19T14:30:00Z",
  "gps_location": {
    "lat": 37.456789,
    "lon": -105.987654
  },
  "depth_inches": 8,
  "serves_lrzn_compensation": [
    "LRZN-A1B2C3D4",
    "LRZN-B2C3D4E5",
    "LRZN-C3D4E5F6"
  ],
  "calibration_date": "2026-03-19",
  "warranty_expires": "2029-03-19"
}
```

### 11.2 Data Output

```json
{
  "device_id": "LRZB-E5F6G7H8",
  "timestamp": "2026-03-19T14:30:00Z",
  "vwc": 0.245,
  "vwc_percent": 24.5,
  "soil_temperature_c": 18.3,
  "battery_voltage": 2.92,
  "quality_score": 99,
  "measurement_mode": "DORMANT",
  "temp_compensation_applied": true
}
```

---

## 12. Revision History

| Version | Date | Changes | Author |
|-----------|------|---------|--------|
| 1.0 | 2025-11-01 | Initial release | Engineering |
| 1.1 | 2026-01-15 | Improved temp accuracy (±1→±0.5°C) | RF Team |
| 1.2 | 2026-03-19 | Cost optimization, renamed from LRZ2 | Documentation |

---

## 13. Related Documentation

- `LRZN-SPEC.md` — Basic/density variant
- `PMT-SPEC.md` — Field hub receiving LRZB data
- `VFA-SPEC.md` — Deep vertical profile anchor
- `NETWORK-SPEC.md` — LoRa topology and protocols
- `SFD-SPEC.md` — Single Field Deployment configurations

---

*Proprietary IP of bxthre3 inc. — Confidential*
*© 2026 bxthre3 inc. All rights reserved.*

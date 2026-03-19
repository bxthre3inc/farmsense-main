---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Device Code: PFA
Full Name: Pressure & Flow Analyzer
Version: 1.9
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding implementation MUST be reflected here immediately.
> 3. **AI Agent Compliance**: Agents MUST verify current implementation against this document before proposing changes.
> 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

---

# PFA V1.9: Pressure & Flow Analyzer

## 1. Executive Summary

The PFA (Pressure & Flow Analyzer) is a wellhead-mounted sentinel providing legal-defensible flow measurement, pump electrical signature analysis, and emergency actuation capabilities. As the primary measurement point for water rights compliance, the PFA delivers NIST-traceable flow data suitable for State Engineer reporting and Water Court evidence. The PFA maintains autonomous pump shutdown authority via safety relay for critical fault conditions.

**Primary Role:** Wellhead flow measurement and legal compliance
**Secondary Role:** Predictive pump maintenance via electrical signature analysis
**Tertiary Role:** Emergency safety actuator with autonomous shutdown authority
**Deployment Target:** 1 unit per wellhead

---

## 2. Functional Requirements

### 2.1 Core Capabilities

| Function | Specification | Priority |
|----------|---------------|----------|
| Flow Measurement | ±1.0% accuracy, ultrasonic transit-time | P0 |
| Legal Defensibility | NIST-traceable, "Gold Standard" for State Engineer | P0 |
| Pump Current Analysis | FFT harmonic analysis for predictive maintenance | P1 |
| Wellhead Pressure | Depth-to-water monitoring | P1 |
| Emergency Actuation | SIL 3 safety relay, <50ms response | P0 |
| Telemetry | 900MHz CSS LoRa to PMT | P0 |
| Power | Solar + battery, autonomous operation | P0 |

### 2.2 Critical Functions

1. **Flow Rate Measurement:** ±1.0% accuracy (ultrasonic transit-time)
2. **Pump Electrical Signatures:** Current harmonics for predictive maintenance
3. **Wellhead Pressure Monitoring:** Depth to water tracking
4. **Emergency Pump Shutdown:** Safety relay actuation
5. **Compliance Reporting:** Immutable flow records to Digital Water Ledger

---

## 3. Hardware Architecture

### 3.1 Mechanical Specifications

| Attribute | Specification |
|-----------|---------------|
| Mounting | Wellhead discharge pipe, 4"-12" diameter |
| Enclosure | Polycase WP-21F, NEMA 4X, IP65 |
| Dimensions | 14" × 10" × 6" (main enclosure) |
| Material | Polycarbonate + stainless hardware |
| Solar Panel | Renogy 50W, pole-mounted |
| Battery | Battle Born BB1220 (12V, 20Ah LiFePO₄) |
| Operating Temp | -20°C to +60°C (with heater) |
| Weight | 12 lbs (enclosure) + 28 lbs (battery) |

**Installation Configuration:**
- Clamp-on ultrasonic transducers (non-invasive)
- Split-core CT clamps (non-invasive electrical measurement)
- Vented differential pressure tap (wellhead depth)
- Safety relay in series with pump contactor

### 3.2 Flow Measurement Subsystem

**Sensor: Badger Meter TFX-5000**

| Parameter | Specification |
|-----------|---------------|
| Principle | Ultrasonic transit-time |
| Pipe Size | 4" - 12" (clamp-on) |
| Accuracy | ±1.0% of reading |
| Repeatability | ±0.2% |
| Velocity Range | 0.1 - 40 ft/s |
| Outputs | 4-20mA, pulse, Modbus RTU |
| Display | Integrated LCD with totalizer |
| Calibration | NIST-traceable, annual recertification |

**Legal Defensibility:**
- Matches "Gold Standard" for State Engineer water accounting
- Traceable calibration chain to NIST standards
- Tamper-evident seal on meter housing
- Core evidence for Water Court proceedings

### 3.3 Electrical Signature Analysis

**Current Transformers: Magnelab SCT-0400**

| Parameter | Specification |
|-----------|---------------|
| Current Range | 5 - 400A |
| Accuracy | ±1% |
| Frequency Response | 50/60Hz fundamental + harmonics to 5kHz |
| Installation | Split-core (non-invasive) |
| Output | 0-5V proportional to current |

**Predictive Maintenance Algorithm:**
```
FFT Analysis of Current Waveform:

- Fundamental (60Hz): Normal operating torque
- 2nd Harmonic (120Hz): Bearing wear indicator
- 3rd Harmonic (180Hz): Magnetic saturation/stator issues
- 5th Harmonic (300Hz): Rotor bar problems
- High Frequency (>1kHz): Cavitation signatures

Alert Thresholds:
- Bearing Wear: 2nd harmonic >5% of fundamental
- Cavitation: HF energy >threshold baseline
- Efficiency Drop: >10% from baseline power curve
- Unbalanced Phases: >15% current delta between legs
```

**Maintenance Prediction:**
| Condition | Indicator | Action |
|-----------|-----------|--------|
| Bearing degradation | 2nd harmonic rise | Schedule inspection |
| Impeller cavitation | HF energy spike | Reduce pump speed |
| Rotor bar issues | 5th harmonic | Major overhaul required |
| Phase imbalance | Current delta | Electrical check |

### 3.4 Actuation System

**Safety Relay: Omron G9SE-221-T05**

| Parameter | Specification |
|-----------|---------------|
| Contacts | 2× SPST-NO |
| Rating | 30A @ 240VAC |
| Response Time | <50ms |
| SIL Rating | SIL 3 (IEC 61508) |
| Force-Guided | Mechanical interlock prevents welding |
| Reset | Manual only (no automatic restart) |

**Reflex Logic Table:**

| Condition | Sensor | Threshold | Action |
|-----------|--------|-----------|--------|
| PMT Stall Command | PMT IMU | >3g shock | ACTUATE_STOP |
| Line Pressure Loss | PBLTX | <5 PSI | ACTUATE_STOP |
| Saturation Detected | VFA | >95% VWC at 36" | ACTUATE_STOP |
| Cavitation Signature | CT Clamps | HF >threshold | ACTUATE_STOP + alert |
| Power Anomaly | CT Clamps | >110% or <85% | ACTUATE_STOP |
| Manual Emergency | PMT/Cloud | Emergency flag | ACTUATE_STOP |

**Actuation Authority:**
- PFA has highest priority shutdown authority
- Overrides all other pump control systems
- Manual reset required after any actuation
- Event logged to Digital Water Ledger with timestamp

### 3.5 Wellhead Depth Measurement

**Sensor: Dwyer PBLTX**

| Parameter | Specification |
|-----------|---------------|
| Principle | Vented differential pressure |
| Range | 0 - 300 ft water depth |
| Accuracy | ±0.25% full scale |
| Material | 316 stainless steel |
| Output | 4-20mA |
| Vented | Atmospheric reference via desiccant tube |

**Applications:**
- Static water level monitoring
- Drawdown tracking during pumping
- Aquifer health assessment
- Well efficiency calculations

### 3.6 Processing Subsystem

**MCU: Nordic Semiconductor nRF52840-QIAA**

| Feature | Specification |
|---------|-------------|
| Core | ARM Cortex-M4 @ 64MHz |
| Flash | 1MB |
| RAM | 256KB |
| ADC | 12-bit SAR (multiple channels) |
| Crypto | Cryptocell CC-310 for AES-256 |
| Interfaces | SPI, I2C, UART, Modbus RTU |

**Peripheral Mapping:**

| Interface | Device | Purpose |
|-----------|--------|---------|
| Modbus RTU | TFX-5000 | Flow rate, totalizer |
| 4-20mA ADC | PBLTX | Depth to water |
| Analog ADC ×3 | SCT-0400 | Current on L1, L2, L3 |
| Digital Out | G9SE-221 | Safety relay actuation |
| SPI | RFM95W | LoRa telemetry |

### 3.7 Communication Subsystem

**LoRa Module: HopeRF RFM95W-915S2**

| Parameter | Specification |
|-----------|---------------|
| Frequency | 915MHz ISM |
| Bandwidth | 125kHz |
| Spreading Factor | SF9 |
| TX Power | +20dBm (100mW) |
| Range | 1km+ to PMT |
| Priority Channel | Emergency actuation = immediate TX |

**Priority Message Types:**
1. **EMERGENCY_STOP** — Immediate, max power, max retries
2. **FLOW_ALARM** — High priority, flow threshold exceeded
3. **PUMP_STATUS** — Normal status, 15-minute interval
4. **MAINTENANCE_ALERT** — Predictive maintenance warning

### 3.8 Power Subsystem

**Solar: Renogy 50W Panel**

| Attribute | Specification |
|-----------|---------------|
| Power | 50W peak |
| Voltage | 18.6V Vmp |
| Current | 2.69A Imp |
| Efficiency | 19.8% |
| Cells | Monocrystalline |

**Battery: Battle Born BB1220**

| Attribute | Specification |
|-----------|---------------|
| Chemistry | LiFePO₄ (Lithium Iron Phosphate) |
| Capacity | 20Ah @ 12.8V = 256Wh |
| Cycles | 3000+ @ 80% DOD |
| Temperature | -20°C to +60°C |
| BMS | Integrated, protects against all fault conditions |
| Weight | 6 lbs |

**Power Budget:**

| Component | Active | Sleep | Daily Energy |
|-----------|--------|-------|--------------|
| MCU + LoRa | 45mA @ 3.3V | 15µA | 3.6Wh |
| TFX-5000 | 5mA @ 12V | 2mA | 1.4Wh |
| Heater (cold) | 3A @ 12V | — | 18Wh (seasonal) |
| **Total** | — | — | **5-23Wh / day** |
| **Solar Production** | — | — | **150Wh / day** (winter) |

---

## 4. Bill of Materials

| Component | Supplier | Part Number | Unit Cost | Qty | Extended |
|-----------|----------|-------------|-----------|-----|----------|
| Flow Meter | Badger Meter | TFX-5000-4 | $425.00 | 1 | $425.00 |
| CT Clamps | Magnelab | SCT-0400-400 | $45.00 | 3 | $135.00 |
| Depth Sensor | Dwyer | PBLTX-40-30 | $285.00 | 1 | $285.00 |
| Safety Relay | Omron | G9SE-221-T05 | $89.00 | 1 | $89.00 |
| MCU | Nordic | nRF52840-QIAA | $8.50 | 1 | $8.50 |
| Cryptocell | Nordic | CC-310 | $3.00 | 1 | $3.00 |
| LoRa Module | HopeRF | RFM95W-915S2 | $15.00 | 1 | $15.00 |
| Enclosure | Polycase | WP-21F | $78.00 | 1 | $78.00 |
| Solar Panel | Renogy | RNG-50D | $65.00 | 1 | $65.00 |
| Battery | Battle Born | BB1220 | $245.00 | 1 | $245.00 |
| Charge Controller | Victron | SmartSolar MPPT 75/10 | $95.00 | 1 | $95.00 |
| Heater | Omega | KH-505/5-P | $28.00 | 1 | $28.00 |
| Cable/Connectors | Various | — | $85.00 | 1 | $85.00 |
| PCB Assembly | JLCPCB | Custom 4-layer | $95.00 | 1 | $95.00 |
| Calibration | — | NIST-traceable | $125.00 | 1 | $125.00 |
| **TOTAL BOM** | | | | | **$1,886.50** |

**Notes:**
- Flow meter is largest cost component ($425)
- Annual recalibration: $125/year (not included in BOM)
- Expected lifespan: 10+ years (battery replacement at year 8)

---

## 5. Calibration & Legal Defensibility

### 5.1 Factory Calibration

**Badger TFX-5000 Calibration:**
- NIST-traceable calibration certificate
- Zero-flow baseline
- Span calibration at multiple flow points
- Temperature compensation curve
- Certificate valid for 12 months

### 5.2 Field Recalibration

**Annual Recertification:**
1. Remove meter, ship to certified lab
2. Flow bench comparison to NIST-traceable standard
3. Issuance of new calibration certificate
4. Re-install with tamper-evident seal
5. Update Digital Water Ledger with certificate hash

**In-Situ Verification:**
- Portable clamp-on meter comparison (quarterly)
- Volumetric tank test (annual)
- Document all verification in compliance log

---

## 6. Deployment Specifications

### 6.1 Installation Procedure

1. **Mount Enclosure:** Wellhead post or wall, south-facing for solar
2. **Install Transducers:** Clamp on discharge pipe at 12 o'clock and 6 o'clock
3. **Install CT Clamps:** Split-core around L1, L2, L3 pump leads
4. **Install Depth Tap:** Tee into wellhead vent or dedicated tap
5. **Wire Safety Relay:** Series with pump contactor coil
6. **Connect Solar:** Panel to charge controller to battery
7. **Commission:** Pair with PMT, verify all readings
8. **Calibrate:** Zero-flow check, span verification

**Installation Time:** 2 hours (certified technician)

### 6.2 Regulatory Compliance

**State Engineer Requirements:**
- NIST-traceable flow measurement
- Daily totalizer readings
- Annual recalibration
- Tamper-evident seals
- Digital Water Ledger integration

**Water Court Evidence:**
- Immutable flow records with SHA-256 hashing
- GPS timestamp on all readings
- Chain of custody for calibration certificates
- PBFT consensus for critical events

---

## 7. Telemetry Protocol

### 7.1 Payload Format (CBOR)

```c
typedef struct {
    uint32_t device_id;
    uint32_t timestamp;
    uint32_t flow_totalizer_gal;   // Lifetime gallons
    uint16_t flow_rate_gpm;        // Current GPM × 10
    uint16_t depth_to_water_ft;  // × 100 (2 decimal places)
    int16_t  current_l1_a;       // L1 current × 10
    int16_t  current_l2_a;       // L2 current × 10
    int16_t  current_l3_a;       // L3 current × 10
    uint16_t pump_power_kw;      // Calculated × 100
    uint16_t battery_voltage;    // × 100
    uint8_t  relay_status;       // 0=normal, 1=actuated
    uint8_t  pump_running;       // Boolean
    uint8_t  alert_flags;        // Bitfield
    int8_t   rssi;
    uint8_t  quality_score;
} pfa_payload_t;                 // 32 bytes
```

### 7.2 Transmission Schedule

| Condition | Interval | Priority |
|-----------|----------|----------|
| Normal operation | 15 minutes | Normal |
| Pump active | 5 minutes | High |
| Flow threshold exceeded | Immediate | Critical |
| Emergency actuation | Immediate + 3 retries | Emergency |

---

## 8. Maintenance & Lifecycle

### 8.1 Expected Lifespan

| Component | Lifespan | Maintenance |
|-----------|----------|-------------|
| Flow meter electronics | 15+ years | Annual recalibration |
| Ultrasonic transducers | 20+ years | Clean annually |
| CT clamps | 10+ years | Verify clamp torque |
| Safety relay | 10+ years | Test quarterly |
| Battery | 8-10 years | Replace when <80% capacity |
| Solar panel | 25+ years | Clean quarterly |

### 8.2 Maintenance Schedule

| Interval | Action |
|----------|--------|
| Weekly | Visual inspection, solar panel clean |
| Monthly | Battery voltage check, alert log review |
| Quarterly | Safety relay test, CT clamp check |
| Annually | Flow meter recalibration, depth sensor check |

---

## 9. Integration & APIs

### 9.1 Device Registration

```json
{
  "device_type": "PFA",
  "hardware_version": "1.9",
  "firmware_version": "2.3.1",
  "device_id": "PFA-9876WXYZ",
  "field_id": "field-550e8400",
  "well_id": "well-42-12345",
  "installed_at": "2026-03-19T09:00:00Z",
  "gps_location": {
    "lat": 37.456789,
    "lon": -105.987654
  },
  "flow_meter": {
    "model": "TFX-5000-4",
    "serial": "BM123456",
    "calibration_date": "2026-03-15",
    "calibration_expires": "2027-03-15",
    "nist_traceable": true
  },
  "pump": {
    "hp": 75,
    "phases": 3,
    "rated_gpm": 850
  },
  "warranty_expires": "2031-03-19"
}
```

### 9.2 Compliance Data Output

```json
{
  "device_id": "PFA-9876WXYZ",
  "timestamp": "2026-03-19T14:30:00Z",
  "compliance": {
    "flow_totalizer_gal": 1523456789,
    "flow_rate_gpm": 847.5,
    "daily_volume_af": 2.34,
    "depth_to_water_ft": 145.32,
    "drawdown_ft": 12.5,
    "pump_efficiency_pct": 78.3
  },
  "ledger_hash": "a3f7b2c8d9e1f4a5b6c7d8e9f0a1b2c3",
  "pbft_confirmed": true
}
```

---

## 10. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-05-01 | Initial release | Engineering |
| 1.5 | 2025-09-15 | Added electrical signature analysis | Hardware |
| 1.8 | 2026-01-10 | Upgraded to SIL 3 relay | Safety |
| 1.9 | 2026-03-19 | Cost optimization, documentation standard | Documentation |

---

## 11. Related Documentation

- `PMT-SPEC.md` — Field hub coordinating PFA data
- `VFA-SPEC.md` — Deep soil moisture for saturation detection
- `SFD-SPEC.md` — Single Field Deployment configurations
- `CLOUD-SPEC.md` — Digital Water Ledger integration
- `MASTER_EVIDENCE_SPEC.md` — Legal defensibility requirements

---

*Proprietary IP of bxthre3 inc. — Confidential*
*© 2026 bxthre3 inc. All rights reserved.*

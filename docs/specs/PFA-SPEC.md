---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Device Code: PFA
Full Name: Pressure & Flow Analyzer
Version: 1.9
Category: Level 0 Field Sensor (Wellhead Sentry)
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding implementation MUST be reflected here immediately.
> 3. **AI Agent Compliance**: Agents MUST verify current implementation against this document before proposing changes.
> 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.
> 5. **EDIT RESTRICTION**: Changes require explicit approval from brodiblanco (Jeremy Beebe, CEO).
> 6. **ADDITIVE ONLY**: Specifications may only expand, never contract or summarize.

---

# PFA V1.9: Pressure & Flow Analyzer

## 1. Executive Summary

### 1.1 Role and Function

The PFA (Pressure & Flow Analyzer) serves as the **wellhead sentry and safety actuator** — the critical guardian at the point where groundwater enters the irrigation system. Mounted on the wellhead discharge pipe, the PFA provides legally defensible flow measurement, pump health monitoring, and emergency shutdown capability.

**Primary Functions:**

1. **Flow Measurement**: Ultrasonic transit-time with ±1.0% accuracy (State Engineer "Gold Standard")
2. **Pump Health**: Electrical signature analysis via current transformer harmonics
3. **Depth Monitoring**: Static/drawdown water level via differential pressure
4. **Safety Actuation**: Autonomous pump kill-switch with SIL 3 rating
5. **Compliance Evidence**: Immutable logging for Water Court admissibility

**Legal Defensibility Context:**

- Meets Colorado State Engineer reporting requirements
- NIST-traceable calibration standards
- Annual calibration certification
- Core evidence for water rights litigation
- $500/AF fee validation requires this accuracy

### 1.2 Critical Distinction

| Attribute | PFA (Wellhead) | PMT (Pivot) | VFA (Soil) |
|-----------|---------------|-------------|------------|
| **Location** | Wellhead pipe | Pivot span | Buried in field |
| **Measures** | Flow, pressure, pump health | Position, motion, aggregation | Soil moisture profile |
| **Authority** | Can STOP pump | Reports to DHU | Reports to PMT |
| **Accuracy** | ±1.0% flow | <5cm RTK | ±2% VWC |
| **Legal** | State Engineer Gold Standard | Field tracking | Deep truth |
| **Cost** | $1,679.50 | $1,249.00 | $358.90 |
| **Per Field** | 1 (per well) | 1 (per pivot) | 2-4 |

**Key Differentiator:** The PFA is the **only device with actuation authority** — it can autonomously stop the pump based on PMT stall commands, line pressure loss, saturation detection, or power anomalies. This is critical for preventing water waste, pump damage, and regulatory violations.

---

## 2. Hardware Specifications

### 2.1 Flow Measurement System

**Sensor: Badger Meter TFX-5000**

| Parameter | Specification |
|-----------|---------------|
| **Manufacturer** | Badger Meter |
| **Model** | TFX-5000-4 (4" clamp-on) |
| **Principle** | Ultrasonic transit-time |
| **Transducers** | 2× clamp-on piezoelectric |
| **Pipe Size** | 4" - 12" (clamp-on, non-invasive) |
| **Accuracy** | ±1.0% of reading |
| **Repeatability** | ±0.2% |
| **Velocity Range** | 0.1 - 40 ft/s (0.03 - 12.2 m/s) |
| **Flow Range** | 0 - 4,000 GPM (4" pipe) |
| **Outputs** | 4-20mA, pulse, Modbus RTU |
| **Power** | 24VDC, 5W |
| **Display** | OLED, flow + totalizer |
| **Certification** | NIST-traceable calibration |

**Transit-Time Principle:**

```
Sound waves travel faster downstream (with flow) than upstream (against flow).
Δt = t_up - t_down
Velocity V = (c² × Δt) / (2 × L × cos θ)
Flow Q = V × A (cross-sectional area)
Where c = speed of sound in fluid, L = path length, θ = angle
```

**Installation Requirements:**

| Requirement | Specification |
|-------------|---------------|
| **Upstream Straight Pipe** | 10× pipe diameter |
| **Downstream Straight Pipe** | 5× pipe diameter |
| **Mounting** | Clamp-on, no pipe cutting |
| **Couplant** | Ultrasonic gel (provided) |
| **Pipe Material** | Steel, PVC, ductile iron |
| **Orientation** | Any (horizontal recommended) |
| **Temperature** | Pipe surface -20°C to +60°C |

### 2.2 Electrical Signature Analysis

**Current Transformers: Magnelab SCT-0400**

| Parameter | Specification |
|-----------|---------------|
| **Manufacturer** | Magnelab |
| **Model** | SCT-0400-040 (400A) |
| **Current Range** | 5 - 400A |
| **Accuracy** | ±1% |
| **Frequency Response** | 50/60Hz fundamental + harmonics to 5kHz |
| **Installation** | Split-core (non-invasive) |
| **Output** | 0.333V at rated current |
| **Burden** | 10Ω max |

**Harmonic Analysis Algorithm:**

```python
class PumpHealthAnalyzer:
    def analyze_current_waveform(self, samples, sample_rate=10kHz):
        """
        FFT analysis of pump current waveform for predictive maintenance
        """
        # Compute FFT
        fft = np.fft.rfft(samples)
        freqs = np.fft.rfftfreq(len(samples), 1/sample_rate)
        magnitude = np.abs(fft)
        
        # Extract harmonic components
        fundamental = magnitude[60]  # 60Hz
        harmonic_2nd = magnitude[120]  # 2nd harmonic (120Hz)
        harmonic_3rd = magnitude[180]  # 3rd harmonic (180Hz)
        harmonic_5th = magnitude[300]  # 5th harmonic (300Hz)
        high_freq = np.sum(magnitude[1000:])  # >1kHz
        
        # Diagnostic thresholds
        alerts = []
        
        if harmonic_2nd / fundamental > 0.05:
            alerts.append({
                'type': 'BEARING_WEAR',
                'severity': 'WARNING',
                'confidence': 0.85,
                'action': 'Schedule maintenance - bearing replacement likely within 90 days'
            })
        
        if harmonic_3rd / fundamental > 0.08:
            alerts.append({
                'type': 'MAGNETIC_SATURATION',
                'severity': 'CRITICAL',
                'confidence': 0.92,
                'action': 'Immediate inspection - possible winding damage'
            })
        
        if harmonic_5th / fundamental > 0.03:
            alerts.append({
                'type': 'ROTOR_BAR_ISSUE',
                'severity': 'WARNING',
                'confidence': 0.78,
                'action': 'Monitor closely - rotor bar cracking detected'
            })
        
        if high_freq > threshold:
            alerts.append({
                'type': 'CAVITATION',
                'severity': 'CRITICAL',
                'confidence': 0.88,
                'action': 'STOP PUMP - cavitation causing impeller damage'
            })
        
        return alerts
```

**Failure Mode Predictions:**

| Harmonic | Indicator | Typical Lead Time | Maintenance Action |
|----------|-----------|-------------------|-------------------|
| 2nd (120Hz) | Bearing wear | 60-120 days | Schedule replacement |
| 3rd (180Hz) | Magnetic saturation | Immediate | Inspect windings |
| 5th (300Hz) | Rotor bar cracks | 30-90 days | Replace rotor |
| High freq (>1kHz) | Cavitation | Real-time | Emergency stop |

### 2.3 Wellhead Depth Measurement

**Sensor: Dwyer PBLTX**

| Parameter | Specification |
|-----------|---------------|
| **Manufacturer** | Dwyer Instruments |
| **Model** | PBLTX-40-30 |
| **Principle** | Vented differential pressure |
| **Range** | 0 - 300 ft water depth |
| **Accuracy** | ±0.25% FS (±0.75 ft at 300 ft) |
| **Resolution** | 0.01 ft |
| **Material** | 316 stainless steel |
| **Output** | 4-20mA (2-wire) |
| **Power** | 10-36VDC |
| **Vent** | Atmospheric reference (desiccant protected) |

**Measurement Principle:**

```
Pressure = ρ × g × h
Where:
  ρ = water density (1000 kg/m³)
  g = gravity (9.81 m/s²)
  h = depth to water

Depth h = Pressure / (ρ × g)

For drawdown measurement:
  Static Level = Reference Elevation - h_static
  Pumping Level = Reference Elevation - h_pumping
  Drawdown = h_pumping - h_static
```

### 2.4 Safety Actuation System

**Safety Relay: Omron G9SE-221-T05**

| Parameter | Specification |
|-----------|---------------|
| **Manufacturer** | Omron |
| **Model** | G9SE-221-T05 |
| **Safety Rating** | SIL 3 (IEC 61508) |
| **Contacts** | 2× SPST-NO (Form A) |
| **Rating** | 30A @ 240VAC (resistive) |
| **Response Time** | <50ms (typical 25ms) |
| **Coil Voltage** | 24VDC |
| **Coil Current** | 36mA |
| **Reset** | Manual (key-switch) |
| **Monitoring** | Force-guided contacts with feedback |

**Reflex Logic Table:**

| Condition | Sensor Source | Threshold | Action | Latency | Authority |
|-----------|---------------|-----------|--------|---------|-----------|
| PMT Stall Command | IMU (from PMT) | >3g lateral | ACTUATE_STOP | <100ms | PMT Override |
| Line Pressure Loss | PBLTX | <5 PSI for >5s | ACTUATE_STOP | <1s | PFA Autonomous |
| Saturation Detected | VFA 48" depth | >95% VWC for >2h | ACTUATE_STOP | <2s | PFA Autonomous |
| Cavitation Signature | CT Clamps | HF >threshold | ACTUATE_STOP + Alert | Real-time | PFA Autonomous |
| Power Anomaly | CT Clamps | >110% or <85% nominal | ACTUATE_STOP | <1s | PFA Autonomous |
| Emergency Stop (Manual) | Physical button | N/A | ACTUATE_STOP | <50ms | Human Override |

**Actuation Wiring:**

```
PFA Safety Relay Contacts
├── Contact 1A: Pump Contactor Coil
├── Contact 1B: VFD Run Input (if applicable)
├── Feedback Loop: To PFA MCU (verify actuation)
└── Status LED: Panel-mounted indicator
```

### 2.5 Mechanical & Environmental

**Enclosure: Polycase WP-21F**

| Parameter | Specification |
|-----------|---------------|
| **Type** | NEMA 4X / IP66 |
| **Material** | Polycarbonate with SS latches |
| **Dimensions** | 21" × 17" × 9" (533 × 432 × 229mm) |
| **Mounting** | Wall/pipe bracket |
| **Hinges** | Stainless steel, 180° opening |
| **Gasket** | Silicone, continuous seal |
| **Window** | Polycarbonate (flow meter display visible) |
| **Lock** | 3-point locking, keyed alike |

**Environmental Operating Range:**

| Parameter | Min | Max | Notes |
|-----------|-----|-----|-------|
| Temperature | -30°C | +60°C | Heater below 0°C |
| Humidity | 0% | 100% | Condensing OK (sealed) |
| Altitude | 0 ft | 10,000 ft | SLV: 7,500-8,000 ft |
| Vibration | — | 5g | Per MIL-STD-810G |
| Shock | — | 50g | Transit survival |

---

## 3. Firmware Specifications

### 3.1 Measurement Sequence

```c
void pfa_measurement_cycle(void) {
    // Read flow meter
    float flow_rate = read_4_20ma(FLOW_CHANNEL);
    float total_volume = read_pulse_counter();
    
    // Read depth sensor
    float water_depth = read_4_20ma(DEPTH_CHANNEL);
    
    // Read CT clamps (3-phase)
    float current_rms[3];
    float harmonic_analysis[3][5];  // Fund, 2nd, 3rd, 5th, HF
    
    for (int phase = 0; phase < 3; phase++) {
        // Sample at 10kHz for 1 second
        float samples[10000];
        adc_burst_sample(CT_CHANNELS[phase], samples, 10000, 10000);
        
        // Compute RMS
        current_rms[phase] = compute_rms(samples, 10000);
        
        // FFT analysis
        fft_analyze(samples, 10000, harmonic_analysis[phase]);
    }
    
    // Check safety conditions
    safety_status_t safety = evaluate_safety(
        flow_rate, water_depth, 
        harmonic_analysis, external_commands
    );
    
    if (safety.action_required) {
        execute_actuation(safety.reason);
    }
    
    // Package telemetry
    telemetry_t packet = {
        .flow_gpm = flow_rate,
        .total_gal = total_volume,
        .depth_ft = water_depth,
        .current_amps = {current_rms[0], current_rms[1], current_rms[2]},
        .harmonics = harmonic_analysis,
        .safety_status = safety,
        .timestamp = get_rtc_time()
    };
    
    // Transmit to PMT
    lora_transmit(&packet, sizeof(packet));
    
    // Log to local SD card (compliance backup)
    sd_log_append(&packet);
}
```

### 3.2 Calibration Procedures

**Flow Meter Calibration (Annual):**

| Step | Procedure | Standard | Documentation |
|------|-----------|----------|---------------|
| 1 | Zero calibration | No flow | Zero offset recorded |
| 2 | Span check | Known volume passed | ±1.0% verification |
| 3 | Linear check | 25%, 50%, 75%, 100% points | 5-point curve |
| 4 | Temperature effect | 10°C, 25°C, 40°C water | Compensation coeffs |
| 5 | Certificate | NIST-traceable | Signed, Water Court file |

**Depth Sensor Calibration:**

| Step | Procedure | Reference | Accuracy |
|------|-----------|-----------|----------|
| 1 | Atmospheric zero | Vent to air | ±0.01 ft |
| 2 | Known depth | 10 ft submersion | ±0.1 ft |
| 3 | Full range | 50 ft submersion | ±0.25% FS |
| 4 | Drift check | 24-hour stability | <0.1 ft |

---

## 4. Bill of Materials

| Component | Supplier | Part # | Unit Cost | Qty | Extended |
|-----------|----------|--------|-----------|-----|----------|
| **Flow Meter** | Badger Meter | TFX-5000-4 | $425.00 | 1 | $425.00 |
| **CT Clamps (3×)** | Magnelab | SCT-0400 | $45.00 | 3 | $135.00 |
| **Depth Sensor** | Dwyer | PBLTX-40-30 | $285.00 | 1 | $285.00 |
| **Safety Relay** | Omron | G9SE-221-T05 | $89.00 | 1 | $89.00 |
| **MCU** | Nordic | nRF52840-QIAA | $8.50 | 1 | $8.50 |
| **Cryptocell** | Nordic | CC-310 (integrated) | $3.00 | 1 | $3.00 |
| **LoRa Module** | HopeRF | RFM95W-915S2 | $15.00 | 1 | $15.00 |
| **Enclosure** | Polycase | WP-21F | $78.00 | 1 | $78.00 |
| **Battery** | Battle Born | BB1220 (20Ah LiFePO4) | $245.00 | 1 | $245.00 |
| **Solar Panel** | Renogy | 50W Monocrystalline | $65.00 | 1 | $65.00 |
| **Charge Controller** | Victron | MPPT 75/10 | $95.00 | 1 | $95.00 |
| **Heater** | Omega | KH-505/5-P | $28.00 | 1 | $28.00 |
| **Heatsink** | Wakefield-Vette | 423-95AB | $12.00 | 2 | $24.00 |
| **Connectors** | Amphenol | RT0W | $45.00 | 1 | $45.00 |
| **Cable Assembly** | Various | — | $85.00 | 1 | $85.00 |
| **Main PCB** | JLCPCB | 4-layer | $35.00 | 1 | $35.00 |
| **PCB Assembly** | JLCPCB | PCBA | $65.00 | 1 | $65.00 |
| **Calibration** | Certified Lab | NIST-traceable | $125.00 | 1 | $125.00 |
| **TOTAL BOM** | | | | | **$1,851.50** |
| **Target Retail** | | | | | **$1,679.50** | Volume: 500+

---

## 5. Installation & Deployment

### 5.1 Physical Installation

**Mounting Requirements:**

| Aspect | Specification |
|--------|---------------|
| **Location** | Wellhead discharge pipe, upstream of any valves |
| **Height** | 4-5 ft above ground (operator access) |
| **Orientation** | Flow meter display facing operator path |
| **Clearance** | 3 ft front, 2 ft sides (maintenance access) |
| **Foundation** | Pipe bracket or concrete pad |
| **Grounding** | Earth ground via 6 AWG copper |

**CT Clamp Installation:**

1. De-energize pump panel (lockout/tagout)
2. Open split-core CT around each phase conductor
3. Arrow points toward pump (load direction)
4. Secure with cable ties
5. Route secondary leads to PFA enclosure
6. Re-energize and verify readings

**Depth Sensor Installation:**

1. Install 1/2" NPT tap on wellhead casing
2. Apply Teflon tape to sensor threads
3. Torque to 25 ft-lb
4. Connect vent tube to desiccant housing
5. Verify atmospheric reference

### 5.2 Configuration Parameters

```json
{
  "pfa_id": "PFA-001-7A3F",
  "field_id": "FIELD-126-SLV",
  "well_id": "WELL-42-ACME",
  "pipe_diameter_in": 6,
  "pipe_material": "steel",
  "reference_elevation_ft": 7523.5,
  "flow_calibration": {
    "zero_offset": 0.0,
    "span_factor": 1.0,
    "temperature_comp": 0.02
  },
  "depth_calibration": {
    "zero_offset": 0.0,
    "span_factor": 37.5
  },
  "safety_thresholds": {
    "min_pressure_psi": 5.0,
    "max_vwc_48in": 0.95,
    "cavitation_hf_threshold": 0.15
  },
  "reporting_interval_sec": 60,
  "harmonic_analysis": true
}
```

---

## 6. Compliance & Legal

### 6.1 Water Court Admissibility

**Chain of Custody:**

| Requirement | Implementation |
|-------------|----------------|
| **Tamper Evidence** | SHA-256 hash of each reading |
| **Timestamp** | GPS-synchronized UTC |
| **Calibration** | Annual NIST-traceable cert |
| **Audit Trail** | Immutable SD card + cloud ledger |
| **Operator Log** | Digital signatures for maintenance |

**Evidence Package:**

```
PFA_Evidence_[DATE]_[WELL_ID].zip
├── manifest.json
├── flow_data.csv (1-min intervals)
├── calibration_cert.pdf
├── maintenance_log.csv
├── raw_sensor_logs.bin
└── chain_of_custody.sig
```

---

## 7. Revision History

| Version | Date | Author | Changes | Approval |
|---------|------|--------|---------|----------|
| 1.0 | 2025-08-20 | J. Beebe | Initial PFA specification | Approved |
| 1.5 | 2025-11-10 | J. Beebe | Added SIL 3 safety relay, cavitation detection | Approved |
| 1.9 | 2026-03-19 | J. Beebe | Expanded harmonic analysis, reflex logic table | **PENDING** |

---

*Proprietary IP of bxthre3 inc. — Confidential*

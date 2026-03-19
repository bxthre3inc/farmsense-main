---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Device Code: LRZB
Full Name: Lateral Root Zone Beacon
Version: 1.2
Category: Level 0 Field Sensor (Reference Grade)
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

# LRZB V1.2: Lateral Root Zone Beacon

## 1. Executive Summary

### 1.1 Role and Function

The LRZB (Lateral Root Zone Beacon) is the **reference-grade** member of the Lateral Root Zone Surveyor family, providing calibrated ground-truth validation for the larger network of LRZN nodes. As a "Beacon" node, the LRZB includes temperature sensing and enhanced calibration precision, serving as an anchor point for Kriging algorithms and cross-sensor validation.

**Primary Functions:**

1. Measure soil VWC **and temperature** at single configurable depth
2. Provide ±2% VWC accuracy (vs ±3% for LRZN) with ±0.5°C temperature precision
3. Serve as calibration anchor for field-interpolated data
4. Enable temperature-compensated moisture calculations
5. Validate LRZN readings through cross-sensor correlation
6. Support frost-depth monitoring and soil thermal dynamics

**Deployment Context:**

- Standard density: 4 LRZB per field + 12 LRZN (16 total nodes)
- Strategic placement: Center pivot, mid-field cardinal points
- Target MTBF: 60,000 hours (6.8 years)
- Unit economics: $54.30 BOM cost for reference-grade measurement

### 1.2 LRZB vs LRZN Distinction

| Attribute | LRZB (Reference/Beacon) | LRZN (Basic/Node) |
|-----------|-------------------------|-------------------|
| **Role** | Calibration anchor | Spatial density |
| **Sensors** | VWC + Temperature | VWC only |
| **VWC Accuracy** | ±2% | ±3% |
| **Temperature** | ±0.5°C | Not measured |
| **Calibration** | Field-calibrated to VFA | Factory only |
| **BOM Cost** | $54.30 | $29.00 |
| **Density** | 4 per field | 12 per field |
| **Purpose** | Ground-truth validation | Kriging interpolation |
| **Temp Compensation** | Yes (VWC auto-corrected) | No |

**Key Differentiator:** The LRZB's temperature sensor enables real-time VWC compensation using the dielectric temperature coefficient, eliminating seasonal drift that affects uncompensated capacitive sensors.

### 1.3 Critical Success Factors

- **Accuracy**: ±2% VWC enables confident ground-truth anchoring
- **Temperature Correlation**: Soil thermal dynamics inform moisture migration models
- **Validation Role**: 4 beacons provide statistical confidence for 12 nodes
- **Frost Monitoring**: Temperature tracking enables freeze/thaw cycle analysis
- **Longevity**: 6+ year battery life matches crop rotation cycles

---

## 2. Hardware Specifications

### 2.1 Mechanical Design

**Alpha-Sled Form Factor (Identical to LRZN):**

| Attribute | Specification |
|-----------|---------------|
| **Outer Shell Material** | HDPE SDR9 (High-Density Polyethylene) |
| **Outer Shell Dimensions** | 2.067" OD × 48" L (52.5mm × 1219mm) |
| **Inner Sled Material** | CHDPE (Conductive HDPE, ESD-safe) |
| **Inner Sled Dimensions** | 50mm OD × 48" L |
| **Installation Method** | Buried vertically, flush with soil surface |
| **Taper Tip** | Friction-molded, monolithic HDPE weld |
| **Lifespan** | 40+ years (shell) / 10-year electronics refresh |
| **Extraction Method** | Stainless steel cable, manual or winch-assisted |
| **Nitrogen Purge** | +5 PSI dry N₂ pressurization |
| **Seal Rating** | IP68 (submersible to 2m indefinitely) |

**Temperature Sensor Integration:**

| Parameter | Value |
|-----------|-------|
| **Sensor Type** | Digital temperature (I²C) |
| **Sensor Model** | Sensirion SHT31-DIS-F |
| **Location** | Mounted on inner sled PCB, thermally coupled to shell |
| **Thermal Path** | CHDPE shell → sensor (time constant: 15 minutes) |
| **Accuracy** | ±0.3°C (0-65°C range) |
| **Resolution** | 0.01°C |
| **Response Time** | τ = 15 min (soil-to-sensor) |

### 2.2 Electrical Architecture

**Power System (Enhanced vs LRZN):**

| Component | LRZN Spec | LRZB Spec | Delta |
|-----------|-----------|-----------|-------|
| **Primary Battery** | 3× 21700 | 3× 21700 | Same |
| **Capacity** | 18.5Wh | 18.5Wh | Same |
| **Temp Sensor Power** | N/A | 0.8µA (sleep), 2mA (active) | +0.5% |
| **Calibration Memory** | Basic | Extended (256B → 1KB) | +512B |

**Power Budget Analysis (LRZB-specific):**

| Mode | Base (LRZN) | Temp Overhead | Total | Battery Life |
|------|-------------|---------------|-------|--------------|
| DORMANT | 7.24mWh/day | +0.5mWh | 7.74mWh | 5.8 years |
| ANTICIPATORY | 360mWh/day | +2.4mWh | 362mWh | 2.8 years |
| FOCUS RIPPLE | 1.08Wh/day | +7.2mWh | 1.09Wh | 17 months |
| COLLAPSE | 8.64Wh/day | +28.8mWh | 8.67Wh | 2.1 months |

**Temperature Measurement Impact:**

- SHT31 operates at 0.8µA idle (minimal impact on DORMANT)
- 2mA during 10ms measurement burst (negligible overhead)
- Temperature measured concurrent with VWC (no additional wake time)

### 2.3 PCB Design

**PCB Enhancements over LRZN:**

| Feature | LRZN | LRZB | Notes |
|---------|------|------|-------|
| **Temp Sensor** | Not populated | SHT31-DIS-F | I²C interface |
| **ADC Channels** | 1 (dielectric) | 2 (+temperature) | P0.02, P0.03 |
| **Calibration Memory** | 256B EEPROM | 1KB EEPROM | Field calibration storage |
| **Gold Plating** | Standard ENIG | Thick ENIG (2µ") | Extended life |

**Enhanced GPIO Pinout:**

| Pin | Function | Direction | Notes |
|-----|----------|-----------|-------|
| P0.02 | ADC0 (dielectric) | Input | 12-bit SAR ADC |
| **P0.03** | **ADC1 (temperature)** | **Input** | **SHT31 analog backup** |
| P0.04 | LoRa NSS | Output | Active low |
| P0.05 | LoRa DIO0 | Input | RX ready |
| P0.06 | LoRa DIO1 | Input | TX done |
| P0.07 | LoRa DIO2 | Input | CAD detect |
| P0.28 | SPI SCK (LoRa) | Output | 8MHz |
| P0.29 | SPI MISO | Input | — |
| P0.30 | SPI MOSI | Output | — |
| **P0.31** | **I²C SCL (SHT31)** | **Output** | **100kHz I²C clock** |
| **P1.00** | **I²C SDA (SHT31)** | **I/O** | **I²C data** |
| P1.01 | Battery ADC | Input | Voltage monitoring |
| P1.02 | Heater Control | Output | PWM capable |
| P1.03 | Dielectric Excitation | Output | 100MHz oscillator |
| **P1.04** | **Temp Alert** | **Input** | **SHT31 alert pin** |
| P1.05 | Antenna Switch | Output | TX/RX control |
| P1.06 | CryptoCell Reset | Output | CC-310 control |
| P1.07 | Factory Mode | Input | Pull-down boot |

### 2.4 Environmental Specifications

**Identical to LRZN:**

| Parameter | Specification | Notes |
|-----------|---------------|-------|
| **Operating Temperature** | -40°C to +60°C | Sensor rated -40 to +125°C |
| **Temperature Accuracy Range** | -40°C to +80°C | ±0.3°C spec range |
| **Soil pH Range** | 4.0-10.0 | No sensor degradation |
| **Salinity Tolerance** | 0-5 dS/m | Temperature compensation helps |
| **Burial Depth** | 48" (1.2m) standard | Thermal mass stabilizes readings |

**Temperature-Specific Considerations:**

- Soil temperature lags air temperature by 2-4 hours (thermal mass)
- Frost depth penetration: ~1" per day in freezing conditions
- LRZB placement at 24" depth captures active root zone thermal profile
- Temperature gradient useful for detecting water table proximity

---

## 3. Firmware Specifications

### 3.1 Temperature-Compensated VWC Measurement

**Dielectric Temperature Coefficient:**

Water's dielectric constant varies with temperature:
- ε(20°C) = 80.4 (reference)
- ε(0°C) = 88.0 (+9.5%)
- ε(40°C) = 73.3 (-8.8%)

**Compensation Algorithm:**

```c
float compensate_vwc_for_temperature(float raw_vwc, float temp_c) {
    // Reference temperature: 20°C
    const float T_ref = 20.0;
    const float dEps_dT = -0.36;  // Dielectric constant temp coefficient
    
    // Calculate dielectric constant from raw VWC (inverse Topp)
    float epsilon = inverse_topp(raw_vwc);
    
    // Adjust to reference temperature
    float epsilon_corrected = epsilon - dEps_dT * (temp_c - T_ref);
    
    // Convert back to VWC
    float vwc_corrected = topp_equation(epsilon_corrected);
    
    return clamp(vwc_corrected, 0.0, 1.0);
}
```

**Accuracy Improvement:**

| Condition | LRZN (uncompensated) | LRZB (compensated) | Improvement |
|-----------|----------------------|-------------------|-------------|
| 5°C soil (spring) | ±4.5% error | ±2.0% | 56% better |
| 20°C soil (reference) | ±3.0% error | ±2.0% | 33% better |
| 35°C soil (summer) | ±3.8% error | ±2.0% | 47% better |

### 3.2 SHT31 Temperature/Humidity Sensor

**Sensor Specifications:**

| Parameter | Value |
|-----------|-------|
| **Manufacturer** | Sensirion |
| **Model** | SHT31-DIS-F (filter membrane) |
| **Interface** | I²C (100kHz/400kHz) |
| **Address** | 0x44 (default) |
| **Temperature Range** | -40°C to +125°C |
| **Temperature Accuracy** | ±0.3°C (0-65°C) |
| **Temperature Resolution** | 0.01°C |
| **RH Range** | 0-100% |
| **RH Accuracy** | ±2% RH |
| **Power (sleep)** | 0.8µA |
| **Power (measuring)** | 2mA @ 3.3V |
| **Measurement Time** | 10ms (single shot) |

**SHT31 Operation:**

```c
void read_sht31(float *temp_c, float *rh_pct) {
    // Trigger measurement (single shot, high repeatability)
    uint8_t cmd[] = {0x2C, 0x06};
    i2c_write(SHT31_ADDR, cmd, 2);
    
    // Wait 10ms for conversion
    delay_ms(10);
    
    // Read 6 bytes (temp MSB, LSB, CRC, RH MSB, LSB, CRC)
    uint8_t data[6];
    i2c_read(SHT31_ADDR, data, 6);
    
    // Verify CRCs
    if (crc8(data[0], data[1]) != data[2]) return ERROR;
    if (crc8(data[3], data[4]) != data[5]) return ERROR;
    
    // Convert raw to engineering units
    uint16_t temp_raw = (data[0] << 8) | data[1];
    uint16_t rh_raw = (data[3] << 8) | data[4];
    
    *temp_c = -45.0 + 175.0 * (float)temp_raw / 65535.0;
    *rh_pct = 100.0 * (float)rh_raw / 65535.0;
}
```

**Note on RH Measurement:**

The SHT31 measures relative humidity inside the sealed sled, not soil RH. This reading is used for:
1. Sled seal integrity monitoring (RH should stay low)
2. Condensation detection (RH >90% indicates potential leak)
3. Factory calibration verification

### 3.3 Field Calibration Capability

**VFA Calibration Reference:**

The LRZB can be field-calibrated against VFA (Vertical Field Anchor) readings:

```c
void field_calibrate_to_vfa(float vfa_vwc, float local_raw_vwc) {
    // Store calibration point in EEPROM
    calibration_table[cal_point_count].vfa_vwc = vfa_vwc;
    calibration_table[cal_point_count].local_raw = local_raw_vwc;
    calibration_table[cal_point_count].timestamp = get_timestamp();
    calibration_point_count++;
    
    // Compute new calibration coefficients (if N≥3 points)
    if (cal_point_count >= 3) {
        compute_calibration_polynomial();
        store_to_eeprom();
        report_calibration_to_pmt();
    }
}
```

**Calibration Process:**

1. Install LRZB alongside existing VFA (within 2m)
2. Wait 7 days for soil equilibration
3. Record 50+ paired readings (LRZB raw vs VFA ground truth)
4. Compute linear regression: VWC_calibrated = a × raw + b
5. Store coefficients in LRZB EEPROM
6. Apply calibration to all future readings
7. Re-calibrate annually or if soil conditions change

### 3.4 Enhanced Telemetry Format

**LRZB-Specific TLV Payload:**

```c
struct lrzb_payload {
    uint8_t   magic[4];           // "FS01"
    uint16_t  device_id;          // 16-bit short address
    uint8_t   msg_type;           // 0x02 = VWC+Temp report
    uint32_t  timestamp;          // Unix epoch
    uint16_t  vwc_raw;            // Dielectric reading
    uint16_t  vwc_calibrated;     // 0-10000 (×10000)
    int16_t   temperature;        // Degrees C × 100 (LRZB specific!)
    uint16_t  rh_internal;        // Sled RH × 100 (diagnostic)
    uint16_t  battery_voltage;      // mV
    int16_t   rssi;               // Last RX RSSI
    uint8_t   quality_score;      // 0-100
    uint8_t   calibration_status; // 0=none, 1=factory, 2=field
    uint32_t  sequence_num;       // Anti-replay
    uint8_t   padding[142];         // Reserved
    uint8_t   auth_tag[16];         // AES-256-GCM
} __attribute__((packed));
```

**Temperature Field:**

- Signed 16-bit integer
- Scale: 0.01°C (2350 = 23.50°C)
- Range: -327.68°C to +327.67°C (way beyond sensor capability)
- Special value: 0x7FFF = sensor fault / not populated (LRZN compatibility)

---

## 4. Cross-Sensor Validation

### 4.1 LRZB as Validation Anchor

**Statistical Validation Model:**

```python
# PMT-level cross-validation
def validate_field_with_lrzb(field_id):
    lrzb_nodes = get_nodes_by_type(field_id, 'LRZB')  # 4 nodes
    lrzn_nodes = get_nodes_by_type(field_id, 'LRZN')  # 12 nodes
    
    # LRZB inter-consistency check
    lrzb_vwc = [n.vwc for n in lrzb_nodes]
    lrzb_mean = mean(lrzb_vwc)
    lrzb_std = std(lrzb_vwc)
    
    if lrzb_std > 0.03:  # >3% spread among beacons
        flag_alert("LRZB divergence", field_id)
    
    # LRZN vs LRZB validation
    for lrzn in lrzn_nodes:
        # Find nearest LRZB
        nearest_lrzb = find_nearest(lrzn, lrzb_nodes)
        expected_vwc = interpolate(lrzn.location, lrzb_nodes)
        
        deviation = abs(lrzn.vwc - expected_vwc)
        if deviation > 0.05:  # >5% from interpolated expectation
            lrzn.quality_score -= 25
            flag_for_review(lrzn.id, "VWC deviation from LRZB prediction")
        
        # Temperature correlation (seasonal)
        if abs(lrzn.location.temp - nearest_lrzb.temp) > 5.0:
            flag_alert("Thermal anomaly", lrzn.id)
```

### 4.2 Temperature-Enabled Features

**Frost Depth Detection:**

```python
def detect_frost_conditions(lrzb_readings):
    # Collect all LRZB temperature readings
    temps = [r.temperature for r in lrzb_readings]
    
    # Check for below-freezing conditions
    if any(t < 0.0 for t in temps):
        frost_nodes = [r for r in lrzb_readings if r.temperature < 0.0]
        
        # Estimate frost depth based on which nodes are frozen
        # Assuming nodes at 8", 16", 24", 36"
        max_frost_depth = max(r.depth for r in frost_nodes)
        
        return {
            'frost_detected': True,
            'max_depth_inches': max_frost_depth,
            'severity': 'moderate' if max_frost_depth > 12 else 'light',
            'recommendation': 'Delay irrigation until thaw'
        }
```

**Soil Thermal Conductivity:**

Temperature gradients between LRZB at different depths inform soil thermal properties:
- Steep gradient = low thermal conductivity (dry, sandy)
- Shallow gradient = high thermal conductivity (wet, clay)
- Useful for inferring moisture without direct VWC measurement

---

## 5. Bill of Materials

### 5.1 Complete LRZB BOM

| Component | Supplier | Part Number | Unit Cost | Qty | Extended |
|-----------|----------|-------------|-----------|-----|----------|
| **MCU** | Nordic | nRF52840-QIAA | $8.50 | 1 | $8.50 |
| **CryptoCell** | Nordic | CC-310 (integrated) | — | 1 | — |
| **LoRa Module** | HopeRF | RFM95W-915S2 | $15.00 | 1 | $15.00 |
| **Dielectric Sensor** | Custom | 100MHz oscillator PCB | $3.50 | 1 | $3.50 |
| **Temperature Sensor** | Sensirion | SHT31-DIS-F | $4.80 | 1 | $4.80 |
| **Electrodes** | Custom | 316 SS rings | $1.20 | 2 | $2.40 |
| **Battery Cells** | LG Chem | INR21700-M50T | $4.50 | 3 | $13.50 |
| **Battery Management** | TI | BQ40Z50 | $2.80 | 1 | $2.80 |
| **Heater Element** | Omega | KH-505/5-P | $8.00 | 1 | $8.00 |
| **Main PCB** | JLCPCB | 4-layer FR-4 enhanced | $4.50 | 1 | $4.50 |
| **PCB Assembly** | JLCPCB | SMT + test | $5.50 | 1 | $5.50 |
| **Alpha-Sled (CHDPE)** | Custom | Conductive HDPE | $8.00 | 1 | $8.00 |
| **Outer Shell (HDPE)** | JM Eagle | SDR9-2 pipe | $4.25 | 1 | $4.25 |
| **Seals (Viton)** | Parker | FKM-001 O-rings | $0.40 | 4 | $1.60 |
| **Nitrogen Valve** | Swagelok | SS-1RS4 | $18.00 | 1 | $18.00 |
| **Desiccant** | Dry-Packs | Silica gel 25g | $1.50 | 1 | $1.50 |
| **Antenna** | Taoglas | SS-Whip helical | $2.50 | 1 | $2.50 |
| **Cable Assembly** | Various | Internal wiring | $2.50 | 1 | $2.50 |
| **Label/QR Code** | Avery | Weatherproof label | $0.50 | 1 | $0.50 |
| **Packaging** | Uline | Cardboard tube | $2.00 | 1 | $2.00 |
| **Calibration** | In-house | Dielectric + temp standards | $8.00 | 1 | $8.00 |
| **Certification** | External | FCC Part 15 | $2.50 | 1 | $2.50 |
| **TOTAL BOM** | | | | | **$118.35** |
| **Target Retail** | | | | | **$54.30** | Volume: 10K+

### 5.2 LRZN vs LRZB BOM Comparison

| Component | LRZN | LRZB | Delta | Notes |
|-----------|------|------|-------|-------|
| **MCU** | $8.50 | $8.50 | — | Same |
| **LoRa** | $15.00 | $15.00 | — | Same |
| **Dielectric** | $3.50 | $3.50 | — | Same |
| **Temperature** | — | $4.80 | +$4.80 | SHT31 sensor |
| **Battery** | $13.50 | $13.50 | — | Same |
| **PCB** | $3.50 | $4.50 | +$1.00 | Enhanced I²C routing |
| **Assembly** | $4.50 | $5.50 | +$1.00 | Additional testing |
| **Sled/Shell** | $12.25 | $12.25 | — | Same |
| **Calibration** | $5.00 | $8.00 | +$3.00 | Temp calibration |
| **TOTAL** | $78.75 | $91.55 | +$12.80 | BOM difference |

---

## 6. Deployment Patterns

### 6.1 16-Node Standard Configuration

| Ring | Radius | Count | Type | Purpose | Temp Value |
|------|--------|-------|------|---------|------------|
| Center | 0% | 1 | **LRZB** | Pivot reference + thermal center | Core temp |
| Inner | 25% | 3 | LRZN | Near-pivot zone | — |
| Middle | 50% | 4 | **LRZB** | Cardinal validation points | N/E/S/W temps |
| Outer | 75% | 8 | LRZN | Edge interpolation | — |

**LRZB Strategic Value:**

- **Center node**: Captures thermal signature of pivot wetting pattern
- **Middle ring**: N/E/S/W placement captures directional temperature gradients (sun exposure, wind)
- Enables thermal mapping: soil warms faster on south side, stays cooler north side

### 6.2 Temperature Gradient Analysis

**Solar Heating Pattern:**

```
        N (cooler)
        ↑
   W ←  PIVOT  → E (warmer afternoon)
        ↓
        S (warmest)
        
LRZB placement captures this gradient:
- North LRZB: Reference for shaded conditions
- South LRZB: Reference for direct sun exposure
- Temp differential informs evaporation models
```

---

## 7. Revision History

| Version | Date | Author | Changes | Approval |
|---------|------|--------|---------|----------|
| 1.0 | 2026-01-15 | J. Beebe | Initial LRZ2 specification | Approved |
| 1.1 | 2026-02-20 | Engineering | Added SHT31 specs | Approved |
| 1.2 | 2026-03-19 | J. Beebe | **MAJOR**: Renamed LRZ2→LRZB, temp compensation algorithms, field calibration | **PENDING** |

---

## 8. References

| Document | Relationship | Location |
|----------|--------------|----------|
| **LRZN-SPEC.md** | Companion spec (Node variant) | `docs/specs/LRZN-SPEC.md` |
| **VFA-SPEC.md** | Calibration reference standard | `docs/specs/VFA-SPEC.md` |
| **SHT31 Datasheet** | Temperature sensor reference | Sensirion (external) |

---

*Proprietary IP of bxthre3 inc. — Confidential*

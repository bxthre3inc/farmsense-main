---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Device Code: LRZN
Full Name: Lateral Root Zone Node
Version: 1.2
Category: Level 0 Field Sensor
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

# LRZN V1.2: Lateral Root Zone Node

## 1. Executive Summary

### 1.1 Role and Function

The LRZN (Lateral Root Zone Node) is a Level 0 field sensor providing high-density spatial coverage for soil volumetric water content (VWC) measurement across the lateral extent of center-pivot irrigated fields. As the "Basic" tier of the Lateral Root Zone Surveyor family, the LRZN prioritizes cost-effective density deployment over sensor sophistication, enabling comprehensive Kriging interpolation coverage at 12 units per standard 130-acre field.

**Primary Functions:**

1. Measure soil VWC at a single configurable depth (8", 16", 24", 36" configurable)
2. Report to PMT (Pivot Motion Tracker) via 900MHz CSS LoRa
3. Enable spatial interpolation for 50m, 20m, 10m, and 1m Kriging grids
4. Provide 4+ year battery life at 4-hour baseline chirp intervals
5. Maintain AES-256 encrypted telemetry with CryptoCell-310

**Deployment Context:**

- Standard density: 12 LRZN per field + 4 LRZB (16 total nodes)
- Placement: Concentric ring pattern avoiding wheel tracks
- Target MTBF: 50,000 hours (5.7 years)
- Unit economics: $29.00 BOM cost enables sub-$500 total field sensor investment

### 1.2 LRZN vs LRZB Distinction

| Attribute | LRZN (Basic/Node) | LRZB (Reference/Beacon) |
|-----------|-------------------|-------------------------|
| **Role** | Spatial density | Calibration anchor |
| **Sensors** | VWC only | VWC + Temperature |
| **Depth** | Single (variable) | Single (variable) |
| **Accuracy** | ±3% VWC | ±2% VWC, ±0.5°C |
| **Calibration** | Factory calibrated | Field-calibrated to VFA |
| **BOM Cost** | $29.00 | $54.30 |
| **Density** | 12 per field | 4 per field |
| **Purpose** | Kriging interpolation | Ground-truth validation |
| **MCU** | nRF52840 | nRF52840 + temp sensor |

### 1.3 Critical Success Factors

- **Coverage**: 12 nodes provide 130-acre field with <75m spacing for 50m Kriging
- **Battery Life**: 4+ years eliminates mid-season replacement risk
- **Canopy Penetration**: 900MHz CSS LoRa achieves 100% coverage vs 60% loss at 2.4GHz
- **Cost**: $29 BOM enables $348 field-level investment (12× LRZN) vs $2,000+ competitor nodes

---

## 2. Hardware Specifications

### 2.1 Mechanical Design

**Alpha-Sled Form Factor:**

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
| **Nitrogen Purge** | +5 PSI dry N₂ pressurization (via Swagelok SS-1RS4 valve) |
| **Seal Rating** | IP68 (submersible to 2m indefinitely) |

**Electrode Configuration:**

| Parameter | Value |
|-----------|-------|
| **Sensing Electrodes** | 2× stainless steel rings embedded in sled wall |
| **Electrode Spacing** | 40mm (defines sensing volume) |
| **Sensing Method** | Non-contact capacitive through CHDPE wall |
| **Field Penetration** | ~100mm radius from sled surface |
| **Soil Contact** | None required (dielectric measurement through wall) |

### 2.2 Electrical Architecture

**Power System:**

| Component | Specification |
|-----------|---------------|
| **Primary Battery** | 3× 21700 Li-ion cells (18.5Wh total) |
| **Nominal Voltage** | 3.7V (3.0V-4.2V operating range) |
| **Battery Chemistry** | LiFePO₄ or Li-Ion (operator preference) |
| **Battery Configuration** | Series-parallel for 11.1V system voltage |
| **Capacity** | 5000mAh @ 3.7V |
| **Heater System** | 5W resistive cartridge (Omega KH-505/5-P) |
| **Heater Activation** | < -10°C ambient, < 0°C soil temp |
| **Solar Option** | Not applicable (buried, zero light) |

**Power Budget Analysis:**

| Mode | Current | Duration | Daily Energy |
|------|---------|----------|--------------|
| Deep Sleep | 8µA | 3h 45m | 0.03mWh |
| Sensor Warmup | 15mA | 2 sec | 0.31mWh |
| VWC Measurement | 25mA | 500ms | 0.13mWh |
| LoRa TX | 120mA | 150ms | 6.25mWh |
| MCU Active | 12mA | 50ms | 0.52mWh |
| **Daily Total** | — | — | **7.24mWh** |
| **4-Year Capacity** | — | — | **18.5Wh** |
| **Margin** | — | — | **29% reserve** |

### 2.3 PCB Design

**Mainboard Specifications:**

| Attribute | Value |
|-----------|-------|
| **PCB Material** | FR-4, 4-layer, 1.6mm thickness |
| **PCB Dimensions** | 35mm × 80mm (fits within sled core) |
| **Surface Finish** | ENIG (Electroless Nickel Immersion Gold) |
| **Assembly** | JLCPCB PCBA service |
| **Conformal Coat** | Acrylic (humidity protection) |
| **Operating Temp** | -40°C to +85°C |
| **Storage Temp** | -40°C to +125°C |

**PCBA GPIO Pinout (nRF52840-QIAA):**

| Pin | Function | Direction | Notes |
|-----|----------|-----------|-------|
| P0.02 | ADC0 (dielectric measurement) | Input | 12-bit SAR ADC |
| P0.03 | Reserved (temperature) | Input | Not populated on LRZN |
| P0.04 | LoRa NSS (chip select) | Output | Active low |
| P0.05 | LoRa DIO0 (RX ready) | Input | Interrupt-triggered |
| P0.06 | LoRa DIO1 (TX done) | Input | Interrupt-triggered |
| P0.07 | LoRa DIO2 (CAD detect) | Input | Channel activity |
| P0.28 | SPI SCK (clock) | Output | 8MHz max |
| P0.29 | SPI MISO (data in) | Input | — |
| P0.30 | SPI MOSI (data out) | Output | — |
| P0.31 | Status LED | Output | Diagnostic only |
| P1.00 | Wake Button | Input | Factory test/maint |
| P1.01 | Battery ADC | Input | Voltage monitoring |
| P1.02 | Heater Control | Output | PWM capable |
| P1.03 | Dielectric Excitation | Output | 100MHz oscillator |
| P1.04 | Temperature (reserved) | Input | Not connected LRZN |
| P1.05 | Antenna Switch | Output | TX/RX control |
| P1.06 | CryptoCell Reset | Output | CC-310 control |
| P1.07 | Factory Mode | Input | Pull-down boot mode |

### 2.4 Environmental Specifications

| Parameter | Specification | Test Standard |
|-----------|---------------|---------------|
| **Operating Temperature** | -40°C to +60°C | IEC 60068-2-1/2 |
| **Storage Temperature** | -40°C to +85°C | IEC 60068-2-1/2 |
| **Humidity** | 0-100% RH (condensing) | IEC 60068-2-78 |
| **Soil pH Range** | 4.0-10.0 | Continuous exposure |
| **Salinity Tolerance** | 0-5 dS/m | EC compensation |
| **Burial Depth** | 48" (1.2m) standard | Installation spec |
| **Pressure Rating** | 2 ATM (20m water depth equivalent) | IP68 |
| **Vibration** | 5-2000Hz, 20g RMS | IEC 60068-2-6 |
| **Shock** | 50g half-sine, 11ms | IEC 60068-2-27 |
| **ESD Protection** | ±8kV contact, ±15kV air | IEC 61000-4-2 |
| **EMC Immunity** | EN 55032 Class B | Emissions |
| **Corrosion Resistance** | 40+ year soil exposure | HDPE material |

---

## 3. Firmware Specifications

### 3.1 Microcontroller Platform

**nRF52840-QIAA (Nordic Semiconductor):**

| Attribute | Specification |
|-----------|---------------|
| **Core** | ARM Cortex-M4F with FPU |
| **Clock Speed** | 64MHz |
| **Flash Memory** | 1MB |
| **RAM** | 256KB |
| **Bluetooth** | BLE 5.0, 2Mbps, Long Range |
| **802.15.4** | Thread/Zigbee capable (unused) |
| **NFC** | Integrated (unused) |
| **USB** | Full-speed device |
| **CryptoCell** | CC-310 (AES-256, ECC) |
| **Package** | QIAA (7×7mm QFN) |
| **Operating Voltage** | 1.7V-3.6V |
| **Current (Active)** | 7.5mA @ 3V (64MHz) |
| **Current (Sleep)** | 1.9µA (RAM retention) |

### 3.2 Dielectric Sensing Method

**Principle:** High-frequency capacitive measurement (~100MHz)

**Implementation Details:**

| Parameter | Value |
|-----------|-------|
| **Excitation Frequency** | 100MHz ±5% |
| **Oscillator Type** | Colpitts LC with soil as dielectric |
| **Measurement Method** | Frequency counting (timer capture) |
| **Resolution** | 0.1% VWC |
| **Accuracy** | ±3% VWC (factory calibrated) |
| **Repeatability** | ±1% VWC |
| **Response Time** | <500ms (settling) |
| **Temperature Effect** | <0.5% VWC/°C (compensated) |
| **Salinity Effect** | <2% VWC per dS/m (limited range) |

**Topp Equation Calibration:**

```c
// Dielectric constant to VWC conversion
float dielectric_to_vwc(float epsilon) {
    // Topp et al. (1980) empirical relationship
    // Valid for 1 < epsilon < 80 (air to water)
    float vwc = -0.053 + 0.0292 * epsilon 
                - 0.00055 * pow(epsilon, 2) 
                + 0.0000043 * pow(epsilon, 3);
    return clamp(vwc, 0.0, 1.0);  // 0-100%
}
```

**Factory Calibration Process:**

1. Measure dielectric constant in air (ε ≈ 1.0)
2. Measure dielectric constant in deionized water (ε ≈ 80)
3. Measure at 3 intermediate points (known VWC standards)
4. Compute 3rd-order polynomial coefficients
5. Store in device EEPROM with CRC32 checksum
6. Laser-etched QR code links to calibration certificate

### 3.3 Communication Protocol Stack

**LoRa Physical Layer:**

| Parameter | Specification |
|-----------|---------------|
| **Modulation** | Chirp Spread Spectrum (CSS) |
| **Frequency Band** | 902-928MHz (US ISM, configurable) |
| **Bandwidth** | 125kHz (standard) / 250kHz (fast) |
| **Spreading Factor** | SF7 (fast) to SF12 (long range) |
| **Coding Rate** | 4/5 (standard) |
| **TX Power** | +20dBm (100mW, FCC limit) |
| **RX Sensitivity** | -148dBm @ SF12, 125kHz |
| **Range (LoS)** | 15km @ SF12 |
| **Range (Canopy)** | 500m-2km @ SF9 (agricultural) |
| **Data Rate** | 0.3-37.5 kbps |
| **Module** | HopeRF RFM95W-915S2 |
| **Antenna** | Helical wire (integrated in sled) |

**Network Protocol (FarmSense Field Mesh):**

| Layer | Protocol | Purpose |
|-------|----------|---------|
| **Application** | FarmSense TLV | Sensor data encoding |
| **Transport** | LoRaWAN-compatible (private) | Unconfirmed Data Up |
| **Network** | Field Mesh (star topology) | PMT as hub |
| **MAC** | CSS LoRa | Channel access |
| **Physical** | 900MHz RF | Air interface |

**Message Format (187-byte TLV Payload):**

```c
struct lrzn_payload {
    uint8_t   magic[4];           // "FS01"
    uint16_t  device_id;          // 16-bit short address
    uint8_t   msg_type;           // 0x01 = VWC report
    uint32_t  timestamp;          // Unix epoch (seconds)
    uint16_t  vwc_raw;            // Dielectric reading (×100)
    uint16_t  vwc_calibrated;     // 0-10000 (×10000 = 100%)
    int16_t   temperature;      // Reserved (0x7FFF on LRZN)
    uint16_t  battery_voltage;    // mV
    int16_t   rssi;               // Last RX RSSI
    uint8_t   quality_score;      // 0-100 (measurement confidence)
    uint32_t  sequence_num;       // Anti-replay counter
    uint8_t   padding[147];       // Reserved / encrypted ext
    uint8_t   auth_tag[16];       // AES-256-GCM tag
} __attribute__((packed));
```

### 3.4 Encryption & Security

**CryptoCell-310 Implementation:**

| Feature | Implementation |
|---------|----------------|
| **Algorithm** | AES-256-GCM |
| **Key Storage** | Hardware-backed (ARM TrustZone) |
| **Key Lifecycle** | Factory-injected, never extractable |
| **Nonce** | 96-bit (sequence number + timestamp) |
| **Tag Length** | 128-bit (16 bytes) |
| **Key Rotation** | Remote OTA (quarterly) |
| **Side-Channel Resistance** | Hardware masking enabled |
| **Physical Tamper** | Die-level intrusion detection |

**Security Architecture:**

1. **Device Provisioning**:
   - Unique 256-bit device key injected at JLCPCB assembly
   - Public key certificate signed by FarmSense CA
   - QR code links to device registry entry

2. **Field Pairing**:
   - PMT broadcasts pairing beacon (unencrypted)
   - LRZN responds with signed challenge
   - ECDH key exchange establishes session keys
   - Session keys rotated every 24 hours

3. **Data Integrity**:
   - All telemetry includes AES-256-GCM auth tag
   - Sequence numbers prevent replay attacks
   - Timestamp validation (±5 minute drift tolerance)

4. **Physical Security**:
   - Tamper-evident nitrogen pressure seal
   - Intrusion detection (pressure drop = alert)
   - No debug interfaces exposed
   - Firmware readback disabled (RDP Level 2)

### 3.5 Power Management & Adaptive States

**Adaptive Recalculation Engine: "Fisherman's Attention"**

| Mode | Trigger | Chirp Interval | Power Draw | Battery Life |
|------|---------|----------------|------------|--------------|
| **DORMANT** | Stable moisture, pivot parked | 4 hours | 8µA | 6+ years |
| **ANTICIPATORY** | Sunrise, T > 5°C rise/hr | 60 minutes | 15mA avg | 3 years |
| **FOCUS RIPPLE** | Anomaly >5% VWC deviation | 15 minutes | 45mA avg | 18 months |
| **COLLAPSE** | Pivot active / critical fault | 5 seconds | 120mA avg | 2 months |

**Mode Transitions:**

```c
// Volatility Score calculation
float calculate_volatility(void) {
    float vwc_delta = fabs(vwc_history[0] - vwc_history[1]);  // 1-hour change
    float pivot_factor = pmt_status.irrigation_active ? 0.3 : 0.0;
    float vpd_factor = (meteo.vpd > 2.0) ? 0.2 : 0.0;  // kPa
    float wind_factor = (meteo.wind > 5.0) ? 0.1 : 0.0;  // m/s
    
    float V = (vwc_delta * 0.4) + pivot_factor + vpd_factor + wind_factor;
    return clamp(V, 0.0, 1.0);
}

// Mode decision
if (V > 0.7) {
    enter_mode(COLLAPSE);
} else if (V > 0.3) {
    enter_mode(FOCUS_RIPPLE);
} else if (sunrise_detected || temp_rising_fast) {
    enter_mode(ANTICIPATORY);
} else {
    enter_mode(DORMANT);
}
```

**Deep Sleep Implementation:**

- nRF52840 System OFF mode (1.9µA)
- RTC2 wakeup timer (configurable interval)
- GPIO event detection (emergency override)
- RAM retention for state persistence
- Fast wake (<5ms to active)

---

## 4. Communication & Network

### 4.1 Topology Position

**Network Hierarchy:**

```
Level 3: RSS (Regional Superstation)
    ↑ 5GHz microwave / fiber
Level 2: DHU (District Hub Unit) — 100-pivot radius
    ↑ 2.4GHz LTU / LTE-M
Level 1.5: PMT (Pivot Motion Tracker) — Per-field hub
    ↓ 900MHz CSS LoRa — STAR TOPOLOGY
Level 0: LRZN (Lateral Root Zone Node) — 12 per field
Level 0: LRZB (Lateral Root Zone Beacon) — 4 per field
Level 0: VFA (Vertical Field Anchor) — 2-4 per field
Level 0: PFA (Pressure & Flow Anchor) — 1 per field (wellhead)
```

**LRZN Network Role:**

- **Node Type**: End device (star leaf)
- **Parent**: PMT (always, never direct to DHU)
- **Addressing**: 16-bit short address (allocated by PMT)
- **Uplink**: Unconfirmed Data Up (reliability via redundancy)
- **Downlink**: Confirmed Data Down (config updates, rare)

### 4.2 Radio Specifications

**RF Performance:**

| Parameter | Specification |
|-----------|---------------|
| **Frequency Range** | 902-928MHz (configurable by region) |
| **Channel Spacing** | 200kHz (8 channels typical) |
| **Modulation** | LoRa CSS (Chirp Spread Spectrum) |
| **Bandwidth Options** | 125kHz, 250kHz |
| **Spreading Factors** | SF7-SF12 (ADR adaptive) |
| **TX Power** | +2 to +20dBm (configurable) |
| **RX Sensitivity** | -148dBm @ SF12, 125kHz |
| **Link Budget** | 168dB max |
| **Antenna Gain** | +2.15dBi (helical wire) |
| **VSWR** | <2.0:1 |
| **Impedance** | 50Ω |

**Link Budget Analysis:**

| Scenario | TX Power | Antenna | Path Loss | Margin | Result |
|----------|----------|---------|-----------|--------|--------|
| LoS 1km | +20dBm | +2dBi | -108dB | 62dB | ✓ Excellent |
| Corn 500m | +20dBm | +2dBi | -125dB | 45dB | ✓ Good |
| Corn 1km, rain | +20dBm | +2dBi | -135dB | 35dB | ✓ Adequate |
| Dense canopy 2km | +20dBm | +2dBi | -148dB | 22dB | ✓ Marginal |

**Adaptive Data Rate (ADR):**

| RSSI | SF | BW | DR | Range | Use Case |
|------|-----|-----|-----|-------|----------|
| > -80dBm | SF7 | 250kHz | 5.5kbps | 500m | Clear field |
| -80 to -100dBm | SF9 | 125kHz | 1.8kbps | 1km | Standard |
| -100 to -120dBm | SF11 | 125kHz | 0.5kbps | 2km | Dense crop |
| < -120dBm | SF12 | 125kHz | 0.3kbps | 3km | Emergency |

### 4.3 Field Deployment Pattern

**16-Node Standard Configuration (130-acre center pivot):**

| Ring | Radius % | Nodes | Type | Purpose | LoRa SF |
|------|----------|-------|------|---------|---------|
| Center | 0% | 1 | LRZB | Pivot point reference | SF7 |
| Inner | 25% | 3 | LRZN | Near-pivot zone | SF9 |
| Middle | 50% | 4 | LRZB | Mid-field validation | SF7 |
| Outer | 75% | 8 | LRZN | Edge interpolation | SF9-SF11 |

**Placement Strategy:**

1. **Avoid Wheel Tracks**: Stay 10' from tire paths (compaction zones)
2. **Avoid Crop Rows**: Offset 5' from previous year rows (residue effects)
3. **Maximize Spatial Coverage**: Equal-area distribution algorithm
4. **Ensure LoRa Visibility**: Minimize terrain/crop obstructions to PMT
5. **Depth Consistency**: All nodes at same depth per field (typically 24")

**Coordinate System:**

- Field-relative polar coordinates (r, θ) from pivot center
- r = % of pivot radius (0.25, 0.5, 0.75 typical)
- θ = 45° increments for outer ring, 120° for inner
- GPS coordinates for absolute reference (stored in registry)

---

## 5. Compute & Processing

### 5.1 Edge Compute Role

The LRZN performs **minimal edge compute** by design. Processing responsibilities:

| Function | Implementation | Location |
|----------|----------------|----------|
| VWC measurement | Dielectric → Topp equation | LRZN firmware |
| Quality scoring | SNR, variance check | LRZN firmware |
| Encryption | AES-256-GCM | CryptoCell-310 |
| Kriging interpolation | IDW/OK algorithms | PMT (Level 1.5) |
| Spatial prediction | 20m/10m grids | DHU (Level 2) |
| Master gridding | 1m regression | RSS (Level 3) |

### 5.2 Data Quality Pipeline

**On-Device Quality Scoring:**

```c
uint8_t calculate_quality_score(void) {
    uint8_t score = 100;
    
    // Dielectric range check
    if (dielectric < 1.0 || dielectric > 80.0) {
        score -= 30;  // Invalid reading
    }
    
    // Variance from recent history
    float variance = calculate_variance(vwc_history, 6);
    if (variance > 0.05) {  // >5% swing
        score -= 20;  // Unstable reading
    }
    
    // Battery voltage impact
    if (battery_voltage < 3300) {  // <3.3V
        score -= 15;  // Low power = less accurate
    }
    
    // Temperature compensation check
    if (abs(soil_temp - last_temp) > 10.0) {
        score -= 10;  // Rapid thermal change
    }
    
    return max(score, 0);
}
```

**Quality Score Interpretation:**

| Score | Meaning | Action |
|-------|---------|--------|
| 90-100 | Excellent | Use for Kriging anchor |
| 70-89 | Good | Use for interpolation |
| 50-69 | Fair | Weight reduced 50% |
| 30-49 | Poor | Flag for review, exclude from critical |
| 0-29 | Invalid | Reject, alert maintenance |

### 5.3 Cross-Sensor Validation

**PMT-Level Validation (Upstream):**

The PMT performs correlation checks between LRZN and other sensors:

- LRZN vs LRZB: Expect <3% VWC difference at same radius
- LRZN vs VFA: Expect depth-proportional relationship
- LRZN vs Satellite: NDVI correlation check (weekly)

**Anomaly Detection:**

```python
# PMT-side validation pseudocode
def validate_lrzn_reading(lrzn_id, vwc):
    neighbors = get_spatial_neighbors(lrzn_id, radius=50m)
    neighbor_vwc = [n.vwc for n in neighbors]
    
    # Z-score check
    mean_vwc = mean(neighbor_vwc)
    std_vwc = std(neighbor_vwc)
    z_score = abs(vwc - mean_vwc) / std_vwc
    
    if z_score > 3.0:
        flag_anomaly(lrzn_id, vwc, "outlier_zscore")
        return False
    
    # Temporal consistency
    if abs(vwc - lrzn_history[lrzn_id][-1]) > 0.15:  # 15% jump
        flag_anomaly(lrzn_id, vwc, "temporal_jump")
        return False
    
    return True
```

---

## 6. Interface Specifications

### 6.1 Physical Interface

**No External Interfaces** (Buried, Sealed Design)

The LRZN has zero external connectors by design:

| Interface | Status | Notes |
|-----------|--------|-------|
| **USB** | Not present | No debug port exposed |
| **Serial** | Not present | No UART exposed |
| **JTAG/SWD** | Disabled | RDP Level 2, no debug |
| **Test Points** | Internal only | Factory access only |
| **Antenna** | Integrated | Helical wire inside sled |
| **Battery** | Internal | Non-serviceable 4-year life |

**Factory Programming:**

- Pogo-pin contact pads on PCB (under sled cap)
- Programming jig mates with Alpha-Sled during assembly
- All provisioning done before nitrogen seal
- No field-serviceable components

### 6.2 Data Interface (LoRa Application Layer)

**Uplink Telemetry (LRZN → PMT):**

| Field | Type | Description |
|-------|------|-------------|
| `device_id` | uint16 | Short address (PMT-assigned) |
| `timestamp` | uint32 | Unix epoch seconds |
| `vwc` | uint16 | Calibrated VWC × 10000 (0-10000 = 0-100%) |
| `dielectric_raw` | uint16 | Raw dielectric constant × 100 |
| `battery_v` | uint16 | Millivolts |
| `quality_score` | uint8 | 0-100 measurement confidence |
| `sequence` | uint32 | Anti-replay counter |
| `mode` | uint8 | Current power mode (DORMANT/ANTICIPATORY/FOCUS/COLLAPSE) |

**Downlink Commands (PMT → LRZN):**

| Command | Opcode | Payload | Response |
|---------|--------|---------|----------|
| GET_STATUS | 0x01 | None | Full status TLV |
| SET_INTERVAL | 0x02 | uint32 seconds | ACK |
| SET_MODE | 0x03 | uint8 mode | ACK |
| FORCE_MEASURE | 0x04 | None | Immediate TLV |
| CALIBRATE | 0x05 | None | ACK + status |
| FACTORY_RESET | 0xFF | Auth token | ACK (dangerous) |

### 6.3 API Specifications (Cloud-Exposed)

**LRZN data is accessed through field-level APIs, not direct device APIs.**

```http
GET /v1/devices/{lrzn_id}/telemetry?start=2026-03-01&end=2026-03-19

{
  "device_id": "lrzn-sd1-f042-018",
  "field_id": "sd1-f042",
  "pivot_id": "pmt-sd1-f042",
  "location": {
    "lat": 37.5842,
    "lon": -105.8431,
    "elevation_m": 2345,
    "field_relative": {"r": 0.75, "theta": 135}
  },
  "telemetry": [
    {
      "timestamp": "2026-03-19T14:30:00Z",
      "vwc": 0.247,
      "quality_score": 94,
      "battery_v": 3.72,
      "mode": "DORMANT",
      "rssi_to_pmt": -87
    }
  ],
  "calibration": {
    "factory_date": "2026-01-15",
    "topp_coefficients": [ -0.053, 0.0292, -0.00055, 0.0000043 ],
    "last_field_cal": null
  },
  "metadata": {
    "firmware_version": "1.2.3",
    "hardware_revision": "B",
    "deployment_date": "2026-03-01",
    "expected_eol": "2030-03-01"
  }
}
```

---

## 7. Bill of Materials

### 7.1 Complete BOM

| Component | Supplier | Part Number | Unit Cost | Qty | Extended | Lead Time |
|-----------|----------|-------------|-----------|-----|----------|-----------|
| **MCU** | Nordic Semiconductor | nRF52840-QIAA | $8.50 | 1 | $8.50 | 8 weeks |
| **CryptoCell** | Nordic Semiconductor | CC-310 (integrated) | — | 1 | — | — |
| **LoRa Module** | HopeRF | RFM95W-915S2 | $15.00 | 1 | $15.00 | 4 weeks |
| **Dielectric Sensor** | Custom | 100MHz oscillator PCB | $3.50 | 1 | $3.50 | In-house |
| **Electrodes** | Custom | 316 SS rings | $1.20 | 2 | $2.40 | In-house |
| **Battery Cells** | LG Chem | INR21700-M50T | $4.50 | 3 | $13.50 | 6 weeks |
| **Battery Management** | Texas Instruments | BQ40Z50 | $2.80 | 1 | $2.80 | 4 weeks |
| **Heater Element** | Omega | KH-505/5-P | $8.00 | 1 | $8.00 | 2 weeks |
| **Temperature Sensor** | — | Not populated | — | — | — | — |
| **Main PCB** | JLCPCB | 4-layer FR-4 | $3.50 | 1 | $3.50 | 2 weeks |
| **PCB Assembly** | JLCPCB | SMT service | $4.50 | 1 | $4.50 | 1 week |
| **Alpha-Sled (CHDPE)** | Custom extrusion | Conductive HDPE | $8.00 | 1 | $8.00 | 4 weeks |
| **Outer Shell (HDPE)** | JM Eagle | SDR9-2 pipe | $4.25 | 1 | $4.25 | Stock |
| **Seals (Viton)** | Parker | FKM-001 O-rings | $0.40 | 4 | $1.60 | Stock |
| **Nitrogen Valve** | Swagelok | SS-1RS4 | $18.00 | 1 | $18.00 | 1 week |
| **Desiccant** | Dry-Packs | Silica gel 25g | $1.50 | 1 | $1.50 | Stock |
| **Antenna** | Taoglas | SS-Whip helical | $2.50 | 1 | $2.50 | 4 weeks |
| **Cable Assembly** | Various | Internal wiring | $2.00 | 1 | $2.00 | Stock |
| **Label/QR Code** | Avery | Weatherproof label | $0.50 | 1 | $0.50 | Stock |
| **Packaging** | Uline | Cardboard tube | $2.00 | 1 | $2.00 | Stock |
| **Calibration** | In-house | Dielectric standards | $5.00 | 1 | $5.00 | 1 day |
| **Certification** | External | FCC Part 15 | $2.50 | 1 | $2.50 | (amortized) |
| **TOTAL BOM** | | | | | **$104.05** | |
| **Target Retail** | | | | | **$29.00** | Volume: 10K+ |

### 7.2 Cost Analysis

**Volume Pricing Tiers:**

| Volume | BOM Cost | Retail Price | Margin | Notes |
|--------|----------|--------------|--------|-------|
| Prototype (1-10) | $104 | $199 | 48% | Hand assembly |
| Pilot (100) | $45 | $79 | 43% | Semi-automated |
| Subdistrict (1,000) | $32 | $39 | 18% | Full automation |
| Scale (10,000+) | $22 | $29 | 24% | Injection molding |

**Cost Reduction Path:**

1. **Custom LoRa Module**: Replace RFM95W with discrete SX1262 ($15→$8)
2. **Injection Molded Sled**: Replace extrusion with mold ($8→$3)
3. **Integrated BMS**: Replace BQ40Z50 with nRF52840 native ($2.80→$0.50)
4. **Volume Battery**: 21700 cells at 50K+ units ($4.50→$2.80)

---

## 8. Installation & Deployment

### 8.1 Pre-Installation Checklist

**Site Survey:**

- [ ] Pivot coverage map generated (PMT location confirmed)
- [ ] Soil type documented (sandy/clay/loam)
- [ ] Crop rotation plan obtained
- [ ] Wheel track paths identified on satellite imagery
- [ ] Previous crop row orientations noted
- [ ] Buried obstacles located (utility locates)
- [ ] Depth to water table confirmed

**Equipment Required:**

| Item | Quantity | Purpose |
|------|----------|---------|
| Soil auger (2" diameter) | 1 | Pilot holes |
| Post-hole driver | 1 | Sled insertion |
| Winch (portable) | 1 | Extraction (if needed) |
| Nitrogen tank (N₂) | 1 | +5 PSI pressurization |
| Pressure gauge | 1 | Seal verification |
| RTK GPS unit | 1 | Precise positioning |
| Tablet (FieldTools app) | 1 | Registry update |

### 8.2 Installation Procedure

**Step 1: Positioning (15 minutes per node)**

```
1. Navigate to GPS coordinates from deployment plan
2. Verify visual clearance to PMT (line of sight preferred)
3. Mark location with stake
4. Confirm 10' offset from wheel tracks
5. Confirm 5' offset from crop rows
6. Record actual GPS (RTK accuracy <10cm)
```

**Step 2: Excavation (10 minutes)**

```
1. Use soil auger to create 2" diameter pilot hole
2. Depth: 48" (or as specified in deployment plan)
3. Remove loose soil from hole
4. Check for rocks/impediments (relocate if >6" obstruction)
5. Document soil conditions at depth (photo)
```

**Step 3: Sled Insertion (5 minutes)**

```
1. Remove protective end caps from LRZN
2. Verify nitrogen valve is closed (factory sealed)
3. Lower sled into hole using extraction cable as guide
4. Align so antenna end faces pivot center
5. Insert until flush with ground surface
6. Ensure 1" minimum soil coverage over top cap
```

**Step 4: Pressurization (5 minutes)**

```
1. Connect nitrogen tank to Swagelok valve
2. Pressurize to +5 PSI (verify on gauge)
3. Close valve, disconnect tank
4. Wait 60 seconds, verify pressure holds
5. If pressure drops >0.5 PSI in 60s, abort and replace unit
6. Record pressure reading in FieldTools app
```

**Step 5: Registry Activation (5 minutes)**

```
1. Scan QR code on sled with FieldTools app
2. Confirm device ID matches shipping label
3. Enter field ID, pivot ID, relative coordinates (r, θ)
4. Record GPS coordinates (auto-captured)
5. Enter installation depth
6. Enter soil type, crop type
7. Submit to DHU for network registration
8. Verify PMT acknowledges node (green status in app)
```

### 8.3 Deployment Patterns

**Standard Pivot (130 acres, 1/4 mile radius):**

| Ring | Radius | Count | Type | Angle Spacing | Depth |
|------|--------|-------|------|---------------|-------|
| Center | 0% | 1 | LRZB | — | 24" |
| Inner | 25% | 3 | LRZN | 120° | 24" |
| Middle | 50% | 4 | LRZB | 90° | 24" |
| Outer | 75% | 8 | LRZN | 45° | 24" |
| **Total** | — | **16** | **12× LRZN, 4× LRZB** | — | — |

**Half-Section Pivot (65 acres, 1/8 mile radius):**

| Ring | Radius | Count | Type | Notes |
|------|--------|-------|------|-------|
| Center | 0% | 1 | LRZB | — |
| Inner | 25% | 2 | LRZN | 180° |
| Middle | 50% | 2 | LRZB | 180° |
| Outer | 75% | 4 | LRZN | 90° |
| **Total** | — | **9** | **6× LRZN, 3× LRZB** | — |

**Corner-Swing Configuration:**

- Standard 16-node layout for circular portion
- Additional 4× LRZN at 100% radius for swing arm
- 1× CSA (Corner Swing Arm) on end tower
- Total: 20× LRZN, 4× LRZB for 180-acre effective

---

## 9. Operational Modes

### 9.1 Power State Machine

**State Diagram:**

```
[BOOT] → [INIT] → [DORMANT] ←→ [ANTICIPATORY] ←→ [FOCUS_RIPPLE] ←→ [COLLAPSE]
                              ↓                      ↓                  ↓
                           [MEASURE]              [MEASURE]          [MEASURE]
                              ↓                      ↓                  ↓
                           [TX]                   [TX]               [TX]
                              ↓                      ↓                  ↓
                           [SLEEP]                [SLEEP]            [SLEEP]
```

**Mode Descriptions:**

**DORMANT (Default):**

- Trigger: Stable conditions, no irrigation
- Chirp Interval: 4 hours
- Actions: VWC measurement, LoRa TX, deep sleep
- Entry Condition: Volatility Score < 0.3, no PMT activity flags
- Power Draw: 8µA average (6+ year battery life)

**ANTICIPATORY:**

- Trigger: Sunrise, rapid temperature rise, scheduled irrigation window
- Chirp Interval: 60 minutes
- Actions: Enhanced measurement, weather correlation
- Entry Condition: Sunrise ±30min OR temp rise >5°C/hour
- Power Draw: 15mA average (3 year battery life)

**FOCUS_RIPPLE:**

- Trigger: Moisture anomaly >5% deviation, neighbor flags
- Chirp Interval: 15 minutes
- Actions: Frequent sampling, anomaly documentation
- Entry Condition: |VWC - expected| > 0.05 OR neighbor anomaly flagged
- Power Draw: 45mA average (18 month battery life)

**COLLAPSE:**

- Trigger: Active irrigation, critical fault, manual override
- Chirp Interval: 5 seconds
- Actions: Real-time streaming, stall detection correlation
- Entry Condition: PMT reports irrigation_active OR fault detected
- Power Draw: 120mA average (2 month battery life, for <8hr events)

### 9.2 Fault Detection & Recovery

**Self-Test Routine (weekly):**

```c
void weekly_self_test(void) {
    // Battery voltage
    if (battery_voltage < 3300) {
        report_fault(FAULT_LOW_BATTERY);
    }
    
    // Dielectric sanity check
    float epsilon = measure_dielectric();
    if (epsilon < 0.5 || epsilon > 85.0) {
        report_fault(FAULT_SENSOR_DRIFT);
    }
    
    // LoRa loopback test
    if (!lora_ping_pmt()) {
        report_fault(FAULT_NO_CONNECTIVITY);
    }
    
    // Memory integrity
    if (!verify_firmware_crc()) {
        report_fault(FAULT_CORRUPTION);
    }
}
```

**Auto-Recovery Actions:**

| Fault | Detection | Recovery Action | Escalation |
|-------|-----------|-----------------|------------|
| Low Battery | V < 3.3V | Reduce chirp to 8hr, alert | Replace at <3.0V |
| Sensor Drift | ε out of range | Flag quality=0, use last good | Field calibrate |
| No Connectivity | 3 failed TX | Boost TX power, try backup SF | Maintenance dispatch |
| Temperature Fault | Heater stuck ON | Disable heater, alert | Immediate replacement |
| Pressure Loss | <3 PSI (seal breach) | Emergency mode, max alerts | Immediate replacement |

---

## 10. Integration & Dependencies

### 10.1 Upstream Dependencies (What LRZN Needs)

| Dependency | Provider | Interface | Criticality |
|------------|----------|-----------|-------------|
| **PMT Hub** | Field infrastructure | 900MHz LoRa | CRITICAL |
| **RTK Corrections** | DHU → PMT → LRZN | Indirect (PMT positioning) | Medium |
| **Time Sync** | PMT beacon | LoRa downlink | Medium |
| **Config Updates** | Cloud → PMT | LoRa downlink | Low |
| **Firmware OTA** | PMT cache | LoRa multicast | Low |

### 10.2 Downstream Consumers (What Uses LRZN Data)

| Consumer | Purpose | Data Used | Latency Requirement |
|----------|---------|-----------|---------------------|
| **PMT** | Field aggregation | Raw VWC, quality | <1 hour |
| **DHU** | 20m Kriging | Aggregated field | <4 hours |
| **RSS** | 1m Master Grid | District synthesis | <24 hours |
| **Cloud (Zo)** | ML training | Historical archive | <7 days |
| **Farmer Dashboard** | Visualization | Real-time (via PMT) | <15 min |
| **Compliance Ledger** | Water Court evidence | Quality-scored VWC | <24 hours |

### 10.3 API Contracts

**LoRa TLV Contract (LRZN ↔ PMT):**

| Direction | Message | Frequency | Payload Size | SLA |
|-----------|---------|-----------|--------------|-----|
| LRZN → PMT | TELEMETRY | 4hr-5sec (adaptive) | 187 bytes | 95% delivery |
| PMT → LRZN | CONFIG | On change | 64 bytes | 99% delivery (confirmed) |
| PMT → LRZN | PING | Diagnostic | 16 bytes | Best effort |
| LRZN → PMT | ALERT | Event-driven | 187 bytes | 99.9% delivery (3 retries) |

---

## 11. Compliance & Legal

### 11.1 Certifications

| Certification | Status | Body | Notes |
|---------------|--------|------|-------|
| **FCC Part 15** | Approved | FCC ID: 2AFSK-LRZN1 | 915MHz ISM operation |
| **IC RSS-210** | Approved | IC ID: 21099-LRZN1 | Canada operation |
| **CE RED** | In Progress | Notified Body | EU market entry 2027 |
| **UL 50E** | Approved | UL | Outdoor enclosure rating |
| **IP68** | Verified | Internal | 2m submersion tested |
| **RoHS 3** | Compliant | Supplier certs | No restricted substances |
| **REACH** | Compliant | Supplier certs | Chemical safety |

### 11.2 Water Court Admissibility

**Legal Defensibility Features:**

| Feature | Implementation | Evidence Value |
|---------|--------------|----------------|
| **Timestamp Integrity** | GPS-synchronized via PMT | Challenge: Sync accuracy |
| **Measurement Chain** | Factory calibration → Field validation | Challenge: Calibration drift |
| **Anti-Tamper** | Nitrogen pressure seal | Challenge: Physical access |
| **Cryptographic Signing** | AES-256-GCM on all telemetry | Challenge: Data authenticity |
| **Quality Scoring** | Real-time confidence metric | Challenge: Measurement validity |
| **Audit Trail** | PBFT consensus at DHU level | Challenge: Ledger tampering |
| **Cross-Validation** | LRZN vs LRZB vs VFA correlation | Challenge: Sensor failure |

**Admissibility Checklist (State Engineer Review):**

- [ ] Sensor calibration certificate on file
- [ ] Installation photo documentation
- [ ] Pressure seal verification log
- [ ] 90-day measurement continuity
- [ ] Cross-sensor correlation >0.85
- [ ] No quality_score <30 in reporting period
- [ ] PBFT hash chain intact
- [ ] Digital Water Ledger export generated

### 11.3 Data Retention & Privacy

| Data Type | Retention | Storage Location | Access Control |
|-----------|-----------|------------------|----------------|
| Raw telemetry | 7 years | RSS cold storage | Farmer + Court order |
| Aggregated VWC | 10 years | Compliance ledger | Public (anonymized) |
| Calibration certs | 40 years (sled life) | RSS vault | FarmSense QA only |
| Installation photos | 10 years | Cloud (encrypted) | Farmer + Ops |
| Diagnostic logs | 2 years | Cloud | FarmSense support |

---

## 12. Maintenance & Lifecycle

### 12.1 Expected Lifespan

| Component | Design Life | Replacement Trigger | Cost |
|-----------|-------------|----------------------|------|
| **Alpha-Sled (CHDPE)** | 40 years | Physical damage | $12 |
| **Outer Shell (HDPE)** | 40 years | UV degradation | $6.75 |
| **Battery Pack** | 4-6 years | <20% capacity | $13.50 |
| **Electronics Assembly** | 10 years | Obsolescence/failure | $35 |
| **LoRa Module** | 10 years | End-of-life | $15 |
| **Seals** | 10 years | Nitrogen leak | $1.60 |

### 12.2 Preventive Maintenance

**Annual Inspection (Remote):**

```
1. Review quality_score trends (alert if declining)
2. Verify battery voltage trajectory (predict EOL)
3. Check nitrogen pressure logs (alert if dropping)
4. Validate LoRa link margin (alert if degrading)
5. Cross-sensor correlation check (LRZN vs LRZB vs VFA)
```

**3-Year Field Service (Physical):**

```
1. Locate sled via GPS + RFID
2. Excavate to 12" depth
3. Verify nitrogen pressure (+5 PSI)
4. Perform extraction test (winch check)
5. Visual inspection of shell condition
6. Document with photos
7. Re-bury if condition good
8. Flag for replacement if issues found
```

### 12.3 End-of-Life Procedures

**Battery Depletion (<3.0V):**

1. PMT flags low battery alert
2. FieldTools app notifies farmer
3. Maintenance scheduled (next convenient window)
4. Old sled extracted, returned to RSS Sled Hospital
5. Alpha-Sled removed from shell, electronics recycled
6. Battery pack properly disposed (Li-ion recycling)
7. New sled installed in existing shell (if shell condition good)
8. Registry updated with new device ID
9. Old device archived in inventory system

**Complete Unit Failure:**

1. Anomaly detected (quality_score <30 for >24hr)
2. Cross-validation fails (deviation >10% from neighbors)
3. Maintenance dispatched with replacement unit
4. Failed unit extracted, returned to RSS for failure analysis
5. Root cause determined (moisture ingress, component failure, etc.)
6. Warranty claim filed if applicable
7. Process feedback to QA for continuous improvement

### 12.4 Refurbishment Process (Sled Hospital)

**Alpha-Sled Refurbishment at RSS:**

1. Receive extracted sled from field
2. Pressure-decay test (<0.1 PSI drop/15 min)
3. Disassemble in clean room
4. Test all components individually
5. Replace battery pack (mandatory every 4 years)
6. Re-calibrate dielectric sensor
7. Re-flash firmware (latest version)
8. New nitrogen seal (+5 PSI)
9. 48-hour burn-in test
10. Re-certify with new QR code
11. Return to Ready-Rack inventory

---

## 13. Revision History

| Version | Date | Author | Changes | Approval |
|---------|------|--------|---------|----------|
| 1.0 | 2026-01-15 | J. Beebe | Initial LRZ1 specification | Approved |
| 1.1 | 2026-02-20 | Engineering | Added heater specs, ADR table | Approved |
| 1.2 | 2026-03-19 | J. Beebe | **MAJOR**: Renamed LRZ1→LRZN, expanded all sections | **PENDING** |

**Pending Changes (v1.2):**

- [x] Rename LRZ1 → LRZN (Lateral Root Zone Node)
- [x] Expand hardware specifications (full mechanical detail)
- [x] Add complete GPIO pinout
- [x] Document power budget analysis
- [x] Expand firmware specifications (dielectric method)
- [x] Add quality scoring algorithm
- [x] Document installation procedure
- [x] Add deployment patterns (standard, half-section, corner-swing)
- [x] Expand BOM with volume pricing
- [x] Add Water Court admissibility section
- [x] Document Sled Hospital refurbishment

---

## 14. References & Related Documents

| Document | Relationship | Location |
|----------|--------------|----------|
| **LRZB-SPEC.md** | Companion spec (Beacon variant) | `docs/specs/LRZB-SPEC.md` |
| **VFA-SPEC.md** | Upstream validation reference | `docs/specs/VFA-SPEC.md` |
| **PMT-SPEC.md** | Parent hub specification | `docs/specs/PMT-SPEC.md` |
| **DHU-SPEC.md** | District aggregation spec | `docs/specs/DHU-SPEC.md` |
| **SFD-SPEC.md** | Deployment topology | `docs/specs/SFD-SPEC.md` |
| **v2_1_part5_remaining_hardware.md** | Legacy master document | `docs/md/` |
| **MASTER_MANUAL.md** | System-wide architecture | `docs/md/` |

---

*Proprietary IP of bxthre3 inc. — Confidential*
*Unauthorized distribution prohibited*
*For licensing inquiries: licensing@bxthre3.com*

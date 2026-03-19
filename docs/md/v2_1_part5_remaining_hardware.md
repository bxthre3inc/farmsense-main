---
Status: Active
Last Audited: 2026-03-14
Drift Aversion: REQUIRED
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding code or system behavior MUST be reflected here immediately.
> 3. **AI Agent Compliance**: Agents MUST verify the current implementation against this document before proposing changes.
> 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

## 5.4 Pressure & Flow Analyzer (PFA) V1.9

### 5.4.1 Role and Function

**Primary Role:** Wellhead sentry and safety actuator
**Location:** Mounted on wellhead discharge pipe
**Critical Functions:**

1. Measure flow rate with ±1.0% accuracy (ultrasonic transit-time)
2. Monitor pump electrical signatures (current harmonics)
3. Detect wellhead pressure (depth to water)
4. Execute emergency pump shutdown (safety relay)
5. Report to PMT via 900MHz CSS LoRa

### 5.4.2 Flow Measurement

**Sensor: Badger Meter TFX-5000**

| Parameter | Specification |
|-----------|---------------|
| Principle | Ultrasonic transit-time |
| Pipe size | 4" - 12" (clamp-on) |
| Accuracy | ±1.0% of reading |
| Repeatability | ±0.2% |
| Velocity range | 0.1 - 40 ft/s |
| Outputs | 4-20mA, pulse, Modbus |

**Legal Defensibility:**

- Matches "Gold Standard" for State Engineer reporting
- Traceable calibration (annual)
- NIST-traceable standards
- Core evidence for Water Court admissibility

### 5.4.3 Electrical Signature Analysis

**Current Transformers: Magnelab SCT-0400**

| Parameter | Specification |
|-----------|---------------|
| Current range | 5 - 400A |
| Accuracy | ±1% |
| Frequency response | 50/60Hz fundamental + harmonics |
| Installation | Split-core (non-invasive) |

**Predictive Maintenance Algorithm:**
```
FFT analysis of current waveform:

- Fundamental (60Hz): Normal torque
- 2nd harmonic: Bearing wear indicator
- 3rd harmonic: Magnetic saturation
- 5th harmonic: Rotor bar issues
- High frequency (>1kHz): Cavitation

Alert thresholds:

- Bearing: 2nd harmonic >5% of fundamental
- Cavitation: HF energy >threshold
- Efficiency drop: >10% from baseline

```

### 5.4.4 Actuation System

**Safety Relay: Omron G9SE-221-T05**

| Parameter | Specification |
|-----------|---------------|
| Contacts | 2× SPST-NO |
| Rating | 30A @ 240VAC |
| Response time | <50ms |
| SIL rating | SIL 3 (IEC 61508) |

**Reflex Logic Table:**

| Condition | Sensor | Threshold | Action |
|-----------|--------|-----------|--------|
| PMT stall command | IMU | >3g | ACTUATE_STOP |
| Line pressure loss | PBLTX | <5 PSI | ACTUATE_STOP |
| Saturation detected | VFA | >95% VWC at 48" | ACTUATE_STOP |
| Cavitation signature | CT clamps | HF >threshold | ACTUATE_STOP + alert |
| Power anomaly | CT clamps | >110% or <85% | ACTUATE_STOP |

### 5.4.5 Wellhead Depth Measurement

**Sensor: Dwyer PBLTX**

| Parameter | Specification |
|-----------|---------------|
| Principle | Vented differential pressure |
| Range | 0 - 300 ft water depth |
| Accuracy | ±0.25% FS |
| Material | 316 stainless steel |
| Output | 4-20mA |

**Application:**

- Static water level monitoring
- Drawdown tracking during pumping
- Aquifer health assessment

### 5.4.6 PFA Full Bill of Materials

| Component | Supplier | Part # | Unit Cost | Qty | Ext. |
|-----------|----------|--------|-----------|-----|------|
| Flow Meter | Badger Meter | TFX-5000-4 | $425.00 | 1 | $425.00 |
| CT Clamps | Magnelab | SCT-0400 | $45.00 | 3 | $135.00 |
| Depth Sensor | Dwyer | PBLTX-40-30 | $285.00 | 1 | $285.00 |
| Safety Relay | Omron | G9SE-221-T05 | $89.00 | 1 | $89.00 |
| MCU | Nordic | nRF52840-QIAA | $8.50 | 1 | $8.50 |
| Cryptocell | Nordic | CC-310 | $3.00 | 1 | $3.00 |
| LoRa Module | HopeRF | RFM95W-915S2 | $15.00 | 1 | $15.00 |
| Enclosure | Polycase | WP-21F | $78.00 | 1 | $78.00 |
| Battery | Battle Born | BB1220 | $245.00 | 1 | $245.00 |
| Solar Panel | Renogy | 50W | $65.00 | 1 | $65.00 |
| Heater | Omega | KH-505/5-P | $28.00 | 1 | $28.00 |
| Cable/Connector | Various | — | $85.00 | 1 | $85.00 |
| PCB Assembly | JLCPCB | Custom | $95.00 | 1 | $95.00 |
| Calibration | — | — | $125.00 | 1 | $125.00 |
| **PFA TOTAL** | | | | | **$1,679.50** |

---

## 5.5 Vertical Field Anchor (VFA) V2.1

### 5.5.1 Role and Function

**Primary Role:** Deep-truth probe for vertical soil moisture profile
**Location:** Buried vertically, 48" depth
**Key Functions:**

1. Measure 4-depth VWC profile (8", 16", 24", 36")
2. Capture deep percolation and leaching events
3. Provide ground-truth for Kriging algorithms
4. Report to PMT via 900MHz CSS LoRa

### 5.5.2 The 48U Stack Sequence

| Slot | Component | Function | Depth |
|------|-----------|----------|-------|
| 1 | Desiccant Pack | Apex moisture trap | Surface |
| 2-5 | Battery Cartridge #1 | 3× 21700 Li-ion + heater | 0-10" |
| 6-9 | Battery Cartridge #2 | 3× 21700 Li-ion + heater | 10-20" |
| 10 | Advanced Sensor | Root zone ingest (10") | 10" |
| 11-17 | Battery Cartridge #3 | Power reserve | 20-30" |
| 18 | Basic Sensor | VWC/Temp (18") | 18" |
| 19-24 | Spacers | Structural | — |
| 25 | Advanced Sensor | Root anchor (25") | 25" |
| 26-34 | Battery Cartridge #4 | Deep power | 30-40" |
| 35 | Basic Sensor | Wetting front (35") | 35" |
| 36-47 | Battery Cartridge #5 | Deep reserve | 40-48" |
| 48 | Advanced Sensor | Deep percolation (48") | 48" |

### 5.5.3 Advanced vs Basic Sensors

**Advanced Sensor (GroPoint Profile):**

| Parameter | Specification |
|-----------|---------------|
| Measurement | VWC, temperature, EC |
| VWC range | 0-100% |
| Accuracy | ±2% |
| Temperature range | -40°C to +60°C |
| EC range | 0-5 dS/m |
| Interface | SDI-12 |

**Basic Sensor (Capacitive DIY):**

| Parameter | Specification |
|-----------|---------------|
| Measurement | VWC only |
| VWC range | 0-100% |
| Accuracy | ±3% |
| Interface | Analog (12-bit) |
| Cost | $15 vs $150 |

### 5.5.4 The Alpha-Sled Design

**Outer Shell (Permanent):**

| Attribute | Specification |
|-----------|---------------|
| Material | HDPE SDR9 |
| Dimensions | 2.067" OD × 48" L |
| Installation | Buried vertically, flush with surface |
| Taper tip | Friction-molded, monolithic weld |
| Lifespan | 40+ years |

**Alpha-Sled (Removable):**

| Attribute | Specification |
|-----------|---------------|
| Material | CHDPE (conductive HDPE, ESD-safe) |
| Dimensions | 50mm OD × 48" L |
| Insertion | Stainless cable, winch extraction |
| Nitrogen gap | +5 PSI dry N₂ pressurization |
| Sensing | Non-contact capacitive through wall |

### 5.5.5 VFA Full Bill of Materials

| Component | Supplier | Part # | Unit Cost | Qty | Ext. |
|-----------|----------|--------|-----------|-----|------|
| Outer Shell (HDPE) | JM Eagle | SDR9-2 | $6.75 | 1 | $6.75 |
| Alpha-Sled (CHDPE) | Custom | — | $12.00 | 1 | $12.00 |
| Antenna | Taoglas | SS-Whip | $3.50 | 1 | $3.50 |
| MCU | Nordic | nRF52840 | $8.50 | 1 | $8.50 |
| Advanced Sensors | GroPoint | TDT-310S | $47.00 | 3 | $141.00 |
| Basic Sensors | Custom | Cap-12bit | $15.00 | 2 | $30.00 |
| Seals (Viton) | Parker | FKM-001 | $2.40 | 6 | $14.40 |
| Battery Cartridges | Custom | 21700×3 | $16.75 | 5 | $83.75 |
| Desiccant | Dry-Packs | Silica-50g | $3.00 | 1 | $3.00 |
| Nitrogen Valve | Swagelok | SS-1RS4 | $18.00 | 1 | $18.00 |
| Cable Assembly | Various | — | $12.00 | 1 | $12.00 |
| PCB | JLCPCB | Custom | $35.00 | 1 | $35.00 |
| **VFA TOTAL** | | | | | **$358.90** |

---

## 5.6 Lateral Root Zone Surveyor (LRZN/LRZB) V1.2

### 5.6.1 LRZN vs LRZB Distinction

| Attribute | LRZN (Basic) | LRZB (Reference) |
|-----------|--------------|------------------|
| **Role** | Spatial density | Calibration anchor |
| **Sensors** | VWC only | VWC + Temperature |
| **Depth** | Single (variable) | Single (variable) |
| **Accuracy** | ±3% VWC | ±2% VWC, ±0.5°C |
| **Cost** | $29 | $54 |
| **Density** | 12 per field | 4 per field |
| **Purpose** | Kriging interpolation | Ground-truth validation |

### 5.6.2 Field Deployment Pattern

**16-Node Standard Configuration:**

| Ring | Radius | Nodes | Type | Purpose |
|------|--------|-------|------|---------|
| Center | 0% | 1 | LRZB | Pivot point reference |
| Inner | 25% | 3 | LRZN | Near-pivot zone |
| Middle | 50% | 4 | LRZB | Mid-field validation |
| Outer | 75% | 8 | LRZN | Edge interpolation |

**Placement Strategy:**

- Avoid wheel tracks (compaction zones)
- Avoid previous crop rows (residue effects)
- Maximize spatial coverage
- Ensure LoRa visibility to PMT

### 5.6.3 PCBA GPIO Pinout

**nRF52840 GPIO Assignment:**

| Pin | Function | Direction |
|-----|----------|-----------|
| P0.02 | ADC0 (dielectric) | Input |
| P0.03 | ADC1 (temperature - LRZB) | Input |
| P0.04 | LoRa NSS | Output |
| P0.05 | LoRa DIO0 | Input |
| P0.06 | LoRa DIO1 | Input |
| P0.07 | LoRa DIO2 | Input |
| P0.28 | SPI SCK | Output |
| P0.29 | SPI MISO | Input |
| P0.30 | SPI MOSI | Output |
| P0.31 | Status LED | Output |
| P1.00 | Wake Button | Input |
| P1.01 | Battery ADC | Input |

### 5.6.4 Dielectric Sensing Method

**Principle:** High-frequency capacitive (~100MHz)
**Implementation:**

- Two electrodes embedded in sled wall
- Field projected through HDPE into soil
- Dielectric constant (ε) measured
- Topp equation converts to VWC:

  ```
  VWC = -5.3×10⁻² + 2.92×10⁻²×ε - 5.5×10⁻⁴×ε² + 4.3×10⁻⁶×ε³
  ```

**Calibration:**

- Factory: Air (ε=1), water (ε=80)
- Field: Saturated soil, oven-dry soil
- Temperature correction (LRZB only)

### 5.6.5 BOM Comparison

| Component | LRZN | LRZB | Delta |
|-----------|------|------|-------|
| nRF52840 | $4.50 | $4.50 | — |
| LoRa RFM95W | $15.00 | $15.00 | — |
| PCB | $8.00 | $8.00 | — |
| Dielectric IC | $12.00 | $12.00 | — |
| Temperature IC | — | $6.00 | +$6 |
| Battery (LiSOCl2) | $4.50 | $4.50 | — |
| Housing (HDPE) | $6.50 | $6.50 | — |
| Assembly | $5.00 | $5.00 | — |
| Testing | $2.00 | $3.00 | +$1 |
| **TOTAL** | **$29.00** | **$54.30** | **+$25.30** |

---

## 5.7 Single Field Deployment (SFD) Configurations

### 5.7.1 SFD-P: Standard Pivot (126-acre Circular)

**Configuration:**

| Component | Quantity | Unit Cost | Extended |
|-----------|----------|-----------|----------|
| PMT | 1 | $1,166.50 | $1,166.50 |
| PFA | 1 | $1,679.50 | $1,679.50 |
| VFA | 2 | $358.90 | $717.80 |
| LRZB | 4 | $54.30 | $217.20 |
| LRZN | 12 | $29.00 | $348.00 |
| Installation Labor | — | $124.00 | $124.00 |
| **SFD-P TOTAL** | | | **$4,253.00** |

**Coverage:**

- Resolution: 50m (compliance) to 1m (enterprise)
- Nodes: 20 per field
- Telemetry: 100% via PMT

### 5.7.2 SFD-C: Corner-Swing Arm (150+ acre)

**Additional Components:**

| Component | Quantity | Purpose |
|-----------|----------|---------|
| CSA | 1 | Corner-swing arm tracking |
| VFA | +2 | Extended coverage |
| LRZB | +2 | Additional validation |
| LRZN | +4 | Extended interpolation |

**CSA (Corner-Swing Auditor):**

- BLE 5.2 distance ranging
- Calculates swing-arm angle
- ±0.1° joint resolution
- Reports to PMT

**SFD-C TOTAL: ~$5,800** (vs $4,253 for SFD-P)

### 5.7.3 SFD-F: Flood/Surface Irrigation

**Configuration:**

| Component | Quantity | Purpose |
|-----------|----------|---------|
| Static-PMT | 1 | Fixed field hub |
| PFA | 1 | Headgate flow |
| VFA | 4 | Cross-field transect |
| LRZB | 8 | Validation grid |
| LRZN | 20 | Interpolation density |

**Special Features:**

- Wetting Front Propagation algorithms
- Slope-aware runoff modeling
- Ditch-level scheduling

**SFD-F TOTAL: ~$6,200**

---

## 5.8 Subdistrict 1 Scale (1,280 Fields)

### 5.8.1 Phase 1: Compliance Foundation

**Scope:** 1,280 fields, basic PMT+PFA only
**Purpose:** Immediate Water Court defensibility
**Timeline:** Q1-Q2 2026

| Category | Calculation | Amount |
|----------|-------------|--------|
| PMTs (1,280 × $1,166.50) | | $1,493,120 |
| PFAs (1,280 × $1,679.50) | | $2,149,760 |
| Installation (1,280 × $124) | | $158,720 |
| RSS Infrastructure | | $95,000 |
| Initial DHUs (6) | | $21,924 |
| **PHASE 1 TOTAL** | | **$4,028,524** |

### 5.8.2 Phase 2: Full Ecosystem Saturation

**Scope:** Add VFAs, LRZs, full DHU network
**Purpose:** 1m resolution, predictive maintenance
**Timeline:** Q3 2026 - Q2 2027

| Component | Units | Unit Cost | Extended |
|-----------|-------|-----------|----------|
| VFAs (2 per field) | 2,560 | $358.90 | $918,784 |
| LRZBs (4 per field) | 5,120 | $54.30 | $278,016 |
| LRZNs (12 per field) | 15,360 | $29.00 | $445,440 |
| DHUs (full 25) | 19 | $3,654.00 | $69,426 |
| RSS Expansion | 1 | $200,000 | $200,000 |
| Fleet (3 trucks) | 3 | $45,000 | $135,000 |
| Sled Hospital | 1 | $75,000 | $75,000 |
| Installation (Phase 2) | | | $192,000 |
| **PHASE 2 TOTAL** | | | **$2,313,666** |

### 5.8.3 Full Ecosystem Fleet BOM

| Component | Phase 1 Only | Phase 2 Added | Total Fleet |
|-----------|--------------|---------------|-------------|
| RSS | 1 | 0 | 1 |
| DHU | 6 | 19 | 25 |
| PMT | 1,280 | 0 | 1,280 |
| PFA | 1,280 | 0 | 1,280 |
| VFA | 0 | 2,560 | 2,560 |
| LRZB | 0 | 5,120 | 5,120 |
| LRZN | 0 | 15,360 | 15,360 |
| **Total Active Nodes** | **2,566** | **23,040** | **25,606** |

**Fleet Value:** $6,342,190 CAPEX
**Annual SaaS Revenue:** $7,664,640 (Year 2)
**Maintenance Reserve:** 10% annually = $634,219

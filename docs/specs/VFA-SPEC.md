---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Device Code: VFA
Full Name: Vertical Field Anchor
Version: 2.1
Category: Level 0 Field Sensor (Deep Truth)
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding implementation MUST be reflected here immediately.
> 3.**AI Agent Compliance**: Agents MUST verify current implementation against this document before proposing changes.
> 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.
> 5. **EDIT RESTRICTION**: Changes require explicit approval from brodiblanco (Jeremy Beebe, CEO).
> 6. **ADDITIVE ONLY**: Specifications may only expand, never contract or summarize.

---

# VFA V2.1: Vertical Field Anchor

## 1. Executive Summary

### 1.1 Role and Function

The VFA (Vertical Field Anchor) is the **ground-truth standard** for soil moisture measurement, providing deep-profile volumetric water content (VWC) at four depths from 8" to 48". As the "Deep Truth" probe, the VFA serves as the calibration reference for all lateral sensors (LRZN/LRZB) and provides critical evidence for deep percolation, leaching, and aquifer recharge monitoring.

**Primary Functions:**

1. Measure VWC profile at 8", 16", 24", 36" depths simultaneously
2. Provide ±2% VWC accuracy with factory + field calibration
3. Capture deep percolation and leaching events below root zone
4. Serve as primary ground-truth for Kriging algorithm validation
5. Monitor soil temperature profile (thermal dynamics)
6. Report to PMT via 900MHz CSS LoRa

**Deployment Context:**

- Standard density: 2-4 VFA per field (strategic placement)
- Placement: Near wellhead, mid-field, and edge positions
- Target MTBF: 80,000 hours (9.1 years)
- Unit economics: $358.90 BOM cost for 4-depth measurement

### 1.2 VFA vs LRZ Distinction

| Attribute | VFA (Vertical Field Anchor) | LRZN/LRZB (Lateral Root Zone) |
|-----------|----------------------------|-------------------------------|
| **Measurement** | 4-depth vertical profile | Single depth lateral |
| **Depth Range** | 8" to 48" (1.2m) | 8" to 36" (configurable) |
| **Sensors** | 4× GroPoint Profile | 1× capacitive |
| **Accuracy** | ±2% VWC (each depth) | ±3% LRZN, ±2% LRZB |
| **Soil Contact** | Direct (buried in soil) | Non-contact (through wall) |
| **Extraction** | Alpha-Sled removable | Alpha-Sled removable |
| **BOM Cost** | $358.90 | $29 (LRZN), $54 (LRZB) |
| **Density** | 2-4 per field | 16 per field (total) |
| **Purpose** | Deep truth, calibration | Spatial interpolation |

**Key Differentiator:** The VFA's 48" penetration captures the **deep percolation zone** — critical for detecting nitrate leaching, aquifer recharge, and over-irrigation waste. No lateral sensor can match this depth.

### 1.3 The 48U Stack Sequence

The VFA implements a modular "48U" (48-unit) stack architecture:

| Slot | Component | Function | Depth | Notes |
|------|-----------|----------|-------|-------|
| 1 | Desiccant Pack | Apex moisture trap | Surface | Replaceable cartridge |
| 2-5 | Battery Cartridge #1 | 3× 21700 Li-ion + heater | 0-10" | Zone 1 power |
| 6-9 | Battery Cartridge #2 | 3× 21700 Li-ion + heater | 10-20" | Zone 2 power |
| 10 | **Advanced Sensor** | VWC/Temp/EC | **10"** | Root zone edge |
| 11-17 | Battery Cartridge #3 | Power reserve | 20-30" | Zone 3 power |
| 18 | **Basic Sensor** | VWC only | **18"** | Mid-root zone |
| 19-24 | Structural Spacers | Mechanical integrity | — | HDPE tubes |
| 25 | **Advanced Sensor** | VWC/Temp/EC | **25"** | Root anchor |
| 26-34 | Battery Cartridge #4 | Deep power | 30-40" | Zone 4 power |
| 35 | **Basic Sensor** | VWC only | **35"** | Wetting front |
| 36-47 | Battery Cartridge #5 | Deep reserve | 40-48" | Zone 5 power |
| 48 | **Advanced Sensor** | VWC/Temp/EC | **48"** | Deep percolation |

**Total:** 4 sensors (3 advanced + 1 basic at each of 2 depths) distributed across 48" depth

---

## 2. Hardware Specifications

### 2.1 Alpha-Sled Design

**Outer Shell (Permanent):**

| Attribute | Specification |
|-----------|---------------|
| **Material** | HDPE SDR9 (Schedule DR9) |
| **Dimensions** | 2.067" OD × 48" L (52.5mm × 1219mm) |
| **Wall Thickness** | 0.188" (4.8mm) |
| **Installation** | Buried vertically, flush with surface |
| **Taper Tip** | Friction-molded HDPE, monolithic weld |
| **Lifespan** | 40+ years |
| **Color** | Terracotta (soil-matching, UV stable) |
| **Marking** | Laser-etched QR code + device ID |

**Alpha-Sled (Removable Core):**

| Attribute | Specification |
|-----------|---------------|
| **Material** | CHDPE (Conductive High-Density Polyethylene, ESD-safe) |
| **Dimensions** | 50mm OD × 48" L |
| **Insertion Method** | Vertical drop-in with alignment keys |
| **Extraction** | Stainless steel cable, winch-assisted (500lb capacity) |
| **Nitrogen Gap** | +5 PSI dry N₂ pressurization |
| **Pressure Monitoring** | Swagelok SS-1RS4 valve with gauge port |
| **Seal System** | Double O-ring (Viton FKM) at top/bottom |

### 2.2 Sensor Specifications

**Advanced Sensor: GroPoint Profile TDT-310S**

| Parameter | Specification |
|-----------|---------------|
| **Manufacturer** | Acclima (GroPoint brand) |
| **Model** | TDT-310S (True Dielectric Technology) |
| **Measurement** | VWC, Temperature, Electrical Conductivity (EC) |
| **VWC Range** | 0-100% |
| **VWC Accuracy** | ±2% |
| **Temperature Range** | -40°C to +60°C |
| **Temperature Accuracy** | ±0.5°C |
| **EC Range** | 0-5 dS/m |
| **EC Accuracy** | ±3% |
| **Interface** | SDI-12 (serial digital) |
| **Power** | 9-18VDC, 4mA (active) |
| **Measurement Time** | 300ms |
| **Cable Length** | 3m (integrated) |
| **Depth Placement** | 10", 25", 48" (3 units) |

**Basic Sensor: Custom Capacitive**

| Parameter | Specification |
|-----------|---------------|
| **Principle** | High-frequency capacitive |
| **Frequency** | 100MHz |
| **Measurement** | VWC only |
| **VWC Range** | 0-100% |
| **VWC Accuracy** | ±3% |
| **Interface** | Analog (12-bit ADC) |
| **Cost** | $15 (vs $150 GroPoint) |
| **Depth Placement** | 18", 35" (2 units) |

**Sensor Placement Rationale:**

- **10" (Advanced)**: Top of active root zone, quick response to irrigation
- **18" (Basic)**: Mid-root zone, cost-effective coverage
- **25" (Advanced)**: Deepest active roots, critical moisture anchor
- **35" (Basic)**: Wetting front monitoring, leaching detection
- **48" (Advanced)**: Deep percolation, aquifer recharge evidence

### 2.3 Power System

**Battery Architecture:**

| Cartridge | Cells | Capacity | Voltage | Depth Zone | Purpose |
|-----------|-------|----------|---------|------------|---------|
| #1 | 3× 21700 | 6.2Wh | 11.1V | 0-10" | Surface sensors + heater |
| #2 | 3× 21700 | 6.2Wh | 11.1V | 10-20" | Upper root zone |
| #3 | 3× 21700 | 6.2Wh | 11.1V | 20-30" | Mid-profile |
| #4 | 3× 21700 | 6.2Wh | 11.1V | 30-40" | Deep root zone |
| #5 | 3× 21700 | 6.2Wh | 11.1V | 40-48" | Deep percolation |
| **TOTAL** | **15 cells** | **31Wh** | — | — | 8+ year life |

**Heating System:**

| Parameter | Specification |
|-----------|---------------|
| **Heater Type** | 5W resistive cartridge (per zone) |
| **Heater Model** | Omega KH-505/5-P |
| **Activation** | < -10°C ambient, < 0°C soil temp |
| **Control** | PWM via nRF52840 |
| **Zones** | 5 independent zones (per cartridge) |

**Power Budget Analysis:**

| Function | Active Current | Duration | Daily Energy |
|----------|---------------|----------|--------------|
| Deep Sleep | 12µA | 3h 45m | 0.05mWh |
| Sensor Warmup | 45mA | 2 sec | 0.62mWh |
| GroPoint Read (3×) | 25mA | 900ms | 1.13mWh |
| Capacitive Read (2×) | 18mA | 500ms | 0.45mWh |
| LoRa TX | 120mA | 200ms | 8.33mWh |
| MCU Processing | 15mA | 100ms | 0.42mWh |
| **Daily Total** | — | — | **11.0mWh** |
| **8-Year Capacity** | — | — | **31Wh** |
| **Margin** | — | — | **23% reserve** |

### 2.4 Electrical Architecture

**Main Controller:**

| Attribute | Specification |
|-----------|---------------|
| **MCU** | Nordic nRF52840-QIAA |
| **Core** | ARM Cortex-M4F @ 64MHz |
| **Flash** | 1MB |
| **RAM** | 256KB |
| **Crypto** | ARM CryptoCell-310 |
| **LoRa** | HopeRF RFM95W-915S2 |

**SDI-12 Interface:**

| Parameter | Value |
|-----------|-------|
| **Protocol** | SDI-12 v1.3 |
| **Baud Rate** | 1200 bps |
| **Voltage** | 12V power, 5V logic |
| **Addressing** | 0-9 (3 GroPoint sensors = addresses 0,1,2) |
| **Cable** | 3-wire (power, data, ground) |

**ADC Channels (Basic Sensors):**

| Channel | Sensor | Depth | Notes |
|---------|--------|-------|-------|
| ADC0 | Capacitive 1 | 18" | 12-bit SAR |
| ADC1 | Capacitive 2 | 35" | 12-bit SAR |
| ADC2 | Battery Voltage | Internal | Voltage divider |
| ADC3 | Temperature (backup) | PCB | NTC thermistor |

---

## 3. Firmware Specifications

### 3.1 Measurement Sequence

**Standard Measurement Cycle:**

```c
void perform_measurement_cycle(void) {
    // Wake from deep sleep
    power_up_sensors();
    
    // Read advanced sensors (SDI-12)
    for (int i = 0; i < 3; i++) {
        sdi12_wake(sensors[i].address);
        delay_ms(100);
        readings[i] = sdi12_measure(sensors[i].address);
        // readings[i] contains: vwc, temp, ec
    }
    
    // Read basic sensors (ADC)
    readings[3].vwc = adc_read(ADC0);  // 18" depth
    readings[3].temp = interpolate_temp(readings[0].temp, readings[2].temp);
    readings[4].vwc = adc_read(ADC1);  // 35" depth
    readings[4].temp = readings[2].temp;  // Use 48" as proxy
    
    // Apply calibration coefficients
    apply_calibration(&readings);
    
    // Compute quality scores
    for (int i = 0; i < 5; i++) {
        readings[i].quality = compute_quality_score(readings[i]);
    }
    
    // Package and transmit
    transmit_telemetry(readings, 5);
    
    // Return to sleep
    power_down_sensors();
    schedule_next_wake();
}
```

### 3.2 Calibration System

**Factory Calibration:**

| Step | Action | Standard | Accuracy |
|------|--------|----------|----------|
| 1 | Air reading | ε = 1.0 (±0.1%) | Baseline |
| 2 | Deionized water | ε = 80.4 (±0.5%) | Full scale |
| 3 | Known VWC #1 | 10% ±0.5% | Low point |
| 4 | Known VWC #2 | 25% ±0.5% | Mid point |
| 5 | Known VWC #3 | 45% ±0.5% | High point |
| 6 | Temperature sweep | 5°C to 40°C | Compensation |

**Field Calibration:**

```c
void field_calibration_procedure(void) {
    // Step 1: Collect gravimetric samples at each sensor depth
    for (int depth : {10, 18, 25, 35, 48}) {
        float gravimetric_vwc = take_soil_sample(depth);
        float sensor_raw = read_sensor_at_depth(depth);
        
        cal_table[depth].gravimetric = gravimetric_vwc;
        cal_table[depth].raw = sensor_raw;
    }
    
    // Step 2: Compute linear correction factors
    for (int depth : DEPTHS) {
        // Linear regression: true = a × raw + b
        fit_linear(&cal_table[depth], &a[depth], &b[depth]);
    }
    
    // Step 3: Store to EEPROM
    write_calibration_to_eeprom(a, b);
    
    // Step 4: Report to cloud
    report_calibration_event(field_id, a, b);
}
```

### 3.3 Deep Percolation Detection

**Algorithm:**

```python
def detect_deep_percolation(vfa_readings_48h):
    """
    Detect water movement below root zone (48" depth)
    indicating over-irrigation or leaching event
    """
    vwc_48in = [r.depth_48in.vwc for r in vfa_readings_48h]
    
    # Check if 48" VWC is increasing while shallower layers stable
    shallows_stable = all(abs(vwc_10in[i] - vwc_10in[i-1]) < 0.02 
                          for i in range(1, len(readings)))
    deep_rising = vwc_48in[-1] > vwc_48in[0] + 0.03  # 3% increase
    
    if shallows_stable and deep_rising:
        return {
            'event': 'DEEP_PERCOLATION',
            'confidence': 0.85,
            'recommendation': 'Reduce irrigation rate',
            'evidence': {
                'vwc_48in_start': vwc_48in[0],
                'vwc_48in_end': vwc_48in[-1],
                'duration_hours': 48
            }
        }
```

---

## 4. Bill of Materials

| Component | Supplier | Part # | Unit Cost | Qty | Extended |
|-----------|----------|--------|-----------|-----|----------|
| **Advanced Sensors** | Acclima | TDT-310S | $150.00 | 3 | $450.00 |
| **Basic Sensors** | Custom | Cap-12bit | $15.00 | 2 | $30.00 |
| **MCU** | Nordic | nRF52840-QIAA | $8.50 | 1 | $8.50 |
| **LoRa Module** | HopeRF | RFM95W-915S2 | $15.00 | 1 | $15.00 |
| **Battery Cells** | LG Chem | INR21700-M50T | $4.50 | 15 | $67.50 |
| **Battery Mgmt** | TI | BQ40Z50 (×5) | $2.80 | 5 | $14.00 |
| **Heaters** | Omega | KH-505/5-P | $8.00 | 5 | $40.00 |
| **Outer Shell** | JM Eagle | SDR9-2 | $6.75 | 1 | $6.75 |
| **Alpha-Sled** | Custom | CHDPE | $12.00 | 1 | $12.00 |
| **Antenna** | Taoglas | SS-Whip | $3.50 | 1 | $3.50 |
| **Seals (Viton)** | Parker | FKM-001 | $2.40 | 6 | $14.40 |
| **Desiccant** | Dry-Packs | 50g | $3.00 | 1 | $3.00 |
| **Nitrogen Valve** | Swagelok | SS-1RS4 | $18.00 | 1 | $18.00 |
| **Main PCB** | JLCPCB | 6-layer | $35.00 | 1 | $35.00 |
| **PCB Assembly** | JLCPCB | PCBA | $45.00 | 1 | $45.00 |
| **TOTAL BOM** | | | | | **$762.65** |
| **Target Retail** | | | | | **$358.90** | Volume: 1K+

---

## 5. Revision History

| Version | Date | Author | Changes | Approval |
|---------|------|--------|---------|----------|
| 2.0 | 2026-01-15 | J. Beebe | Initial VFA v2 spec | Approved |
| 2.1 | 2026-03-19 | J. Beebe | Expanded Alpha-Sled detail, added 48U stack, deep percolation detection | **PENDING** |

---

*Proprietary IP of bxthre3 inc. — Confidential*

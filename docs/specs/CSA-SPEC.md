---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Device Code: CSA
Full Name: Corner Swing Arm
Version: 1.0
Category: Level 0 Field Sensor (Extension)
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

# CSA V1.0: Corner Swing Arm

## 1. Executive Summary

### 1.1 Role and Function

The CSA (Corner Swing Arm) is the **Pivot Extension Monitor** — a specialized sensor suite that tracks the extension arm on corner-swing and linear-move irrigation systems. While center-pivots irrigate circular fields, many systems have corner arms that extend into square field corners, or linear systems that traverse rectangular fields. The CSA ensures these extended sections receive the same precision monitoring as the main span.

**Primary Functions:**

1. **Extension Tracking**: Monitor swing arm angle and extension length
2. **Position Calculation**: Compute precise nozzle coordinates
3. **Flow Monitoring**: Track extended-section water application
4. **Terrain Compensation**: Adjust for elevation changes
5. **Zone Reporting**: Feed data to PMT for VRI inclusion

**When CSA is Required:**

| Pivot Type | CSA Needed | Coverage |
|------------|------------|----------|
| **Standard Center Pivot** | No | Circular only |
| **Corner Swing Arm** | Yes | Square field corners |
| **Linear Move** | Yes | Rectangular fields |
| **Bender Arm** | Optional | Irregular boundaries |

**Critical Distinction:**

| Attribute | CSA (Extension) | PMT (Main Span) |
|-----------|-----------------|-----------------|
| **Location** | End of extension arm | Main span tower |
| **Motion** | Variable radius/angle | Fixed radius, variable angle |
| **Sensors** | Angle, length, flow | Position, IMU, aggregation |
| **Reporting** | To PMT | To DHU |
| **Per System** | 0-1 | 1 |

**Key Differentiator:** The CSA enables **non-circular field coverage** — critical for farms with square or rectangular fields where a standard center-pivot leaves dry corners. Without the CSA, these corner areas receive no monitoring, creating compliance gaps and water waste.

---

## 2. Hardware Specifications

### 2.1 Position Tracking

**Arm Angle Encoder:**

| Parameter | Specification |
|-----------|---------------|
| **Manufacturer** | AMS (Austria Micro Systems) |
| **Model** | AS5048A |
| **Principle** | Magnetic Hall effect |
| **Resolution** | 14-bit (0.022°) |
| **Accuracy** | ±0.05° |
| **Interface** | SPI (10MHz) |
| **Update Rate** | 1kHz |
| **Redundancy** | Dual encoders (primary + backup) |

**Extension Length Sensor:**

| Parameter | Specification |
|-----------|---------------|
| **Type** | Cable-drawn potentiometer |
| **Range** | 0-150 ft (adjustable) |
| **Resolution** | 0.1 ft (1.2 inches) |
| **Linearity** | ±0.1% FS |
| **Cable** | Stainless steel, UV resistant |
| **Spring Return** | Constant tension, 5 lb pull |

**GPS Augmentation (Optional):**

| Parameter | Specification |
|-----------|---------------|
| **Module** | u-blox NEO-M9N |
| **Accuracy** | 2-3m (standard GPS) |
| **Purpose** | Absolute backup positioning |
| **Update Rate** | 10Hz |
| **Integration** | Fused with encoder data |

### 2.2 Compute Platform

**MCU: Nordic nRF52840**

| Parameter | Specification |
|-----------|---------------|
| **Core** | Arm Cortex-M4 @ 64MHz |
| **Flash** | 1MB |
| **RAM** | 256KB |
| **Radio** | Bluetooth 5 / 802.15.4 |
| **Crypto** | ARM TrustZone, AES-256 |
| **Interface** | SPI, I2C, UART, PWM |

**Position Calculation Algorithm:**

```c
typedef struct {
    float main_span_angle_deg;     // From PMT via LoRa
    float extension_angle_deg;     // From CSA encoder
    float extension_length_ft;     // From CSA cable sensor
    float pivot_center_lat;
    float pivot_center_lon;
    float main_span_radius_ft;
} csa_position_input_t;

typedef struct {
    float nozzle_lat;
    float nozzle_lon;
    float total_radius_ft;
    float elevation_ft;
    float coverage_area_acres;
} csa_position_output_t;

csa_position_output_t compute_nozzle_position(csa_position_input_t *input) {
    csa_position_output_t output;
    
    // Convert angles to radians
    float main_rad = DEG_TO_RAD(input->main_span_angle_deg);
    float ext_rad = DEG_TO_RAD(input->extension_angle_deg);
    
    // Main span end position
    float main_x = input->main_span_radius_ft * cos(main_rad);
    float main_y = input->main_span_radius_ft * sin(main_rad);
    
    // Extension offset
    float ext_x = input->extension_length_ft * cos(main_rad + ext_rad);
    float ext_y = input->extension_length_ft * sin(main_rad + ext_rad);
    
    // Total position
    float total_x = main_x + ext_x;
    float total_y = main_y + ext_y;
    
    output.total_radius_ft = sqrt(total_x * total_x + total_y * total_y);
    
    // Convert to lat/lon (simplified equirectangular)
    float delta_lat = total_y / FEET_PER_DEGREE_LAT;
    float delta_lon = total_x / (FEET_PER_DEGREE_LON * cos(DEG_TO_RAD(input->pivot_center_lat)));
    
    output.nozzle_lat = input->pivot_center_lat + delta_lat;
    output.nozzle_lon = input->pivot_center_lon + delta_lon;
    
    // Compute coverage area (approximate sector)
    float coverage_radius_ft = output.total_radius_ft + 15;  // + nozzle spread
    output.coverage_area_acres = M_PI * coverage_radius_ft * coverage_radius_ft / SQUARE_FEET_PER_ACRE;
    
    return output;
}
```

### 2.3 Communication

**To PMT (900MHz CSS LoRa):**

| Parameter | Specification |
|-----------|---------------|
| **Module** | HopeRF RFM95W-915S2 |
| **Frequency** | 915MHz |
| **Power** | +20dBm |
| **Protocol** | Proprietary (16-byte payload) |
| **Rate** | Every 5 seconds when moving |
| **Latency** | <100ms to PMT |

**CSA Payload (16 bytes):**

```c
typedef struct __attribute__((packed)) {
    uint8_t device_type;           // 0x06 = CSA
    uint8_t device_id;
    uint16_t main_span_angle;      // 0.01° resolution
    uint16_t extension_angle;
    uint16_t extension_length;     // 0.1 ft resolution
    uint16_t flow_rate;           // GPM × 10
    uint16_t quality_score;
    uint32_t timestamp_offset;
} csa_payload_t;
```

### 2.4 Flow Monitoring

**Electromagnetic Flow Meter:**

| Parameter | Specification |
|-----------|---------------|
| **Type** | Insertion magmeter |
| **Range** | 50-500 GPM |
| **Accuracy** | ±0.5% of reading |
| **Output** | 4-20mA, pulse |
| **Material** | 316 stainless steel |

**Flow Integration:**

- CSA flow + PMT flow = Total system flow
- Enables per-section water accounting
- Critical for corner-area compliance

---

## 3. Mechanical Specifications

### 3.1 Enclosure

| Parameter | Specification |
|-----------|---------------|
| **Material** | Polycarbonate, UV stabilized |
| **Rating** | NEMA 4X (IP66) |
| **Mounting** | Pivot tower bracket |
| **Access** | Tool-less hinged cover |
| **Size** | 8" × 6" × 4" |

### 3.2 Cable Management

| Component | Specification |
|-----------|---------------|
| **Draw Cable** | 1/16" stainless, 7×19 construction |
| **Sheave** | Nylon, 3" diameter |
| **Spring Housing** | Powder-coated steel |
| **Travel** | 0-150 ft (field adjustable) |
| **Tension** | 5 lb constant pull |

### 3.3 Power

| Component | Specification |
|-----------|---------------|
| **Source** | 24VAC from pivot panel |
| **Conversion** | On-board buck converter |
| **Battery** | 18650 backup (4 hour runtime) |
| **Consumption** | 25mA @ 12V (active), 5mA (sleep) |

---

## 4. Bill of Materials

| Component | Supplier | Part # | Unit Cost | Qty | Extended |
|-----------|----------|--------|-----------|-----|----------|
| **MCU** | Nordic | nRF52840-QIAA | $8.50 | 1 | $8.50 |
| **Angle Encoder** | AMS | AS5048A | $18.00 | 2 | $36.00 |
| **Cable Sensor** | Celesco | PT101-0015 | $145.00 | 1 | $145.00 |
| **LoRa Module** | HopeRF | RFM95W-915S2 | $15.00 | 1 | $15.00 |
| **Flow Meter** | Rosemount | 8711EM | $450.00 | 1 | $450.00 |
| **GPS Module** | u-blox | NEO-M9N | $35.00 | 1 | $35.00 |
| **Enclosure** | Polycase | WP-21F | $78.00 | 1 | $78.00 |
| **Mounting Kit** | Custom | CSA bracket | $45.00 | 1 | $45.00 |
| **Battery** | Samsung | 18650-35E | $8.00 | 1 | $8.00 |
| **PCB** | JLCPCB | 4-layer | $25.00 | 1 | $25.00 |
| **PCBA** | JLCPCB | Assembly | $45.00 | 1 | $45.00 |
| **Cable Assembly** | Various | Sensor harness | $35.00 | 1 | $35.00 |
| **TOTAL BOM** | | | | | **$925.50** |
| **Target Retail** | | | | | **$1,799.00** | 1.94× markup |

---

## 5. Deployment

### 5.1 Installation

| Step | Specification | Time |
|------|---------------|------|
| 1 | Mount enclosure on extension tower | 30 min |
| 2 | Install angle encoder on pivot joint | 45 min |
| 3 | Route draw cable to anchor point | 60 min |
| 4 | Install flow meter in extension line | 45 min |
| 5 | Connect to PMT LoRa network | 15 min |
| 6 | Calibrate zero and span positions | 30 min |
| **Total** | | **4.25 hours** |

### 5.2 Calibration

| Parameter | Method | Accuracy |
|-----------|--------|----------|
| **Zero Angle** | Magnetic alignment with main span | ±0.1° |
| **Max Extension** | Physical measurement | ±0.5 ft |
| **Flow Zero** | Dry pipe baseline | ±0.1 GPM |
| **Flow Span** | Volumetric test | ±1% |

---

## 6. Corner Coverage Analysis

| Field Shape | Without CSA | With CSA |
|-------------|-------------|----------|
| **Square 160 acres** | 126 acres irrigated (79%) | 160 acres (100%) |
| **Water Savings** | — | 31% reduction in dry corners |
| **Compliance Risk** | High (unmonitored areas) | Low (full coverage) |
| **ROI** | — | 2.3 years (water fees avoided) |

---

## 7. Revision History

| Version | Date | Author | Changes | Approval |
|---------|------|--------|---------|----------|
| 1.0 | 2026-03-19 | J. Beebe | Initial CSA specification | **PENDING** |

---

*Proprietary IP of bxthre3 inc. — Confidential*

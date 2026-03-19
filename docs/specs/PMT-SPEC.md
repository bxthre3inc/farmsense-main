---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Device Code: PMT
Full Name: Pivot Motion Tracker
Version: 1.7
Category: Level 1.5 Field Hub
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

# PMT V1.7: Pivot Motion Tracker

## 1. Executive Summary

### 1.1 Role and Function

The PMT (Pivot Motion Tracker) is the **Field Hub** — the central aggregator and kinematic auditor for all field operations. Mounted on the pivot span 10-15 feet above ground, the PMT tracks the irrigation machine's position in real-time, aggregates data from all sub-sensors (VFA, LRZN, LRZB, PFA), and routes telemetry to the District Hub (DHU).

**Primary Functions:**

1. **RTK GNSS Positioning**: <5cm absolute accuracy for compliance mapping
2. **IMU Stall Detection**: Detect obstructions and trigger safety stops
3. **Field State Aggregation**: 187-byte payload bundling all sensor data
4. **Edge Compute**: 50m grid IDW interpolation
5. **Dual Radio Routing**: 900MHz CSS LoRa (sensors) + 2.4GHz/LTE-M (DHU)
6. **Flow Meter Integration**: Last-span flow monitoring

**Critical Distinction:**

| Attribute | PMT (Field Hub) | DHU (District) | RSS (Regional) |
|-----------|-----------------|----------------|----------------|
| **Level** | 1.5 (Edge) | 2 (District) | 3 (Regional) |
| **Compute** | ESP32-S3 | Jetson Orin Nano | Threadripper PRO |
| **Grid** | 50m IDW | 20m/10m Kriging | 1m Master |
| **Sensors Served** | 20-34 per pivot | 100 pivots | Districts |
| **Authority** | Stall detection | PBFT consensus | FHE vaulting |
| **Per Field** | 1 | 1 per 100 fields | 1 per district |

**Key Differentiator:** The PMT is the **only device with direct kinematic awareness** of the irrigation machine. It knows exactly where water is being applied at all times — critical for VRI (Variable Rate Irrigation) compliance and water right defense.

---

## 2. Hardware Specifications

### 2.1 Position & Orientation System

**RTK GNSS: u-blox ZED-F9P**

| Parameter | Specification |
|-----------|---------------|
| **Manufacturer** | u-blox |
| **Model** | ZED-F9P-02B |
| **Constellations** | GPS, GLONASS, Galileo, BeiDou |
| **Bands** | L1/L2/L5 (multi-band) |
| **RTK Accuracy** | <5cm horizontal, <10cm vertical |
| **Update Rate** | 10Hz (100ms latency) |
| **Convergence** | <10 seconds (hot start) |
| **Correction** | NTRIP via LTE (DHU provides corrections) |
| **Antenna** | Tallysman TW3972 (multi-band, IP67) |

**IMU: Bosch BNO055**

| Parameter | Specification |
|-----------|---------------|
| **Manufacturer** | Bosch |
| **Model** | BNO055 |
| **Sensors** | 3-axis accel, 3-axis gyro, 3-axis mag |
| **Fusion** | On-chip sensor fusion (quaternion output) |
| **Accelerometer Range** | ±2g / ±4g / ±8g / ±16g (configurable) |
| **Gyroscope Range** | ±125°/s to ±2000°/s |
| **Interface** | I2C (400kHz) |
| **Update Rate** | 100Hz |
| **Calibration** | Auto-calibration for accel/gyro |

**Stall Detection Algorithm:**

```c
bool detect_stall_condition(imu_data_t *imu, gnss_data_t *gnss, float dt) {
    // Compute expected angular velocity from GNSS
    float expected_angular_velocity = compute_angular_velocity_from_gnss(gnss, dt);
    
    // Get actual angular velocity from IMU gyroscope Z-axis
    float actual_angular_velocity = imu->gyro_z;  // degrees/second
    
    // Detect stall condition
    if (gnss->ground_speed > 0.5 &&  // Pivot is moving (not parked)
        fabs(expected_angular_velocity - actual_angular_velocity) > STALL_THRESHOLD_DEG_S) {
        
        // Check for abnormal acceleration (impact)
        float accel_magnitude = sqrt(imu->accel_x*imu->accel_x + 
                                     imu->accel_y*imu->accel_y + 
                                     imu->accel_z*imu->accel_z);
        
        if (accel_magnitude > STALL_ACCEL_THRESHOLD_G) {
            return true;  // STALL DETECTED
        }
    }
    return false;
}
```

**Stall Response Protocol:**

| Stage | Action | Latency | Authority |
|-------|--------|---------|-----------|
| Detection | IMU/GNSS mismatch + high-g | 200ms | PMT Autonomous |
| Verification | Confirm over 500ms window | 500ms | PMT Autonomous |
| Command | Send ACTUATE_STOP to PFA | <100ms | PMT → PFA |
| Execution | PFA opens safety relay | <50ms | PFA Autonomous |
| **Total** | **From detection to pump stop** | **<850ms** | — |

### 2.2 Compute Platform

**MCU: Espressif ESP32-S3-WROOM-1**

| Parameter | Specification |
|-----------|---------------|
| **Manufacturer** | Espressif |
| **Model** | ESP32-S3-WROOM-1-N8 |
| **Core** | Dual-core Xtensa LX7 @ 240MHz |
| **WiFi** | 802.11 b/g/n (2.4GHz) |
| **Bluetooth** | BLE 5.0 |
| **Flash** | 8MB (QSPI) |
| **PSRAM** | 8MB (Octal, 120MB/s) |
| **AI Acceleration** | Vector instructions for ML |

**Edge Interpolation (50m IDW):**

```c
void compute_idw_grid_50m(sensor_reading_t *sensors, int num_sensors,
                          float grid[GRID_50M_SIZE][GRID_50M_SIZE]) {
    for (int y = 0; y < GRID_50M_SIZE; y++) {
        for (int x = 0; x < GRID_50M_SIZE; x++) {
            float lat = grid_origin_lat + y * 50.0 / METERS_PER_DEGREE;
            float lon = grid_origin_lon + x * 50.0 / METERS_PER_DEGREE;
            
            float weighted_sum = 0;
            float weight_sum = 0;
            
            for (int i = 0; i < num_sensors; i++) {
                float d = haversine_distance(lat, lon, sensors[i].lat, sensors[i].lon);
                if (d < 100) {  // 100m radius
                    float w = 1.0 / (d * d);  // Inverse distance squared
                    weighted_sum += w * sensors[i].vwc;
                    weight_sum += w;
                }
            }
            
            grid[y][x] = (weight_sum > 0) ? weighted_sum / weight_sum : NAN;
        }
    }
}

// Performance: 20×20 grid in <100ms on ESP32-S3
```

### 2.3 Radio Systems

**900MHz CSS LoRa (Sensor Downlink):**

| Parameter | Specification |
|-----------|---------------|
| **Module** | HopeRF RFM95W-915S2 |
| **Frequency** | 915MHz ISM band |
| **Modulation** | CSS LoRa (SF7-SF12) |
| **Sensitivity** | -148dBm @ SF12 |
| **Output Power** | +20dBm (100mW) |
| **Range** | 5km+ line-of-sight, 1km canopy |
| **Bandwidth** | 125kHz |
| **Coding Rate** | 4/5 |
| **Antenna** | 1/4-wave whip, 3dBi |

**2.4GHz/LTE-M (DHU Uplink):**

| Parameter | Specification |
|-----------|---------------|
| **WiFi** | ESP32-S3 integrated |
| **LTE-M** | Quectel BG96 (optional) |
| **Bands** | B2/B4/B12/B13 (US) |
| **Data Rate** | 300kbps LTE-M |
| **Fallback** | WiFi mesh to DHU |

### 2.4 Field State Payload

**187-Byte Aggregation Format:**

```c
typedef struct __attribute__((packed)) {
    // Header (7 bytes)
    uint8_t protocol_version;      // 0x02
    uint8_t device_type;           // 0x05 (PMT)
    uint16_t sequence_number;
    uint32_t timestamp_unix;
    
    // GNSS Position (16 bytes)
    int32_t latitude_e7;           // Degrees × 10^7
    int32_t longitude_e7;
    int32_t altitude_mm;
    uint16_t accuracy_mm;
    uint16_t ground_speed_mm_s;
    uint16_t heading_degrees;
    uint8_t num_satellites;
    uint8_t fix_type;              // 0=none, 1=2D, 2=3D, 3=RTK
    
    // IMU Data (12 bytes)
    int16_t accel_x, accel_y, accel_z;    // mg
    int16_t gyro_x, gyro_y, gyro_z;         // 0.01 deg/s
    int16_t mag_x, mag_y, mag_z;          // 0.1 µT
    
    // Aggregated Sensor Data (96 bytes = 6 sensors × 16 bytes)
    subnode_data_t vfa[2];         // 2 VFAs
    subnode_data_t lrzb[2];        // 2 LRZBs
    subnode_data_t lrzn[2];        // 2 LRZNs
    
    // Flow Data (8 bytes)
    uint32_t flow_total_gal;
    uint16_t flow_rate_gpm;
    uint16_t flow_quality;
    
    // Grid Statistics (32 bytes)
    uint16_t grid_mean_vwc;        // 0.01%
    uint16_t grid_min_vwc;
    uint16_t grid_max_vwc;
    uint16_t grid_std_vwc;
    uint8_t grid_data[24];         // Compressed grid tile
    
    // Status & Diagnostics (16 bytes)
    uint8_t cpu_load_percent;
    uint8_t heap_free_percent;
    int16_t temperature_c;
    uint16_t battery_mv;
    uint32_t uptime_seconds;
    uint8_t error_flags;
    uint8_t reserved[5];
    
} pmt_field_state_t;  // Total: 187 bytes

typedef struct __attribute__((packed)) {
    uint8_t sensor_type;           // 0x01=VFA, 0x02=LRZB, 0x03=LRZN
    uint8_t sensor_id;
    uint16_t vwc_10cm;             // 0.01%
    uint16_t vwc_25cm;
    uint16_t vwc_48cm;
    int16_t temp_c;
    uint16_t quality_score;
    uint32_t timestamp_offset;     // Seconds since PMT timestamp
} subnode_data_t;  // 16 bytes per sensor
```

---

## 3. Installation & Deployment

### 3.1 Physical Mounting

**Location Requirements:**

| Aspect | Specification |
|--------|---------------|
| **Mount Point** | Last span tower, upstream end |
| **Height** | 10-15 ft above ground |
| **Clearance** | 2 ft from tower legs |
| **Orientation** | Antenna array facing center pivot |
| **Vibration** | Pivot motion <0.5g expected |
| **Weather** | Fully exposed (IP67 rated) |

**Antenna Configuration:**

| Antenna | Type | Location | Purpose |
|---------|------|----------|---------|
| GNSS | Tallysman TW3972 | Top of enclosure | RTK positioning |
| LoRa 915MHz | 1/4-wave whip | Side mount | Sensor downlink |
| WiFi/LTE | Panel antenna | Directional | DHU uplink |

### 3.2 Power System

| Component | Specification |
|-----------|---------------|
| **Primary** | 24VAC from pivot panel (transformer) |
| **Battery** | 4× 18650 Li-ion (14.4V, 6.8Ah) |
| **Runtime** | 8 hours (pivot stopped) |
| **Charging** | MPPT solar trickle (20W panel) |
| **Consumption** | 450mA @ 12V (active), 15mA (sleep) |

---

## 4. Bill of Materials

| Component | Supplier | Part # | Unit Cost | Qty | Extended |
|-----------|----------|--------|-----------|-----|----------|
| **MCU Module** | Espressif | ESP32-S3-WROOM-1-N8 | $4.50 | 1 | $4.50 |
| **GNSS Module** | u-blox | ZED-F9P-02B | $65.00 | 1 | $65.00 |
| **GNSS Antenna** | Tallysman | TW3972 | $45.00 | 1 | $45.00 |
| **IMU** | Bosch | BNO055 | $12.00 | 1 | $12.00 |
| **LoRa Module** | HopeRF | RFM95W-915S2 | $15.00 | 1 | $15.00 |
| **LTE Module** | Quectel | BG96 | $35.00 | 1 | $35.00 |
| **SIM Holder** | Various | Micro-SIM | $2.50 | 1 | $2.50 |
| **Battery Pack** | Custom | 4S1P 18650 | $32.00 | 1 | $32.00 |
| **Solar Panel** | Renogy | 20W | $35.00 | 1 | $35.00 |
| **Charge Controller** | Victron | MPPT 75/5 | $65.00 | 1 | $65.00 |
| **Enclosure** | Hammond | 1554JGY | $48.00 | 1 | $48.00 |
| **Mounting Kit** | Custom | Pivot bracket | $75.00 | 1 | $75.00 |
| **Antenna Set** | Taoglas | Multi-band kit | $55.00 | 1 | $55.00 |
| **PCB** | JLCPCB | 6-layer | $45.00 | 1 | $45.00 |
| **PCBA** | JLCPCB | Assembly | $85.00 | 1 | $85.00 |
| **Cable Assembly** | Various | Sensor harness | $125.00 | 1 | $125.00 |
| **Flow Meter** | Badger | FT-100 (optional) | $180.00 | 0 | $0 |
| **TOTAL BOM** | | | | | **$636.00** |
| **Target Retail** | | | | | **$1,249.00** | 2× BOM markup |

---

## 5. Revision History

| Version | Date | Author | Changes | Approval |
|---------|------|--------|---------|----------|
| 1.0 | 2025-06-15 | J. Beebe | Initial PMT specification | Approved |
| 1.5 | 2025-09-20 | J. Beebe | Added RTK GNSS, 187-byte payload | Approved |
| 1.7 | 2026-03-19 | J. Beebe | Expanded stall detection, dual-radio architecture | **PENDING** |

---

*Proprietary IP of bxthre3 inc. — Confidential*

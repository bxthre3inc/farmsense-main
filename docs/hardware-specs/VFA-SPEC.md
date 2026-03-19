---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Device Code: VFA
Full Name: Vertical Field Anchor
Version: 2.1
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding implementation MUST be reflected here immediately.
> 3. **AI Agent Compliance**: Agents MUST verify current implementation against this document before proposing changes.
> 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

---

# VFA V2.1: Vertical Field Anchor

## 1. Executive Summary

The VFA (Vertical Field Anchor) is a deep-truth soil probe providing vertical moisture profiling across four depths (8", 16", 24", 36"). Buried vertically to 48" depth, the VFA captures deep percolation events, leaching, and the complete soil moisture profile necessary for SPAC (Soil-Plant-Atmosphere Continuum) modeling. The VFA uses a proprietary "Alpha-Sled" design enabling sensor retrieval and maintenance without excavation.

**Primary Role:** Deep vertical moisture profiling for SPAC modeling
**Secondary Role:** Ground-truth validation for deep percolation and leaching events
**Deployment Target:** 2-4 units per standard field

---

## 2. Functional Requirements

### 2.1 Core Capabilities

| Function | Specification | Priority |
|----------|---------------|----------|
| Multi-Depth VWC | 4 depths: 8", 16", 24", 36" | P0 |
| VWC Accuracy | ±2% (Advanced), ±3% (Basic) | P0 |
| Soil Temperature | At each sensor depth | P1 |
| EC Measurement | Electrical conductivity (salinity) | P1 |
| Deep Percolation Detection | 36" wetting front capture | P0 |
| Telemetry | 900MHz CSS LoRa to PMT | P0 |
| Battery Life | 10+ years (large battery reserve) | P0 |
| Serviceability | Retrievable Alpha-Sled design | P0 |

### 2.2 The 48U Stack Sequence

The VFA is organized as a 48-unit vertical stack ("48U"), combining sensors, batteries, and spacers in a calculated sequence for optimal power distribution and sensing coverage.

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

---

## 3. Hardware Architecture

### 3.1 Mechanical Specifications

**Outer Shell (Permanent):**

| Attribute | Specification |
|-----------|---------------|
| Material | HDPE SDR9 (high-density polyethylene) |
| Dimensions | 2.067" OD × 48" L (Schedule 40 equivalent) |
| Installation | Buried vertically, flush with surface |
| Taper Tip | Friction-molded, monolithic weld |
| Cap | Threaded HDPE access cap with antenna port |
| Lifespan | 40+ years (HDPE UV/chemical resistance) |
| Antenna | 900MHz whip, 2" protrusion |

**Alpha-Sled (Removable Insert):**

| Attribute | Specification |
|-----------|---------------|
| Material | CHDPE (conductive HDPE, ESD-safe) |
| Dimensions | 50mm OD × 48" L |
| Insertion | Stainless cable, winch-assisted |
| Extraction | Nitrogen pressurization + mechanical winch |
| Nitrogen Gap | +5 PSI dry N₂ maintains positive pressure |
| Sensing | Non-contact capacitive through CHDPE wall |
| Connector | IP67-rated multi-pin at cap interface |

### 3.2 Sensing Subsystem

**Advanced Sensors (Slots 10, 25, 48): GroPoint Profile TDT-310S**

| Parameter | Specification |
|-----------|---------------|
| Measurement | VWC, Temperature, EC |
| VWC Range | 0-100% |
| VWC Accuracy | ±2% |
| VWC Resolution | 0.1% |
| Temperature Range | -40°C to +60°C |
| Temperature Accuracy | ±0.5°C |
| EC Range | 0-5 dS/m |
| EC Accuracy | ±5% |
| Interface | SDI-12 (digital) |
| Power | 4-28VDC, 50mA active |
| Sensor Type | Time Domain Transmissometry (TDT) |

**Basic Sensors (Slots 18, 35): Custom Capacitive**

| Parameter | Specification |
|-----------|---------------|
| Measurement | VWC only |
| VWC Range | 0-100% |
| VWC Accuracy | ±3% |
| VWC Resolution | 0.1% |
| Interface | Analog (12-bit ADC) |
| Power | 3.3V, 5mA active |
| Cost | $15 vs $150 (Advanced) |

**Cost-Performance Optimization:**
- Advanced sensors at critical depths (root zone, deep percolation)
- Basic sensors for interpolation points
- 3 Advanced + 2 Basic = optimal cost/performance ratio

### 3.3 Processing Subsystem

**MCU: Nordic Semiconductor nRF52840**

| Feature | Specification |
|---------|-------------|
| Core | ARM Cortex-M4 @ 64MHz |
| Flash | 1MB |
| RAM | 256KB |
| SDI-12 | Bit-banged (software) |
| ADC | 12-bit SAR |
| Crypto | ARM TrustZone + Cryptocell CC-310 |
| Power Modes | Sophisticated deep-sleep |

**Sensor Reading Sequence:**
1. Wake from deep sleep (RTC alarm)
2. Power up sensor rail (sequenced to minimize surge)
3. Query SDI-12 sensors (Advanced)
4. Sample analog sensors (Basic)
5. Compile CBOR payload
6. Transmit via LoRa
7. Return to deep sleep

### 3.4 Communication Subsystem

**LoRa Module: HopeRF RFM95W-915S2**

| Parameter | Specification |
|-----------|---------------|
| Frequency | 915MHz ISM |
| Modulation | LoRa CSS |
| Bandwidth | 125kHz |
| Spreading Factor | SF10 (extended range for ground-level antenna) |
| TX Power | +17dBm (50mW) |
| Sensitivity | -152dBm @ SF10 |
| Range | 1.5km+ to PMT |
| Antenna | Taoglas SS-Whip (stainless steel) |

### 3.5 Power Subsystem

**Battery Architecture: 5 Cartridges × 3× 21700 Li-ion**

| Attribute | Specification |
|-----------|---------------|
| Cell Type | 21700 cylindrical Li-ion |
| Cell Capacity | 5000mAh per cell |
| Cells per Cartridge | 3 (series: 11.1V nominal) |
| Cartridge Capacity | 5000mAh @ 11.1V = 55.5Wh |
| Total Batteries | 15 cells, 5 cartridges |
| Total Energy | 277.5Wh |

**Power Budget:**

| Mode | Daily Frequency | Daily Energy |
|------|-----------------|--------------|
| Sensor reading (all 5) | 6× / day | 18Wh |
| LoRa TX | 6× / day | 1.2Wh |
| Quiescent (sleep) | 24 hours | 2.4Wh |
| **Daily Total** | — | **21.6Wh** |
| **Annual Total** | — | **7.9kWh** |
| **Battery Life** | — | **35+ years theoretical, 10+ years rated** |

**Heating System (Cold Weather):**

| Component | Specification |
|-----------|---------------|
| Heater Type | Resistive film heater |
| Power | 5W per cartridge zone |
| Activation | <0°C soil temp |
| Duration | 30 min pre-measurement |
| Annual Impact | ~5% battery capacity |

---

## 4. Bill of Materials

| Component | Supplier | Part Number | Unit Cost | Qty | Extended |
|-----------|----------|-------------|-----------|-----|----------|
| Outer Shell (HDPE) | JM Eagle | SDR9-2.067 | $6.75 | 1 | $6.75 |
| Alpha-Sled (CHDPE) | Custom extrusion | 50mm OD | $12.00 | 1 | $12.00 |
| Antenna | Taoglas | SS-Whip-915 | $3.50 | 1 | $3.50 |
| MCU | Nordic | nRF52840-QIAA | $8.50 | 1 | $8.50 |
| Advanced Sensors | Acclima | TDT-310S | $47.00 | 3 | $141.00 |
| Basic Sensors | Custom | Cap-12bit | $15.00 | 2 | $30.00 |
| Seals (Viton) | Parker | FKM-214 | $2.40 | 6 | $14.40 |
| Battery Cartridges | Custom | 21700×3 holder | $16.75 | 5 | $83.75 |
| 21700 Cells | Samsung | INR21700-50S | $12.00 | 15 | $180.00 |
| Desiccant | Dry-Packs | Silica-100g | $3.00 | 1 | $3.00 |
| Nitrogen Valve | Swagelok | SS-1RS4 | $18.00 | 1 | $18.00 |
| Cable Assembly | Various | Multi-conductor | $12.00 | 1 | $12.00 |
| PCB | JLCPCB | 4-layer | $35.00 | 1 | $35.00 |
| **TOTAL BOM** | | | | | **$537.90** |

**Target Price:** $358.90/unit at 1,000+ volume (cell cost reduction)

---

## 5. The Alpha-Sled Design

### 5.1 Retrieval Procedure

1. **Attach Winch Cable:** Connect to sled extraction loop
2. **Pressurize Nitrogen:** Open valve to +5 PSI
3. **Extract:** Winch pulls sled upward at 1"/sec
4. **Service:** Replace sensors, batteries, or entire sled
5. **Re-insert:** Lower new/refurbished sled, release nitrogen
6. **Seal:** Torque cap to 15 N·m

**Service Time:** 15 minutes (vs. 4+ hours for traditional excavation)

### 5.2 Nitrogen System

| Parameter | Specification |
|-----------|---------------|
| Gas | Dry nitrogen (N₂), 99.999% pure |
| Pressure | +5 PSI above ambient |
| Purpose | Prevents soil ingress during extraction |
| Source | Portable N₂ bottle or RSS nitrogen station |
| Connector | Quick-connect Swagelok SS-QC4 |

---

## 6. Deployment Specifications

### 6.1 Field Placement

**Standard Configuration:**
- 2 VFAs per 126-acre field (minimum)
- 4 VFAs for high-value crops or research fields
- Placement: 25% and 75% of pivot radius
- Orientation: Perpendicular to pivot travel direction

**Depth Zones Monitored:**

| Depth | Zone | Crop Relevance |
|-------|------|----------------|
| 8" | Shallow root zone | Early growth, seed germination |
| 16" | Active root zone | Peak uptake, tuber development |
| 24" | Deep root zone | Stress avoidance, late season |
| 36" | Deep percolation | Leaching detection, aquifer recharge |

### 6.2 Installation Procedure

1. **Auger Bore:** 3" diameter hole to 48" depth
2. **Insert Outer Shell:** Drop HDPE casing to bottom
3. **Backfill:** Sand around casing, native soil on top
4. **Install Alpha-Sled:** Lower via cable to bottom
5. **Connect Antenna:** Torque whip antenna to cap
6. **Seal:** Thread cap, torque to spec
7. **Nitrogen Charge:** Pressurize to +5 PSI
8. **Commission:** Register with PMT, verify all sensors

**Installation Time:** 45 minutes (with auger)

---

## 7. Telemetry Protocol

### 7.1 Payload Format (CBOR)

```c
typedef struct {
    uint32_t device_id;
    uint32_t timestamp;
    uint16_t vwc_8in;          // 8" depth VWC × 100
    uint16_t vwc_16in;         // 16" depth VWC × 100
    uint16_t vwc_24in;         // 24" depth VWC × 100
    uint16_t vwc_36in;         // 36" depth VWC × 100
    int16_t  temp_8in;         // 8" temp × 10 (decidegrees C)
    int16_t  temp_16in;        // 16" temp × 10
    int16_t  temp_24in;        // 24" temp × 10
    int16_t  temp_36in;        // 36" temp × 10
    uint16_t ec_8in;           // EC at 8" (dS/m × 100)
    uint16_t battery_pct;      // Battery percentage
    int8_t   rssi;
    uint8_t  quality_score;
    uint8_t  reserved[4];
} vfa_payload_t;               // 36 bytes total
```

### 7.2 Transmission Schedule

| Mode | Interval | Trigger |
|------|----------|---------|
| STANDARD | 4 hours | Time-based |
| IRRIGATION | 15 minutes | PMT signals active irrigation |
| ALERT | 5 minutes | Deep percolation detected (>30% at 36") |
| DIAGNOSTIC | On-demand | Manual trigger from PMT |

---

## 8. Deep Percolation Detection

### 8.1 Algorithm

```python
def detect_deep_percolation(vwc_profile, previous_profile):
    """
    Detect water moving below root zone (36" depth)
    Returns: (detected: bool, severity: int)
    """
    delta_36 = vwc_profile['36in'] - previous_profile['36in']
    
    if delta_36 > 0.05:  # >5% increase at 36"
        return True, 1  # Minor percolation
    elif delta_36 > 0.10:  # >10% increase
        return True, 2  # Significant percolation
    elif delta_36 > 0.20:  # >20% increase
        return True, 3  # Severe leaching event
    
    return False, 0
```

**Alert Routing:**
- Severity 1: Logged, included in next regular report
- Severity 2: Immediate chirp to PMT, farmer notification
- Severity 3: Immediate chirp + PMT reflex logic (irrigation stop consideration)

---

## 9. Compliance & Certifications

| Standard | Status | Notes |
|----------|--------|-------|
| FCC Part 15.247 | ✅ | 915MHz ISM operation |
| IP68 Rating | ✅ | Submersible to 1m |
| RoHS 3 | ✅ | Lead-free |
| UL 2595 | ✅ | Battery system safety |
| CE Marking | 🔄 | In progress |

---

## 10. Maintenance & Lifecycle

### 10.1 Service Intervals

| Component | Interval | Action |
|-----------|----------|--------|
| Alpha-Sled retrieval | 5 years | Inspect, replace batteries |
| Battery replacement | 10 years | Full cartridge swap |
| Sensor recalibration | 2 years | Field gravimetric check |
| Outer shell | 40 years | Visual inspection only |

### 10.2 Sled Hospital (RSS)

**Refurbishment Process:**
1. Receive retrieved Alpha-Sled via RSS logistics
2. Pressure-decay test (<0.1 PSI drop / 15 min)
3. Disassemble, clean, inspect
4. Replace all O-rings and seals
5. Install fresh batteries and sensors
6. Reprogram MCU with calibration
7. Nitrogen purge and reseal
8. Return to field-ready inventory

---

## 11. Integration & APIs

### 11.1 Device Registration

```json
{
  "device_type": "VFA",
  "hardware_version": "2.1",
  "firmware_version": "3.0.2",
  "device_id": "VFA-1234ABCD",
  "field_id": "field-550e8400",
  "installed_at": "2026-03-19T10:00:00Z",
  "gps_location": {
    "lat": 37.456789,
    "lon": -105.987654
  },
  "depths": {
    "sensor_1": {"depth_in": 8, "type": "advanced"},
    "sensor_2": {"depth_in": 16, "type": "basic"},
    "sensor_3": {"depth_in": 24, "type": "advanced"},
    "sensor_4": {"depth_in": 36, "type": "basic"},
    "sensor_5": {"depth_in": 48, "type": "advanced"}
  },
  "warranty_expires": "2031-03-19"
}
```

### 11.2 SPAC Integration

```json
{
  "device_id": "VFA-1234ABCD",
  "timestamp": "2026-03-19T14:00:00Z",
  "spac_profile": {
    "root_zone": {"vwc": 0.245, "temp_c": 18.5, "depth": 16},
    "shallow": {"vwc": 0.198, "temp_c": 19.2, "depth": 8},
    "deep": {"vwc": 0.312, "temp_c": 17.1, "depth": 24},
    "percolation": {"vwc": 0.156, "temp_c": 15.8, "depth": 36}
  },
  "mad_status": "NOMINAL",
  "percolation_alert": false
}
```

---

## 12. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-06-01 | Initial 3-depth design | Engineering |
| 2.0 | 2025-11-15 | Alpha-Sled retrieval, 5 sensors | Mechanical |
| 2.1 | 2026-03-19 | Cost reduction, mixed sensor types | Documentation |

---

## 13. Related Documentation

- `LRZN-SPEC.md` — Lateral density sensors
- `LRZB-SPEC.md` — Temperature reference beacons
- `PMT-SPEC.md` — Field hub aggregator
- `SFD-SPEC.md` — Deployment configurations
- `RSS-SPEC.md` — Sled Hospital operations

---

*Proprietary IP of bxthre3 inc. — Confidential*
*© 2026 bxthre3 inc. All rights reserved.*

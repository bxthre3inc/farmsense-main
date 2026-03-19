---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Device Code: DHU
Full Name: District Hub Unit
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

# DHU V1.9: District Hub Unit

## 1. Executive Summary

The DHU (District Hub Unit) is a Level 2 edge compute node serving as the coordination point for up to 100 center-pivot fields within a district. Mounted on a 35-foot timber pole or tower structure, the DHU performs 20m/10m Ordinary Kriging, maintains PBFT consensus for the AllianceChain water ledger, provides RTK base station corrections to all subordinate PMTs, and maintains a 30-day "Black Box" audit cache for compliance continuity during backhaul failures.

**Primary Role:** District-level edge compute and coordination
**Secondary Role:** PBFT consensus node for Digital Water Ledger
**Tertiary Role:** RTK base station for sub-meter positioning
**Deployment Target:** 1 unit per 100-pivot district (~10,000 acres)

---

## 2. Functional Requirements

### 2.1 Core Capabilities

| Function | Specification | Priority |
|----------|---------------|----------|
| Field Coordination | 100 PMTs, 3,400 sensors | P0 |
| Kriging Compute | 20m/10m Ordinary Kriging | P0 |
| PBFT Consensus | AllianceChain ledger validation | P0 |
| RTK Base Station | ±2cm corrections to all PMTs | P0 |
| Black Box Cache | 30-day audit preservation | P0 |
| Backhaul | Fiber or 5GHz PtP microwave | P0 |
| LoRa Gateway | 900MHz for static sensors | P0 |

### 2.2 District Architecture

**DHU Coverage Model:**

| Metric | Specification |
|--------|---------------|
| Field Radius | 10km (6.2 miles) |
| Max PMTs | 100 |
| Max Sensors | 3,400 (34 per field) |
| Area Covered | ~10,000 acres |
| Population | 150-250 farms |

**Hierarchical Role:**
- **Level 0:** Sensors (VFA, LRZ, PFA) — data ingestion
- **Level 1.5:** PMT — field aggregation, 50m grid
- **Level 2:** DHU — district coordination, 20m/10m grid, PBFT
- **Level 3:** RSS — regional master, 1m grid, legal vault
- **Level 4:** Cloud — global analytics, ML training

---

## 3. Hardware Architecture

### 3.1 Mechanical Specifications

| Attribute | Specification |
|-----------|---------------|
| Mounting | 35' Class 4 timber pole or tower |
| Enclosure | Fibrebyn FRP cabinet, 24" × 20" × 12" |
| Mount Height | 30 feet (above obstructions) |
| Wind Rating | 120 mph with ice loading |
| Solar/Wind | Optional (if no grid) |
| Battery Backup | 4-hour runtime (grid failure) |
| Weight | 45 lbs (electronics) + 15 lbs (battery) |
| Operating Temp | -40°C to +60°C |

**Cabinet Zones:**
- **Zone A:** Compute (heatsink side facing north)
- **Zone B:** Power (batteries, solar charge controller)
- **Zone C:** Radio (antenna bulkhead, lightning protection)

### 3.2 Compute Subsystem

**Edge AI: NVIDIA Jetson Orin Nano 8GB**

| Feature | Specification |
|---------|-------------|
| CPU | 6-core ARM Cortex-A78AE @ 1.5GHz |
| GPU | 1024-core NVIDIA Ampere GPU |
| AI Performance | 40 TOPS |
| Memory | 8GB 128-bit LPDDR5 |
| Storage | 128GB Swissbit PSLC SSD (industrial) |
| Video Encode | 1080p60 (4 streams) |
| Interfaces | GbE, USB 3.2, M.2, GPIO |

**Kriging Performance:**

| Grid Resolution | Processing Time | Frequency |
|-----------------|-----------------|-----------|
| 20m IDW | 500ms | Every 15 minutes |
| 10m Ordinary Kriging | 3 seconds | Every hour |
| Variogram fitting | 15 seconds | Daily |
| PBFT consensus | <1 second | Per block (1 min) |

**Black Box Cache:**

| Parameter | Specification |
|-----------|---------------|
| Storage | 128GB Swissbit PSLC SSD |
| Retention | 30 days of audit packets |
| Write Pattern | Append-only, circular buffer |
| Encryption | AES-256-XTS at rest |
| Hash Chain | SHA-256 linking for tamper evidence |

### 3.3 RTK Base Station Subsystem

**GNSS Base: u-blox ZED-F9P**

| Parameter | Specification |
|-----------|---------------|
| Constellations | GPS, GLONASS, Galileo, BeiDou |
| Bands | L1/L2 multi-band |
| Base Accuracy | ±2cm (known point surveyed) |
| Correction Output | RTCM 3.3 (1004, 1006, 1012, 1033) |
| Update Rate | 1Hz corrections |
| Range | 10km+ radius |

**Base Station Requirements:**
- Surveyed position (±1cm absolute, via OPUS or PPP)
- Clear sky view (no obstructions above 15°)
- Stable monument or structure
- Continuous power (base never moves)

**Correction Distribution:**
- 2.4GHz LTU: broadcast to all PMTs
- RTCM injection via cellular (backup)
- NTRIP server (for external users)

### 3.4 Communication Subsystems

**Backhaul (Primary):**

| Option | Technology | Bandwidth | Range |
|--------|------------|-----------|-------|
| A | Fiber optic | 1Gbps | 20km |
| B | 5GHz PtP | 500Mbps | 10km |
| C | LTE-A | 100Mbps | Carrier dependent |

**PTP Radio: Ubiquiti AirFiber 5XHD**

| Parameter | Specification |
|-----------|---------------|
| Frequency | 5.7GHz |
| Bandwidth | 500Mbps+ |
| Range | 10km+ |
| Latency | <1ms |
| PoE | 24V |
| Antenna | 34dBi dish |

**PMT Downlink (2.4GHz):**

| Parameter | Specification |
|-----------|---------------|
| Technology | Ubiquiti LTU (proprietary) |
| Band | 2.4GHz ISM |
| Bandwidth | 20MHz |
| Throughput | 10Mbps per PMT |
| Client Capacity | 100 PMTs |
| Sector Antenna | 120° × 3 sectors |

**LoRa Gateway (900MHz):**

| Parameter | Specification |
|-----------|---------------|
| Concentrator | MultiTech mCard XL |
| Channels | 8 simultaneous |
| Bandwidth | 125kHz |
| Sensitivity | -142dBm |
| Capacity | 10,000+ sensors |
| Coverage | 5km radius |

### 3.5 AllianceChain PBFT Node

**Consensus Requirements:**

| Parameter | Specification |
|-----------|---------------|
| Minimum Nodes | 4 DHUs per consensus group |
| Block Time | 60 seconds |
| Block Size | 1,000 water rights transactions |
| Finality | 1 block (immediate) |
| BFT Tolerance | f < n/3 (33% Byzantine fault tolerance) |

**PBFT State Machine:**
```
1. REQUEST: Client sends water transaction
2. PRE-PREPARE: Leader proposes block
3. PREPARE: 2f+1 nodes validate
4. COMMIT: 2f+1 nodes commit
5. REPLY: Confirmation to client
```

**Water Rights Transactions:**
- Irrigation event start/stop
- Volume pumped (PFA attestation)
- Zone irrigated (PMT attestation)
- Timestamp (GPS-synchronized)
- Digital signature (device key)

### 3.6 Power Subsystem

**Primary: Grid AC**

| Parameter | Specification |
|-----------|---------------|
| Input | 120/240VAC, 30A service |
| Conversion | 48VDC distribution |
| PSU | Redundant 600W supplies |
| Efficiency | 92% |

**Backup: Battery**

| Component | Specification |
|-----------|---------------|
| Chemistry | LiFePO₄ |
| Capacity | 200Ah @ 48V = 9.6kWh |
| Runtime | 4 hours at full load |
| Cycles | 3000+ @ 80% DOD |
| BMS | Integrated, remote monitoring |

**Solar (Optional Remote Sites):**

| Component | Specification |
|-----------|---------------|
| Panels | 4 × 400W = 1.6kW |
| Controller | MPPT 150/60 |
| Battery | 400Ah @ 48V |
| Autonomy | 3 days (no sun) |

**Power Budget:**

| Component | Power | Notes |
|-----------|-------|-------|
| Jetson Orin Nano | 25W | Peak during Kriging |
| SSD | 5W | Always on |
| ZED-F9P | 0.5W | Always on |
| LTU Sector | 15W | ×3 = 45W |
| LoRa Gateway | 10W | Always on |
| AirFiber | 20W | If PtP active |
| Heater | 100W | Cold weather only |
| **Total** | **~100W** | 200W with heater |

---

## 4. Bill of Materials

| Component | Supplier | Part Number | Unit Cost | Qty | Extended |
|-----------|----------|-------------|-----------|-----|----------|
| Edge AI | NVIDIA | Jetson Orin Nano 8GB | $499.00 | 1 | $499.00 |
| SSD | Swissbit | X-60m 128GB PSLC | $245.00 | 1 | $245.00 |
| GNSS Base | u-blox | ZED-F9P-02B | $68.00 | 1 | $68.00 |
| LoRa Gateway | MultiTech | Conduit AEP + mCard XL | $895.00 | 1 | $895.00 |
| LTU Sector | Ubiquiti | LTU-Rocket + 120° antenna | $650.00 | 3 | $1,950.00 |
| AirFiber | Ubiquiti | AF-5XHD + dish | $1,200.00 | 1 | $1,200.00 |
| Enclosure | Fibrebyn | FRP-242012-H | $485.00 | 1 | $485.00 |
| Battery | Simpliphi | PHI-3.8-48-130 | $2,800.00 | 1 | $2,800.00 |
| Power Supply | Mean Well | RST-5000-48 | $485.00 | 2 | $970.00 |
| Surge Protection | Polyphaser | IS-PTC-111 | $245.00 | 1 | $245.00 |
| Antenna (GNSS) | Trimble | Zephyr 3 Geodetic | $1,200.00 | 1 | $1,200.00 |
| Pole | Prescott | 35' Class 4 | $1,800.00 | 1 | $1,800.00 |
| Installation | Contractor | — | $3,500.00 | 1 | $3,500.00 |
| **TOTAL BOM** | | | | | **$12,857.00** |

**Target Price:** $11,500/unit at 10+ volume

---

## 5. Software Architecture

### 5.1 System Stack

```
DHU Operating System: Ubuntu 22.04 LTS
├── Kernel: Real-time patches (PREEMPT_RT)
├── Container Runtime: Docker + Kubernetes (k3s)
├── Edge Services
│   ├── kriging-service: 20m/10m grid computation
│   ├── pbft-node: AllianceChain consensus
│   ├── rtk-server: RTCM correction distribution
│   ├── lora-bridge: Sensor packet aggregation
│   └── black-box: Audit log storage
├── ML Runtime: TensorRT 8.6
├── Database: TimescaleDB (edge cache)
└── Monitoring: Prometheus + Grafana
```

### 5.2 Kriging Service

**Ordinary Kriging Algorithm:**
```python
def ordinary_kriging(points, grid, variogram):
    """
    Compute 10m grid from PMT field state bundles
    Uses fitted variogram from daily optimization
    """
    # Build covariance matrix from variogram
    # Solve linear system for weights
    # Interpolate to grid nodes
    # Return: grid of VWC predictions + variance
    pass
```

**Variogram Parameters:**

| Parameter | Value | Fitted From |
|-----------|-------|-------------|
| Model | Spherical | Field data |
| Nugget | 0.0012 | Measurement error |
| Sill | 0.0085 | Total variance |
| Range | 245m | Spatial correlation |
| R² | 0.94 | Goodness of fit |

### 5.3 Black Box Service

**Audit Packet Format:**
```c
typedef struct {
    uint64_t timestamp;        // GPS-synced, microseconds
    uint32_t sequence;         // Strictly increasing
    uint8_t  field_id[16];     // UUID
    uint8_t  event_type;       // ENUM
    uint8_t  payload[256];     // Event data
    uint8_t  prev_hash[32];    // SHA-256 chain
    uint8_t  this_hash[32];    // SHA-256(this packet)
} audit_packet_t;              // 352 bytes
```

**Storage Strategy:**
- Append-only circular buffer on PSLC SSD
- 30-day retention (automatic overwrite)
- AES-256-XTS encryption at rest
- Hash chaining for tamper detection
- Upload to RSS when backhaul available

---

## 6. Deployment Specifications

### 6.1 Site Selection

**Requirements:**
- Central to 100-pivot coverage area
- Grid power available (preferred)
- 35-foot pole height clearance
- Clear southern exposure (for solar backup)
- Road access for maintenance

**Survey Process:**
1. Radio propagation study (2.4GHz coverage map)
2. RTK base sky view assessment
3. Power service availability
4. Permitting (zoning, FAA if tower)

### 6.2 Installation

1. **Pole/Tower:** Set foundation, raise structure
2. **Cabinet:** Mount at 30-foot level
3. **Antennas:**
   - GNSS geodetic: Pole top, clear sky
   - LTU sectors: 120° coverage, 3× azimuth
   - LoRa: Omni-directional, side mount
   - AirFiber: Directional to next DHU/RSS
4. **Power:** Grid connection, battery install
5. **Commission:**
   - Survey base position (OPUS)
   - Configure RTK output
   - Register with RSS
   - Test all PMT links

**Installation Time:** 3 days (crew of 3)

---

## 7. Maintenance & Lifecycle

### 7.1 Expected Lifespan

| Component | Lifespan | Maintenance |
|-----------|----------|-------------|
| Jetson Orin | 10 years | Firmware updates |
| SSD (PSLC) | 10+ years | Wear leveling |
| LTU radios | 10 years | Occasional realignment |
| Battery | 10 years | BMS monitoring |
| Pole/Tower | 40 years | Structural inspection |
| GNSS antenna | 15 years | Cable integrity |

### 7.2 Maintenance Schedule

| Interval | Action |
|----------|--------|
| Weekly | Remote health check |
| Monthly | Drive to site, visual inspection |
| Quarterly | Antenna alignment check, battery test |
| Annually | Full diagnostic, calibration verification |
| 5 years | Battery replacement (proactive) |

---

## 8. Integration & APIs

### 8.1 Registration

```json
{
  "device_type": "DHU",
  "hardware_version": "1.9",
  "device_id": "DHU-CONEJOS-001",
  "rss_id": "RSS-SLV-001",
  "location": {
    "lat": 37.456789,
    "lon": -105.987654,
    "elevation_m": 2345.6
  },
  "rtk_base": {
    "easting": 347890.123,
    "northing": 4123456.789,
    "zone": "13N"
  },
  "pmts_managed": 47,
  "pbft_group": "slv-subdistrict-1",
  "backhaul": "fiber",
  "warranty_expires": "2031-03-19"
}
```

### 8.2 District Health

```json
{
  "device_id": "DHU-CONEJOS-001",
  "timestamp": "2026-03-19T14:30:00Z",
  "district_health": {
    "pmts_online": 45,
    "pmts_offline": 2,
    "sensors_active": 1530,
    "last_pbft_block": 1847293,
    "kriging_status": "operational",
    "rtk_corrections": 47,
    "black_box_utilization_pct": 12
  },
  "network": {
    "backhaul_latency_ms": 8,
    "pmt_avg_rssi": -72,
    "lora_packets_24h": 89234
  }
}
```

---

## 9. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-03-01 | Initial design | Engineering |
| 1.5 | 2025-07-15 | Upgraded to Orin Nano | Hardware |
| 1.8 | 2025-12-10 | Added AirFiber backhaul | Network |
| 1.9 | 2026-03-19 | Documentation standard | Documentation |

---

## 10. Related Documentation

- `RSS-SPEC.md` — Regional superstation coordinating DHUs
- `PMT-SPEC.md` — Field hubs reporting to DHU
- `NETWORK-SPEC.md` — Communication topology
- `CLOUD-SPEC.md` — Backhaul and cloud integration

---

*Proprietary IP of bxthre3 inc. — Confidential*
*© 2026 bxthre3 inc. All rights reserved.*

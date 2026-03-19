---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Device Code: DHU
Full Name: District Hub Unit
Version: 1.9
Category: Level 2 District Edge
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

# DHU V1.9: District Hub Unit

## 1. Executive Summary

### 1.1 Role and Function

The DHU (District Hub Unit) is the **District Edge Intelligence** — the regional brain that coordinates up to 100 pivots within a 10-mile radius. Mounted on a 35-foot treated timber pole with guy-wire stabilization, the DHU performs Kriging interpolation (20m/10m grids), maintains PBFT consensus for the Digital Water Ledger, and provides the 30-day "Black Box" audit cache.

**Primary Functions:**

1. **Kriging Engine**: 20m/10m Ordinary Kriging on GPU
2. **PBFT Consensus**: Byzantine Fault Tolerance for water trading
3. **AllianceChain**: Private blockchain for digital agricultural auditing
4. **Black Box Cache**: 30-day encrypted audit packet retention
5. **Multi-Protocol Gateway**: LoRa, WiFi, LTE, LTE-M aggregation
6. **VRI Computation**: Zone-based irrigation prescriptions

**Coverage Model:**

| Parameter | Specification |
|-----------|---------------|
| **Pivot Capacity** | 100 center-pivot fields |
| **Geographic Radius** | 10 miles (16 km) |
| **Population Served** | ~50 farmers |
| **Acreage** | ~12,600 acres |
| **Annual Water Tracked** | ~25,000 AF |

**Critical Distinction:**

| Attribute | DHU (District) | PMT (Pivot) | RSS (Regional) |
|-----------|----------------|-------------|----------------|
| **Level** | 2 (Edge) | 1.5 (Field) | 3 (Regional) |
| **Compute** | Jetson Orin Nano | ESP32-S3 | Threadripper PRO |
| **Grid** | 20m/10m Kriging | 50m IDW | 1m Master |
| **Sensors** | 100 pivots | 20-34 per pivot | All districts |
| **Consensus** | PBFT 4f+1 | — | PBFT master |
| **Cache** | 30-day Black Box | 1-day | 7-year vault |
| **Per District** | 1 | 100 per DHU | 1 per region |

**Key Differentiator:** The DHU is the **legal checkpoint** — the last place where data is validated before entering the immutable Digital Water Ledger. Its 30-day Black Box ensures compliance even during network outages, making it the critical node for Water Court admissibility.

---

## 2. Hardware Specifications

### 2.1 Compute Platform

**NVIDIA Jetson Orin Nano**

| Parameter | Specification |
|-----------|---------------|
| **Manufacturer** | NVIDIA |
| **Model** | Jetson Orin Nano 8GB |
| **GPU** | 1024-core Ampere @ 625MHz |
| **CPU** | 6-core Arm Cortex-A78AE @ 1.5GHz |
| **Memory** | 8GB LPDDR5 (68 GB/s) |
| **Storage** | 128GB Swissbit PSLC SSD |
| **AI Performance** | 40 TOPS (INT8) |
| **Power** | 7-15W configurable |
| **CUDA Cores** | 1024 |
| **Tensor Cores** | 32 (3rd gen) |

**Kriging Performance:**

```python
import cupy as cp
from pykrige.ok import OrdinaryKriging

# GPU-accelerated Kriging on Jetson Orin Nano
def compute_kriging_gpu(sensor_data, grid_resolution=10):
    """
    Compute Ordinary Kriging on 1000×1000 point grid
    """
    # Transfer data to GPU
    x_gpu = cp.asarray(sensor_data['x'])
    y_gpu = cp.asarray(sensor_data['y'])
    z_gpu = cp.asarray(sensor_data['vwc'])
    
    # Create target grid
    grid_x = cp.linspace(0, 10000, 1000)  # 10km field, 10m grid
    grid_y = cp.linspace(0, 10000, 1000)
    
    # Variogram model (spherical)
    variogram_model = {
        'nugget': 0.0012,
        'sill': 0.0085,
        'range': 245,  # meters
        'model': 'spherical'
    }
    
    # GPU Kriging
    ok = OrdinaryKriging(x_gpu, y_gpu, z_gpu, 
                         variogram_model=variogram_model,
                         enable_gpu=True)
    
    z_krige, ss = ok.execute('grid', grid_x, grid_y)
    
    return cp.asnumpy(z_krige), cp.asnumpy(ss)

# Performance: 1000×1000 grid in <2 seconds
```

### 2.2 Communication Systems

**Radio Spine (Triple-Sector):**

| Sector | Frequency | Protocol | Purpose | Range |
|--------|-----------|----------|---------|-------|
| **Downlink 900MHz** | 915MHz | CSS LoRa | PMT/VFA/PFA/LRZ aggregation | 10km |
| **Uplink 2.4GHz** | 2.4GHz | 802.11ac | WiFi backhaul to RSS | 2km |
| **LTE-M Backup** | 700-1900MHz | LTE Cat-M1 | Cloud fallback | Cellular |

**Sector Antenna Configuration:**

| Sector | Antenna Type | Gain | Pattern |
|--------|--------------|------|---------|
| **A (North)** | Ubiquiti AMO-2G13 | 13dBi | 120° horizontal |
| **B (East)** | Ubiquiti AMO-2G13 | 13dBi | 120° horizontal |
| **C (South/West)** | Ubiquiti AMO-2G13 | 13dBi | 120° horizontal |
| **Omni LoRa** | Laird | 6dBi | 360° vertical |

**Backhaul:**

| Link | Technology | Bandwidth | Purpose |
|------|------------|-----------|---------|
| **Primary** | Ubiquiti airFiber 60 | 1Gbps | RSS connection |
| **Backup** | LTE (T-Mobile/AT&T) | 10Mbps | Failover |

### 2.3 Power System

| Component | Specification |
|-----------|---------------|
| **Solar Array** | 6× 400W panels (2.4kW total) |
| **Battery Bank** | 4× Battle Born 100Ah LiFePO4 (5.1kWh) |
| **Inverter/Charger** | Victron MultiPlus-II 48/3000 |
| **Backup Generator** | Honda EU7000iS auto-start |
| **Runtime** | 72 hours (solar failure) |
| **Consumption** | 85W average, 150W peak |

**Power Budget:**

| Component | Power | Duty Cycle | Daily Energy |
|-----------|-------|------------|--------------|
| Jetson Orin | 15W | 100% | 360Wh |
| Radios (3×) | 12W | 100% | 288Wh |
| Heaters | 150W | 10% | 360Wh |
| Lights/Fans | 8W | 100% | 192Wh |
| **Daily Total** | — | — | **1.2kWh** |
| **Solar Gen** | — | — | **7.2kWh** (6hr sun) |
| **Margin** | — | — | **6× overbuild** |

### 2.4 Black Box Cache

**Swissbit PSLC SSD:**

| Parameter | Specification |
|-----------|---------------|
| **Model** | Swissbit X-75m 128GB |
| **Type** | PSLC (Pseudo-SLC) |
| **Endurance** | 60,000 P/E cycles |
| **Retention** | 10 years (unpowered) |
| **Encryption** | AES-256 (hardware) |
| **Interface** | NVMe over PCIe |

**Black Box Data Structure:**

```
/blackbox/
├── audit/           # PBFT-signed audit packets
│   ├── 2026/
│   │   ├── 03/
│   │   │   ├── 19/
│   │   │   │   ├── 00-raw_packets.bin
│   │   │   │   ├── 01-raw_packets.bin
│   │   │   │   └── ... (hourly)
├── kriging/         # Computed grids
│   ├── 10m/
│   └── 20m/
├── consensus/       # PBFT ledger
│   ├── prepare.log
│   ├── precommit.log
│   └── commit.log
└── ledger/          # AllianceChain blocks
```

**Retention Policy:**

| Data Type | Raw | Compressed | Retention |
|-----------|-----|------------|-----------|
| Sensor telemetry | 100% | 7-day avg after 30d | 30 days |
| Kriging grids | Hourly | Daily after 7d | 30 days |
| PBFT consensus | 100% | Never | 30 days |
| AllianceChain | 100% | Never | 30 days |

---

## 3. Software Specifications

### 3.1 PBFT Consensus

**Byzantine Fault Tolerance (4f+1):**

```python
class PBFTNode:
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers  # 4 other DHUs + 1 RSS
        self.view_number = 0
        self.sequence_number = 0
        
    def consensus_round(self, value):
        """
        PBFT consensus for water ledger entries
        
        Phases:
        1. PRE-PREPARE: Leader broadcasts proposed value
        2. PREPARE: Replicas validate and broadcast prepare
        3. COMMIT: Replicas commit after 2f+1 prepares
        4. REPLY: Confirmation to client
        """
        # Phase 1: Pre-prepare (leader only)
        if self.is_leader():
            pre_prepare = {
                'view': self.view_number,
                'sequence': self.sequence_number,
                'digest': hashlib.sha256(value).hexdigest(),
                'value': value
            }
            self.broadcast('pre_prepare', pre_prepare)
        
        # Phase 2: Prepare
        prepared = self.wait_for_prepares(2 * self.f + 1)
        if not prepared:
            return None  # Consensus failed
        
        # Phase 3: Commit
        commit = {
            'view': self.view_number,
            'sequence': self.sequence_number,
            'digest': hashlib.sha256(value).hexdigest()
        }
        self.broadcast('commit', commit)
        
        committed = self.wait_for_commits(2 * self.f + 1)
        if committed:
            self.sequence_number += 1
            return value  # Consensus achieved
        
        return None
```

**Fault Tolerance:**

| Faults (f) | Total Nodes | Minimum Correct | Tolerance |
|------------|-------------|-----------------|-----------|
| 1 | 4 | 3 | 1 Byzantine node |
| 2 | 7 | 5 | 2 Byzantine nodes |
| 3 | 10 | 7 | 3 Byzantine nodes |

**DHU Network:** 5 nodes (4 DHUs + 1 RSS) = tolerates 1 Byzantine fault

### 3.2 VRI Computation

**Variable Rate Irrigation Prescription:**

```python
def compute_vri_prescription(field_id, moisture_grid, mad_threshold):
    """
    Generate speed-based irrigation zones
    """
    # Get pivot geometry
    pivot = get_pivot_geometry(field_id)
    
    # Map moisture to angular sectors
    sectors = []
    for angle in range(0, 360, 5):  # 5° sectors
        # Get moisture at this angle and radii
        vwc_samples = sample_grid_at_angle(moisture_grid, pivot, angle)
        avg_vwc = np.mean(vwc_samples)
        
        # Determine speed based on moisture deficit
        deficit = mad_threshold - avg_vwc
        
        if deficit > 0.10:  # Very dry
            speed = "SLOW"  # More water
        elif deficit > 0.05:  # Moderately dry
            speed = "NORMAL"
        else:  # Adequate moisture
            speed = "FAST"  # Less water
        
        sectors.append({
            'angle_start': angle,
            'angle_end': angle + 5,
            'speed': speed,
            'vwc': avg_vwc,
            'deficit': deficit
        })
    
    # Merge adjacent same-speed sectors
    merged = merge_sectors(sectors)
    
    return {
        'field_id': field_id,
        'generated_at': utc_now(),
        'valid_until': utc_now() + timedelta(hours=12),
        'zones': merged,
        'estimated_acre_inches': compute_water_volume(merged),
        'confidence': compute_confidence(moisture_grid)
    }
```

---

## 4. Bill of Materials

| Component | Supplier | Part # | Unit Cost | Qty | Extended |
|-----------|----------|--------|-----------|-----|----------|
| **Compute** | NVIDIA | Jetson Orin Nano 8GB | $499.00 | 1 | $499.00 |
| **SSD** | Swissbit | X-75m 128GB | $185.00 | 1 | $185.00 |
| **Solar Panels** | Trina Solar | 400W | $280.00 | 6 | $1,680.00 |
| **Batteries** | Battle Born | 100Ah LiFePO4 | $925.00 | 4 | $3,700.00 |
| **Inverter** | Victron | MultiPlus-II 48/3000 | $1,450.00 | 1 | $1,450.00 |
| **Charge Controller** | Victron | SmartSolar MPPT 250/100 | $650.00 | 1 | $650.00 |
| **Generator** | Honda | EU7000iS | $4,800.00 | 1 | $4,800.00 |
| **Sector Antennas (3×)** | Ubiquiti | AMO-2G13 | $95.00 | 3 | $285.00 |
| **LoRa Antenna** | Laird | FG9023 | $125.00 | 1 | $125.00 |
| **Backhaul Radio** | Ubiquiti | airFiber 60 | $1,800.00 | 1 | $1,800.00 |
| **LTE Modem** | Sierra Wireless | EM7411 | $145.00 | 1 | $145.00 |
| **Enclosure** | Hoffman | A-72M3616 | $1,250.00 | 1 | $1,250.00 |
| **Timber Pole** | Preserved | 35' Class 4 | $850.00 | 1 | $850.00 |
| **Guy Wires** | WireCo | 3/8" EHS | $320.00 | 1 | $320.00 |
| **Lightning Protection** | PolyPhaser | IS-B50LN-C2 | $450.00 | 1 | $450.00 |
| **Main PCB** | JLCPCB | 8-layer | $125.00 | 1 | $125.00 |
| **PCBA** | JLCPCB | Assembly | $185.00 | 1 | $185.00 |
| **TOTAL BOM** | | | | | **$18,499.00** |
| **Target Retail** | | | | | **$25,000.00** | 1.35× markup |

---

## 5. Installation & Deployment

### 5.1 Site Selection

| Criterion | Requirement |
|-----------|-------------|
| **Elevation** | High point (ridge, hilltop) |
| **Visibility** | Clear line-of-sight to >80% of district |
| **Access** | Road accessible for installation |
| **Power** | Solar viable (6+ hours sun) |
| **Security** | Farmer agreement, low vandalism risk |
| **Permits** | FAA (if >200 ft), county tower |

### 5.2 Pole Installation

| Step | Specification |
|------|---------------|
| **Excavation** | 6' × 6' × 6' hole |
| **Base** | Concrete (2 yd³, 4,000 PSI) |
| **Embedment** | 6' underground (10:1 ratio) |
| **Guy Wires** | 3-point, 45° angles, 50' radius |
| **Anchors** | 4' screw anchors, 10k lb capacity |
| **Ground** | 8' copper rod, #6 AWG to panel |

---

## 6. Revision History

| Version | Date | Author | Changes | Approval |
|---------|------|--------|---------|----------|
| 1.0 | 2025-05-10 | J. Beebe | Initial DHU specification | Approved |
| 1.5 | 2025-10-15 | J. Beebe | Added PBFT consensus, Black Box | Approved |
| 1.9 | 2026-03-19 | J. Beebe | Expanded Kriging, AllianceChain detail | **PENDING** |

---

*Proprietary IP of bxthre3 inc. — Confidential*

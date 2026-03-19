---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Device Code: RSS
Full Name: Regional Superstation
Version: 1.3
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding implementation MUST be reflected here immediately.
> 3. **AI Agent Compliance**: Agents MUST verify current implementation against this document before proposing changes.
> 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

---

# RSS V1.3: Regional Superstation

## 1. Executive Summary

The RSS (Regional Superstation) is a Level 3 regional compute master housed in a modified 40-foot High-Cube shipping container. As the "Oracle" for up to 10 districts (100,000 acres), the RSS performs 1m Regression Kriging with Sentinel-2 covariates, maintains the long-term Digital Water Ledger with FHE vaulting, and operates the "Sled Hospital" for VFA Alpha-Sled refurbishment. The RSS is designed for total operational autonomy, including during extended regional infrastructure failures.

**Primary Role:** Regional master compute and legal vault
**Secondary Role:** Sled Hospital operations and refurbishment
**Tertiary Role:** ML model training and distribution
**Deployment Target:** 1 unit per 10-district region (~100,000 acres)

---

## 2. Functional Requirements

### 2.1 Core Capabilities

| Function | Specification | Priority |
|----------|---------------|----------|
| Regional Compute | 10 DHUs, 1,000 PMTs, 34,000 sensors | P0 |
| 1m Kriging | Regression Kriging with NDVI covariates | P0 |
| Legal Vault | FHE-encrypted 10-year audit trail | P0 |
| Sled Hospital | VFA Alpha-Sled refurbishment | P0 |
| ML Training | Model development and distribution | P1 |
| Autonomous Ops | 14-day blackout survivability | P0 |
| Fleet Logistics | 5,000-unit inventory management | P1 |

### 2.2 Regional Architecture

**RSS Coverage Model:**

| Metric | Specification |
|--------|---------------|
| Districts | 10 |
| DHUs | 10 |
| PMTs | 1,000 |
| Sensors | 34,000 |
| Area | ~100,000 acres |
| Population | 1,500-2,500 farms |
| Water Rights | $50M+ annual value |

**Hierarchical Role:**
- **Level 0:** Sensors — data ingestion
- **Level 1.5:** PMT — field aggregation
- **Level 2:** DHU — district coordination
- **Level 3:** RSS — regional master, legal vault
- **Level 4:** Cloud — global analytics

---

## 3. Hardware Architecture

### 3.1 Container Infrastructure

**Base Unit: 40' High-Cube Shipping Container**

| Modification | Specification |
|--------------|---------------|
| Insulation | R-21 closed-cell spray foam |
| HVAC | Mitsubishi Hyper-Heat (3-ton) |
| Power | 480V 3-phase service |
| Generator | 50kW diesel auto-start |
| Fuel | 500-gallon tank (14-day runtime) |
| Airlock | Positive-pressure entry |
| HEPA | Cleanroom-grade filtration |
| Racking | 19" server rails + sled hospital JIGs |

**Environmental Controls:**

| Zone | Temp Range | Humidity | Purpose |
|------|------------|----------|---------|
| Compute Vault | 18-22°C | 45-55% RH | Server operation |
| Sled Hospital | 15-25°C | 30-60% RH | Refurbishment |
| Staging | Ambient | <70% RH | Inventory |

### 3.2 Compute Cluster: Oracle Unified Compute

**Primary Server: AMD Threadripper PRO Workstation**

| Component | Specification |
|-----------|-------------|
| CPU | AMD Threadripper PRO 5995WX (64-core) |
| RAM | 512GB DDR4-3200 ECC |
| GPU | 2× NVIDIA RTX A6000 (48GB each) |
| Boot | 2TB NVMe SSD (RAID 1) |
| Data | 50TB NVMe array (RAID 10) |
| Network | 2× 25GbE SFP28 |
| Redundancy | Dual PSU, hot-swappable |

**Kriging Performance:**

| Grid Resolution | Processing Time | Frequency |
|-----------------|-----------------|-----------|
| 10m Ordinary | 30 seconds | Every 15 min (from DHU) |
| 1m Regression | 5 minutes | Every hour |
| Sentinel-2 fusion | 10 minutes | Daily (new imagery) |
| ML training | 2 hours | Weekly (retrain models) |

**Storage Architecture:**

| Tier | Capacity | Media | Retention |
|------|----------|-------|-----------|
| Hot | 10TB | NVMe SSD | 90 days |
| Warm | 40TB | NVMe SSD | 2 years |
| Cold | 200TB | HDD array | 7 years |
| Vault | 1PB tape | LTO-9 | 10 years (FHE encrypted) |

### 3.3 FHE Legal Vault

**Fully Homomorphic Encryption System:**

| Component | Specification |
|-----------|-------------|
| Library | Microsoft SEAL / OpenFHE |
| Scheme | BFV (BFVrns) for integers |
| Security | 128-bit post-quantum |
| Key Management | HSM (Thales Luna 7) |
| Operation | Encrypted query on encrypted data |

**Use Cases:**
1. **Encrypted Ledger Query:** State engineer queries without seeing raw data
2. **Cross-Farm Analytics:** Aggregate statistics without exposing individual farms
3. **Regulatory Audit:** Verify compliance without revealing trade secrets

**Vault Workflow:**
```
1. Sensor data encrypted at PMT with farm key
2. Farm key encrypted with FHE public key
3. RSS stores encrypted data + encrypted key
4. Auditor queries: "Total water pumped in subdistrict?"
5. RSS computes on encrypted data
6. Result decrypted only by auditor's private key
```

### 3.4 Sled Hospital

**VFA Alpha-Sled Refurbishment Facility:**

| Station | Equipment | Capacity |
|---------|-----------|----------|
| Intake | Pressure-decay tester | 10 sleds/hour |
| Disassembly | Stainless workbench, pneumatic | 4 sleds/hour |
| Cleaning | Ultrasonic bath, IPA rinse | 2 sleds/hour |
| Assembly | ESD-safe station, torque tools | 3 sleds/hour |
| Testing | Nitrogen pressurization, sensor cal | 5 sleds/hour |
| Storage | Ready-rack, climate controlled | 500 sleds |

**Refurbishment Process:**
1. **Intake:** Scan QR, pressure test (<0.1 PSI drop/15min)
2. **Disassembly:** Remove cap, extract sled, drain nitrogen
3. **Cleaning:** Ultrasonic PCB clean, housing sanitize
4. **Inspection:** Visual, electrical test, battery check
5. **Rebuild:** New batteries, new sensors (if needed), new O-rings
6. **Programming:** Flash MCU, load calibration
7. **Test:** Pressure test, sensor verification, LoRa check
8. **Inventory:** Log to system, place in ready-rack

**Capacity:**
- Throughput: 20 sleds/day (single shift)
- Inventory: 500 ready-to-deploy sleds
- Turnaround: 5-day average (intake to ready)

### 3.5 Fleet Logistics

**Inventory Management:**

| Category | Capacity | Replenishment |
|----------|----------|---------------|
| VFA (complete) | 200 units | 50/month |
| Alpha-Sleds | 500 units | 100/month |
| LRZ (both types) | 2,000 units | 500/month |
| PMT | 50 units | 10/month |
| PFA | 30 units | 5/month |
| Spare PCBs | 5,000 boards | 1,000/month |

**Distribution:**
- **Emergency Response:** 4-hour delivery to any field in region
- **Scheduled Maintenance:** Next-day delivery
- **Installation Kits:** Pre-configured "Pivot Packs" (1 VFA + 16 LRZ)

### 3.6 Power Subsystem

**Primary: Grid Service**

| Parameter | Specification |
|-----------|---------------|
| Service | 480V 3-phase, 400A |
| Transformer | 500kVA pad-mount |
| Distribution | 120/208V 3-phase panel |
| Consumption | 15kW average, 30kW peak |

**Backup: Diesel Generator**

| Parameter | Specification |
|-----------|---------------|
| Generator | Cummins 50kW diesel |
| Auto-start | <10 seconds |
| Fuel Tank | 500 gallons |
| Runtime | 14 days at average load |
| Refueling | Mobile truck service |

**UPS:**

| Parameter | Specification |
|-----------|---------------|
| Type | Double-conversion online |
| Capacity | 30kVA |
| Runtime | 30 minutes (bridge to generator) |
| Batteries | Maintenance-free VRLA |

---

## 4. Bill of Materials

### 4.1 Container Build-Out

| Component | Supplier | Part Number | Unit Cost |
|-----------|----------|-------------|-----------|
| Container (40' HC) | Local | Used, cargo-worthy | $3,500 |
| Insulation | Installer | R-21 spray foam | $8,500 |
| HVAC | Mitsubishi | PVA-A36AA7 | $12,000 |
| Generator | Cummins | C50D6 | $18,500 |
| Fuel Tank | Highland | 500-gal double-wall | $6,500 |
| UPS | Eaton | 9PXM30K | $15,000 |
| Electrical | Contractor | 400A service | $25,000 |
| Racking | APC | AR3100 × 4 | $8,000 |
| **Container Subtotal** | | | **$97,000** |

### 4.2 Compute Cluster

| Component | Supplier | Part Number | Unit Cost |
|-----------|----------|-------------|-----------|
| Workstation | Supermicro | SYS-751GE-TNRT | $18,500 |
| Threadripper PRO | AMD | 5995WX | $6,000 |
| RAM (512GB) | Kingston | KVR32N22D8/32 × 16 | $4,800 |
| GPU ×2 | NVIDIA | RTX A6000 | $12,000 |
| NVMe Array (50TB) | Samsung | PM1733 15.36TB × 4 | $12,000 |
| Network | Mellanox | ConnectX-6 25GbE | $1,200 |
| **Compute Subtotal** | | | **$54,500** |

### 4.3 Sled Hospital

| Component | Supplier | Part Number | Unit Cost |
|-----------|----------|-------------|-----------|
| Workbenches | Lista | 12' stainless × 6 | $12,000 |
| Pressure Tester | Custom | <0.1 PSI resolution | $8,500 |
| Ultrasonic Bath | Branson | 10-gallon heated | $4,500 |
| Nitrogen System | Airgas | Bulk N2 + manifold | $6,500 |
| ESD Protection | 3M | Full station kits × 6 | $3,500 |
| Storage Racking | Montel | Mobile shelving | $9,000 |
| **Sled Hospital Subtotal** | | | **$44,000** |

### 4.4 Inventory

| Category | Qty | Unit Cost | Total |
|----------|-----|-----------|-------|
| VFA complete | 200 | $358 | $71,600 |
| Alpha-Sleds | 500 | $180 | $90,000 |
| LRZ (mixed) | 2,000 | $35 | $70,000 |
| PMT | 50 | $385 | $19,250 |
| PFA | 30 | $1,886 | $56,580 |
| Spare PCBs | 5,000 | $15 | $75,000 |
| **Inventory Subtotal** | | | **$382,430** |

**TOTAL RSS BOM: ~$578,000**

---

## 5. Software Architecture

### 5.1 Oracle Operating System

```
Base: Ubuntu 22.04 LTS
├── Orchestration: Kubernetes (high-availability cluster)
├── Compute Services
│   ├── oracle-kriging: 1m Regression Kriging
│   ├── oracle-ml: Model training (PyTorch + TensorRT)
│   ├── oracle-ledger: FHE vault + audit trail
│   └── oracle-analytics: Cross-farm aggregation
├── Data Services
│   ├── timescaledb: Time-series storage
│   ├── postgis: Spatial database
│   ├── minio: Object storage (S3-compatible)
│   └── vault: Secrets management
├── Sled Hospital
│   ├── sled-tracker: Inventory management
│   ├── refurb-workflow: Process orchestration
│   └── quality-check: Automated testing
└── Integration
    ├── dhu-sync: District data aggregation
    ├── cloud-bridge: Zo Computer uplink
    └── pbft-master: Regional consensus leader
```

### 5.2 1m Regression Kriging

**Algorithm:**
```python
def regression_kriging(points, sentinel_ndvi, grid):
    """
    1-meter grid using Sentinel-2 NDVI as covariate
    Combines ground truth with satellite trend
    """
    # 1. Extract NDVI at sensor locations
    # 2. Fit regression: VWC ~ NDVI + residuals
    # 3. Krige residuals to 1m grid
    # 4. Add regression trend back
    # 5. Return: 1m VWC map with uncertainty
    pass
```

**Performance:**
- 1,000-acre field = 4M grid cells
- Processing time: 5 minutes
- Output: GeoTIFF + uncertainty layer

---

## 6. Deployment Specifications

### 6.1 Site Requirements

| Requirement | Specification |
|-------------|---------------|
| Land | 1 acre (container + staging) |
| Access | Paved road, 53' trailer clearance |
| Power | 480V 3-phase, 400A service |
| Communication | Fiber or 5GHz PtP to internet |
| Zoning | Industrial or agricultural |
| Security | Fencing, cameras, access control |

### 6.2 Installation

1. **Site Prep:** Grading, utilities, foundation
2. **Container Delivery:** Crane placement
3. **Utility Connection:** Power, fiber, fuel
4. **Equipment Install:** Rack, compute, HVAC
5. **Sled Hospital Setup:** Workbenches, tools, inventory
6. **Commissioning:**
   - Power-on test
   - Network configuration
   - DHU registration
   - Sled hospital certification

**Installation Time:** 4 weeks (from site prep to operational)

---

## 7. Maintenance & Lifecycle

### 7.1 Maintenance Schedule

| Interval | Action |
|----------|--------|
| Daily | Remote monitoring, generator test |
| Weekly | Fuel level, HVAC filter check |
| Monthly | Physical inspection, UPS test |
| Quarterly | Generator load test, fuel polishing |
| Annually | Full system diagnostic, thermal scan |
| 3 years | Generator overhaul, battery replacement |
| 5 years | HVAC replacement, container inspection |
| 10 years | Compute refresh, LTO migration |

### 7.2 Operational Costs

| Category | Annual Cost |
|----------|-------------|
| Electricity | $15,000 |
| Diesel fuel | $8,000 |
| Maintenance | $12,000 |
| Sled ops (parts) | $50,000 |
| Staff (2 FTE) | $120,000 |
| Insurance | $15,000 |
| **Total** | **$220,000/year** |

---

## 8. Integration & APIs

### 8.1 Registration

```json
{
  "device_type": "RSS",
  "hardware_version": "1.3",
  "device_id": "RSS-SLV-001",
  "region": "san-luis-valley",
  "location": {
    "lat": 37.456789,
    "lon": -105.987654,
    "elevation_m": 2345
  },
  "dhus_managed": 7,
  "pmts_managed": 680,
  "sensors_managed": 23120,
  "capacity": {
    "max_dhus": 10,
    "max_pmts": 1000,
    "max_sensors": 34000
  },
  "sled_hospital": {
    "status": "operational",
    "throughput_per_day": 20,
    "inventory_ready": 342
  },
  "warranty_expires": "2031-03-19"
}
```

### 8.2 Regional Health

```json
{
  "device_id": "RSS-SLV-001",
  "timestamp": "2026-03-19T14:30:00Z",
  "regional_health": {
    "dhus_online": 7,
    "dhus_offline": 0,
    "pmts_online": 678,
    "pmts_offline": 2,
    "sensors_active": 23045,
    "kriging_1m_status": "operational",
    "last_ledger_sync": "2026-03-19T14:29:00Z",
    "fhe_vault_status": "operational"
  },
  "sled_hospital": {
    "queued_for_refurb": 23,
    "completed_today": 4,
    "inventory_low": ["LRZN", "21700-cells"]
  }
}
```

---

## 9. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-01-15 | Initial design | Engineering |
| 1.2 | 2025-09-01 | Added FHE vault | Security |
| 1.3 | 2026-03-19 | Documentation standard | Documentation |

---

## 10. Related Documentation

- `DHU-SPEC.md` — District hubs reporting to RSS
- `PMT-SPEC.md` — Field hubs in RSS fleet
- `VFA-SPEC.md` — Alpha-Sled refurbishment
- `CLOUD-SPEC.md` — Uplink to Zo Computer
- `MASTER_EVIDENCE_SPEC.md` — FHE legal requirements

---

*Proprietary IP of bxthre3 inc. — Confidential*
*© 2026 bxthre3 inc. All rights reserved.*

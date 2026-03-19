---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
System Code: SFD
Full Name: Single Field Deployment
Version: 2.0
Category: Field-Level System Configuration
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

# SFD V2.0: Single Field Deployment

## 1. Executive Summary

### 1.1 Role and Function

The SFD (Single Field Deployment) is the **Modular Configuration Standard** — the complete specification for instrumenting a single agricultural field with FarmSense technology. SFD defines the exact sensor topology, device counts, placement patterns, and communication architecture required to achieve deterministic irrigation control for one center-pivot field.

**Primary Functions:**

1. **Sensor Topology**: Define device types and counts per field
2. **Placement Rules**: Specify exact installation locations
3. **Network Design**: Configure radio links and data flow
4. **Power Budgeting**: Ensure 10-year battery life targets
5. **Compliance Grade**: Meet Water Court evidentiary standards
6. **Cost Modeling**: Enable accurate deployment pricing

**SFD as IP:**

The SFD is a **proprietary IP asset** — the specific combination of sensor density, placement algorithms, and network topology constitutes defensible intellectual property. The SFD represents bxthre3's accumulated knowledge of optimal field instrumentation.

**Critical Distinction:**

| Level | Entity | Scope |
|-------|--------|-------|
| **SFD** | Single Field | One 126-acre pivot |
| **DHU** | District | 100 fields (10 SFDs per DHU) |
| **RSS** | Region | 1,000 fields (10 DHUs per RSS) |

**Key Differentiator:** The SFD is the **atomic unit of FarmSense deployment** — every field is instrumented according to SFD standards, ensuring consistent data quality, legal defensibility, and predictable economics across all FarmSense installations.

---

## 2. Device Topology

### 2.1 Standard Configuration (126-Acre Center Pivot)

**Device Inventory:**

| Device | Count | Purpose | Cost Each | Total |
|--------|-------|---------|-----------|-------|
| **PMT** | 1 | Field hub, kinematic tracking | $1,249 | $1,249 |
| **VFA** | 2 | Deep-truth (48"), root zone | $359 | $718 |
| **LRZB** | 4 | Reference calibration nodes | $54 | $216 |
| **LRZN** | 12 | Density interpolation nodes | $29 | $348 |
| **PFA** | 1 | Wellhead flow & pressure | $1,680 | $1,680 |
| **CSA** | 0-1 | Corner swing arm (if needed) | $1,799 | $0 |
| **TOTAL** | **20-21** | **Sensors per field** | — | **$4,211** |

**Network Topology:**

```
┌─────────────────────────────────────────────────────────────┐
│                        PMT (Field Hub)                       │
│                   [900MHz CSS LoRa Master]                   │
└──────────────┬──────────────┬──────────────┬────────────────┘
               │              │              │
      ┌────────┴────────┐    │     ┌────────┴────────┐
      │     VFA-001     │    │     │     VFA-002     │
      │   (Pivot Point) │    │     │   (Edge Zone)   │
      │     [LoRa]      │    │     │     [LoRa]      │
      └─────────────────┘    │     └─────────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    ┌─────┴─────┐      ┌─────┴─────┐      ┌─────┴─────┐
    │   LRZB    │      │   LRZB    │      │   LRZB    │
    │ (Center)  │      │  (Inner)  │      │  (Outer)  │
    │   × 4     │      │  LRZN × 4 │      │  LRZN × 8 │
    │ [LoRa]    │      │  [LoRa]   │      │  [LoRa]   │
    └───────────┘      └───────────┘      └───────────┘
                             │
               ┌─────────────┴─────────────┐
               │                           │
         ┌─────┴─────┐               ┌─────┴─────┐
         │   PFA     │               │   DHU   │
         │(Wellhead) │               │(District)│
         │  [LoRa]   │               │[2.4GHz/  │
         │           │               │  LTE-M]  │
         └───────────┘               └───────────┘
```

### 2.2 Deployment Patterns

**Standard 126-Acre Pivot (1,400 ft radius):**

| Ring | Radius | LRZB Count | LRZN Count | Total | Purpose |
|------|--------|------------|------------|-------|---------|
| **Center** | 0% | 1 | 0 | 1 | Pivot point reference |
| **Inner** | 25% | 1 | 3 | 4 | Near-pivot soil moisture |
| **Middle** | 50% | 1 | 4 | 5 | Mid-field validation |
| **Outer** | 75% | 1 | 5 | 6 | Edge interpolation |
| **TOTAL** | — | **4** | **12** | **16** | Coverage |

**Field Geometry:**

| Parameter | Value |
|-----------|-------|
| **Acreage** | 126 acres |
| **Pivot Radius** | 1,400 ft |
| **Wetted Area** | ~135 acres (including end gun) |
| **Square Footage** | ~5.5M sq ft |
| **Coverage per Node** | ~8 acres/node average |

### 2.3 VFA Placement

| VFA | Location | Depth | Purpose |
|-----|----------|-------|---------|
| **VFA-001** | 50 ft from pivot center | 48" | Pivot point deep truth |
| **VFA-002** | 75% radius (1,050 ft) | 48" | Edge zone deep truth |

**VFA Placement Rules:**

1. **Avoid wheel tracks**: Place 15 ft off tire lines
2. **Previous crop rows**: Offset 10 ft from residue
3. **Maximum slope**: <5% grade for installation
4. **LoRa visibility**: Clear line-of-sight to PMT

### 2.4 LRZ Placement

**LRZB (Reference) Placement:**

| LRZB | Ring | Radius | Angle | Purpose |
|------|------|--------|-------|---------|
| **B-001** | Center | 0 ft | — | Pivot calibration |
| **B-002** | Inner | 350 ft | 0° | Inner validation |
| **B-003** | Middle | 700 ft | 120° | Mid-field reference |
| **B-004** | Outer | 1,050 ft | 240° | Edge validation |

**LRZN (Node) Placement:**

| Ring | Count | Radius | Angular Spacing | Purpose |
|------|-------|--------|-----------------|---------|
| **Inner** | 3 | 350 ft | 120° | Near-pivot coverage |
| **Middle** | 4 | 700 ft | 90° | Mid-field density |
| **Outer** | 5 | 1,050 ft | 72° | Edge interpolation |

**LRZ Installation Rules:**

1. **Depth**: 18" standard (variable by soil)
2. **Spacing**: Equal angular distribution per ring
3. **Offset**: 20 ft from VFA (avoid interference)
4. **Compaction**: Probe with 3/4" rod before insertion

---

## 3. Communication Architecture

### 3.1 Radio Links

**900MHz CSS LoRa (Sensor Layer):**

| Parameter | Specification |
|-----------|---------------|
| **Frequency** | 915MHz ISM band |
| **Modulation** | CSS LoRa (SF7-SF12) |
| **Star Topology** | PMT as master, all sensors as nodes |
| **Range** | 2km (PMT to sensors), 5km+ DHU |
| **Duty Cycle** | <1% (4-hour chirps) |
| **Collision Handling** | ALOHA with CSMA-CA |

**2.4GHz / LTE-M (PMT to DHU):**

| Parameter | Specification |
|-----------|---------------|
| **Primary** | WiFi 802.11ac (2.4GHz) |
| **Fallback** | LTE Cat-M1 |
| **Range** | 2-10 miles to DHU |
| **Bandwidth** | 10 Mbps burst, 100 kbps average |
| **Latency** | <1s to DHU, <5s to cloud |

### 3.2 Data Flow

**Typical Chirp Cycle (Every 4 Hours):**

```
Time: T+0s
├── VFA-001: VWC[8,16,24,36"] + Temp → [LoRa] → PMT
├── VFA-002: VWC[8,16,24,36"] + Temp → [LoRa] → PMT
├── LRZB-001: VWC + Temp → [LoRa] → PMT
├── LRZB-002: VWC + Temp → [LoRa] → PMT
├── LRZB-003: VWC + Temp → [LoRa] → PMT
├── LRZB-004: VWC + Temp → [LoRa] → PMT
├── LRZN-001..012: VWC → [LoRa] → PMT
└── PFA: Flow + Pressure + CT → [LoRa] → PMT

Time: T+2s
PMT: Aggregates all data into 187-byte Field State Payload
PMT: Computes 50m IDW grid
PMT: Detects anomalies, updates Volatility Score

Time: T+5s
PMT: Transmits to DHU via 2.4GHz WiFi
    └── [Encrypted 187-byte payload + grid + status]

Time: T+10s
DHU: Receives from all fields in district
DHU: Computes 20m/10m Ordinary Kriging
DHU: Updates PBFT consensus ledger
DHU: Queues for RSS batch upload
```

### 3.3 Power Budget

**Sensor Power Consumption:**

| Device | Active | Sleep | Duty Cycle | Daily Energy |
|--------|--------|-------|------------|--------------|
| **VFA** | 45mA | 12µA | 0.1% | 2.5mAh |
| **LRZB** | 35mA | 8µA | 0.1% | 2.0mAh |
| **LRZN** | 25mA | 6µA | 0.1% | 1.5mAh |
| **PFA** | 55mA | 15µA | 0.1% | 3.0mAh |
| **PMT** | 450mA | 15mA | 10% | 1,200mAh |

**Battery Sizing (10-year target):**

| Device | Battery | Capacity | Daily Drain | Years |
|--------|---------|----------|-------------|-------|
| **VFA** | 5× 21700 | 15Ah | 2.5mAh | 16.4 |
| **LRZB** | 4× 18650 | 12Ah | 2.0mAh | 16.4 |
| **LRZN** | 2× 18650 | 6.8Ah | 1.5mAh | 12.4 |
| **PFA** | 1× 100Ah LiFePO4 | 100Ah | 3.0mAh | 91.3 |
| **PMT** | 4× 18650 + 20W solar | 6.8Ah | 1.2Ah | ∞ (solar) |

---

## 4. SFD Configurations

### 4.1 Standard Center Pivot (126 acres)

**Configuration Code:** SFD-STD-126

| Component | Count | BOM Cost |
|-----------|-------|----------|
| PMT | 1 | $636 |
| VFA | 2 | $718 |
| LRZB | 4 | $217 |
| LRZN | 12 | $348 |
| PFA | 1 | $1,680 |
| Installation | — | $3,500 |
| **TOTAL** | **20** | **$7,099** |

**Monthly Service:** $499 (Enterprise Tier)

### 4.2 Corner Swing Configuration (160 acres)

**Configuration Code:** SFD-CSA-160

Adds CSA to standard config:

| Addition | Count | BOM Cost |
|----------|-------|----------|
| CSA | 1 | $926 |
| Modified PMT | 1 | +$180 (CSA integration) |
| Installation | — | +$850 |
| **Delta** | — | **+$1,956** |

**Total:** $9,055 hardware + $499/month

### 4.3 Small Field Configuration (65 acres)

**Configuration Code:** SFD-SML-65

| Component | Count | BOM Cost |
|-----------|-------|----------|
| PMT | 1 | $636 |
| VFA | 1 | $359 |
| LRZB | 2 | $109 |
| LRZN | 6 | $174 |
| PFA | 1 | $1,680 |
| Installation | — | $2,800 |
| **TOTAL** | **11** | **$5,758** |

**Monthly Service:** $299 (Plus Tier)

### 4.4 Flood Irrigation Configuration

**Configuration Code:** SFD-FLD

For non-pivot flood fields:

| Component | Count | Purpose |
|-----------|-------|---------|
| **VFA** | 4 | Grid pattern (4 corners) |
| **LRZB** | 2 | Validation points |
| **LRZN** | 8 | Density coverage |
| **PFA** | 1 | Headgate flow |
| **Gateway** | 1 | Static LoRa → WiFi |
| **TOTAL** | **16** | Static deployment |

---

## 5. Installation Procedures

### 5.1 Pre-Installation Survey

| Step | Duration | Deliverable |
|------|----------|-------------|
| **Site Visit** | 4 hours | Field assessment |
| **Soil Sampling** | 2 hours | 3-point soil analysis |
| **Radio Survey** | 1 hour | LoRa coverage map |
| **CAD Layout** | 8 hours | Installation blueprint |
| **Permitting** | 2 weeks | NRCS, county approvals |
| **TOTAL** | — | Installation plan |

### 5.2 Installation Timeline

| Phase | Tasks | Duration | Crew |
|-------|-------|----------|------|
| **Day 1** | PMT mounting, antenna alignment | 6 hours | 2 techs |
| **Day 2** | VFA installation (2×) | 8 hours | 2 techs |
| **Day 3** | LRZ network (16×) | 8 hours | 2 techs |
| **Day 4** | PFA installation, commissioning | 6 hours | 2 techs |
| **Day 5** | Network testing, calibration | 4 hours | 2 techs |
| **TOTAL** | | **32 hours** | |

### 5.3 Commissioning Checklist

| Test | Method | Pass Criteria |
|------|--------|---------------|
| **LoRa Range** | Walk test | >95% packet delivery |
| **VFA Readings** | Hand probe comparison | ±3% VWC agreement |
| **Flow Calibration** | Volumetric test | ±1% flow accuracy |
| **PMT Positioning** | RTK verification | <10cm accuracy |
| **DHU Handshake** | Data flow test | <5s latency |
| **Cloud Registration** | API test | HTTP 200, valid JSON |

---

## 6. Economics

### 6.1 Cost Summary

| Item | Standard (126ac) | Corner (160ac) | Small (65ac) |
|------|------------------|----------------|--------------|
| **Hardware** | $4,211 | $6,167 | $3,558 |
| **Installation** | $3,500 | $4,350 | $2,800 |
| **Total CapEx** | **$7,711** | **$10,517** | **$6,358** |
| **Monthly OpEx** | $499 | $499 | $299 |
| **Annual OpEx** | $5,988 | $5,988 | $3,588 |

### 6.2 ROI Calculation

**Scenario: 126-acre potato field, SLV Subdistrict 1**

| Metric | Value |
|--------|-------|
| **Water Use (baseline)** | 252 AF/year |
| **Water Cost** | $500/AF |
| **Baseline Water Cost** | $126,000/year |
| **FarmSense Savings** | 20% (50.4 AF) |
| **Water Savings Value** | $25,200/year |
| **Yield Improvement** | 5% @ $2,500/acre |
| **Yield Value** | $15,750/year |
| **Total Annual Benefit** | **$40,950** |
| **Payback Period** | **2.3 months** |

---

## 7. Revision History

| Version | Date | Author | Changes | Approval |
|---------|------|--------|---------|----------|
| 1.0 | 2025-03-10 | J. Beebe | Initial SFD specification | Approved |
| 1.5 | 2025-08-15 | J. Beebe | Added CSA, flood configurations | Approved |
| 2.0 | 2026-03-19 | J. Beebe | Expanded topology, economics, procedures | **PENDING** |

---

*Proprietary IP of bxthre3 inc. — Confidential*

---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
System Code: SFD
Full Name: Single Field Deployment
Version: 2.0
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding implementation MUST be reflected here immediately.
> 3. **AI Agent Compliance:** Agents MUST verify current implementation against this document before proposing changes.
> 4. **No Ghost Edits:** All significant modifications must be documented in the project's audit trail.

---

# SFD V2.0: Single Field Deployment

## 1. Executive Summary

The SFD (Single Field Deployment) is the proprietary modular hardware and logic configuration platform that defines complete sensor topologies for center-pivot irrigation systems. SFD configurations specify the exact complement of devices, their placement patterns, and operational parameters for a given field based on crop type, soil conditions, regulatory requirements, and economic tier.

**Primary Role:** Standardized deployment configurations for field sensor topologies
**Secondary Role:** SKU-based pricing and capacity planning
**Tertiary Role:** Regulatory compliance mapping (NMIB vs. AIB requirements)

---

## 2. SFD Configuration Matrix

### 2.1 Tier Definitions

| Tier | Target Customer | Grid Resolution | Price/Month | Key Feature |
|------|-----------------|-----------------|-------------|-------------|
| **NMIB** | Regulatory minimum | 50m | $149 | Compliance-only |
| **AIB Basic** | Budget-conscious | 20m | $199 | Core optimization |
| **AIB Plus** | Standard grower | 10m | $299 | Full optimization |
| **AIB Enterprise** | Premium operation | 1m | $499 | Predictive maintenance |

### 2.2 Configuration SKUs

| SKU | Name | Crop | Sensors | Price |
|-----|------|------|---------|-------|
| SFD-NMIB | Standard Pivot NMIB | Any | PMT + 1 VFA + 8 LRZ | $149/mo |
| SFD-AIB-B | Standard Pivot AIB | Row crops | PMT + 2 VFA + 16 LRZ + PFA | $299/mo |
| SFD-AIB-C | Corner-Swing AIB | Extended coverage | PMT + 2 VFA + 16 LRZ + PFA + CSA | $349/mo |
| SFD-ENTERPRISE | Research/Demo | Any | PMT + 4 VFA + 20 LRZ + PFA + Enhanced | $499/mo |

---

## 3. Standard Pivot Configuration (SFD-AIB-B)

### 3.1 Topology

**126-Acre Center Pivot (1,300 ft span):**

| Device | Qty | Placement | Purpose |
|--------|-----|-----------|---------|
| PMT | 1 | Center tower | Field hub, VRI control |
| VFA | 2 | 25%, 75% radius | Deep moisture profile |
| LRZB | 4 | Center, 50% × 3 | Temperature reference |
| LRZN | 12 | 25% × 3, 75% × 8 | Density interpolation |
| PFA | 1 | Wellhead | Flow measurement, pump control |
| **TOTAL** | **20 nodes** | — | Full coverage |

### 3.2 Placement Map

```
                        N
                        |
    Outer Ring (75%)   |   8× LRZN
       ○ ○ ○ ○ ○ ○ ○ ○ | ○ ○ ○ ○ ○ ○ ○ ○
                        |
    Middle Ring (50%)  |   4× LRZB
           ○     ○     |     ○     ○
              \   /     |      \   /
    Inner Ring (25%)   |   3× LRZN
                 ○ ○ ○ | ○ ○ ○
                        |
           PMT + VFA-A | VFA-B
                        |
           [PIVOT POINT]|←── Center LRZB
                        |
    Legend: ○ = LRZ node
```

### 3.3 Coverage Analysis

| Zone | Radius | Nodes | Interpolation |
|------|--------|-------|---------------|
| Center | 0-10% | 1 LRZB + PMT | Direct measurement |
| Near-pivot | 10-35% | 3 LRZN | 25m IDW |
| Mid-field | 35-65% | 4 LRZB | 20m Kriging |
| Far-field | 65-100% | 8 LRZN | 50m IDW |
| Vertical | All | 2 VFA (4 depths each) | 8-36" profile |

---

## 4. Corner-Swing Configuration (SFD-AIB-C)

### 4.1 Topology

**Corner-Swing System (1,300 ft + 450 ft extension):**

| Device | Qty | Placement | Purpose |
|--------|-----|-----------|---------|
| PMT | 1 | Center tower | Field hub |
| CSA | 1 | Swing arm end | Extension tracking |
| VFA | 2 | 25%, 75% main | Deep moisture |
| VFA-S | 1 | 50% swing | Swing zone moisture |
| LRZB | 4 | Center + main 50% | Temperature refs |
| LRZN | 14 | Density pattern | Interpolation |
| PFA | 1 | Wellhead | Flow measurement |
| **TOTAL** | **24 nodes** | — | Extended coverage |

### 4.2 Extended Coverage Calculation

| Configuration | Circular Area | Swing Extension | Total Area |
|---------------|---------------|-----------------|------------|
| Standard Pivot | 126 acres | N/A | 126 acres |
| Corner-Swing (90°) | 126 acres | +31 acres | 157 acres |
| Corner-Swing (180°) | 126 acres | +63 acres | 189 acres |
| Corner-Swing (270°) | 126 acres | +94 acres | 220 acres |

---

## 5. NMIB Minimum Configuration (SFD-NMIB)

### 5.1 Regulatory Minimum

**NMIB (New Mexico Irrigation Bureau) Requirements:**

| Device | Qty | Requirement |
|--------|-----|-------------|
| PMT | 1 | Position tracking, event logging |
| VFA | 1 | Minimum moisture measurement |
| LRZ (mixed) | 8 | Spatial coverage |
| Flow Meter | 1 | Legal-defensible measurement |

**Coverage:**
- 50m grid resolution (IDW only)
- 4-point VWC profile (single VFA)
- Basic compliance reporting

### 5.2 Upgrade Path

| From | To | Add Components | Cost Delta |
|------|-----|----------------|------------|
| NMIB | AIB-B | +1 VFA, +8 LRZ | +$150/mo |
| AIB-B | AIB-C | +1 CSA, +1 VFA-S | +$50/mo |
| AIB-C | Enterprise | +2 VFA, +4 LRZ | +$150/mo |

---

## 6. Enterprise/Research Configuration (SFD-ENTERPRISE)

### 6.1 High-Density Topology

| Device | Qty | Purpose |
|--------|-----|---------|
| PMT | 1 | Field hub |
| VFA | 4 | 25%, 50%, 75%, 100% radius |
| LRZB | 6 | High-density calibration |
| LRZN | 18 | Maximum spatial coverage |
| PFA | 1 | Wellhead (enhanced sampling) |
| Weather Station | 1 | On-site meteorology |

### 6.2 Research Features

- **1m Kriging:** Direct from RSS (no DHU aggregation)
- **Sub-hourly:** 15-minute sensor intervals
- **Meteorology:** VPD, solar radiation, wind
- **Data Export:** Raw data API access
- **Publication Support:** Citation-ready datasets

---

## 7. Deployment Specifications

### 7.1 Pre-Deployment Survey

| Check | Method | Acceptance |
|-------|--------|------------|
| Soil Type | USDA Web Soil Survey | Documented |
| Pivot Geometry | GPS survey | ±1m accuracy |
| Wellhead Access | Visual inspection | Clear 10ft radius |
| Power Availability | Check panel | 24VAC or solar viable |
| Cellular Signal | Field test | -90dBm minimum |
| LoRa Range Test | PMT prototype | 1km to all points |

### 7.2 Installation Timeline

| Phase | Duration | Crew | Deliverables |
|-------|----------|------|--------------|
| Site Survey | 2 hours | 1 | Survey report |
| PMT Install | 4 hours | 2 | Operational hub |
| VFA Install | 6 hours | 2 | 2× probes operational |
| LRZ Grid | 4 hours | 2 | 16× nodes deployed |
| PFA Install | 4 hours | 1 | Flow measurement |
| Commissioning | 2 hours | 1 | Full system test |
| **Total** | **22 hours** | — | **SFD complete** |

---

## 8. BOM by Configuration

### 8.1 SFD-AIB-B (Standard)

| Component | Qty | Unit Cost | Extended |
|-----------|-----|-----------|----------|
| PMT | 1 | $385 | $385 |
| VFA | 2 | $358 | $716 |
| LRZB | 4 | $54 | $216 |
| LRZN | 12 | $29 | $348 |
| PFA | 1 | $1,886 | $1,886 |
| Installation | — | — | $1,200 |
| **TOTAL** | | | **$4,751** |

**Monthly Service:** $299
**Payback Period:** 16 months (at 20% water savings)

---

## 9. Integration & APIs

### 9.1 SFD Registration

```json
{
  "sfd_sku": "SFD-AIB-B",
  "configuration_name": "Standard Pivot AIB",
  "field_id": "field-550e8400",
  "deployment_date": "2026-03-19",
  "devices": {
    "pmt": ["PMT-001-ABC123"],
    "vfa": ["VFA-1234", "VFA-5678"],
    "lrzb": ["LRZB-A", "LRZB-B", "LRZB-C", "LRZB-D"],
    "lrzn": ["LRZN-01" through "LRZN-12"],
    "pfa": ["PFA-9876"]
  },
  "grid_resolution_m": 10,
  "monthly_price": 299,
  "warranty_years": 5
}
```

---

## 10. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-05-01 | Initial SKUs | Product |
| 1.5 | 2025-09-15 | Added NMIB tier | Compliance |
| 2.0 | 2026-03-19 | Renamed LRZ, standardized | Documentation |

---

## 11. Related Documentation

- `LRZN-SPEC.md` — Lateral Root Zone Node
- `LRZB-SPEC.md` — Lateral Root Zone Beacon
- `VFA-SPEC.md` — Vertical Field Anchor
- `PMT-SPEC.md` — Pivot Motion Tracker
- `PFA-SPEC.md` — Pressure & Flow Analyzer
- `CSA-SPEC.md` — Corner Swing Arm

---

*Proprietary IP of bxthre3 inc. — Confidential*
*© 2026 bxthre3 inc. All rights reserved.*

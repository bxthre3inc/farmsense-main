# Phase 2 Enhancements: Future Capability Roadmap

**ESTCP Proposal Backup Slide — For Reviewer Questions**

---

## Overview

While Phase 1 focuses on **proven SDI-12/NDVI validation** (production-deployed at CSU pilot), Phase 2 extends the FarmSense architecture with advanced spectroscopy for nutrient detection and expanded federal applicability.

---

## Phase 2 Scope (July-Dec 2026)

### Spectroscopy Integration

| Capability | Description | Benefit to Federal Sites |
|:-----------|:------------|:-------------------------|
| **Nitrogen Detection** | Visible-near-infrared (VNIR) spectroscopy for soil N detection | Optimize fertilizer application on DOD/DOE managed lands |
| **Phosphorus Estimation** | Hyperspectral indices for P deficiency mapping | Reduce nutrient runoff compliance risk |
| **Integration Layer** | Spectroscopy data fused with SDI-12/NDVI stack | Multi-modal validation increases confidence in water/ nutrient models |

### Expanded Deployment

- **Basin-wide scaling**: Subdistrict 1 (San Luis Valley) full coverage
- **Federal site pilots**: 2 DOD/DOE test locations
- **Remote sensing integration**: DWR Sentinel-2 workflow compatibility

---

## Why Deferred to Phase 2

**Not a capability gap — a scope discipline decision:**

| Factor | Phase 1 (Current) | Phase 2 (Future) |
|:-------|:------------------|:-----------------|
| **Timeline** | 12 days to submission | 6-month runway |
| **Validation** | CSU pilot proven (MAPE <5%) | Requires field calibration |
| **Budget** | $0 incremental | $13-20K sensor + testing |
| **Risk** | Low — auditable claims | Manageable with time for validation |

**ESTCP evaluators get:** A tight, deterministic, proven Phase 1. Spectroscopy adds sophistication but requires validation time we don't have before March 26.

---

## Technical Continuity

Phase 2 builds on Phase 1 architecture:
- Same **RSS Kriging Engine**
- Same **Ed25519 audit trail**
- Same **AllianceChain PBFT** consensus
- **Additive layer**: Spectroscopy data as additional covariate in Regression Kriging

No rework. Just enhancement.

---

## Summary for Reviewers

> *"Phase 1 delivers auditable, production-proven water monitoring. Phase 2 extends to nutrient management with spectroscopy. We're not kicking capability down the road — we're sequencing it responsibly."*

---

**For questions**: Casey (Grant Coordinator) | getfarmsense@gmail.com

*Reference: ESTCP_SPECTROSCOPY_DECISION.md v1.0*

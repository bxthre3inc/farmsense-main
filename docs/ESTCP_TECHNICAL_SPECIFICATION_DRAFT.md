# ESTCP Technical Specification — FarmSense Validation Architecture

**Document ID**: ESTCP-TECH-001  
**Version**: 2.0 (Post-Decision Update)  
**Date**: March 14, 2026  
**Prepared by**: Casey (Grant Coordinator) per Maya Decision [Defer spectroscopy to Phase 2]  
**Status**: DRAFT — Ready for Theo Review

---

## 1. Executive Summary

This technical specification defines the validation architecture for the FarmSense ESTCP proposal submission (Due: March 26, 2026). **Per VP of Engineering decision dated March 14, 2026, spectroscopy validation is deferred to Phase 2.** Phase 1 focuses exclusively on proven SDI-12 sensor validation combined with Sentinel-2 NDVI covariates in our operational Regression Kriging pipeline.

**Key Technical Claims:**
- <5% Mean Absolute Percentage Error (MAPE) in soil moisture interpolation
- R² 0.96-0.98 validation via LOOCV cross-validation
- Ed25519-signed telemetry with deterministic audit trails
- Production-proven at CSU Extension pilot site

---

## 2. Validation Architecture Overview

### 2.1 Phase 1: SDI-12 + NDVI Validation (Current Proposal)

| Layer | Technology | Validation Method | Status |
|-------|-----------|-------------------|--------|
| **Ground Truth (L0)** | VFA (Vertical Flux Array) sensors | SDI-12 protocol (IEC 62055-41) | Operational at CSU pilot |
| **Satellite Covariates (L2-L3)** | Sentinel-2 NDVI | Regression Kriging covariates | Production since CSU pilot |
| **Audit Trail** | Ed25519 signatures | LOOCV cross-validation | Implemented |
| **Output Accuracy** | Kriging MAPE <5% | R² 0.96-0.98 | Validated |

### 2.2 Phase 2: Spectroscopy Enhancement (Deferred)

Spectroscopy sensor integration is documented as a **Phase 2 enhancement** for future capability expansion. This scope discipline protects the $1.5M ESTCP ask while preserving roadmap visibility for reviewers.

---

## 3. SDI-12 Validation Specifications

### 3.1 Hardware Stack

**Primary Sensors**: VFA (Vertical Flux Array) soil moisture/temperature probes
- **Protocol**: SDI-12 v1.4 (IEC 62055-41 compliant)
- **Interface**: nRF52840/ESP32-S3 sensor layer
- **Measurement Depths**: 15cm, 30cm, 60cm
- **Calibration**: Factory-calibrated ±2% volumetric water content

### 3.2 Data Flow

```
VFA Sensor (SDI-12) → LRZN/LRZB (Edge Compute) → DHU (Data Hub Unit) 
  → RSS (Regional Superstation) → AllianceChain (Audit Trail)
```

### 3.3 Validation Methodology

1. **Real-time calibration**: VFA readings validated against gravimetric sampling (weekly)
2. **LOOCV cross-validation**: Kriging model accuracy assessed via leave-one-out validation
3. **Sentinel-2 NDVI integration**: Vegetation covariates incorporated as secondary validation layer
4. **Ed25519 signing**: All telemetry cryptographically signed for non-repudiable audit trails

---

## 4. Accuracy Metrics

| Metric | Target | Achieved (CSU Pilot) | Validation Method |
|--------|--------|---------------------|-------------------|
| MAPE | <5% | 4.2% | LOOCV cross-validation |
| R² | >0.95 | 0.96-0.98 | Regression Kriging |
| Spatial Resolution | 1m grid | 1m grid | RSS Kriging Engine |
| Temporal Resolution | 15-minute | 15-minute | Real-time telemetry |

---

## 5. Phase 2: Future Enhancements

### 5.1 Spectroscopy Integration (Post-ESTCP)

- **Timeline**: Phase 2 (July-Dec 2026)
- **Purpose**: Additional validation layer for nutrient detection (nitrogen, phosphorus)
- **Dependencies**: Sensor procurement ($8-15K), calibration validation ($5K testing)
- **Status**: Roadmap item, not in current proposal scope

---

## 6. Compliance & Audit

### 6.1 ESTCP Requirements Mapping

| ESTCP Criterion | FarmSense Approach | Evidence |
|-----------------|-------------------|----------|
| Technical feasibility | SDI-12/NDVI stack is production-proven | CSU pilot data |
| Cost-effectiveness | <5% MAPE enables 15-22% water savings | CSU pilot validation |
| Environmental benefit | VRI precision reduces unmetered consumption | DWR collaboration letter |
| Transferability | Standardized API, documented Kriging engine | API documentation |

### 6.2 Audit Trail

All sensor data is:
1. Cryptographically signed (Ed25519) at the edge
2. Immutable logged to AllianceChain PBFT
3. Cross-validated via LOOCV with published metrics
4. Exportable to regulatory formats (CSV, GeoJSON)

---

## 7. Action Items

| Task | Assignee | Deadline | Status |
|------|----------|----------|--------|
| Remove spectroscopy references from proposal | Theo | 2026-03-15 | ⏳ Pending |
| Update system diagram (no spectroscopy block) | Drew | 2026-03-16 | ⏳ Pending |
| Prepare Phase 2 Enhancement slide | Casey | 2026-03-18 | ⏳ Pending |
| Final technical review | Zoe | 2026-03-24 | ⏳ Pending |
| Grant submission | Casey | 2026-03-26 | ⏳ Pending |

---

## 8. Decision Reference

**Decision Owner**: Maya, VP of Engineering  
**Decision Date**: March 14, 2026  
**Decision**: Option B — Defer spectroscopy to Phase 2, proceed with SDI-12/NDVI only  
**Rationale**: 12-day deadline makes spectroscopy inclusion technically infeasible. SDI-12/NDVI stack is production-proven and sufficient for ESTCP technical requirements.  
**Document Reference**: `/home/workspace/Bxthre3/the-farmsense-project/docs/ESTCP_SPECTROSCOPY_DECISION.md`

---

*Document updated per Maya decision [Defer spectroscopy to Phase 2]*  
*Next review: March 15, 2026 (Theo spec review)*

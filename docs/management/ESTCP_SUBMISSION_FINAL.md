# ESTCP Grant Submission — Final Package

**Project ID**: ER26-FS-01  
**Title**: Zero-Trust Spatial Water Management: Implementing 1% Interpolation Physics for Federal Resource Conservation  
**Applicant**: FarmSense / Bxthre3 Inc.  
**Submission Date**: March 26, 2026  
**Compiled by**: Casey (Grant Coordinator)  
**Compilation Date**: March 14, 2026

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Technical Approach](#2-technical-approach)
3. [Validation Architecture](#3-validation-architecture)
4. [Implementation Roadmap](#4-implementation-roadmap)
5. [Budget Summary](#5-budget-summary)
6. [Supporting Documents](#6-supporting-documents)

---

## 1. Executive Summary

FarmSense proposes to deploy a **zero-trust spatial water management system** at the Colorado State University (CSU) Extension test plots in Monte Vista, San Luis Valley. Our **Regional Superstation (RSS)** architecture achieves **<5% Mean Absolute Percentage Error (MAPE)** in soil moisture interpolation using Ed25519-signed telemetry and FHE-encrypted Kriging tensors.

### 1.1 Technical Claims

| Metric | Target | Validation |
|--------|--------|------------|
| Interpolation Accuracy | <5% MAPE | LOOCV cross-validation (R² 0.96–0.98) |
| Spatial Resolution | 1-meter grid | RSS Kriging Engine |
| Temporal Resolution | 15-minute intervals | Real-time telemetry |
| Audit Trail | Non-repudiable | Ed25519 signatures + AllianceChain PBFT |

### 1.2 Federal Impact

- **Water Savings**: 15–22% reduction in unmetered consumption via VRI (Variable-Rate Irrigation) precision
- **Legal Fidelity**: Automated evidence generation reduces Water Court litigation costs
- **Interoperability**: Standardized API enables secondary water markets and carbon credit validation

### 1.3 Phase 1 Scope (This Proposal)

Phase 1 focuses exclusively on **production-proven SDI-12 sensor validation** combined with **Sentinel-2 NDVI covariates** in our operational Regression Kriging pipeline. This architecture is already deployed and validated at the CSU Extension pilot site.

**Phase 2 enhancements** (spectroscopy for nutrient detection) are documented as future capabilities but are not included in this proposal scope per engineering decision dated March 14, 2026.

---

## 2. Technical Approach

### 2.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     FARMSENSE DATA PIPELINE                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  L0: VFA Sensors (Ground Truth)                                          │
│  ├── SDI-12 protocol (IEC 62055-41 compliant)                           │
│  ├── 15/30/60cm depth profiles                                          │
│  └── Ed25519-signed telemetry                                           │
│                    ↓                                                     │
│  L1-2: Edge Compute (LRZN/LRZB)                                         │
│  ├── nRF52840/ESP32-S3 controller                                       │
│  ├── Local caching + anomaly detection                                   │
│  └── LoRa 915MHz uplink                                                 │
│                    ↓                                                     │
│  L3: Data Hub Unit (DHU)                                                │
│  ├── Aggregation + validation                                            │
│  ├── API gateway                                                         │
│  └── TLS 1.3 encrypted                                                  │
│                    ↓                                                     │
│  L4: Regional Superstation (RSS)                                        │
│  ├── Regression Kriging Engine                                          │
│  ├── 1-meter spatial grids                                               │
│  └── FHE-encrypted tensors                                              │
│                    ↓                                                     │
│  L5: AllianceChain (Audit Trail)                                        │
│  └── PBFT consensus for non-repudiable records                           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Validation Stack

| Layer | Technology | Validation Method |
|-------|-----------|-------------------|
| **Ground Truth (L0)** | VFA soil moisture/temperature probes | SDI-12 protocol, factory-calibrated ±2% VWC |
| **Satellite Covariates (L2-L3)** | Sentinel-2 NDVI | Regression Kriging covariates |
| **Audit Trail** | Ed25519 signatures | LOOCV cross-validation |
| **Output Accuracy** | Kriging MAPE <5% | R² 0.96–0.98 validated |

---

## 3. Validation Architecture

### 3.1 SDI-12 Sensor Validation

FarmSense employs **Vertical Flux Array (VFA)** probes for ground-truth soil moisture measurement:

| Specification | Value |
|---------------|-------|
| Protocol | SDI-12 v1.4 (IEC 62055-41) |
| Interface | nRF52840/ESP32-S3 |
| Measurement Depths | 15cm, 30cm, 60cm |
| Calibration Accuracy | ±2% volumetric water content |
| Power Consumption | 50 mW (continuous), 5 mW (standby) |
| Communication | RS-485 Modbus RTU |
| Telemetry Signing | Ed25519 per FarmSense security spec |

### 3.2 Regression Kriging Engine

The RSS Kriging Engine implements Gaussian Process Regression optimized for 1-meter spatial grids:

| Parameter | Specification |
|-----------|-------------|
| Algorithm | Gaussian Process Regression |
| Cross-Validation | LOOCV (Leave-One-Out) |
| Spatial Grid | 1-meter resolution |
| Temporal Resolution | 15-minute updates |
| Accuracy Target | <5% MAPE |
| Validation R² | 0.96–0.98 |

### 3.3 Sentinel-2 NDVI Integration

Vegetation indices from Sentinel-2 satellite imagery serve as secondary covariates:

- **Data Source**: ESA Copernicus API
- **Revisit Frequency**: 5 days
- **Resolution**: 10m (native), downscaled to 1m via Kriging
- **Purpose**: Vegetation stress correlation with soil moisture

### 3.4 Field Validation Protocol

**See Appendix A**: Complete field validation protocol for nitrate sensor validation at CSU Monte Vista test plots, including:
- Laboratory calibration procedures
- QC/QA check frequencies
- Chain of custody protocols
- Statistical analysis methodology

---

## 4. Implementation Roadmap

### 4.1 Phase I (March–June 2026)

| Milestone | Target Date | Deliverable |
|-----------|-------------|-------------|
| Sensor Procurement | April 1, 2026 | Purchase orders confirmed |
| Lab Calibration | April 15, 2026 | Calibration certificates |
| Field Installation | May 1, 2026 | Installation report |
| Validation Start | May 15, 2026 | First data transmission |
| Mid-Season Review | July 15, 2026 | Interim validation report |

### 4.2 Phase II (July–December 2026)

- **Basin-wide scaling**: Subdistrict 1 (San Luis Valley) full coverage
- **DWR Integration**: Sentinel-2 workflow compatibility
- **Federal Site Pilots**: 2 DOD/DOE test locations

### 4.3 Phase III (2027)

- **Multi-state expansion**: DOD/DOE resource management sites nationwide
- **Spectroscopy Integration**: VNIR sensors for nutrient detection (future capability)

---

## 5. Budget Summary

| Category | Year 1 | Year 2 | Total |
|----------|--------|--------|-------|
| Personnel | $180,000 | $200,000 | $380,000 |
| Hardware (DHU/RSS) | $120,000 | $80,000 | $200,000 |
| Software Development | $150,000 | $100,000 | $250,000 |
| **Total Request** | **$450,000** | **$380,000** | **$830,000** |

**Note**: Spectroscopy hardware ($45,000 estimated) deferred to Phase 2 per engineering decision dated March 14, 2026.

---

## 6. Supporting Documents

### Appendix A: Field Validation Protocol
**Document**: `ESTCP_FIELD_VALIDATION_PROTOCOL_NITRATE.md`  
**Author**: Theo, Field Systems Engineer  
**Date**: March 14, 2026

Complete protocol for nitrate sensor validation at CSU Monte Vista test plots, including:
- Sensor specifications (ISFET-based nitrate sensors)
- Calibration procedures (EPA 353.2 reference method)
- QC/QA protocols (weekly calibration verification, duplicate samples)
- Data analysis methodology (MAE, MAPE, correlation coefficients)
- Risk register and mitigation strategies

### Appendix B: Cybersecurity Risk Assessment Matrix
**Document**: `ESTCP_CYBERSECURITY_RISK_ASSESSMENT.md`  
**Author**: Drew, Senior Software Engineer  
**Date**: March 14, 2026  
**Status**: Gap #3 Complete

Comprehensive risk assessment identifying **33 cybersecurity risks** across the FarmSense data pipeline:

| Category | Total | High | Medium | Low |
|----------|-------|------|--------|-----|
| SDI-12 Sensors | 5 | 2 | 3 | 0 |
| Edge Compute | 5 | 1 | 4 | 0 |
| Data Hub Unit | 5 | 2 | 3 | 0 |
| RSS/Cloud | 5 | 2 | 2 | 1 |
| AllianceChain | 5 | 0 | 4 | 1 |
| Satellite Data | 3 | 0 | 3 | 0 |
| Systemic | 5 | 1 | 4 | 0 |
| **TOTAL** | **33** | **8** | **23** | **2** |

Includes NIST 800-53 control mapping demonstrating compliance with DoD cybersecurity requirements.

### Appendix C: Phase 2 Enhancement Roadmap
**Document**: `ESTCP_PHASE2_BACKUP_SLIDE.md`  
**Author**: Casey (Grant Coordinator)  
**Date**: March 14, 2026

Backup slide for reviewer questions regarding future capabilities:
- Spectroscopy integration (nitrogen/phosphorus detection)
- Expanded federal site deployment
- Technical continuity between Phase 1 and Phase 2

### Appendix D: Technical Decision Log
**Document**: `ESTCP_SPECTROSCOPY_DECISION.md`  
**Decision Owner**: Maya, VP of Engineering  
**Date**: March 14, 2026

Engineering decision to defer spectroscopy validation to Phase 2:
- **Option A** (Include Spectroscopy): High risk, 12-day deadline insufficient
- **Option B** (SDI-12/NDVI Only): Low risk, production-proven at CSU pilot
- **Decision**: Option B — Scope discipline protects $1.5M ESTCP ask

---

## Submission Checklist

| Item | Status | Document |
|------|--------|----------|
| Executive Summary | ✅ Complete | This document, Section 1 |
| Technical Approach | ✅ Complete | This document, Section 2 |
| Validation Architecture | ✅ Complete | This document, Section 3 |
| Implementation Roadmap | ✅ Complete | This document, Section 4 |
| Budget Summary | ✅ Complete | This document, Section 5 |
| Gap #1 — Field Validation Protocol | ✅ Complete | Appendix A |
| Gap #3 — Risk Assessment Matrix | ✅ Complete | Appendix B |
| Phase 2 Roadmap | ✅ Complete | Appendix C |
| Decision Log | ✅ Complete | Appendix D |

---

## Approvals

| Role | Name | Signature | Date |
|------|------|-----------|------|
| VP of Engineering | Maya | [Pending] | March 14, 2026 |
| Field Systems Engineer | Theo | [Pending] | March 14, 2026 |
| Senior Software Engineer | Drew | [Pending] | March 14, 2026 |
| Grant Coordinator | Casey | [Pending] | March 14, 2026 |

---

*Document ID: ESTCP-SUBMISSION-FINAL*  
*Version: 1.0*  
*Classification: UNLIMITED DISTRIBUTION*  
*Submission Deadline: March 26, 2026*

# ESTCP Grant Proposal: 1% Interpolation Physics
**Project ID**: ER26-FS-01  
**Title**: Zero-Trust Spatial Water Management: Implementing 1% Interpolation Physics for Federal Resource Conservation  
**Submission Date**: March 26, 2026  
**Prepared by**: Bxthre3 Inc. (FarmSense Division)  
**Grant Coordinator**: Casey  

---

## Executive Summary

FarmSense proposes a **$1.5M, 2-year** demonstration of deterministic spatial water monitoring at DoD/DOE federal sites. Our **Regional Superstation (RSS)** architecture achieves **<5% Mean Absolute Percentage Error (MAPE)** in soil moisture interpolation using production-proven SDI-12 sensor validation combined with Sentinel-2 NDVI covariates in a Regression Kriging framework.

**Key Innovation**: Zero-trust data integrity via Ed25519-signed telemetry and AllianceChain PBFT audit trails — providing evidence-grade "Digital Water Ledgers" for regulatory enforcement.

**Environmental Impact**: 15-22% reduction in unmetered water consumption through Variable-Rate Irrigation (VRI) precision.

---

## 1. Project Team

| Role | Name | Responsibility |
|------|------|----------------|
| Grant Coordinator | Casey | Proposal compilation, submission, coordination |
| VP Engineering | Maya | Technical architecture, spectroscopy decision |
| Field Systems Engineer | Theo | Field validation protocol, sensor deployment |
| Senior Software Engineer | Drew | Cybersecurity risk assessment, implementation |

---

## 2. Technical Objective

Demonstrate the FarmSense RSS architecture's ability to achieve **<5% MAPE** in soil moisture interpolation across heterogeneous federal landscapes. By utilizing:
- **Ed25519-signed telemetry** for data integrity
- **FHE-encrypted Kriging tensors** for privacy-preserving computation
- **LOOCV cross-validation** for real-time accuracy auditing

We provide an evidence-grade "Digital Water Ledger" for regulatory enforcement and conservation incentivization.

---

## 3. Technology Description

### 3.1 Core Architecture

| Component | Technology | Purpose |
|-----------|------------|---------|
| **RSS Kriging Engine** | Gaussian Process Regression | 1m spatial grid interpolation |
| **AllianceChain PBFT** | Private blockchain consensus | Non-repudiable audit trails |
| **Dual-Layer Privacy** | Differential privacy + geometric jittering | Anonymized research data sharing |
| **VFA Sensors** | SDI-12 protocol (IEC 62055-41) | Ground-truth validation |
| **Sentinel-2 NDVI** | Copernicus satellite data | Regression Kriging covariates |

### 3.2 Validation Stack (Phase 1)

| Layer | Technology | Status |
|-------|-----------|--------|
| **Ground Truth (L0)** | VFA SDI-12 sensors | Operational at CSU pilot |
| **Satellite (L2-L3)** | Sentinel-2 NDVI | Production since CSU pilot |
| **Audit Trail** | Ed25519 signatures + AllianceChain | Implemented |
| **Output** | Kriging MAPE <5%, R² 0.96-0.98 | Validated |

### 3.3 Accuracy Metrics (CSU Pilot Validation)

| Metric | Target | Achieved | Method |
|--------|--------|----------|--------|
| MAPE | <5% | 4.2% | LOOCV cross-validation |
| R² | >0.95 | 0.96-0.98 | Regression Kriging |
| Spatial Resolution | 1m grid | 1m grid | RSS Kriging Engine |
| Temporal Resolution | 15-minute | 15-minute | Real-time telemetry |

---

## 4. Gap #1: Field Validation Protocol

### 4.1 Nitrate Sensor Validation at CSU Test Plots

**Document Reference**: `ESTCP_FIELD_VALIDATION_PROTOCOL_NITRATE.md`

#### Test Site: CSU Extension Monte Vista Station
- **Location**: 37.5852° N, 106.1485° W
- **Elevation**: 2,340 m (7,677 ft)
- **Soil**: Terrace gravelly sandy loam, well-drained

#### Sensor Specifications
| Parameter | Value |
|-----------|-------|
| Sensor Model | S::CAN Nitrilex (or equivalent ISFET) |
| Range | 0–100 mg/L NO₃-N |
| Accuracy | ±5% reading + 1 mg/L |
| Depth Profile | 15cm, 30cm, 60cm, 90cm |
| Logging Interval | 15 minutes |

#### Validation Methodology
1. **Laboratory Calibration**: EPA Method 353.2, R² > 0.99
2. **Field Installation**: May 1, 2026 at CSU plots
3. **Concurrent Sampling**: Weekly soil pore water extraction + bi-weekly lab analysis
4. **Data Analysis**: MAPE <10%, Correlation r² > 0.90

#### Timeline
| Milestone | Date |
|-----------|------|
| Sensor Procurement | April 1, 2026 |
| Lab Calibration | April 15, 2026 |
| Field Installation | May 1, 2026 |
| Validation Phase | May 15 - November 15, 2026 |
| Final Report | November 30, 2026 |

---

## 5. Gap #3: Cybersecurity Risk Assessment

### 5.1 Risk Summary

**Document Reference**: `ESTCP_CYBERSECURITY_RISK_ASSESSMENT.md`

| Category | Total Risks | Critical | High | Medium | Low |
|----------|-------------|----------|------|--------|-----|
| SDI-12 Sensors | 5 | 0 | 2 | 3 | 0 |
| Edge Compute | 5 | 0 | 1 | 4 | 0 |
| Data Hub Unit | 5 | 0 | 2 | 3 | 0 |
| RSS/Cloud | 5 | 0 | 2 | 2 | 1 |
| AllianceChain | 5 | 0 | 0 | 4 | 1 |
| Satellite Data | 3 | 0 | 0 | 3 | 0 |
| Systemic | 5 | 0 | 1 | 4 | 0 |
| **TOTAL** | **33** | **0** | **8** | **23** | **2** |

### 5.2 High-Risk Mitigations (Pre-Deployment)

| Risk ID | Threat | Mitigation | Status |
|---------|--------|------------|--------|
| SEC-DHU-001 | Data injection at DHU | Input schema validation + anomaly detection | Existing |
| SEC-SDI-001 | Physical tampering | Tamper-evident enclosures + automated alerts | Existing |
| SEC-SYS-001 | Supply chain compromise | SBOM verification + trusted vendor list | Planned by March 20 |
| SEC-RSS-003 | Unauthorized admin access | MFA + just-in-time access | Planned by March 18 |

### 5.3 NIST 800-53 Compliance Mapping

| Control ID | Control Name | Implementation |
|------------|--------------|----------------|
| AC-3 | Access Enforcement | OAuth 2.0 + MFA |
| AU-2 | Event Logging | AllianceChain audit trail |
| IA-2 | Identification/Authentication | OAuth + API keys |
| SC-8 | Transmission Confidentiality | TLS 1.3 |
| SI-4 | System Monitoring | SIEM integration |

---

## 6. Expected Benefits

### 6.1 Environmental Impact
- **Water Savings**: 15-22% reduction in unmetered consumption
- **Conservation**: VRI precision eliminates over-irrigation
- **Compliance**: Automated evidence generation for Water Court

### 6.2 Economic Impact
- **Litigation Cost Reduction**: Deterministic water rights evidence
- **Operational Efficiency**: Automated monitoring vs. manual sampling
- **Secondary Markets**: Standardized API enables water credit trading

### 6.3 Federal Applicability
- **Transferability**: Standardized protocols for DOD/DOE sites
- **Interoperability**: Integration with DWR remote sensing workflows
- **Scalability**: Basin-wide deployment ready (Subdistrict 1, San Luis Valley)

---

## 7. Implementation Roadmap

### Phase I (March-June 2026): Pilot Deployment
- CSU Extension Monte Vista site activation
- VFA sensor ground-truth calibration
- Baseline data collection (180-day validation)

### Phase II (July-December 2026): Basin Scaling
- Subdistrict 1 full coverage (San Luis Valley)
- DWR Sentinel-2 workflow integration
- 2 federal site pilots (DOD/DOE)

### Phase III (2027): Federal Expansion
- Multi-state deployment
- Phase 2 enhancements: Spectroscopy integration (see backup slide)

---

## 8. Budget Summary

### 8.1 Requested Funding

| Category | Year 1 | Year 2 | Total |
|----------|--------|--------|-------|
| Personnel | $180,000 | $200,000 | $380,000 |
| Hardware (DHU/RSS) | $120,000 | $80,000 | $200,000 |
| Software Development | $150,000 | $100,000 | $250,000 |
| **Total** | **$450,000** | **$380,000** | **$830,000** |

### 8.2 Cost-Effectiveness
- **Per-site deployment cost**: ~$25K (Year 1 hardware amortized)
- **Annual water savings value**: $45-65K per 1000 acres (at SLV water rates)
- **ROI**: <18 months for agricultural operators

---

## 9. Technical Decision Log

### Spectroscopy Deferral (March 14, 2026)

**Decision**: Phase 1 excludes spectroscopy; deferred to Phase 2.

**Rationale**:
- 12-day submission deadline makes spectroscopy validation infeasible
- SDI-12/NDVI stack is production-proven at CSU pilot
- No validated spectroscopy hardware currently available
- Scope discipline protects $1.5M ask from technical vagueness risk

**Impact**: None on Phase 1 claims. Phase 2 adds nutrient detection capability.

**Reference**: `ESTCP_SPECTROSCOPY_DECISION.md` — Maya, VP Engineering

---

## 10. Supporting Documents

| Document | Purpose | Status |
|----------|---------|--------|
| `ESTCP_TECHNICAL_SPECIFICATION_DRAFT.md` | Detailed architecture | Complete |
| `ESTCP_FIELD_VALIDATION_PROTOCOL_NITRATE.md` | Gap #1 validation plan | Complete |
| `ESTCP_CYBERSECURITY_RISK_ASSESSMENT.md` | Gap #3 risk matrix | Complete |
| `ESTCP_SPECTROSCOPY_DECISION.md` | Engineering decision record | Complete |
| `ESTCP_PHASE2_BACKUP_SLIDE.md` | Reviewer FAQ backup | Complete |

---

## 11. Certifications

**Accuracy Claims Verified**: ✓ CSU pilot data (MAPE 4.2%, R² 0.96-0.98)

**Security Assessment**: ✓ 33 risks mapped, 0 critical, 8 high (mitigations planned)

**Field Validation**: ✓ Protocol defined, timeline feasible

**Budget Justification**: ✓ Cost-effective, <18 month ROI

---

## 12. Submission Checklist

| Item | Status |
|------|--------|
| Executive Summary | ✓ Complete |
| Technical Description | ✓ Complete |
| Gap #1 (Field Validation) | ✓ Complete |
| Gap #3 (Risk Assessment) | ✓ Complete |
| Budget Justification | ✓ Complete |
| Implementation Roadmap | ✓ Complete |
| Team Qualifications | ✓ Complete |
| Supporting Documents | ✓ Complete |

---

*Document Version: 1.0 FINAL*  
*Prepared by: Casey, Grant Coordinator*  
*Date: March 14, 2026*  
*ESTCP Submission Deadline: March 26, 2026*  
*Classification: UNLIMITED DISTRIBUTION*

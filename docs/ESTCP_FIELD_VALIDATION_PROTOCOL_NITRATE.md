# ESTCP Field Validation Protocol — Gap #1
## Nitrate Sensor Validation at CSU Test Plots

**Document Version**: 1.0  
**Date**: March 14, 2026  
**Prepared by**: Theo, Field Systems Engineer  
**For**: ESTCP Grant Application (Due: March 26, 2026)  
**Project**: ER26-FS-01 — Zero-Trust Spatial Water Management  
**Classification**: UNLIMITED DISTRIBUTION

---

## 1. Purpose & Scope

This Field Validation Protocol establishes the procedures for validating nitrate concentration sensors deployed at the Colorado State University (CSU) Extension test plots in Monte Vista, San Luis Valley, Colorado. The protocol addresses **Gap #1** in the ESTCP execution plan: field validation of in-soil nitrate sensing technology.

### 1.1 Objectives

| Objective | Target Metric |
|-----------|---------------|
| Sensor Accuracy | ±10% of laboratory reference methods |
| Detection Range | 0–100 mg/L NO₃-N |
| Response Time | <15 minutes for 90% step change |
| Field Reliability | >95% uptime over 180-day deployment |
| Data Integrity | Ed25519-signed telemetry packets |

### 1.2 Regulatory Alignment

- **EPA Method 353.2**: Standard for nitrate determination
- **USDA NRCS Conservation Practice Standard**: Nutrient management (Code 590)
- **Colorado Water Quality Control Division**: Discharge permit monitoring requirements

---

## 2. Test Site Description

### 2.1 CSU Extension Monte Vista Station

| Parameter | Value |
|-----------|-------|
| Location | 37.5852° N, 106.1485° W |
| Elevation | 2,340 m (7,677 ft) |
| Soil Series | Terrace gravelly sandy loam |
| Drainage Class | Well-drained |
| irrigation Type | Pivot and linear move |

### 2.2 Test Plot Layout

```
┌─────────────────────────────────────────────────────────┐
│                   CSU TEST PLOT MAP                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   Plot A (Nitrogen Rate Trial)                          │
│   ┌─────┬─────┬─────┬─────┐                            │
│   │ N0  │ N50 │N100 │N150│  (kg N/ha)                  │
│   └─────┴─────┴─────┴─────┘                            │
│                                                          │
│   Plot B (Irrigation Gradient)                          │
│   ┌─────┬─────┬─────┬─────┐                            │
│   │100% │ 75% │ 50% │ 25% │  (% ETc)                   │
│   └─────┴─────┴─────┴─────┘                            │
│                                                          │
│   Sensor Deployment Grid: 5m spacing                    │
│   Depth Profile: 15cm, 30cm, 60cm, 90cm                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Soil Characteristics

| Property | 0–30 cm | 30–60 cm | 60–90 cm |
|----------|---------|----------|----------|
| pH | 7.2 | 7.4 | 7.5 |
| Organic Matter (%) | 1.8 | 1.2 | 0.8 |
| Bulk Density (g/cm³) | 1.45 | 1.52 | 1.58 |
| Clay (%) | 12 | 15 | 18 |
| CEC (meq/100g) | 14 | 12 | 10 |

---

## 3. Sensor System Specification

### 3.1 Nitrate Sensor (ISFET-Based)

| Parameter | Specification |
|-----------|---------------|
| Sensor Model | S::CAN Nitrilex (or approved equivalent) |
| Measurement Principle | Ion-Selective Field Effect Transistor (ISFET) |
| Range | 0–100 mg/L NO₃-N |
| Accuracy | ±5% reading + 1 mg/L |
| Resolution | 0.1 mg/L |
| Operating Temperature | 0–40°C |
| Power Consumption | 50 mW (continuous), 5 mW (standby) |
| Communication | RS-485 Modbus RTU |
| Calibration Interval | 30 days |

### 3.2 Supporting Sensors

| Sensor | Model | Purpose |
|--------|-------|---------|
| Soil Moisture | Campbell Scientific CS655 | Pore water extraction reference |
| Soil Temperature | Campbell Scientific 107-L | Temperature compensation |
| Soil Electrical Conductivity | Campbell Scientific GS3 | Ionic strength correction |
| Soil pH | METERter pH | Interference monitoring |

### 3.3 Data Acquisition System

- **Controller**: Campbell Scientific CR1000X
- **Communication**: LoRa 915 MHz to DHU
- **Logging Interval**: 15 minutes
- **Telemetry**: Ed25519-signed packets per FarmSense security spec

---

## 4. Validation Methodology

### 4.1 Reference Methods

#### 4.1.1 Laboratory Analysis (Primary Reference)

| Method | Laboratory | Turnaround | Accuracy |
|--------|------------|------------|----------|
| EPA 353.2 | CSU Soil, Water & Plant Laboratory | 48 hours | ±2% |
| Colorimetric (Cadmium Reduction) | Certified external lab | 72 hours | ±5% |

#### 4.1.2 Field Reference Methods

| Method | Equipment | Frequency |
|--------|-----------|-----------|
| Portable Nitrate Meter | Horiba LAQUA twin | Weekly spot checks |
| Soil Extraction (KCl) | Field lab kit | Bi-weekly |

### 4.2 Validation Procedures

#### Phase 1: Laboratory Calibration (Pre-Deployment)

1. Prepare standard solutions: 0, 10, 25, 50, 75, 100 mg/L NO₃-N
2. Condition sensors in standards for 24 hours
3. Record readings at 1-minute intervals
4. Generate calibration curve: Sensor Output (mV) vs. Concentration (mg/L)
5. Calculate R²; accept if R² > 0.99
6. Document calibration coefficients in sensor EEPROM

#### Phase 2: Field Installation Verification

1. Install sensors at designated depth profiles (15, 30, 60, 90 cm)
2. Verify soil contact and compaction
3. Connect to data logger and verify telemetry
4. Perform initial reading verification against portable meter
5. Document GPS coordinates and sensor IDs

#### Phase 3: Concurrent Sampling (Active Validation)

| Activity | Frequency | Sample Size |
|----------|-----------|-------------|
| In-situ sensor readings | Continuous (15 min) | All sensors |
| Soil pore water extraction | Weekly | 3 cores per plot |
| Laboratory analysis | Bi-weekly | 12 samples per event |
| Portable meter verification | Weekly | All sensor locations |
| Sensor cleaning/inspection | Weekly | All sensors |

#### Phase 4: Data Analysis & Reporting

1. Calculate correlation between sensor and lab values
2. Compute Mean Absolute Error (MAE) and MAPE
3. Assess temporal stability
4. Identify and document anomalies
5. Generate validation report

---

## 5. Data Collection Procedures

### 5.1 Sensor Data

```
Sensor Reading Schema (FarmSense Telemetry Packet):
{
  "timestamp": "ISO8601",
  "sensor_id": "VFA-NO3-XXX",
  "nitrate_mgl": 12.4,
  "temperature_c": 18.2,
  "moisture_vol_pct": 28.5,
  "ec_ds": 0.8,
  "battery_v": 12.6,
  "signal_rssi": -85,
  "signature": "Ed25519sig..."
}
```

### 5.2 Reference Sample Collection

1. **Soil Coring**: Use a 5-cm diameter auger
2. **Pore Water Extraction**: Use rhizon samplers at designated depths
3. **Sample Handling**:
   - Store on ice immediately
   - Filter through 0.45 μm membrane
   - Preserve with H₂SO₄ to pH < 2
   - Ship to laboratory within 24 hours

### 5.3 Chain of Custody

| Field | Description |
|-------|-------------|
| Sample ID | Unique identifier (e.g., CSU-NO3-2026-001) |
| Collection Date/Time | ISO 8601 format |
| Collector | Full name |
| Location | GPS coordinates + plot/depth |
| Preservation | Method used |
| Lab Received | Date/time + receiver signature |

---

## 6. Quality Assurance / Quality Control

### 6.1 QC Check Frequencies

| QC Activity | Frequency | Acceptance Criteria |
|-------------|-----------|---------------------|
| Calibration verification | Daily | ±10% of standard |
| Duplicate samples | 10% of total | RPD < 20% |
| Field blanks | Weekly | < detection limit |
| Equipment blanks | Monthly | < detection limit |
| Standard reference | Weekly | ±10% of known value |

### 6.2 Data Quality Indicators

| Indicator | Target | Action if Exceeded |
|-----------|--------|-------------------|
| MAPE | <10% | Investigate sensor performance |
| Correlation (r²) | >0.90 | Recalibrate or replace |
| Uptime | >95% | Review power/communication |
| Missing Data | <5% | Redeploy backup sensors |

### 6.3 Anomaly Detection

- **Drift Detection**: Flag readings >2 standard deviations from 7-day mean
- **Jump Detection**: Alert on >20% change between consecutive readings
- **Range Validation**: Reject values outside 0–150 mg/L NO₃-N
- **Temperature Compensation**: Apply correction if temp < 5°C or > 35°C

---

## 7. Data Analysis & Reporting

### 7.1 Statistical Analysis

| Metric | Formula | Target |
|--------|---------|--------|
| Mean Absolute Error | (1/n)Σ| sensor - lab | | <5 mg/L |
| Mean Absolute Percentage Error | (1/n)Σ| sensor - lab | / lab × 100 | <10% |
| Bias | Mean(sensor - lab) | ±2 mg/L |
| Correlation Coefficient | Pearson r | >0.90 |

### 7.2 Reporting Schedule

| Report | Due Date | Audience |
|--------|----------|----------|
| Installation Verification | +7 days from deployment | Internal |
| Weekly QC Summary | Every Friday | Internal |
| Monthly Progress | 1st of month | ESTCP PM |
| Validation Final Report | +180 days | ESTCP/DOD |

### 7.3 Validation Report Contents

1. Executive Summary
2. Sensor Performance Metrics
3. Comparison Analysis (Sensor vs. Lab)
4. Soil-Specific Calibration Adjustments
5. Anomaly Log and Resolution
6. Recommendations for Scale-Up

---

## 8. Timeline & Milestones

| Milestone | Target Date | Deliverable |
|-----------|-------------|--------------|
| Sensor Procurement | April 1, 2026 | PO placed, lead times confirmed |
| Lab Calibration | April 15, 2026 | Calibration certificates |
| Field Installation | May 1, 2026 | Installation report |
| Validation Phase Start | May 15, 2026 | First data transmission |
| Mid-Season Review | July 15, 2026 | Interim report |
| Validation Phase End | November 15, 2026 | Final validation report |
| ESTCP Deliverable | November 30, 2026 | Complete evidence package |

---

## 9. Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Sensor drift | Medium | High | Weekly calibration verification |
| Equipment failure | Low | High | 20% spare sensors on-site |
| Sample contamination | Low | Medium | Strict chain of custody |
| Weather delays | Medium | Low | Flexible sampling schedule |
| Lab turnaround delays | Medium | Medium | Backup lab relationship |

---

## 10. Approvals

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Field Systems Engineer | Theo | [Pending] | 2026-03-14 |
| VP Engineering | Maya | [Pending] | 2026-03-14 |
| ESTCP Program Manager | TBD | [Pending] | 2026-03-14 |

---

*Document ID: ESTCP-FVP-NO3-001*  
*Project: ER26-FS-01*  
*Classification: UNLIMITED DISTRIBUTION*

---
Status: Active
Last Audited: 2026-03-14
Drift Aversion: REQUIRED
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding code or system behavior MUST be reflected here immediately.
> 3. **AI Agent Compliance**: Agents MUST verify the current implementation against this document before proposing changes.
> 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# FarmSense Project Glossary

| Term | Definition | Layer |
| :--- | :--- | :--- |

| **CSA** | **Corner Swing Arm** tracker. Actuator for sweeping corners on fields. | L1 |
| **DHU** | **District Hub**. Edge coordinator mounted on 35ft poles; manages ~100 pivots. | L2 |
| **EBK** | **Empirical Bayesian Kriging**. Geostatistical interpolation method for moisture mapping. | L1.5 / L2 |
| **FHE** | **Fully Homomorphic Encryption**. Cryptography allowing math on encrypted data. | L3 / L4 |
| **HAPS** | **Horizontal Profiling Sled**. Sensor configuration for lateral moisture tracking. | L1 |
| **Kriging** | A geostatistical interpolation method that accounts for spatial autocorrelation. | L2 / L3 |
| **LPI/LPD** | **Low Probability of Intercept / Detection**. Secure radio emission standards. | L1 |
| **LRZB / LRZN** | **Lateral Root Zone Beacon / Lateral Root Zone Node**. High-density ground-truth sensors. | L1 |
| **MAD** | **Management Allowable Depletion**. Percentage of water soil can lose before stress. | Logic |
| **NDVI** | **Normalized Difference Vegetation Index**. Satellite-derived measure of plant health. | L0 / L4 |
| **PFA** | **Pressure & Flow Analyzer**. Safety actuator and wellhead monitoring node. | L1 |
| **PMT** | **Pivot Motion Tracker**. Field aggregator and kinematic auditor on the pivot span. | L1.5 |
| **RSS** | **Regional Superstation**. territory master node (40' HC Container). | L3 |
| **SFD** | **Single Field Deployment**. Modular configurations for pivot, corner, or flood fields. | Logic |
| **SPAC** | **Soil-Plant-Atmosphere Continuum**. Modeling fluxes across soil, plants, and air. | Science |
| **VFA** | **Vertical Field Anchor**. Sub-surface truth node for deep percolation auditing. | L1 |
| **VRI** | **Variable Rate Irrigation**. Precisely applying different water amounts across a field. | Execution |
| **Zo** | The **Core Compute Server** executing master geostatistical models. | L3 / L4 |

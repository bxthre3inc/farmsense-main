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

# IP_INVENTORY: Defensible Intellectual Property Portfolio

This document registers the core Intellectual Property (IP) modules of the FarmSense project. Each entry links to its primary specification and logic owner.

## 1. Physical & Core Logic

- **SFD (Single Field Deployment)**: The proprietary modular hardware and logic configuration platform.

  - *Spec Link*: [Master Manual §5.7](v2_1_part5_remaining_hardware.md#57-single-field-deployment-sfd-configurations)

- **SPAC Engine**: Soil-Plant-Atmosphere Continuum thermodynamics engine.

  - *Spec Link*: [Master Manual §1.2](MASTER_MANUAL.md#12-spac-modeling-and-edaphic-variability)

- **Adaptive Recalculation**: The "Fisherman's Attention" engine for localized moisture reactivity.

  - *Spec Link*: [Master Manual §4.5](MASTER_MANUAL.md#45-adaptive-recalculation-engine-fishermans-attention)

- **Kriging Engine**: Advanced Geostatistical interpolation (Zo/Oracle).

  - *Spec Link*: [Master Manual §1.4](MASTER_MANUAL.md#14-system-architecture-overview)

## 2. Hardware Topology & Deployment

- **RSS (Regional Superstation)**: Level 3 territory master node.

  - *Spec Link*: [Master Manual §1.4](MASTER_MANUAL.md#14-system-architecture-overview)

- **DHU (District Hub)**: Level 2 regional mesh manager.

  - *Spec Link*: [Master Manual §5.2](MASTER_MANUAL.md#52-district-hub-dhu-v19)

- **PMT (Pivot Motion Tracker)**: The "Field Hub" — span-mounted primary aggregator and kinematic auditor.

  - *Spec Link*: [Master Manual §5.3](MASTER_MANUAL.md#53-pivot-motion-tracker-pmt-v17)

- **HAPS (Horizontal Profiling Sled)**: Sensor configuration for lateral moisture tracking (Alpha-Sled variant).
  - *Spec Link*: [Master Manual §5.5.4](v2_1_part5_remaining_hardware.md#554-the-alpha-sled-design)

## 3. Communication & Infrastructure

- **LRZN (Lateral Root Zone Node)**: High-density RF mesh nodes.
  - *Spec Link*: [Master Manual §1.5](MASTER_MANUAL.md#15-telemetry-architecture-resolution)

- **LRZB (Lateral Root Zone Beacon)**: Primary beacon nodes for field network synchronization.
  - *Spec Link*: [Master Manual §1.5](MASTER_MANUAL.md#15-telemetry-architecture-resolution)

- **AllianceChain**: Private PBFT consensus for digital agricultural auditing.
  - *Spec Link*: [Master Evidence Spec §3](MASTER_EVIDENCE_SPEC.md#3-data-integrity-requirements)

- **FHE Enclave**: Zero-Knowledge Privacy framework for spatial data.
  - *Spec Link*: [Master Manual §4.1.2](v2_1_part4_tech_hardware.md#412-compute-hierarchy)

## 4. Analytics & Regulatory

- **VFA (Vertical Field Anchor)**: Sub-surface truth node for deep percolation auditing.

  - *Spec Link*: [Master Manual §5.5](MASTER_MANUAL.md#55-vertical-field-anchor-vfa-v21)

- **PFA (Pressure & Flow Analyzer)**: Wellhead monitoring and safety actuator.

  - *Spec Link*: [Master Manual §5.4](MASTER_MANUAL.md#54-pressure-flow-anchor-pfa-v19)

- **CSA (Corner Swing Arm)**: Tracker and auditor for swing-arm irrigation sections.

- **DAP (Drift Aversion Protocol)**: The proprietary modular framework for specification/implementation synchronization.

  - *Spec Link*: [MASTER_IP_LEGAL.md](MASTER_IP_LEGAL.md)

- **DFOS (Deterministic Farming Operating System)**: The core system identity and rule-based compute logic.

---
*Proprietary IP of bxthre3 inc. — Confidential*

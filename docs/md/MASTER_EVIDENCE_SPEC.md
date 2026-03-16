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

# MASTER_EVIDENCE_SPEC: Digital Water Ledger Compliance

## 1. Statutory Context

This specification ensures that the FarmSense RSS Ledger exports meet the non-repudiation and evidentiary requirements for **DWR Rule 12.0** and the **Subdistrict 1 Adaptive Management Plan**.

## 2. Export Format: Digital Water Ledger (DWL)

Evidence must be exported as a cryptographically sealed ZIP manifest containing:

- `manifest.json`: Root metadata with Ed25519 system signature.
- `ledger.csv`: Historical transaction records (Trade ID, From, To, Amount, Pulse-Timestamp).
- `proofs/*.sig`: Individual PBFT consensus certificates for each transaction.
- `validation_report.pdf`: Human-readable summary of Kriging MAPE scores and ground-truth alignment.

## 3. Data Integrity Requirements

| Requirement | System Implementation |
| :--- | :--- |
| **Immutability** | AllianceChain PBFT Consensus (Quorum-based COMMIT) |
| **Authenticity** | Ed25519 Field-Layer Signatures (DHU RSA/EdDSA) |
| **Spatial Grounding** | RSS 1m Kriging with LOOCV validation (<5% MAPE) |
| **Auditability** | `audit_logs` table with unique integrity hashes |

## 4. Evidence Retrieval Procedure

1. **Selection**: User selects the Date Range and Field ID(s) via the Compliance Portal.
2. **Aggregation**: `AuditService` pulls records from `WaterTrade` and `AuditLog`.
3. **Sealing**: The `RegulatoryAuditService.sign_audit_payload` applies the Master Private Key.
4. **Download**: System generates the `.dwl` file for submittal to the Water Court Clerk.

## 5. Compliance Checklist for June 29 Hearing

- [ ] Verify Master DHU Public Keys are on file with the State Engineer's Office.
- [ ] Ensure all 'Suspect' quality sensors are flagged and excluded from the export.
- [ ] Generate a 'Dry Run' audit report for the Monte Vista Pilot site by May 15.

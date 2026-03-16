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

# DAP Framework (Agent Guide)

This skill mandates that all AI agents acting within the FarmSense repository adhere to the **DAP (Drift Aversion Protocol)** framework, comprising **D-DAP** and **E-DAP**.

## Core Mandates

### 1. D-DAP: Documentation Drift Aversion
Before proposing or implementing any changes, you MUST read the corresponding documentation in the `docs/` directory to understand the "Single Source of Truth."

### 2. E-DAP: Engineering Drift Aversion
Every implementation change MUST be synchronized with documentation updates in the same transaction. "Ghost Edits" (code changes without documentation updates) are a violation of D-DAP. Architectural deviations and file sprawl (e.g., `.bak` files) are violations of E-DAP.

### 3. Maintain Metadata
Ensure all documentation files have the required metadata header:
```yaml
---
Status: Active
Last Audited: [Today's Date]
Drift Aversion: REQUIRED
---
```

### 4. Continuous Audit
Run the `scripts/verification/verify_drift_protocol.py` script frequently to ensure the repository remains compliant.

## Implementation Examples

### Wrong:
1. Update `backend/api/router.py` to add a new endpoint.
2. Notify user.

### Right:
1. Update `backend/api/router.py` to add a new endpoint.
2. Update `docs/MASTER_SOFTWARE_ARCH.md` with the new endpoint details.
3. Update `docs/MASTER_SOFTWARE_ARCH.md` metadata header `Last Audited` date.
4. Run `python3 scripts/verification/verify_drift_protocol.py`.
5. Notify user.
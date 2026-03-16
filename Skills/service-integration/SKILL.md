---
Status: Active
Last Audited: 2026-03-15
Drift Aversion: REQUIRED
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding code or system behavior MUST be reflected here immediately.
> 3. **AI Agent Compliance**: Agents MUST verify the current implementation against this document before proposing changes.
> 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

---
name: service-integration
description: |
  Autonomous management of service transitions from mock implementations 
  to real-world production providers. Handles payment gateways, KYC, 
  and geolocation service integration flows.
compatibility: Optimized for VPC Core Engine
metadata:
  author: antigravity.agent
  category: Integration
  version: 1.0
---

# Service Integration Skill

Guidelines and automation for swapping mock services with production APIs.

## Capabilities

1. **Provider Mapping**
   - Identify mock implementations in the `backend/services/` directory.
   - Map mock interfaces to production provider SDKs (e.g., Stripe, Plaid).
   - Generate adapter layers for seamless swapping.

2. **Integration Verification**
   - Run integration test suites against sandbox environments.
   - Verify transaction state mapping between VPC engine and provider.
   - Audit webhooks and async callback logic for and edge-case handling.

3. **Compliance Sync**
   - Ensure production providers meet regulatory standards documented in `docs/md/MASTER_IP_LEGAL.md`.
   - Update `IP_INVENTORY.md` when new core service IP is integrated.

4. **Secret Management**
   - Securely provision provider API keys via environment injection.
   - Verify non-committal of secrets to version control.

## Usage

### Switch Service to Production

```bash
python3 scripts/integration/swap_service.py --service payment --provider stripe
```

### Verify Sandbox Integration

```bash
python3 scripts/integration/verify_sandbox.py --service kyc
```

## Integration Safeguards
- **Circuit Breaking**: Automated fallback to "Maintenance Mode" if production provider latency exceeds 500ms.
- **Audit Logging**: Mandatory logging of all external provider state transitions.

---
*Standardizing FarmSense integration pipelines — 2026-03-15*

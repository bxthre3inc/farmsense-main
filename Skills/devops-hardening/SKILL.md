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
name: devops-hardening
description: |
  Autonomous production hardening and security auditing for the FarmSense 
  cloud and edge infrastructure. Standardizes Zo server deployment, 
  environment variable verification, JWT security, and network rate limiting.
compatibility: Optimized for Zo Server & FastAPI
metadata:
  author: antigravity.agent
  category: DevOps
  version: 1.0
---

# DevOps Hardening Skill

Automated procedures for ensuring production-grade security and reliability.

## Capabilities

1. **Environment Audit**
   - Verify all required `.env` variables for production.
   - Flag missing secrets or insecure defaults.
   - Sync local `.env` with production vault.

2. **Security Hardening**
   - Audit JWT implementation for expiry and signature strength.
   - Verify WebSocket rate limiting and CORS policies.
   - Sanitize error responses to prevent information leakage.

3. **Zo Server Deployment**
   - Validate Docker Compose configurations for production resources.
   - Run pre-deployment connectivity tests (PostgreSQL, TimescaleDB).
   - Audit CI/CD pipeline integrity before deployment.

4. **Resource Monitoring Setup**
   - Standardize Prometheus/Grafana alerting thresholds.
   - Verify log rotation and retention policies.

## Usage

### Run Production Readiness Audit

```bash
python3 scripts/devops/audit_production.py --env production
```

### Verify Security Middleware

```bash
python3 scripts/devops/verify_middleware.py --targets jwt,ratelimit
```

### Validate Docker Configs

```bash
python3 scripts/devops/validate_docker.py --composition production
```

## Performance Standards
- **Sync Time**: < 10s for full environment validation.
- **Audit Depth**: Recursive scanning of all `backend/` and `edge-compute/` modules.

---
*Codifying FarmSense production standards — 2026-03-15*

# ESTCP Spectroscopy Validation Decision

**Decision Owner:** Maya, VP of Engineering  
**Date:** March 14, 2026  
**Deadline:** March 26, 2026 (12 days)  
**Decision:** **OPTION B — Remove spectroscopy references**

---

## Assessment Summary

| Criterion | Option A (Include Spectroscopy) | Option B (SDI-12/NDVI Only) |
|-----------|-----------------------------------|----------------------------|
| **Technical Feasibility (12d)** | ❌ **High Risk** — No existing spectroscopy specs in repo. Patent filing shows this was a known blocker. Drew would need 24h minimum to generate specs, plus integration documentation. | ✅ **Low Risk** — SDI-12 protocol is standardized (IEC 62055-41). NDVI validation via Sentinel-2 is operational in current Kriging pipeline. |
| **Reviewer Perception** | Moderate positive — "Additional validation layer" sounds impressive but reviewers value *demonstrated* capability over *claimed* sophistication. | **Strong positive** — Clean, proven architecture. ESTCP evaluators prefer deterministic systems with measurable outcomes. Our Kriging MAPE <5% claim is already auditable. |
| **Risk Profile** | **CRITICAL** — Incomplete spectroscopy specs = fatal flaw. Reviewers will flag vague technical claims. Casey flagged this as blocking in AGENT_EMPLOYEE_ARCHITECTURE.md. | **Managed** — VFA ground-truth sensors + Sentinel-2 NDVI provide dual-validation. This is production-proven at CSU pilot. |

---

## Technical Rationale

### Why Spectroscopy is the Wrong Call for ESTCP

1. **We lack validated spectroscopy hardware** — The patent filing (line 318) explicitly notes "spectroscopy sensor integration" as a critical task we haven't completed. There's no BOM, no supplier engagement, no calibration data.

2. **12 days is insufficient for credible specification** — Even with Drew generating specs in 24h (best case), we need:
   - Supplier sourcing and quotes
   - Calibration methodology documentation  
   - Integration specs with our nRF52840/ESP32-S3 sensor layer
   - Field validation data (impossible in 12 days)

3. **SDI-12 + NDVI is already production-proven** — Our tri-layer compute topology validates via:
   - **Level 0:** VFA (Vertical Flux Array) sensors with SDI-12 output — ground-truth calibration target
   - **Level 2-3:** NDVI covariates in Regression Kriging — operational since CSU pilot
   - **Audit trail:** Ed25519-signed telemetry with LOOCV cross-validation

4. **ESTCP evaluators value execution over ambition** — DoD program officers have seen too many "kitchen sink" proposals with unproven tech. A tight, validated SDI-12/NDVI/Kriging stack demonstrates *deterministic* water monitoring capability.

---

## Risk Analysis

### Option A Risks (if chosen)
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Incomplete spectroscopy specs | 90% | **FATAL** — Proposal rejected for technical vagueness | N/A — cannot mitigate in 12d |
| Integration holes flagged in review | 70% | HIGH — Technical score reduction | Would require emergency spec generation |
| Casey blocked on submission | 60% | HIGH — Miss March 26 deadline | Parallel workstreams (high coordination cost) |

### Option B Risks (if chosen)
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Reviewers perceive less sophistication | 30% | LOW — Can counter with MAPE <5% metric | Emphasize Kriging R² 0.96-0.98 in narrative |
| Future capability gap | 20% | LOW — Spectroscopy remains roadmap item | Document as Phase II enhancement |

---

## Recommendation

**Execute Option B immediately.**

This is not a technical compromise — it's a **scope discipline decision**. We are not removing validation; we are standardizing on the validation architecture that already works. Our SDI-12/NDVI/Kriging pipeline delivered <5% MAPE at CSU pilot. That's the story ESTCP needs to hear.

Adding spectroscopy now would be resume-driven development at the worst possible moment. It risks the entire $1.5M ask for a "nice to have" that we cannot substantiate.

---

## Action Items

| # | Action | Owner | Due | Status |
|---|--------|-------|-----|--------|
| 1 | **Remove all spectroscopy references** from ESTCP_TECHNICAL_SPECIFICATION_DRAFT.md | Zoe | Today | ⏳ Pending |
| 2 | **Expand SDI-12 validation section** — Document VFA sensor integration, calibration methodology, field accuracy metrics | Maya | March 16 | ⏳ Pending |
| 3 | **Strengthen NDVI narrative** — Reference Sentinel-2 integration, Regression Kriging covariates, R² 0.96-0.98 validation | Casey | March 17 | ⏳ Pending |
| 4 | **Update proposal budget** — Remove spectroscopy hardware line items (~$45K estimated), reallocate to VFA sensor densification if needed | Alex | March 18 | ⏳ Pending |
| 5 | **Verify no patent/IP conflicts** — Confirm removing spectroscopy doesn't affect provisional filing claims | Maya + Legal | March 19 | ⏳ Pending |
| 6 | **Final technical review** — Ensure no orphaned spectroscopy mentions in submission package | Zoe | March 24 | ⏳ Pending |

---

## Decision Log

**Decision:** **B** — Delete spectroscopy references, proceed with SDI-12/NDVI validation only.

**Rationale:** 12-day deadline makes spectroscopy inclusion technically infeasible and review-risky. Our existing SDI-12/NDVI/Kriging validation stack is production-proven, auditable, and sufficient for ESTCP technical requirements. Scope discipline protects the $1.5M ask.

**Escalation trigger:** If Drew produces spectroscopy specs before March 18 AND Casey confirms no submission delay, Maya may reconsider as **Phase II addendum** (not primary validation method).

---

*Document status: DECIDED — Awaiting execution*  
*Next checkpoint: March 16 (post-SDI-12 section expansion)*

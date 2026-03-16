---
Status: Active
Last Audited: 2026-03-15
Drift Aversion: REQUIRED
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> **Requirement: Integrity Skill (CRP/IDR/ARA)**
> 1. **Cross-Referencing Protocol (CRP)**: All document links MUST be relative and verified.
> 2. **Intra-Document Referencing (IDR)**: Internal anchors and section references MUST be consistent.
> 3. **Alignment & Redundancy Audit (ARA)**: Ensure single source of truth across all "Master" documents.

# Documentation Integrity Skill

This skill provides mandatory procedures for ensuring that the FarmSense documentation remains a high-fidelity, synchronized, and reliable "Single Source of Truth."

## 1. CRP: Cross-Referencing Protocol
When adding or modifying links between documents:
- **Relative Paths**: Always use relative paths from the current document (e.g., `[Manual](MASTER_MANUAL.md)` from `docs/md/`).
- **Reciprocity**: If Document A refers to a critical section in Document B, verify if Document B needs a back-reference to Document A for navigational symmetry.
- **Link Auditing**: Before committing documentation changes, run `python3 scripts/verification/verify_links.py`.

## 2. IDR: Intra-Document Referencing
When referencing sections within the same document:
- **Anchor Validity**: Use standard Markdown anchors (e.g., `#section-name`). Verify that the anchor exactly matches the header.
- **Line-by-Line Alignment**: For high-stakes specifications (BOMs, Lawsuit Evidence), perform a line-by-line comparison with the source of truth if updates are manual.
- **No Orphan Headers**: Every header must be reachable and relevant to the document's scope.

## 3. ARA: Alignment & Redundancy Audit
When managing information across multiple files:
- **Single Source of Truth (SSoT)**: Technical data (e.g., hardware costs) should reside in ONE master document (usually `MASTER_MANUAL.md`). Refer to it from others, do not duplicate.
- **Redundancy Elimination**: If a data point exists in two places, identify the authoritative source and convert the other into a reference link.
- **Missing Link Detection**: Audit documents to ensure every "canonical" data point (from the `NAVIGATION.md` index) is properly detailed in its respective master file.

## Implementation Workflow (Agentic)
1. **Research**: Identify all documents affected by the change.
2. **Draft**: Update the authoritative document.
3. **Cross-Check**: Verify all references to updated sections in other documents.
4. **Verify**: Run `scripts/verification/verify_links.py` and `scripts/verification/verify_drift_protocol.py`.
5. **Audit**: Update the `Last Audited` metadata field.

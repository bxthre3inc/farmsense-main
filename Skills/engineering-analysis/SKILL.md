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

---
name: engineering-analysis
description: |
  Autonomous engineering analysis for FarmSense technical documentation,
  protocol resolution, BOM validation, and RF coexistence verification.
  Runs technical reviews, produces Engineering Decision Records (EDRs),
  and maintains Engineering Review Plans without requiring human engineers.
compatibility: Created for Zo Computer
metadata:
  author: brodiblanco.zo.computer
  category: FarmSense
  version: 1.0
---

# Engineering Analysis Skill

Autonomous technical review and analysis for solo-founder engineering workflows.

## Capabilities

1. **Protocol Architecture Analysis**
   - Identify receiver/transmitter mismatches
   - Recommend standardization paths
   - Produce EDRs with trade-off matrices

2. **BOM Validation**
   - Cross-reference BOMs against specifications
   - Flag cost variations and component mismatches
   - Generate aligned BOM CSVs

3. **RF Coexistence Analysis**
   - Analyze frequency band conflicts
   - Calculate interference margins
   - Recommend guard bands and filtering

4. **Documentation Harmonization**
   - Standardize terminology across specs
   - Resolve naming inconsistencies
   - Maintain master glossary

## Usage

### Run Engineering Review Phase

```bash
python3 /home/workspace/Skills/engineering-analysis/scripts/review.py --phase 1
```

Phases:
- 1: Protocol Architecture Lock
- 2: BOM Validation  
- 3: RF Coexistence Analysis
- 4: Documentation Harmonization

### Generate EDR

```bash
python3 /home/workspace/Skills/engineering-analysis/scripts/edr.py --topic "PMT Receiver Protocol" --options nRF52840,SX1262
```

### Validate BOM Alignment

```bash
python3 /home/workspace/Skills/engineering-analysis/scripts/bomcheck.py --spec VFA --bom /path/to/bom.csv
```

## Output Format

All deliverables saved to:
- `docs/engineering/EDRs/` — Engineering Decision Records
- `docs/engineering/Reports/` — Analysis reports
- `docs/engineering/BOMs/` — Validated BOM CSVs

## Task Management Integration

When running in Antigravity IDE context, the skill:
1. Reads task files from `Tasks/`
2. Updates status in task frontmatter
3. Writes completion reports to `Reports/`
4. Creates follow-up tasks as needed

---
*For FarmSense solo-founder engineering workflows*
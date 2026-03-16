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

# Grant Application Tracking System (GATS)

**For Managing 100+ Grant Opportunities**

## System Overview

This document defines the tracking infrastructure for Bxthre3/FarmSense's global grant pipeline. 

## Tracking Schema

### Grant Record Structure

```
GRANT_ID: [CATEGORY]-[REGION]-[NUMBER]
  Example: FED-US-001, FDN-GLB-015, STA-CO-003

FIELDS:
├── Basic Information
│   ├── grant_name (string)
│   ├── funder (string)
│   ├── category (enum: FEDERAL, STATE, FOUNDATION, INTERNATIONAL, CORPORATE)
│   ├── region (string: US, CO, CA, EU, AF, AS, SA, OC)
│   └── url (string)
│
├── Financial
│   ├── max_amount (number)
│   ├── min_amount (number)
│   ├── currency (enum: USD, EUR, GBP, AUD, CAD)
│   └── funding_type (enum: GRANT, PRIZE, EQUITY, DEBT, HYBRID)
│
├── Timeline
│   ├── deadline (date)
│   ├── deadline_type (enum: HARD, ROLLING, INVITE)
│   ├── award_date (date)
│   └── project_duration (months)
│
├── Status Tracking
│   ├── stage (enum: IDENTIFIED, RESEARCHING, PITCHING, APPLIED, SHORTLIST, AWARDED, REJECTED, WITHDRAWN)
│   ├── priority (enum: P0, P1, P2, P3)
│   ├── probability (percent)
│   └── expected_value (calculated: amount × probability)
│
├── Application Details
│   ├── application_portal (string)
│   ├── account_created (boolean)
│   ├── requirements_checklist (array)
│   ├── materials_submitted (array)
│   └── notes (text)
│
└── Team Assignment
    ├── lead_applicant (string)
    ├── support_team (array)
    └── external_partners (array)
```

## Stage Definitions

| Stage | Definition | Action Required |
|-------|-----------|-----------------|
| **IDENTIFIED** | Grant discovered, basic info captured | Research eligibility |
| **RESEARCHING** | Eligibility confirmed, requirements known | Gather materials, assess fit |
| **PITCHING** | Initial outreach/LOI submitted | Prepare full application |
| **APPLIED** | Full application submitted | Track status, prepare for interview |
| **SHORTLIST** | Advanced to final round | Prepare presentation, negotiate |
| **AWARDED** | Funding secured | Execute contract, begin project |
| **REJECTED** | Declined | Capture feedback, archive |
| **WITHDRAWN** | Voluntarily withdrawn | Document reason |

## Priority Matrix

```
PRIORITY = f(Amount, Deadline, Probability, Strategic Fit)

P0 (CRITICAL): >$500K, <30 days, >25% probability, core mission
P1 (HIGH): >$250K, <90 days, >15% probability, strong alignment  
P2 (MEDIUM): >$100K, <180 days, >10% probability, good fit
P3 (LOW): <$100K, >180 days, any probability, opportunistic
```

## Automation Rules

### Date-Based Triggers

- **T-30 days**: Move P2 → P1 if materials ready
- **T-14 days**: Daily standup on P0 grants
- **T-7 days**: Final review required
- **T-3 days**: Submit or withdraw decision
- **T+1 day**: Archive if not submitted

### Status-Based Actions

- **IDENTIFIED → RESEARCHING**: Auto-assign to grant queue
- **RESEARCHING → PITCHING**: Create application workspace
- **APPLIED → SHORTLIST**: Schedule prep call
- **REJECTED**: Capture funder feedback, update probability model

## Dashboard Views

### 1. Pipeline Overview

```
Active Grants: [COUNT]
By Stage: [IDENTIFIED: X] [RESEARCHING: X] [PITCHING: X] [APPLIED: X] [SHORTLIST: X]
By Priority: [P0: X] [P1: X] [P2: X] [P3: X]
Expected Value: $[SUM of (amount × probability) for APPLIED+SHORTLIST]
```

### 2. This Week's Actions

```
Deadline This Week: [LIST]
New Applications Started: [LIST]
Awaiting Materials: [LIST]
Follow-up Required: [LIST]
```

### 3. Performance Metrics

```
Win Rate: [AWARDED / (AWARDED + REJECTED)]
Avg Time to Award: [Days from APPLIED to AWARDED]
Pipeline Conversion: [% advancing from RESEARCHING to APPLIED]
Funding Secured (YTD): $[TOTAL]
```

## Integration Points

### With FarmSense Systems

- Pull pilot data for "Current Impact" fields
- Auto-populate "Team" from org chart
- Sync deadlines with calendar
- Export reports for investor updates

### With Calendar

- T-30: Create calendar event
- T-14: Block time for daily check-ins
- T-7: Block time for final review
- T-1: Submission deadline alarm

## Implementation Options

### Option A: Airtable (Recommended)

- Base with 6 tables: Grants, Applications, Tasks, Documents, Contacts, Reports
- Views: Kanban by stage, Calendar by deadline, Grid by priority
- Automations: Email reminders, status updates, Slack notifications

### Option B: Notion Database

- Single database with filtered views
- Linked pages for application workspaces
- Templates for common grant types

### Option C: Custom Web App/Add to Admin Console

- React + Supabase (scales to any size)
- API integrations with Grants.gov, foundations
- Custom reporting dashboards

## Recommended: Airtable Setup

### Table: Grants (Master List)

Fields as defined in schema above

### Table: Applications (Per-Grant Workspaces)

- Link to Grant
- Status (In Progress, Under Review, Submitted, Awarded, Rejected)
- Application Portal URL
- Username/Password (encrypted)
- Key Documents (file attachments)
- Notes & Decisions

### Table: Tasks

- Link to Grant
- Task Type (Research, Draft, Review, Submit)
- Due Date
- Assigned To
- Status (Open, In Progress, Done, Blocked)

### Table: Documents

- Document Type (Narrative, Budget, Logic Model, Letters)
- Version
- Last Updated
- Status (Draft, Review, Final)
- File Attachment

### Automations to Configure

1. **Deadline Alert**: 7 days before → Slack DM + Email
2. **Status Change**: Move to APPLIED → Post to #grants-wins
3. **Weekly Digest**: Every Monday → Pipeline status report
4. **Monthly Review**: 1st of month → Win rate analysis

## Next Steps

1. **Choose platform** (Airtable recommended)
2. **Import 167 grants** from Global Intelligence doc
3. **Assign priorities** to all grants
4. **Set up automations**
5. **Create first 5 application workspaces**

---

*This system enables managing 100+ grants with the rigor of a Series A startup.*

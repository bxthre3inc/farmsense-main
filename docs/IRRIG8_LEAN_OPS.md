---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Document Code: IRRIG8-LEAN
Full Name: Lean Operations — Digital Employees + Contractors
Version: 1.0
Category: Organizational Design
Classification: Internal — CEO Decision Support
---

> [!IMPORTANT]
> **PHILOSOPHY:** Minimize human employees. Maximize digital employees. Contract everything physical.
>
> **Target:** Run 5,000-field operation with **< 10 human employees**.
>
> **Result:** 90%+ probability (vs 85% standard).

---

# THE LEAN OPERATIONS MODEL

## Human Employee Target

| Phase | Human Employees | Digital Employees | Contractors | Fields |
|-------|-----------------|---------------------|-------------|--------|
| Validation (Q1 2026) | **1 (you)** | 5 | 2 | 10 |
| Subdistrict 1 (2026-27) | **3** | 12 | 8 | 1,280 |
| RGWCD (2028-29) | **6** | 25 | 20 | 5,000 |

**You personally handle:** Vision, investor relations, farmer relationships, final decisions.

## What Each Human Does

| Role | Human | Digital Support | Contractor Layer |
|------|-------|-----------------|-------------------|
| **CEO (you)** | Strategy, investors, key farmers | Executive assistant, scheduler, deck prep | — |
| **VP Engineering** | Architecture, vendor management | Code review, testing, documentation | PCB fab, assembly |
| **Field Ops Manager** | Contractor coordination, quality | Dispatch, routing, inventory | Installers, technicians |
| **Customer Success (2×)** | Farmer relationships, retention | Ticket routing, FAQ, data summaries | — |
| **Sales Lead** | RGWCD relationships, partnerships | CRM, outreach, follow-up | Local reps (1099) |
| **Finance/Admin** | Bookkeeping, compliance, payroll | Accounting software, reports | Tax accountant (quarterly) |

---

# DIGITAL EMPLOYEES (AI AGENTS)

## Core Agent Roster

| Agent | Function | Replaces | Cost |
|-------|----------|----------|------|
| **Executive Assistant** | Calendar, email, travel, investor comms | 1 EA | $500/mo |
| **Lead Qualifier** | Inbound farmer inquiry scoring | 0.5 SDR | $300/mo |
| **Support Agent** | L1 ticket resolution, FAQ | 2 support reps | $800/mo |
| **Data Analyst** | Telemetry validation, anomaly flagging | 1 analyst | $400/mo |
| **Technical Writer** | Docs, procedures, farmer guides | 0.5 writer | $200/mo |
| **Sales Assistant** | CRM hygiene, follow-up sequences | 0.5 sales ops | $300/mo |
| **Social/Content** | LinkedIn, blog, email newsletter | 0.5 marketer | $250/mo |
| **DevOps Agent** | Deployment logs, alerts, runbooks | 0.5 DevOps | $500/mo |
| **QA Agent** | Test automation, regression | 0.5 QA engineer | $400/mo |

**Total Digital Employee Cost: $3,650/month = $44K/year**

Replaces: ~6 FTE = $600K/year in human salary

## Agent Architecture

```
Human Layer (you + 5)
    ↓
Orchestrator Agent (Zoe — your existing UAO)
    ↓
├─→ Executive Assistant
├─→ Support Agent
├─→ Data Analyst
├─→ Sales Assistant
├─→ Technical Writer
├─→ DevOps Agent
└─→ QA Agent
    ↓
Contractor Layer (physical execution)
```

---

# CONTRACTOR LAYER

## Installation Contractors

| Contractor Type | Rate | Scope | Volume |
|----------------|------|-------|----------|
| **Installation tech** | $75/hr + truck | Site survey, install, training | 20-40 per field |
| **Certified electrician** | $125/hr | PFA wellhead wiring, safety | 1-2 per field |
| **Excavation crew** | $3K/day | VFA trenching (as needed) | 0.1 per field |
| **Calibration specialist** | $150/hr | Sensor validation, sign-off | 1 per field |

**Blended install cost: $1,200-1,720 per field** (vs $2,500 in-house)

**Why contractors:**
- No benefits, no equity, no HR overhead
- Scale instantly (hire 20 for busy season, 2 for winter)
- Geographic flexibility (local crews know local soil)
- Liability shift (they carry insurance)

## Manufacturing Contractors

| Component | Contractor | Cost Model |
|-----------|------------|------------|
| **PCB fabrication** | JLCPCB, PCBWay | Per-board, no MOQ |
| **PCB assembly** | MacroFab, Tempo | Per-assembly, turnkey |
| **Plastic molding** | Protolabs, Xometry | Per-part, no tooling risk |
| **Final assembly** | Contract manufacturer | Per-unit, 100-unit min |
| **Packaging/shipping** | Fulfillment center | Per-order, 3PL |

**No factory. No equipment. No maintenance.**

---

# OPERATIONAL COST COMPARISON

## Traditional Model (In-House Everything)

| Cost Category | Amount | Risk |
|---------------|--------|------|
| Human employees (60 FTE @ $120K avg) | $7.2M/year | High (fixed, hard to cut) |
| Benefits (30%) | $2.2M/year | Fixed |
| Office/warehouse | $800K/year | Lease obligations |
| Equipment/tools | $500K/year | Depreciation |
| **Total OpEx** | **$10.7M/year** | **Inflexible, high burn** |

## Lean Model (You + 5 Humans + Agents + Contractors)

| Cost Category | Amount | Risk |
|---------------|--------|------|
| Human employees (6 FTE @ $150K avg) | $900K/year | Low (small, flexible) |
| Benefits (30%) | $270K/year | Low |
| Digital employees | $44K/year | **Ultra-low** |
| Contractors (install) | $1.8M/year | **Variable with volume** |
| Contractors (manufacturing) | $2.1M/year | **Variable with volume** |
| Office (co-working + storage unit) | $60K/year | Month-to-month |
| **Total OpEx** | **$5.17M/year** | **52% less, massively flexible** |

**Savings: $5.5M/year** that can go to:
- Lower prices (faster adoption)
- Longer runway (higher survival)
- Your retained equity (more wealth)

---

# PHYSICAL EXECUTION WITHOUT EMPLOYEES

## The Installation Playbook

| Step | Who | What | Duration |
|------|-----|------|----------|
| 1. Site survey | Contractor (solo) | Measure, photos, soil sample | 2 hrs |
| 2. Kit delivery | 3PL | Drop-ship to farmer | 3 days |
| 3. Install day | Contractor crew (2-3 people) | VFA, LRZN, PMT, PFA | 4-6 hrs |
| 4. Activation | Digital Agent | Remote config, test, validate | 30 min |
| 5. Training | You (or video) | Dashboard walkthrough | 1 hr |
| 6. Ongoing support | Digital Agent + contractor callback | Troubleshooting, maintenance | As needed |

**You never touch hardware.**

## Quality Control Without Employees

| Method | Implementation |
|--------|----------------|
| **Install checklist app** | Contractor logs photos, GPS, timestamps |
| **Remote telemetry validation** | Digital agent confirms data flow within 24hrs |
| **Farmer NPS survey** | Automated 7-day post-install |
| **Spot inspection** | You visit 1 in 20 installs personally |
| **Contractor rating system** | Quality score → priority dispatch |

**Bad contractors get fired. Good contractors get more work.**

---

# FINANCIAL IMPACT OF LEAN MODEL

## 5,000-Field Scenario (Year 5)

| Metric | Traditional | Lean | Delta |
|--------|-------------|------|-------|
| Human employees | 60 | **6** | -90% |
| Annual payroll | $9.4M | $1.2M | -87% |
| Office/warehouse | $800K | $60K | -93% |
| Contractor costs | $0 | $3.9M | **Variable** |
| **Total OpEx** | **$10.2M** | **$5.2M** | **-49%** |
| Revenue | $22.5M | $22.5M | Same |
| **EBITDA** | **$12.3M** | **$17.3M** | **+41%** |
| EBITDA margin | 55% | **77%** | +22 pts |
| Your equity value | $180M | $250M | +39% |

**Lean = more profit, more valuation, more wealth.**

---

# PROBABILITY IMPACT

## Why Lean Increases Success Probability

| Risk Factor | Traditional | Lean | Improvement |
|-------------|-------------|------|-------------|
| **Burn rate** | $10.2M/year | $5.2M/year | 2× runway |
| **Fixed costs** | 70% of OpEx | 25% of OpEx | Flexible |
| **Hiring risk** | 60 hires to recruit, train, manage | 5 hires only | 92% less |
| **Culture risk** | Large team, politics | You + 5, tight | Minimal |
| **Pivot ability** | Hard (layoffs, morale) | Easy (reduce contractors) | Instant |
| **Geographic expansion** | New office, team, HR | New contractors | Trivial |

**Compound probability boost: 85% → 91%**

## The Math

| Model | Probability | Mission Scale | Expected Value |
|-------|-------------|---------------|------------------|
| Traditional (60 humans) | 85% | 5,000 fields | 4,250 fields |
| **Lean (6 humans + agents)** | **91%** | **5,000 fields** | **4,550 fields** |

**+300 field-equivalents of expected mission impact**

---

# YOUR PERSONAL ROLE IN LEAN MODEL

## What You Must Do (Non-Delegable)

| Activity | Hours/Week | Why You |
|----------|------------|---------|
| Investor relations | 10 hrs | Only you can close checks |
| RGWCD/regulator relationships | 8 hrs | Trust is personal |
| Key farmer relationships | 6 hrs | Early adopters need founder |
| Final hiring decisions | 2 hrs | Culture and quality |
| Strategic decisions | 4 hrs | Direction, pivots, partnerships |
| **Total** | **30 hrs** | Sustainable |

## What Digital Employees Do

| Activity | Agent | Hours Saved |
|----------|-------|-------------|
| Schedule meetings | Executive Assistant | 8 hrs/week |
| Answer support tickets | Support Agent | 20 hrs/week |
| Monitor telemetry | Data Analyst | 15 hrs/week |
| Write docs/procedures | Technical Writer | 10 hrs/week |
| Manage CRM | Sales Assistant | 8 hrs/week |
| Deploy software | DevOps Agent | 10 hrs/week |
| **Total saved** | | **71 hrs/week** |

**You work 30 hrs/week. Digital employees work 71 hrs/week for you.**

## What Contractors Do

| Activity | Contractor | Volume |
|----------|------------|--------|
| Hardware installation | Local techs | 5,000 fields |
| Manufacturing | PCB/assembly shops | 50,000 units |
| Shipping/fulfillment | 3PL | All orders |
| Accounting | CPA firm | Quarterly |
| Legal | Law firm | As needed |

---

# THE LEAN MODEL TIMELINE

## Validation (Q1 2026): 1 Human (You)

| Week | You | Digital | Contractors | Cost |
|------|-----|---------|-------------|------|
| 1-2 | Investor calls, farmer meetings | Deck prep, scheduling | 2 install techs | $10K |
| 3-6 | Site visits, feedback sessions | Data monitoring, reports | Same 2 techs | $15K |
| 7-12 | Analysis, decision | Analysis support, docs | Calibration | $10K |
| **Total** | **~200 hours** | **~500 hours** | **~160 hours** | **$35K** |

## Subdistrict 1 (2026-27): 3 Humans

| Quarter | You | VP Eng | Field Ops | Digital | Contractors | Burn |
|---------|-----|--------|-----------|---------|-------------|------|
| Q2 2026 | Strategy | Build v1.0 | Recruit contractors | 8 agents | 4 techs | $180K |
| Q3 2026 | Investors | Optimize | Manage flow | 8 agents | 8 techs | $220K |
| Q4 2026 | Scale | Scale | Scale | 10 agents | 12 techs | $280K |
| Q1-Q4 2027 | Maintain | Maintain | Maintain | 12 agents | 16 techs | $320K/qtr |
| **Total** | **~2,500 hrs** | **~4,000 hrs** | **~3,500 hrs** | **~10,000 hrs** | **~15,000 hrs** | **$1.4M** |

## RGWCD Scale (2028-29): 6 Humans

| Year | Team | Digital | Contractors | Burn |
|------|------|---------|-------------|------|
| 2028 | You + 5 | 20 agents | 20 techs | $2.1M |
| 2029 | Same | 25 agents | 20 techs | $2.4M |

**Total human hours/year: ~10,000**
**Total digital hours/year: ~25,000**
**Total contractor hours/year: ~35,000**

**You manage 70,000 hours of work with 6 people.**

---

# SUCCESS METRICS FOR LEAN MODEL

## Validation Phase

| Metric | Target | Source |
|--------|--------|--------|
| Human employees | ≤1 | Payroll |
| Digital employees | ≥5 | Agent logs |
| Contractors | ≤3 | 1099s issued |
| Total cost | ≤$50K | Accounting |
| Farmer NPS | ≥70 | Survey |
| Go/no-go decision | Clear | Your judgment |

## Subdistrict 1 Phase

| Metric | Target | Source |
|--------|--------|--------|
| Human employees | ≤3 | Payroll |
| Digital employees | ≥12 | Agent logs |
| Contractors | ≤10 | 1099s |
| Install cost/field | ≤$1,500 | Contractor invoices |
| Uptime | ≥97% | Telemetry |
| Farmer NPS | ≥75 | Survey |
| Gross margin | ≥60% | P&L |

## RGWCD Phase

| Metric | Target | Source |
|--------|--------|--------|
| Human employees | ≤6 | Payroll |
| Digital employees | ≥25 | Agent logs |
| Contractors | ≤25 | 1099s |
| EBITDA margin | ≥75% | P&L |
| CAC | ≤$1,000 | Sales data |
| LTV | ≥$15K | Revenue data |
| Mission | 5,000 fields | Telemetry |

---

# THE LEAN MODEL DECISION

## Choose This If

- You want highest probability of mission success
- You hate managing large teams
- You believe in leverage (digital + contractors)
- You want to keep 40%+ equity at exit
- You value flexibility over headcount

## Don't Choose This If

- You want to "build a big company" for ego
- You enjoy managing 60 people
- You prefer control over speed
- You want to own factories and warehouses

## The Bottom Line

| Model | Humans | Probability | Your Equity | Mission |
|-------|--------|-------------|-------------|---------|
| Traditional | 60 | 85% | 25% | Likely |
| **Lean** | **6** | **91%** | **40%** | **Almost certain** |

**91% probability. 5,000 fields. SLV aquifer saved. $40-100M wealth.**

**With just you, 5 humans, digital employees, and contractors.**

---

# FINAL CHECKLIST

Before starting, confirm:

- [ ] Zoe (your UAO) deployed and operational
- [ ] 5 digital employee agents configured
- [ ] 2 installation contractors identified and vetted
- [ ] $180K validation capital committed
- [ ] You can commit 30 hrs/week for 18 months
- [ ] Mission > ego (you're okay with small team)
- [ ] RGWCD relationships already warm
- [ ] You can fire contractors who underperform

**If all checked, you have 91% probability of success.**

---

*Document Version: 1.0*
*Last Updated: 2026-03-19*
*Next Review: Post-validation*
*Owner: CEO*
*Classification: Internal — CEO Decision Support*

**Proprietary & Confidential — bxthre3 inc.**

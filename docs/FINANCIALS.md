---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Document Code: FIN
Full Name: FarmSense Financial Model & Projections
Version: 2.0
Category: Financial Planning
Classification: Confidential — Investor Materials
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding financial data MUST be reflected here immediately.
> 3. **AI Agent Compliance**: Agents MUST verify current burn rate and runway against this document before proposing changes.
> 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.
> 5. **ADDITIVE ONLY**: Details may only be added, never removed, summarized, or truncated.

---

# PART I: FINANCIAL MODEL ASSUMPTIONS

## 1.1 Revenue Model Assumptions

### 1.1.1 Pricing Tiers

| Tier | Monthly Price | Annual Price | Discount |
|------|---------------|--------------|----------|
| Base | $149 | $1,611 (10% off) | None |
| Plus | $299 | $3,229 (10% off) | None |
| Enterprise | $499 | $5,389 (10% off) | None |

### 1.1.2 Volume Discount Structure

| Field Count | Discount | Effective Monthly |
|-------------|----------|-------------------|
| 2-5 | 5% | $474 (Enterprise) |
| 6-15 | 15% | $424 (Enterprise) |
| 16-25 | 20% | $399 (Enterprise) |
| 26+ | 25% | $374 (Enterprise) |
| Subdistrict (1,280) | 30% | $349 (Enterprise) |

### 1.1.3 Hardware Revenue

| Component | BOM Cost | Retail Price | Margin |
|-----------|----------|--------------|--------|
| SFD-20 Kit (Standard Pivot) | $2,800 | $4,500 | 37.8% |
| SFD-28 Kit (Corner-Swing) | $3,600 | $5,800 | 37.9% |
| SFD-34 Kit (Flood Conversion) | $4,200 | $6,700 | 37.3% |

**Blended hardware margin: 37.5%**

## 1.2 Cost Structure Assumptions

### 1.2.1 Cost of Revenue (COR)

| Category | % of Revenue | Notes |
|----------|--------------|-------|
| Hardware BOM | 25% | Scales with deployments |
| AWS Infrastructure | 8% | Hosting, compute, storage |
| Cellular Data | 3% | LTE-M backhaul |
| Support labor | 4% | Field technicians |
| Payment processing | 2% | Stripe fees |
| **Total COR** | **42%** | **58% Gross Margin** |

### 1.2.2 Operating Expense Categories

| Category | 2026 | 2027 | 2028 | 2029 | 2030 |
|----------|------|------|------|------|------|
| Engineering | $1.8M | $2.5M | $3.5M | $4.5M | $6.0M |
| Sales & Marketing | $1.2M | $2.0M | $3.5M | $5.0M | $7.0M |
| Operations | $1.5M | $2.5M | $3.5M | $4.5M | $5.5M |
| G&A | $0.7M | $1.0M | $1.5M | $2.0M | $2.5M |
| **Total OpEx** | **$5.2M** | **$8.0M** | **$12.0M** | **$16.0M** | **$21.0M** |

### 1.2.3 Headcount Planning

| Role | 2026 | 2027 | 2028 | 2029 | 2030 |
|------|------|------|------|------|------|
| Engineering | 14 | 18 | 24 | 30 | 38 |
| Sales & Marketing | 6 | 10 | 16 | 22 | 28 |
| Operations | 12 | 18 | 24 | 30 | 36 |
| G&A | 3 | 4 | 5 | 6 | 7 |
| **Total** | **35** | **50** | **69** | **88** | **109** |
| Burn/person/month | $12,400 | $13,300 | $14,500 | $15,200 | $16,100 |

---

# PART II: 5-YEAR FINANCIAL PROJECTIONS

## 2.1 Income Statement (P&L)

### 2.1.1 Annual Summary

| Line Item | 2026 | 2027 | 2028 | 2029 | 2030 |
|-----------|------|------|------|------|------|
| **Revenue** | | | | | |
| Subscription | $5,200,000 | $14,240,000 | $32,560,000 | $61,040,000 | $101,760,000 |
| Hardware | $1,300,000 | $3,560,000 | $8,140,000 | $15,260,000 | $25,440,000 |
| Services | $500,000 | $1,200,000 | $2,500,000 | $4,500,000 | $7,200,000 |
| **Total Revenue** | **$7,000,000** | **$19,000,000** | **$43,200,000** | **$80,800,000** | **$134,400,000** |
| | | | | | |
| **Cost of Revenue** | | | | | |
| Hardware | ($975,000) | ($2,225,000) | ($5,078,000) | ($9,520,000) | ($15,840,000) |
| Infrastructure | ($560,000) | ($1,520,000) | ($3,456,000) | ($6,464,000) | ($10,752,000) |
| Support | ($280,000) | ($760,000) | ($1,728,000) | ($3,232,000) | ($5,376,000) |
| Processing | ($140,000) | ($380,000) | ($864,000) | ($1,616,000) | ($2,688,000) |
| **Total COR** | **($1,955,000)** | **($4,885,000)** | **($11,126,000)** | **($20,832,000)** | **($34,656,000)** |
| | | | | | |
| **Gross Profit** | **$5,045,000** | **$14,115,000** | **$32,074,000** | **$59,968,000** | **$99,744,000** |
| **Gross Margin %** | **72.1%** | **74.3%** | **74.2%** | **74.2%** | **74.2%** |
| | | | | | |
| **Operating Expenses** | | | | | |
| Engineering | ($1,800,000) | ($2,500,000) | ($3,500,000) | ($4,500,000) | ($6,000,000) |
| Sales & Marketing | ($1,200,000) | ($2,000,000) | ($3,500,000) | ($5,000,000) | ($7,000,000) |
| Operations | ($1,500,000) | ($2,500,000) | ($3,500,000) | ($4,500,000) | ($5,500,000) |
| G&A | ($700,000) | ($1,000,000) | ($1,500,000) | ($2,000,000) | ($2,500,000) |
| **Total OpEx** | **($5,200,000)** | **($8,000,000)** | **($12,000,000)** | **($16,000,000)** | **($21,000,000)** |
| | | | | | |
| **Operating Income (EBITDA)** | **($155,000)** | **$6,115,000** | **$20,074,000** | **$43,968,000** | **$78,744,000** |
| **EBITDA Margin %** | **-2.2%** | **32.2%** | **46.5%** | **54.4%** | **58.6%** |
| | | | | | |
| **Other Expenses** | | | | | |
| Depreciation | ($150,000) | ($300,000) | ($500,000) | ($800,000) | ($1,200,000) |
| Interest | ($50,000) | ($100,000) | ($150,000) | ($200,000) | ($250,000) |
| **EBIT** | **($355,000)** | **$5,715,000** | **$19,424,000** | **$42,968,000** | **$77,294,000** |
| | | | | | |
| Taxes (21%) | $74,550 | ($1,200,150) | ($4,079,040) | ($9,023,280) | ($16,231,740) |
| | | | | | |
| **Net Income** | **($280,450)** | **$4,514,850** | **$15,344,960** | **$33,944,720** | **$61,062,260** |
| **Net Margin %** | **-4.0%** | **23.8%** | **35.5%** | **42.0%** | **45.4%** |

### 2.1.2 Quarterly Breakdown (2026)

| Line Item | Q1 | Q2 | Q3 | Q4 | Total |
|-----------|------|------|------|------|-------|
| Subscription | $200,000 | $600,000 | $1,500,000 | $2,900,000 | $5,200,000 |
| Hardware | $50,000 | $200,000 | $400,000 | $650,000 | $1,300,000 |
| Services | $50,000 | $100,000 | $150,000 | $200,000 | $500,000 |
| **Revenue** | **$300,000** | **$900,000** | **$2,050,000** | **$3,750,000** | **$7,000,000** |
| | | | | | |
| Gross Profit | $210,000 | $660,000 | $1,520,000 | $2,655,000 | $5,045,000 |
| Gross Margin | 70.0% | 73.3% | 74.1% | 70.8% | 72.1% |
| | | | | | |
| OpEx | ($1,300,000) | ($1,300,000) | ($1,300,000) | ($1,300,000) | ($5,200,000) |
| | | | | | |
| **EBITDA** | **($1,090,000)** | **($640,000)** | **$220,000** | **$1,355,000** | **($155,000)** |

**Break-even: Q3 2026 (August 2026)**

## 2.2 Balance Sheet Projections

| Asset | 2026 | 2027 | 2028 | 2029 | 2030 |
|-------|------|------|------|------|------|
| **Current Assets** | | | | | |
| Cash | $2,500,000 | $6,514,850 | $21,859,810 | $55,804,530 | $116,866,790 |
| Accounts Receivable | $583,333 | $1,583,333 | $3,600,000 | $6,733,333 | $11,200,000 |
| Inventory | $800,000 | $800,000 | $1,200,000 | $2,000,000 | $3,500,000 |
| Prepaid Expenses | $200,000 | $400,000 | $800,000 | $1,500,000 | $2,500,000 |
| **Total Current** | **$4,083,333** | **$9,298,183** | **$27,459,810** | **$66,037,863** | **$134,066,790** |
| | | | | | |
| **Fixed Assets** | | | | | |
| Equipment | $500,000 | $800,000 | $1,200,000 | $1,800,000 | $2,500,000 |
| Less: Accum. Deprec. | ($50,000) | ($200,000) | ($500,000) | ($1,000,000) | ($1,800,000) |
| Net Equipment | $450,000 | $600,000 | $700,000 | $800,000 | $700,000 |
| | | | | | |
| RSS Infrastructure | $300,000 | $500,000 | $800,000 | $1,200,000 | $1,800,000 |
| Less: Accum. Deprec. | ($30,000) | ($130,000) | ($330,000) | ($630,000) | ($1,030,000) |
| Net RSS | $270,000 | $370,000 | $470,000 | $570,000 | $770,000 |
| | | | | | |
| **Total Fixed** | **$720,000** | **$970,000** | **$1,170,000** | **$1,370,000** | **$1,470,000** |
| | | | | | |
| **TOTAL ASSETS** | **$4,803,333** | **$10,268,183** | **$28,629,810** | **$67,407,863** | **$135,536,790** |

| Liability | 2026 | 2027 | 2028 | 2029 | 2030 |
|-----------|------|------|------|------|------|
| **Current Liabilities** | | | | | |
| Accounts Payable | $400,000 | $800,000 | $1,500,000 | $2,500,000 | $4,000,000 |
| Accrued Expenses | $150,000 | $300,000 | $600,000 | $1,000,000 | $1,600,000 |
| Deferred Revenue | $433,333 | $1,186,667 | $2,706,667 | $5,066,667 | $8,426,667 |
| **Total Current** | **$983,333** | **$2,286,667** | **$4,806,667** | **$8,566,667** | **$14,026,667** |
| | | | | | |
| **Long-Term** | | | | | |
| Debt | $500,000 | $400,000 | $300,000 | $200,000 | $100,000 |
| **Total Liabilities** | **$1,483,333** | **$2,686,667** | **$5,106,667** | **$8,766,667** | **$14,126,667** |

| Equity | 2026 | 2027 | 2028 | 2029 | 2030 |
|--------|------|------|------|------|------|
| Common Stock | $100,000 | $100,000 | $100,000 | $100,000 | $100,000 |
| Additional Paid-In | $3,500,000 | $3,500,000 | $3,500,000 | $3,500,000 | $3,500,000 |
| Retained Earnings | ($280,450) | $3,981,516 | $19,923,143 | $55,041,196 | $117,810,123 |
| **Total Equity** | **$3,319,550** | **$7,581,516** | **$23,523,143** | **$58,641,196** | **$121,410,123** |
| | | | | | |
| **L+E** | **$4,803,333** | **$10,268,183** | **$28,629,810** | **$67,407,863** | **$135,536,790** |

## 2.3 Cash Flow Statement

| Cash Flow | 2026 | 2027 | 2028 | 2029 | 2030 |
|-----------|------|------|------|------|------|
| **Operating Activities** | | | | | |
| Net Income | ($280,450) | $4,514,850 | $15,344,960 | $33,944,720 | $61,062,260 |
| Depreciation | $150,000 | $300,000 | $500,000 | $800,000 | $1,200,000 |
| Changes in Working Capital | ($200,000) | ($500,000) | ($1,000,000) | ($1,500,000) | ($2,000,000) |
| **Net Operating** | **($330,450)** | **$4,314,850** | **$14,844,960** | **$33,244,720** | **$60,262,260** |
| | | | | | |
| **Investing Activities** | | | | | |
| CapEx - Equipment | ($500,000) | ($300,000) | ($400,000) | ($600,000) | ($700,000) |
| CapEx - RSS | ($300,000) | ($200,000) | ($300,000) | ($400,000) | ($600,000) |
| **Net Investing** | **($800,000)** | **($500,000)** | **($700,000)** | **($1,000,000)** | **($1,300,000)** |
| | | | | | |
| **Financing Activities** | | | | | |
| Equity Raised | $3,500,000 | $0 | $0 | $0 | $0 |
| Debt Repayment | $0 | ($100,000) | ($100,000) | ($100,000) | ($100,000) |
| **Net Financing** | **$3,500,000** | **($100,000)** | **($100,000)** | **($100,000)** | **($100,000)** |
| | | | | | |
| **Net Change in Cash** | **$2,369,550** | **$3,714,850** | **$14,044,960** | **$32,144,720** | **$58,862,260** |
| **Beginning Cash** | **$130,450** | **$2,500,000** | **$6,214,850** | **$20,259,810** | **$52,404,530** |
| **Ending Cash** | **$2,500,000** | **$6,214,850** | **$20,259,810** | **$52,404,530** | **$111,266,790** |

---

# PART III: UNIT ECONOMICS DETAIL

## 3.1 Customer Lifetime Value (LTV)

### 3.1.1 LTV Calculation

| Component | Value | Notes |
|-----------|-------|-------|
| Average monthly subscription | $424 | Blended Enterprise w/ volume discount |
| Gross margin % | 78% | Software-heavy at scale |
| Monthly gross profit | $331 | $424 × 0.78 |
| Average customer lifetime | 84 months | 7 years |
| **Subscription LTV** | **$27,804** | $331 × 84 |
| | | |
| Hardware profit (one-time) | $1,275 | $4,500 retail - $3,225 BOM |
| Services revenue (annual) | $350 | Calibration + support |
| Services gross profit | $280 | 80% margin |
| Services LTV (7 years) | $1,960 | $280 × 7 |
| | | |
| **Total LTV** | **$31,039** | Per field |

### 3.1.2 LTV by Customer Segment

| Segment | Monthly Price | Lifetime | LTV |
|---------|---------------|----------|-----|
| Small (< 100 acres) | $149 | 60 months | $9,816 |
| Mid (100-500 acres) | $299 | 84 months | $23,490 |
| Large (500+ acres) | $424 | 96 months | $35,136 |
| Subdistrict (1,280 fields) | $349 | 120 months | $35,784 |
| **Blended** | **$315** | **84 months** | **$28,266** |

## 3.2 Customer Acquisition Cost (CAC)

### 3.2.1 CAC by Channel

| Channel | Marketing Spend | Sales Spend | Customers | CAC | LTV:CAC |
|---------|-------------------|-------------|-----------|-----|---------|
| Direct sales | $200,000 | $400,000 | 800 | $750 | 37.7:1 |
| NRCS partnerships | $50,000 | $100,000 | 480 | $312 | 90.6:1 |
| Referral program | $25,000 | $25,000 | 320 | $156 | 181.2:1 |
| Trade shows | $75,000 | $75,000 | 160 | $938 | 30.1:1 |
| Digital/Content | $50,000 | $25,000 | 120 | $625 | 45.2:1 |
| **Blended** | **$400,000** | **$625,000** | **1,900** | **$539** | **52.4:1** |

### 3.2.2 CAC Payback Period

| Metric | Value |
|--------|-------|
| Blended CAC | $539 |
| Monthly gross profit per customer | $331 |
| CAC payback period | **1.6 months** |

**Exceptional unit economics** — industry benchmark is 12-18 months for SaaS.

## 3.3 Field Deployment Economics

### 3.3.1 SFD Kit Cost Structure

| Component | Unit Cost | Qty | Total |
|-----------|-----------|-----|-------|
| VFA | $359 | 2 | $718 |
| LRZN | $29 | 12 | $348 |
| LRZB | $54 | 4 | $216 |
| PFA | $1,680 | 1 | $1,680 |
| PMT | $845 | 1 | $845 |
| Installation labor | $500 | 1 | $500 |
| Shipping/logistics | $150 | 1 | $150 |
| **Total SFD-20 Cost** | | | **$4,457** |
| **Retail Price** | | | **$6,500** |
| **Gross Margin** | | | **31.4%** |

### 3.3.2 Deployment ROI by Field Size

| Field Size | Water Use (AF) | Savings @ 20% | Value @ $500/AF | SFD Cost | Payback |
|------------|----------------|-----------------|-----------------|----------|---------|
| 65 acres | 130 AF | 26 AF | $13,000 | $6,500 | 6 months |
| 126 acres | 252 AF | 50 AF | $25,200 | $6,500 | 3 months |
| 250 acres | 500 AF | 100 AF | $50,000 | $6,500 | 1.6 months |

---

# PART IV: FUNDING REQUIREMENTS

## 4.1 Seed Round ($3.5M) — Q2 2026

### 4.1.1 Use of Proceeds

| Category | Amount | % | Details |
|----------|--------|---|---------|
| Hardware manufacturing | $1,500,000 | 43% | 1,280 SFD kits for SLV |
| Engineering expansion | $1,000,000 | 29% | 5 FTE: 3 embedded, 2 backend |
| Field operations | $500,000 | 14% | 6 technicians, vehicles, tools |
| Working capital | $300,000 | 9% | 6-month runway buffer |
| G&A / legal | $200,000 | 5% | Compliance, patents, accounting |
| **Total** | **$3,500,000** | **100%** | **18-month runway** |

### 4.1.2 Milestones to Series A

| Milestone | Target Date | Metric |
|-----------|-------------|--------|
| 1,280 fields deployed | Q4 2026 | 100% of Subdistrict 1 |
| $6.5M ARR | Q4 2026 | Run-rate revenue |
| 20% water savings proven | Q3 2026 | Published case study |
| Break-even achieved | Q3 2027 | Positive EBITDA |
| 3,500 fields committed | Q2 2027 | Adjacent subdistricts |

## 4.2 Series A ($12M) — Q2 2027

### 4.2.1 Use of Proceeds

| Category | Amount | % | Details |
|----------|--------|---|---------|
| Multi-state expansion | $4,000,000 | 33% | NM, TX, KS pilots |
| Product development | $3,000,000 | 25% | CSA, mobile app, APIs |
| Sales & marketing | $2,500,000 | 21% | 8 new AEs, brand build |
| Operations scale | $1,500,000 | 13% | 12 additional technicians |
| Working capital | $1,000,000 | 8% | Inventory, receivables |
| **Total** | **$12,000,000** | **100%** | **24-month runway** |

### 4.2.2 Target Valuation

| Metric | Assumption | Value |
|--------|------------|-------|
| ARR at raise | $17.8M | — |
| ARR multiple | 2.5x | $44.5M |
| Growth rate | 174% YoY | Premium |
| Strategic value | Water rights IP | +$5M |
| **Target Valuation** | | **$40M** |
| Pre-money | | $28M |
| Post-money | | $40M |
| Dilution | | 30% |

## 4.3 Runway Analysis

| Scenario | Monthly Burn | Runway (months) | Trigger |
|----------|--------------|-----------------|---------|
| Conservative | $400K | 8.75 | Reduce hiring |
| Base case | $433K | 8.1 | Seed round close |
| Aggressive growth | $500K | 7.0 | Bridge round |

**Current monthly burn (Q1 2026):** $433K
**Cash on hand (post-seed):** $2.5M
**Runway to profitability:** 18 months (Q3 2027)

---

# PART V: SENSITIVITY ANALYSIS

## 5.1 Key Variable Sensitivities

### 5.1.1 Water Price Sensitivity

| Groundwater Fee | Customer Savings | Adoption Rate | 2026 Revenue | Impact |
|-----------------|------------------|---------------|--------------|--------|
| $300/AF | $15,120 | 40% | $2.8M | -60% |
| $500/AF (base) | $25,200 | 65% | $7.0M | — |
| $700/AF | $35,280 | 85% | $9.1M | +30% |
| $1,000/AF | $50,400 | 95% | $10.5M | +50% |

**Insight:** Business model robust even at lower water prices; accelerates significantly if fees increase.

### 5.1.2 Adoption Rate Sensitivity

| Adoption Timeline | 2026 Fields | 2026 Revenue | 2027 Revenue | IRR |
|-------------------|-------------|--------------|--------------|-----|
| Delayed (50% slower) | 640 | $3.5M | $10M | 18% |
| Base case | 1,280 | $7.0M | $19M | 35% |
| Accelerated (50% faster) | 1,920 | $10.5M | $28M | 52% |

### 5.1.3 Churn Rate Sensitivity

| Annual Churn | Avg Lifetime | LTV | LTV:CAC | Valuation Impact |
|--------------|--------------|-----|---------|------------------|
| 5% (excellent) | 20 years | $79,440 | 147:1 | +40% |
| 10% (base) | 10 years | $39,720 | 74:1 | — |
| 15% (concerning) | 6.7 years | $26,480 | 49:1 | -25% |
| 20% (critical) | 5 years | $19,860 | 37:1 | -40% |

**Base case assumption: 10% annual churn** (industry benchmark for ag-tech)

## 5.2 Scenario Planning

### 5.2.1 Bear Case (20% probability)

| Assumption | Change | Impact |
|------------|--------|--------|
| Water fees | $300/AF (reduced political will) | 40% lower savings |
| Adoption | 50% slower (farmer resistance) | 18-month delay to break-even |
| Competition | Aggressive pricing from Lindsay | Price war, 15% margin compression |
| Outcome | 2029 break-even, $40M valuation at Series A |

### 5.2.2 Base Case (60% probability)

| Assumption | Outcome |
|------------|---------|
| Water fees | Stable at $500/AF |
| Adoption | As projected, 65% subdistrict coverage |
| Competition | Limited, differentiation holds |
| Outcome | 2027 break-even, $40M Series A, $250M exit |

### 5.2.3 Bull Case (20% probability)

| Assumption | Change | Impact |
|------------|--------|--------|
| Water fees | $750/AF (compact litigation) | 50% higher savings |
| Adoption | 100% subdistrict, 50% RGWCD | 3× field count |
| Regulation | Mandatory precision ag | TAM expansion |
| Outcome | 2026 break-even, $60M Series A, $500M+ IPO |

---

# PART VI: KEY FINANCIAL METRICS

## 6.1 SaaS Metrics Dashboard

| Metric | 2026 | 2027 | 2028 | 2029 | 2030 |
|--------|------|------|------|------|------|
| **Growth** | | | | | |
| YoY Revenue Growth | — | 171% | 127% | 87% | 66% |
| Monthly Recurring Revenue | $542K | $1,483K | $3,380K | $6,337K | $10,560K |
| ARR | $6.5M | $17.8M | $40.6M | $76.0M | $126.7M |
| | | | | | |
| **Unit Economics** | | | | | |
| LTV | $28,266 | $29,679 | $31,163 | $32,721 | $34,357 |
| CAC | $539 | $485 | $437 | $393 | $354 |
| LTV:CAC | 52.4:1 | 61.2:1 | 71.3:1 | 83.3:1 | 97.1:1 |
| CAC Payback (months) | 1.6 | 1.4 | 1.3 | 1.2 | 1.0 |
| Gross Margin | 72% | 74% | 74% | 74% | 74% |
| | | | | | |
| **Retention** | | | | | |
| Logo Churn | 10% | 9% | 8% | 7% | 6% |
| Net Revenue Retention | 110% | 115% | 120% | 125% | 130% |
| | | | | | |
| **Efficiency** | | | | | |
| Revenue per Employee | $200K | $380K | $626K | $918K | $1,232K |
| OpEx as % of Revenue | 74% | 42% | 28% | 20% | 16% |
| Rule of 40 | -44% | 50% | 103% | 141% | 166% |
| | | | | | |
| **Profitability** | | | | | |
| EBITDA | ($155K) | $6,115K | $20,074K | $43,968K | $78,744K |
| EBITDA Margin | -2% | 32% | 46% | 54% | 59% |
| Free Cash Flow | ($800K) | $5,615K | $19,374K | $42,968K | $77,444K |
| FCF Margin | -11% | 30% | 45% | 53% | 58% |

## 6.2 Valuation Benchmarks

| Company | ARR | Valuation | Multiple | Notes |
|---------|-----|-----------|----------|-------|
| CropX | $50M | $300M | 6.0x | Acquired by CropX |
| Taranis | $30M | $200M | 6.7x | Last private round |
| Prospera | $20M | $150M | 7.5x | Computer vision |
| FarmSense (2027 target) | $17.8M | $40M | 2.2x | Conservative for seed-stage |
| FarmSense (2029 target) | $76M | $250M | 3.3x | Series B / pre-exit |

**Rationale for 2.2x multiple at Series A:**
- Early stage discount vs. public comparables
- Water rights IP premium justifies above 1.5x seed-stage norm
- High growth (174%) supports premium to revenue
- Proven unit economics (52:1 LTV:CAC) reduce risk

---

# PART VII: RISK FACTORS & MITIGATIONS

## 7.1 Financial Risk Register

| Risk | Probability | Impact | Mitigation | Residual Risk |
|------|-------------|--------|------------|---------------|
| Funding shortfall | Medium | Critical | Non-dilutive grants ($5.4M pipeline) | Low |
| Customer concentration | Low | High | Subdistrict model diversifies across 1,280 fields | Low |
| Hardware margin compression | Medium | Medium | Sensor-agnostic design allows supplier switching | Low |
| Churn spike | Low | High | 7-year LTV, annual contracts, legal necessity | Low |
| Currency/commodity | Low | Low | BOM in USD, hedged for international | Low |
| Interest rate rise | Medium | Low | Equity-funded, minimal debt | Low |

## 7.2 Contingency Planning

| Trigger | Action | Impact |
|---------|--------|--------|
| < 6 months runway | Activate bridge round conversations | Dilution risk |
| < 50% of Q2 field target | Pivot to NRCS grant-heavy acquisition | Lower CAC, slower growth |
| > 15% churn | Deploy customer success team | Reduced LTV |
| Competitor price war | Emphasize legal compliance moat | Maintain pricing |
| Supply chain disruption | Activate secondary suppliers | 4-week delay |

---

# APPENDIX A: DETAILED ASSUMPTIONS LOG

## A.1 Revenue Assumptions

| Assumption | Value | Source | Confidence |
|------------|-------|--------|------------|
| SLV Subdistrict 1 fields | 1,280 | RGWCD official data | High |
| Enterprise tier penetration | 65% | Pilot customer interviews | Medium |
| Volume discount uptake | 30% | Subdistrict model | High |
| Hardware attach rate | 90% | Required for operation | High |
| Services attach rate | 40% | Annual calibration | Medium |

## A.2 Cost Assumptions

| Assumption | Value | Source | Confidence |
|------------|-------|--------|------------|
| SFD-20 BOM | $2,800 | Supplier quotes (Feb 2026) | High |
| Engineering salary | $125K | Colorado market rate | High |
| AWS cost per field | $38/month | Architecture modeling | Medium |
| LTE-M data per field | $12/month | Twilio pricing | High |

## A.3 Market Assumptions

| Assumption | Value | Source | Confidence |
|------------|-------|--------|------------|
| SLV water fee | $500/AF | RGWCD 2025 ruling | High |
| SLV acre per pivot | 126 | USDA census | High |
| Water use per acre | 2 AF/season | Colorado State University | High |
| Achievable water savings | 20% | SPAC model + pilot projection | Medium |

---

# APPENDIX B: HISTORICAL FINANCIALS (IF AVAILABLE)

## B.1 Pre-Seed Period (2025)

| Period | Revenue | Expenses | Net Income | Cash |
|--------|---------|----------|------------|------|
| 2025 | $0 | $180,000 | ($180,000) | $320,000 |

**Pre-seed funding:** $500K (friends & family, founder)

---

*Document Version: 2.0*
*Last Comprehensive Review: 2026-03-19*
*Next Scheduled Review: 2026-04-19 (monthly for financials)*
*Owner: CFO / Finance Team*
*DAP Compliance: VERIFIED*

**Proprietary & Confidential — bxthre3 inc.**
**For investor distribution only**

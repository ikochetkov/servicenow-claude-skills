# ITSM (IT Service Management) Pricing & Packaging

## Overview
ITSM provides incident, problem, change, request, and asset management capabilities. Licensed by **Fulfiller** (per agent) or **Unrestricted User** (all active users) models.

---

## ITSM Pricing Models

### Fulfiller Model (Role-Based)
- **Requester**: Submits requests - no subscription required
- **Business Stakeholder**: Approves, views records/reports - $35/user (PROD17800)
- **Fulfiller**: Works on/fulfills requests - requires product subscription

### Unrestricted User Model
- Every active user in sys_user table
- Full rights subscription required
- **Restricted SKU** - requires Partner Ops approval

---

## ITSM Package Tiers (Q4 2025)

### ITSM Standard v3 - $100/Fulfiller or $15/UU (PROD17243/PROD17252)
**Includes:**
- Incident Management
- Problem Management
- Change Management
- Cost Management
- Asset Management
- Request Management
- Walk-Up Experience
- Digital Portfolio Management
- Universal Request
- App Engine Starter (25 tables)

### ITSM Professional v3 - $150/Fulfiller or $20/UU (PROD17256/PROD17257)
**Includes ITSM Standard plus:**
- Performance Analytics Advanced
- Digital Product Release
- Virtual Agent (1000 conversations/Fulfiller/month)
- Predictive Intelligence
- Continual Improvement Management
- Mobile Publishing
- DevOps Change Velocity
- Universal Request Pro
- App Engine Starter (50 tables)

### ITSM Enterprise v3 - $225/Fulfiller or $30/UU (PROD17259/PROD17269)
**Includes ITSM Professional plus:**
- Process Mining
- Workforce Optimization
- App Engine Starter (50 tables)

---

## Now Assist for ITSM

### ITSM Pro Plus / Enterprise Plus - $90/Fulfiller or $12/UU
- PROD21190/PROD21191 (Pro Plus)
- PROD21192/PROD21193 (Enterprise Plus)

**Assist Entitlements:**
- 6,000 Assists per Fulfiller per year
- 800 Assists per Unrestricted User per year

**Included Capabilities:**

| Generative AI Skills | AI Agents |
|---------------------|-----------|
| Now Assist in Virtual Agent with ITSM LLM Topics | Incident resolution agents |
| Chat Summarization | SecOps Metrics Agent |
| Chat Reply Recommendations | Shift Handover Agent |
| Incident Summarization | Incident Wrap-up Agent |
| Resolution Note Generation | |
| Knowledge Generation | |
| Change Summarization | |
| Change Risk Explanation | |

**Assist Consumption by Task:**
| Task Type | Assists |
|-----------|---------|
| Agent summarization | 1 |
| Email reply recommendation | 5 |
| VA conversation | 10 |
| Contract analysis | 50 |
| AI agent task (small, up to 4 actions) | 25 |
| AI agent task (medium, 5-8 actions) | 50 |
| AI agent task (large, 9-20 actions) | 150 |

**Licensing Rules:**
- Fulfiller customers: minimum 25 licenses
- UU customers: cannot purchase subset, but can buy on Fulfiller meter (min 25)
- Pro Plus requires ITSM Pro base SKU
- Enterprise Plus requires ITSM Enterprise base SKU

---

## Digital End-User Experience (DEX)

### DEX v2 - $24/Subscription Unit (PROD22260)
**Subscription Unit Ratio:**
- 4 End-User Computing Devices = 1 SU

**Includes:**
- Agent Client Collector for Visibility
- Event Management
- DEX Score
- Proactive Engagement
- Investigation Framework

**Limits:**
- End-User Computing Devices: 1,000 - 400,000 (250 - 100,000 SUs)
- MetricBase Series limit controlled by data collection policies
- Active Applications monitoring limits per documentation

**Prerequisites:**
- ITSM Standard or equivalent (including CSM/Industry packages with ITSM)
- ITSM Pro required for NLU-powered Virtual Agent in Desktop Assistant
- ITSM Pro Plus required for Now Assist powered Virtual Agent

---

## Add-On Products

### Business Stakeholder v4 - $35/User (PROD17800)
- Approve any record, view record details
- View any report or record
- Update comments to incidents/requests on behalf of users
- Available for: ITSM, DevOps, SPM/ITBM, CSM, TSM, FSO, PSDS, TPSM, HCLS-SM, App Engine

### App Engine for ITSM - 20% of ITSM Fulfiller Spend (PROD13079)
- Unlimited custom tables for ITSM
- Only available for Fulfiller model
- Cannot be discounted

### Workforce Optimization Add-Ons (ITSM Pro)
| SKU | Price | Product ID |
|-----|-------|-----------|
| WFO for ITSM Pro (% ACV) | 30% of ITSM Pro ACV | PROD18591/PROD18592 |
| WFO for ITSM Pro (Per User) | $75/Application User | PROD22124 (Restricted) |

### Process Mining Add-Ons (ITSM Pro)
| SKU | Price | Product ID |
|-----|-------|-----------|
| PM for ITSM Pro | 20% of ITSM Pro ACV | PROD18593/PROD18595 |
| Process and Task Mining | $125K/Year | PROD23563 |

---

## Virtual Agent Details

### Included in ITSM Pro
- 1,000 ITSM Conversation Transactions per Fulfiller per month
- Conversations NOT shared across product lines
- Unlimited conversations in Unrestricted model

### Additional Transactions
- Virtual Agent Additional Transactions Pack: $25K per 4,000 conversations (PROD09218)

### VA Lite (ITSM Standard)
- Limited version for Standard customers
- Includes: Report IT Issue, Check Status, Search Knowledge
- Keywords only (no NLU)
- Cannot create new conversations

---

## Service Operations Workspace

- Available to all ITSM SKUs (Std/Pro/Ent) including legacy SKUs
- NOT a separate SKU - included with ITSM licenses
- ITOM customers need separate ITSM licenses

**Key Features:**
- Incident management with contextual information
- Investigation and root cause analysis
- Experts on-call
- Collaboration tools
- Recommendations for investigation
- Alert management

---

## Deprecation Notes

### Deprecated Applications
- **Vendor Manager Workspace**: EOL started May 2025, removed Q4 Store release
- **Release Management**: EOL started Xanadu GA (Sep 2024), replaced by Digital Product Release

### Migration Path
- Release Management users should migrate to Digital Product Release (DPR)
- DPR available in ITSM Pro and Enterprise packages
- Utilities available for migration (some manual steps may be required)

---

## Digital Portfolio Management

- Included in ITSM Std/Pro/Ent at no additional cost
- Also included in SPM Std/Pro, ITBM Std/Pro, and APM
- Shared capability for managing services, applications, and products lifecycle

**Key Features:**
- Enterprise Portfolios
- Personal Portfolios
- Roadmap Planning
- Service Impacts visibility

**Licensing:**
- Read access: Free across ITSM, SPM/ITBM, APM
- Write access: Requires license for specific product tables

---

## Integration Hub

### Integration Hub Starter v4 - $0 (PROD22417)
- Paired when customers don't purchase paid Integration Hub/Automation Engine
- 100,000 transactions annually
- Pre-built Spokes and Templates (Starter list)

**Notes:**
- Cannot be paired with Automation Engine Pro/Enterprise
- Custom spokes NOT available
- Must migrate to paid IH for additional transactions

---

## Pricing Summary

| Product | Fulfiller Price | UU Price | Product ID |
|---------|----------------|----------|------------|
| ITSM Standard v3 | $100/month | $15/month | PROD17243/PROD17252 |
| ITSM Professional v3 | $150/month | $20/month | PROD17256/PROD17257 |
| ITSM Enterprise v3 | $225/month | $30/month | PROD17259/PROD17269 |
| ITSM Pro Plus | $90/month | $12/month | PROD21190/PROD21191 |
| ITSM Enterprise Plus | $90/month | $12/month | PROD21192/PROD21193 |
| Business Stakeholder v4 | $35/user | - | PROD17800 |
| DEX v2 | $24/SU | - | PROD22260 |

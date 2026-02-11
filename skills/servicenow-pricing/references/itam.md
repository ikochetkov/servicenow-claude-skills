# IT Asset Management (ITAM) Pricing & Packaging

## Overview
ITAM includes Software Asset Management (SAM), Hardware Asset Management (HAM), Cloud Cost Management (CCM), Enterprise Asset Management (EAM), and OT Asset Management. Licensed by **Subscription Units (SU)** based on managed resources.

---

## Software Asset Management (SAM)

### SAM Pricing Models
Licensed by Subscription Units (SU):
| Resource Type | SU Ratio |
|--------------|----------|
| Server | 1:1 |
| End User Computing Device | 4:1 |
| SaaS Subscription User | 15:1 |
| IaaS Resources (Enterprise only) | 3:1 |
| PaaS Resources (Enterprise only) | 3:1 |

Managed devices: Those with software install discovered in past 90 days or empty discovered date.

### SAM Professional - $8/SU (PROD15033)
**Includes:**
- Asset Management
- Client Software Distribution for SAM (reclamation only)
- Platform Analytics Advanced
- Predictive Intelligence
- Software Asset Management
- Software Spend Detection
- Service Graph Connectors (SCCM, Workspace One, Intune, JAMF only)
- App Engine Starter (5 tables)
- SBOM Core
- Data Model for SBOM

**Min ACV Guidance:** $45K

### SAM Enterprise - $12/SU (PROD24723)
**Includes SAM Professional plus:**
- Coupa Procurement Integration
- ML Normalization
- Cloud License Simulator
- Cloud Cost Management
- SaaS License Management Connections
- IaaS/PaaS resource management (Vancouver+)

### SAM Pro Plus / Enterprise Plus - $5/SU (PROD25499/PROD25450)
**Assist Limit:** 350/SU/year (shareable)

**Included Capabilities:**
| Generative AI | Agentic AI |
|--------------|------------|
| Publisher Compliance Summarization | Manage Software Asset Requests |
| Product Compliance Summarization | Create Software Reclamation Rule |
| Recommended Actions | Evaluate Software Removal Candidates |
| Now Assist for CMDB | SaaS User Resolution |
| Now Assist for SGC | |
| DocIntel | |

---

## Hardware Asset Management (HAM)

### HAM Subscription Unit Ratios
| Resource Type | SU Ratio |
|--------------|----------|
| Server | 1:1 |
| Unclassified Hardware | 1:1 |
| Storage | 3:1 |
| End User Computing Devices | 4:1 |
| Network Devices | 5:1 |
| Mobile Devices | 10:1 |
| Printers | 10:1 |
| Monitors | 15:1 |

### HAM Professional v6 - $6/SU (PROD23841)
**Includes:**
- Asset Management
- Hardware Asset Management
- Platform Analytics Advanced
- Predictive Intelligence
- Hardware Asset Management for DaaS
- Service Graph Connectors
- Bundled Custom Tables (5)

### HAM Professional Plus - $3.60/SU (PROD26247)
**Assist Limit:** 250/SU/year (shareable)

**Included Capabilities:**
| Generative AI | Agentic AI |
|--------------|------------|
| Now Assist for HAM | Manage Hardware Asset Requests |
| Now Assist for CMDB | Asset Repair |
| Now Assist for SGC | |
| DocIntel | |

---

## ITAM for Financial Services

### ITAM for Financial Services - $4/SU (PROD26855)
**Add-on requiring SAM Pro/Enterprise or HAM Professional**

**Includes:**
- App Engine Starter
- Asset Audit Response
- Policy and Compliance Management
- Audit Management
- Advanced Core
- Platform Analytics Advanced
- Predictive Intelligence

**Use Cases:**
- Regulatory audit response (FFIEC, NYDFS, DORA)
- Evidence request management
- Asset and Risk collaboration

**Same SU Ratios as HAM**

---

## Cloud Cost Management (CCM)

### CCM Subscription Unit Ratios
| Resource Type | SU Ratio |
|--------------|----------|
| Server | 1:1 |
| IaaS Resources | 3:1 |
| PaaS Resources | 3:1 |

- Servers include virtual machines in AWS, Azure, GCP
- IaaS includes Storage Volumes
- PaaS includes Databases

### CCM Professional - $8/SU (PROD24727)
**Includes:**
- Cloud Cost Management
- Platform Analytics Advanced
- Predictive Intelligence
- Bundled Custom Tables (5)

**Min ACV Guidance:** $45K

**Important:** CCM Pro CANNOT be combined with SAM Pro. Upgrade path is SAM Enterprise.

### Legacy Cloud Insights Migration - $0 (PROD15043)
- Migration-only SKU for customers moving from legacy ITOM

---

## Enterprise Asset Management (EAM)

### EAM Subscription Unit Ratios
| Resource Type | SU Ratio |
|--------------|----------|
| Consumables | 25:1 |
| Simple Assets | 5:1 |
| Parent Assets | 1:1 |
| Linear Assets | 1:1 |
| Linear Asset Segments | 2:1 |

### EAM Professional v3 - $12/SU (PROD23593)
**Includes:**
- Enterprise Asset Management
- Asset Management
- App Engine Starter (5 tables)
- Planned Maintenance
- Predictive Intelligence
- Platform Analytics Advanced

### EAM Add-On SKUs

| SKU | Price | Product ID |
|-----|-------|-----------|
| EAM Field Service Technician | $35/Fulfiller | PROD19381 |
| Indoor Mapping Service | $100/Floor | PROD22878 |

**EAM Field Service Technician:**
- Required for Work Order Tasks in Workspace and Agent Mobile
- Not required if entitled to FSM Standard/Pro/Enterprise

---

## OT Asset Management (OTAM)

### OTAM Subscription Unit Ratios
| Resource Type | SU Ratio |
|--------------|----------|
| OT Supervisory System | 1:1 |
| OT Control System | 3:1 |
| OT Field Devices | 10:1 |
| OT End User Computers | 4:1 |
| OT Mobile Devices | 10:1 |
| OT Monitors | 15:1 |
| OT Network Gear | 5:1 |
| OT Printer | 10:1 |
| OT Servers | 1:1 |
| OT Storage | 3:1 |
| Operational Equipment | 1:1 |
| Industrial Consumable | 25:1 |
| Unclassed OT | 1:1 |
| Unclassed Hardware | 1:1 |

### OT Asset Management v2 - $10,000/Industrial Site (PROD25305)
**Includes:**
- Asset Management
- Hardware Asset Management (Limited)
- 5,000 OT Devices/OE Assets default
- OT Obsolescence Management
- Operational Technology Asset Management
- Planned Maintenance
- Predictive Intelligence
- Platform Analytics Advanced
- App Engine Starter (5 tables)

### OTAM Add-On SKUs

| SKU | Price | Product ID |
|-----|-------|-----------|
| EAM Field Service Technician | $35/Fulfiller | PROD19381 |
| Indoor Mapping Service | $100/Floor | PROD22878 |
| OT Max Devices Pack | $2,000/1,000 devices | PROD25251 |

---

## Telecommunications & Data Center

### Telecom Network Inventory (TNI) - $24/SU (PROD22246)
**SU Ratios:**
- 3 Servers = 1 SU
- 15 Network Devices = 1 SU
- 15 Sites = 1 SU
- 15 Managed Functions = 1 SU

**Includes:**
- Network Inventory Core
- Network Inventory Advanced
- Hardware Asset Management for TNI
- Predictive Intelligence
- Platform Analytics Advanced

**Requires:** At least 1 FF subscription for TSM/TPSM (or ITSM, CSM) for Change Management access

### Data Center & Network Asset Management (DCNAM) Professional - $24/SU (PROD27966)
**SU Ratios:**
- 3 Servers = 1 SU
- 15 Network Devices = 1 SU
- 15 Racks/Cabinets = 1 SU
- 15 Data Centers = 1 SU
- 50 Cables = 1 SU
- 10 Facility Assets = 1 SU

**Includes:**
- Enterprise Asset Management for DCNAM
- Hardware Asset Management for TNI
- Network Inventory Advanced
- Network Inventory Core
- Predictive Intelligence
- Platform Analytics Advanced

### DCNAM Professional Plus - $14.40/SU (PROD27968)
**Assist Limit:** 1000/SU/year (shareable)

**Includes:**
- Now Assist for HAM
- Manage Hardware Asset Requests (AI Agent)
- Asset Repair (AI Agent)
- Now Assist for CMDB
- Now Assist for SGC

---

## Integration Hub Considerations

- Starting Utah, Automation Engine may charge for transactions
- SaaS License Management calls via spokes may be impacted
- Integration Hub SKU may be required for outbound transactions
- Existing customers can download Integration Hub Usage Dashboard to estimate volume
- Transactions from included Spokes count as Integration Hub Transactions and require Automation Engine license

---

## Self-Tracking License Consumption

Customers can track license consumption:
1. Navigate to ITAM Licensing > ITAM License Report
2. View aggregated counts of EUC, Servers, Databases, Storage Volumes, Subscription Users
3. Click on records to see related list of all resources included in metric counts

---

## Pricing Summary Table

| Product | Price | Product ID |
|---------|-------|-----------|
| SAM Professional | $8/SU | PROD15033 |
| SAM Enterprise | $12/SU | PROD24723 |
| SAM Pro/Ent Plus | $5/SU | PROD25499/PROD25450 |
| HAM Professional v6 | $6/SU | PROD23841 |
| HAM Pro Plus | $3.60/SU | PROD26247 |
| ITAM for Financial Services | $4/SU | PROD26855 |
| CCM Professional | $8/SU | PROD24727 |
| EAM Professional v3 | $12/SU | PROD23593 |
| OT Asset Management v2 | $10,000/site | PROD25305 |
| TNI | $24/SU | PROD22246 |
| DCNAM Professional | $24/SU | PROD27966 |
| DCNAM Pro Plus | $14.40/SU | PROD27968 |
| Indoor Mapping Service | $100/Floor | PROD22878 |

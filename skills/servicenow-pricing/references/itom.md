# ITOM (IT Operations Management) Pricing & Packaging

## Overview
ITOM provides visibility, health monitoring, and cloud management for IT infrastructure. Licensed by **Subscription Units (SUs)** based on managed resources.

---

## ITOM Packaging Hierarchy (Q4 2025)

### ITOM AIOps Enterprise v3 - $42/SU/month (PROD25358)
**Includes everything in AIOps Professional plus:**
- Health Log Analytics (HLA)
- ITOM Observability (Service Observability, Synthetic Monitoring)
- Cloud Accelerate (Cloud Services Catalog, Cloud Configuration Governance, Cloud Migration Assessment, Cloud Action Library, Cloud Account Management)

**Available Add-Ons:**
- ITOM Enterprise Plus (PROD22524) - $14/SU/month - Now Assist for ITOM
- Now Assist for CMDB
- Now Assist for SGCs
- API Insights (PROD25492) - $12/SU/month

### ITOM AIOps Professional v2 - $24/SU/month (PROD14995)
**Includes Now Platform, Visibility plus:**
- Platform Analytics Advanced
- Full Predictive Intelligence
- ITOM Health (Event Management, Metric Intelligence)
- ACC for Monitoring
- Service Level Objective Management
- Service Reliability Management
- Spokes & Protocols (Jenkins, MS Active Directory v2, MS Azure AD, MS SCCM, Kubernetes, F5; PowerShell, SSH)

**Available Add-Ons:**
- ITOM Professional Plus (PROD22521) - $14/SU/month - Now Assist for ITOM
- Cloud Accelerate (PROD16960) - $8/SU/month
- Health Log Analytics (PROD16964) - $14/SU/month
- API Insights (PROD25492) - $12/SU/month

### ITOM Visibility v2 - $12/SU/month (PROD14997)
**Includes Now Platform plus:**
- Agentless Discovery
- ACC for Visibility
- Service Graph Connectors
- CMDB 360 (Multisource)
- Service Mapping
- Tag Governance
- TLS Certificate Inventory & Management
- Firewall Audits & Reporting

**Available Add-Ons:**
- Cloud Accelerate (PROD16960) - $8/SU/month
- API Insights (PROD25492) - $12/SU/month

### ITOM Discovery v2 - $8/SU/month (PROD15000)
- Agentless Discovery only
- Restricted SKU (not recommended, use Visibility instead)

### ITOM Health v2 - $14/SU/month (PROD14998)
- Event Management
- Metric Intelligence
- ACC for Monitoring
- Restricted SKU (use AIOps Professional instead)

---

## Subscription Units (SU) Definition

| Resource Type | SU Ratio |
|--------------|----------|
| Server / Virtual Server | 1:1 |
| PaaS Resources | 3:1 |
| Functions as a Service (FaaS) | 20:1 |
| Containers | 10:1 |
| End User Devices* | 4:1 |
| Unresolved Monitored Objects** | 4:1 |

*Only where an ITOM component is deployed
**IT resources receiving health data but not resolved to CMDB CI

### CMDB Classes for SU Counting
- **Servers**: cmdb_ci_server, cmdb_ci_vm_instance, cmdb_ci_ucs_rack_unit, cmdb_ci_ucs_blade, cmdb_ci_mainframe_hardware
- **Containers**: cmdb_ci_oslv_container
- **PaaS**: cmdb_ci_cloud_appserver, cmdb_ci_cloud_database, cmdb_ci_dynamodb_table, cmdb_ci_cloud_directory, cmdb_ci_cloud_gateway, cmdb_ci_cloud_messaging_service, cmdb_ci_cloud_webserver
- **FaaS**: cmdb_ci_cloud_function
- **End User Devices**: cmdb_ci_computer

---

## Alternate SKU Variations

### TSOM (Telecom Service Operations) SKUs
Additional SU categories:
- Networking Devices: 25:1
- Customer Premises Devices: 250:1
- IoT: 40:1

### OT (Operational Technology) SKUs
Now exclusively metered by **Industrial Site** (not SU):
- OT Supervisory System: 1:1
- OT Control System: 3:1
- OT Field Device: 10:1

**Important**: ITOM, TSOM, and IoT SKUs cannot be mixed. OT SKUs must be combined with one of the others.

---

## Now Assist for ITOM Pricing

### ITOM Professional Plus / Enterprise Plus - $14/SU/month
- Requires equal SU capacity in base Pro/Ent SKU
- Includes 1000 Assists/year/SU (shareable across products)

**Eligible Base SKUs:**
- ITOM AIOps Professional
- ITOM AIOps Enterprise
- TSOM Professional/Enterprise

**Included Capabilities:**

| Generative AI | Agentic AI |
|--------------|------------|
| Now Assist for ITOM: Alert analysis (1 Assist), Alert investigation (1 Assist) | AIOps LEAP: Cluster/topic creation, topic prioritization, resolution note generation (25-125 Assists) |
| Now Assist for CMDB: CI summarization, manage duplicate CIs (5 Assists per duplicate) | Automation playbook creation (2500 Assists, requires Text-to-Flow) |
| Now Assist for SGCs: SGC diagnosis (5 Assists per error/problem) | Agentic Workflow: Triage alert (25), Analyze alert impact (25-50), Change impact (25), Certificate renewal (25) |

---

## Key Add-On Products

### Health Log Analytics (HLA) - $14/SU/month (PROD16964)
- Add-on to ITOM Health v2 or ITOM AIOps Professional
- Requires Health SU capacity >= HLA SU capacity
- **Not available for on-prem or Azure regulated markets**
- Provides automated log anomaly detection

### ITOM Observability (included in Enterprise v3)
- Service Observability: Service operational conditions for L1 operators
- Synthetic Monitoring: Monitor HTTP/API endpoints proactively

### Cloud Accelerate - $8/SU/month (PROD16960)
- Requires ITOM Visibility
- Cloud Services Catalog
- Cloud Configuration Governance
- Cloud Migration Assessment
- Cloud Action Library
- Cloud Account Management (requires Cloud Governance Suite SKU)

### Cloud Governance Suite - $50K flat price
- Prerequisite for Cloud Account Management
- No discounting
- Provides Cloud Workspace access

### API Insights v2 - $12/SU/month (PROD25492)
- cGTM SKU (requires approval from Ravi Bansal)
- API Workspace and API Service Graph Connectors
- 1:1 SU ratio for APIs

---

## SU Consumption Rules

### Counting Logic
1. **90-day rolling average** of daily resource counts
2. **Unique superset** - using multiple features on one resource = 1 SU
3. **Bundles first, highwater mark** - highest consumption in bundle sets level

### Visibility Counting Criteria
1. CI discovered by SN Discovery, ACC-V, SN/Partner SGCs
2. Most Recent Discovery within 90 days
3. Duplicate_of field is empty
4. Install Status not retired/stolen/absent
5. Excludes VM instances with virtualization relationships, VDIs

### Health Counting Criteria
1. CIs linked to alerts via ITOM AIOps or ACC-Monitoring
2. Alerts created within past 365 days
3. Same deduplication rules as Visibility

---

## Migration Guidance

### Node to SU Migration
- Node and SU pricing cannot be mixed
- Use ITOM SU Licensing store app to estimate SU counts
- Consider ACC on end user devices increases SU count

### Key Migration Paths

| From | To | Price Impact |
|------|-----|-------------|
| Discovery Node | ITOM Visibility v2 | +50% |
| Event Management Node | ITOM AIOps Professional v2 | Uplift |
| ServiceWatch Suite | ITOM AIOps Enterprise v3 | +62% |
| ITOM Standard | ITOM AIOps Professional v2 | +71% |
| ITOM Professional | ITOM AIOps Professional v2 | +18% |
| ITOM Enterprise | ITOM AIOps Enterprise v3 | +24% |

### Reasons to Migrate
- Access to Log Analytics (HLA)
- Agent Client Collector on end user devices
- Cloud Services Catalog
- ITOM Observability

---

## OT Management Products (Site-Based Pricing)

### OT Service Management (OTSM)
| Tier | Price | Key Features |
|------|-------|--------------|
| Standard | $6,000/site/month | Incident, Change, Request, Problem Management |
| Professional | $8,000/site/month | + Continual Improvement, DevOps Change Velocity, Virtual Agent |
| Enterprise | $10,000/site/month | + Process Mining, Workforce Optimization |

### OT Visibility - $10,000/site/month
- Discovery for OT
- ITOM Visibility
- Industrial Process Manager
- 5,000 OT Devices default

### OT Vulnerability Response
| Tier | Price |
|------|-------|
| Standard | $6,000/site/month |
| Professional | $8,000/site/month |
| Enterprise | $10,000/site/month |

### OT Asset Management - $10,000/site/month
- Hardware Asset Management (Limited)
- OT Obsolescence Management
- Planned Maintenance

### OT Operations Management (OTOM)
| Tier | Price |
|------|-------|
| Professional | $30,000/site/month |
| Enterprise | $33,000/site/month |

### OT Health - $12,000/site/month
- Requires OT Visibility

### Now Assist for OTSM Plus - $7,000/site/month
- 300,000 Assists/site annually
- Now Assist for CMDB, SGC, Docintel

### Mandatory Add-Ons for OT
- **Industrial Footprint Management Pack** - $10/site/month (required for all site-based SKUs)
- **OT Devices Pack** - $2,000/1000 devices/month (for additional devices beyond 5,000 default)
- **OT Site User Pack** - $10,000/all industrial sites (for additional users beyond 50 default)

---

## Pricing Summary Table

| SKU | Price | Product ID |
|-----|-------|-----------|
| ITOM Discovery v2 | $8/SU/month | PROD15000 |
| ITOM Visibility v2 | $12/SU/month | PROD14997 |
| ITOM Health v2 | $14/SU/month | PROD14998 |
| ITOM AIOps Professional v2 | $24/SU/month | PROD14995 |
| ITOM AIOps Enterprise v3 | $42/SU/month | PROD25358 |
| ITOM Professional Plus | $14/SU/month | PROD22521 |
| ITOM Enterprise Plus | $14/SU/month | PROD22524 |
| Cloud Accelerate | $8/SU/month | PROD16960 |
| Health Log Analytics | $14/SU/month | PROD16964 |
| API Insights v2 | $12/SU/month | PROD25492 |
| Cloud Governance Suite | $50,000 flat | - |

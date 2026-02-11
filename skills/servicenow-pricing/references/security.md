# Security Operations Pricing & Packaging

## Overview
Security Operations includes Security Incident Response (SIR), Vulnerability Response (VR), and Security Posture Control (SPC). Licensed by **Unrestricted User** (SIR), **Devices** (VR), or **Subscription Units** (USEM).

---

## Security Incident Response (SIR)

### SIR Packaging Tiers

**Meter: Unrestricted User (UU)**
An Unrestricted User is every user with a unique username and active user profile.

### SIR Standard v4 - $2.50/UU (PROD20790)
**Includes:**
- Security Incident Response (SIR)
- Performance Analytics Advanced
- App Engine Starter (5 tables)

### SIR Professional v2 - $4.00/UU (PROD16744)
**Includes SIR Standard plus:**
- Threat Intelligence for SIR
- Event Management for Security Operations
- SIR Integration Bundles
- Major Security Incident Management
- Cybersecurity Executive Dashboard
- Predictive Intelligence

### SIR Enterprise - $6.00/UU (PROD22090)
**Includes SIR Professional plus:**
- Threat Intelligence Security Center (TISC)
- App Engine Starter (25 tables)

### SIR Pro/Enterprise Plus - $2.40/UU (PROD23697/PROD23700)
**Assist Entitlement:** 150 Assists/UU/year

**Included Capabilities:**
| Generative AI | AI Agents |
|--------------|-----------|
| Incident Summarization | Incident Resolver Agents |
| Resolution Notes Generation | SecOps Metrics Agent |
| Recommended Actions | Shift Handover Agent |
| Correlation Insights | Incident Wrap-up Agent |
| Platform AI Capabilities | |

**Licensing:**
- Add-on SKU UU count must match base Pro/Enterprise SKU
- Same price for Pro Plus and Enterprise Plus

---

## Vulnerability Response (VR)

### VR Packaging Tiers

**Meter: Devices**
A Device is an active IP device or interface monitored/scanned as part of corporate security infrastructure.

### VR Standard v2 - $1.25/Device (PROD20824)
**Includes:**
- Vulnerability Response
- Performance Analytics Advanced
- App Engine Starter (5 tables)

### VR Professional v2 - $2.25/Device (PROD20825)
**Includes VR Standard plus:**
- Vulnerability Solution Management
- CISA Plugin
- Vulnerability Crisis Management
- Application Vulnerability Response
- Cybersecurity Executive Dashboard
- Patch Orchestration
- SBOM Management
- Predictive Intelligence

### VR Enterprise v2 - $3.00/Device (PROD20826)
**Includes VR Professional plus:**
- Configuration Compliance
- Container Vulnerability Response
- Cloud Security for Cloud Workspace
- App Engine Starter (25 tables)

### VR Pro/Enterprise Plus - $1.40/Device (PROD26349/PROD26350)
**Assist Entitlement:** 100 Assists/device/year

**Included Capabilities:**
- Vulnerability Exposure Analysis
- Remediation Status Analysis
- Vulnerable Item De-duplication
- Solution Recommendation
- Remediation Assistance
- Platform AI Capabilities

---

## Unified Security Exposure Management (USEM) - cGTM

### USEM Professional with AI - $19/SU (PROD26966)
**Includes ALL VR Enterprise + SPC + Now Assist for VR**

**Assist Entitlement:** 500 Assists/SU/year

**Includes:**
- All Vulnerability Response features
- Security Posture Control
- Configuration Compliance
- Container Vulnerability Response
- Cloud Security for Cloud Workspace
- Now Assist for VR
- Patch Orchestration
- SBOM Management
- Predictive Intelligence
- Performance Analytics Advanced
- App Engine Starter (25 tables)

### USEM SU Resource Ratios
| Resource Type | SU Ratio |
|--------------|----------|
| Server | 1:1 |
| PaaS Resource | 3:1 |
| Container Images | 1:1 |
| Unresolved Scanned Devices | 20:1 |
| End User Computing Devices | 4:1 |
| Networking Device | 25:1 |
| Networking Device Advanced | 25:1 |
| FaaS Resource | 20:1 |
| Applications | 1:1 |
| APIs | 1:1 |
| Database | 4:1 |
| Services | 4:1 |
| Others | 20:1 |
| IoT | 40:1 |

**Note:** Running container instances are no longer metered.

---

## Security Posture Control (SPC)

### SPC - $2.00/Device (PROD20860)
**Includes:**
- Security Posture Control
- Configuration Compliance (SPC use cases only)
- Performance Analytics
- App Engine Starter (5 tables)

**Requirements:**
- ITOM Discovery or Visibility entitlement required
- Does NOT include cloud/CC integration entitlements (requires VR Enterprise)

**Scope:**
- Hardware CI classes and child classes in CMDB
- Cloud VMs in AWS, Azure, GCP

---

## Add-On Products

### Data Loss Prevention Incident Response (DLPIR) - $2.25/UU (PROD16746)
**Includes:**
- DLP Incident Response
- App Engine Starter (5 tables)
- Performance Analytics

### Threat Intelligence Security Center (TISC) - $3.00/UU (PROD22290)
**Includes:**
- Threat Intelligence Security Center
- App Engine Starter (5 tables)
- Performance Analytics

**Note:** Cannot purchase with SIR Enterprise (TISC is included). Can purchase with SIR Std/Pro.

---

## Now Assist for Security Operations

### Now Assist for SIR
**Skills:**
- Incident Summarization
- Resolution Notes Generation
- Recommended Actions
- Correlation Insights
- AI Agents: Incident Resolver, SecOps Metrics, Shift Handover, Incident Wrap-up

**Microsoft Integration:** SIR + Microsoft Security Copilot
- Enrich SIR with threat data from MS Defender
- Enrich MS Security Copilot with SIR summary, CMDB info

### Now Assist for VR
**Skills:**
- Vulnerability Exposure Assessment
- Remediation Status Analysis
- Vulnerable Item De-duplication
- Solution Recommendation
- Remediation Assistance

---

## Migration Guidance

### Legacy SecOps Enterprise (SIR + VR)
| Migration Path | Guidance |
|---------------|----------|
| VR Enterprise & SIR Enterprise | 100% upsell, 50% minimum |
| VR Enterprise & SIR Pro | 150% upsell, 75% minimum |
| 2 Pros (VR Pro & SIR Pro) | 100% upsell, 50% minimum |
| Renew Legacy SecOps Pro | Maintain entitlements |

### VR Version Upgrades
| From | To | Guidance |
|------|-----|----------|
| VR Pro v1 | VR Pro v2 | 30% upsell (15% min) |
| VR Enterprise v1 | VR Enterprise v2 | 25% upsell (10% min) |
| SIR/VR Std (No PA) | SIR/VR Std (w/ PA) | 25% upsell (10% min) |

---

## Buying Rules

### Key Constraints
1. **Single Tier:** Cannot buy different VR tiers for different environments
2. **Single Tier:** Cannot buy different SIR tiers for different environments
3. **Device Matching:** SIR on Devices requires same device count as VR
4. **TISC Exclusivity:** Cannot purchase SIR Enterprise + TISC (already included)
5. **SPC Prerequisites:** Requires ITOM Discovery or Visibility
6. **SPC Configuration Compliance:** Only grants SPC use cases, not full CC

### USEM-Specific Rules
- Cannot add USEM alongside existing non-USEM VR (double metering)
- No UU metering option (requires custom SKU)
- No device metering option (requires custom SKU)
- Cannot substitute Assists for SUs
- Devices from multiple scanners are de-duplicated in CMDB

---

## Why Security Products

### Why TISC?
- Consolidated threat data visibility
- Automated threat prioritization
- Collaborative defense sharing
- Orchestrated response with SIR
- Single pane of glass for SOC personas

### Why SPC?
- Visibility into asset inventory and security tool coverage gaps
- Identify assets with critical vulnerabilities missing security tools
- Visibility into high-risk cloud assets
- Custom policies for configuration requirements
- Automated remediation workflows

### Why USEM?
- Single SKU for all Attack Surface Management features
- SU metering pays only for resources used
- Easy expansion from workstations/servers to cloud/containers
- Standardized ratios across resource types

---

## Pricing Summary Table

| Product | Price | Meter | Product ID |
|---------|-------|-------|-----------|
| SIR Standard v4 | $2.50 | UU | PROD20790 |
| SIR Professional v2 | $4.00 | UU | PROD16744 |
| SIR Enterprise | $6.00 | UU | PROD22090 |
| SIR Pro/Enterprise Plus | $2.40 | UU | PROD23697/PROD23700 |
| VR Standard v2 | $1.25 | Device | PROD20824 |
| VR Professional v2 | $2.25 | Device | PROD20825 |
| VR Enterprise v2 | $3.00 | Device | PROD20826 |
| VR Pro/Enterprise Plus | $1.40 | Device | PROD26349/PROD26350 |
| USEM Pro with AI | $19.00 | SU | PROD26966 |
| SPC | $2.00 | Device | PROD20860 |
| DLPIR | $2.25 | UU | PROD16746 |
| TISC | $3.00 | UU | PROD22290 |

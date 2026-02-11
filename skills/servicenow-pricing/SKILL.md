---
name: servicenow-pricing
description: ServiceNow pricing and packaging expert. Use when answering questions about ServiceNow product pricing, licensing, SKUs, packaging tiers, module comparisons, Now Assist, AI features, or any ServiceNow commercial questions.
allowed-tools: Read, Grep, Glob
---

# ServiceNow Pricing & Packaging Expert

Comprehensive knowledge base for ServiceNow pricing, packaging, licensing, and SKU information based on official documentation.

## Reference Documents

When answering pricing questions, consult the relevant reference file:

| Category | Reference File | Coverage |
|----------|---------------|----------|
| **IT Operations (ITOM)** | [references/itom.md](references/itom.md) | Discovery, Service Mapping, Event Management, Health Log Analytics, Cloud Management |
| **IT Service Management (ITSM)** | [references/itsm.md](references/itsm.md) | Incident, Problem, Change, Request Management |
| **IT Asset Management (ITAM)** | [references/itam.md](references/itam.md) | Hardware/Software Asset Management, SAM |
| **Security Operations** | [references/security.md](references/security.md) | SecOps, SOAR, Vulnerability Response, Platform Security |
| **AI & Now Assist** | [references/ai-now-assist.md](references/ai-now-assist.md) | Now Assist, AI Agents, Gen AI requirements, AI Starter Pack |
| **App Engine** | [references/app-engine.md](references/app-engine.md) | App Engine Studio, Low-code development |
| **Employee Workflows** | [references/employee-workflows.md](references/employee-workflows.md) | HRSD, Legal, Workplace, Manufacturing |
| **Strategic Portfolio Management** | [references/spm.md](references/spm.md) | Project Portfolio Management, Agile |
| **Customer Workflows (CRM)** | [references/crm.md](references/crm.md) | Customer Service Management, Field Service |
| **Other Modules** | [references/other-modules.md](references/other-modules.md) | GRC/Risk, Impact, Data Fabric, Process Mining, Source-to-Pay |

## How to Answer Questions

1. **Identify the product area** from the user's question
2. **Read the relevant reference file(s)** using the paths above
3. **Provide specific information**:
   - Packaging tiers (Standard, Professional, Enterprise)
   - SKU names and requirements
   - Prerequisites and dependencies
   - Pricing models (subscription, fulfiller-based, capacity-based)
4. **Cross-reference** if the question spans multiple areas (e.g., Now Assist requires base SKUs)

## Common Pricing Patterns

### Subscription Tiers
Most products follow: **Standard** < **Professional** < **Enterprise**
- Standard: Core functionality
- Professional: Advanced features, analytics
- Enterprise: Full capabilities, AI features

### Licensing Models
- **Fulfiller-based**: Licensed per IT agent/user
- **Unrestricted users**: Self-service portals
- **Capacity-based**: Usage metrics (nodes, events, transactions)
- **Named user**: Specific individuals

### AI/Now Assist Requirements
- Requires base product SKU (e.g., ITSM Pro for Now Assist for ITSM)
- Gen AI Base SKU requirements vary by release
- Check [references/ai-now-assist.md](references/ai-now-assist.md) for current requirements

## Key Cross-References

- **Now Assist** requires underlying product SKUs - check both AI and product-specific references
- **ITOM** products often have interdependencies - check ITOM reference for bundles
- **Industry solutions** may map to multiple base products - see Other Modules reference

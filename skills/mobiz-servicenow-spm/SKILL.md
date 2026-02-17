---
name: mobiz-servicenow-spm
description: |
  Manage ServiceNow Strategic Portfolio Management (SPM) artifacts via AI Bridge.
  Use when the user wants to:
  - Create, read, update, or delete SPM records (projects, tasks, milestones, epics, stories, sprints, resources, demands, portfolios, programs)
  - Import a complete project hierarchy from a SOW or structured format document
  - Manage resource plans, financial plans, time cards, or cost plans
  - Query project status, agile backlogs, demand pipelines, or portfolio health
  - Convert a Statement of Work into ServiceNow SPM artifacts
  - Understand SPM processes (project management, demand, resource planning, agile)
  Keywords: SPM, strategic portfolio management, project, portfolio, program, demand, resource, epic, story, sprint, milestone, agile, project task, pm_project, rm_epic, rm_story, pm_project_task, pm_milestone, resource_plan, dmn_demand, SOW import, project hierarchy, AI Bridge
allowed-tools: Bash, Read, Grep, Glob
---

# ServiceNow Strategic Portfolio Management (SPM) Skill

Comprehensive knowledge base for managing ServiceNow SPM artifacts via the AI Bridge REST adapter. Covers project portfolio management, demand management, resource planning, agile development, and bulk project import from SOW documents.

## Prerequisites

1. **AI Bridge** update set installed on the target ServiceNow instance (`servicenow-ai-bridge` skill provides the generic API reference)
2. **Admin credentials** for the ServiceNow instance (Basic Auth)
3. Base URL: `https://{instance}.service-now.com/api/1851835/ai_adapter_rest/{tableName}`

## Workflow Decision Tree

### Query / Read SPM Data
1. Identify the correct table from [references/table-reference.md](references/table-reference.md)
2. Build your GET request — see [references/ai-bridge-spm.md](references/ai-bridge-spm.md)
3. Use `sysparm_display_value=all` to get both sys_ids and display values

### Create a Single Record
1. **Check Mobiz mandatory fields FIRST** — see [references/mobiz-mandatory-fields.md](references/mobiz-mandatory-fields.md)
2. Identify the table and its key fields from [references/table-reference.md](references/table-reference.md)
3. Resolve reference field sys_ids first (query sys_user, core_company, pm_project, etc.)
4. POST via AI Bridge — see [references/ai-bridge-spm.md](references/ai-bridge-spm.md)

### Update an Existing Record
1. Query to find the record and get its sys_id
2. PUT via AI Bridge with only the fields to change

### Import a Complete Project Hierarchy (SOW → SPM)
1. If starting from a SOW document: use `mobiz-pdf` skill to parse the SOW
2. Convert content to structured import format — see [references/structured-import-format.md](references/structured-import-format.md)
3. Follow the step-by-step workflow in [references/import-workflow.md](references/import-workflow.md)

### Understand SPM Processes
- Project Management: [references/project-management.md](references/project-management.md)
- Demand Management: [references/demand-management.md](references/demand-management.md)
- Resource Management: [references/resource-management.md](references/resource-management.md)
- Agile (Epics/Stories/Sprints): [references/agile-management.md](references/agile-management.md)

### Introspect Instance Schema
- Run: `bash scripts/introspect_schema.sh <instance_url> <user> <password>`
- Or query manually: `GET /api/1851835/ai_adapter_rest/sys_dictionary?sysparm_query=name=pm_project`

## Reference Documents

| Category | Reference File | Coverage |
|----------|---------------|----------|
| **AI Bridge for SPM** | [references/ai-bridge-spm.md](references/ai-bridge-spm.md) | CRUD curl examples for all SPM tables |
| **Table Reference** | [references/table-reference.md](references/table-reference.md) | All SPM tables, fields, relationships, states, roles |
| **Project Management** | [references/project-management.md](references/project-management.md) | Project lifecycle, phases, tasks, milestones, dependencies |
| **Demand Management** | [references/demand-management.md](references/demand-management.md) | Demand intake, assessment, approval, conversion to project |
| **Resource Management** | [references/resource-management.md](references/resource-management.md) | Resource plans, allocation, capacity, time cards |
| **Agile Management** | [references/agile-management.md](references/agile-management.md) | Epics, stories, sprints, backlogs, Scrum/SAFe |
| **Import Workflow** | [references/import-workflow.md](references/import-workflow.md) | Step-by-step bulk import from structured format |
| **Structured Import Format** | [references/structured-import-format.md](references/structured-import-format.md) | Canonical template for AI-generated project hierarchies |
| **Mobiz Mandatory Fields** | [references/mobiz-mandatory-fields.md](references/mobiz-mandatory-fields.md) | Mobiz-specific mandatory fields, agile board setup, import checklist |
| **Instance Schema** | [references/instance-schema.md](references/instance-schema.md) | Introspected field definitions, choice values, custom fields |

## Quick Start Examples

### Query all projects
```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project?sysparm_fields=sys_id,short_description,start_date,end_date,state,project_manager&sysparm_limit=20&sysparm_display_value=all"
```

### Create a project (with Mobiz mandatory fields)
```bash
curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project" \
  -H "Content-Type: application/json" \
  -d '{"data": {
    "short_description": "My Project",
    "start_date": "2026-03-01",
    "end_date": "2026-06-30",
    "state": "-5",
    "project_manager": "<user_sys_id>",
    "company": "<company_sys_id>",
    "x_mobit_spm_enh_commercial_contract_model": "t&m",
    "x_mobit_spm_enh_payment_source": "mobiz",
    "x_mobit_spm_enh_planned_effort_sow": "960",
    "approved_start_date": "2026-03-01",
    "approved_end_date": "2026-06-30",
    "business_case": "<p>Business justification</p>",
    "in_scope": "<p>Project scope</p>"
  }}'
```

### Create a project task (phase)
```bash
curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task" \
  -H "Content-Type: application/json" \
  -d '{"data": {
    "short_description": "Phase 1: Discovery",
    "parent": "<project_sys_id>",
    "start_date": "2026-03-01",
    "end_date": "2026-03-15",
    "state": "-5",
    "assigned_to": "<user_sys_id>",
    "phase_type": "waterfall"
  }}'
```

## Credential Handling

Ask the user for credentials and set shell variables:
```bash
export SN_INSTANCE="https://devXXXXXX.service-now.com"
export SN_USER="admin"
export SN_PASS="password"
```

## Important Rules

1. **Check Mobiz mandatory fields FIRST** — see [references/mobiz-mandatory-fields.md](references/mobiz-mandatory-fields.md)
2. **Always query first** before creating — check for duplicates
3. **Save sys_ids** from creation responses for subsequent operations
4. **Dates** in ServiceNow format: `YYYY-MM-DD` or `YYYY-MM-DD HH:MM:SS`
5. **Reference fields** (parent, project, epic, assigned_to, company) require sys_id of target record
6. **State values** are numeric strings — see [references/table-reference.md](references/table-reference.md) for mappings
7. **Import order matters**: Users → Company → Project (with mandatory fields) → Agile Board → Phases → Milestones → Epics → Stories → Resources
8. **ALWAYS ask user** if they want an agile board when creating a project
9. **Milestones**: Use `pm_project_task` with `milestone: "true"`, NOT `pm_milestone` table. Must be under waterfall phases or directly under the project.
10. **Stories**: Must include `project`, `company`, and `assignment_group` (if agile board). `project_phase` must be set via separate PUT (silently ignored during POST).
11. **Use `sysparm_display_value=all`** when you need both sys_ids and human-readable values
12. **Phase nesting constraints** (ServiceNow design rules — do NOT bypass via API):
    - **Agile phases** must be top-level only (direct children of the project)
    - **Agile phases** cannot have child pm_project_task records — they hold stories only
    - **Waterfall phases** support nested task hierarchy (sub-tasks, sub-phases, milestones)
    - See [references/mobiz-mandatory-fields.md](references/mobiz-mandatory-fields.md) → "Phase Nesting Constraints" for architecture options

## Integration with Other Skills

- **`mobiz-pdf`**: Parse SOW documents before importing into SPM
- **`servicenow-ai-bridge`**: Generic AI Bridge API reference (prerequisite)
- **`servicenow-pricing`**: SPM licensing and packaging info

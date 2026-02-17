# SPM Import Workflow: Structured Format to ServiceNow

Step-by-step guide for creating a complete SPM project hierarchy from a structured import document via AI Bridge.

## Overview

This workflow takes a structured project definition (see [structured-import-format.md](structured-import-format.md)) and creates all artifacts in ServiceNow in the correct order, maintaining parent-child relationships throughout.

## Prerequisites

1. AI Bridge installed on the target instance
2. Admin credentials set as shell variables:
   ```bash
   export SN_INSTANCE="https://devXXXXXX.service-now.com"
   export SN_USER="admin"
   export SN_PASS="password"
   ```
3. Structured import format document ready (see [structured-import-format.md](structured-import-format.md))
4. `jq` installed for JSON parsing (`brew install jq`)

## Import Order (Critical)

The order matters because each step requires sys_ids from previous steps:

```
Step 1:  Resolve User sys_ids
Step 2:  Resolve Company sys_id (from core_company)
Step 3:  Ask user for missing Mobiz mandatory fields
Step 4:  Create Portfolio (optional)
Step 5:  Create Program (optional)
Step 6:  Create Project (with ALL Mobiz mandatory fields)
Step 7:  ASK: Create agile board? → If yes: Create Group → Backlog → Update Project
Step 8:  Create Phases (pm_project_task with phase_type — see Phase Architecture Rules below)
Step 9:  Create Waterfall Sub-tasks (only under waterfall phases)
Step 10: Create Milestones (pm_project_task with milestone: "true", under waterfall phases only)
Step 11: Create Epics
Step 12: Create Stories (with project, company, assignment_group; project_phase via PUT)
Step 13: Create Resource Plans
Step 14: Set Task Dependencies
```

> **IMPORTANT**: Before creating a project, ALWAYS check [mobiz-mandatory-fields.md](mobiz-mandatory-fields.md) for required Mobiz-specific fields.

## Sys_id Tracking Pattern

Maintain a mapping of local IDs to ServiceNow sys_ids throughout the import. Track these in your conversation context:

```
USER MAPPINGS:
  "Igor Kochetkov" -> abc123def456...
  "Viktor Bardakov" -> ghi789jkl012...

PROJECT:
  "SOVHUB-2026-Q1" -> mno345pqr678...

PHASES:
  PT-001 -> stu901vwx234...
  PT-002 -> yza567bcd890...
  PT-002.1 -> efg123hij456...

MILESTONES:
  MS-001 -> klm789nop012...

EPICS:
  EPIC-001 -> qrs345tuv678...

STORIES:
  Story-001.1 -> wxy901zab234...
```

## Step 1: Resolve User Sys_ids

Before creating any records, resolve all users mentioned in the import document.

```bash
# Query for a user by name
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/sys_user?sysparm_query=name=Igor Kochetkov&sysparm_fields=sys_id,name,email,title&sysparm_limit=1" | jq '.result[0].sys_id'

# Query multiple users
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/sys_user?sysparm_query=nameINIgor Kochetkov,Viktor Bardakov,Fares Arnous&sysparm_fields=sys_id,name,email&sysparm_display_value=true"
```

**Important**: If a user doesn't exist, you may need to create them first or ask the user for the correct name.

## Step 2: Resolve Company Sys_id

Resolve the company from `core_company` table. This is required for the project and all stories.

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/core_company?sysparm_query=nameLIKE{CLIENT_NAME}&sysparm_fields=sys_id,name&sysparm_limit=5"
```

Save `COMPANY_SYS_ID` for use in project creation and all story records.

**If company not found**: ASK the user for the correct company name.

## Step 3: Ask for Missing Mobiz Mandatory Fields

Before creating a project, check which Mobiz mandatory fields can be derived from the SOW and which need to be asked:

1. **Commercial/Contract Model** (`x_mobit_spm_enh_commercial_contract_model`): Values: `staff_aug`, `boh`, `support`, `ff`, `t&m`
2. **Payment Source** (`x_mobit_spm_enh_payment_source`): Values: `client`, `mobiz`, `ecif`, `amm`, `other`
3. **Project Type** (`x_mobit_spm_enh_project_type`): Only if company != "Mobiz IT". Values: `Presales`, `Billable`, `Internal`
4. **Planned Effort (SOW)** (`x_mobit_spm_enh_planned_effort_sow`): Total hours from SOW
5. **Business Case** (`business_case`): From SOW justification
6. **In Scope** (`in_scope`): From SOW scope section

ASK the user for any values that cannot be derived from the source document.

See [mobiz-mandatory-fields.md](mobiz-mandatory-fields.md) for the complete field reference.

## Step 4: Create Portfolio (Optional)

```bash
PORTFOLIO_ID=$(curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_portfolio" \
  -H "Content-Type: application/json" \
  -d '{"data": {
    "short_description": "ServiceNow Practice IP Development",
    "owner": "<owner_sys_id>",
    "state": "1"
  }}' | jq -r '.result.sys_id')
echo "Portfolio sys_id: $PORTFOLIO_ID"
```

## Step 5: Create Program (Optional)

```bash
PROGRAM_ID=$(curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_program" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"short_description\": \"Sovereign Hub GTM Initiative\",
    \"pm_portfolio\": \"$PORTFOLIO_ID\",
    \"program_manager\": \"<pm_sys_id>\"
  }}" | jq -r '.result.sys_id')
echo "Program sys_id: $PROGRAM_ID"
```

## Step 6: Create Project

Include ALL Mobiz mandatory fields. See [mobiz-mandatory-fields.md](mobiz-mandatory-fields.md) for the complete reference.

```bash
PROJECT_ID=$(curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"short_description\": \"Sovereign Hub Demo & Content Pipeline\",
    \"description\": \"Phase 2: ITSM Catalogs\",
    \"start_date\": \"2026-02-17\",
    \"end_date\": \"2026-03-28\",
    \"state\": \"-5\",
    \"project_manager\": \"<pm_sys_id>\",
    \"company\": \"$COMPANY_SYS_ID\",
    \"x_mobit_spm_enh_commercial_contract_model\": \"t&m\",
    \"x_mobit_spm_enh_payment_source\": \"mobiz\",
    \"x_mobit_spm_enh_planned_effort_sow\": \"960\",
    \"approved_start_date\": \"2026-02-17\",
    \"approved_end_date\": \"2026-03-28\",
    \"business_case\": \"<p>Business case from SOW</p>\",
    \"in_scope\": \"<p>Scope from SOW</p>\"
  }}" | jq -r '.result.sys_id')
echo "Project sys_id: $PROJECT_ID"
```

**Key project fields**:
- `short_description` - Project name (required)
- `start_date`, `end_date` - Project timeline
- `state` - `-5` for Draft
- `project_manager` - User sys_id
- `description` - Detailed description
- `pm_program` - Link to program (optional)
- `company` - Company sys_id (MANDATORY on Mobiz)
- `x_mobit_spm_enh_commercial_contract_model` - Contract model (MANDATORY on Mobiz)
- `x_mobit_spm_enh_payment_source` - Payment source (MANDATORY on Mobiz)
- `x_mobit_spm_enh_planned_effort_sow` - Total hours from SOW (MANDATORY on Mobiz)
- `approved_start_date`, `approved_end_date` - Approved dates (MANDATORY on Mobiz)
- `business_case` - Business case HTML (MANDATORY on Mobiz)
- `in_scope` - In scope HTML (MANDATORY on Mobiz)

## Step 7: Create Agile Board (Ask User First)

**ALWAYS ask the user if they want an agile board** when creating a project. If yes:

### Step 7a: Create Agile Group
```bash
GROUP_SYS_ID=$(curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/sys_user_group" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"name\": \"$PROJECT_NUMBER $PROJECT_NAME\",
    \"type\": \"1bff3b1493030200ea933007f67ffb6d\"
  }}" | jq -r '.result.sys_id')
echo "Group sys_id: $GROUP_SYS_ID"
```

### Step 7b: Create Backlog Definition
```bash
BACKLOG_SYS_ID=$(curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/backlog_definition" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"name\": \"$PROJECT_NUMBER $PROJECT_NAME\",
    \"shared_with_groups\": \"$GROUP_SYS_ID\",
    \"owner\": \"$CURRENT_USER_SYS_ID\",
    \"u_project\": \"$PROJECT_ID\",
    \"filter\": \"sys_class_name=rm_story^active=true^sprintISEMPTY^u_project=$PROJECT_ID\"
  }}" | jq -r '.result.sys_id')
echo "Backlog sys_id: $BACKLOG_SYS_ID"
```

### Step 7c: Link Board to Project
```bash
curl -s -u "$SN_USER:$SN_PASS" -X PUT \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project/$PROJECT_ID" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"u_default_agile_teams\": \"$GROUP_SYS_ID\",
    \"backlog_definition\": \"$BACKLOG_SYS_ID\"
  }}"
```

Save `GROUP_SYS_ID` — it will be used in all story records.

## Step 8: Create Phases (Top-level Project Tasks)

Create each phase as a `pm_project_task` with `parent` set to the project sys_id. **Always set `phase_type`**.

### Phase Architecture Rules (ServiceNow Design Constraints)

> **CRITICAL**: These are ServiceNow platform rules. Do NOT bypass them via API.

- **Agile phases** (`phase_type: "agile"`): Must be **top-level only** (direct children of the project). Cannot have child pm_project_task records. Hold stories only (linked via `project_phase`).
- **Waterfall phases** (`phase_type: "waterfall"`): Can have nested child tasks, sub-phases, and milestones.
- **Milestones**: Can only exist under waterfall phases or directly under the project.

See [mobiz-mandatory-fields.md](mobiz-mandatory-fields.md) → "Phase Nesting Constraints" for full architecture options.

### Example: Agile Phase (top-level, holds stories)
```bash
PHASE_001=$(curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"short_description\": \"Employee Onboarding\",
    \"description\": \"Employee onboarding service catalog demos\",
    \"parent\": \"$PROJECT_ID\",
    \"start_date\": \"2026-02-17\",
    \"end_date\": \"2026-03-06\",
    \"state\": \"-5\",
    \"assigned_to\": \"<user_sys_id>\",
    \"phase_type\": \"agile\"
  }}" | jq -r '.result.sys_id')
echo "Phase PT-001: $PHASE_001"
```

### Example: Waterfall Phase (can have child tasks)
```bash
PHASE_002=$(curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"short_description\": \"Phase 2: ITSM Catalogs\",
    \"description\": \"Build ITSM service catalog demos\",
    \"parent\": \"$PROJECT_ID\",
    \"start_date\": \"2026-02-17\",
    \"end_date\": \"2026-03-06\",
    \"state\": \"-5\",
    \"assigned_to\": \"<user_sys_id>\",
    \"phase_type\": \"waterfall\"
  }}" | jq -r '.result.sys_id')
echo "Phase PT-002: $PHASE_002"
```

Repeat for each top-level phase.

## Step 9: Create Waterfall Sub-tasks

Create sub-tasks **only under waterfall phases**. Do NOT create child tasks under agile phases.

```bash
TASK_002_1=$(curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"short_description\": \"Employee Onboarding Setup\",
    \"description\": \"Configure onboarding catalog items and workflows\",
    \"parent\": \"$PHASE_002\",
    \"start_date\": \"2026-02-17\",
    \"end_date\": \"2026-02-21\",
    \"state\": \"-5\",
    \"assigned_to\": \"<user_sys_id>\",
    \"phase_type\": \"waterfall\"
  }}" | jq -r '.result.sys_id')
echo "Task PT-002.1: $TASK_002_1"
```

## Step 10: Create Milestones

Create milestones as `pm_project_task` records with `milestone: "true"`. Do NOT use the `pm_milestone` table.

```bash
MS_001=$(curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"short_description\": \"Milestone: Phase 2 Complete\",
    \"description\": \"All ITSM catalog stories delivered and demoed\",
    \"parent\": \"$PHASE_002\",
    \"start_date\": \"2026-03-06\",
    \"end_date\": \"2026-03-06\",
    \"state\": \"-5\",
    \"milestone\": \"true\",
    \"phase_type\": \"waterfall\"
  }}" | jq -r '.result.sys_id')
echo "Milestone MS-001: $MS_001"
```

**Important**: Use `pm_project_task` with `milestone: "true"`, not `pm_milestone` table.

## Step 11: Create Epics

```bash
EPIC_001=$(curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_epic" \
  -H "Content-Type: application/json" \
  -d '{"data": {
    "short_description": "Employee Lifecycle Management",
    "description": "Onboarding and offboarding automation",
    "state": "draft",
    "story_points": "30",
    "start_date": "2026-02-17",
    "end_date": "2026-02-21"
  }}' | jq -r '.result.sys_id')
echo "Epic EPIC-001: $EPIC_001"
```

## Step 12: Create Stories

Include Mobiz mandatory fields: `project`, `company`, and `assignment_group` (if agile board exists). Set `project_phase` via PUT after creation.

```bash
STORY_001_1=$(curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_story" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"short_description\": \"Service Catalog Request Form (Arabic)\",
    \"description\": \"Create Arabic onboarding request form\",
    \"epic\": \"$EPIC_001\",
    \"state\": \"-6\",
    \"story_points\": \"5\",
    \"assigned_to\": \"<user_sys_id>\",
    \"effort\": \"1970-01-01 08:00:00\",
    \"acceptance_criteria\": \"Form submittable in Arabic UI\",
    \"project\": \"$PROJECT_ID\",
    \"company\": \"$COMPANY_SYS_ID\",
    \"assignment_group\": \"$GROUP_SYS_ID\"
  }}" | jq -r '.result.sys_id')
echo "Story Story-001.1: $STORY_001_1"
```

**Mandatory story fields (Mobiz)**:
- `project` - Project sys_id
- `effort` - GlideDuration format: `"1970-01-01 HH:00:00"` (8 hours = `"1970-01-01 08:00:00"`)
- `company` - Same company as the project
- `assignment_group` - Agile team group sys_id (if agile board was created)
- `project_phase` - Agile phase sys_id. **IMPORTANT: Must be set via separate PUT call after story creation** (silently ignored during POST)

**Recommended**: Create all stories first, then batch-update with `project_phase`, `effort`, and `assignment_group` via PUT.

## Step 13: Create Resource Plans

```bash
curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/resource_plan" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"resource\": \"<user_sys_id>\",
    \"top_task\": \"$PROJECT_ID\",
    \"planned_hours\": \"120\",
    \"start_date\": \"2026-02-17\",
    \"end_date\": \"2026-03-28\",
    \"state\": \"1\"
  }}"
```

**Key fields**:
- `resource` - sys_user sys_id
- `top_task` - The project or top-level task sys_id
- `planned_hours` - Total planned hours
- `state` - `1` for Open

## Step 14: Set Task Dependencies

Use the `planned_task_rel_planned_task` table to create predecessor/successor relationships.

```bash
curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/planned_task_rel_planned_task" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"parent\": \"$PHASE_001\",
    \"child\": \"$PHASE_002\",
    \"type\": \"fs\"
  }}"
```

**Dependency types**:
- `fs` - Finish-to-Start (most common): child starts after parent finishes
- `ss` - Start-to-Start: both start together
- `ff` - Finish-to-Finish: both finish together
- `sf` - Start-to-Finish: child finishes when parent starts

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 400 Bad Request | Missing required field | Check mandatory fields in instance-schema.md |
| 404 Not Found | Invalid table name | Verify table exists (may need plugin activation) |
| 401 Unauthorized | Bad credentials | Verify username/password |
| Duplicate record | Record already exists | Query first, update instead of create |
| Invalid reference | sys_id doesn't exist | Verify the referenced record exists |

### Recovery Strategy
If an import fails partway through:
1. Note which steps completed successfully (you have the sys_ids)
2. Fix the error (missing field, bad reference, etc.)
3. Resume from the failed step — don't re-create already-created records
4. Query to verify: `GET /pm_project_task?sysparm_query=parent=<project_sys_id>`

## Verification

After completing the import, verify the hierarchy:

```bash
# Count phases under project
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task?sysparm_query=parent=$PROJECT_ID&sysparm_fields=sys_id,short_description&sysparm_display_value=true" | jq '.result | length'

# Count stories under an epic
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_story?sysparm_query=epic=$EPIC_001&sysparm_fields=sys_id,short_description&sysparm_display_value=true" | jq '.result | length'

# Count milestones
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_milestone?sysparm_query=project=$PROJECT_ID&sysparm_fields=sys_id,short_description,date&sysparm_display_value=true" | jq '.result | length'

# Verify resource plans
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/resource_plan?sysparm_query=top_task=$PROJECT_ID&sysparm_fields=sys_id,resource,planned_hours&sysparm_display_value=true"
```

## SOW-to-SPM Pipeline

To import from a Statement of Work:

### Pipeline Flow
```
SOW Document (.pdf/.docx)
    │
    ▼
[mobiz-pdf skill] ── Parse SOW, extract phases, tasks, roles, effort
    │
    ▼
Structured Import Format (markdown)
    │  (see structured-import-format.md for template)
    ▼
[This import workflow] ── Execute CRUD operations via AI Bridge
    │
    ▼
ServiceNow SPM Artifacts
```

### Steps
1. **Parse SOW**: Use the `mobiz-pdf` skill to read and parse the SOW document
2. **Generate structured format**: Convert the parsed SOW into the structured import format (see [structured-import-format.md](structured-import-format.md))
3. **Review with user**: Present the structured format for user review before importing
4. **Execute import**: Follow Steps 1-11 above to create all artifacts
5. **Verify**: Run verification queries to confirm the import

## Performance Notes

- **API rate**: The AI Bridge has no explicit rate limit, but allow ~1 second between calls
- **Large imports**: For 100+ records, consider batching by type (all phases, then all milestones, etc.)
- **Timeout**: Each curl call should complete in <10 seconds. If not, check instance health
- **Estimated time**: A full project import (1 project + 6 phases + 10 milestones + 12 epics + 83 stories + 7 resources) takes ~30-45 minutes with AI automation

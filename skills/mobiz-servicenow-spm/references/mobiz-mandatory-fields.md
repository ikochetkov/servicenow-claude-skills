# Mobiz Mandatory Fields Reference

Mobiz-specific mandatory fields that MUST be set when creating SPM records on the Mobiz ServiceNow instance. These are in addition to standard ServiceNow fields.

> **CRITICAL**: When creating projects, ALWAYS check this file first. Missing mandatory fields will result in incomplete records.

---

## pm_project — Mandatory Fields

| # | Field API Name | Label | Type | Required | Notes |
|---|---|---|---|---|---|
| 1 | `company` | Company | Reference (core_company) | Always | Resolve by searching `core_company` by name. If not found in SOW → ASK user |
| 2 | `x_mobit_spm_enh_commercial_contract_model` | Commercial/Contract Model | Choice | Always | Values: `staff_aug`, `boh`, `support`, `ff`, `t&m`. If not in SOW → ASK user |
| 3 | `x_mobit_spm_enh_project_type` | Project type | Choice | When company != "Mobiz IT" | Values: `Presales`, `Billable`, `Internal`. If not in SOW → ASK user. **Not required when company is "Mobiz IT"** |
| 4 | `x_mobit_spm_enh_payment_source` | Payment source | Choice | Always | Values: `client`, `mobiz`, `ecif`, `amm`, `other`. If not in SOW → ASK user |
| 5 | `x_mobit_spm_enh_planned_effort_sow` | Planned effort (SOW) | Integer | Always | Total hours from SOW |
| 6 | `approved_start_date` | Approved start date | Date | Always | From SOW start date |
| 7 | `approved_end_date` | Approved end date | Date | Always | From SOW end date |
| 8 | `business_case` | Business case | HTML | Always | From SOW business case / justification |
| 9 | `in_scope` | In scope | HTML | Always | From SOW scope section |

### Company Resolution Pattern

Always resolve company sys_id before creating a project:

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/core_company?sysparm_query=nameLIKE{CLIENT_NAME}&sysparm_fields=sys_id,name&sysparm_limit=5"
```

If the company is not found, ASK the user for the correct company name.

### Decision: Internal vs External Project

- **Company = "Mobiz IT"**: This is an internal project. `x_mobit_spm_enh_project_type` is NOT required.
- **Company != "Mobiz IT"**: This is an external/client project. `x_mobit_spm_enh_project_type` IS required. ASK the user if not in SOW.

### Complete Project Create Example (Mobiz)

```bash
curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"short_description\": \"Sovereign Hub Demo & Content Pipeline\",
    \"description\": \"Phase 2: ITSM Catalogs — Employee Lifecycle, Arabic Service Catalog, Change & Incident, Asset & Knowledge\",
    \"start_date\": \"2026-02-17\",
    \"end_date\": \"2026-03-28\",
    \"state\": \"-5\",
    \"project_manager\": \"<pm_sys_id>\",
    \"company\": \"<company_sys_id>\",
    \"x_mobit_spm_enh_commercial_contract_model\": \"t&m\",
    \"x_mobit_spm_enh_payment_source\": \"mobiz\",
    \"x_mobit_spm_enh_planned_effort_sow\": \"960\",
    \"approved_start_date\": \"2026-02-17\",
    \"approved_end_date\": \"2026-03-28\",
    \"business_case\": \"<p>Convert unbillable developer capacity into Sovereign Hub IP and marketing content.</p>\",
    \"in_scope\": \"<p>ITSM service catalog demos covering Employee Lifecycle, Arabic Service Catalog, Change & Incident Management, Asset & Knowledge Management</p>\"
  }}"
```

---

## pm_project_task — Mandatory Fields

| # | Field API Name | Label | Type | Notes |
|---|---|---|---|---|
| 1 | `short_description` | Short description | String | Task/phase name |
| 2 | `description` | Description | String | Task description |
| 3 | `phase_type` | Phase type | Choice | `waterfall` for regular tasks/milestones, `agile` for agile phases |

### Milestone Rule

When creating a milestone, set `milestone: "true"` on the pm_project_task record. Do NOT use the `pm_milestone` table — use `pm_project_task` with the milestone checkbox.

```bash
curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"short_description\": \"Milestone: Phase 2 Complete\",
    \"description\": \"All ITSM catalog stories delivered and demoed\",
    \"parent\": \"<phase_sys_id>\",
    \"start_date\": \"2026-03-06\",
    \"end_date\": \"2026-03-06\",
    \"state\": \"-5\",
    \"milestone\": \"true\",
    \"phase_type\": \"waterfall\"
  }}"
```

### Phase Create Example (Agile Phase)

```bash
curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"short_description\": \"Phase 2: ITSM Catalogs\",
    \"description\": \"Build ITSM service catalog demos\",
    \"parent\": \"$PROJECT_ID\",
    \"start_date\": \"2026-02-17\",
    \"end_date\": \"2026-03-06\",
    \"state\": \"-5\",
    \"phase_type\": \"agile\"
  }}"
```

---

## rm_story — Mandatory Fields

| # | Field API Name | Label | Type | Notes |
|---|---|---|---|---|
| 1 | `project` | Project | Reference (pm_project) | sys_id of the project |
| 2 | `project_phase` | Project phase | Reference (pm_project_task) | sys_id of the agile phase the story belongs to |
| 3 | `effort` | Planned effort | Duration | GlideDuration format: `"1970-01-01 HH:00:00"`. E.g., 8 hours = `"1970-01-01 08:00:00"` |
| 4 | `company` | Company | Reference (core_company) | Same company as the project |
| 5 | `assignment_group` | Assignment group | Reference (sys_user_group) | Agile team group sys_id (if agile board exists) |

### Story Create Example (Mobiz)

```bash
curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_story" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"short_description\": \"Service Catalog Request Form (Arabic)\",
    \"description\": \"Create Arabic onboarding request form\",
    \"epic\": \"$EPIC_SYS_ID\",
    \"state\": \"-6\",
    \"story_points\": \"5\",
    \"assigned_to\": \"<user_sys_id>\",
    \"effort\": \"1970-01-01 08:00:00\",
    \"acceptance_criteria\": \"Form submittable in Arabic UI\",
    \"project\": \"$PROJECT_ID\",
    \"company\": \"$COMPANY_SYS_ID\",
    \"assignment_group\": \"$GROUP_SYS_ID\"
  }}"
```

### Important: project_phase Requires Separate PUT

The `project_phase` field is **silently ignored** during story POST creation. You must set it via a separate PUT call after creating the story:

```bash
# After creating the story, update it with project_phase
curl -s -u "$SN_USER:$SN_PASS" -X PUT \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_story/$STORY_SYS_ID" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"project_phase\": \"$PHASE_SYS_ID\",
    \"effort\": \"1970-01-01 08:00:00\",
    \"assignment_group\": \"$GROUP_SYS_ID\"
  }}"
```

**Recommended workflow**: Create all stories first (POST), then batch-update them with `project_phase`, `effort`, and `assignment_group` via PUT.

---

## Phase Nesting Constraints (ServiceNow Design Rules)

**These are ServiceNow platform design constraints — do NOT bypass them via API:**

### Agile Phases
1. **Agile phases (`phase_type: "agile"`) must be TOP-LEVEL only** — direct children of the project. They cannot be nested under other phases.
2. **Agile phases cannot have child pm_project_task records.** They hold stories only (linked via `project_phase` field on rm_story).
3. **Do NOT nest agile phases under waterfall phases.** While the API may allow it (bypassing UI validation), this is not the intended design and causes UI issues.

### Waterfall Phases
4. **Only waterfall phases support nested task hierarchy.** Waterfall phases can have child tasks, sub-phases, and milestones.
5. **Milestones must be under waterfall phases** (or directly under the project). They cannot be created under agile phases.

### Choosing the Right Architecture

**Option A: Pure Waterfall** — For projects needing nested task hierarchy with assignments.
```
Project (pm_project)
  └── Phase: ITSM Catalogs (pm_project_task, phase_type: "waterfall")
        ├── Task: Employee Onboarding (pm_project_task, phase_type: "waterfall", assigned_to: Fares)
        │     ├── Task: Prepare automation (pm_project_task, assigned_to: Vlad)
        │     ├── Task: Record video English (pm_project_task, assigned_to: Igor)
        │     └── Task: Record video Arabic (pm_project_task, assigned_to: Fares)
        ├── Task: Termination (pm_project_task, phase_type: "waterfall", assigned_to: Andrii)
        ├── Milestone: Week 1 Review (pm_project_task, milestone: "true")
        └── Milestone: Phase Complete (pm_project_task, milestone: "true")
```

**Option B: Flat Agile Phases + Stories** — For agile teams using backlogs and sprints.
```
Project (pm_project)
  ├── Phase: Employee Onboarding (pm_project_task, phase_type: "agile") ← stories link here
  ├── Phase: Termination (pm_project_task, phase_type: "agile") ← stories link here
  ├── Phase: Service Catalog (pm_project_task, phase_type: "agile") ← stories link here
  └── Phase: Milestones (pm_project_task, phase_type: "waterfall")
        ├── Milestone: Week 1 Review (pm_project_task, milestone: "true")
        └── Milestone: Phase Complete (pm_project_task, milestone: "true")
```
In Option B, all agile phases are flat (direct children of the project). Stories reference their agile phase via `project_phase` (set via PUT). Use a separate waterfall phase to hold milestones.

**Option C: Hybrid** — Waterfall container with waterfall tasks + separate agile phases at project level.
```
Project (pm_project)
  ├── Phase: ITSM Catalogs (pm_project_task, phase_type: "waterfall")
  │     ├── Task: Employee Onboarding (pm_project_task, assigned_to: Fares)
  │     ├── Task: Termination (pm_project_task, assigned_to: Andrii)
  │     └── Milestone: Phase Complete (pm_project_task, milestone: "true")
  ├── Agile Phase: Sprint 1 (pm_project_task, phase_type: "agile") ← stories link here
  └── Agile Phase: Sprint 2 (pm_project_task, phase_type: "agile") ← stories link here
```

---

## Agile Board Setup

When creating a project, ALWAYS ask the user if they want an agile board. If yes, follow these steps **after** project creation and **before** creating phases.

### Step A: Create Agile Group

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

### Step B: Create Backlog

```bash
BACKLOG_SYS_ID=$(curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/backlog_definition" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"name\": \"$PROJECT_NUMBER $PROJECT_NAME\",
    \"shared_with_groups\": \"$GROUP_SYS_ID\",
    \"owner\": \"$CURRENT_USER_SYS_ID\",
    \"u_project\": \"$PROJECT_SYS_ID\",
    \"filter\": \"sys_class_name=rm_story^active=true^sprintISEMPTY^u_project=$PROJECT_SYS_ID\"
  }}" | jq -r '.result.sys_id')
echo "Backlog sys_id: $BACKLOG_SYS_ID"
```

### Step C: Link Board to Project

```bash
curl -s -u "$SN_USER:$SN_PASS" -X PUT \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project/$PROJECT_SYS_ID" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {
    \"u_default_agile_teams\": \"$GROUP_SYS_ID\",
    \"backlog_definition\": \"$BACKLOG_SYS_ID\"
  }}"
```

### Step D: Add Group to Stories

When creating stories, include the `assignment_group` field with the agile group sys_id:
```json
"assignment_group": "$GROUP_SYS_ID"
```

---

## Import Checklist

Before creating any project, verify you have:

- [ ] Company sys_id resolved from `core_company`
- [ ] Commercial/Contract Model value identified (ask user if not in SOW)
- [ ] Payment Source value identified (ask user if not in SOW)
- [ ] Project Type value identified (only if company != "Mobiz IT"; ask user if not in SOW)
- [ ] Planned effort (SOW) total hours calculated
- [ ] Approved start/end dates from SOW
- [ ] Business case text from SOW
- [ ] In scope text from SOW
- [ ] User decision on agile board (ALWAYS ASK)

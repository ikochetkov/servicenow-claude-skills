# AI Bridge REST API Reference for SPM Operations

The AI Bridge is a REST adapter installed on ServiceNow instances that uses GlideRecord internally. This bypasses the limitations of the standard Table API (such as restricted field writes, ACL interference, and incomplete reference handling). All SPM record creation and querying should go through the AI Bridge endpoints documented here.

## API Basics

| Property | Value |
|---|---|
| Base URL | `https://{instance}.service-now.com/api/1851835/ai_adapter_rest/{tableName}` |
| Authentication | Basic Auth (admin credentials) |
| Methods | GET (query), POST (create), PUT (update) |
| Content-Type | `application/json` (for POST and PUT) |
| Body Format | `{"data": {"field1": "value1", "field2": "value2"}}` |

### Response Format

**Success (POST/PUT):**
```json
{
  "result": {
    "sys_id": "abc123def456...",
    "table": "pm_project",
    "field1": "value1"
  },
  "meta": {
    "fields_set": ["field1", "field2"],
    "fields_skipped": [],
    "message": "Record created successfully"
  }
}
```

**Success (GET):**
```json
{
  "result": [
    {"sys_id": "abc123...", "short_description": "Project A", ...},
    {"sys_id": "def456...", "short_description": "Project B", ...}
  ]
}
```

**Error:**
```json
{
  "error": {
    "message": "Record not found",
    "detail": "Could not find record with sys_id xyz in table pm_project"
  }
}
```

### Query Parameters for GET

| Parameter | Description | Example |
|---|---|---|
| `sysparm_query` | Encoded query string | `state=-5^project_manager=<sys_id>` |
| `sysparm_fields` | Comma-separated field list | `sys_id,short_description,state` |
| `sysparm_limit` | Maximum records returned (default: 100) | `10` |
| `sysparm_offset` | Pagination offset | `0` |
| `sysparm_display_value` | Return display values | `true`, `false`, or `all` |
| `sys_id` | Retrieve a single record by sys_id | `abc123def456...` |

---

## 1. Setup and Authentication

### Shell Variables

Set these environment variables before running any commands. All curl examples in this document reference them.

```bash
export SN_INSTANCE="https://devXXXXXX.service-now.com"
export SN_USER="admin"
export SN_PASS="password"
```

### Basic Auth Pattern

Every request uses `-u "$SN_USER:$SN_PASS"` for authentication:

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project?sysparm_limit=1"
```

### Test Connectivity

Verify you can reach the AI Bridge by querying a single project record:

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project?sysparm_limit=1" | jq .
```

If the connection is working, you will receive a JSON response with a `result` array. If authentication fails, you will receive a 401 status with an error message.

---

## 2. User Resolution

Before creating any SPM records that reference users (project managers, resource assignments, task owners), you must resolve the user's `sys_id` from the `sys_user` table. SPM reference fields require the sys_id, not the display name.

### Find User by Name

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/sys_user?sysparm_query=name=Abel Tuter&sysparm_fields=sys_id,name,email,user_name" | jq .
```

### Find User by Email

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/sys_user?sysparm_query=email=abel.tuter@example.com&sysparm_fields=sys_id,name,email,user_name" | jq .
```

### Find User by Username

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/sys_user?sysparm_query=user_name=abel.tuter&sysparm_fields=sys_id,name,email,user_name" | jq .
```

### Search Users by Partial Name

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/sys_user?sysparm_query=nameLIKEAbel&sysparm_fields=sys_id,name,email&sysparm_limit=10" | jq .
```

### Extract sys_id from Response

```bash
USER_SYS_ID=$(curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/sys_user?sysparm_query=name=Abel Tuter&sysparm_fields=sys_id" | jq -r '.result[0].sys_id')

echo "User sys_id: $USER_SYS_ID"
```

---

## 3. Portfolio Operations (pm_portfolio)

Portfolios are the top-level organizational container in SPM. Programs and projects roll up into portfolios.

### GET All Portfolios

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_portfolio?sysparm_fields=sys_id,short_description,owner,state&sysparm_limit=50" | jq .
```

### GET Portfolio by sys_id

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_portfolio?sys_id=PORTFOLIO_SYS_ID&sysparm_fields=sys_id,short_description,owner,state" | jq .
```

### POST Create Portfolio

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Digital Transformation Portfolio",
      "owner": "USER_SYS_ID",
      "state": "2"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_portfolio" | jq .
```

**Key fields:**
| Field | Type | Description |
|---|---|---|
| `short_description` | String | Portfolio name |
| `owner` | Reference (sys_user) | Portfolio owner sys_id |
| `state` | Integer | Portfolio state |

### PUT Update Portfolio

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Digital Transformation Portfolio - Updated",
      "state": "2"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_portfolio?sys_id=PORTFOLIO_SYS_ID" | jq .
```

---

## 4. Program Operations (pm_program)

Programs group related projects under a portfolio. A program has a program manager and belongs to a portfolio.

### GET All Programs

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_program?sysparm_fields=sys_id,short_description,pm_portfolio,program_manager,state&sysparm_limit=50" | jq .
```

### GET Programs in a Portfolio

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_program?sysparm_query=pm_portfolio=PORTFOLIO_SYS_ID&sysparm_fields=sys_id,short_description,program_manager,state" | jq .
```

### POST Create Program

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Cloud Migration Program",
      "pm_portfolio": "PORTFOLIO_SYS_ID",
      "program_manager": "USER_SYS_ID"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_program" | jq .
```

**Key fields:**
| Field | Type | Description |
|---|---|---|
| `short_description` | String | Program name |
| `pm_portfolio` | Reference (pm_portfolio) | Parent portfolio sys_id |
| `program_manager` | Reference (sys_user) | Program manager sys_id |
| `state` | Integer | Program state |

### PUT Update Program

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Cloud Migration Program - Phase 2",
      "program_manager": "NEW_USER_SYS_ID"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_program?sys_id=PROGRAM_SYS_ID" | jq .
```

---

## 5. Project Operations (pm_project)

Projects are the core entity in SPM. They belong to programs, have phases (project tasks), milestones, resources, and track state through a lifecycle.

### Project State Values

| Value | Label |
|---|---|
| `-5` | Draft |
| `-4` | Pending |
| `1` | Open |
| `2` | Work in Progress |
| `3` | Closed Complete |
| `4` | Closed Incomplete |
| `7` | Cancelled |

### GET All Projects

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project?sysparm_fields=sys_id,short_description,state,project_manager,start_date,end_date&sysparm_limit=50" | jq .
```

### GET Projects by State

```bash
# Get all draft projects
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project?sysparm_query=state=-5&sysparm_fields=sys_id,short_description,state,project_manager" | jq .
```

### GET Projects by Project Manager

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project?sysparm_query=project_manager=USER_SYS_ID&sysparm_fields=sys_id,short_description,state,start_date,end_date" | jq .
```

### GET Projects with Combined Query

```bash
# Draft projects for a specific project manager
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project?sysparm_query=state=-5^project_manager=USER_SYS_ID&sysparm_fields=sys_id,short_description,state" | jq .
```

### GET Single Project by sys_id

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project?sys_id=PROJECT_SYS_ID" | jq .
```

### GET Projects with Display Values

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project?sysparm_display_value=true&sysparm_fields=sys_id,short_description,state,project_manager&sysparm_limit=10" | jq .
```

### POST Create Project (with Mobiz Mandatory Fields)

> **IMPORTANT**: Always include Mobiz mandatory fields. See [mobiz-mandatory-fields.md](mobiz-mandatory-fields.md) for details.

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Website Redesign Project",
      "start_date": "2026-03-01",
      "end_date": "2026-09-30",
      "state": "-5",
      "project_manager": "USER_SYS_ID",
      "description": "Complete redesign of the corporate website.",
      "company": "COMPANY_SYS_ID",
      "x_mobit_spm_enh_commercial_contract_model": "t&m",
      "x_mobit_spm_enh_payment_source": "client",
      "x_mobit_spm_enh_project_type": "Billable",
      "x_mobit_spm_enh_planned_effort_sow": "960",
      "approved_start_date": "2026-03-01",
      "approved_end_date": "2026-09-30",
      "business_case": "<p>Business justification from SOW</p>",
      "in_scope": "<p>Project scope from SOW</p>"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project" | jq .
```

### POST Create Project Under a Program

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Database Migration Project",
      "start_date": "2026-04-01",
      "end_date": "2026-08-31",
      "state": "-5",
      "project_manager": "USER_SYS_ID",
      "pm_program": "PROGRAM_SYS_ID",
      "description": "Migrate legacy databases to cloud infrastructure.",
      "company": "COMPANY_SYS_ID",
      "x_mobit_spm_enh_commercial_contract_model": "ff",
      "x_mobit_spm_enh_payment_source": "client",
      "x_mobit_spm_enh_project_type": "Billable",
      "x_mobit_spm_enh_planned_effort_sow": "1200",
      "approved_start_date": "2026-04-01",
      "approved_end_date": "2026-08-31",
      "business_case": "<p>Business case</p>",
      "in_scope": "<p>Scope</p>"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project" | jq .
```

**Key fields:**
| Field | Type | Description |
|---|---|---|
| `short_description` | String | Project name |
| `description` | String | Detailed project description |
| `start_date` | Date (YYYY-MM-DD) | Project start date |
| `end_date` | Date (YYYY-MM-DD) | Project end date |
| `state` | Integer | Project state (see table above) |
| `project_manager` | Reference (sys_user) | Project manager sys_id |
| `pm_program` | Reference (pm_program) | Parent program sys_id |
| `pm_portfolio` | Reference (pm_portfolio) | Parent portfolio sys_id |
| `priority` | Integer | Priority (1=Critical, 2=High, 3=Moderate, 4=Low, 5=Planning) |
| `risk` | Integer | Risk level |
| `company` | Reference (core_company) | **MANDATORY (Mobiz)** — Company sys_id |
| `x_mobit_spm_enh_commercial_contract_model` | Choice | **MANDATORY (Mobiz)** — `staff_aug`, `boh`, `support`, `ff`, `t&m` |
| `x_mobit_spm_enh_payment_source` | Choice | **MANDATORY (Mobiz)** — `client`, `mobiz`, `ecif`, `amm`, `other` |
| `x_mobit_spm_enh_project_type` | Choice | **MANDATORY when company != "Mobiz IT"** — `Presales`, `Billable`, `Internal` |
| `x_mobit_spm_enh_planned_effort_sow` | Integer | **MANDATORY (Mobiz)** — Total SOW hours |
| `approved_start_date` | Date | **MANDATORY (Mobiz)** — Approved start |
| `approved_end_date` | Date | **MANDATORY (Mobiz)** — Approved end |
| `business_case` | HTML | **MANDATORY (Mobiz)** — Business justification |
| `in_scope` | HTML | **MANDATORY (Mobiz)** — Scope description |

### PUT Update Project State

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "state": "1"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project?sys_id=PROJECT_SYS_ID" | jq .
```

### PUT Update Project Dates

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "start_date": "2026-04-01",
      "end_date": "2026-12-31"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project?sys_id=PROJECT_SYS_ID" | jq .
```

### PUT Update Multiple Project Fields

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Website Redesign Project - Phase 2",
      "state": "2",
      "project_manager": "NEW_USER_SYS_ID",
      "end_date": "2026-12-15"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project?sys_id=PROJECT_SYS_ID" | jq .
```

---

## 6. Project Task / Phase Operations (pm_project_task)

Project tasks represent phases, sub-phases, and work items within a project. Phases are top-level tasks whose `parent` is the project itself. Sub-phases have a `parent` set to the phase sys_id.

### Task State Values

| Value | Label |
|---|---|
| `-5` | Pending |
| `1` | Open |
| `2` | Work in Progress |
| `3` | Closed Complete |
| `4` | Closed Incomplete |
| `7` | Cancelled |

### POST Create Phase (Top-Level Task Under a Project)

The `parent` field must be set to the project sys_id to make this a direct phase of the project.

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Phase 1: Discovery and Planning",
      "parent": "PROJECT_SYS_ID",
      "start_date": "2026-03-01",
      "end_date": "2026-04-15",
      "state": "-5",
      "assigned_to": "USER_SYS_ID",
      "description": "Initial discovery phase including stakeholder interviews, requirements gathering, and project planning."
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task" | jq .
```

### POST Create Sub-Phase (Task Under a Phase)

Set `parent` to the phase sys_id to nest this under an existing phase.

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Requirements Gathering",
      "parent": "PHASE_SYS_ID",
      "start_date": "2026-03-01",
      "end_date": "2026-03-21",
      "state": "-5",
      "assigned_to": "USER_SYS_ID"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task" | jq .
```

### GET All Phases for a Project

Query for tasks whose `parent` is the project sys_id to get top-level phases.

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task?sysparm_query=parent=PROJECT_SYS_ID&sysparm_fields=sys_id,short_description,parent,state,start_date,end_date,assigned_to" | jq .
```

### GET Sub-Phases Under a Phase

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task?sysparm_query=parent=PHASE_SYS_ID&sysparm_fields=sys_id,short_description,parent,state,start_date,end_date,assigned_to" | jq .
```

### GET All Tasks for a Project (All Levels)

Use the `top_task` field to find all tasks at any nesting level that belong to a project.

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task?sysparm_query=top_task=PROJECT_SYS_ID&sysparm_fields=sys_id,short_description,parent,state,start_date,end_date&sysparm_limit=200" | jq .
```

### PUT Update Task State

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "state": "2"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task?sys_id=TASK_SYS_ID" | jq .
```

### PUT Update Task Assignment

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "assigned_to": "NEW_USER_SYS_ID",
      "state": "1"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task?sys_id=TASK_SYS_ID" | jq .
```

**Key fields:**
| Field | Type | Description |
|---|---|---|
| `short_description` | String | Task / phase name |
| `description` | String | Detailed description |
| `parent` | Reference | Project sys_id (for phases) or phase sys_id (for sub-phases) |
| `top_task` | Reference | The root project sys_id (auto-set, useful for querying) |
| `start_date` | Date (YYYY-MM-DD) | Task start date |
| `end_date` | Date (YYYY-MM-DD) | Task end date |
| `state` | Integer | Task state (see table above) |
| `assigned_to` | Reference (sys_user) | Assigned user sys_id |
| `percent_complete` | Integer | Completion percentage (0-100) |
| `priority` | Integer | Priority level |

---

## 7. Milestone Operations (pm_milestone)

Milestones are key checkpoints within a project, linked to a parent task (phase) and the overall project.

### POST Create Milestone

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Requirements Sign-Off",
      "parent": "PHASE_SYS_ID",
      "project": "PROJECT_SYS_ID",
      "date": "2026-04-15",
      "state": "-5"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_milestone" | jq .
```

### POST Create Milestone at Project Level

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Go-Live Date",
      "project": "PROJECT_SYS_ID",
      "date": "2026-09-30",
      "state": "-5"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_milestone" | jq .
```

### GET Milestones for a Project

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_milestone?sysparm_query=project=PROJECT_SYS_ID&sysparm_fields=sys_id,short_description,parent,project,date,state" | jq .
```

### GET Milestones for a Specific Phase

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_milestone?sysparm_query=parent=PHASE_SYS_ID&sysparm_fields=sys_id,short_description,date,state" | jq .
```

### PUT Update Milestone

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "state": "3",
      "date": "2026-04-20"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_milestone?sys_id=MILESTONE_SYS_ID" | jq .
```

**Key fields:**
| Field | Type | Description |
|---|---|---|
| `short_description` | String | Milestone name |
| `parent` | Reference (pm_project_task) | Parent phase sys_id |
| `project` | Reference (pm_project) | Project sys_id |
| `date` | Date (YYYY-MM-DD) | Milestone target date |
| `state` | Integer | Milestone state |

---

## 8. Epic Operations (rm_epic)

Epics are large bodies of work in Agile planning within SPM. They can span across sprints and contain multiple stories.

### POST Create Epic

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "User Authentication System",
      "state": "1",
      "story_points": "40",
      "start_date": "2026-03-01",
      "end_date": "2026-06-30",
      "description": "Implement complete user authentication including SSO, MFA, and role-based access control."
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_epic" | jq .
```

### POST Create Epic Linked to a Project

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Payment Processing Integration",
      "state": "1",
      "story_points": "60",
      "start_date": "2026-04-01",
      "end_date": "2026-07-31",
      "project": "PROJECT_SYS_ID"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_epic" | jq .
```

### GET All Epics

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_epic?sysparm_fields=sys_id,short_description,state,story_points,start_date,end_date&sysparm_limit=50" | jq .
```

### GET Epics by State

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_epic?sysparm_query=state=1&sysparm_fields=sys_id,short_description,story_points,start_date,end_date" | jq .
```

### PUT Update Epic

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "state": "2",
      "story_points": "55"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_epic?sys_id=EPIC_SYS_ID" | jq .
```

**Key fields:**
| Field | Type | Description |
|---|---|---|
| `short_description` | String | Epic name |
| `description` | String | Detailed description |
| `state` | Integer | Epic state |
| `story_points` | Integer | Total story points estimate |
| `start_date` | Date (YYYY-MM-DD) | Epic start date |
| `end_date` | Date (YYYY-MM-DD) | Epic end date |
| `project` | Reference (pm_project) | Associated project sys_id |

---

## 9. Story Operations (rm_story)

Stories are individual units of work within an epic. They represent specific user-facing functionality or deliverables.

### POST Create Story

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Implement login page with SSO support",
      "epic": "EPIC_SYS_ID",
      "story_points": "8",
      "assigned_to": "USER_SYS_ID",
      "planned_effort": "40:00:00",
      "state": "1",
      "acceptance_criteria": "1. User can log in with username/password\n2. SSO redirect works for configured identity providers\n3. Error messages display for invalid credentials\n4. Session persists across page refreshes"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_story" | jq .
```

### POST Create Story with Minimal Fields

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Add password reset flow",
      "epic": "EPIC_SYS_ID",
      "story_points": "5",
      "state": "1"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_story" | jq .
```

### GET Stories by Epic

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_story?sysparm_query=epic=EPIC_SYS_ID&sysparm_fields=sys_id,short_description,epic,story_points,assigned_to,state,acceptance_criteria" | jq .
```

### GET Stories Assigned to a User

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_story?sysparm_query=assigned_to=USER_SYS_ID&sysparm_fields=sys_id,short_description,epic,story_points,state" | jq .
```

### GET Stories by State

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_story?sysparm_query=state=2&sysparm_fields=sys_id,short_description,epic,story_points,assigned_to" | jq .
```

### PUT Update Story

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "state": "2",
      "assigned_to": "USER_SYS_ID",
      "story_points": "10"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_story?sys_id=STORY_SYS_ID" | jq .
```

**Key fields:**
| Field | Type | Description |
|---|---|---|
| `short_description` | String | Story title |
| `description` | String | Detailed description |
| `epic` | Reference (rm_epic) | Parent epic sys_id |
| `story_points` | Integer | Story point estimate |
| `assigned_to` | Reference (sys_user) | Assigned developer sys_id |
| `planned_effort` | Duration (HH:MM:SS) | Planned effort in hours |
| `state` | Integer | Story state |
| `acceptance_criteria` | String | Acceptance criteria text |
| `priority` | Integer | Priority level |

---

## 10. Resource Plan Operations (resource_plan)

Resource plans allocate team members to project tasks, defining who is working on what and for how long.

### POST Create Resource Plan

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "user": "USER_SYS_ID",
      "task": "PROJECT_SYS_ID",
      "planned_hours": "160",
      "start_date": "2026-03-01",
      "end_date": "2026-06-30",
      "resource_type": "project_team",
      "state": "1"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/resource_plan" | jq .
```

### POST Create Resource Plan for a Specific Phase

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "user": "USER_SYS_ID",
      "task": "PHASE_SYS_ID",
      "planned_hours": "80",
      "start_date": "2026-03-01",
      "end_date": "2026-04-15",
      "state": "1"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/resource_plan" | jq .
```

### GET Resource Plans for a Project

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/resource_plan?sysparm_query=task=PROJECT_SYS_ID&sysparm_fields=sys_id,user,task,planned_hours,start_date,end_date,state" | jq .
```

### GET Resource Plans for a User

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/resource_plan?sysparm_query=user=USER_SYS_ID&sysparm_fields=sys_id,user,task,planned_hours,start_date,end_date,state" | jq .
```

### PUT Update Resource Plan

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "planned_hours": "200",
      "end_date": "2026-07-31"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/resource_plan?sys_id=RESOURCE_PLAN_SYS_ID" | jq .
```

**Key fields:**
| Field | Type | Description |
|---|---|---|
| `user` | Reference (sys_user) | Resource (person) sys_id |
| `task` | Reference (planned_task) | Project or task sys_id |
| `planned_hours` | Integer | Planned effort in hours |
| `start_date` | Date (YYYY-MM-DD) | Resource allocation start |
| `end_date` | Date (YYYY-MM-DD) | Resource allocation end |
| `resource_type` | String | Type of resource allocation |
| `state` | Integer | Resource plan state |

---

## 11. Demand Operations (dmn_demand)

Demands represent requests for work that may become projects. They flow through an approval process before being converted to projects.

### POST Create Demand

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "New CRM System Implementation",
      "description": "Request to implement a new CRM system to replace the legacy platform. Expected to improve sales team productivity by 30%.",
      "type": "project",
      "priority": "2",
      "requested_by": "USER_SYS_ID",
      "state": "1",
      "start_date": "2026-06-01",
      "end_date": "2026-12-31"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/dmn_demand" | jq .
```

### GET All Demands

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/dmn_demand?sysparm_fields=sys_id,short_description,state,type,priority,requested_by,start_date,end_date&sysparm_limit=50" | jq .
```

### GET Demands by State

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/dmn_demand?sysparm_query=state=1&sysparm_fields=sys_id,short_description,type,priority,requested_by" | jq .
```

### GET Demands Requested by a User

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/dmn_demand?sysparm_query=requested_by=USER_SYS_ID&sysparm_fields=sys_id,short_description,state,priority" | jq .
```

### PUT Update Demand

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "state": "2",
      "priority": "1"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/dmn_demand?sys_id=DEMAND_SYS_ID" | jq .
```

**Key fields:**
| Field | Type | Description |
|---|---|---|
| `short_description` | String | Demand title |
| `description` | String | Detailed description |
| `type` | String | Demand type (e.g., "project") |
| `priority` | Integer | Priority (1=Critical, 2=High, 3=Moderate, 4=Low) |
| `requested_by` | Reference (sys_user) | Requestor sys_id |
| `state` | Integer | Demand state |
| `start_date` | Date (YYYY-MM-DD) | Requested start date |
| `end_date` | Date (YYYY-MM-DD) | Requested end date |

---

## 12. Dependency Operations (planned_task_rel_planned_task)

Dependencies define predecessor/successor relationships between project tasks, phases, or milestones. These control scheduling logic such that a successor cannot start until its predecessor completes.

### POST Create Dependency (Predecessor/Successor)

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "parent": "PREDECESSOR_TASK_SYS_ID",
      "child": "SUCCESSOR_TASK_SYS_ID",
      "type": "fs"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/planned_task_rel_planned_task" | jq .
```

### Dependency Type Values

| Value | Label | Description |
|---|---|---|
| `fs` | Finish-to-Start | Successor starts after predecessor finishes (most common) |
| `ss` | Start-to-Start | Both tasks start at the same time |
| `ff` | Finish-to-Finish | Both tasks finish at the same time |
| `sf` | Start-to-Finish | Successor finishes when predecessor starts |

### POST Create Finish-to-Start Dependency Between Phases

```bash
# Phase 2 cannot start until Phase 1 finishes
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "parent": "PHASE_1_SYS_ID",
      "child": "PHASE_2_SYS_ID",
      "type": "fs"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/planned_task_rel_planned_task" | jq .
```

### GET Dependencies for a Task (as Predecessor)

Find all tasks that depend on a given task (where this task is the predecessor).

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/planned_task_rel_planned_task?sysparm_query=parent=TASK_SYS_ID&sysparm_fields=sys_id,parent,child,type" | jq .
```

### GET Dependencies for a Task (as Successor)

Find all tasks that a given task depends on (where this task is the successor).

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/planned_task_rel_planned_task?sysparm_query=child=TASK_SYS_ID&sysparm_fields=sys_id,parent,child,type" | jq .
```

### GET All Dependencies Involving a Task

```bash
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/planned_task_rel_planned_task?sysparm_query=parent=TASK_SYS_ID^ORchild=TASK_SYS_ID&sysparm_fields=sys_id,parent,child,type" | jq .
```

**Key fields:**
| Field | Type | Description |
|---|---|---|
| `parent` | Reference (planned_task) | Predecessor task sys_id |
| `child` | Reference (planned_task) | Successor task sys_id |
| `type` | String | Dependency type: fs, ss, ff, sf |

---

## 13. Batch Operations Pattern

When building a complete project structure (project, phases, tasks, milestones, dependencies), you must create records sequentially because each subsequent record references the sys_id of a previously created record. Use `jq` to extract the sys_id from each response and store it in a shell variable for the next request.

### Extract sys_id from a Response

```bash
RESPONSE=$(curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "My Project",
      "state": "-5"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project")

PROJECT_SYS_ID=$(echo "$RESPONSE" | jq -r '.result.sys_id')
echo "Created project: $PROJECT_SYS_ID"
```

### Full Example: Create a Project with Phases, Milestones, and Dependencies

```bash
#!/bin/bash
set -e

# Prerequisites: SN_INSTANCE, SN_USER, SN_PASS must be set
# Prerequisites: USER_SYS_ID must be resolved (see Section 2)

# --- Step 1: Create the project ---
echo "Creating project..."
PROJECT_RESPONSE=$(curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Q3 Platform Upgrade",
      "start_date": "2026-03-01",
      "end_date": "2026-09-30",
      "state": "-5",
      "project_manager": "'"$USER_SYS_ID"'",
      "description": "Full platform upgrade including infrastructure, application, and data migration."
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project")

PROJECT_SYS_ID=$(echo "$PROJECT_RESPONSE" | jq -r '.result.sys_id')
echo "Project created: $PROJECT_SYS_ID"

# --- Step 2: Create Phase 1 ---
echo "Creating Phase 1..."
PHASE1_RESPONSE=$(curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Phase 1: Planning",
      "parent": "'"$PROJECT_SYS_ID"'",
      "start_date": "2026-03-01",
      "end_date": "2026-04-30",
      "state": "-5"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task")

PHASE1_SYS_ID=$(echo "$PHASE1_RESPONSE" | jq -r '.result.sys_id')
echo "Phase 1 created: $PHASE1_SYS_ID"

# --- Step 3: Create Phase 2 ---
echo "Creating Phase 2..."
PHASE2_RESPONSE=$(curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Phase 2: Implementation",
      "parent": "'"$PROJECT_SYS_ID"'",
      "start_date": "2026-05-01",
      "end_date": "2026-08-31",
      "state": "-5"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task")

PHASE2_SYS_ID=$(echo "$PHASE2_RESPONSE" | jq -r '.result.sys_id')
echo "Phase 2 created: $PHASE2_SYS_ID"

# --- Step 4: Create Phase 3 ---
echo "Creating Phase 3..."
PHASE3_RESPONSE=$(curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Phase 3: Go-Live and Support",
      "parent": "'"$PROJECT_SYS_ID"'",
      "start_date": "2026-09-01",
      "end_date": "2026-09-30",
      "state": "-5"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project_task")

PHASE3_SYS_ID=$(echo "$PHASE3_RESPONSE" | jq -r '.result.sys_id')
echo "Phase 3 created: $PHASE3_SYS_ID"

# --- Step 5: Create a milestone at the end of Phase 1 ---
echo "Creating milestone..."
MILESTONE_RESPONSE=$(curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "short_description": "Planning Complete",
      "parent": "'"$PHASE1_SYS_ID"'",
      "project": "'"$PROJECT_SYS_ID"'",
      "date": "2026-04-30"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_milestone")

MILESTONE_SYS_ID=$(echo "$MILESTONE_RESPONSE" | jq -r '.result.sys_id')
echo "Milestone created: $MILESTONE_SYS_ID"

# --- Step 6: Create dependency: Phase 2 depends on Phase 1 ---
echo "Creating dependency: Phase 1 -> Phase 2..."
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "parent": "'"$PHASE1_SYS_ID"'",
      "child": "'"$PHASE2_SYS_ID"'",
      "type": "fs"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/planned_task_rel_planned_task" | jq .

# --- Step 7: Create dependency: Phase 3 depends on Phase 2 ---
echo "Creating dependency: Phase 2 -> Phase 3..."
curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "parent": "'"$PHASE2_SYS_ID"'",
      "child": "'"$PHASE3_SYS_ID"'",
      "type": "fs"
    }
  }' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/planned_task_rel_planned_task" | jq .

echo ""
echo "=== Project Structure Created ==="
echo "Project:    $PROJECT_SYS_ID"
echo "Phase 1:    $PHASE1_SYS_ID"
echo "Phase 2:    $PHASE2_SYS_ID"
echo "Phase 3:    $PHASE3_SYS_ID"
echo "Milestone:  $MILESTONE_SYS_ID"
echo "Dependencies: Phase 1 -> Phase 2 -> Phase 3"
```

### Utility: Extract sys_id with Error Checking

```bash
extract_sys_id() {
  local response="$1"
  local label="$2"
  local sys_id=$(echo "$response" | jq -r '.result.sys_id // empty')

  if [ -z "$sys_id" ]; then
    echo "ERROR: Failed to create $label" >&2
    echo "$response" | jq . >&2
    return 1
  fi

  echo "$sys_id"
}

# Usage:
RESPONSE=$(curl -s -u "$SN_USER:$SN_PASS" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"data": {"short_description": "Test Project", "state": "-5"}}' \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project")

PROJECT_SYS_ID=$(extract_sys_id "$RESPONSE" "project") || exit 1
echo "Project: $PROJECT_SYS_ID"
```

---

## 14. Error Handling

### Common Errors and Solutions

**401 Unauthorized**
```json
{"error": {"message": "User Not Authenticated", "detail": "..."}}
```
Cause: Invalid credentials or user account is locked.
Solution: Verify `SN_USER` and `SN_PASS` are correct. Ensure the admin account is active.

**403 Forbidden**
```json
{"error": {"message": "Insufficient rights", "detail": "..."}}
```
Cause: The user does not have the required role (e.g., `project_manager`, `admin`).
Solution: Verify the user has SPM-related roles assigned in ServiceNow.

**404 Not Found**
```json
{"error": {"message": "Record not found", "detail": "..."}}
```
Cause: The sys_id in the query does not match any record, or the table name is incorrect.
Solution: Double-check the sys_id and table name in the URL.

**Invalid Table Name**
```json
{"error": {"message": "Invalid table", "detail": "Table 'xyz' does not exist"}}
```
Cause: The table name in the URL path is misspelled.
Solution: Verify the table name. Common SPM tables: `pm_project`, `pm_project_task`, `pm_milestone`, `pm_portfolio`, `pm_program`, `rm_epic`, `rm_story`, `resource_plan`, `dmn_demand`, `planned_task_rel_planned_task`.

**Field Not Set (Skipped)**
Check the `meta.fields_skipped` array in the response. If a field you sent appears there, it means:
- The field name is misspelled
- The field does not exist on that table
- The field is read-only or calculated
- The value format is incorrect for that field type

Example response with skipped fields:
```json
{
  "result": {"sys_id": "abc123..."},
  "meta": {
    "fields_set": ["short_description", "state"],
    "fields_skipped": ["nonexistent_field"],
    "message": "Record created successfully"
  }
}
```

**Reference Field Errors**
If a reference field value (like `project_manager` or `parent`) is not a valid sys_id, the field will either be skipped or set to empty. Always verify that:
1. The referenced record exists
2. You are using the sys_id, not the display value
3. The sys_id is the correct 32-character hex string

### Defensive Scripting Pattern

```bash
create_record() {
  local table="$1"
  local data="$2"
  local label="$3"

  local response=$(curl -s -w "\n%{http_code}" -u "$SN_USER:$SN_PASS" \
    -X POST \
    -H "Content-Type: application/json" \
    -d "$data" \
    "$SN_INSTANCE/api/1851835/ai_adapter_rest/$table")

  local http_code=$(echo "$response" | tail -1)
  local body=$(echo "$response" | sed '$d')

  if [ "$http_code" -ne 200 ] && [ "$http_code" -ne 201 ]; then
    echo "ERROR: HTTP $http_code creating $label" >&2
    echo "$body" | jq . >&2
    return 1
  fi

  local sys_id=$(echo "$body" | jq -r '.result.sys_id // empty')
  if [ -z "$sys_id" ]; then
    echo "ERROR: No sys_id in response for $label" >&2
    echo "$body" | jq . >&2
    return 1
  fi

  local skipped=$(echo "$body" | jq -r '.meta.fields_skipped | length')
  if [ "$skipped" -gt 0 ]; then
    echo "WARNING: $skipped field(s) skipped for $label:" >&2
    echo "$body" | jq -r '.meta.fields_skipped[]' >&2
  fi

  echo "$sys_id"
}

# Usage:
PROJECT_SYS_ID=$(create_record "pm_project" \
  '{"data": {"short_description": "Test", "state": "-5"}}' \
  "project") || exit 1

echo "Created project: $PROJECT_SYS_ID"
```

### Timeout and Connectivity Issues

For large batch operations, individual requests may time out. Add timeout and retry logic:

```bash
curl -s --connect-timeout 10 --max-time 30 -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/pm_project?sysparm_limit=1" | jq .
```

If you receive empty responses or connection resets, check:
1. The instance URL is correct (no trailing slash)
2. The instance is awake (dev instances hibernate after inactivity)
3. Network connectivity to the ServiceNow instance

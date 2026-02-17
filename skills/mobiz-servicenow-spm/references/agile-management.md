# Agile Management in ServiceNow SPM

## Overview

ServiceNow SPM includes Agile Development 2.0 (included with SPM Standard via the Agile Team $0 SKU). It provides epics, stories, sprints, backlogs, and board views for teams using Scrum, Kanban, or hybrid project management approaches.

Agile artifacts in SPM can be linked to traditional project management structures (projects, phases) for hybrid management, or used standalone for pure agile teams.

## Core Agile Tables

| Table | API Name | Purpose |
|-------|----------|---------|
| Epic | `rm_epic` | Large bodies of work decomposed into stories |
| Story | `rm_story` | User stories — the primary unit of agile work |
| Sprint | `rm_sprint` | Time-boxed iteration (typically 2 weeks) |
| Defect | `rm_defect` | Bugs/defects tracked alongside stories |
| Scrum Task | `rm_scrum_task` | Subtasks within a story |
| Release | `rm_release` | Groups sprints into a release |
| Theme | `rm_theme` | High-level strategic themes grouping epics |
| Feature | `rm_feature` | SAFe-level feature (between theme and epic) |

## Epic (rm_epic)

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `short_description` | String | Epic name/title |
| `description` | String | Detailed description |
| `state` | Choice | Draft, Ready, In Progress, Complete, Cancelled |
| `story_points` | Integer | Total story points (may auto-rollup from stories) |
| `start_date` | Date | Planned start |
| `end_date` | Date | Planned end |
| `assigned_to` | Reference (sys_user) | Epic owner |
| `product` | Reference | Product this epic belongs to |
| `theme` | Reference (rm_theme) | Parent theme |
| `release` | Reference (rm_release) | Target release |
| `priority` | Choice | 1-Critical, 2-High, 3-Moderate, 4-Low |
| `acceptance_criteria` | String | Criteria for epic completion |
| `color` | String | Color code for board display |

### Epic States
| Value | Label |
|-------|-------|
| draft | Draft |
| ready | Ready |
| in_progress | In Progress |
| complete | Complete |
| cancelled | Cancelled |

### Creating an Epic via AI Bridge
```bash
curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_epic" \
  -H "Content-Type: application/json" \
  -d '{"data": {
    "short_description": "Employee Lifecycle Management",
    "description": "Onboarding and offboarding automation",
    "state": "draft",
    "story_points": "30",
    "start_date": "2026-02-17",
    "end_date": "2026-02-21"
  }}'
```

## Story (rm_story)

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `short_description` | String | Story title |
| `description` | String | As a [role], I want [feature] so that [benefit] |
| `epic` | Reference (rm_epic) | Parent epic |
| `state` | Choice | Draft, Ready, Work in Progress, Complete, Accepted, Cancelled |
| `story_points` | Integer | Estimated complexity (Fibonacci: 1,2,3,5,8,13,21) |
| `assigned_to` | Reference (sys_user) | Developer assigned |
| `sprint` | Reference (rm_sprint) | Sprint this story is in |
| `planned_effort` | Duration | Planned hours |
| `actual_effort` | Duration | Actual hours spent |
| `acceptance_criteria` | String | Definition of done |
| `priority` | Choice | 1-Critical, 2-High, 3-Moderate, 4-Low |
| `blocked` | Boolean | Whether the story is blocked |
| `blocked_reason` | String | Why the story is blocked |
| `type` | Choice | Story, Spike, Enabler |
| `release` | Reference (rm_release) | Target release |
| `product` | Reference | Product this story belongs to |
| `classification` | Choice | Functional, Non-functional, Technical Debt |

### Story States
| Value | Label | Description |
|-------|-------|-------------|
| -6 | Draft | Initial state, not ready for sprint |
| -5 | Ready | Groomed and ready for sprint planning |
| 1 | Work in Progress | Currently being worked on |
| 2 | Testing | In QA/testing |
| 3 | Complete | Development complete, pending acceptance |
| 4 | Accepted | Product owner accepted |
| 7 | Cancelled | Story cancelled |

### Creating a Story via AI Bridge
```bash
curl -s -u "$SN_USER:$SN_PASS" -X POST \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_story" \
  -H "Content-Type: application/json" \
  -d '{"data": {
    "short_description": "Service Catalog Request Form (Arabic)",
    "description": "Create Arabic onboarding request form with fields: name, department, start date, manager, location",
    "epic": "<epic_sys_id>",
    "state": "-6",
    "story_points": "5",
    "assigned_to": "<user_sys_id>",
    "planned_effort": "28800",
    "acceptance_criteria": "Form submittable in Arabic UI"
  }}'
```

**Note on planned_effort**: ServiceNow stores duration fields in seconds. 8 hours = 28800 seconds. When using `sysparm_display_value=true`, it shows as "8 Hours".

## Sprint (rm_sprint)

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `short_description` | String | Sprint name (e.g., "Sprint 1 - Feb 2026") |
| `start_date` | Date | Sprint start |
| `end_date` | Date | Sprint end (typically start + 14 days) |
| `state` | Choice | Planning, In Progress, Complete, Closed |
| `release` | Reference (rm_release) | Parent release |
| `team` | Reference (sys_user_group) | Scrum team |
| `goal` | String | Sprint goal |
| `velocity` | Integer | Team velocity for this sprint |

### Sprint States
| Value | Label |
|-------|-------|
| -5 | Planning |
| 1 | In Progress |
| 2 | Complete |
| 3 | Closed |

## Defect (rm_defect)

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `short_description` | String | Defect title |
| `description` | String | Steps to reproduce |
| `state` | Choice | Draft, Ready, Work in Progress, Complete, Accepted, Cancelled |
| `severity` | Choice | 1-Critical, 2-High, 3-Moderate, 4-Low |
| `priority` | Choice | 1-Critical, 2-High, 3-Moderate, 4-Low |
| `assigned_to` | Reference (sys_user) | Developer assigned |
| `sprint` | Reference (rm_sprint) | Sprint |
| `epic` | Reference (rm_epic) | Related epic |
| `story_points` | Integer | Points for sizing |
| `found_in` | Reference (rm_release) | Release where defect was found |

## Scrum Task (rm_scrum_task)

Subtasks within a story for tracking individual pieces of work.

| Field | Type | Description |
|-------|------|-------------|
| `short_description` | String | Task name |
| `story` | Reference (rm_story) | Parent story |
| `state` | Choice | To Do, In Progress, Done |
| `assigned_to` | Reference (sys_user) | Task owner |
| `estimated_hours` | Float | Estimated hours |
| `remaining_hours` | Float | Hours remaining (for burndown) |
| `actual_hours` | Float | Actual hours spent |
| `type` | Choice | Development, Testing, Documentation, Design |

## Backlog Management

### Backlog Hierarchy
```
Theme (rm_theme)
  └── Epic (rm_epic)
        └── Story (rm_story)
              └── Scrum Task (rm_scrum_task)
```

### Backlog Grooming Workflow
1. **Create epics** from project requirements or SOW phases
2. **Decompose epics** into stories with acceptance criteria
3. **Estimate stories** using story points (team consensus)
4. **Prioritize backlog** by business value and dependencies
5. **Sprint planning**: Pull stories from backlog into sprint based on team velocity
6. **Break stories into scrum tasks** during sprint planning

### Querying the Backlog
```bash
# Get all stories in Draft/Ready state (backlog)
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_story?sysparm_query=stateIN-6,-5&sysparm_fields=sys_id,short_description,epic,story_points,priority&sysparm_display_value=all"

# Get stories for a specific epic
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_story?sysparm_query=epic=<epic_sys_id>&sysparm_fields=sys_id,short_description,state,story_points,assigned_to&sysparm_display_value=all"

# Get stories in a sprint
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/1851835/ai_adapter_rest/rm_story?sysparm_query=sprint=<sprint_sys_id>&sysparm_fields=sys_id,short_description,state,story_points,assigned_to&sysparm_display_value=all"
```

## Board Views

ServiceNow provides Scrum and Kanban board views:

### Scrum Board
- Columns: To Do, In Progress, Done
- Cards: Stories and defects
- Swimlanes: By assignee or epic
- Shows sprint burndown chart

### Kanban Board
- Configurable columns matching workflow states
- WIP limits per column
- No sprint boundaries — continuous flow

## Hybrid Project Management

SPM supports linking agile artifacts to traditional project structures:

### Linking Epics to Project Phases
Epics can be associated with project tasks (phases) to track agile work within a waterfall project structure. The link is typically through:
- Setting the epic's product or release to match the project
- Using custom reference fields to link epics to pm_project_task records
- Using the Agile board within the project workspace

### Linking Stories to Project Tasks
Stories can reference project tasks for reporting rollup:
- Story effort rolls up to the project task level
- Project managers see combined waterfall + agile progress
- Resource plans can cover both traditional tasks and agile stories

## Velocity and Estimation

### Story Point Scale
Fibonacci sequence is standard: 1, 2, 3, 5, 8, 13, 21

| Points | Effort Level | Typical Duration |
|--------|-------------|-----------------|
| 1 | Trivial | Hours |
| 2 | Small | Half day |
| 3 | Medium | 1 day |
| 5 | Large | 2-3 days |
| 8 | Very Large | 1 week |
| 13 | Epic-sized | Should be split |
| 21 | Too large | Must be split |

### Velocity Tracking
- Velocity = total story points completed per sprint
- Used to forecast future sprint capacity
- Stabilizes after 3-4 sprints
- Query completed stories per sprint to calculate velocity

## SAFe Support (SPM Professional)

SPM Professional adds Scrum Programs for SAFe (Scaled Agile Framework):

### Additional Tables
| Table | API Name | Purpose |
|-------|----------|---------|
| Feature | `rm_feature` | SAFe features (between theme and epic) |
| Program Increment | `rm_release` | PI planning (uses release table) |
| Team | sys_user_group | Agile teams (type = scrum) |

### SAFe Hierarchy
```
Portfolio → Theme → Feature → Epic → Story → Task
              │
              └── Program Increment (PI) → Sprint
```

## Key Tables Summary

| Table | API Name | Primary Use |
|-------|----------|-------------|
| `rm_epic` | Epic | Group related stories |
| `rm_story` | Story | Primary work item |
| `rm_sprint` | Sprint | Time-boxed iteration |
| `rm_defect` | Defect | Bug tracking |
| `rm_scrum_task` | Scrum Task | Story subtasks |
| `rm_release` | Release | Group sprints |
| `rm_theme` | Theme | Strategic grouping |
| `rm_feature` | Feature | SAFe features |

# SPM Table & Role Reference

Complete catalog of ServiceNow Strategic Portfolio Management tables, fields, roles, and state mappings. Use this reference when building AI Bridge API calls for any SPM module.

---

## Artifact Hierarchy

```
Portfolio (pm_portfolio)
  |
  +-- Program (pm_program)
  |     |
  |     +-- Program Task (pm_program_task)
  |
  +-- Project (pm_project)
        |
        +-- Project Task / Phase (pm_project_task)
        |     |
        |     +-- Sub-task (pm_project_task, parent = phase sys_id)
        |     |
        |     +-- Milestone (pm_project_task, is_milestone = true)
        |
        +-- Epic (rm_epic)
        |     |
        |     +-- Feature (rm_feature)
        |     |
        |     +-- Story (rm_story)
        |           |
        |           +-- Scrum Task (rm_scrum_task)
        |           |
        |           +-- Defect (rm_defect)
        |
        +-- Sprint (rm_sprint)
        |
        +-- Resource Plan (resource_plan)
        |
        +-- Cost Plan (cost_plan)
        |
        +-- Benefit Plan (benefit_plan)
        |
        +-- Risk (risk)
        |
        +-- Issue (issue)
        |
        +-- Status Report (project_status)

Demand (dmn_demand)  -->  converts to -->  Project (pm_project)

Idea (im_idea_core)  -->  converts to -->  Demand or Project or Epic/Story
```

Key relationships:
- Projects belong to Portfolios via `pm_m2m_portfolio_project` (many-to-many)
- Projects belong to Programs via the `program` field on `pm_project`
- Tasks form a hierarchy via the `parent` field on `pm_project_task`
- Milestones are project tasks with `is_milestone = true`
- Epics/Stories link to projects via the `project` reference field
- Resource Plans link to projects via the `top_task` field (set to project sys_id)
- Task dependencies use `planned_task_rel_planned_task` or `task_rel_task`

---

## Core Tables

These are the tables used most frequently for CRUD operations via the AI Bridge.

### pm_project -- Project

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| short_description | string | Yes | Project name / title |
| description | string | No | Detailed description |
| state | integer (string) | Yes | Project state (see State Mappings below) |
| start_date | date | Yes | Planned start date (YYYY-MM-DD) |
| end_date | date | Yes | Planned end date (YYYY-MM-DD) |
| project_manager | reference (sys_user) | Yes | sys_id of the project manager |
| program | reference (pm_program) | No | sys_id of parent program |
| portfolio | reference (pm_portfolio) | No | sys_id of portfolio (via relationship table) |
| priority | integer | No | 1=Critical, 2=High, 3=Moderate, 4=Low, 5=Planning |
| phase | string | No | Current phase label |
| percent_complete | decimal | No | Auto-calculated or manual completion percentage |
| business_unit | reference (cmn_department) | No | Department / business unit |
| risk | integer | No | Risk level |
| goal | string | No | Project goal |
| sys_id | string (auto) | -- | Unique identifier, returned on creation |

Common query: `GET /api/1851835/ai_adapter_rest/pm_project?sysparm_query=state=-5^ORstate=1&sysparm_display_value=all`

---

### pm_project_task -- Project Task / Phase / Milestone

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| short_description | string | Yes | Task name |
| description | string | No | Detailed description |
| parent | reference (pm_project or pm_project_task) | Yes | sys_id of parent project or parent phase |
| top_task | reference (pm_project) | Auto | sys_id of the root project (auto-set) |
| state | integer (string) | Yes | Task state (see State Mappings) |
| start_date | date | Yes | Start date |
| end_date | date | Yes | End date |
| assigned_to | reference (sys_user) | No | sys_id of assigned user |
| is_milestone | boolean | No | true = milestone (zero-duration marker) |
| priority | integer | No | 1-4 priority scale |
| percent_complete | decimal | No | Completion percentage |
| work_effort | duration | No | Estimated effort |
| order | integer | No | Sort order within parent |
| constraint_date | date | No | Must-start-on or must-finish-on date |
| html_description | html | No | Rich text description |
| sys_id | string (auto) | -- | Unique identifier |

Notes:
- A **Phase** is a `pm_project_task` whose `parent` is a `pm_project` sys_id.
- A **Sub-task** is a `pm_project_task` whose `parent` is another `pm_project_task` sys_id.
- A **Milestone** is a `pm_project_task` with `is_milestone = true`. Its `start_date` and `end_date` should be the same.

---

### rm_epic -- Epic

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| short_description | string | Yes | Epic name |
| description | string | No | Detailed description |
| project | reference (pm_project) | No | sys_id of parent project |
| state | integer (string) | Yes | State value |
| priority | integer | No | Priority (1-4) |
| assigned_to | reference (sys_user) | No | Epic owner |
| acceptance_criteria | string | No | Definition of done |
| story_points | integer | No | Total story points |
| release | reference (rm_release) | No | Target release |
| theme | reference (rm_theme) | No | Associated theme |
| sys_id | string (auto) | -- | Unique identifier |

---

### rm_story -- Story

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| short_description | string | Yes | Story title |
| description | string | No | Detailed description / user story |
| epic | reference (rm_epic) | No | sys_id of parent epic |
| project | reference (pm_project) | No | sys_id of project |
| sprint | reference (rm_sprint) | No | sys_id of sprint |
| state | integer (string) | Yes | Story state (see State Mappings) |
| priority | integer | No | Priority (1-4) |
| assigned_to | reference (sys_user) | No | Developer assigned |
| story_points | integer | No | Effort estimate |
| acceptance_criteria | string | No | Acceptance criteria |
| blocked | boolean | No | Whether story is blocked |
| release | reference (rm_release) | No | Target release |
| order | integer | No | Backlog order |
| sys_id | string (auto) | -- | Unique identifier |

---

### rm_sprint -- Sprint

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| short_description | string | Yes | Sprint name |
| start_date | date | Yes | Sprint start |
| end_date | date | Yes | Sprint end |
| state | integer (string) | Yes | Sprint state |
| assignment_group | reference (sys_user_group) | No | Scrum team |
| goal | string | No | Sprint goal |
| sys_id | string (auto) | -- | Unique identifier |

---

### resource_plan -- Resource Plan

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| top_task | reference (pm_project) | Yes | sys_id of the project this plan is for |
| program | reference (pm_program) | No | sys_id of the program |
| portfolio | reference (pm_portfolio) | No | sys_id of the portfolio |
| state | integer (string) | No | Plan state |
| resource_type | string | No | Type of resource |
| sys_id | string (auto) | -- | Unique identifier |

---

### resource_allocation -- Resource Allocation

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| resource_plan | reference (resource_plan) | Yes | sys_id of the resource plan |
| user | reference (sys_user) | Yes | sys_id of the allocated user |
| start_date | date | Yes | Allocation start |
| end_date | date | Yes | Allocation end |
| planned_hours | float | No | Planned hours |
| state | string | No | Allocation state |
| resource_role | reference (resource_role) | No | Role of the resource |
| group | reference (sys_user_group) | No | Resource group |
| sys_id | string (auto) | -- | Unique identifier |

---

### dmn_demand -- Demand

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| short_description | string | Yes | Demand title |
| description | string | No | Detailed description |
| state | integer (string) | Yes | Demand state (see State Mappings) |
| type | string | No | Demand type |
| priority | integer | No | Priority (1-4) |
| assigned_to | reference (sys_user) | No | Demand owner |
| business_unit | reference (cmn_department) | No | Requesting department |
| requested_by | reference (sys_user) | No | Requester |
| start_date | date | No | Desired start |
| end_date | date | No | Desired end |
| business_case | string | No | Justification |
| sys_id | string (auto) | -- | Unique identifier |

---

### pm_program -- Program

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| short_description | string | Yes | Program name |
| description | string | No | Detailed description |
| state | integer (string) | Yes | Program state |
| start_date | date | Yes | Start date |
| end_date | date | Yes | End date |
| program_manager | reference (sys_user) | No | Program manager |
| portfolio | reference (pm_portfolio) | No | Parent portfolio |
| sys_id | string (auto) | -- | Unique identifier |

---

### pm_portfolio -- Portfolio

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| short_description | string | Yes | Portfolio name |
| description | string | No | Detailed description |
| state | integer (string) | No | Portfolio state |
| manager | reference (sys_user) | No | Portfolio manager |
| start_date | date | No | Start date |
| end_date | date | No | End date |
| sys_id | string (auto) | -- | Unique identifier |

---

### rm_defect -- Defect

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| short_description | string | Yes | Defect title |
| description | string | No | Steps to reproduce / details |
| story | reference (rm_story) | No | Related story |
| sprint | reference (rm_sprint) | No | Sprint |
| project | reference (pm_project) | No | Project |
| state | integer (string) | Yes | Defect state |
| priority | integer | No | Priority |
| assigned_to | reference (sys_user) | No | Assigned developer |
| severity | integer | No | Severity level |
| sys_id | string (auto) | -- | Unique identifier |

---

### rm_scrum_task -- Scrum Task

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| short_description | string | Yes | Task name |
| story | reference (rm_story) | Yes | Parent story sys_id |
| state | integer (string) | Yes | Task state |
| assigned_to | reference (sys_user) | No | Assigned to |
| type | string | No | Task type (development, testing, etc.) |
| remaining_hours | float | No | Hours remaining |
| sys_id | string (auto) | -- | Unique identifier |

---

## Supporting Tables

### Financial Management

| Table | API Name | Description | Key Fields |
|-------|----------|-------------|------------|
| Cost Plan | cost_plan | Cost plan for project resources | project, state, total |
| Cost Plan Breakdown | cost_plan_breakdown | Rollup of all costs by project/program/portfolio | cost_plan, cost_type, amount |
| Cost Type Definition | resource_type_definition | Operating vs capital expense definitions, GL links | name, type |
| Project Funding | project_funding | Target and budget expense values per fiscal year | project, fiscal_year, capital, operating |
| Benefit Plan | benefit_plan | Expected benefits from project/demand | project, state, total |
| Benefit Breakdown | benefit_plan_breakdown | Rollup of all benefits | benefit_plan, amount |
| Budget Reference Rates | itfm_fx_rate | Exchange rates for budgets | currency, rate, effective_date |

### Resource Management

| Table | API Name | Description | Key Fields |
|-------|----------|-------------|------------|
| Resource Plan | resource_plan | All resource plans | top_task, program, portfolio, state |
| Resource Allocation | resource_allocation | Allocations for resources | resource_plan, user, start_date, end_date, planned_hours |
| Requested Allocation | requested_allocation | Resource plan requests | resource_plan, user, state |
| Requested Allocation Daily | requested_allocation_daily | Day-level request breakdown (read-only) | requested_allocation, date, hours |
| Resource Allocation Daily | resource_allocation_daily | Day-to-day actuals (read-only) | resource_allocation, date, hours |
| Resource Aggregate Daily | resource_aggregate_daily | Daily capacity/allocated/available | user, date, capacity, allocated, available |
| Resource Aggregate Weekly | resource_aggregate_weekly | Weekly aggregated (async) | user, week, capacity, allocated |
| Resource Aggregate Monthly | resource_aggregate_monthly | Monthly aggregated (async) | user, month, capacity, allocated |
| Resource Event | resource_event | Calendar events for a user | user, start, end, type |
| Resource Event Color | resource_event_color | Color coding for event types | event_type, color |
| Resource Plan Logs | resource_plan_logs | Errors/warnings during allocation | resource_plan, message, level |
| Resource Report | resource_report | Saved resource reports | name, type |
| Resource Report Daily | resource_report_daily | Daily report data | report, date |
| Resource Report Monthly | resource_report_monthly | Monthly report data | report, month |
| Resource Report Export | resource_report_export | JPG/PNG exports | report, format |
| Resource Role | resource_role | Project-specific roles | name, description |
| User Resource Role | user_has_resource_role | Roles assigned to a user | user, resource_role |
| Group Resource Roles | group_has_resource_role | Roles for groups (read-only) | group, resource_role |
| User Calendar Event | user_calendar_event | User calendar events | user, start, end, type |
| User Schedule | user_has_schedule | Schedule assigned to user | user, schedule |

### Project Portfolio Management

| Table | API Name | Description | Key Fields |
|-------|----------|-------------|------------|
| Portfolio | pm_portfolio | Portfolios | short_description, manager, state |
| Portfolio Project | pm_portfolio_project | Portfolio-level project view | portfolio, project |
| Portfolio Project Relationships | pm_m2m_portfolio_project | M2M: portfolio <-> project | portfolio, project |
| Portfolio Project Goal | pm_portfolio_goal | Portfolio-level goals | portfolio, goal |
| Portfolio Project Issue | pm_portfolio_issue | Portfolio-level issues | portfolio, issue |
| Portfolio Project Risk | pm_portfolio_risk | Portfolio-level risks | portfolio, risk |
| Project Stakeholder | pm_m2m_project_stakeholder | M2M: project <-> stakeholder | project, user, role |
| Project Template | project_template | Reusable project templates | name, description |
| Project Template Configuration | project_template_config | Template settings | template, setting |
| Project Template Task | project_template_task | Tasks within templates | template, short_description |
| Project Change Request | project_change_request | Change requests on projects | project, state, description |
| Status Report | project_status | Project status reports | project, state, report_date |
| Teamspace | pm_app_config | Teamspace configuration | name, config |
| Personalize Workbench | workbench_config_user | User workbench settings | user, config |
| Risk | risk | Project risks | project, description, probability, impact |
| Issue | issue | Project issues | project, description, priority |
| Goal | goal | Project goals | project, description |

### Task Dependencies & Baselines

| Table | API Name | Description | Key Fields |
|-------|----------|-------------|------------|
| Planned Task Relationship | planned_task_rel_planned_task | Predecessor/successor with lag | parent, child, type, lag |
| Task Relationship | task_rel_task | Generic predecessor/successor | parent, child, type |
| Baseline | planned_task_baseline | Project baselines | project, name, created |
| Baseline Item | planned_task_baseline_item | Tasks in a baseline | baseline, task, start_date, end_date |
| Planned Task Recalc Exclusions | planned_task_recalculation_exclusions | Tables excluded from date recalc | table_name |
| Project Task Link | pm_project_task_link | Linked changes (v3 plugin) | task, linked_record |

### Demand Management

| Table | API Name | Description | Key Fields |
|-------|----------|-------------|------------|
| Demand | dmn_demand | All demands | short_description, state, type, priority |
| Decision | dmn_decision | Demand decisions | demand, decision, decided_by |
| Stakeholder Register | dmn_stakeholder_register | Demand stakeholders | demand, user |
| Requirement | dmn_requirement | Demand requirements | demand, description, priority |
| Demand Stakeholder | dmn_m2m_demand_stakeholder | M2M: demand <-> stakeholder | demand, stakeholder |
| Demand Stage Config | dmn_stage_config | Stage pop-up images | stage, image |
| Idea (Demand) | idea | Ideas from demand module | short_description, state |

### Program Management

| Table | API Name | Description | Key Fields |
|-------|----------|-------------|------------|
| Program | pm_program | All programs | short_description, state, program_manager |
| Program Task | pm_program_task | Tasks within programs | program, short_description, state |

### Innovation Management

| Table | API Name | Description | Key Fields |
|-------|----------|-------------|------------|
| Idea | im_idea_core | Idea portal data (extends Task) | short_description, state, category, submitted_by |
| Idea Category | im_category | Static categories | name, description |
| Idea Category Configuration | im_category_config | Category definitions & mappings | category, config |
| Idea Categories (M2M) | im_m2m_idea_category | M2M: idea <-> category | idea, category |
| Idea Module | im_module | Idea portal configuration | name, config |

### Time Card Management

| Table | API Name | Description | Key Fields |
|-------|----------|-------------|------------|
| Time Card | time_card | Time logged against a category | user, category, total, state |
| Time Sheet | time_sheet | Groups time cards for a user per week | user, week_starts_on, state |
| Time Sheet Policy | time_sheet_policy | Time sheet policies | name, description |
| Time Card Daily | time_card_daily | Daily time entries | time_card, date, hours |
| Project Time Card Exception | project_timecard_exception | Exceptions: week start, user, project, state | user, project, week_starts_on |
| Project Time Category | project_time_category | Sub-categories for time cards | name, project |
| Time Sheet Exception | time_sheet_exception | Time sheet exceptions | user, week_starts_on, state |

### Rate Model

| Table | API Name | Description | Key Fields |
|-------|----------|-------------|------------|
| Rate Model | rate_model | Rate model definitions | name, description, state |
| Rate Model Entity | rate_model_entity | Source entities for attributes | rate_model, entity |
| Rate Model Entity Attribute | rate_model_entity_attribute | Attributes within entities | entity, attribute |
| Rate Model Line | rate_model_line | Rate line values | rate_model, rate, effective_date |
| Rate Model Line Attribute | rate_model_line_attribute | Rate line attributes | rate_line, attribute, value |
| Rate Line Import Set | imp_rate_model_line | Imported rate data | rate_model, import_data |

### Agile / SAFe

| Table | API Name | Description | Key Fields |
|-------|----------|-------------|------------|
| Epic | rm_epic | Agile epics | short_description, project, state |
| Story | rm_story | User stories | short_description, epic, sprint, story_points |
| Sprint | rm_sprint | Sprint containers | short_description, start_date, end_date, state |
| Defect | rm_defect | Bug tracking | short_description, story, severity, state |
| Scrum Task | rm_scrum_task | Sub-tasks within stories | short_description, story, state, remaining_hours |
| Release | rm_release | Release management | short_description, start_date, end_date |
| Theme | rm_theme | Agile themes | short_description, description |
| Feature | rm_feature | SAFe features | short_description, epic, state |

---

## Task Dependencies

### planned_task_rel_planned_task -- Predecessor/Successor Relationships

Use this table to create dependencies between project tasks, phases, or milestones.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| parent | reference (pm_project_task) | Yes | sys_id of the predecessor task |
| child | reference (pm_project_task) | Yes | sys_id of the successor task |
| type | string | No | Relationship type: `fs` (finish-to-start, default), `ss` (start-to-start), `ff` (finish-to-finish), `sf` (start-to-finish) |
| lag | duration | No | Lag time between predecessor end and successor start |

Example -- create a finish-to-start dependency:
```json
{
  "data": {
    "parent": "<predecessor_task_sys_id>",
    "child": "<successor_task_sys_id>",
    "type": "fs",
    "lag": "0 00:00:00"
  }
}
```

### task_rel_task -- Generic Task Dependencies

Broader dependency table used across ServiceNow (not SPM-specific). Same structure as above but operates on the base `task` table. Use `planned_task_rel_planned_task` for SPM project tasks.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| parent | reference (task) | Yes | sys_id of predecessor |
| child | reference (task) | Yes | sys_id of successor |
| type | string | No | Relationship type |

---

## Roles Reference

### Project Portfolio Suite (PPS)

| Role Title | API Name | Description | Contains Roles |
|-----------|----------|-------------|----------------|
| PPS admin | it_pps_admin | Full admin for all SPM modules: view/modify preferences, configs, settings | it_program_manager, it_portfolio_manager, it_project_manager, it_demand_manager, pps_admin, timeline_admin, rate_model_admin |
| Portfolio manager | it_portfolio_manager | Access all portfolios; includes project user + demand user + budget owner | it_demand_user, it_project_manager, it_project_user, portfolio_manager, it_demand_manager, it_project_portfolio_user |

### Project Management

| Role Title | API Name | Description | Contains Roles |
|-----------|----------|-------------|----------------|
| Project manager | it_project_manager | Full config access to all Project Management features | resource_user, it_demand_manager, it_project_user, project_manager (contains timecard_approver), timeline_user, rate_model_user |
| Project user | it_project_user | View Project form fields, modify Project Task fields | it_project_portfolio_user, project_user |
| Portfolio user | it_project_portfolio_user | View IT Portfolio Project records (read-only portfolio access) | project_portfolio_user |

### Program Management

| Role Title | API Name | Description | Contains Roles |
|-----------|----------|-------------|----------------|
| Program manager | it_program_manager | Access all programs | resource_user, it_project_user, program_manager, it_demand_user |

### Demand Management

| Role Title | API Name | Description | Contains Roles |
|-----------|----------|-------------|----------------|
| Demand manager | it_demand_manager | Access all Demand Management modules | it_project_user, resource_user, timeline_user, demand_manager, it_demand_user, rate_model_user |
| Demand user | it_demand_user | Access Demand and Stakeholders modules | demand_user, pps_resource |

### Resource Management

| Role Title | API Name | Description | Contains Roles |
|-----------|----------|-------------|----------------|
| Resource manager | resource_manager | Review/confirm/allocate resources, create skills, read schedules, manage groups | resource_user, timecard_approver, skill_admin, rate_model_user |
| Resource user | resource_user | Create resource plans, request resources. Cannot change Confirmed/Allocated plans | -- |
| PPS resource | pps_resource | Only users with this role are considered for resource planning | -- |

### Innovation Management

| Role Title | API Name | Description | Contains Roles |
|-----------|----------|-------------|----------------|
| Idea admin | idea_admin | Create modules, define categories, manage ideas, create tasks from ideas | idea_manager |
| Idea manager | idea_manager | Manage ideas, create project/demand from ideas | -- |
| Idea manager professional | idea_manager_professional | Manage ideas, create story/epic/feature/project/demand from ideas | -- |

### Time Card Management

| Role Title | API Name | Description | Contains Roles |
|-----------|----------|-------------|----------------|
| Time card admin | timecard_admin | Write access to all time cards | timecard_user, timecard_approver |
| Time card approver | timecard_approver | Approve/reject time cards | timecard_user |
| Time card user | timecard_user | Create time cards for self | -- |

### Rate Model

| Role Title | API Name | Description | Contains Roles |
|-----------|----------|-------------|----------------|
| Rate model admin | it_rate_model_admin | Manage rate models and lines, configure attributes, export/import | rate_model_user, import_set_loader, import_transformer, import_admin |
| Rate model user | rate_model_user | View rate model and rate lines | -- |

---

## State Value Mappings

State values in ServiceNow are stored as numeric strings. Always pass these as strings (e.g., `"state": "-5"`) in API calls.

### pm_project -- Project States

| Value | Label | Description |
|-------|-------|-------------|
| -5 | Draft | Initial creation, not yet active |
| -4 | Pending | Awaiting approval or scheduling |
| 1 | Open | Active, work in progress |
| 2 | Work in Progress | Actively being executed |
| 3 | On Hold | Temporarily suspended |
| 4 | Closed Complete | Successfully completed |
| 7 | Cancelled | Cancelled, will not be completed |
| -6 | Pending Closure | Awaiting closure approval |

### pm_project_task -- Project Task States

| Value | Label | Description |
|-------|-------|-------------|
| -5 | Pending | Not yet started |
| 1 | Open | Ready to begin / in progress |
| 2 | Work in Progress | Actively being worked on |
| 3 | On Hold | Temporarily paused |
| 4 | Closed Complete | Finished successfully |
| 7 | Closed Skipped | Skipped, not completed |
| -6 | Closed Incomplete | Closed without full completion |

### rm_story -- Story States

| Value | Label | Description |
|-------|-------|-------------|
| -6 | Draft | Initial creation |
| 1 | Ready | Groomed and ready for sprint |
| 2 | Work in Progress | Actively being developed |
| 3 | Testing | In QA / testing |
| 4 | Complete | Done |
| 7 | Cancelled | Will not be done |

### rm_epic -- Epic States

| Value | Label | Description |
|-------|-------|-------------|
| -6 | Draft | Initial creation |
| 1 | Open | Active |
| 2 | Work in Progress | Actively being worked |
| 3 | On Hold | Paused |
| 4 | Complete | Done |
| 7 | Cancelled | Will not be done |

### dmn_demand -- Demand States

| Value | Label | Description |
|-------|-------|-------------|
| 1 | New | Newly submitted demand |
| 2 | Screening | Under initial review |
| 3 | Qualified | Passed screening |
| 4 | Approved | Approved for execution |
| 5 | Scheduled | Scheduled for implementation |
| 6 | In Progress | Being executed |
| 7 | Closed | Completed or rejected |
| -7 | Cancelled | Cancelled |

### rm_sprint -- Sprint States

| Value | Label | Description |
|-------|-------|-------------|
| -5 | Draft | Planning phase |
| 1 | Planning | Sprint being planned |
| 2 | Active / In Progress | Sprint is underway |
| 3 | Complete | Sprint finished |
| 4 | Closed | Sprint closed out |

---

## Quick Lookup: Table Name to API Name

| Common Name | API Name |
|-------------|----------|
| Project | pm_project |
| Project Task / Phase | pm_project_task |
| Milestone | pm_project_task (is_milestone=true) |
| Epic | rm_epic |
| Story | rm_story |
| Sprint | rm_sprint |
| Defect | rm_defect |
| Scrum Task | rm_scrum_task |
| Feature | rm_feature |
| Release | rm_release |
| Theme | rm_theme |
| Program | pm_program |
| Program Task | pm_program_task |
| Portfolio | pm_portfolio |
| Demand | dmn_demand |
| Idea (Innovation) | im_idea_core |
| Idea (Demand) | idea |
| Resource Plan | resource_plan |
| Resource Allocation | resource_allocation |
| Resource Role | resource_role |
| Cost Plan | cost_plan |
| Benefit Plan | benefit_plan |
| Time Card | time_card |
| Time Sheet | time_sheet |
| Risk | risk |
| Issue | issue |
| Status Report | project_status |
| Rate Model | rate_model |
| Task Dependency | planned_task_rel_planned_task |
| Baseline | planned_task_baseline |
| Portfolio-Project Link | pm_m2m_portfolio_project |
| Project Stakeholder | pm_m2m_project_stakeholder |

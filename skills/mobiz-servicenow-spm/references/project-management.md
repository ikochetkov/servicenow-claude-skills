# Project Management Process Guide

Reference for ServiceNow SPM (Strategic Portfolio Management) Project Management, based on the Zurich release process guide. This document covers the project lifecycle, states, roles, task management, dependencies, scheduling, reporting, and closure within ServiceNow SPM.

## Overview

Project management in ServiceNow SPM applies knowledge, skills, tools, and techniques to project activities through five process groups:

1. **Initiating** - Evaluate and approve/reject proposed projects
2. **Planning** - Define scope, prerequisites, and plan for execution
3. **Executing** - Start the project and measure against estimates
4. **Delivering** - Track budget, scope, schedule, risks, and issues
5. **Closing** - Post-implementation review and formal closure

There are two main types of SPM implementations:

- **Execution-level**: Project managers, resource managers, and team members managing tactical details of project execution, using reporting to communicate progress and expenditures.
- **Portfolio-level**: Business sponsors, steering committees, and PMOs creating decision frameworks, selecting projects, planning delivery, tracking investments, and reporting.

## Project Description

A project is a temporary endeavor with a defined scope, start and end points, intended to create a unique product, service, or result. Projects differ from "operations" which are ongoing and repetitive. Projects can involve any number of individuals, departments, or business units across the organization.

## Project States

Throughout the project lifecycle, tasks are tracked to support the project schedule and status reporting. The state indicates position in the project schedule. Base system state values:

| State | Usage |
|---|---|
| Pending | Default value when a record is created |
| Open / Work in Progress | Work is in progress |
| Closed Complete | Work is completed, task is closed |
| Closed Incomplete | Work was done but not yet completed, task is closed. Also used for "Postponed/Freeze/On-Hold" projects |
| Closed Skipped | Work was not performed, task is closed. Also used for "Cancelled" projects |

## Project Templates

Project templates are best-practice approaches that outline activities and deliverables required to satisfy project requirements.

- **Save as New Template**: Creates a template from a project, copying all attachments, tasks, and checklists. Attachments can be added or removed from the template afterward.
- **Copy Project**: Creates a new project including all tasks, relationships, and document links from an existing project. Partial projects can also be copied via the Planning Console.
- Multiple templates can be applied to a single project.
- Templates can be automatically applied if selected from the Demand record.

## Move Project

The "Move Project" feature allows project managers to move or leave tasks based on constraint type. It can be performed at any time, regardless of task state.

## Project Workspace

The Project Workspace application provides an interactive UI for project managers to define, plan, track, and monitor projects from a single location. It includes:

- Project dashboard with Analytics
- Project details, planning, resources, financials tabs
- Status report tab
- Planning Console for task management and Gantt chart view

## Schedule

Schedule pages can be displayed daily, weekly, or monthly. A schedule page is a record containing scripts that enable custom generation of a calendar or timeline display.

## Programs

A Program is a group of related projects, demands, and program activities managed in a coordinated way. Program managers:

- Create program-specific tasks outside project scope
- Define critical milestones, anticipated risks, and issues
- Ensure all program participants' projects are on track with respect to cost, resources, and schedule

## Project Roles

| Role | Key Responsibilities |
|---|---|
| PMO | Defines project process mission, ensures consistent execution, monitors effectiveness, resolves cross-functional issues |
| Project Manager | Plans/executes/closes projects, manages day-to-day activities, leads team, manages issues and risks |
| Team Member | Executes tasks, produces deliverables, communicates status/issues/risks, enters time worked |
| Resource Manager | Deploys resources efficiently, tracks supply/demand, assigns resources to tasks, tracks utilization |
| BRM | Represents business needs, gathers requirements, submits project requests, tracks status |
| Project Sponsor | Secures funding/resources, champions goals, monitors risks/issues, provides business guidance |
| Stakeholders | Reviews status, provides business guidance/support |
| Program Manager | Manages programs aligned with strategy, coordinates cross-department demands/projects |
| Portfolio Manager | Selects projects based on business objectives and resources, maintains optimal investment mix |
| Project Administrator | Technical implementation: properties, form/view customization, workflows, reports/dashboards |

## RACI Matrix

| ID | Activity | Business User | Project Manager | Team Member | PMO | Program Manager | Stakeholder/Sponsor | Resource Manager |
|---|---|---|---|---|---|---|---|---|
| **SPM 1.0** | **Project Initiation** | | | | | | | |
| SPM 1.1 | Create Project | | R | | A | C/I | C | |
| SPM 1.2 | Add Project to Portfolio | | | | R/A | | C | |
| SPM 1.3 | Assign Project Manager | | I | | R/A | C/I | | |
| **SPM 2.0** | **Project Planning** | | | | | | | |
| SPM 2.1 | Plan the Project | | R/A | | | | C | |
| SPM 2.2 | Apply Templates | | R/A | | | | | |
| SPM 2.3 | Add Tasks | | R/A | I | | | | |
| SPM 2.4 | Build Task Relationships via Planning Console | | R/A | | | | | |
| SPM 2.5 | Approve Resources | | C | | | | | R/A |
| SPM 2.6 | Assign Goals to Project and Strategy | C | R/A | | I | | C | |
| **SPM 3.0** | **Project Execution** | | | | | | | |
| SPM 3.1 | Start Project | | R/A | | | | | |
| SPM 3.2 | Create Baseline | | R/A | | | | | |
| SPM 3.3 | Workflow | I | R/A | | | | | |
| SPM 3.4 | Task Status | I | A | R | | | I | |
| **SPM 4.0** | **Project Delivering** | | | | | | | |
| SPM 4.1 | Manage Variables | | R/A | | | | | |
| SPM 4.2 | Documentation | I | R/A | | | | I | |
| SPM 4.3 | Risk Register / Issue Management | I | R/A | | | C/I | I | |
| SPM 4.4 | Project Communication | I | R/A | | I | I | | |
| SPM 4.5 | Project Status Report | I | R/A | I | I | I | I | I |
| **SPM 5.0** | **Project Closing** | | | | | | | |
| SPM 5.1 | Post Implementation Review | | R/A | | | | | |
| SPM 5.2 | Close Project | I | R/A | | | C/I | I | |

R = Responsible, A = Accountable, C = Consulted, I = Informed

## Project Management Process

### Basics

Setting up a project involves:

1. Deciding on an approach for creating and linking project tasks
2. Ensuring necessary users and groups are created in ServiceNow for assignment
3. Creating a Baseline (point-in-time snapshot of schedule and financial data) to measure against initial estimates
4. Managing ongoing changes to costs, priority, schedule, strategy, goals, and planned values
5. Maintaining detailed project records of risks and issues
6. Creating additional baselines when there is an approved change of scope
7. Managing status reports for visibility at program and portfolio levels
8. Closing the project (state changed to Closed Complete), which triggers actual value calculations

Post-project activities include analyzing baselines and actual values, generating a final dashboard, and potentially using the project as a template for future projects.

ServiceNow SPM supports multiple methodologies including Agile and Waterfall.

### Phase 1: Initiating a Project

Project initiation evaluates a proposed project based on business case, cost, timeframe, and alignment with business objectives or strategic plan. The initiation plan can include: business case, overall goal, specific objectives, success criteria, scope, high-level schedule, stakeholder accountabilities, communication plan, benefits/costs, governance/resourcing, and risk mitigation.

| ID | Task | Primary Role | Input | Output |
|---|---|---|---|---|
| SPM 1.1 | Create Project | Project Managers | Import Project (MS or Other), Create new project, or from Demand | Project Record |
| SPM 1.2 | Add Project to Portfolio | PMO | Existing projects (any state) | Portfolio projects |
| SPM 1.3 | Assign Project Manager | PMO | Project Record | Assigned Project Record |

**Key details:**

- Most projects are created via the Demand Process. When created from a Demand, Approved Start/End Dates auto-populate from the Demand's dates and are used in the Strategic Planning Workspace roadmap. Projects not requiring a demand can be created manually.
- If a Portfolio was defined in the Demand Process, it carries over to the Project. Projects can be linked to roadmapping for tracking in the Strategic Planning Workspace.
- After project generation, the PMO assigns it to a specific Project Manager.

### Phase 2: Planning the Project

Planning defines the scope and identifies all prerequisites for execution. Project scope, budget, and schedule should be confirmed. Deliverables are refined. Risk assessment and mitigation plans are developed. Team members may be allocated.

| ID | Task | Primary Role | Input | Output |
|---|---|---|---|---|
| SPM 2.1 | Plan the Project | Project Manager | Assigned Project Record | Additional details added to Project form (State: Pending) |
| SPM 2.2 | Apply Template | Project Manager | Project Record | Project Record with Template(s) Applied |
| SPM 2.3 | Add Tasks | Project Manager | Project tasks | Project tasks added to project (State: Pending) |
| SPM 2.4 | Build Task Relationships via Planning Console | Project Manager | Task dependencies | Gantt chart with project dependencies |
| SPM 2.5 | Approve Resource Assignments | Resource Manager | User resources; Group resources | Approval of resource assignment across the project |
| SPM 2.6 | Assign Goals to Project and Strategy | Project Manager / Business User | Strategy and goals identified by Business Managers | Linked project to achieve one or more goals |

**Key details:**

- Before creating a project, consider: top-down or bottom-up tasking, portfolio membership, dependency types, template availability, milestones/baselines, and whether necessary skills/groups/resources exist in ServiceNow.
- Templates automatically build the WBS (Work Breakdown Structure) and may be auto-applied from the Demand Record. Multiple templates can be applied to one project.
- Populate projects with phases, tasks, and subtasks. Build relationships and dependencies while creating task sets.
- Use the Project Workspace to build relationships, add milestones for significant events, and create dependencies between milestones and tasks.
- Resource Assignments should be initially generated in the Demand Process. The Resource Management Workspace provides a graphical map of task-to-resource relationships.
- Strategy and goals should be initially generated in the Demand Process. Link to the Strategy and Goal framework to track consecution and costs.

### Phase 3: Executing the Project

After initiation steps are complete, the project can be started and measured against initial estimates.

| ID | Task | Primary Role | Input | Output |
|---|---|---|---|---|
| SPM 3.1 | Start Project | Project Manager | Project record, child project tasks | Work in Progress project |
| SPM 3.2 | Create Baseline | Project Manager | Updates to project and tasks | Baseline record captured |
| SPM 3.3 | Workflow | Project Manager | Project process | Workflows for project automation |
| SPM 3.4 | Task Status | Team Member / Project Manager | Task description, state change, percent complete, actual effort | Updated project actuals (time and cost) |

**Key details:**

- Change project state to Work in Progress and Save to set Actual start date to current date.
- Initial baseline is auto-captured from Demand records. Subsequent baselines can be manually captured. Use Baseline Variance to view variance between current plan and baseline end dates.
- Consider automation for approvals, milestone/gate review processes, and integrated change request processes.
- Team members update task status and actual effort promptly for accurate project reporting.

### Phase 4: Delivering the Project

The project manager tracks budget, scope, and schedule (the "Triple Constraint") and their effect on quality.

| ID | Task | Primary Role | Input | Output |
|---|---|---|---|---|
| SPM 4.1 | Manage Variables | Project Manager | Actual time, effort, cost | Aggregate project effort and costs |
| SPM 4.2 | Documentation | Project Manager / Administrator | Project documents and deliverables | Stored documents, approval process |
| SPM 4.3 | Risk Register / Issue Management | Project Manager | Risk management plan, risks/issues | Risk/issues records (related lists) |
| SPM 4.4 | Project Communication | Project Manager | Stakeholder KPIs and Metrics | Communication process, dashboards, reports, notifications |
| SPM 4.5 | Project Status Report | Project Manager | Project, cost, progress, risk, issue, schedule, scope statuses | Reports to stakeholders, dashboards |

**Key details:**

- Track cost, effort, and scope. Cost is mapped to existing cost plans; the system auto-generates one if none exists.
- Document management options: attachments, knowledge base, managed documents, and gates.
- Track risks and issues with detailed records for post-completion analysis.
- Status Reports fill portfolio/program workbenches, investment portal, and dashboards. Evaluate overall, schedule, resource, cost, and scope health. RIDAC items shown via "Show on Project Status Report" checkbox.

### Phase 5: Closing the Project

Project closing includes a post-implementation review to gather feedback, identify lessons learned and best practices.

| ID | Task | Primary Role | Input | Output |
|---|---|---|---|---|
| SPM 5.1 | Post Implementation Review | Project Manager | Project feedback | Post-implementation report |
| SPM 5.2 | Close Project | Project Manager | Appropriate documents and signoffs | Project State: Closed Complete |

**Key details:**

- Gather feedback from all stakeholders. Conduct post-implementation review and prepare report. Optionally create a Continual Improvement Initiative (CIM).
- Complete all administrative tasks for official close. Determine how well requirements were met, document lessons learned.

## Relationship with ITSM

ServiceNow SPM integrates with ITSM processes on the same platform:

| Process | Relationship |
|---|---|
| Configuration Management | Underpins both ITIL and project management activities. Hosts project and ITSM records. Single consistent view of all activities against a CI. |
| Service Catalog | Simple, consistent approach to capturing demand and project proposals. Request information auto-entered into project management. |
| Change Management | RFCs can be submitted for project changes. Project tasks can depend on changes. Issues and risks can transition to change control. |
| Digital Portfolio Management | Reads from Project Management to show projects/demands created against business applications in the Digital Portfolio. |
| Service Level Management | Defines measurable actions on critical path tasks. Provides historical data for schedule review. Defines acceptable timeframes for task start times, pause conditions, and completion times. |

## Relationship with Other SPM Processes

| Process | Relationship | Direction |
|---|---|---|
| Innovation Management | Ideas can bypass demand and convert directly to a project | Input |
| Demand Management | Approved Demands become managed Projects | Input |
| Resource Management | Resource Assignments generated during Project Process | Input/Output |
| Agile/EAP | Agile story dates roll up to the project | Input/Output |
| Test Management | Manage the test schedule | Input/Output |
| Enterprise Architecture | Manage applications and costs for alignment | Input/Output |
| Release Management | Plan and manage enterprise/product releases and deployment | Output |
| Investment Funding | Funding for Projects, Portfolios, or Programs | Output |
| ESG | Shows projects planned or in execution to achieve ESG goals | Input |
| Customer Service Management | Enables managing projects with multiple tasks and gives end users visibility | Input/Output |
| Roadmap Planning | Projects are planning items in Portfolio Planning/Strategic Planning Workspace | Input |
| Backlog Planning | Projects are work items in Strategic Planning Backlog; new projects added with draft state | Output |

## Project Process Controls

### PMO Dashboard

Provides a comprehensive view of Portfolio, Program, Organization, or entity information with a left-to-right flow:

| Section | KPI/Metric | Purpose |
|---|---|---|
| Summary | Active projects count, counts per investment type/class/priority, rolled-up financials (planned, actuals, forecasts) | High-level overview of critical in-flight project information |
| Pipeline | Ages of ideas/demands/projects, conversion ratios from ideas to demands to projects | Track pipeline performance and identify bottlenecks |
| Project Health | Count of projects in red status, overdue, over budget, high risks, negative ROI | Identify areas for intervention |
| Data Quality | Count of demands/projects with 12 types of missing data | Guide training and communications efforts |
| Actuals | Planned, budgeted, actual, and benefit costs; allocated and solid hours | Compare planned vs actual for costs, resources, and benefits |
| Calendar | Tasks and milestones in calendar view | Visualize key planned end dates |

### Investment Portal

Tracks progress of in-flight work for different personas (C-level executive, program manager, project manager, business application owner). Provides configurable views for:

- Health status overview
- Timeline view (project schedules and milestones)
- Financials view

### Status Reports

Status Reports fill portfolio/program workbenches, investment portal, and dashboard pages. They evaluate overall, schedule, resource, cost, and scope health. RIDAC items are included when "Show on Project Status Report" is checked. Reports can be printed or sent to stakeholders as attachments.

## Timecards and Costing

### Timecards

- Team members update time worked on individual tasks or multiple tasks via inline editing
- Timecard application can submit timecards periodically
- Timecards are filled using the Time Sheet Portal
- Timecards automatically create expense lines using labor rate cards
- Timecards roll up to the project's actual costs
- Timecards can be linked to resource assignments and costs
- Approval process applies to timecards after submission

### Project Costing

Key costing features:

- Create fiscal calendars with defined fiscal periods for timecards or cost plans
- Estimate resource costs during planning using Rate Models
- Track actual cost of each user resource for a project
- Track actual task costs from timecards and other expenses
- Allocate project costs to the business using Expense Lines and Expense Allocations
- Represent project costs to affected CIs
- Roll up actual task expenses to parent tasks and the project record
- Review project forecasting metrics (schedule the job "Calculate Project Completion Estimates" to populate forecast data)

## Notifications

Notifications should be created to keep the project on track:

- Email notifications when a project request, task, or deliverable needs review/approval
- Live feed group notifications based on conditions
- Dashboard gauges indicating records requiring attention
- Scheduled reports to the project sponsor or stakeholders

## Project Diagnostics

Project Diagnostics detects corrupt data including task validity, dependencies, and relationships.

Data may become corrupt due to:
- Incorrect field mapping during project import
- Incorrect scheduling of tasks
- Incorrect dependency and relationship definitions

Available diagnostic scans:

- **Tasks with invalid top task/portfolio/program** - Lists tasks with null or mismatched hierarchy references
- **Invalid relations** - Relations where predecessor/successor is not part of the project (unless external) or doesn't exist
- **Validate parent tasks** - Tasks with empty or invalid parents
- **Check cyclic dependencies** - Cyclic relations (not permitted in a project)
- **Recalculate project** - Recalculates task dates (warning: may change dates)
- **Check duplicate/redundant relationships** - Tasks with duplicate or redundant relations
- **Cost plans with no start/end fiscal period** - Missing fiscal period boundaries
- **Validate task constraints** - Invalid constraint types (e.g., "Start no later than" on a parent)
- **Validate tasks with invalid state** - Invalid WIP or Closed state based on actual dates
- **Budget diagnostics** - Negative fiscal-year budgets, funding mismatches, invalid fiscal periods in breakdowns, duplicate task type breakdowns
- **Orphan expense lines** - Expense lines not associated with any cost plan (fix script associates them with system-generated cost plan)

## Project Features Reference

- **Project logic**: Planned start/end dates, durations, dependencies, time calculations, resources. All planned tasks (project, project task, and custom planned-type tasks) inherit this functionality.
- **Parent/child relationships**: Uses the Parent field on the Task table for building the hierarchy (phases and tasks).
- **Dependencies**: Many-to-many dependency capabilities allowing tasks to be both predecessor and successor to multiple other tasks.
- **Modular templates**: Any existing project can be used as a template. Sub-projects can be copied from larger structures. A project usually consists of many smaller templates (structure, approval tasks, closure tasks).
- **Platform integration**: Create Project option enables project creation directly from an incident, problem, or change record, pre-populated with source data.
- **Baselines**: Point-in-time data copy of current project schedule and financial data for variance reporting.
- **Milestones**: Planned tasks with zero duration. Represented by a diamond on the Gantt chart (customizable). Treated like any other planned task.
- **Risks and Issues**: Tracked against a project. Issues are Task table extensions, so they can be assigned, measured with SLAs, or included in notifications.
- **Resource allocation**: User Resources associates users with tasks at a percentage allocation, checked against the schedule to calculate hours and determine availability.
- **Assignment restrictions**: Task assignments can be restricted to users listed in the project's User Resources list.
- **RIDAC**: Management of Risks, Issues, Decisions, Actions, and Requests for Changes within projects.
- **Project Forecasting**: Forecast costs (Estimate to Completion, Estimate at Completion) by Fiscal Period.

## Task Dependency Types

| Dependency Type | Description | Supported |
|---|---|---|
| Finish to Start (FS) | Task 2 cannot start until Task 1 finishes | Yes |
| Finish to Finish (FF) | Task 2 cannot finish until Task 1 finishes | Yes |
| Start to Start (SS) | Task 2 cannot start until Task 1 starts | Yes |
| Start to Finish (SF) | Task 2 cannot finish until Task 1 starts | Yes |

Time constraints supported: ASAP, Start on Specific Date, Start No Earlier Than, Start No Later Than. Tasks imported from Microsoft Project have their constraint set to "Start on Specific Date" if the MS Project constraint differs from ASAP.

## Portfolio Management

Project portfolio management maintains the optimal mix of projects/investments to support the organization. SPM addresses all enterprise maturities:

1. **Visibility**: List portfolios and projects, reporting. No duplicate/mystery/side projects; all activity is inventoried. Investment Portal provides visibility.
2. **Budget management**: Manage portfolios, prepare/build/approve budgets. Compose, evaluate, and select scenarios based on which projects/demands are executed and their budget impact. Uses Portfolio Workbench.
3. **Forecast tracking**: Manage portfolios, prepare/build/approve yearly budgets. Track and promote forecasted budgets during the year. Uses Portfolio Workbench.

Portfolios and programs can both manage demands and projects in a flexible structure. SPM does not manage portfolio hierarchies or program hierarchies.

## Key Tables

The following ServiceNow tables are central to project management in SPM:

| Table | Description |
|---|---|
| `pm_project` | Project records. Extends `planned_task`. Contains project-level fields: state, project manager, portfolio, program, approved dates, actual dates, baselines, cost plans. |
| `pm_project_task` | Project task records. Extends `planned_task`. Contains task-level fields: assigned to, state, percent complete, actual effort, planned/actual dates, constraint type. |
| `pm_milestone` | Milestone records. Planned tasks with zero duration marking significant project events or gates. |
| `planned_task_rel_planned_task` | Task dependency/relationship records. Defines predecessor/successor relationships between planned tasks with dependency type (FS, FF, SS, SF) and lag time. |
| `project_status` | Project status report records. Contains overall, schedule, resource, cost, and scope health indicators with comments. |
| `risk` | Risk records associated with projects. Contains risk description, probability, impact, response strategy, and status. |
| `issue` | Issue records associated with projects. Extends `task`. Contains issue description, priority, assignment, and resolution details. |
| `goal` | Strategic goal records that projects can be linked to. Used to track alignment between project execution and organizational strategy. |

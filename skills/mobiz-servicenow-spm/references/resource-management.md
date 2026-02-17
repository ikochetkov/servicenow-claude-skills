# Resource Management Process Guide

> ServiceNow SPM -- Resource Management (Next Experience), Zurich Release

## Overview

The Resource Management process forecasts and tracks the demand for and supply of human resources within an organization. It enables resource requesters (project managers, demand managers, change managers) to create resource assignments, request resources, and analyze demand, availability, and utilization. This guide is aligned with OOTB functionality.

Resource Management can be used for:

- Defining resource availability schedules
- Creating resource assignments that specify needs for group, role, skill, or user resources (at the demand, project, epic, or itemized task level)
- Verifying resource availability and making changes to resource assignments before requesting resources
- Maintaining a work calendar to ensure non-working time (vacations, holidays) is visible to the resource manager
- Viewing availability, existing assignments, and utilization for requested resources
- Performing what-if analysis by changing resource assignment dates, resources, and requested hours

## Process Description

The Resource Management process tracks resource assignments, resource availability, utilization, and capacity planning.

A resource requester forecasts their resource requirements by creating and working with the Resource Manager to maintain resource assignments across projects, demands, epics, or any other operational work. Once complete, the resource requester submits their resource assignments for approval to the designated resource manager(s). The requests then proceed through a negotiation stage. The resource manager can then assign named resources and approve or unapprove the request(s). If approved, the resource requester can assign the task(s) to the resource(s) and track them to completion.

## Process Goal

The primary goal of the Resource Management process is to ensure that the best possible decisions on resourcing of organizational demands can be made by providing accurate information on resource demand and capacity.

## Process Objectives

- Ensure human resources are deployed as efficiently and effectively as possible
- Provide a single source of truth for resource requesters and resource managers
- Forecast the volume and type of resources required to execute the organization's portfolio of work
- Ensure the most appropriately skilled resources are assigned to the work requested
- Provide Resource Managers visibility on current and planned resource work
- Assess resource capacity and review existing allocations to make informed decisions

## Relationships With Other Processes

| Process | Relation | Direction |
|---|---|---|
| Demand Management | Resource requirements from Demands; assignments copied to project/enhancement/request. Approval notifications sent back. | Both |
| Project Management | Resource planning and requirements within Projects. Approval notifications sent back. | Both |
| Portfolio Planning | Resource requirements during portfolio planning. Capacity Planning screen for resource capacity mapping. | Input |
| Cost Management | CI-related cost information for calculating resource costs. | Input |
| Change Management | Resource assignment updates from approved Change Requests. | Input |
| Timecard Management | Timecards reference Resource Assignments for tracking estimate accuracy. | Both |

## Definitions

- **Resource Availability**: The time a resource is committable, operable, and usable upon a demand.
- **Ready to Review**: A list to confirm if a resource assignment is ready for a Resource Manager's review for allocation.
- **Resource Capacity**: The quantity and quality of resource availability.
- **Resource Demand**: The desire for an available resource with the appropriate skill and capacity.
- **Resource Calendar**: Used to reflect working hours, holidays, vacations, and other committed time for a resource.
- **Person Days**: Hours calculated as Total number of person-days * Average Daily FTE Hours/Hours Per Person Day. Example: Average Daily FTE is 8 hrs, person-days is 3, then planned hours = 8 * 3 = 24 hours.
- **FTE**: An equivalent value that represents full-time work. When request type is FTE, planned hours = Average Daily FTE * number of working days * FTE value. Average daily FTE hours are specified in User and Group records; if not set, taken from the Default Average Daily FTE property. Working days are calculated based on the user's schedule (user resource) or default schedule (group resources).

## Resource Assignment States

Resource Assignments are tracked throughout their lifecycle. The state is a read-only field changed based on the decisions of the requester and approver.

1. **Pending**: The resource assignment needs to be evaluated, typically indicating that a named resource has not been assigned yet.
2. **Approved**: A named resource has been added, their availability has been confirmed, and the resource assignment is approved to proceed.
3. **Unapproved**: There is an issue with the resource assignment (resource unavailable, conflicts exist, etc.). The assignment returns to the resource requester for changes or cancellation.
4. **Unassigned**: No named resource has been added to the resource assignment.

The requester can request a change when a resource assignment is in the Requested or Confirmed state (but not yet allocated). If approved and actioned, the plan moves back to the Planning state.

## Process Roles

| Role | Description |
|---|---|
| **Resource Management Process Owner** | Stakeholder with authority to ensure RM process is implemented correctly. Defines overall mission, communicates goals, resolves cross-functional issues, ensures consistent execution, reports on effectiveness, initiates process improvements. |
| **Resource Manager** | Ensures efficient deployment of resources. Responsible for: timely response to resource requests, ensuring resources are used efficiently, tracking supply of resources, maintaining resource demand forecast, approving resources, tracking utilization. |
| **Resource Requester** | Works with Resource Managers to plan and assign resources. Responsible for: creation and maintenance of resource assignments, submission of resource assignments, negotiation with resource managers, assignment of approved resources to tasks, releasing underutilized resources. |
| **Resource** | Individuals being requested via this process. Responsible for ensuring their availability for work is kept up to date. |

## RACI Matrix

| ID | Activity | Resource Requester | Resource Manager | Demand Mgr | Project Mgr | Change Mgr | Portfolio Planner |
|---|---|---|---|---|---|---|---|
| RSM 1.0 | **Create and Submit Resource Assignments** | | | | | | |
| RSM 1.1 | Confirm Resource Requirements | A/R | C | C | C | | |
| RSM 1.2 | Select Required Resource Group | A/R | | | | | |
| RSM 1.3 | Select Named Resource | A/R | | | | | |
| RSM 1.4 | Select Group Member Preference | A/R | | | | | |
| RSM 1.5 | Create Resource Assignments | A/R | | | | | |
| RSM 1.6 | Update Resource Assignments | A/R | | | | | |
| RSM 1.7 | Submit Resource Assignments for Review | A/R | C | | C | C | |
| RSM 2.0 | **Fulfill Resource Request** | | | | | | |
| RSM 2.1 | Confirm Resource Availability | | A/R | | | | |
| RSM 2.2 | Unapproved Resource Assignment | C | A/R | | | | |
| RSM 2.3 | Assign Resources | C | A/R | | | | |
| RSM 2.4 | Approve Resources | | A/R | | | | |
| RSM 2.5 | Communicate Resource Request Outcome | C | A/R | I | I | I | I |
| RSM 3.0 | **Maintain Resource Assignments** | | | | | | |
| RSM 3.1 | Identify Re-planning Requirements | A/R | C | | C | | |
| RSM 3.2 | Review Resource Assignments | C | A/R | | C | C | |
| RSM 3.3 | Delete Unused Allocations | | A/R | | | | |
| RSM 3.4 | Update Resource Assignments | | A/R | | | | |
| RSM 3.5 | Delete Resource Assignments | | A/R | | | | |
| RSM 3.6 | Monitor Resource Assignments | | A/R | | | | |

R: Responsible, A: Accountable, C: Consulted, I: Informed

## Process Phases

| Phase | States | Summary |
|---|---|---|
| **RSM 1.0: Create and Submit** | Unassigned, Pending | Requester creates resource assignments, ensures completeness, adjusts if needed, then submits for review/approval by resource managers. |
| **RSM 2.0: Fulfill Request** | Unassigned, Approved, Unapproved, Pending | Manager receives request, compares against availability and competing demands, negotiates with requester, assigns/approves or unapproves, communicates outcome. |
| **RSM 3.0: Maintain Assignments** | Completed, Canceled | Requester identifies re-planning needs; Manager reviews and updates. Completed when End Date reached. Canceled: delete if no actuals, or zero out future hours if actuals exist. |

## Task Details

### RSM 1.0: Create and Submit Resource Assignment

The Resource Requester performs all tasks in this phase:

- **RSM 1.1 - Confirm Resource Requirements**: Confirm requirements within a project, demand, enhancement, epic, story, or change. Choose a named resource or group.
- **RSM 1.2 - Select Required Resource Group**: Specify the group if requesting from a pool (e.g., 'Analyst' group).
- **RSM 1.3 - Select Group Member Preference**: Functional groups (need one member) or matrix groups (all members needed).
- **RSM 1.4 - Determine Effort**: Set effort type: FTE, hours, or person days. All are ultimately broken down to hours.
- **RSM 1.5 - Create Resource Assignment**: Create the initial assignment based on above inputs. Assign costs when appropriate.
- **RSM 1.6 - Update Resource Assignment**: Refine until finalized. Requested allocations are automatically updated by ServiceNow.
- **RSM 1.7 - Submit for Review**: Submit to the resource manager. Assignment is locked for editing by the requester once submitted.

### RSM 2.0: Fulfill Resource Request

The Resource Manager performs all tasks in this phase:

- **RSM 2.1 - Confirm Resource Availability**: View assignments awaiting approval via the Requested module or RM Workspace. Weigh against capacity and competing demands.
- **RSM 2.2 - Reject Resource Assignment**: If no resources are available, unapprove the assignment.
- **RSM 2.3 - Assign Resources**: If available, assign the appropriate resource(s).
- **RSM 2.4 - Confirm Resources**: Pending = still in review; Assigned = named resource allocated but not approved; Approved = approved to proceed.
- **RSM 2.5 - Communicate Outcome**: Notify the Requester and impacted stakeholders of the result.

### RSM 3.0: Maintain Resource Assignments

- **RSM 3.1 - Identify Re-planning Requirements** (Requester): Determine if re-planning is needed (e.g., delays, changed timeframe).
- **RSM 3.2 - Confirm Approved Assignment** (Requester): Verify named resource is assigned and state is Approved.
- **RSM 3.3 - Review Assignment** (Manager): Determine next steps: complete, update (shift allocations/replace resources), cancel, or delete.
- **RSM 3.4 - Delete Unused Allocations** (Manager): Before marking complete, ensure unused allocations are deleted; otherwise they remain unusable.
- **RSM 3.5 - Update Allocations** (Manager): Direct changes move state back to Pending. Use "Reassign Work" to replace resources. For delays: change End Date (within work item dates) or create a new assignment.
- **RSM 3.6 - Delete Assignment** (Manager): Only for assignments with no actuals reported.
- **RSM 3.7 - Cancel Assignment** (Manager): Set all future allocations to "0" via the RM Workspace.
- **RSM 3.8 - Complete Assignment** (Manager): When all tasks/projects are done and unused allocations are zeroed out.

## Operational Resource Assignment

An operational resource assignment reserves a portion of the team's capacity for operational (non-project) work. Typically, a resource manager creates these for their team, often for a longer duration (e.g., one year) to plan for operational work in advance.

Examples of non-project work: meetings, training, KTLO activities, admin work.

**Best practice**: Plan operational work capacity at the beginning of the year or quarter.

## Resource Management Workspace

The Resource Management Workspace provides Resource Managers a centralized view of all work across all resources.

### Capabilities

- **Allocation boards**: Create focused views to view and work on resource allocations, filtered by:
  - Primary Group
  - Primary Group Manager
  - Primary Resource Role
  - Primary Resource Skill
  - User Manager
- **Resource grid**: List of all resources and associated resource assignments with actions:
  - Edit row, change state, modify allocation amounts (weekly/monthly)
  - Unassign Work (if assignment has not begun)
  - Reassign Work (replace individual resources)
- **Unassigned Work view**: View unassigned resource assignments with "Assign Work" action (can select multiple resources to split work)
- **Heatmap modals**: Breakdown view of assigned work and efforts
- **Header options**: Timeline, Status, Unassigned tasks toggle, Hours/FTE/Person days view, Week/Month view, Export, Delete Board, Column Configuration

**Important**: Resource Assignments must fall within the project/demand/work item date boundaries.

## Walkthrough: Common Operations

**Creating a Resource Assignment**:
1. Select "New" from the Resource Assignment Related list on a Demand, Project, or Work Item.
2. Choose group or user (specific individual).
3. Select the resource group or named resource.
4. Fill in Role, Skill, Effort Type, and Effort, then Save.

**Fulfilling a Resource Request**:
1. Resource manager confirms availability from the RM Workspace resource grid. Over-allocated resources are visually indicated.
2. Insufficient resources: "Unapprove" by editing the Resource Status field.
3. Resources available: assign the resource and mark as "Approved."
4. Unassigned assignments: use "Assign Work" from the Unassigned Task section, enter resource(s), and click "Allocate."

**Maintaining Resource Assignments**:
1. To extend: change the End Date directly on the Resource Assignment record.
2. Resource managers can edit allocations directly inline in the workspace.

## Capacity Planning

The Capacity Planning screen (in Strategic Planning/Portfolio Planning Workspaces) provides portfolio managers with a comprehensive view of capacity, allocations, and utilization:

- View resource capacity for prioritized portfolio items
- Understand resource capacity needs by group, role, skill, or other resource attributes (department, cost center, etc.)
- Forecast supply of resources and demand of work
- View allocation health with color indicators including overallocations
- Plan for resources with specific skills or roles for future assignments

## Custom Planning Attributes

ServiceNow Resource Management supports custom planning attributes beyond the OOTB group, role, and skill.

### Considerations

- Custom planning attributes start from fields on the Employee Profile record. Any field on that record or one dot-walk away (e.g., fields on the User table) can be used. Two-hop dot-walks are not supported.
- Use data in a reference table as a planning attribute.
- After configuring, recalculate capacity in the Strategic Planning Workspace for impacted resources.

### Setup Steps

1. **Create Planning Attribute Record**: Navigate to All > Strategic Planning > Planning Attributes > New. Set Attribute Type = Resource, Attribute Name, Enable for Capacity Planning if needed, Attribute Table = Employee Profile, Attribute Field.
2. **Add Reference Field to Tables**: Add a reference field on each of these tables:
   - Resource Plan (`resource_plan`)
   - Resource Assignment (`sn_plng_att_core_resource_assignment`)
   - Resource Allocation (`resource_allocation`)
   - Attribute Aggregate Combination (`sn_plng_att_core_cpaam_combination`) -- only if using Capacity
3. **Update Planning Attribute Record**: Identify the reference field in the Planning Attribute column configuration, then set Active = true.
4. **Modify Resource Assignment Form**: Add the new field to both Default and Operational work views. Create a UI Policy to make the field read-only when Assignment Type = group.
5. **Modify Workspace List Views**: Add the new attribute to Project Workspace View, Resource Manager View, and Resource Unassigned View.
6. **Modify Column Configuration**: Reset columns in both Project Workspace and RM Workspace to include the new attribute.

## Key Tables

| Table Name | Label | Description |
|---|---|---|
| `resource_plan` | Resource Plan | Top-level resource plan associated with a project, demand, or work item |
| `resource_allocation` | Resource Allocation | Individual resource allocation records linking resources to assignments |
| `resource_allocation_daily` | Resource Allocation Daily | Daily breakdown of resource allocation hours |
| `resource_aggregate_weekly` | Resource Aggregate Weekly | Weekly aggregated resource allocation and capacity data |
| `resource_aggregate_monthly` | Resource Aggregate Monthly | Monthly aggregated resource allocation and capacity data |
| `requested_allocation` | Requested Allocation | Allocation records for requested (not yet approved) resource assignments |
| `resource_role` | Resource Role | Defines resource roles used as planning attributes |
| `user_has_resource_role` | User Has Resource Role | Maps users to their assigned resource roles |
| `resource_event` | Resource Event | Calendar events affecting resource availability (vacations, holidays, etc.) |
| `user_has_schedule` | User Has Schedule | Associates users with their work schedules |
| `time_card` | Time Card | Individual time card entries for tracking actual hours worked |
| `time_sheet` | Time Sheet | Time sheet records grouping time cards for a reporting period |
| `time_card_daily` | Time Card Daily | Daily breakdown of time card entries |
| `sn_plng_att_core_resource_assignment` | Resource Assignment | Resource assignment records (Next Experience / planning attributes model) |
| `sn_plng_att_core_cpaam_combination` | Attribute Aggregate Combination | Capacity planning aggregate combinations for custom planning attributes |

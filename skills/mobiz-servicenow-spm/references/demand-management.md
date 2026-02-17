# Demand Management Process Guide

Reference for ServiceNow SPM Demand Management (Zurich release).

## Overview

A **Demand** is a request for a new product or service, or a change to an existing one, that requires expenditure of resources to deliver. Demands compete for resources and must be evaluated and prioritized relative to the business value they provide.

Users can create a Demand through the Service Catalog or submit an Idea that gets promoted to a Demand. Not all Ideas become Demands -- Ideas can be set to "Unlikely to implement" or converted directly to a project, epic, initiative, or story.

## Process Goal

Centrally capture all strategic and operational demand requests for evaluation, comparison, prioritization, and approval or denial based on organizational needs.

## Process Objectives

- Capture, centralize, and assess strategic and operational demands
- Provide a single-entry point for demand requests to prevent "side projects" or unapproved resource assignments
- Ensure prioritized, categorized, and approved demands are scheduled and fulfilled consistently
- Give managers complete visibility of demand for their resources to optimize utilization

## Relationship with Other Processes

| Process | Relation | Input | Output |
|---------|----------|:-----:|:------:|
| Portfolio Management | Provides assessed/prioritized list of investments for portfolio review | X | |
| Project Management | Approved large demands become Projects | | X |
| Agile Development / SAFe | Demands convert to Stories, Epics, or Agile items | X | X |
| Change Management | Changes can be an output of the Demand Process | | X |
| Resource Management | Resource Assignments can be generated from a Demand | X | X |
| Financial Management | Cost and Benefit plans can be generated from a Demand | X | X |
| Incident Management | Incidents can generate demands if of sufficient size | X | |
| Problem Management | Problems can generate demands if of adequate size | X | |
| Continual Improvement Management | Improvement Initiatives can be created from/to a Demand | X | X |
| Investment Funding | Funding for Demands managed via Investment Funding app | | X |
| Roadmap Planning | Demands are planning items used in Strategic Planning | X | |
| Strategy and Goal Management | Primary/secondary goals can be linked to demands | X | |
| Enterprise Architecture (APM) | Demands can be generated to retire or develop business applications | X | X |

## Demand States (Lifecycle)

Demand is tracked through these lifecycle states. The state determines available actions.

### Draft

The demand manager accepts a submitted idea, or a Business User creates a new Demand from the Service Catalog. Business Users can add collaborators who can update the Demand.

Available actions: **Update**, **Submit Demand**, **Delete**

### Submitted

An accepted idea creates a demand record, or a business user submits a Demand directly. The business user or collaborator can update a demand until it progresses to Screening.

Available actions: **Update**, **Screen**, **Qualify**, **Defer**, **Delete**, **Reset to Draft**

### Screening

The demand manager initiates assessments for the demand. Assessments are sent to stakeholders. During screening, the demand is scored and a business case is finalized.

Available actions: **Update**, **Qualify**, **Defer**, **Delete**, **Reset to Draft**

### Qualified

The demand has been qualified and is ready for review. ServiceNow automatically sets the demand to Qualified once all assessments are submitted, or the Demand Manager can qualify manually.

Available actions: **Update**, **Approve**, **Defer**, **Delete**, **Reset to Draft**

### Deferred

The demand has been put on hold and can be revisited in the future (typically at the next governance meeting).

Available actions: **Update**, **Approve**, **Reset to Draft**, **Delete**

### Approved

The demand is approved for execution. The Demand Manager creates the corresponding output record (project, enhancement, etc.).

Available actions: **Update**, **Close**, **Delete**, **Reset to Draft**

### Completed

The demand is moved to completed state. This happens automatically when the related record (Project, Enhancement, Change, etc.) is closed, or the Demand Manager can complete it manually based on the "Close Demand" preference field.

## Demand Tasks

Demand tasks delegate cost, effort, risk, and benefit assessment activities. You can assign a resource or group to track actual time and effort spent on assessment work.

## RIDAC

Risks, Issues, Decisions, Actions, and Request Changes can be managed within demands. These items carry forward when a demand is converted to a project or other output record.

## Strategy and Goal Allocations

You can allocate a percentage of demand cost/benefit to Goals and Strategies. The planned/actual cost/benefit is distributed to the strategy/goal based on the allocation percentage and values in Cost Plans and Benefit Plans.

## Process Roles

| Role | Responsibilities |
|------|-----------------|
| **Process Owner** | Senior manager who ensures the process is rolled out and used across IT. Defines mission, establishes goals, resolves cross-functional issues, reports effectiveness, initiates improvements. |
| **Demand Manager** | Manages day-to-day process activities. Drives efficiency, gathers metrics, delegates work via demand tasks. |
| **BRM (Business Relationship Manager)** | Maintains customer relationships, identifies needs, ensures service provider meets needs. Works closely with Demand Manager. |
| **IT Steering Group (ISG)** | Sets direction and strategy for IT Services. Reviews business/IT alignment. Sets priorities for service development programs/projects. |
| **Business User / Requester** | Identifies need, problem, or opportunity. Obtains commitment from an internal Sponsor. |
| **Collaborator** | Contributes to demand by providing subject matter expertise. |
| **Stakeholder** | Individuals involved in the project or whose interests may be affected by it. Complete assessments during screening. |

## RACI Matrix

| ID | Activity | Business User | Demand Manager | Stakeholders | ServiceNow |
|----|----------|:---:|:---:|:---:|:---:|
| DMD 1.1 | Submit Idea | R | A | | |
| DMD 1.2 | Submit Defect Demand from Incident | R | A | | |
| DMD 1.3 | Submit Enhancement Demand from Change | R | A | | |
| DMD 1.4 | Submit Enhancement Demand from Problem | R | A | | |
| DMD 1.5 | Submit Demand | R/A | R/A | | |
| DMD 1.6 | Promote Idea to Demand | I | R/A | | |
| DMD 2.1 | Assist Completion of Demand | C | R/A | C | |
| DMD 2.2 | Add T-Shirt Size, Impact, Business Drivers, Timeline | C | R/A | | |
| DMD 2.3 | Add Resource Assignments to Demand | C | R/A | C | |
| DMD 2.4 | Add Cost & Benefit Plans to Demand | C | R/A | C | |
| DMD 2.5 | Update Portfolio, Stakeholders, Requirements, Allocations | C | R/A | I | |
| DMD 2.6 | Move Demand to Screening | I | R/A | I | |
| DMD 2.7 | Complete Assessments | I | I | R/A | |
| DMD 2.8 | Move Demand to Qualified (Auto) | I | I | I | R/A |
| DMD 2.9 | Move Demand to Qualified (Manual) | I | R/A | I | |
| DMD 3.1 | Review Demands | C | A | R | |
| DMD 3.2 | Defer Demand | I | A | R | |
| DMD 3.3 | Set Demand to Approved | I | R/A | I | |
| DMD 3.4 | Create Execution Activity Record | I | R/A | I | |
| DMD 3.5 | Generate Activity Record | I | I | I | R/A |
| DMD 3.6 | Set Demand to Complete | I | I | I | R/A |

R: Responsible, A: Accountable, C: Consulted, I: Informed

## Process Phases Detail

### Phase 1: Create Demand (DMD 1.0) -- Draft to Submitted

Demand creation paths:
- **DMD 1.1** Submit Idea via Service/Idea Portal or Innovation Portal (Business User)
- **DMD 1.2** Create Demand from APM to retire or develop an application (Application Owner)
- **DMD 1.3** Create Enhancement Demand from a CIM improvement initiative (Change User)
- **DMD 1.4** Create Demand from Digital Portfolio Management Workspace (Digital Product Manager)
- **DMD 1.5** Create Demand via Service Portal catalog item or Demand Application (Business User / Demand Manager)
- **DMD 1.6** Promote Idea to Demand after evaluating size, scope, and impact (Demand Manager)

### Phase 2: Enhance and Assess Demand (DMD 2.0) -- Screening to Qualified

- **DMD 2.1** Demand Manager populates additional details, may create Demand Tasks for assistance
- **DMD 2.2** Add T-Shirt Size, Impact, Business Drivers, and high-level timeline
- **DMD 2.3** Add Resource Assignments (for large/medium demands)
- **DMD 2.4** Add Cost & Benefit Plans for financial return calculations (for large demands)
- **DMD 2.5** Set Portfolio (auto-populates stakeholders), add Requirements, allocate to Strategies/Goals
- **DMD 2.6** Move to Screening -- sends assessments to all stakeholders
- **DMD 2.7** Stakeholders complete assessments on Strategic Alignment and Risk categories
- **DMD 2.8** Auto-Qualify: ServiceNow sets to Qualified when all assessments submitted
- **DMD 2.9** Manual Qualify: Demand Manager can qualify at any point during Screening

### Phase 3: Approve Demand (DMD 3.0) -- Approved to Completed

- **DMD 3.1** Stakeholders review Qualified demands via Workbench during governance meetings
- **DMD 3.2** Defer Demand for future reconsideration
- **DMD 3.3** Approve Demand for execution
- **DMD 3.4** Create output record based on Category and Type (see conversion rules below)
- **DMD 3.5** System copies critical data (stakeholders, requirements, risks, decisions, resources, cost/benefit plans) to new record
- **DMD 3.6** Auto-completed when related record closes, or manually by Demand Manager

## Demand-to-Output Conversion Rules

The output record type is determined by the demand's **Category** and **Type** fields:

| Category | Type | Creates |
|----------|------|---------|
| Strategic | Project | Project Record |
| Strategic | Enhancement | Agile Enhancement Record |
| Strategic | Feature | Feature or SAFe Feature Record |
| Strategic | Story | Story or SAFe Story Record |
| Strategic | Epic | Epic or SAFe Epic Record |
| Strategic | CIM | Continual Improvement Management Record |
| Operational | Defect | Agile Defect Record |
| Operational | Change | Change Record |

## Key Demand Fields

### Header Fields

| Field | Purpose | Type | When Populated |
|-------|---------|------|----------------|
| Name* | Name for the demand | Text | Draft |
| Category* | Categorizes demand as Operational vs Strategic | Choice | Draft/Submitted |
| Type* | Type of demand (Project, Enhancement, Change, Defect, Story, Epic, Feature, CIM, No Conversion) | Choice | Draft/Submitted |
| Number | Auto-generated identification number | Auto | Draft/Submitted |
| Start Date | Planned start date (cascades to cost/resource assignments if configured) | Date | Draft/Submitted |
| Due Date | Requested completion date | Date | Draft/Submitted |
| Description | Brief description (copied from Idea if promoted) | String | Draft/Submitted |

### Details Fields

Key reference fields: Portfolio, Program, Submitted By, Demand Manager, Project Manager, Department, Business Unit, Idea (source idea if promoted).

Key choice fields: Investment Class (Change/Transformation vs Run/KTLO), Investment Type, Priority.

Other: Collaborators (watch-list of users who can view/edit), Impacted Business Unit, Business Capabilities, Business Applications.

### Business Case Fields

| Field | Purpose |
|-------|---------|
| Strategic Priority | Read-only, displayed from primary goal |
| Primary Goal | Goal this demand helps achieve |
| Business Case | Arguments justifying the need |
| Risk of Performing | Risks if demand is implemented |
| Risk of Not Performing | Risks if demand is not approved |
| Enablers | Key enablers |
| Barriers | Major barriers |
| In Scope / Out of Scope | Scope boundaries |
| Assumptions | Assumptions for scope, risk, and estimates |

### Financial Fields

Capital Expense (Capex), Operating Expense (Opex), Total Planned Cost (Capex + Opex), Financial Benefit (estimated revenue), Financial Return (cost minus benefit), ROI %, Discount Rate, Net Present Value, Internal Rate of Return %. Also: Capital Budget, Operating Budget, Demand Actual Cost.

### Assessment Data Fields

| Field | Purpose |
|-------|---------|
| Impact | High, Medium, or Low |
| Risk | Calculated from assessment |
| Value | Calculated business value from assessment |
| T-Shirt Size | XX-Large, X-Large, Large, Medium, Small |
| Score | Calculated from risk, value, and size (high risk/size = low score; high value = high score) |
| Assessment Required | Checkbox to enable assessments |

### Preferences

| Field | Purpose |
|-------|---------|
| Close Demand | When to auto-close demand after conversion to project |
| Project Calculation | Sets Calculation field on resulting project record |

### Related Lists

Demand Tasks, Stakeholders, Requirements, Risks, Issues, Decisions, Actions, Request Changes, Resource Assignments, Cost Plans, Benefit Plans, Non-monetary Benefit Plans, Baselines, Budget, Assessment Instances/Results, Strategy Allocations, Goal Allocations, Expense Lines, Goals.

## Demand Workbench

Central location for viewing and assessing demands. Displays demands in Screening or Qualified states by default. Two panes:

- **Bubble Chart** (top): Plots demands on Risk (X), Value (Y), Size (Z), scale 0-10. Quadrants: upper-left = high value/low risk (green); lower-right = low value/high risk (red); other two = "Consider" (orange).
- **List View** (bottom): Demand details synced with bubble chart. Supports filtering, searching, and creating output artifacts.

## Recommended Metrics

- **% Demands Submitted from total Draft** -- indicates submission quality
- **Total Approved Demands** -- future project delivery workload
- **% Demands moving to Approved** -- investment requirements indicator
- **% Demands needing More Information** -- training needs indicator
- **Average time Submitted to Approved** -- process efficiency measure

## Key Tables

| Table | Label | Description |
|-------|-------|-------------|
| `dmn_demand` | Demand | Core demand records with lifecycle state, category, type, and all demand fields |
| `dmn_decision` | Demand Decision | Decisions recorded against demands (part of RIDAC) |
| `dmn_requirement` | Demand Requirement | Requirements associated with demands, carried forward to projects |
| `dmn_stakeholder_register` | Stakeholder Register | Master stakeholder records for portfolios and demands |
| `dmn_m2m_demand_stakeholder` | Demand Stakeholder (M2M) | Many-to-many relationship linking stakeholders to specific demands |
| `idea` | Idea | Ideas submitted via ideation that can be promoted to demands |
| `dmn_demand_task` | Demand Task | Tasks delegated for demand assessment activities |
| `assessment_instance` | Assessment Instance | Individual assessment instances sent to stakeholders during screening |
| `cost_plan` | Cost Plan | Cost plans associated with demands |
| `benefit_plan` | Benefit Plan | Benefit plans (financial and non-monetary) associated with demands |

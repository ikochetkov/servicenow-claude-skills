# SPM Structured Import Format Specification

Canonical template for generating project hierarchies that can be imported into ServiceNow SPM via the AI Bridge. Use this format when converting SOW documents, project plans, or requirements into SPM artifacts.

## Format Overview

The structured import format is a markdown document with clearly labeled sections following the SPM hierarchy. Each section contains records with their field values.

## Table Mappings

| Document Section | ServiceNow Table | API Name |
|-----------------|-----------------|----------|
| PROJECT DEFINITION | Project | `pm_project` |
| PORTFOLIO | Portfolio | `pm_portfolio` |
| PROGRAM | Program | `pm_program` |
| PROJECT PHASES | Project Task | `pm_project_task` |
| MILESTONES | Milestone | `pm_milestone` |
| EPICS | Epic | `rm_epic` |
| STORIES | Story | `rm_story` |
| RESOURCE ASSIGNMENTS | Resource Plan | `resource_plan` |
| DEPENDENCIES | Planned Task Relationship | `planned_task_rel_planned_task` |

## Hierarchy Rules

```
Portfolio (optional)
  └── Program (optional)
        └── Project (required)
              ├── Phase (pm_project_task, parent = project)
              │     ├── Sub-phase (pm_project_task, parent = phase)
              │     │     └── Milestone (pm_milestone, parent = sub-phase)
              │     └── Milestone (pm_milestone, parent = phase)
              ├── Epic (rm_epic)
              │     └── Story (rm_story, epic = epic)
              └── Resource Plan (resource_plan, top_task = project)
```

## Field Requirements

| Field Type | Format | Examples |
|-----------|--------|---------|
| Dates | ISO 8601 | `2026-03-01`, `2026-03-01 09:00:00` |
| Effort | Hours (integer) | `8`, `40`, `120` |
| Story Points | Integer (Fibonacci) | `1`, `2`, `3`, `5`, `8`, `13`, `21` |
| State | String | `Draft`, `Open`, `Work in Progress` |
| References | Local ID or name | `PT-001`, `EPIC-001`, `Igor Kochetkov` |

## Import Order

1. Create Project
2. Create all Phases and sub-phases (parent → child order)
3. Create all Milestones (linked to their parent phases)
4. Create all Epics
5. Create all Stories (linked to epics and assigned to users)
6. Create Resource Plans (linking users to the project)
7. Set all Dependencies between tasks

---

## Template Sections

### PROJECT DEFINITION

```markdown
## PROJECT DEFINITION

### Project
- **Name:** <Project Name>
- **Short Name:** <SHORT-CODE>
- **Type:** Project
- **Start Date:** YYYY-MM-DD
- **End Date:** YYYY-MM-DD
- **State:** Draft
- **Project Manager:** <Full Name>
- **Description:** <Project description>
- **Expected Benefits:**
  - <Benefit 1>
  - <Benefit 2>
```

### PORTFOLIO & PROGRAM (Optional)

```markdown
## PORTFOLIO & PROGRAM (OPTIONAL)

### Portfolio
- **Name:** <Portfolio Name>
- **Owner:** <Full Name>
- **Type:** <Strategic Initiative | Operational | etc.>

### Program
- **Name:** <Program Name>
- **Parent Portfolio:** <Portfolio Name>
- **Program Manager:** <Full Name>
- **Child Projects:**
  - <This project name>
```

### PROJECT PHASES

```markdown
## PROJECT PHASES

### Phase 1: <Phase Name>
- **Task ID:** PT-001
- **Name:** <Phase Name>
- **Type:** Project Task (Phase)
- **Parent:** Project: <Project Name>
- **Assigned To:** <Full Name>
- **Start Date:** YYYY-MM-DD
- **End Date:** YYYY-MM-DD
- **Duration:** <N> days
- **Planned Effort:** <N> hours
- **State:** Draft
- **Description:** <Phase description>

#### Sub-Phase: PT-001.1 - <Sub-phase Name>
- **Task ID:** PT-001.1
- **Name:** <Sub-phase Name>
- **Type:** Project Task
- **Parent:** PT-001
- **Assigned To:** <Full Name>
- **Start Date:** YYYY-MM-DD
- **End Date:** YYYY-MM-DD
- **Duration:** <N> days
- **Planned Effort:** <N> hours
- **State:** Draft

##### Milestone: MS-001 - <Milestone Name>
- **Type:** Milestone
- **Parent Phase:** PT-001.1
- **Date:** YYYY-MM-DD HH:MM:SS
- **Gate Type:** <Internal | External Deliverable | Customer-Facing>
- **Gate Criteria:** <What must be true>
- **Approver:** <Full Name>
```

### EPICS

```markdown
## EPICS

### Epic 1: <Epic Name>
- **Epic ID:** EPIC-001
- **Name:** <Epic Name>
- **Parent Phase:** PT-001 (informational link)
- **Description:** <Epic description>
- **Story Points:** <Total points>
- **Start Date:** YYYY-MM-DD
- **End Date:** YYYY-MM-DD
- **State:** Draft
```

### STORIES

```markdown
## STORIES

### EPIC-001: <Epic Name>

#### Story: Story-001.1
- **Name:** <Story Name>
- **Parent Epic:** EPIC-001
- **Assigned To:** <Full Name>
- **Story Points:** <Points>
- **Planned Effort:** <N> hours
- **Start Date:** YYYY-MM-DD HH:MM:SS
- **End Date:** YYYY-MM-DD HH:MM:SS
- **State:** Draft
- **Description:** <Story description>
- **Acceptance Criteria:** <Definition of done>
- **Dependencies:** <Task/Story IDs this depends on>
```

### RESOURCE ASSIGNMENTS

```markdown
## RESOURCE ASSIGNMENTS

### Resource: <Full Name>
- **Role:** <Role title>
- **Allocation:** <Percentage>%
- **Total Planned Effort:** <N> hours
- **Assigned Phases:** <Phase IDs>
- **Assigned Stories:** <Story ID range>
- **Notes:** <Availability, vacation, etc.>
```

### DEPENDENCY MATRIX

```markdown
## DEPENDENCY MATRIX

**Key Dependencies:**
- <Source task/phase> → <Target task/phase> (finish-to-start)
- <All stories in Phase X> depend on <Phase Y completion>
```

### IMPORT NOTES

```markdown
## IMPORT NOTES FOR AI

**Table Mappings:**
- Project → pm_project
- Phase (Project Task) → pm_project_task
- Milestone → pm_milestone
- Epic → rm_epic
- Story → rm_story
- Resource → sys_user (link via resource_plan)

**Import Order:**
1. Create Project
2. Create Phases and sub-phases
3. Create Milestones
4. Create Epics
5. Create Stories
6. Create Resource Plans
7. Set Dependencies

**Total Artifacts to Create:**
- N Projects
- N Phases
- N Sub-Phases
- N Milestones
- N Epics
- N Stories
- N Resource Assignments
- N Dependencies
```

---

## Minimal Example

A small project to use as a template or test:

```markdown
# SERVICENOW SPM - STRUCTURED IMPORT FORMAT

## PROJECT DEFINITION

### Project
- **Name:** Website Redesign
- **Short Name:** WEB-2026-Q2
- **Start Date:** 2026-04-01
- **End Date:** 2026-05-31
- **State:** Draft
- **Project Manager:** Jane Smith
- **Description:** Redesign corporate website with modern UI

## PROJECT PHASES

### Phase 1: Discovery
- **Task ID:** PT-001
- **Name:** Discovery & Requirements
- **Parent:** Project: Website Redesign
- **Assigned To:** Jane Smith
- **Start Date:** 2026-04-01
- **End Date:** 2026-04-14
- **Planned Effort:** 80 hours
- **State:** Draft

##### Milestone: MS-001 - Requirements Signed Off
- **Parent Phase:** PT-001
- **Date:** 2026-04-14 17:00:00
- **Gate Criteria:** Stakeholder sign-off on requirements document
- **Approver:** Jane Smith

### Phase 2: Design & Development
- **Task ID:** PT-002
- **Name:** Design & Development
- **Parent:** Project: Website Redesign
- **Assigned To:** John Doe
- **Start Date:** 2026-04-15
- **End Date:** 2026-05-16
- **Planned Effort:** 160 hours
- **State:** Draft

### Phase 3: Testing & Launch
- **Task ID:** PT-003
- **Name:** Testing & Launch
- **Parent:** Project: Website Redesign
- **Assigned To:** Jane Smith
- **Start Date:** 2026-05-17
- **End Date:** 2026-05-31
- **Planned Effort:** 60 hours
- **State:** Draft

##### Milestone: MS-002 - Go Live
- **Parent Phase:** PT-003
- **Date:** 2026-05-31 17:00:00
- **Gate Criteria:** All tests passed, stakeholder approval
- **Approver:** Jane Smith

## EPICS

### Epic 1: Frontend Redesign
- **Epic ID:** EPIC-001
- **Name:** Frontend Redesign
- **Description:** New UI components and responsive layout
- **Story Points:** 21
- **Start Date:** 2026-04-15
- **End Date:** 2026-05-16
- **State:** Draft

## STORIES

### EPIC-001: Frontend Redesign

#### Story: Story-001.1
- **Name:** Homepage Wireframe
- **Parent Epic:** EPIC-001
- **Assigned To:** John Doe
- **Story Points:** 3
- **Planned Effort:** 8 hours
- **Start Date:** 2026-04-15
- **End Date:** 2026-04-16
- **State:** Draft
- **Description:** Create wireframe for new homepage layout
- **Acceptance Criteria:** Wireframe approved by design team

#### Story: Story-001.2
- **Name:** Homepage Implementation
- **Parent Epic:** EPIC-001
- **Assigned To:** John Doe
- **Story Points:** 8
- **Planned Effort:** 24 hours
- **Start Date:** 2026-04-17
- **End Date:** 2026-04-22
- **State:** Draft
- **Description:** Implement homepage based on approved wireframe
- **Acceptance Criteria:** Homepage renders correctly on desktop and mobile
- **Dependencies:** Story-001.1

#### Story: Story-001.3
- **Name:** Contact Page
- **Parent Epic:** EPIC-001
- **Assigned To:** John Doe
- **Story Points:** 5
- **Planned Effort:** 16 hours
- **Start Date:** 2026-04-23
- **End Date:** 2026-04-25
- **State:** Draft
- **Description:** Build contact page with form and map
- **Acceptance Criteria:** Form submits successfully, map renders

## RESOURCE ASSIGNMENTS

### Resource: Jane Smith
- **Role:** Project Manager
- **Allocation:** 50%
- **Total Planned Effort:** 60 hours

### Resource: John Doe
- **Role:** Frontend Developer
- **Allocation:** 100%
- **Total Planned Effort:** 160 hours

## DEPENDENCY MATRIX
- PT-001 → PT-002 (finish-to-start)
- PT-002 → PT-003 (finish-to-start)
- Story-001.1 → Story-001.2 (finish-to-start)

## IMPORT NOTES FOR AI

**Total Artifacts:**
- 1 Project
- 3 Phases
- 2 Milestones
- 1 Epic
- 3 Stories
- 2 Resource Assignments
- 3 Dependencies
```

---

## Converting a SOW to This Format

When converting from a SOW or project proposal:

1. **Extract project metadata**: name, dates, PM, description, objectives
2. **Identify phases**: map SOW sections/phases to project tasks
3. **Identify milestones**: deliverable dates, gates, approvals
4. **Extract work items**: convert SOW deliverables/tasks to epics and stories
5. **Map resources**: team members, roles, allocations from the SOW
6. **Identify dependencies**: sequential phases, story prerequisites
7. **Estimate effort**: convert SOW effort estimates to hours and story points
8. **Generate the structured format** using the templates above

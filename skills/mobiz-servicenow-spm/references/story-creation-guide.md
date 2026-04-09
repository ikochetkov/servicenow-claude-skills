# Mobiz Story Creation Guide (rm_story)

Complete workflow for creating stories properly on the Mobiz ServiceNow instance. Follow this guide every time a user asks to create a story.

## Mandatory Fields

| # | Field | API Name | Type | How to Populate |
|---|---|---|---|---|
| 1 | **Project** | `project` | Reference (pm_project) | Resolve from keywords — see [Step 1](#step-1-resolve-project) |
| 2 | **Assignment Group** | `assignment_group` | Reference (sys_user_group) | Auto-populate from project — see [Step 2](#step-2-resolve-assignment-group) |
| 3 | **Assigned To** | `assigned_to` | Reference (sys_user) | From context or ask user — see [Step 3](#step-3-resolve-assigned-to) |
| 4 | **Update Sets** | `u_update_sets` | String | Update set name + deployment instructions — see [Step 4](#step-4-update-sets) |
| 5 | **Planned Effort** | `effort` | Duration | Estimate or ask user — see [Step 5](#step-5-planned-effort) |
| 6 | **Short Description** | `short_description` | String | Concise story title |
| 7 | **Description** | `description` | String | Detailed story description |
| 8 | **Acceptance Criteria** | `acceptance_criteria` | String | Definition of done — testable conditions |
| 9 | **Company** | `company` | Reference (core_company) | Always **Mobiz IT** |
| 10 | **Domain** | `sys_domain` | Reference | Always **Mobiz (MSP)** |

## Optional Fields

These are typically NOT filled in unless the user specifically requests them:

| Field | API Name | Type | Notes |
|---|---|---|---|
| Sprint | `sprint` | Reference (rm_sprint) | Only if sprint planning is active |
| Epic | `epic` | Reference (rm_epic) | Parent epic if story is part of one |
| Theme | `theme` | Reference (rm_theme) | Strategic theme grouping |
| Story Points | `story_points` | Integer | Fibonacci: 1, 2, 3, 5, 8, 13, 21 |
| Priority | `priority` | Choice | 1-Critical, 2-High, 3-Moderate, 4-Low |
| State | `state` | Choice | Default: -6 (Draft) |
| Project Phase | `project_phase` | Reference (pm_project_task) | **Cannot be set on create — requires separate PUT** |

---

## Step-by-Step Workflow

### Step 1: Resolve Project

**If the user does not specify a project, STOP and ask.** Do not create a story without a project.

The user typically provides keywords from the project name. Search `pm_project` by name:

```
sn_query table=pm_project query=short_descriptionLIKE{keywords}^active=true fields=sys_id,number,short_description,u_default_agile_teams,company limit=5
```

If multiple matches, show the user the list and ask them to pick. If no matches, ask for different keywords.

### Step 2: Resolve Assignment Group

After resolving the project, read the project's `u_default_agile_teams` field. This is a **glide_list** (comma-separated sys_ids) of assignment groups.

**If the project has one group** → auto-populate `assignment_group` with that sys_id.

**If the project has multiple groups** → show the user the group names and ask which one to use:

```
sn_query table=sys_user_group query=sys_idIN{comma_separated_sys_ids} fields=sys_id,name
```

**If the project has no groups** (`u_default_agile_teams` is empty) → ask the user which assignment group to use.

### Step 3: Resolve Assigned To

- If the context makes it clear who should be assigned (e.g., the user says "assign to me" or "assign to Oleksandr"), resolve the user from `sys_user`.
- If NOT clear, ask the user: "Who should this story be assigned to?"

### Step 4: Update Sets

The `u_update_sets` field documents which update sets are needed for this story and any special deployment instructions.

**Format:** Update set name + short deployment notes if applicable.

Examples:
- `FA-STRY0013753` — simple update set reference
- `FA-STRY0013753 — Install ServiceNow SDK app v2.1 after committing update set`
- `FA-STRY0014001 — Move XML export of sys_properties manually to PROD before committing`

If the user is creating a new story for ServiceNow work, the update set name typically follows the pattern: `FA-{story_number}` (e.g., `FA-STRY0013753`).

### Step 5: Planned Effort

The `effort` field uses **GlideDuration format**: `"1970-01-01 HH:MM:SS"`

| Hours | Duration Value |
|---|---|
| 1 hour | `1970-01-01 01:00:00` |
| 2 hours | `1970-01-01 02:00:00` |
| 4 hours | `1970-01-01 04:00:00` |
| 8 hours (1 day) | `1970-01-01 08:00:00` |
| 16 hours (2 days) | `1970-01-01 16:00:00` |
| 24 hours (3 days) | `1970-01-02 00:00:00` |
| 40 hours (1 week) | `1970-01-02 16:00:00` |

If you have enough context to estimate the effort (e.g., from a SOW or similar past stories), set it yourself. Otherwise, ask the user.

---

## Domain and Company Defaults

**Always set these for Mobiz internal ServiceNow stories:**
- `company` = Mobiz IT (resolve sys_id from `core_company` where `name=Mobiz IT`)
- `sys_domain` = Mobiz (MSP) domain

These are ServiceNow platform development stories — they always belong to the Mobiz IT company and the Mobiz (MSP) domain.

---

## Complete Example: Create a Story via MCP Tool

```
sn_create table=rm_story data={
  "short_description": "AI Validation - revert changes and make presales category only mandatory",
  "description": "Revert the AI validation changes from previous sprint. Update category field to make presales mandatory only (not all categories). Update business rule and UI policy accordingly.",
  "acceptance_criteria": "1. Presales category is mandatory on the form\n2. Other categories are not mandatory\n3. AI validation business rule reflects the change\n4. Tested on DEV instance",
  "project": "{resolved_project_sys_id}",
  "assignment_group": "{resolved_from_u_default_agile_teams}",
  "assigned_to": "{resolved_user_sys_id}",
  "effort": "1970-01-01 04:00:00",
  "u_update_sets": "FA-STRY0013753",
  "company": "{mobiz_it_sys_id}",
  "state": "-6"
}
```

**After creating the story:** If the user wants to link it to a project phase, make a separate update call (project_phase is silently ignored on create):

```
sn_update table=rm_story sys_id={story_sys_id} data={
  "project_phase": "{agile_phase_sys_id}"
}
```

---

## Story States Reference

| Value | Label | When to Use |
|---|---|---|
| -6 | Draft | Just created, not groomed |
| -5 | Ready | Groomed and ready for sprint |
| 1 | Work in Progress | Developer is actively working |
| 2 | Testing | In QA/testing |
| 3 | Complete | Dev complete, pending acceptance |
| 4 | Accepted | Product owner accepted |
| 7 | Cancelled | Story cancelled |

## Conversation Flow Summary

```
User: "Create a story for [description]"
    ↓
1. Is project specified? NO → Ask user for project keywords
                          YES → Search pm_project by keywords → confirm match
    ↓
2. Read project.u_default_agile_teams
   - 1 group → auto-set assignment_group
   - Multiple → ask user to pick
   - None → ask user
    ↓
3. Is assignee clear from context? NO → Ask user
                                    YES → Resolve sys_user
    ↓
4. Ask for/generate: short_description, description, acceptance_criteria
    ↓
5. Ask for/estimate: effort (duration), u_update_sets
    ↓
6. Create story with company=Mobiz IT, domain=Mobiz (MSP)
    ↓
7. Return story number + link to user
```

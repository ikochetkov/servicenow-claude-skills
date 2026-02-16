# Design-Time Flow Analysis

## Two Table Formats: V1 (Legacy) vs V2 (Modern)

ServiceNow Flow Designer stores flow steps in two different table hierarchies depending on when the flow was created/updated. **Always check V2 first** — if `sys_hub_flow_component` has records for the flow, it's V2.

## V2 Tables (Modern Flows)

Query directly by `flow={master_flow_sys_id}` — no deduplication needed.

```
sys_hub_flow_component           ← parent table (all V2 steps, but child-specific fields are empty)
  sys_hub_action_instance_v2     ← action steps (field: action_type)
  sys_hub_sub_flow_instance_v2   ← subflow calls (field: subflow)
  sys_hub_flow_logic_instance_v2 ← logic blocks (field: logic_definition)
sys_hub_flow_stage               ← named stages (field: label, order)
```

**Important:** Query each child table directly — the parent `sys_hub_flow_component` won't have `action_type`, `subflow`, or `logic_definition` values populated.

### V2 Action Steps

```
GET /api/now/table/sys_hub_action_instance_v2
  ?sysparm_query=flow={flow_sys_id}^ORDERBYorder
  &sysparm_fields=sys_id,ui_id,action_type,order,comment,parent_ui_id
  &sysparm_display_value=all&sysparm_limit=100
```

### V2 Subflow Calls

```
GET /api/now/table/sys_hub_sub_flow_instance_v2
  ?sysparm_query=flow={flow_sys_id}^ORDERBYorder
  &sysparm_fields=sys_id,ui_id,subflow,order,comment,parent_ui_id
  &sysparm_display_value=all&sysparm_limit=100
```

**Field name is `subflow`** (no underscore) — NOT `sub_flow`.

### V2 Logic Blocks

```
GET /api/now/table/sys_hub_flow_logic_instance_v2
  ?sysparm_query=flow={flow_sys_id}^ORDERBYorder
  &sysparm_fields=sys_id,ui_id,logic_definition,order,comment,parent_ui_id,flow_variables_assigned
  &sysparm_display_value=all&sysparm_limit=100
```

Common logic definitions: "Top Level Try", "Top Level Catch", "If", "Else", "Make a decision", "Set Flow Variables", "Wait for a duration of time"

### V2 Stages

```
GET /api/now/table/sys_hub_flow_stage
  ?sysparm_query=flow={flow_sys_id}^ORDERBYorder
  &sysparm_fields=label,order,value,always_show
  &sysparm_limit=50
```

Stages define named phases in the flow (e.g., "Create AD user", "Add to AD groups", "Sync Entra ID"). Stages only exist in V2 format.

## V1 Tables (Legacy Flows)

Query by **dot-walk** `flow.name={flow_name}` — direct sys_id filter won't work because V1 flows have multiple snapshot versions with different IDs.

```
sys_hub_action_instance   ← action steps (field: action_type)
sys_hub_sub_flow_instance ← subflow calls (field: subflow — NOT sub_flow)
sys_hub_flow_logic        ← logic blocks
```

### V1 Action Steps

```
GET /api/now/table/sys_hub_action_instance
  ?sysparm_query=flow.name={flow_name}^ORDERBYorder
  &sysparm_fields=flow,ui_id,action_type,order,comment,parent_ui_id
  &sysparm_display_value=all&sysparm_limit=200
```

### V1 Subflow Calls

```
GET /api/now/table/sys_hub_sub_flow_instance
  ?sysparm_query=flow.name={flow_name}^ORDERBYorder
  &sysparm_fields=flow,ui_id,subflow,order,comment,parent_ui_id
  &sysparm_display_value=all&sysparm_limit=200
```

### V1 Deduplication Strategy

V1 queries return results from ALL snapshot versions of the flow. To get the correct step list:

1. Group results by `flow` value (each unique flow value = one version/snapshot)
2. For each version, count total steps (actions + subflows + logic)
3. Pick the version with the most combined steps (most complete version)
4. Within that version, deduplicate by `ui_id` (keep first occurrence)

### V1 Order Notation

- Normal order: `1`, `2`, `3`
- Arrow notation: `6➛7` indicates a wait step (flow pauses and resumes)

## Common Tables (Both Formats)

### Catalog Item → Flow Link

```
GET /api/now/table/sc_cat_item
  ?sysparm_query=name={item_name}
  &sysparm_fields=sys_id,name,flow_designer_flow
  &sysparm_display_value=all
```

`flow_designer_flow` references `sys_hub_flow`.

### Trigger Type

```
GET /api/now/table/sys_hub_trigger_instance
  ?sysparm_query=flow.name={flow_name}
  &sysparm_fields=trigger_type,comment
  &sysparm_display_value=all
```

### Label Cache (Shortcut — Partial Data Only)

`sys_hub_flow.label_cache` is a JSON field containing steps whose outputs are referenced by other steps. This is a quick way to see some steps, but it **misses many consumer-only steps** that don't produce referenced outputs.

```
GET /api/now/table/sys_hub_flow
  ?sys_id={flow_sys_id}
  &sysparm_fields=sys_id,name,label_cache
```

## Step Hierarchy

In both V1 and V2, `parent_ui_id` creates a nesting hierarchy:
- Top-level steps have no `parent_ui_id` (or it points to a logic block like "Top Level Try")
- Steps nested inside If/Else/Try/Catch blocks have `parent_ui_id` pointing to that logic block
- This allows reconstructing the visual nesting seen in Flow Designer UI

## Format Detection Strategy

```
1. Get flow sys_id from sc_cat_item.flow_designer_flow or sys_hub_flow query
2. Check sys_hub_flow_component for flow={sys_id} (limit=1)
3. If count > 0 → V2 (query _v2 child tables directly by flow={sys_id})
4. If count = 0 → V1 (query legacy tables by flow.name={name}, deduplicate)
```

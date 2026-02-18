# Stage Usage Analysis

Detect which flow stages are actively used by steps vs defined but never triggered. This helps identify stale or misconfigured stages.

## Key Concept: `component_indexes`

The `sys_hub_flow_stage` table has a **`component_indexes`** field that directly maps each stage to the flow components (steps) that set it. This is the single source of truth — no need to query step tables.

- **null or empty** → stage is unused (no step sets this stage)
- **has values** (e.g., `"2"` or `"5,9"`) → stage is used (component at that `order` value sets it)

The values in `component_indexes` are comma-separated `order` values from `sys_hub_flow_component`.

## Query Pattern

### Step 1: Fetch stages with component_indexes

```
GET /api/now/table/sys_hub_flow_stage
  ?sysparm_query=flow={flow_sys_id}^ORDERBYorder
  &sysparm_fields=sys_id,label,order,value,always_show,component_indexes
  &sysparm_limit=50
```

### Step 2: Classify each stage

For each stage record:
```
used = component_indexes is not null AND component_indexes is not empty string
```

### Step 3 (Optional): Map to specific steps

To identify which step sets each stage, query the flow components:

```
GET /api/now/table/sys_hub_flow_component
  ?sysparm_query=flow={flow_sys_id}^ORDERBYorder
  &sysparm_fields=sys_id,sys_class_name,order,name
  &sysparm_display_value=all&sysparm_limit=200
```

Then match: stage `component_indexes` value `"2,5"` → components with `order=2` and `order=5`.

Component `sys_class_name` tells you the type:
- `sys_hub_action_instance_v2` → action step
- `sys_hub_sub_flow_instance_v2` → subflow call
- `sys_hub_flow_logic_instance_v2` → logic block (If, End, etc.)

## Reporting Example

When asked "which stages are created but not used?", produce a breakdown like:

```
Flow: MHS - Unlock Active Directory Account
Format: V2
Total stages: 6
Used: 3 | Unused: 3

USED STAGES:
  1. Request Cancelled (order 0) — set by: End block (component #11)
  2. Fulfillment (order 3) — set by: MHS - Look Up User in AD (component #2)
  3. Completed (order 4) — set by: End block (component #5), End block (component #9)

UNUSED STAGES:
  1. Delivery (order 1) — no steps reference this stage
  2. Waiting for Approval (order 2) — no steps reference this stage
  3. Request Approved (order 5) — no steps reference this stage
```

## Bulk Analysis: All Flows with Unused Stages

To find all flows that have unused stages:

### Step 1: Get all stages with empty component_indexes

```
GET /api/now/table/sys_hub_flow_stage
  ?sysparm_query=component_indexesISEMPTY
  &sysparm_fields=sys_id,label,order,flow,component_indexes
  &sysparm_display_value=all&sysparm_limit=500
```

### Step 2: Group by flow

Group the results by `flow` display value to see which flows have unused stages and how many.

## Important Notes

- **V2 only**: Stages (`sys_hub_flow_stage`) only exist in V2 format flows. V1 flows do not have stages.
- **`always_show` is independent of usage**: All stages may have `always_show=1` regardless of whether they're actually referenced. This field controls portal display, not step assignment.
- **Stages set by logic blocks**: Stages are often set by End/Complete logic blocks, not just action steps. The `component_indexes` may point to `sys_hub_flow_logic_instance_v2` records like "End Flow" that transition the request to a specific stage.
- **Multiple components per stage**: A stage can be set by multiple steps (e.g., `component_indexes: "5,9"` means two different paths can transition to this stage).

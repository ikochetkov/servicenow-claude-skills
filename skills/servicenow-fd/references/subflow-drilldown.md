# Subflow Drill-Down

## Recursive Subflow Analysis

Any subflow referenced in a flow can be analyzed using the same query patterns. The process is recursive — subflows can contain other subflows.

## Finding a Subflow's sys_id

When you query `sys_hub_sub_flow_instance_v2` or `sys_hub_sub_flow_instance`, the `subflow` field contains:
- `value`: The sys_id of the subflow in `sys_hub_flow`
- `display_value`: The human-readable name (e.g., "MHS - Add User to AD Groups")

## Drill-Down Strategy

### Step 1: Get the subflow's master flow record

```
GET /api/1851835/ai_adapter_rest/sys_hub_flow
  ?sys_id={subflow_sys_id}
  &sysparm_fields=sys_id,name,label_cache
  &sysparm_display_value=all
```

### Step 2: Check format (V2 or V1)

```
GET /api/1851835/ai_adapter_rest/sys_hub_flow_component
  ?sysparm_query=flow={subflow_sys_id}
  &sysparm_limit=1
```

### Step 3: Query steps using the same patterns as parent flow

**V2 (3 parallel queries):**
```
GET /api/1851835/ai_adapter_rest/sys_hub_action_instance_v2
  ?sysparm_query=flow={subflow_sys_id}^ORDERBYorder
  &sysparm_fields=sys_id,ui_id,action_type,order,comment,parent_ui_id
  &sysparm_display_value=all&sysparm_limit=100

GET /api/1851835/ai_adapter_rest/sys_hub_sub_flow_instance_v2
  ?sysparm_query=flow={subflow_sys_id}^ORDERBYorder
  &sysparm_fields=sys_id,ui_id,subflow,order,comment,parent_ui_id
  &sysparm_display_value=all&sysparm_limit=100

GET /api/1851835/ai_adapter_rest/sys_hub_flow_logic_instance_v2
  ?sysparm_query=flow={subflow_sys_id}^ORDERBYorder
  &sysparm_fields=sys_id,ui_id,logic_definition,order,comment,parent_ui_id,flow_variables_assigned
  &sysparm_display_value=all&sysparm_limit=100
```

**V1 (use subflow name in dot-walk, then deduplicate):**
```
GET /api/1851835/ai_adapter_rest/sys_hub_action_instance
  ?sysparm_query=flow.name={subflow_name}^ORDERBYorder
  &sysparm_fields=flow,ui_id,action_type,order,comment,parent_ui_id
  &sysparm_display_value=all&sysparm_limit=200
```

## Example: Error Handler Subflow

A typical error handler subflow pattern found in MHS flows:

```
MHS Onboarding Flow Error Handler (11 steps)
├── Top Level Try
│   ├── Set Flow Variables (set error context)
│   ├── If (check if RITM exists)
│   │   ├── Look Up Record (get RITM details)
│   │   ├── Update Record (set RITM to error state)
│   │   └── Create Catalog Task (manual remediation)
│   └── Else
│       └── Log (log that RITM was not found)
├── Top Level Catch
│   └── Log (log the catch error — graceful degradation)
└── Subflow: Send Notification (alert admins)
```

This demonstrates **graceful degradation** — even the error handler has its own try/catch to prevent cascading failures.

## Depth Limiting

For complex flows with deeply nested subflows, consider limiting drill-down depth to avoid excessive API calls. Typical approach:
1. First level: Always analyze (parent flow)
2. Second level: Analyze on request (user asks "what's inside subflow X?")
3. Third level+: Summarize from label_cache if available, full analysis only if specifically requested

## Presenting Subflow Results

When presenting subflow analysis, show:
1. **Total step count** (actions + subflows + logic blocks)
2. **Hierarchical view** using indentation to show parent/child nesting via `parent_ui_id`
3. **Step comments** — these often contain the best human-readable descriptions
4. **Nested subflow names** — highlight which steps are themselves subflows that could be drilled into further

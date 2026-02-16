---
name: servicenow-fd
description: ServiceNow Flow Designer analysis and diagnostics. Describes flow structure (actions, subflows, logic blocks, stages), fetches runtime execution details (state, logs, errors, timing), drills into subflows recursively, and generates visual Mermaid diagrams. Supports both V1 (legacy) and V2 (modern) flow table formats. Triggers on flow designer, sys_hub_flow, flow execution, flow analysis, flow steps, subflow, flow diagram, flow logs, flow errors, flow stages, catalog item flow, RITM execution.
---

# ServiceNow Flow Designer Analysis

Analyze any ServiceNow Flow Designer flow — describe its structure, fetch execution history, drill into subflows, and generate visual diagrams.

## Capabilities

| Capability | Description |
|-----------|-------------|
| **Design-time analysis** | List all steps (actions, subflows, logic blocks), stages, and triggers for any flow |
| **Runtime execution** | Fetch latest execution, state, runtime, logs, warnings, and errors |
| **Subflow drill-down** | Recursively describe any subflow's internal steps |
| **Visual diagrams** | Generate Mermaid flowcharts from flow structure |
| **Catalog item linkage** | Find which flow is linked to a catalog item |

## Prerequisites

The **ServiceNow AI Bridge** adapter must be installed on the target instance. All queries use:
```
https://{instance}/api/1851835/ai_adapter_rest/{table}
```

See [references/api-patterns.md](references/api-patterns.md) for authentication and query format.

## Quick Start

### Find a catalog item's flow

```
GET /api/1851835/ai_adapter_rest/sc_cat_item
  ?sysparm_query=name={item_name}
  &sysparm_fields=sys_id,name,flow_designer_flow
  &sysparm_display_value=all
```

The `flow_designer_flow` field links to `sys_hub_flow`. Save the sys_id for all subsequent queries.

### Detect table format (V1 vs V2)

Flows use one of two table formats. **Always check V2 first:**

```
GET /api/1851835/ai_adapter_rest/sys_hub_flow_component
  ?sysparm_query=flow={flow_sys_id}
  &sysparm_limit=1
```

- **Records found** → V2 format (use `_v2` tables, query by `flow={sys_id}`)
- **No records** → V1 format (use legacy tables, query by `flow.name={name}`)

See [references/design-time-analysis.md](references/design-time-analysis.md) for complete V1 and V2 query patterns.

### Get flow steps (V2 — 3 parallel queries)

```
GET /api/1851835/ai_adapter_rest/sys_hub_action_instance_v2
  ?sysparm_query=flow={flow_sys_id}^ORDERBYorder
  &sysparm_fields=sys_id,ui_id,action_type,order,comment,parent_ui_id
  &sysparm_display_value=all&sysparm_limit=100

GET /api/1851835/ai_adapter_rest/sys_hub_sub_flow_instance_v2
  ?sysparm_query=flow={flow_sys_id}^ORDERBYorder
  &sysparm_fields=sys_id,ui_id,subflow,order,comment,parent_ui_id
  &sysparm_display_value=all&sysparm_limit=100

GET /api/1851835/ai_adapter_rest/sys_hub_flow_logic_instance_v2
  ?sysparm_query=flow={flow_sys_id}^ORDERBYorder
  &sysparm_fields=sys_id,ui_id,logic_definition,order,comment,parent_ui_id,flow_variables_assigned
  &sysparm_display_value=all&sysparm_limit=100
```

### Get flow stages (V2 only)

```
GET /api/1851835/ai_adapter_rest/sys_hub_flow_stage
  ?sysparm_query=flow={flow_sys_id}^ORDERBYorder
  &sysparm_fields=label,order,value,always_show
  &sysparm_limit=50
```

### Get latest execution

```
GET /api/1851835/ai_adapter_rest/sys_flow_context
  ?sysparm_query=flow={flow_sys_id}^ORDERBYDESCsys_created_on
  &sysparm_fields=sys_id,name,state,run_time,source_record,source_table,error_message,stages,reporting,sys_created_on,calling_source,execution_id
  &sysparm_display_value=all&sysparm_limit=1
```

See [references/runtime-execution.md](references/runtime-execution.md) for execution logs and RITM details.

### Generate a diagram

After fetching flow steps, generate a Mermaid flowchart. See [references/visual-diagrams.md](references/visual-diagrams.md) for patterns.

## Reference Documents

| Document | Content |
|----------|---------|
| [references/design-time-analysis.md](references/design-time-analysis.md) | V1 vs V2 table formats, complete query patterns, deduplication strategy |
| [references/runtime-execution.md](references/runtime-execution.md) | Execution tables, log levels, RITM details, error analysis |
| [references/subflow-drilldown.md](references/subflow-drilldown.md) | Recursive subflow analysis patterns |
| [references/visual-diagrams.md](references/visual-diagrams.md) | Mermaid flowchart generation from flow data |
| [references/api-patterns.md](references/api-patterns.md) | AI Bridge adapter authentication and query format |

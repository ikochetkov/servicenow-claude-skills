# Programmatic Flow Designer Creation

Build ServiceNow Flow Designer flows via API — create flow records, insert steps, wire inputs with scripts or data pills, and encode payloads correctly.

## Overview

Flow Designer stores flows across several V2 tables. To build a flow programmatically:

1. Create the flow record (`sys_hub_flow`)
2. Create flow variables (optional)
3. Insert logic instances — Set Flow Variables, If, Else, etc. (`sys_hub_flow_logic_instance_v2`)
4. Insert action instances — the actual work steps (`sys_hub_action_instance_v2`)
5. Register each step as a flow component (`sys_hub_flow_component`)
6. Populate input values via the gzip/base64 `values` column on each instance

## Tables Used

| Table | Purpose | When to Use |
|-------|---------|-------------|
| `sys_hub_flow` | Flow definition (name, trigger, scope, status) | Always — root record |
| `sys_hub_flow_variable` | Flow-scoped variables (name, type, default) | When flow needs variables |
| `sys_hub_flow_logic_instance_v2` | Logic blocks: Set Flow Variables, If, Else, For Each, etc. | Conditional/assignment steps |
| `sys_hub_action_instance_v2` | Action steps: spoke actions, subflow calls, timers, etc. | Core work steps |
| `sys_hub_flow_component` | Index of all steps in a flow (parent table linking components to flow) | Every step must be registered here |
| `sys_hub_flow_stage` | Named stages (optional, V2 only) | Multi-stage flows |
| `sys_hub_action_input` | **Global** action type input definitions (read-only) | Discover what inputs an action type requires |

## Step-by-Step Process

### 1. Create the Flow Record

```
POST /api/now/table/sys_hub_flow
{
  "name": "My Flow Name",
  "internal_name": "my_flow_name",
  "trigger_type": "<trigger_sys_id>",
  "scope": "global",
  "active": true,
  "status": "draft"
}
```

Common trigger types:
- **SLA Task:** The trigger for SLA-based flows (fires when task_sla records change state)
- **Record Created/Updated:** Standard record triggers
- **Scheduled:** Time-based triggers

Save the returned `sys_id` — all subsequent steps reference it as the `flow` field.

### 2. Create Flow Variables (optional)

```
POST /api/now/table/sys_hub_flow_variable
{
  "flow": "<flow_sys_id>",
  "name": "my_variable",
  "internal_name": "my_variable",
  "type": "boolean",
  "default_value": "false"
}
```

Variable types: `string`, `boolean`, `integer`, `reference`, `glide_date_time`, etc.

### 3. Insert Steps

Every step needs:
- `flow` — the flow sys_id
- `order` — integer determining execution sequence within the same parent
- `ui_id` — a UUID you generate (e.g., `a0000001-0001-4000-8000-000000000001`)
- `parent_ui_id` — the `ui_id` of the parent (e.g., an If block), or empty for root-level steps
- `values` — the gzip/base64 encoded input payload (see Section 4)

#### Logic instances (If, Set Flow Variables, etc.)

```
POST /api/now/table/sys_hub_flow_logic_instance_v2
{
  "flow": "<flow_sys_id>",
  "logic_definition": "<logic_def_sys_id>",
  "order": 100,
  "ui_id": "a0000001-0001-4000-8000-000000000001",
  "parent_ui_id": "",
  "comment": "Set notifications_enabled = true",
  "values": "<base64_gzip_json>"
}
```

Common logic definitions:
| Logic | sys_id |
|-------|--------|
| Set Flow Variables | `4f787d1e0f9b0010ecf0cc52ff767ea0` |
| If | `af4e1945c3e232002841b63b12d3ae3e` |
| Else If | `76401bc7c72132006fe02e0c0a076134` |
| Else | `d7b2da85c3e232002841b63b12d3ae20` |
| For Each | `3a00d9c5c3e232002841b63b12d3ae34` |

#### Action instances (Spoke actions, timers, etc.)

```
POST /api/now/table/sys_hub_action_instance_v2
{
  "flow": "<flow_sys_id>",
  "action_type": "<action_type_sys_id>",
  "order": 200,
  "ui_id": "a0000002-0002-4000-8000-000000000002",
  "parent_ui_id": "a0000001-0001-4000-8000-000000000001",
  "comment": "50% SLA warning to owner",
  "values": "<base64_gzip_json>"
}
```

### 4. The Values Payload — Encoding and Structure

This is the most critical and complex part. **All action/logic inputs are stored in a single `values` column as Base64-encoded gzip JSON.**

#### Encoding (write)

```python
import base64, gzip, json

payload = [...]  # array for action instances, object for logic instances
json_str = json.dumps(payload)
compressed = gzip.compress(json_str.encode('utf-8'))
encoded = base64.b64encode(compressed).decode('utf-8')
# Set encoded as the 'values' field value
```

#### Decoding (read)

```python
import base64, gzip, json

decoded = base64.b64decode(values_string)
decompressed = gzip.decompress(decoded).decode('utf-8')
parsed = json.loads(decompressed)
```

#### Values structure for ACTION instances

An **array** of input objects, one per action input parameter:

```json
[
  {
    "id": "<input_definition_sys_id>",
    "name": "ah_channel",
    "value": "C040E6FUHPS",
    "displayValue": "C040E6FUHPS",
    "children": [],
    "parameter": {
      "type": "string",
      "label": "Channel ID / Member ID",
      "mandatory": true,
      "sys_id": "<param_sys_id>"
    },
    "scriptActive": false,
    "script": {
      "ah_channel": {
        "scriptActive": false,
        "script": ""
      }
    }
  },
  {
    "id": "<next_input_sys_id>",
    "name": "ah_message",
    "value": "",
    "displayValue": "",
    "children": [],
    "parameter": { "..." : "..." },
    "scriptActive": true,
    "script": {
      "ah_message": {
        "scriptActive": true,
        "script": "var task = fd_data.trigger.task_sla_record.task;\nreturn task.number + '';"
      }
    }
  }
]
```

Key fields per input:
- **`id`** — sys_id from `sys_hub_action_input` for this specific parameter definition
- **`name`** — internal parameter name (e.g., `ah_channel`, `blocks`)
- **`value`** — static value OR data pill reference (when `scriptActive` is false)
- **`scriptActive`** — `true` if this input uses a script, `false` for static/data pill
- **`script`** — nested object keyed by the parameter name; contains the actual script code when `scriptActive: true`

#### Values structure for LOGIC instances (Set Flow Variables)

An **object** (not array):

```json
{
  "outputsToAssign": [],
  "inputs": [
    {
      "name": "notifications_enabled",
      "value": "1",
      "scriptActive": false
    }
  ],
  "variables": [
    {
      "id": "<flow_variable_sys_id>",
      "name": "notifications_enabled",
      "type": "boolean",
      "label": "notifications_enabled"
    }
  ],
  "decisionTableInputs": [],
  "dynamicInputs": [],
  "workflowInputs": []
}
```

#### Values structure for IF logic instances

```json
{
  "lhsOperand": {
    "name": "condition_field",
    "value": "{{FlowVar.my_variable}}",
    "scriptActive": false
  },
  "operator": "=",
  "rhsOperand": {
    "name": "condition_value",
    "value": "1",
    "scriptActive": false
  }
}
```

### 5. Register Flow Components

Every step (logic or action instance) must also be registered in `sys_hub_flow_component`:

```
POST /api/now/table/sys_hub_flow_component
{
  "flow": "<flow_sys_id>",
  "component": "<step_sys_id>",
  "component_table": "sys_hub_action_instance_v2",
  "order": 200,
  "ui_id": "<same_ui_id_as_step>",
  "parent_ui_id": "<same_parent_ui_id_as_step>"
}
```

Use `component_table = sys_hub_flow_logic_instance_v2` for logic steps.

## Discovering Action Type Inputs

Before populating a values payload, you need to know which inputs an action type expects. Query `sys_hub_action_input` for the action type:

```
GET /api/now/table/sys_hub_action_input
  ?sysparm_query=action_type=<action_type_sys_id>^model_type=input
  &sysparm_fields=sys_id,name,label,type,mandatory,default_value,order
  &sysparm_display_value=all
  &sysparm_limit=50
```

This returns every input parameter defined for that action type. Each result gives you:
- **sys_id** — use as the `id` field in the values array
- **name** — the internal parameter name (e.g., `ah_channel`, `percentage`)
- **label** — human-readable label (e.g., "Channel ID / Member ID")
- **type** — data type (string, boolean, integer, reference, etc.)
- **mandatory** — whether the input is required

### Known Action Type Input Maps

#### Mobiz Slack Message (`998a9a3a8770b1500f79caec0ebb350d`)

| Input | Parameter sys_id | Type | Required |
|-------|-----------------|------|----------|
| ah_channel | `d98a9a3a8770b1500f79caec0ebb351e` | string | Yes |
| ah_message | `d18a9a3a8770b1500f79caec0ebb3523` | string | Yes |
| blocks | `9d8a9a3a8770b1500f79caec0ebb3526` | string | No |
| ah_username | `118a9a3a8770b1500f79caec0ebb3537` | string | No |
| ah_icon | `d98a9a3a8770b1500f79caec0ebb353a` | string | No |
| send_from_dev_and_uat_instances | (boolean) | boolean | No |
| do_not_redirect | (boolean) | boolean | No |
| ts | (string) | string | No |

#### SLA Percentage Timer (`a1a50c4573873300d70877186bf6a762`)

| Input | Type | Required |
|-------|------|----------|
| percentage | integer | Yes |
| task_sla_record | reference (task_sla) | Yes |
| sla_flow_inputs | complex JSON | No |

## Data Pills vs Scripts

There are two ways to wire an input value:

### Static value or data pill (scriptActive: false)

Set `value` directly. For data pills, use the `{{TriggerLabel_N.field.path}}` syntax:

```json
{
  "name": "ah_channel",
  "value": "{{SLA Task_1.task_sla_record.task.assigned_to.u_slack_id}}",
  "scriptActive": false,
  "script": { "ah_channel": { "scriptActive": false, "script": "" } }
}
```

**Data pill format:** `{{<TriggerName>_<N>.<field>.<dot>.<walk>}}`
- The trigger name comes from the flow's trigger type display value
- The `_N` suffix is typically `_1` for the first trigger
- Field paths mirror GlideRecord dot-walking

### Script (scriptActive: true)

Leave `value` empty, set the script:

```json
{
  "name": "blocks",
  "value": "",
  "scriptActive": true,
  "script": {
    "blocks": {
      "scriptActive": true,
      "script": "var task = fd_data.trigger.task_sla_record.task;\nvar number = task.number + '';\nreturn JSON.stringify([{type:'section',text:{type:'mrkdwn',text:number}}]);"
    }
  }
}
```

**fd_data context in scripts:**
- `fd_data.trigger.<field>` — trigger record fields
- `fd_data.flow_var.<name>` — flow variables
- `fd_data.action_output.<step_label>.<output>` — outputs from previous steps
- Scripts must `return` a value
- All GlideRecord methods available (`.getDisplayValue()`, `.getValue()`, etc.)
- `gs.getProperty()` works for system properties

### Mapping data pill path to fd_data path

| Data pill | fd_data equivalent |
|-----------|-------------------|
| `{{SLA Task_1.task_sla_record}}` | `fd_data.trigger.task_sla_record` |
| `{{SLA Task_1.task_sla_record.task}}` | `fd_data.trigger.task_sla_record.task` |
| `{{SLA Task_1.task_sla_record.task.number}}` | `fd_data.trigger.task_sla_record.task.number` |
| `{{SLA Task_1.task_sla_record.percentage}}` | `fd_data.trigger.task_sla_record.percentage` |

**Key difference:** Data pills use `TriggerLabel_N.` prefix; fd_data uses `fd_data.trigger.` prefix. The rest of the dot-walk path is identical.

## Parent-Child Nesting

Steps inside conditional blocks (If, Else, For Each) must reference the parent's `ui_id` in their `parent_ui_id` field.

```
Flow root
├── Step 1: Set Flow Variables (parent_ui_id = "")         ← ROOT level
├── Step 2: If (parent_ui_id = "")                         ← ROOT level
│   ├── Step 3: SLA Timer 50% (parent_ui_id = Step 2 ui_id)
│   ├── Step 4: Slack 50% (parent_ui_id = Step 2 ui_id)
│   ├── Step 5: SLA Timer 80% (parent_ui_id = Step 2 ui_id)
│   └── ...all child steps reference Step 2's ui_id
```

Steps at the same nesting level execute in `order` sequence.

## Ordering Convention

Use increments of 100 for `order` values (100, 200, 300...) to leave room for insertions:

| Step | Order |
|------|-------|
| Set Flow Variables | 100 |
| If | 200 |
| First action inside If | 100 (resets within parent) |
| Second action inside If | 200 |
| Third action inside If | 300 |

## Workflow: Interactive Flow Building

When a user asks to build a flow, follow this sequence:

### Phase 1: Gather requirements
1. Ask for the flow name, trigger type, and high-level purpose
2. Ask which actions/spoke actions the flow will use
3. For each action type, query `sys_hub_action_input` to discover required inputs

### Phase 2: Collect input values
For each action step, present the user with the discovered inputs:
```
"For the Mobiz Slack Message action, I need values for these inputs:
 - Channel ID / Member ID (required) — static value, data pill, or script?
 - Message (required) — the fallback text
 - Blocks — Slack Block Kit JSON (optional)
 - Username — display name (optional)
 - Icon — emoji shortcode (optional)"
```

### Phase 3: Build the payload
1. Construct the values JSON for each step
2. Encode as gzip -> base64
3. Create the flow record, then each step via API
4. Register each step in `sys_hub_flow_component`

### Phase 4: Verify
1. Query back all steps to confirm they were created
2. Decode and display values to verify correctness
3. Flow will need to be activated/published via the Flow Designer UI

## Worked Example: SLA Notification Flow

The Mobiz Security Alert SLA flow is a complete real-world example showing:
- 10-step flow with nested If block
- SLA Percentage Timer actions at 50%, 80%, 100%
- Mobiz Slack Message actions with data pills and scripts
- Slack Block Kit JSON construction in fd_data scripts
- Escalation pattern: owner DM -> manager DM -> channel broadcast

### Quick Python example: Build a Slack message step

```python
import base64, gzip, json, requests

INSTANCE = "https://mobizdev.service-now.com"
AUTH = ("user", "pass")

# Step values payload
values = [
    {
        "id": "d98a9a3a8770b1500f79caec0ebb351e",
        "name": "ah_channel",
        "value": "{{SLA Task_1.task_sla_record.task.assigned_to.u_slack_id}}",
        "displayValue": "",
        "children": [],
        "parameter": {"type": "string", "label": "Channel ID / Member ID"},
        "scriptActive": False,
        "script": {"ah_channel": {"scriptActive": False, "script": ""}}
    },
    {
        "id": "d18a9a3a8770b1500f79caec0ebb3523",
        "name": "ah_message",
        "value": "",
        "displayValue": "",
        "children": [],
        "parameter": {"type": "string", "label": "Message"},
        "scriptActive": True,
        "script": {"ah_message": {
            "scriptActive": True,
            "script": (
                "var task = fd_data.trigger.task_sla_record.task;\n"
                "var number = task.number + '';\n"
                "return ':clock3: SLA Warning: ' + number;"
            )
        }}
    }
]

# Encode
encoded = base64.b64encode(
    gzip.compress(json.dumps(values).encode('utf-8'))
).decode('utf-8')

# Create the action instance
resp = requests.post(
    f"{INSTANCE}/api/now/table/sys_hub_action_instance_v2",
    auth=AUTH,
    json={
        "flow": "<flow_sys_id>",
        "action_type": "998a9a3a8770b1500f79caec0ebb350d",
        "order": 200,
        "ui_id": "a0000004-0004-4000-8000-000000000004",
        "parent_ui_id": "<if_block_ui_id>",
        "comment": "50% warning to owner",
        "values": encoded
    },
    headers={"Content-Type": "application/json", "Accept": "application/json"}
)
print(resp.json())
```

## Reading an Existing Flow's Values (Reverse Engineering)

To understand how an existing flow is configured:

```python
import base64, gzip, json, requests

INSTANCE = "https://mobizdev.service-now.com"
AUTH = ("user", "pass")

# Fetch all action instances for a flow
resp = requests.get(
    f"{INSTANCE}/api/now/table/sys_hub_action_instance_v2",
    auth=AUTH,
    params={
        "sysparm_query": f"flow={flow_sys_id}^ORDERBYorder",
        "sysparm_fields": "sys_id,action_type,order,comment,values,ui_id,parent_ui_id",
        "sysparm_display_value": "all",
        "sysparm_limit": 50
    }
)

for step in resp.json()["result"]:
    values_raw = step.get("values", {})
    # Handle display_value format
    val_str = values_raw.get("value", values_raw) if isinstance(values_raw, dict) else values_raw
    if val_str:
        decoded = json.loads(gzip.decompress(base64.b64decode(val_str)).decode('utf-8'))
        print(f"Step {step['order']}: {step['comment']}")
        print(json.dumps(decoded, indent=2))
```

## Common Gotchas

1. **Values encoding is mandatory.** You cannot set inputs via plain fields — they MUST go through the gzip/base64 `values` column.

2. **sys_hub_action_input is global, not per-instance.** It defines what inputs an action TYPE has. The actual values for a specific step are in the `values` column on the instance record.

3. **Data pill syntax uses trigger label, not fd_data.** In the values blob: `{{SLA Task_1.field}}`. In scripts: `fd_data.trigger.field`. Don't mix them up.

4. **fd_data.trigger vs fd_data.trigger.current.** For SLA Task triggers, the trigger record is `fd_data.trigger.task_sla_record`, NOT `fd_data.trigger.current`. The path depends on the trigger type.

5. **Script must return a value.** Every script input must end with a `return` statement.

6. **String coercion.** Always append `+ ''` when reading GlideRecord fields in scripts to avoid getting GlideElement objects instead of strings.

7. **Slack emoji shortcodes.** Use `:large_yellow_circle:`, `:large_orange_circle:`, `:large_blue_circle:` — the short forms (`:yellow_circle:`) render as literal text.

8. **URLs in ServiceNow.** Use `gs.getProperty('glide.servlet.uri')` instead of hardcoding instance URLs.

9. **Parent_ui_id for nested steps.** Steps inside If/Else/ForEach blocks MUST reference the parent block's `ui_id`. Root steps leave `parent_ui_id` empty.

10. **Flow must be published via UI.** Programmatic creation sets up the structure, but the flow typically needs to be activated/published through Flow Designer's UI to become runnable.

11. **Modifying existing values.** To update a single input, you must decode the entire values blob, modify the target input, re-encode the whole thing, and PATCH it back. You cannot update individual inputs in isolation.

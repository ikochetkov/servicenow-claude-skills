# Runtime Execution Analysis

## Execution Tables

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `sys_flow_context` | Main execution record per flow run | `flow`, `state`, `run_time`, `source_record`, `error_message`, `reporting`, `execution_id` |
| `sys_flow_log` | Step-level logs per execution | `context`, `message`, `level`, `action`, `operation` |

**Tables that DON'T exist** (checked — not available in standard instances): `sys_hub_stage_execution`, `sys_hub_action_execution`, `sys_hub_flow_runtime_value`

## Fetching Executions

### Get Latest Execution of a Flow

```
GET /api/now/table/sys_flow_context
  ?sysparm_query=flow={flow_sys_id}^ORDERBYDESCsys_created_on
  &sysparm_fields=sys_id,name,state,run_time,source_record,source_table,error_message,stages,reporting,sys_created_on,calling_source,execution_id
  &sysparm_display_value=all&sysparm_limit=1
```

### Get Multiple Recent Executions

Change `sysparm_limit` to 5 or 10 to see execution history.

### Filter by State

Add state filter to the query:
- `^state=COMPLETE` — only successful executions
- `^state=ERROR` — only failed executions
- `^state=WAITING` — paused/waiting executions

### Execution Fields

| Field | Description | Example Values |
|-------|-------------|----------------|
| `state` | Execution outcome | `COMPLETE`, `WAITING`, `ERROR`, `CANCELLED` |
| `run_time` | Duration in milliseconds | `15283` (= 15.3 seconds) |
| `source_record` | Triggering record | Display: `Requested Item: RITM0047266` |
| `source_table` | Table of triggering record | `sc_req_item` |
| `error_message` | Top-level error (null if successful) | Error description string |
| `reporting` | Log verbosity level | `TRACE`, `FULL`, `ERROR_ONLY` |
| `calling_source` | What triggered the flow | `SERVICE_CATALOG`, `RECORD`, `SCHEDULE` |
| `execution_id` | Unique execution identifier | `T3gsuIknrmvmHR1I2ZBFwUt9kaM1jEjJ` |

## Fetching Execution Logs

### Get All Logs for an Execution

```
GET /api/now/table/sys_flow_log
  ?sysparm_query=context={execution_sys_id}^ORDERBYsys_created_on
  &sysparm_fields=context,message,level,action,operation,sys_created_on
  &sysparm_display_value=all&sysparm_limit=100
```

### Log Levels

| Value | Display | Meaning |
|-------|---------|---------|
| `1` | Warning | Non-fatal issue (missing variable, undeclared output) |
| `2` | Error | Database errors, script failures, API call failures |
| `3` | Info | Informational messages |

### Log Fields

| Field | Description |
|-------|-------------|
| `message` | Full error/warning text. Errors include Java stack traces. |
| `level` | Severity: 1=Warning, 2=Error, 3=Info |
| `action` | Dot-delimited path showing which step generated the log (e.g., `FlowName.StageID.StepID.ActionID`) |
| `operation` | Operation type (often null) |
| `sys_created_on` | Timestamp of the log entry |

### Common Log Patterns

**Missing catalog variable:**
```
Warning: Missing catalog variable: secondary_email
```
The flow expects a variable that doesn't exist on the catalog item. Variable may have been renamed or removed.

**Duplicate key violation:**
```
Error: FAILED TRYING TO EXECUTE ON CONNECTION ... INSERT INTO task_m2m_skill ...
Unique Key violation detected by database
```
A business rule is trying to create a record that already exists. Usually non-fatal — the flow continues.

**AD account already exists (MID Server / PowerShell):**
```
Error: The specified account already exists (Microsoft.ActiveDirectory.Management.ADIdentityAlreadyExistsException)
Error: Failed while executing ActionCreateUserExtended.ps1
Error: IPaaSActionProbe | status=error; message=The specified account already exists
```
The flow tried to create a user in Active Directory but the account already existed. This is a fatal error for the "Create User Extended" step — the flow typically enters WAITING state and requires manual intervention.

**Undeclared output variables:**
```
Warning: Encountered undeclared output variable: Company
Warning: Encountered undeclared output variable: Manager
```
A subflow is producing output values that aren't declared in its output schema. The values are computed but can't be consumed by downstream steps.

## Fetching Source Record Details

### Get RITM Details

```
GET /api/now/table/sc_req_item
  ?sys_id={source_record_sys_id}
  &sysparm_fields=number,state,short_description,opened_by,opened_at,assigned_to,stage
  &sysparm_display_value=all
```

Extract `source_record_sys_id` from the `source_record.value` field of `sys_flow_context`.

## Building an Execution Report

Combine the queries above into a complete execution report:

1. **Fetch execution** from `sys_flow_context` — get state, runtime, source record
2. **Fetch logs** from `sys_flow_log` — get warnings, errors, info messages
3. **Fetch RITM** from `sc_req_item` — get requester, description, current state
4. **Present as table** with:
   - Execution summary (state, runtime, RITM number, requester)
   - Log entries sorted by timestamp with level indicators
   - Analysis of errors and warnings with impact assessment

### Key Insight

Even with ERROR-level logs, the execution state can still be `COMPLETE`. Database constraint violations and business rule errors are often non-fatal — the flow catches them and continues. Check the `state` field on `sys_flow_context` for the actual outcome, not just the presence of error logs.

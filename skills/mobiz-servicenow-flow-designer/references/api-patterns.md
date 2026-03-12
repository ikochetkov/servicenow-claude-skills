# ServiceNow API Patterns

## Base URL

All Flow Designer queries use the standard **ServiceNow Table API**:

```
https://{instance}/api/now/table/{table}
```

No additional plugins, adapters, or update sets required.

> **Alternative:** If the AI Bridge adapter is installed, you can also use `/api/1851835/ai_adapter_rest/{table}` with the same query parameters. The adapter adds a `meta` wrapper to responses but is otherwise identical for read operations.

## Authentication

All requests require Basic Auth:

```bash
curl -u "username:password" \
  "https://{instance}/api/now/table/{table}?{params}"
```

The user needs read access to Flow Designer tables (`sys_hub_flow`, `sys_hub_action_instance_v2`, `sys_flow_context`, etc.).

## Common Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `sysparm_query` | Encoded query filter | `flow=abc123^ORDERBYorder` |
| `sysparm_fields` | Comma-separated fields to return | `sys_id,name,state` |
| `sysparm_limit` | Max records returned | `100` |
| `sysparm_offset` | Pagination offset | `0` |
| `sysparm_display_value` | Value format | `all` (returns both value and display_value) |

## Response Format

### Table API (standard)

```json
{
  "result": [
    {
      "field_name": "value",
      ...
    }
  ]
}
```

### Table API with `sysparm_display_value=all`

Each field returns both raw and display values:

```json
{
  "result": [
    {
      "field_name": {
        "value": "raw_sys_id_or_code",
        "display_value": "Human Readable Name"
      }
    }
  ]
}
```

### AI Bridge adapter (alternative)

Wraps results in an extra layer with metadata:

```json
{
  "result": {
    "result": [ ... ],
    "meta": {
      "table": "sys_hub_action_instance_v2",
      "count": 10,
      "total_count": 10,
      "offset": 0,
      "limit": 100
    }
  }
}
```

## Query Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Equals | `flow=abc123` |
| `^` | AND | `flow=abc123^state=COMPLETE` |
| `^OR` | OR | `state=COMPLETE^ORstate=ERROR` |
| `^ORDERBYorder` | Sort ascending by field | `^ORDERBYorder` |
| `^ORDERBYDESCsys_created_on` | Sort descending | `^ORDERBYDESCsys_created_on` |
| `LIKE` | Contains | `nameLIKEEmployee` |

## Dot-Walk Queries

For V1 tables, use dot-walk to query through reference fields:

```
sysparm_query=flow.name=Mobiz New Hire
```

This traverses `flow` → `sys_hub_flow` → `name` field.

## Pagination

For large result sets:
1. First query with `sysparm_limit=100&sysparm_offset=0`
2. Check response header `X-Total-Count` for total records
3. If more exist, fetch next page with `sysparm_offset=100`

## Error Handling

| HTTP Status | Meaning |
|-------------|---------|
| 200 | Success |
| 400 | Bad request (invalid query syntax) |
| 401 | Authentication failed |
| 404 | Table or record not found |
| 500 | Server error |

## Flow Designer Tables Summary

| Table | Purpose | Format |
|-------|---------|--------|
| `sys_hub_flow` | Flow definition records | Both |
| `sys_hub_flow_component` | V2 parent table (check for V2 detection) | V2 |
| `sys_hub_action_instance_v2` | Action steps | V2 |
| `sys_hub_sub_flow_instance_v2` | Subflow calls | V2 |
| `sys_hub_flow_logic_instance_v2` | Logic blocks | V2 |
| `sys_hub_flow_stage` | Named stages | V2 |
| `sys_hub_action_instance` | Action steps (legacy) | V1 |
| `sys_hub_sub_flow_instance` | Subflow calls (legacy) | V1 |
| `sys_hub_flow_logic` | Logic blocks (legacy) | V1 |
| `sys_hub_trigger_instance` | Flow triggers | Both |
| `sys_flow_context` | Execution records | Runtime |
| `sys_flow_log` | Execution logs | Runtime |
| `sc_cat_item` | Catalog items (flow_designer_flow field) | Linkage |
| `sc_req_item` | Requested items (RITMs) | Runtime |

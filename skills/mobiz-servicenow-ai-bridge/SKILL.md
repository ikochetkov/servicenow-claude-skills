---
name: mobiz-servicenow-ai-bridge
description: |
  Dev-only AI Bridge for programmatic ServiceNow development on mobizdev.service-now.com.
  Use when creating scoped apps, business rules, REST APIs, scheduled jobs, or any ServiceNow artifacts programmatically.
  NOT available for production (mobiz.service-now.com) — production lacks the required update set.
  Keywords: AI bridge, GlideRecord, scoped app, REST API, business rule, scheduled job, artifact, dev instance
---

# Mobiz ServiceNow AI Bridge (Dev Only)

## Environment Gate — READ FIRST

**Before using this skill, you MUST determine the target environment.**

Ask the user:

> "Are your actions against the production environment or dev? If you're a ServiceNow developer planning dev work, I can connect you through the more powerful AI Bridge skill which works in the dev environment only (mobizdev.service-now.com). Otherwise, we'll use the regular ServiceNow MCP server to interact with the instance as usual (works for most actions; for development, the bridge is recommended)."

**Decision:**
- **Dev work** (mobizdev.service-now.com) → proceed with this skill
- **Production** (mobiz.service-now.com) → **STOP**. Do NOT use this skill. Explain: "The AI Bridge update set is not installed on production (mobiz.service-now.com). It will not work. Use the regular ServiceNow MCP server instead for production interactions."

> **WARNING**: The AI Bridge update set is ONLY installed on `mobizdev.service-now.com`. Any attempt to use this adapter against `mobiz.service-now.com` (production) will fail. This is by design — the adapter is a development tool and should never be used on production instances.

---

## What This Skill Does

This skill enables AI agents to programmatically create and manage any artifact in ServiceNow through a REST adapter. The adapter uses GlideRecord internally, bypassing standard Table API limitations (scope assignment, namespace control, read-only fields).

## Prerequisites

1. The "REST adapter for AI agents" XML update set is deployed on `mobizdev.service-now.com`
2. ServiceNow admin credentials for the dev instance

## Adapter Base URL

The adapter is always available at:
```
https://mobizdev.service-now.com/api/1851835/ai_adapter_rest
```

The namespace `1851835` is hardcoded in the update set, so no lookup is required.

## Why Use the Adapter?

ServiceNow's Table API has critical limitations:

| Limitation | Impact |
|------------|--------|
| Records go to **global scope** | `getSessionToken()` returns null |
| `sys_scope` parameter ignored on creation | Cannot deploy to scoped apps |
| Custom `namespace` ignored for REST APIs | URLs get auto-assigned like `/api/1851835/...` |
| Some fields are read-only | Cannot set certain system fields |

The adapter uses **GlideRecord internally**, which has none of these limitations.

## Environment Setup

Use these credentials for the dev instance:

```
SERVICENOW_INSTANCE=https://mobizdev.service-now.com
SERVICENOW_USER=admin
SERVICENOW_PASSWORD=<password>
```

The adapter base URL is always:
```
https://mobizdev.service-now.com/api/1851835/ai_adapter_rest
```

## API Reference

### Authentication

All requests require Basic Auth with admin credentials:
```bash
curl -u "admin:password" https://mobizdev.service-now.com/api/1851835/ai_adapter_rest/{tableName}
```

### GET - Query Records

```bash
GET /api/1851835/ai_adapter_rest/{tableName}
```

**Query Parameters:**
- `sysparm_query` - Encoded query string (e.g., `name=My App`)
- `sysparm_fields` - Comma-separated fields to return
- `sysparm_limit` - Max records (default: 100)
- `sysparm_offset` - Pagination offset
- `sysparm_display_value` - `true`, `false`, or `all`
- `sys_id` - Get single record by sys_id

**Examples:**
```bash
# Get all scoped applications
GET /api/1851835/ai_adapter_rest/sys_app

# Query with filter
GET /api/1851835/ai_adapter_rest/sys_properties?sysparm_query=name=x_myapp.html

# Get specific record
GET /api/1851835/ai_adapter_rest/sys_ws_definition?sys_id=abc123

# Get specific fields only
GET /api/1851835/ai_adapter_rest/sys_app?sysparm_fields=name,scope,sys_id
```

### POST - Create Record

```bash
POST /api/1851835/ai_adapter_rest/{tableName}
Content-Type: application/json

{
  "data": {
    "field1": "value1",
    "field2": "value2",
    "sys_scope": "<scope_sys_id>",
    "sys_package": "<scope_sys_id>"
  }
}
```

**Special Fields:**
- `sys_scope` - Set the scope of the record (sys_id of sys_app)
- `sys_package` - Usually same as sys_scope for scoped apps
- `namespace` - For sys_ws_definition, controls the API URL path

### PUT/PATCH - Update Record

```bash
PUT /api/1851835/ai_adapter_rest/{tableName}/{sysId}
Content-Type: application/json

{
  "data": {
    "field1": "new_value"
  }
}
```

**Update by query (use `_` as sys_id placeholder):**
```bash
PUT /api/1851835/ai_adapter_rest/sys_properties/_?sysparm_query=name=x_myapp.html
```

## Response Format

**Success:**
```json
{
  "result": {
    "sys_id": "abc123...",
    "table": "sys_app",
    "name": "My App",
    "sys_scope": "abc123...",
    "sys_scope_display": "My App"
  },
  "meta": {
    "fields_set": ["name", "scope"],
    "fields_skipped": [],
    "message": "Record created successfully"
  }
}
```

**Error:**
```json
{
  "error": {
    "message": "Record not found",
    "detail": "No record with sys_id \"xyz\" in table \"sys_app\""
  }
}
```

## Common Workflows

### Create a Scoped Application

```bash
POST /api/1851835/ai_adapter_rest/sys_app
{
  "data": {
    "name": "My Custom App",
    "scope": "x_myorg_app",
    "short_description": "Description of my app"
  }
}
# Returns: sys_id of the new scope
```

### Create REST API in Custom Scope

```bash
# 1. First create the scoped app (see above)
# 2. Create REST API with proper scope
POST /api/1851835/ai_adapter_rest/sys_ws_definition
{
  "data": {
    "name": "My API",
    "namespace": "x_myorg_app",
    "sys_scope": "<scope_sys_id>",
    "sys_package": "<scope_sys_id>",
    "active": "true"
  }
}
# Returns: base_uri shows the actual API path (e.g., /api/x_myorg_app/my_api)
```

### Create REST Endpoint in Scope

```bash
POST /api/1851835/ai_adapter_rest/sys_ws_operation
{
  "data": {
    "name": "Get Token",
    "http_method": "GET",
    "relative_path": "/get_token",
    "web_service_definition": "<api_sys_id>",
    "requires_authentication": "false",
    "requires_snc_internal_role": "false",
    "operation_script": "(function process(request, response) { ... })(request, response);",
    "sys_scope": "<scope_sys_id>",
    "sys_package": "<scope_sys_id>"
  }
}
```

### Create/Update System Property

```bash
# Create
POST /api/1851835/ai_adapter_rest/sys_properties
{
  "data": {
    "name": "x_myorg_app.config",
    "type": "string",
    "value": "configuration content here",
    "sys_scope": "<scope_sys_id>",
    "sys_package": "<scope_sys_id>"
  }
}

# Update by name
PUT /api/1851835/ai_adapter_rest/sys_properties/_?sysparm_query=name=x_myorg_app.config
{
  "data": {
    "value": "updated content"
  }
}
```

## Key Tables Reference

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `sys_app` | Scoped applications | name, scope, short_description |
| `sys_ws_definition` | Scripted REST APIs | name, namespace, base_uri, sys_scope |
| `sys_ws_operation` | REST endpoints | name, http_method, relative_path, operation_script, web_service_definition |
| `sys_properties` | System properties | name, type, value, sys_scope |
| `sys_script_include` | Server-side scripts | name, script, api_name, sys_scope |
| `sys_script` | Business rules | name, script, collection, when, sys_scope |
| `sysauto_script` | Scheduled jobs | name, script, run_type, sys_scope |
| `sys_ui_page` | UI pages | name, html, client_script, sys_scope |

## Important Notes

1. **Always query first** - Before creating, check if a record already exists
2. **Save sys_ids** - Store returned sys_ids for subsequent operations (e.g., scope sys_id for all scoped artifacts)
3. **Check base_uri** - For REST APIs, the actual URL is in `base_uri`, not derived from `namespace`
4. **Scope consistency** - Set both `sys_scope` and `sys_package` to the same scope sys_id
5. **Authentication** - The adapter requires admin credentials; all operations respect ACLs
6. **Dev only** - This adapter is ONLY available on `mobizdev.service-now.com`. Never attempt to use it on production.

## Error Handling

If a request fails:
1. Check HTTP status code (400 = bad request, 404 = not found, 500 = server error)
2. Read the `error.detail` field for specific information
3. Verify table name is correct
4. Ensure all required fields are provided
5. Check for duplicate key constraints (unique names, scopes)

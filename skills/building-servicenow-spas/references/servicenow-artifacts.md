# ServiceNow Artifacts Reference

All ServiceNow artifacts required to host a SPA. Create manually in the ServiceNow UI or programmatically via the `servicenow-ai-bridge` skill.

## Contents
- Overview of required artifacts
- System property (HTML storage)
- Scripted REST API definition
- GET /app endpoint (serve SPA)
- GET /get_token endpoint (session auth)
- GET /health endpoint (optional)
- Data endpoints (authentication rules)
- Creating artifacts: manual vs automated
- SPA access URL

## Overview of Required Artifacts

| Artifact | Type | Purpose |
|----------|------|---------|
| System Property | `sys_properties` | Stores the compiled single-file HTML |
| Scripted REST API | `sys_ws_definition` | API definition with namespace |
| GET /app endpoint | `sys_ws_operation` | Serves the SPA HTML to the browser |
| GET /get_token endpoint | `sys_ws_operation` | Returns session token for authentication |
| GET /health endpoint | `sys_ws_operation` | Health check (optional) |
| Data endpoints | `sys_ws_operation` | Your app-specific API endpoints |

## 1. System Property (HTML Storage)

Stores the entire compiled HTML of the SPA.

### Manual Creation

1. Navigate to `System Properties > All Properties`
2. Click "New"
3. Fill in:
   - **Name**: `your_namespace.spa_html` (e.g., `mobit.catalog_manager.spa_html`)
   - **Type**: `string`
   - **Value**: (leave empty — the deploy script fills this)

### Via servicenow-ai-bridge

```bash
POST /api/1851835/ai_adapter_rest/sys_properties
{
  "data": {
    "name": "your_namespace.spa_html",
    "type": "string",
    "value": "",
    "description": "Stores the compiled SPA HTML for serving via REST endpoint"
  }
}
```

Save the returned `sys_id` — you'll need it for the deploy script.

## 2. Scripted REST API Definition

The API definition that groups all your endpoints under a namespace.

### Manual Creation

1. Navigate to `Scripted REST APIs`
2. Click "New"
3. Fill in:
   - **Name**: Your API name (e.g., "Catalog Data API")
   - **API ID**: Short identifier (e.g., `catalog_data_api`)
   - **Namespace**: Your namespace (e.g., `mobit`)
   - **Active**: true

The base path will be: `/api/<namespace>/<api_id>`

### Via servicenow-ai-bridge

```bash
POST /api/1851835/ai_adapter_rest/sys_ws_definition
{
  "data": {
    "name": "My App API",
    "namespace": "my_namespace",
    "active": "true",
    "short_description": "REST API for My SPA Application"
  }
}
```

## 3. GET /app Endpoint (Serve SPA)

This endpoint reads the system property and returns the HTML to the browser.

### Endpoint Configuration

| Field | Value |
|-------|-------|
| HTTP Method | GET |
| Relative Path | `/app` |
| Requires Authentication | **false** (HTML is public; data endpoints handle auth) |
| Requires SNc Internal Role | false |

### Operation Script

```javascript
(function process(request, response) {
    var html = gs.getProperty('your_namespace.spa_html');

    if (!html) {
        response.setStatus(404);
        response.setBody({
            error: 'SPA not deployed. The system property is empty.'
        });
        return;
    }

    response.setContentType('text/html');
    response.setStatus(200);
    response.getStreamWriter().writeString(html);
})(request, response);
```

### Via servicenow-ai-bridge

```bash
POST /api/1851835/ai_adapter_rest/sys_ws_operation
{
  "data": {
    "name": "Serve SPA",
    "http_method": "GET",
    "relative_path": "/app",
    "web_service_definition": "<api_sys_id>",
    "requires_authentication": "false",
    "requires_snc_internal_role": "false",
    "operation_script": "(function process(request, response) {\n    var html = gs.getProperty('your_namespace.spa_html');\n    if (!html) {\n        response.setStatus(404);\n        response.setBody({ error: 'SPA not deployed' });\n        return;\n    }\n    response.setContentType('text/html');\n    response.setStatus(200);\n    response.getStreamWriter().writeString(html);\n})(request, response);"
  }
}
```

## 4. GET /get_token Endpoint (Session Auth)

Returns the current user's session token for CSRF protection.

### Endpoint Configuration

| Field | Value |
|-------|-------|
| HTTP Method | GET |
| Relative Path | `/get_token` |
| Requires Authentication | **false** (must be accessible before SPA has a token) |
| Requires SNc Internal Role | false |

### Operation Script

```javascript
(function process(request, response) {
    var sessionToken = gs.getSessionToken();
    var userName = gs.getUserName();
    var userDisplayName = gs.getUser().getDisplayName();
    var userSysId = gs.getUserID();

    response.setStatus(200);
    response.setBody({
        sessionToken: sessionToken,
        token: sessionToken,
        user_name: userName,
        display_name: userDisplayName,
        user_sys_id: userSysId
    });
})(request, response);
```

**Key points:**
- Returns `sessionToken` — the SPA sends this as `X-userToken` header on all subsequent requests
- Returns `user_name` — the SPA checks if this is `"guest"` to detect unauthenticated users
- This endpoint must NOT require authentication (it's the bootstrap endpoint)

### Via servicenow-ai-bridge

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
    "operation_script": "(function process(request, response) {\n    var sessionToken = gs.getSessionToken();\n    var userName = gs.getUserName();\n    var userDisplayName = gs.getUser().getDisplayName();\n    var userSysId = gs.getUserID();\n    response.setStatus(200);\n    response.setBody({\n        sessionToken: sessionToken,\n        token: sessionToken,\n        user_name: userName,\n        display_name: userDisplayName,\n        user_sys_id: userSysId\n    });\n})(request, response);"
  }
}
```

## 5. GET /health Endpoint (Optional)

Simple health check endpoint.

### Operation Script

```javascript
(function process(request, response) {
    response.setStatus(200);
    response.setBody({
        status: 'ok',
        timestamp: new GlideDateTime().getDisplayValue(),
        instance: gs.getProperty('instance_name')
    });
})(request, response);
```

## 6. Data Endpoints

All endpoints that serve application data should have `requires_authentication=true`.

### Endpoint Authentication Rules

| Endpoint Type | Auth Required | Reason |
|--------------|:---:|--------|
| `/app` (serve HTML) | No | Static HTML, no sensitive data |
| `/get_token` (session bootstrap) | No | SPA needs this before it has a token |
| `/health` (health check) | No | Monitoring/diagnostics |
| **All data endpoints** | **Yes** | Sensitive data, requires authentication |

### Example Data Endpoint

```javascript
(function process(request, response) {
    // Authentication is enforced by requires_authentication=true
    // The user's session determines access rights

    var gr = new GlideRecord('your_table');
    gr.addQuery('active', true);
    gr.query();

    var results = [];
    while (gr.next()) {
        results.push({
            sys_id: gr.getUniqueValue(),
            name: gr.getValue('name'),
            // ... other fields
        });
    }

    response.setStatus(200);
    response.setBody(results);
})(request, response);
```

## Creating Artifacts: Manual vs Automated

### Manual (ServiceNow UI)

1. Navigate to **Scripted REST APIs** in the Application Navigator
2. Create the API definition first
3. Under the API definition, create each Resource (endpoint)
4. Create the system property via **System Properties > All Properties**

### Automated (servicenow-ai-bridge skill)

If you have the `servicenow-ai-bridge` skill installed:
1. The AI agent creates all artifacts programmatically via the adapter REST API
2. No manual ServiceNow UI work needed
3. All artifacts are version-tracked in the change log

### Automated (Standard Table API)

Without the bridge, you can use ServiceNow's standard Table API, but with limitations:
- Records may go to global scope instead of your scoped app
- Namespace field may be ignored on REST API creation
- Some fields may be read-only

## SPA Access URL

After all artifacts are created and the SPA is deployed:

```
https://<instance>.service-now.com/api/<namespace>/<api_id>/app
```

Example:
```
https://mobizdev.service-now.com/api/mobit/catalog_data_api/app
```

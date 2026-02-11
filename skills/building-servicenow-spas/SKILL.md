---
name: building-servicenow-spas
description: Builds and deploys Single Page Applications to ServiceNow using Vite single-file bundling, HashRouter, and dual-mode authentication. Handles new SPA creation, existing app conversion, deployment pipelines, and ServiceNow artifact setup. Triggers on ServiceNow SPA, single page application, vite-plugin-singlefile, HashRouter, deploy to ServiceNow, embedded SPA, X-userToken, ServiceNow React app, ServiceNow dashboard.
---

# Building ServiceNow SPAs

Compiles any web app (React, Vue, Svelte, etc.) into a single HTML file via Vite + `vite-plugin-singlefile`, stores it in a ServiceNow system property, and serves it via a Scripted REST endpoint.

Reference implementation: [elinsoftware/servicenow-react-app](https://github.com/elinsoftware/servicenow-react-app)

## Architecture

```
Source Code → tsc → Vite → vite-plugin-singlefile → single index.html
  → deploy script PATCHes to ServiceNow sys_properties
  → GET /api/<namespace>/<api_id>/app serves the HTML
```

Two runtime modes (automatic switching via `isServiceNow()` hostname check):

| Aspect | Local Dev | ServiceNow |
|--------|-----------|------------|
| API calls | Vite proxy → Express → ServiceNow | Direct (same origin) |
| Auth | Express adds Basic Auth from `.env` | Session cookie + `X-userToken` CSRF |
| Router | HashRouter or BrowserRouter | HashRouter (required) |

## Quick Start: New Project

### 1. Scaffold and install

```bash
npm create vite@latest my-sn-app -- --template react-ts
cd my-sn-app && npm install
npm install -D vite-plugin-singlefile
```

### 2. Configure Vite

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { viteSingleFile } from 'vite-plugin-singlefile';

export default defineConfig({
  plugins: [react(), viteSingleFile()],
  build: { assetsInlineLimit: 10000000 },
  server: { port: 3000, proxy: { '/api': 'http://localhost:3001' } },
});
```

### 3. Use HashRouter + ParentHashSync

ServiceNow's REST endpoint URL conflicts with BrowserRouter. HashRouter is required.

When the SPA is loaded inside ServiceNow's classic navigation frame (`/now/nav/ui/classic/params/target/...`), it runs in an iframe. Hash changes are invisible in the browser URL bar. Add `ParentHashSync` to mirror the hash to the parent frame URL via `history.replaceState()`.

```typescript
import { HashRouter, useLocation } from 'react-router-dom';

// See references/authentication-patterns.md for full ParentHashSync implementation
<HashRouter>
  <ParentHashSync />
  <App />
</HashRouter>
```

### 4. Set up dual-mode API client

Create `src/api/config.ts` and `src/api/client.ts` — see [references/authentication-patterns.md](references/authentication-patterns.md) for complete patterns.

### 5. Add SnAuthGate

Wraps the app, fetches session token on ServiceNow, blocks guests. See [references/authentication-patterns.md](references/authentication-patterns.md).

### 6. Create ServiceNow artifacts

Three required artifacts: system property (HTML storage), REST API definition, `GET /app` and `GET /get_token` endpoints. See [references/servicenow-artifacts.md](references/servicenow-artifacts.md).

### 7. Deploy

```bash
npm run build          # Produces single dist/index.html
node scripts/deploy-to-sn.js  # PATCHes HTML into system property
```

Deploy script template: [references/vite-config-reference.md](references/vite-config-reference.md)

App URL: `https://<instance>.service-now.com/api/<namespace>/<api_id>/app`

## Converting an Existing App

Copy this checklist and track progress:

```
Conversion Progress:
- [ ] Replace CRA/webpack with Vite + vite-plugin-singlefile
- [ ] Move public/index.html to root, add <script type="module" src="/src/main.tsx">
- [ ] Update tsconfig.json: "moduleResolution": "bundler"
- [ ] Replace BrowserRouter with HashRouter
- [ ] Create src/api/config.ts with isServiceNow() detection
- [ ] Create src/api/client.ts with dual-mode fetch (credentials: 'same-origin', X-userToken)
- [ ] Replace all hardcoded API URLs with centralized client
- [ ] Add SnAuthGate to entry point (guest detection + login redirect)
- [ ] Create ServiceNow artifacts (property, REST API, endpoints)
- [ ] Set requires_authentication=true on all data endpoints
- [ ] Create deploy script
- [ ] Verify: npm run build produces single dist/index.html
```

## Bundle Size

System properties support ~4-8 MB. Typical sizes: simple apps 200-500 KB, medium 0.5-1.5 MB, complex 1.5-3 MB. If too large, use `sys_attachment` storage or code splitting.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API returns 401 | Add `credentials: 'same-origin'` to fetch; ensure `X-userToken` header is sent |
| Dashboard shows zeros | Detect `user_name === 'guest'` in SnAuthGate, show login prompt |
| Routes don't work on ServiceNow | Switch to HashRouter |
| URL doesn't change in ServiceNow nav frame | Add `ParentHashSync` component (see auth patterns reference) |
| Shared URL duplicates encoded hash | Strip `%23` from parent pathname before appending fresh hash |
| Build produces multiple files | Add `viteSingleFile()` to Vite plugins |
| CSS broken on ServiceNow | `<StyleSheetManager disableCSSOMInjection={isServiceNow()}>` (styled-components) |

## Reference Documents

| Topic | Reference |
|-------|-----------|
| Vite config, deploy script, package.json templates | [references/vite-config-reference.md](references/vite-config-reference.md) |
| ServiceNow artifacts (property, REST API, endpoints) | [references/servicenow-artifacts.md](references/servicenow-artifacts.md) |
| Auth patterns (SnAuthGate, API client, Express proxy) | [references/authentication-patterns.md](references/authentication-patterns.md) |

# Authentication Patterns Reference

Code patterns for dual-mode authentication (local dev + ServiceNow production).

## Contents
- Environment detection: config.ts
- API client: client.ts (dual-mode fetch wrapper)
- SnAuthGate component (main.tsx entry point)
- Authentication flow diagrams
- Styled-components note (CSSOM fix)
- Express backend template (local dev proxy)
- Security checklist

## Environment Detection: config.ts

```typescript
/**
 * API configuration for dual-mode operation:
 * - Development: calls Express backend at localhost:3001 (proxied via Vite)
 * - ServiceNow: calls ServiceNow REST APIs via relative URLs
 */

export const isServiceNow = (): boolean => {
  return window.location.hostname.includes('.service-now.com');
};

let snToken: string | null = null;
let snUserName: string | null = null;

export const getSnToken = () => snToken;
export const setSnToken = (token: string) => {
  snToken = token;
};

export const getSnUserName = () => snUserName;
export const setSnUserName = (name: string) => {
  snUserName = name;
};

/**
 * Returns the base URL for API calls.
 * - In dev mode with Vite proxy: empty string (relative URLs go through proxy)
 * - In ServiceNow: empty string (relative URLs hit same origin)
 */
export const getApiBaseUrl = (): string => {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  return '';
};
```

## API Client: client.ts

The centralized fetch wrapper handles both modes automatically.

```typescript
import { isServiceNow, getSnToken, getApiBaseUrl } from './config';

/**
 * Build request headers.
 * - In ServiceNow mode: adds X-userToken CSRF header
 * - In dev mode: no special headers (Express backend handles auth)
 */
function getHeaders(extra: Record<string, string> = {}): Record<string, string> {
  const headers: Record<string, string> = {
    Accept: 'application/json',
    ...extra,
  };

  if (isServiceNow()) {
    const token = getSnToken();
    if (token) {
      headers['X-userToken'] = token;
    }
  }

  return headers;
}

/**
 * Resolve API path for ServiceNow mode.
 *
 * In local dev, the Express backend uses paths like /api/dashboard/stats.
 * In ServiceNow, these map to /api/<namespace>/<api_id>/dashboard/stats.
 *
 * Customize this function for your specific API namespace and endpoint mapping.
 */
function resolveSnPath(path: string): string {
  if (!isServiceNow()) return path;

  // Example mapping — customize for your project:
  const SN_API_BASE = '/api/your_namespace/your_api_id';

  const mappings: Record<string, string> = {
    '/api/dashboard/stats': `${SN_API_BASE}/dashboard/stats`,
    '/api/dashboard/items': `${SN_API_BASE}/dashboard/items`,
    '/api/dashboard/categories': `${SN_API_BASE}/dashboard/categories`,
    '/api/dashboard/catalogs': `${SN_API_BASE}/dashboard/catalogs`,
    '/api/catalog/hierarchy': `${SN_API_BASE}/full-hierarchy`,
    // Add more mappings as needed
  };

  // Check static mappings first
  if (mappings[path]) return mappings[path];

  // Dynamic path patterns (e.g., /api/items/abc123)
  // Customize these regex patterns for your routes
  const dynamicPatterns = [
    { pattern: /^\/api\/items\/(.+)\/variables$/, replacement: `${SN_API_BASE}/items/$1/variables` },
    { pattern: /^\/api\/items\/(.+)$/, replacement: `${SN_API_BASE}/items/$1` },
  ];

  for (const { pattern, replacement } of dynamicPatterns) {
    const match = path.match(pattern);
    if (match) {
      return path.replace(pattern, replacement);
    }
  }

  // Fallback: prepend SN base
  return `${SN_API_BASE}${path.replace('/api', '')}`;
}

/**
 * Parse ServiceNow response format.
 * ServiceNow wraps responses in { result: ... }, Express returns data directly.
 */
function parseResponse(data: any): any {
  if (isServiceNow() && data && typeof data === 'object' && 'result' in data) {
    return data.result;
  }
  return data;
}

/**
 * GET request with dual-mode support.
 */
export async function apiGet(path: string): Promise<any> {
  const url = `${getApiBaseUrl()}${resolveSnPath(path)}`;
  const response = await fetch(url, {
    method: 'GET',
    headers: getHeaders(),
    credentials: 'same-origin', // Required for ServiceNow session cookies
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  const data = await response.json();
  return parseResponse(data);
}

/**
 * POST request with dual-mode support.
 */
export async function apiPost(path: string, body: any): Promise<any> {
  const url = `${getApiBaseUrl()}${resolveSnPath(path)}`;
  const response = await fetch(url, {
    method: 'POST',
    headers: getHeaders({ 'Content-Type': 'application/json' }),
    credentials: 'same-origin',
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  const data = await response.json();
  return parseResponse(data);
}

/**
 * PATCH request with dual-mode support.
 */
export async function apiPatch(path: string, body: any): Promise<any> {
  const url = `${getApiBaseUrl()}${resolveSnPath(path)}`;
  const response = await fetch(url, {
    method: 'PATCH',
    headers: getHeaders({ 'Content-Type': 'application/json' }),
    credentials: 'same-origin',
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  const data = await response.json();
  return parseResponse(data);
}

/**
 * DELETE request with dual-mode support.
 */
export async function apiDelete(path: string): Promise<any> {
  const url = `${getApiBaseUrl()}${resolveSnPath(path)}`;
  const response = await fetch(url, {
    method: 'DELETE',
    headers: getHeaders(),
    credentials: 'same-origin',
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  const data = await response.json();
  return parseResponse(data);
}
```

## ParentHashSync: URL Sync for ServiceNow Nav Frame (main.tsx)

When the SPA is loaded inside ServiceNow's classic navigation frame (`/now/nav/ui/classic/params/target/...`), it runs in an iframe. HashRouter changes are invisible in the browser URL bar because ServiceNow controls the outer URL. `ParentHashSync` solves this by mirroring the SPA's hash to the parent frame via `history.replaceState()`.

**Why `replaceState` instead of `window.top.location.hash`:** Setting `location.hash` triggers `hashchange` events that ServiceNow may listen for. `replaceState` updates the URL silently with no events.

**`%23` stripping:** When a user copies a URL with a hash and pastes it, ServiceNow re-encodes `#` as `%23` into the path. The component strips any `%23...` suffix from the parent pathname before appending the fresh hash, preventing URL duplication.

```tsx
import { useLocation } from 'react-router-dom';

// Sync SPA hash to parent frame URL when running inside ServiceNow nav frame (iframe)
function ParentHashSync() {
  const location = useLocation();

  useEffect(() => {
    if (window.self === window.top) return; // Not in iframe — nothing to sync
    try {
      const hash = '#' + location.pathname + location.search;
      // Strip any encoded hash (%23...) that ServiceNow adds when re-processing a shared URL
      let parentPath = window.top!.location.pathname;
      const encodedHashIdx = parentPath.indexOf('%23');
      if (encodedHashIdx !== -1) {
        parentPath = parentPath.substring(0, encodedHashIdx);
      }
      window.top!.history.replaceState(null, '',
        parentPath + window.top!.location.search + hash
      );
    } catch { /* cross-origin iframe — ignore */ }
  }, [location.pathname, location.search]);

  return null;
}

// On initial load: if parent frame has a hash (from shared URL), apply it to iframe
// This runs BEFORE React renders, so HashRouter picks up the correct initial route
if (window.self !== window.top) {
  try {
    const parentHash = window.top!.location.hash;
    if (parentHash && parentHash !== '#/' && parentHash !== '#') {
      window.location.hash = parentHash;
    }
  } catch { /* cross-origin */ }
}
```

Place `<ParentHashSync />` inside `<HashRouter>` (it needs router context for `useLocation`). The initial hash read runs at module level, before React mounts.

## Authentication Gate: SnAuthGate (main.tsx)

The `SnAuthGate` component wraps the entire app and handles ServiceNow authentication before rendering.

```tsx
import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';
import { HashRouter, useLocation } from 'react-router-dom';
import App from './App';
import { isServiceNow, setSnToken, setSnUserName } from './api/config';

function SnAuthGate({ children }: { children: React.ReactNode }) {
  const [ready, setReady] = useState(!isServiceNow());
  const [authorized, setAuthorized] = useState<boolean | null>(isServiceNow() ? null : true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Skip auth gate in local development
    if (!isServiceNow()) return;

    fetch('/api/your_namespace/your_api_id/get_token', {
      credentials: 'same-origin',
      headers: { Accept: 'application/json' },
    })
      .then((res) => {
        if (!res.ok) throw new Error(`Token fetch failed: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        const result = data.result || data;
        const token = result.sessionToken || result.token;
        const userName = result.user_name || '';

        if (!token || userName === 'guest' || !userName) {
          // User is not logged in — show login prompt
          setAuthorized(false);
        } else {
          // User is authenticated — store token and proceed
          setSnToken(token);
          setSnUserName(userName);
          setAuthorized(true);
        }
        setReady(true);
      })
      .catch((err) => {
        console.error('ServiceNow auth failed:', err);
        setError(err.message);
        setAuthorized(false);
        setReady(true);
      });
  }, []);

  // Loading state while fetching token
  if (!ready) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        fontFamily: 'system-ui',
      }}>
        <p>Connecting to ServiceNow...</p>
      </div>
    );
  }

  // Unauthorized — show login prompt
  if (authorized === false) {
    const loginUrl = `/login.do?sysparm_goto_url=${encodeURIComponent(
      window.location.pathname + window.location.hash
    )}`;
    return (
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        gap: '1rem',
        fontFamily: 'system-ui',
        color: '#1e293b',
      }}>
        <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>&#128274;</div>
        <h1 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 600 }}>
          Authentication Required
        </h1>
        <p style={{
          color: '#64748b',
          textAlign: 'center',
          maxWidth: '400px',
          margin: 0,
          lineHeight: 1.5,
        }}>
          {error
            ? `Unable to authenticate: ${error}`
            : 'Please log in to ServiceNow to access this application.'}
        </p>
        <a
          href={loginUrl}
          style={{
            marginTop: '0.5rem',
            padding: '0.625rem 1.5rem',
            background: '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '0.925rem',
            textDecoration: 'none',
            fontWeight: 500,
          }}
        >
          Log in to ServiceNow
        </a>
      </div>
    );
  }

  // Authenticated — render the app
  return <>{children}</>;
}

// App entry point
// ParentHashSync must be inside HashRouter (needs useLocation).
// SnAuthGate wraps HashRouter so auth resolves before any routing.
const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <SnAuthGate>
      <HashRouter>
        <ParentHashSync />
        <App />
      </HashRouter>
    </SnAuthGate>
  </React.StrictMode>
);
```

## Authentication Flow Diagrams

### ServiceNow Mode (Production)

```
User visits https://<instance>/api/<namespace>/<api_id>/app
  ↓
Browser loads HTML from system property
  ↓
SnAuthGate component mounts
  ↓
Fetches GET /get_token (public endpoint)
  ↓
Checks response:
  ├─ user_name === "guest" or empty → Show "Authentication Required" + login button
  └─ user_name is valid → Store token, render app
      ↓
All subsequent API calls include:
  ├─ Session cookie (automatic, via credentials: 'same-origin')
  └─ X-userToken header (CSRF protection, set manually)
```

### Local Development Mode

```
User visits http://localhost:3000
  ↓
Vite dev server serves the app
  ↓
isServiceNow() returns false
  ↓
SnAuthGate skips token fetch, renders app immediately
  ↓
All API calls go through Vite proxy:
  localhost:3000/api/* → localhost:3001/api/*
  ↓
Express backend adds Basic Auth headers
  ↓
Express forwards to ServiceNow REST API
```

### Login Redirect Flow

When a user is not authenticated on ServiceNow:

```
1. SnAuthGate detects guest user
2. Shows "Authentication Required" placeholder
3. Login button links to:
   /login.do?sysparm_goto_url=/api/<namespace>/<api_id>/app
4. User logs in via ServiceNow login page
5. ServiceNow redirects back to the SPA URL
6. SPA reloads, SnAuthGate fetches token successfully
7. App renders with authenticated user data
```

## Styled Components Note

If using `styled-components`, ServiceNow may block CSSOM injection. Wrap your app with:

```tsx
import { StyleSheetManager } from 'styled-components';

<StyleSheetManager disableCSSOMInjection={isServiceNow()}>
  <App />
</StyleSheetManager>
```

This forces styled-components to inject `<style>` tags into the DOM instead of using the CSSOM API, which ServiceNow's Content Security Policy may restrict.

## Express Backend Template (Local Development)

A minimal Express backend for local development that proxies to ServiceNow:

```typescript
import express from 'express';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());

const SN_INSTANCE = process.env.SERVICENOW_INSTANCE_URL;
const SN_USER = process.env.SERVICENOW_USER;
const SN_PASSWORD = process.env.SERVICENOW_PASSWORD;
const SN_AUTH = Buffer.from(`${SN_USER}:${SN_PASSWORD}`).toString('base64');

// Proxy helper
async function snFetch(path: string, options: RequestInit = {}) {
  const url = `${SN_INSTANCE}/api/your_namespace/your_api_id${path}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      Authorization: `Basic ${SN_AUTH}`,
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  return response.json();
}

// Example: dashboard stats
app.get('/api/dashboard/stats', async (req, res) => {
  try {
    const data = await snFetch('/dashboard/stats');
    res.json(data.result || data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Add more proxy routes as needed...

app.listen(3001, () => {
  console.log('Express backend running on port 3001');
});
```

## Security Checklist

- [ ] All data endpoints have `requires_authentication=true`
- [ ] Only `/app`, `/get_token`, and `/health` are public
- [ ] `credentials: 'same-origin'` is set on all fetch calls
- [ ] `X-userToken` header is sent on all ServiceNow API calls
- [ ] Guest users see "Authentication Required" placeholder, not the dashboard
- [ ] `.env` file with credentials is in `.gitignore`
- [ ] No hardcoded passwords in frontend code
- [ ] Login redirect URL uses `encodeURIComponent` to prevent injection

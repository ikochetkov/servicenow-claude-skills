---
name: develop-remote-mcp
description: Build and deploy remote MCP servers with OAuth authentication, StreamableHTTP transport, and Railway hosting. Covers MCP SDK architecture, single dispatcher pattern, dual transport (stdio/HTTP), OAuth bridge pattern (OAuthServerProvider, requireBearerAuth, mcpAuthRouter), persistent token storage, Dockerfile best practices, and Claude Desktop connector setup. Triggers on remote MCP server, MCP OAuth, StreamableHTTP, Railway MCP, deploy MCP, MCP authentication, OAuth bridge, Claude Desktop MCP, MCP server hosting.
---

# Developing Remote MCP Servers

Build MCP servers that run as hosted web services (not just local stdio). This skill covers the full stack: MCP SDK, OAuth authentication, HTTP transport, Railway deployment, and Claude Desktop integration.

## Architecture Overview

```
┌─────────────────┐     HTTPS + Bearer      ┌──────────────────────────┐
│  Claude Desktop  │ ◄──────────────────────► │  Remote MCP Server       │
│  or claude.ai    │     (StreamableHTTP)     │  (Railway / any host)    │
└─────────────────┘                          ├──────────────────────────┤
                                             │  Express app             │
                                             │  ├─ mcpAuthRouter        │
                                             │  ├─ /oauth/callback      │
                                             │  ├─ /mcp (Bearer + SSE)  │
                                             │  └─ /health              │
                                             ├──────────────────────────┤
                                             │  MCP Server              │
                                             │  └─ Tool handlers        │
                                             ├──────────────────────────┤
                                             │  OAuth Provider          │
                                             │  └─ Token Store (disk)   │
                                             └──────────┬───────────────┘
                                                        │ OAuth tokens
                                                        ▼
                                             ┌──────────────────────────┐
                                             │  Upstream API            │
                                             │  (ServiceNow, etc.)      │
                                             └──────────────────────────┘
```

## Core Concepts

### 1. MCP SDK Components

| Component | Import | Purpose |
|-----------|--------|---------|
| `Server` | `@modelcontextprotocol/sdk/server/index.js` | Core MCP server — registers tool handlers |
| `StdioServerTransport` | `@modelcontextprotocol/sdk/server/stdio.js` | Local transport (Claude Code plugin) |
| `StreamableHTTPServerTransport` | `@modelcontextprotocol/sdk/server/streamableHttp.js` | HTTP transport (remote hosting) |
| `mcpAuthRouter` | `@modelcontextprotocol/sdk/server/auth/router.js` | Express router for OAuth endpoints |
| `requireBearerAuth` | `@modelcontextprotocol/sdk/server/auth/middleware/bearerAuth.js` | Bearer token validation middleware |
| `OAuthServerProvider` | `@modelcontextprotocol/sdk/server/auth/provider.js` | Interface for custom OAuth providers |

### 2. Single Dispatcher Pattern

Expose ONE tool that routes to many handlers internally. Saves 5K-10K tokens per turn vs exposing dozens of individual tools.

```typescript
// Instead of 38 tools in ListTools:
const dispatcherDefinition = {
  name: "servicenow",
  description: "ServiceNow operations. Use action parameter to select operation.",
  inputSchema: {
    type: "object",
    properties: {
      action: { type: "string", enum: ["sn_query", "sn_create", ...] },
      // ... action-specific params
    },
    required: ["action"],
  },
};

// Route in CallTool:
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { arguments: args } = request.params;
  return await dispatcherExecute(args ?? {}, client);
});
```

### 3. Dual Transport

Support both local (stdio) and remote (HTTP) from the same codebase:

```typescript
async function main() {
  if (process.env.TRANSPORT === "http") {
    const { startHttpServer } = await import("./http-server.js");
    await startHttpServer();
  } else {
    // Default: stdio for local Claude Code plugin
    const transport = new StdioServerTransport();
    await server.connect(transport);
  }
}
```

**Environment variable**: `TRANSPORT=http` switches to HTTP mode. Default is stdio.

### 4. OAuth Bridge Pattern

When your MCP server wraps an API that uses its own OAuth (ServiceNow, Atlassian, Google, etc.), you need a **bridge** — MCP OAuth on the outside, upstream OAuth on the inside.

**Flow:**

```
Claude Desktop                    MCP Server                     Upstream API
     │                               │                               │
     │─── MCP auth request ─────────►│                               │
     │                               │─── redirect to upstream ─────►│
     │                               │                               │
     │                               │◄── upstream callback + code ──│
     │                               │─── exchange for upstream tokens│
     │                               │                               │
     │◄── MCP auth code ────────────│                               │
     │─── exchange for MCP tokens ──►│                               │
     │◄── MCP access + refresh ─────│                               │
     │                               │                               │
     │─── tool call + Bearer ───────►│                               │
     │                               │─── extract upstream token ───►│
     │                               │◄── API response ─────────────│
     │◄── tool result ──────────────│                               │
```

**Key implementation points:**

1. **`OAuthServerProvider` interface** — implement all methods:
   - `authorize()` — redirect user to upstream OAuth
   - `challengeForAuthorizationCode()` — return PKCE challenge for auth code
   - `exchangeAuthorizationCode()` — exchange MCP code → MCP tokens (backed by upstream tokens)
   - `exchangeRefreshToken()` — refresh upstream token, issue new MCP tokens
   - `verifyAccessToken()` — validate MCP token, return AuthInfo with upstream token in `extra`

2. **Permissive client store** — auto-register unknown OAuth clients:
   ```typescript
   class PermissiveClientsStore implements OAuthRegisteredClientsStore {
     async getClient(clientId: string) {
       let client = tokenStore.getClient(clientId);
       if (!client) {
         client = {
           client_id: clientId,
           client_id_issued_at: Math.floor(Date.now() / 1000),
           redirect_uris: [
             "https://claude.ai/api/mcp/auth_callback",
             "http://localhost:3119/oauth/callback",
           ],
           grant_types: ["authorization_code", "refresh_token"],
           response_types: ["code"],
           token_endpoint_auth_method: "none",
           scope: "useraccount",
         };
         tokenStore.storeClient(clientId, client);
       }
       return client;
     }
   }
   ```

3. **Pending auth state** — in-memory Map with TTL cleanup:
   ```typescript
   const pendingAuth = new Map<string, PendingAuth>();
   // Cleanup stale entries every 5 minutes
   setInterval(() => {
     const now = Date.now();
     for (const [state, pa] of pendingAuth) {
       if (now - pa.createdAt > 10 * 60 * 1000) pendingAuth.delete(state);
     }
   }, 5 * 60 * 1000);
   ```

4. **OAuth callback handler** — Express route that:
   - Receives upstream auth code
   - Exchanges it for upstream tokens
   - Generates MCP auth code backed by upstream tokens
   - Redirects to Claude Desktop with MCP auth code

### 5. HTTP Server Setup

```typescript
export async function startHttpServer(): Promise<void> {
  const app = express();
  app.set("trust proxy", 1);  // REQUIRED for Railway reverse proxy

  const provider = new YourOAuthProvider();

  // 1. Mount OAuth routes (/.well-known/oauth-*, /authorize, /token, /register)
  app.use(mcpAuthRouter({
    provider,
    issuerUrl: new URL(SERVER_URL),
    scopesSupported: ["useraccount"],
    clientRegistrationOptions: {
      clientSecretExpirySeconds: 0,
    },
  }));

  // 2. Upstream OAuth callback
  app.get("/oauth/callback", async (req, res) => {
    await handleOAuthCallback(req, res);
  });

  // 3. Bearer auth middleware — MUST be added manually to /mcp
  const bearerAuth = requireBearerAuth({ verifier: provider });

  // 4. StreamableHTTP transport
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: () => crypto.randomUUID(),
  });

  // 5. MCP server + connect
  const mcpServer = new Server(
    { name: "my-mcp-server", version: "1.0.0" },
    { capabilities: { tools: {} } },
  );
  // ... register handlers ...
  await mcpServer.connect(transport);

  // 6. Mount /mcp with bearer auth
  app.all("/mcp", bearerAuth, async (req, res) => {
    await transport.handleRequest(req, res, req.body);
  });

  // 7. Health check (no auth)
  app.get("/health", (_req, res) => res.json({ status: "ok" }));

  app.listen(PORT, "0.0.0.0");
}
```

### 6. Token Store (Persistent)

Tokens must survive container restarts. Use a JSON file on a mounted volume:

```typescript
const TOKEN_PATH = join(process.env.DATA_DIR || "/data", "tokens.json");

interface PersistedData {
  authCodes: Record<string, StoredAuthCode>;
  accessTokens: Record<string, StoredAccessToken>;
  refreshTokens: Record<string, StoredRefreshToken>;
  clients: Record<string, any>;
}

// Load on startup
export function loadTokens(): void {
  if (existsSync(TOKEN_PATH)) {
    data = JSON.parse(readFileSync(TOKEN_PATH, "utf-8"));
  }
}

// Persist after every write operation
export function persistTokens(): void {
  ensureDir();
  writeFileSync(TOKEN_PATH, JSON.stringify(data, null, 2), { mode: 0o600 });
}
```

**Token types:**
- **Auth code** — short-lived (10 min), bridges upstream auth code with MCP params + PKCE
- **Access token** — long-lived (30 days), MCP token backed by upstream access token
- **Refresh token** — indefinite, MCP refresh token backed by upstream refresh token

Always check expiry on read and delete expired tokens automatically.

### 7. Railway Deployment

See `references/railway-checklist.md` for the full checklist.

**Dockerfile:**
```dockerfile
FROM node:20-slim
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --production=false

COPY src ./src
COPY tsconfig.json ./
RUN npx tsc

ENV TRANSPORT=http
ENV PORT=8000
EXPOSE 8000

# Token store directory — mount Railway volume at /data
RUN mkdir -p /data

CMD ["node", "dist/index.js"]
```

**railway.json:**
```json
{
  "$schema": "https://railway.com/railway.schema.json",
  "build": { "builder": "DOCKERFILE", "dockerfilePath": "Dockerfile" },
  "deploy": { "restartPolicyType": "ON_FAILURE", "restartPolicyMaxRetries": 3 }
}
```

**Required env vars on Railway:**
- `TRANSPORT=http`
- `SERVER_URL=https://your-app.up.railway.app` (your Railway public URL)
- `PORT=8000`
- Upstream API credentials (OAuth client ID/secret, instance URL, etc.)

### 8. Claude Desktop Connector

To connect Claude Desktop to your remote MCP server:

1. In Claude Desktop settings, add a remote MCP server
2. Enter the URL: `https://your-app.up.railway.app/mcp`
3. Claude Desktop will:
   - Discover OAuth metadata at `/.well-known/oauth-authorization-server`
   - Register as a client at `/register`
   - Redirect you to authenticate with the upstream provider
   - Store the MCP tokens for future use

## Common Gotchas

### `VOLUME` is banned in Railway Dockerfiles
Railway does not allow `VOLUME` instructions. Use `RUN mkdir -p /data` and mount a Railway volume at `/data` via the dashboard instead.

### `trust proxy` required behind Railway reverse proxy
Without `app.set("trust proxy", 1)`, `express-rate-limit` and other IP-dependent middleware will see `127.0.0.1` for all requests.

### `requireBearerAuth` must be added manually to `/mcp`
`mcpAuthRouter` handles `/.well-known/*`, `/authorize`, `/token`, `/register` — but it does NOT protect your `/mcp` endpoint. You must add `requireBearerAuth()` middleware to `/mcp` yourself.

### `StreamableHTTPServerTransport` handles all session management
Do NOT implement your own session handling. Call `transport.handleRequest(req, res, req.body)` for ALL HTTP methods (GET, POST, DELETE) on `/mcp` — the transport manages sessions, SSE connections, and request routing internally.

### `getAuthConfig()` throws on missing env vars
If you have a helper that reads Basic Auth env vars (for stdio mode), guard it with a transport check. In HTTP mode, auth comes from OAuth tokens, not env vars:
```typescript
if (process.env.TRANSPORT !== "http") {
  const auth = getAuthConfig(); // Reads SN_USERNAME, SN_PASSWORD
  client = new ServiceNowClient(auth.instanceUrl, auth.username, auth.password);
}
```

### `.skill` files are zip archives
When packaging skills for distribution, `.skill` files are just renamed `.zip` archives containing `SKILL.md` and an optional `references/` directory.

## Package Dependencies

```json
{
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.12.1",
    "express": "^4.21.2"
  },
  "devDependencies": {
    "@types/express": "^5.0.2",
    "typescript": "^5.8.3"
  }
}
```

## Project Structure

```
your-mcp-server/
├── src/
│   ├── index.ts            # Entry point — dual transport switch
│   ├── http-server.ts      # Express + OAuth + StreamableHTTP
│   ├── oauth-provider.ts   # OAuthServerProvider bridge implementation
│   ├── token-store.ts      # Persistent token storage (JSON file)
│   ├── auth.ts             # Basic Auth config (stdio mode)
│   ├── client.ts           # Upstream API client
│   ├── dispatcher.ts       # Single tool → many handlers routing
│   └── tools/              # Individual tool handlers
├── Dockerfile
├── railway.json
├── tsconfig.json
└── package.json
```

## Quick Start

1. **Scaffold**: `npm init -y && npm install @modelcontextprotocol/sdk express && npm install -D typescript @types/express`
2. **Implement**: Create `src/index.ts` with dual transport, `src/http-server.ts` with Express + OAuth
3. **Test locally**: `TRANSPORT=http SERVER_URL=http://localhost:8000 node dist/index.js`
4. **Deploy**: Push to Railway, set env vars, mount volume at `/data`
5. **Connect**: Add `https://your-app.up.railway.app/mcp` in Claude Desktop

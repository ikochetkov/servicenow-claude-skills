# OAuth Bridge Provider — Full Pattern

This is a complete, production-tested implementation of the MCP OAuth bridge pattern. It bridges MCP OAuth (what Claude Desktop speaks) with an upstream OAuth provider (ServiceNow in this example, but the pattern applies to any OAuth2 provider).

## oauth-provider.ts

```typescript
import { Response } from "express";
import type {
  OAuthServerProvider,
  AuthorizationParams,
} from "@modelcontextprotocol/sdk/server/auth/provider.js";
import type {
  OAuthClientInformationFull,
  OAuthTokens,
  OAuthTokenRevocationRequest,
} from "@modelcontextprotocol/sdk/shared/auth.js";
import type {
  OAuthRegisteredClientsStore,
} from "@modelcontextprotocol/sdk/server/auth/clients.js";
import type { AuthInfo } from "@modelcontextprotocol/sdk/server/auth/types.js";
import * as crypto from "crypto";
import * as tokenStore from "./token-store.js";

// ---------------------------------------------------------------------------
// Configuration (from environment)
// ---------------------------------------------------------------------------

const UPSTREAM_URL = process.env.UPSTREAM_URL || "";
const UPSTREAM_CLIENT_ID = process.env.UPSTREAM_OAUTH_CLIENT_ID || "";
const UPSTREAM_CLIENT_SECRET = process.env.UPSTREAM_OAUTH_CLIENT_SECRET || "";
const SERVER_URL = process.env.SERVER_URL || "http://localhost:8000";

function upstreamAuthorizeUrl(): string {
  return `${UPSTREAM_URL}/oauth_auth.do`; // Adjust for your provider
}
function upstreamTokenUrl(): string {
  return `${UPSTREAM_URL}/oauth_token.do`; // Adjust for your provider
}

// ---------------------------------------------------------------------------
// Permissive client store — auto-registers Claude Desktop and claude.ai
// ---------------------------------------------------------------------------

class PermissiveClientsStore implements OAuthRegisteredClientsStore {
  async getClient(clientId: string): Promise<OAuthClientInformationFull | undefined> {
    let client = tokenStore.getClient(clientId);
    if (!client) {
      client = {
        client_id: clientId,
        client_id_issued_at: Math.floor(Date.now() / 1000),
        redirect_uris: [
          "https://claude.ai/api/mcp/auth_callback",  // claude.ai
          "http://localhost:3119/oauth/callback",       // Claude Desktop
        ],
        grant_types: ["authorization_code", "refresh_token"],
        response_types: ["code"],
        token_endpoint_auth_method: "none",
        scope: "useraccount",
      };
      tokenStore.storeClient(clientId, client);
      console.log(`[OAuth] Auto-registered client: ${clientId}`);
    }
    return client as OAuthClientInformationFull;
  }

  async registerClient(client: OAuthClientInformationFull): Promise<OAuthClientInformationFull> {
    tokenStore.storeClient(client.client_id, client);
    return client;
  }
}

// ---------------------------------------------------------------------------
// Pending auth state (in-memory, short-lived)
// ---------------------------------------------------------------------------

interface PendingAuth {
  mcpParams: AuthorizationParams;
  client: OAuthClientInformationFull;
  createdAt: number;
}

const pendingAuth = new Map<string, PendingAuth>();

// Cleanup every 5 minutes — delete entries older than 10 minutes
setInterval(() => {
  const now = Date.now();
  for (const [state, pa] of pendingAuth) {
    if (now - pa.createdAt > 10 * 60 * 1000) pendingAuth.delete(state);
  }
}, 5 * 60 * 1000);

// ---------------------------------------------------------------------------
// OAuth Provider Implementation
// ---------------------------------------------------------------------------

export class MyOAuthProvider implements OAuthServerProvider {
  private _clientsStore = new PermissiveClientsStore();

  constructor() {
    tokenStore.loadTokens();
  }

  get clientsStore(): OAuthRegisteredClientsStore {
    return this._clientsStore;
  }

  // Step 1: Redirect to upstream OAuth
  async authorize(
    client: OAuthClientInformationFull,
    params: AuthorizationParams,
    res: Response,
  ): Promise<void> {
    const state = crypto.randomBytes(32).toString("base64url");

    pendingAuth.set(state, {
      mcpParams: params,
      client,
      createdAt: Date.now(),
    });

    const upstreamParams = new URLSearchParams({
      response_type: "code",
      client_id: UPSTREAM_CLIENT_ID,
      redirect_uri: `${SERVER_URL}/oauth/callback`,
      state,
    });

    res.redirect(`${upstreamAuthorizeUrl()}?${upstreamParams.toString()}`);
  }

  // Return PKCE challenge for auth code
  async challengeForAuthorizationCode(
    _client: OAuthClientInformationFull,
    authorizationCode: string,
  ): Promise<string> {
    const ac = tokenStore.getAuthCode(authorizationCode);
    if (!ac) throw new Error("Authorization code not found or expired");
    return ac.codeChallenge;
  }

  // Step 3: Exchange MCP auth code → MCP tokens (backed by upstream tokens)
  async exchangeAuthorizationCode(
    client: OAuthClientInformationFull,
    authorizationCode: string,
  ): Promise<OAuthTokens> {
    const ac = tokenStore.getAuthCode(authorizationCode);
    if (!ac) throw new Error("Authorization code not found or expired");
    tokenStore.removeAuthCode(authorizationCode);

    const mcpAccess = crypto.randomBytes(32).toString("base64url");
    const mcpRefresh = crypto.randomBytes(32).toString("base64url");
    const expiresIn = 30 * 24 * 3600; // 30 days

    tokenStore.storeAccessToken({
      token: mcpAccess,
      clientId: client.client_id,
      scopes: ac.scopes,
      expiresAt: Math.floor(Date.now() / 1000) + expiresIn,
      upstreamTokens: ac.upstreamTokens,
    });

    tokenStore.storeRefreshToken({
      token: mcpRefresh,
      clientId: client.client_id,
      scopes: ac.scopes,
      upstreamRefreshToken: ac.upstreamTokens.refreshToken,
    });

    return {
      access_token: mcpAccess,
      token_type: "bearer",
      expires_in: expiresIn,
      refresh_token: mcpRefresh,
    };
  }

  // Refresh: rotate upstream token → issue new MCP tokens
  async exchangeRefreshToken(
    client: OAuthClientInformationFull,
    refreshToken: string,
  ): Promise<OAuthTokens> {
    const rt = tokenStore.getRefreshToken(refreshToken);
    if (!rt) throw new Error("Refresh token not found");

    // Refresh the upstream token
    const body = new URLSearchParams({
      grant_type: "refresh_token",
      client_id: UPSTREAM_CLIENT_ID,
      client_secret: UPSTREAM_CLIENT_SECRET,
      refresh_token: rt.upstreamRefreshToken,
    });

    const resp = await fetch(upstreamTokenUrl(), {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: body.toString(),
    });

    if (!resp.ok) throw new Error("Upstream token refresh failed");
    const data = await resp.json();

    tokenStore.removeRefreshToken(refreshToken);

    const newAccess = crypto.randomBytes(32).toString("base64url");
    const newRefresh = crypto.randomBytes(32).toString("base64url");
    const expiresIn = 30 * 24 * 3600;

    tokenStore.storeAccessToken({
      token: newAccess,
      clientId: client.client_id,
      scopes: rt.scopes,
      expiresAt: Math.floor(Date.now() / 1000) + expiresIn,
      upstreamTokens: {
        accessToken: data.access_token,
        refreshToken: data.refresh_token || rt.upstreamRefreshToken,
        expiresIn: data.expires_in,
      },
    });

    tokenStore.storeRefreshToken({
      token: newRefresh,
      clientId: client.client_id,
      scopes: rt.scopes,
      upstreamRefreshToken: data.refresh_token || rt.upstreamRefreshToken,
    });

    return {
      access_token: newAccess,
      token_type: "bearer",
      expires_in: expiresIn,
      refresh_token: newRefresh,
    };
  }

  // Verify MCP token → return AuthInfo with upstream token
  async verifyAccessToken(token: string): Promise<AuthInfo> {
    const at = tokenStore.getAccessToken(token);
    if (!at) throw new Error("Access token not found or expired");

    return {
      token: at.token,
      clientId: at.clientId,
      scopes: at.scopes,
      expiresAt: at.expiresAt,
      extra: {
        upstreamAccessToken: at.upstreamTokens.accessToken,
      },
    } as AuthInfo;
  }

  async revokeToken(
    _client: OAuthClientInformationFull,
    request: OAuthTokenRevocationRequest,
  ): Promise<void> {
    tokenStore.removeAccessToken(request.token);
    tokenStore.removeRefreshToken(request.token);
  }

  skipLocalPkceValidation = false;
}

// ---------------------------------------------------------------------------
// OAuth Callback Handler (Express route)
// ---------------------------------------------------------------------------

export async function handleOAuthCallback(
  req: { query: Record<string, string> },
  res: Response,
): Promise<void> {
  const { code, state, error } = req.query;

  if (error) {
    res.status(400).json({ error, description: req.query.error_description });
    return;
  }
  if (!code || !state) {
    res.status(400).json({ error: "Missing code or state" });
    return;
  }

  const pending = pendingAuth.get(state);
  if (!pending) {
    res.status(400).json({ error: "Unknown or expired state" });
    return;
  }
  pendingAuth.delete(state);

  // Exchange upstream auth code for upstream tokens
  const body = new URLSearchParams({
    grant_type: "authorization_code",
    client_id: UPSTREAM_CLIENT_ID,
    client_secret: UPSTREAM_CLIENT_SECRET,
    code,
    redirect_uri: `${SERVER_URL}/oauth/callback`,
  });

  const resp = await fetch(upstreamTokenUrl(), {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: body.toString(),
  });

  if (!resp.ok) {
    res.status(502).json({ error: "Upstream token exchange failed" });
    return;
  }

  const upstreamData = await resp.json();
  const mcpParams = pending.mcpParams;

  // Generate MCP auth code backed by upstream tokens
  const mcpCode = crypto.randomBytes(32).toString("base64url");

  tokenStore.storeAuthCode({
    code: mcpCode,
    clientId: pending.client.client_id,
    scopes: mcpParams.scopes || ["useraccount"],
    codeChallenge: mcpParams.codeChallenge,
    redirectUri: mcpParams.redirectUri,
    state: mcpParams.state,
    expiresAt: Math.floor(Date.now() / 1000) + 600,
    upstreamTokens: {
      accessToken: upstreamData.access_token,
      refreshToken: upstreamData.refresh_token,
      expiresIn: upstreamData.expires_in,
    },
  });

  // Redirect back to Claude Desktop with MCP auth code
  const redirectUrl = new URL(mcpParams.redirectUri);
  redirectUrl.searchParams.set("code", mcpCode);
  if (mcpParams.state) redirectUrl.searchParams.set("state", mcpParams.state);

  res.redirect(302, redirectUrl.toString());
}
```

## Key Design Decisions

1. **Permissive client registration** — Claude Desktop and claude.ai send different client IDs. Auto-registering with known redirect URIs avoids manual configuration.

2. **30-day MCP token expiry** — Long enough that users don't re-authenticate daily, short enough to rotate regularly.

3. **Pending auth in memory** — Auth flow completes in seconds, so in-memory storage with 10-minute TTL is sufficient. No need to persist to disk.

4. **Token store on disk** — Access/refresh tokens must survive container restarts. Persist to a mounted volume.

5. **Upstream token attached to AuthInfo.extra** — After `verifyAccessToken()`, the upstream access token is available in `authInfo.extra.upstreamAccessToken` for API calls.

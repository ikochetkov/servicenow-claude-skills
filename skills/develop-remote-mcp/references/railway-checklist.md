# Railway Deployment Checklist

Pre-deployment checklist for MCP servers on Railway.

## Dockerfile

- [ ] Base image: `node:20-slim` (small, production-ready)
- [ ] `npm ci --production=false` (need devDependencies for TypeScript compilation)
- [ ] `npx tsc` to compile TypeScript in the build stage
- [ ] `ENV TRANSPORT=http` and `ENV PORT=8000`
- [ ] `EXPOSE 8000`
- [ ] `RUN mkdir -p /data` for token store directory
- [ ] **NO `VOLUME` instruction** — Railway bans it. Mount volumes via dashboard.
- [ ] `CMD ["node", "dist/index.js"]`

## railway.json

```json
{
  "$schema": "https://railway.com/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

## Environment Variables (Railway Dashboard)

| Variable | Example | Required |
|----------|---------|----------|
| `TRANSPORT` | `http` | Yes |
| `SERVER_URL` | `https://your-app.up.railway.app` | Yes |
| `PORT` | `8000` | Yes |
| `UPSTREAM_URL` | `https://instance.service-now.com` | Yes |
| `UPSTREAM_OAUTH_CLIENT_ID` | `abc123...` | Yes (for OAuth) |
| `UPSTREAM_OAUTH_CLIENT_SECRET` | `secret...` | Yes (for OAuth) |
| `DATA_DIR` | `/data` | No (default) |

## Railway Volume

1. Go to your service in Railway dashboard
2. Click **Volumes** → **Add Volume**
3. Mount path: `/data`
4. This persists `tokens.json` across deploys

## Express Configuration

- [ ] `app.set("trust proxy", 1)` — Railway uses a reverse proxy. Without this, rate limiters and IP-based middleware see `127.0.0.1`.
- [ ] Listen on `0.0.0.0` (not `localhost`) — Railway requires binding to all interfaces.

## Auth Routes

- [ ] `mcpAuthRouter()` mounted at app level (handles `/.well-known/oauth-*`, `/authorize`, `/token`, `/register`)
- [ ] `requireBearerAuth()` added to `/mcp` endpoint — NOT automatic from `mcpAuthRouter`
- [ ] `/oauth/callback` route for upstream OAuth redirect
- [ ] `/health` endpoint (no auth) for Railway health checks

## Post-Deploy Verification

1. **Health check**: `curl https://your-app.up.railway.app/health`
2. **OAuth metadata**: `curl https://your-app.up.railway.app/.well-known/oauth-authorization-server`
3. **Connect from Claude Desktop**: Add remote MCP server URL → authenticate → verify tool list appears

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Deploy fails with `VOLUME not allowed` | `VOLUME` in Dockerfile | Remove `VOLUME`, use `RUN mkdir -p /data` + Railway volume |
| All requests show same IP | Missing trust proxy | Add `app.set("trust proxy", 1)` |
| `/mcp` returns 401 but OAuth works | `requireBearerAuth` not on `/mcp` | Add middleware: `app.all("/mcp", bearerAuth, ...)` |
| Tokens lost after redeploy | No persistent volume | Mount Railway volume at `/data` |
| OAuth callback fails | Wrong `SERVER_URL` | Set `SERVER_URL` to your Railway public URL (with https) |
| Connection refused | Listening on localhost | Listen on `0.0.0.0`: `app.listen(PORT, "0.0.0.0")` |

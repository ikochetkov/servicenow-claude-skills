# ServiceNow Claude Skills

Skills that teach Claude how to build, deploy, and price ServiceNow solutions.

| Skill | Description |
|-------|-------------|
| **building-servicenow-spas** | Build & deploy Single Page Applications to ServiceNow (Vite, HashRouter, dual-mode auth, ParentHashSync) |
| **building-servicenow-components** | Build UI Builder components using Next Experience framework (createCustomElement, state, effects) |
| **design-servicenow-style** | ServiceNow design system — colors, typography, spacing, component patterns for Next Experience, Service Portal, and Classic UI |
| **servicenow-pricing** | ServiceNow pricing, licensing, SKUs, packaging tiers, and module comparisons |
| **mobiz-servicenow-flow-designer** | Flow Designer analysis, diagnostics & programmatic creation — flow structure, execution logs, subflow drill-down, Mermaid diagrams, build flows via API |
| **develop-remote-mcp** | Build & deploy remote MCP servers with OAuth, StreamableHTTP transport, and Railway hosting |
| **mobiz-servicenow-awa-schedules** | ServiceNow schedule management & AWA eligibility validation (working hours, time off, availability checks, AWA diagnostics) |

---

## Install to Claude Code (VS Code extension or CLI)

This method gives you automatic updates — when skills are updated in this repo, your Claude Code picks up changes automatically.

**Step 1.** Open Claude Code (in VS Code or terminal) and run:

```
/plugin marketplace add ikochetkov/servicenow-claude-skills
```

**Step 2.** Install the skills you need (pick one or all):

```
/plugin install building-servicenow-spas@servicenow-claude-skills
/plugin install building-servicenow-components@servicenow-claude-skills
/plugin install design-servicenow-style@servicenow-claude-skills
/plugin install servicenow-pricing@servicenow-claude-skills
/plugin install mobiz-servicenow-flow-designer@servicenow-claude-skills
/plugin install develop-remote-mcp@servicenow-claude-skills
/plugin install mobiz-servicenow-awa-schedules@servicenow-claude-skills
```

**Step 3.** Done. Start a conversation and mention the topic — Claude will use the skill automatically.

> **Updating:** Skills update automatically. To manually refresh: `/plugin update`

---

## Install to Claude Desktop or Claude.ai

**Step 1.** Download the skill file (`.skill` or `.zip` — same contents, pick whichever your system prefers):

| Skill | .skill | .zip |
|-------|--------|------|
| Building ServiceNow SPAs | [`building-servicenow-spas.skill`](dist/building-servicenow-spas.skill) | [`building-servicenow-spas.zip`](dist/building-servicenow-spas.zip) |
| Building ServiceNow Components | [`building-servicenow-components.skill`](dist/building-servicenow-components.skill) | [`building-servicenow-components.zip`](dist/building-servicenow-components.zip) |
| Design ServiceNow Style | [`design-servicenow-style.skill`](dist/design-servicenow-style.skill) | [`design-servicenow-style.zip`](dist/design-servicenow-style.zip) |
| ServiceNow Pricing | [`servicenow-pricing.skill`](dist/servicenow-pricing.skill) | [`servicenow-pricing.zip`](dist/servicenow-pricing.zip) |
| ServiceNow Flow Designer | [`mobiz-servicenow-flow-designer.skill`](dist/mobiz-servicenow-flow-designer.skill) | [`mobiz-servicenow-flow-designer.zip`](dist/mobiz-servicenow-flow-designer.zip) |
| Develop Remote MCP | [`develop-remote-mcp.skill`](dist/develop-remote-mcp.skill) | [`develop-remote-mcp.zip`](dist/develop-remote-mcp.zip) |
| Mobiz AWA Schedules | [`mobiz-servicenow-awa-schedules.skill`](dist/mobiz-servicenow-awa-schedules.skill) | [`mobiz-servicenow-awa-schedules.zip`](dist/mobiz-servicenow-awa-schedules.zip) |

> Click the link above → then click the **Download raw file** button on GitHub.

**Step 2.** Open **Claude Desktop** or **claude.ai**

**Step 3.** Create or open a **Project**

**Step 4.** Go to **Project settings** → **Skills** → click **Add skill** → upload the `.skill` file

**Step 5.** Done. The skill is now available in all conversations within that project.

> **Updating:** When a skill is updated, re-download the `.skill` file and re-upload it to your project.

---

## Available skills

### building-servicenow-spas

Teaches Claude how to compile any web app (React, Vue, Svelte) into a single HTML file via Vite + `vite-plugin-singlefile`, store it in a ServiceNow system property, and serve it via a Scripted REST endpoint. Covers:

- Vite single-file bundling configuration
- HashRouter + ParentHashSync for ServiceNow nav frame URL sync
- Dual-mode authentication (local dev with cookies, ServiceNow with X-userToken)
- Deployment scripts and ServiceNow artifact setup (Scripted REST, system properties)

### building-servicenow-components

Teaches Claude how to build custom UI Builder components using ServiceNow's Next Experience framework. Covers:

- `createCustomElement` component structure
- Immutable state with `updateState` (not React — Snabbdom)
- Action handlers, HTTP effects, and dispatching
- Now Components library usage
- CLI setup (`snc ui-component`) and deployment

### design-servicenow-style

ServiceNow design system guide for building apps that match the native ServiceNow look and feel. Covers:

- Next Experience (Horizon/Polaris) design tokens and CSS custom properties
- Service Portal (AngularJS/Bootstrap 3) SCSS variables and widget styling
- Classic UI compatibility guidelines
- Complete color system, typography scale, spacing, shadows, and border radius
- Component patterns (forms, lists, cards, modals, navigation, notifications)
- Accessibility (WCAG 2.1 AA) checklist and focus management
- Ready-to-use code templates for UI Builder components, Service Portal widgets, and standalone SPAs
- Dark mode / theming support

### servicenow-pricing

Comprehensive knowledge base for ServiceNow pricing and packaging. Covers:

- ITSM, ITOM, ITAM, CSM/CRM, Security Operations, SPM
- App Engine, Employee Workflows
- Now Assist and AI features
- Packaging tiers (Standard / Pro / Enterprise)
- Module comparisons and licensing models

### mobiz-servicenow-flow-designer

ServiceNow Flow Designer analysis, diagnostics, and programmatic creation. Covers:

- **Design-time analysis** — describe any flow's actions, subflows, logic blocks, and stages
- **V1 vs V2 table detection** — automatically handles legacy and modern flow table formats
- **Runtime execution** — fetch latest execution, state, runtime, logs, warnings, and errors
- **Subflow drill-down** — recursively analyze subflow internals
- **Visual diagrams** — generate Mermaid flowcharts from flow structure
- **Catalog item linkage** — find which flow backs a catalog item
- **Programmatic creation** — build complete flows via API with gzip/base64 encoded values payloads
- **Input discovery** — query any action type to discover its required/optional inputs
- **Values decode/encode** — read and write the compressed values column that stores all step inputs

Uses the standard ServiceNow Table API — no additional plugins required.

### mobiz-servicenow-awa-schedules

ServiceNow schedule management and AWA (Advanced Work Assignment) eligibility validation. Covers:

- **Fetch schedule** — resolve user, read cmn_schedule + cmn_schedule_span, convert UTC to schedule timezone
- **Add time off** — create exclude spans with admin authorization check
- **Update working hours** — end-old/create-new pattern preserving audit history
- **Check availability** — overlap detection against time-off and busy entries
- **AWA eligibility validation** — 6-check diagnostic (excluded group, AWA group membership, agent presence, channel capacity, universal capacity, schedule hours)
- **Timezone mismatch detection** — catches mixed-timezone schedule bugs (days in one TZ, hours in another)
- **Dual presentation** — markdown for Cowork/chat, Slack Block Kit for Slack

Uses the standard ServiceNow Table API — no additional plugins required.

### develop-remote-mcp

Teaches Claude how to build and deploy remote MCP servers that run as hosted web services. Covers:

- MCP SDK architecture (Server, Transport, Tool handlers)
- Single dispatcher pattern (one tool → many handlers, saves 5K-10K tokens/turn)
- Dual transport (stdio for local, HTTP for remote)
- OAuth bridge pattern (MCP OAuth ↔ upstream provider OAuth)
- `OAuthServerProvider` implementation, `requireBearerAuth`, `mcpAuthRouter`
- Persistent token storage for container restarts
- Railway deployment (Dockerfile, volumes, trust proxy, env vars)
- Claude Desktop connector setup and OAuth flow UX
- Common gotchas and blockers (VOLUME banned, trust proxy, session management)

---

## Skill Development

When creating or updating a skill, **always rebuild its dist files** before pushing:

```bash
# From repo root — rebuild dist for a specific skill
cd skills/{skill-name}
zip -r ../../dist/{skill-name}.skill SKILL.md references/
cp ../../dist/{skill-name}.skill ../../dist/{skill-name}.zip
```

The `dist/` folder contains `.skill` and `.zip` files (identical content) used by Claude Desktop and claude.ai users. Claude Code users get updates directly from `skills/`, but Desktop/claude.ai users download from `dist/`.

**Checklist:**
1. Edit files under `skills/{skill-name}/`
2. Rebuild `dist/{skill-name}.skill` and `.zip`
3. Commit both source and dist changes
4. Push to main

---

## Repo structure

```
servicenow-claude-skills/
├── .claude-plugin/
│   └── marketplace.json        ← plugin marketplace (Claude Code auto-install)
├── skills/                     ← skill source files
│   ├── building-servicenow-spas/
│   ├── building-servicenow-components/
│   ├── design-servicenow-style/
│   ├── servicenow-pricing/
│   ├── mobiz-servicenow-flow-designer/
│   ├── develop-remote-mcp/
│   └── mobiz-servicenow-awa-schedules/
├── dist/                       ← downloadable files (Claude Desktop / claude.ai)
│   ├── building-servicenow-spas.skill / .zip
│   ├── building-servicenow-components.skill / .zip
│   ├── design-servicenow-style.skill / .zip
│   ├── servicenow-pricing.skill / .zip
│   ├── mobiz-servicenow-flow-designer.skill / .zip
│   ├── develop-remote-mcp.skill / .zip
│   └── mobiz-servicenow-awa-schedules.skill / .zip
└── README.md
```

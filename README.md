# ServiceNow Claude Skills

Skills that teach Claude how to build, deploy, and price ServiceNow solutions.

| Skill | Description |
|-------|-------------|
| **building-servicenow-spas** | Build & deploy Single Page Applications to ServiceNow (Vite, HashRouter, dual-mode auth, ParentHashSync) |
| **building-servicenow-components** | Build UI Builder components using Next Experience framework (createCustomElement, state, effects) |
| **servicenow-pricing** | ServiceNow pricing, licensing, SKUs, packaging tiers, and module comparisons |

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
/plugin install servicenow-pricing@servicenow-claude-skills
```

**Step 3.** Done. Start a conversation and mention the topic — Claude will use the skill automatically.

> **Updating:** Skills update automatically. To manually refresh: `/plugin update`

---

## Install to Claude Desktop or Claude.ai

**Step 1.** Download the `.skill` file for the skill you need:

| Skill | Download |
|-------|----------|
| Building ServiceNow SPAs | [`building-servicenow-spas.skill`](dist/building-servicenow-spas.skill) |
| Building ServiceNow Components | [`building-servicenow-components.skill`](dist/building-servicenow-components.skill) |
| ServiceNow Pricing | [`servicenow-pricing.skill`](dist/servicenow-pricing.skill) |

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

### servicenow-pricing

Comprehensive knowledge base for ServiceNow pricing and packaging. Covers:

- ITSM, ITOM, ITAM, CSM/CRM, Security Operations, SPM
- App Engine, Employee Workflows
- Now Assist and AI features
- Packaging tiers (Standard / Pro / Enterprise)
- Module comparisons and licensing models

---

## Repo structure

```
servicenow-claude-skills/
├── .claude-plugin/
│   └── marketplace.json        ← plugin marketplace (Claude Code auto-install)
├── skills/                     ← skill source files
│   ├── building-servicenow-spas/
│   ├── building-servicenow-components/
│   └── servicenow-pricing/
├── dist/                       ← downloadable .skill files (Claude Desktop)
│   ├── building-servicenow-spas.skill
│   ├── building-servicenow-components.skill
│   └── servicenow-pricing.skill
└── README.md
```

# ServiceNow Claude Skills

Skills that teach Claude how to build, deploy, and price ServiceNow solutions.

| Skill | Description |
|-------|-------------|
| **building-servicenow-spas** | Build & deploy Single Page Applications to ServiceNow (Vite, HashRouter, dual-mode auth, ParentHashSync) |
| **building-servicenow-components** | Build UI Builder components using Next Experience framework (createCustomElement, state, effects) |
| **design-servicenow-style** | ServiceNow design system — colors, typography, spacing, component patterns for Next Experience, Service Portal, and Classic UI |
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
/plugin install design-servicenow-style@servicenow-claude-skills
/plugin install servicenow-pricing@servicenow-claude-skills
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
│   └── servicenow-pricing/
├── dist/                       ← downloadable files (Claude Desktop / claude.ai)
│   ├── building-servicenow-spas.skill / .zip
│   ├── building-servicenow-components.skill / .zip
│   ├── design-servicenow-style.skill / .zip
│   └── servicenow-pricing.skill / .zip
└── README.md
```

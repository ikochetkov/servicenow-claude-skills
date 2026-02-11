# ServiceNow Claude Skills

Skills that teach Claude how to build, deploy, and price ServiceNow solutions.

| Skill | Description | Size |
|-------|-------------|------|
| **building-servicenow-spas** | Build & deploy Single Page Applications to ServiceNow (Vite, HashRouter, dual-mode auth) | 14 KB |
| **building-servicenow-components** | Build UI Builder components using Next Experience framework (createCustomElement, state, effects) | 15 KB |
| **servicenow-pricing** | ServiceNow pricing, licensing, SKUs, packaging tiers, and module comparisons | 32 KB |

## Installation

### Claude Code (CLI / VS Code extension)

Add the marketplace and install any skills you need:

```
/plugin marketplace add ikochetkov/servicenow-claude-skills
/plugin install building-servicenow-spas@servicenow-claude-skills
/plugin install building-servicenow-components@servicenow-claude-skills
/plugin install servicenow-pricing@servicenow-claude-skills
```

Skills auto-update when the repo is updated.

### Claude Desktop / Claude.ai

1. Download the `.skill` file from the [`dist/`](dist/) folder (or from [Releases](../../releases))
2. Open **Claude Desktop** or **Claude.ai**
3. Go to project **Skills** settings and upload the `.skill` file
4. The skill is now available in that project

### Manual install (any Claude client)

```bash
git clone https://github.com/ikochetkov/servicenow-claude-skills.git
cp -r servicenow-claude-skills/skills/building-servicenow-spas ~/.claude/skills/
```

To update later: `git pull` and re-copy.

## Updating skills

When a skill is updated:
- **Claude Code** — updates automatically via the plugin marketplace
- **Claude Desktop / Claude.ai** — re-download the `.skill` file from `dist/` and re-upload
- **Manual** — `git pull` and re-copy the skill folder

## Repo structure

```
servicenow-claude-skills/
├── .claude-plugin/
│   └── marketplace.json        ← plugin marketplace config (Claude Code)
├── skills/
│   ├── building-servicenow-spas/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── building-servicenow-components/
│   │   ├── SKILL.md
│   │   └── references/
│   └── servicenow-pricing/
│       ├── SKILL.md
│       └── references/
├── dist/                       ← downloadable .skill files (zip archives)
│   ├── building-servicenow-spas.skill
│   ├── building-servicenow-components.skill
│   └── servicenow-pricing.skill
└── README.md
```

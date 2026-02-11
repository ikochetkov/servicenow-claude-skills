# Now CLI and Deployment Reference

## Contents

- [Install Now CLI](#install-now-cli)
- [Configure Profile](#configure-profile)
- [Create Component](#create-component)
- [Project Structure](#project-structure)
- [now-cli.json Configuration](#now-clijson-configuration)
- [now-ui.json Metadata](#now-uijson-metadata)
- [Development Workflow](#development-workflow)
- [Deployment](#deployment)
- [Testing](#testing)
- [Common CLI Commands](#common-cli-commands)
- [Troubleshooting](#troubleshooting)

## Install Now CLI

```bash
npm install -g @servicenow/cli
```

Verify installation:

```bash
snc --version
snc --help
```

Requires Node.js 14+ and npm 6+.

## Configure Profile

A profile connects the CLI to a ServiceNow instance:

```bash
# Interactive setup
snc configure profile set

# Non-interactive
snc configure profile set \
  --host https://devXXXXXX.service-now.com \
  --username admin \
  --password 'your-password'
```

### Profile Management

```bash
# List profiles
snc configure profile list

# Set default profile
snc configure profile set --profile my-profile

# Switch active profile
snc configure profile use my-profile

# Remove profile
snc configure profile remove --profile my-profile
```

Profiles are stored in `~/.snc/config.json`.

## Create Component

```bash
# Create a new component project
snc ui-component create --name x-company-my-component --scope x_company_app

# With specific directory
snc ui-component create --name x-company-my-component --scope x_company_app --dir ./my-component
```

### Naming Rules

- Must contain a hyphen (web component spec)
- Convention: `x-{company}-{component-name}`
- All lowercase, kebab-case
- Example: `x-mobiz-task-board`, `x-acme-user-card`

### Scope

The scope must match an existing scoped application on the ServiceNow instance. Format: `x_{vendor}_{app}`.

## Project Structure

After `snc ui-component create`:

```
x-company-my-component/
├── src/
│   └── x-company-my-component/
│       ├── index.js                  # Main component file
│       ├── __tests__/
│       │   └── x-company-my-component.test.js
│       └── styles.scss               # Optional external styles
├── example/
│   └── element.js                    # Example usage for dev server
├── now-ui.json                       # UI Builder metadata
├── now-cli.json                      # CLI configuration
├── package.json
├── jsconfig.json
└── README.md
```

### Key Files

**src/x-company-my-component/index.js** - Main component:

```javascript
import { createCustomElement } from '@servicenow/ui-core';

createCustomElement('x-company-my-component', {
  view: (state, { updateState }) => {
    return <div>Hello World</div>;
  },
  initialState: {},
  properties: {},
  actionHandlers: {}
});
```

**example/element.js** - Dev server usage example:

```javascript
import '../src/x-company-my-component';

const el = document.createElement('x-company-my-component');
el.title = 'Dev Example';
document.body.appendChild(el);
```

## now-cli.json Configuration

```json
{
  "host": "https://devXXXXXX.service-now.com",
  "development": {
    "proxy": {
      "origin": "https://devXXXXXX.service-now.com"
    }
  }
}
```

### Proxy Configuration

The proxy routes API calls from the local dev server to the ServiceNow instance. Required for `createHttpEffect` and any `/api/` calls during development.

```json
{
  "development": {
    "proxy": {
      "origin": "https://devXXXXXX.service-now.com",
      "auth": {
        "username": "admin",
        "password": "password"
      }
    }
  }
}
```

### Additional Options

```json
{
  "development": {
    "port": 8081,
    "open": true,
    "proxy": {
      "origin": "https://devXXXXXX.service-now.com",
      "paths": ["/api"]
    }
  }
}
```

## now-ui.json Metadata

This file defines how the component appears in UI Builder:

```json
{
  "components": {
    "x-company-my-component": {
      "innerComponents": [],
      "uiBuilder": {
        "associatedTypes": ["global.core", "global.landing-page"],
        "label": "My Component",
        "icon": "document-outline",
        "description": "A custom component for displaying data",
        "category": "primitives"
      },
      "properties": [
        {
          "name": "title",
          "label": "Title",
          "description": "Component title",
          "fieldType": "string",
          "defaultValue": "My Component"
        },
        {
          "name": "maxItems",
          "label": "Max Items",
          "description": "Maximum number of items to display",
          "fieldType": "integer",
          "defaultValue": 20
        }
      ],
      "actions": [
        {
          "name": "ITEM_SELECTED",
          "label": "Item Selected",
          "description": "Fired when a user selects an item",
          "payload": {
            "id": { "type": "string", "description": "Selected item sys_id" }
          }
        }
      ]
    }
  }
}
```

### Associated Types

Controls where the component can be used in UI Builder:

| Type | Context |
|------|---------|
| `global.core` | Standard UI Builder pages |
| `global.landing-page` | Landing/portal pages |
| `global.workspace` | Agent Workspace |
| `global.configurable-workspace` | Configurable Workspace |

### Categories

| Category | Description |
|----------|-------------|
| `primitives` | Basic building blocks |
| `data` | Data display/manipulation |
| `input` | Form inputs |
| `layout` | Page layout components |
| `navigation` | Navigation elements |

## Development Workflow

### Start Dev Server

```bash
# Start with auto-open browser
snc ui-component develop --open

# Start on specific port
snc ui-component develop --port 8081

# Start without opening browser
snc ui-component develop
```

Dev server provides:
- Hot module replacement (HMR)
- API proxy to ServiceNow instance
- Local component rendering

### Development Cycle

1. Edit component code in `src/`
2. Browser auto-refreshes via HMR
3. Test API calls through proxy
4. Write/run tests
5. Deploy when ready

## Deployment

### Deploy to Instance

```bash
# Deploy component
snc ui-component deploy

# Force deploy (skip confirmation)
snc ui-component deploy --force

# Deploy to specific profile
snc ui-component deploy --profile production
```

### What Happens on Deploy

1. Component is packaged and uploaded to the ServiceNow instance
2. Registered in sys_ux_lib_component table
3. Available in UI Builder component palette
4. Associated with the specified scope

### Post-Deployment

After deploying:
1. Open UI Builder on the target instance
2. Navigate to the page where you want to use the component
3. Find the component in the component palette (search by label)
4. Drag it onto the page
5. Configure properties in the property panel

## Testing

### Running Tests

```bash
# Run all tests
npm test

# Run with watch
npm test -- --watch

# Run specific test file
npm test -- --testPathPattern=my-component
```

### Writing Tests

```javascript
import { createCustomElement } from '@servicenow/ui-core';
import '../index.js';

describe('x-company-my-component', () => {
  let element;

  beforeEach(() => {
    element = document.createElement('x-company-my-component');
    document.body.appendChild(element);
  });

  afterEach(() => {
    element.remove();
  });

  it('should render with default state', () => {
    const shadowRoot = element.shadowRoot;
    expect(shadowRoot.querySelector('.container')).toBeTruthy();
  });

  it('should display title from property', async () => {
    element.title = 'Test Title';
    await element.updateComplete;
    const heading = element.shadowRoot.querySelector('h2');
    expect(heading.textContent).toBe('Test Title');
  });
});
```

## Common CLI Commands

| Command | Description |
|---------|-------------|
| `snc ui-component create` | Create new component project |
| `snc ui-component develop` | Start dev server |
| `snc ui-component deploy` | Deploy to instance |
| `snc ui-component deploy --force` | Deploy without confirmation |
| `snc configure profile set` | Configure instance profile |
| `snc configure profile list` | List all profiles |
| `snc configure profile use {name}` | Switch active profile |
| `snc --version` | Show CLI version |
| `snc --help` | Show help |

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `snc: command not found` | CLI not installed globally | `npm install -g @servicenow/cli` |
| 502 errors in dev | Proxy misconfigured or instance down | Check `now-cli.json` proxy origin, verify instance is running |
| Authentication failed | Wrong credentials | Run `snc configure profile set` again |
| Deploy fails | Scope mismatch | Ensure component scope matches an existing scoped app on instance |
| Component not in UI Builder | Not associated with right type | Check `now-ui.json` `associatedTypes` |
| Hot reload not working | Dev server stale | Stop and restart `snc ui-component develop` |
| `Cannot find module '@servicenow/ui-core'` | Dependencies not installed | Run `npm install` |
| API calls fail in dev | Proxy auth missing | Add `auth` to `development.proxy` in `now-cli.json` |

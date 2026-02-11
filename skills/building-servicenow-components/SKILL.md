---
name: building-servicenow-components
description: Builds custom ServiceNow UI Builder components using the Next Experience UI Framework. Covers createCustomElement, immutable state with updateState, action handlers, HTTP effects, Now Components, CLI setup, and deployment. Handles new component creation, React-to-ServiceNow conversion, and ServiceNow-specific patterns. Triggers on ServiceNow component, UI Builder, createCustomElement, Now Experience, snc ui-component, now-button, updateState, actionHandlers, Snabbdom.
---

# Building ServiceNow UI Builder Components

## Contents

- [Critical: Not React](#critical-not-react)
- [Component Template](#component-template)
- [Quick Start](#quick-start)
- [React to ServiceNow Conversion](#react-to-servicenow-conversion)
- [Now Components Library](#now-components-library)
- [Troubleshooting](#troubleshooting)
- [Reference Docs](#reference-docs)

## Critical: Not React

ServiceNow UI Framework uses Snabbdom (not React). The syntax looks like JSX but the runtime is different.

| React | ServiceNow |
|-------|-----------|
| `function Component()` / `class` | `createCustomElement('x-company-name', {...})` |
| `useState()` / `setState()` | `initialState` + `updateState()` |
| `useEffect()` | `actionHandlers` with `COMPONENT_BOOTSTRAPPED` |
| `onClick={fn}` | `on-click={fn}` |
| `<Button>` | `<now-button>` |
| Props as function params | `properties` with `schema` |
| React reconciliation | Snabbdom virtual DOM |

## Component Template

```javascript
import { createCustomElement, actionTypes } from '@servicenow/ui-core';
import { createHttpEffect } from '@servicenow/ui-effect-http';
import '@servicenow/now-button';

const FETCH_SUCCESS = 'FETCH_SUCCESS';
const FETCH_ERROR = 'FETCH_ERROR';

createCustomElement('x-company-my-component', {
  view: (state, { updateState, dispatch }) => {
    if (state.loading) return <div>Loading...</div>;
    if (state.error) return <div className="error">{state.error}</div>;
    return (
      <div className="container">
        <h2>{state.properties.title}</h2>
        {state.items.map(item => (
          <div key={item.sys_id}>{item.name}</div>
        ))}
        <now-button label="Refresh" on-click={() => dispatch('FETCH_REQUESTED')} />
      </div>
    );
  },
  initialState: { items: [], loading: false, error: null },
  properties: {
    title: { default: 'My Component', schema: { type: 'string' } }
  },
  actionHandlers: {
    [actionTypes.COMPONENT_BOOTSTRAPPED]: ({ dispatch }) => {
      dispatch('FETCH_REQUESTED');
    },
    FETCH_REQUESTED: createHttpEffect('/api/now/table/incident', {
      method: 'GET',
      queryParams: [{ name: 'sysparm_limit', value: 10 }],
      successActionType: FETCH_SUCCESS,
      errorActionType: FETCH_ERROR
    }),
    [FETCH_SUCCESS]: ({ action, updateState }) => {
      updateState({ items: action.payload.result, loading: false });
    },
    [FETCH_ERROR]: ({ action, updateState }) => {
      updateState({ error: action.payload.message, loading: false });
    }
  },
  styles: `
    .container { padding: 16px; }
    .error { color: red; }
  `
});
```

## Quick Start

1. Install Now CLI: `npm install -g @servicenow/cli`
2. Configure profile: `snc configure profile set --host https://instance.service-now.com`
3. Create component: `snc ui-component create --name x-company-my-component --scope x_company_app`
4. Install HTTP effect: `npm install @servicenow/ui-effect-http -E`
5. Edit `src/x-company-my-component/index.js` using the template above
6. Run dev server: `snc ui-component develop --open`
7. Deploy to instance: `snc ui-component deploy --force`

## React to ServiceNow Conversion

| Step | From (React) | To (ServiceNow) |
|------|-------------|-----------------|
| 1 | `import React` | `import { createCustomElement, actionTypes } from '@servicenow/ui-core'` |
| 2 | `useState(init)` | Add to `initialState: { ... }` |
| 3 | `setX(val)` | `updateState({ x: val })` |
| 4 | `useEffect(() => {}, [])` | `actionHandlers: { [actionTypes.COMPONENT_BOOTSTRAPPED]: ... }` |
| 5 | `onClick={fn}` | `on-click={fn}` |
| 6 | `<Button>` / MUI | `<now-button>` / Now Components |
| 7 | `fetch()` in effect | `createHttpEffect()` in action handler |
| 8 | `props.x` | `state.properties.x` |
| 9 | Component CSS modules | `styles` string property (SCSS) |
| 10 | `export default` | `createCustomElement('x-company-name', {...})` |

## Now Components Library

Import and use ServiceNow's built-in components:

```javascript
import '@servicenow/now-button';       // <now-button label="Click" variant="primary" />
import '@servicenow/now-input';        // <now-input value={state.text} on-input={...} />
import '@servicenow/now-dropdown';     // <now-dropdown items={items} on-change={...} />
import '@servicenow/now-modal';        // <now-modal opened={state.open} on-close={...} />
import '@servicenow/now-icon';         // <now-icon icon="check-fill" />
import '@servicenow/now-loader';       // <now-loader label="Loading..." />
import '@servicenow/now-alert';        // <now-alert status="info" header="Note" />
import '@servicenow/now-card';         // <now-card size="md" interaction="none" />
import '@servicenow/now-tabs';         // <now-tabs items={tabItems} selected={0} />
import '@servicenow/now-toggle';       // <now-toggle checked={state.on} on-change={...} />
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| State not updating | Direct mutation | Use `updateState()` with new object |
| Events not firing | `onClick` syntax | Use `on-click`, `on-input`, `on-change` |
| Component not rendering | Missing registration | Must call `createCustomElement()` |
| Props undefined | Wrong access | Use `state.properties.propName` |
| HTTP 502 in dev | Proxy not configured | Set `development.proxy.origin` in now-cli.json |
| Styles not scoped | Wrong config | Use `styles` string, not external CSS file |

## Reference Docs

- [Component Patterns](references/component-patterns.md) - Properties, state, view, actions, lifecycle, styles, events
- [State and Effects](references/state-and-effects.md) - Immutable state, HTTP effects, createHttpEffect API, action dispatch
- [CLI and Deployment](references/cli-and-deployment.md) - Now CLI, project structure, development flow, deployment
- Official docs: https://developer.servicenow.com/dev.do#!/reference/next-experience/zurich/ui-framework

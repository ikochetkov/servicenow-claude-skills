# Component Patterns Reference

## Contents

- [Component Anatomy](#component-anatomy)
- [Properties](#properties)
- [Initial State](#initial-state)
- [View Function](#view-function)
- [Action Handlers](#action-handlers)
- [Lifecycle Actions](#lifecycle-actions)
- [Event Handling](#event-handling)
- [Styles](#styles)
- [Now Components](#now-components)
- [File Structure](#file-structure)
- [Naming Conventions](#naming-conventions)

## Component Anatomy

Every component is registered with `createCustomElement` from `@servicenow/ui-core`:

```javascript
import { createCustomElement, actionTypes } from '@servicenow/ui-core';

createCustomElement('x-company-widget', {
  renderer: { type: 'snabbdom' },  // Default, usually omitted
  view,                             // Render function
  initialState,                     // Default state
  properties,                       // External inputs with schemas
  actionHandlers,                   // Business logic handlers
  styles                            // Scoped CSS/SCSS string
});
```

Tag names MUST contain a hyphen (web component spec). Convention: `x-{company}-{component-name}`.

## Properties

Properties are external inputs to the component, equivalent to React props. Accessed via `state.properties.{name}`.

```javascript
properties: {
  title: {
    default: 'Default Title',
    schema: { type: 'string' }
  },
  maxItems: {
    default: 10,
    schema: { type: 'integer' }
  },
  showHeader: {
    default: true,
    schema: { type: 'boolean' }
  },
  items: {
    default: [],
    schema: { type: 'array' }
  },
  config: {
    default: {},
    schema: { type: 'object' }
  }
}
```

### Property Options

| Option | Type | Description |
|--------|------|-------------|
| `default` | any | Default value (required) |
| `schema` | object | JSON Schema for validation |
| `readOnly` | boolean | Cannot be set externally |
| `reflect` | boolean | Reflect to HTML attribute |
| `computed` | function | Derive value from other properties |

### Accessing Properties in View

```javascript
view: (state, helpers) => {
  const { title, maxItems } = state.properties;
  return <h2>{title} (max: {maxItems})</h2>;
}
```

## Initial State

Defines default internal state. Must be a plain object (not a function).

```javascript
initialState: {
  items: [],
  loading: false,
  error: null,
  selectedId: null,
  formData: {
    name: '',
    email: ''
  },
  pagination: {
    page: 1,
    pageSize: 20,
    total: 0
  }
}
```

## View Function

The view function receives `(state, helpers)` and returns JSX (Snabbdom virtual DOM, not React).

```javascript
view: (state, { updateState, dispatch }) => {
  const { items, loading, error } = state;
  const { title } = state.properties;

  if (loading) return <now-loader label="Loading..." />;
  if (error) return <now-alert status="critical" header="Error" content={error} />;

  return (
    <div className="container">
      <h2>{title}</h2>
      <div className="list">
        {items.map(item => (
          <div key={item.sys_id} className="item"
            on-click={() => dispatch('ITEM_SELECTED', { id: item.sys_id })}>
            {item.name}
          </div>
        ))}
      </div>
      {items.length === 0 && <p>No items found.</p>}
    </div>
  );
}
```

### View Helpers

| Helper | Description |
|--------|-------------|
| `updateState(partialState)` | Shallow merge into state, triggers re-render |
| `dispatch(type, payload)` | Dispatch an action to action handlers |
| `updateProperties(props)` | Update component properties |

### Conditional Rendering

```javascript
// Ternary
{state.isOpen ? <div>Open</div> : <div>Closed</div>}

// Short-circuit
{state.error && <now-alert status="critical" content={state.error} />}

// Early return
if (state.loading) return <now-loader />;
```

### List Rendering

```javascript
{state.items.map(item => (
  <div key={item.sys_id} className="item">
    <span>{item.name}</span>
    <now-button label="Delete" variant="tertiary-destructive"
      on-click={() => dispatch('DELETE_ITEM', { id: item.sys_id })} />
  </div>
))}
```

Always provide `key` prop for list items.

## Action Handlers

Action handlers contain business logic. They respond to dispatched actions.

```javascript
actionHandlers: {
  // Lifecycle: runs on component init
  [actionTypes.COMPONENT_BOOTSTRAPPED]: ({ dispatch, updateState }) => {
    updateState({ loading: true });
    dispatch('FETCH_DATA');
  },

  // Custom action
  ITEM_SELECTED: ({ action, updateState }) => {
    updateState({ selectedId: action.payload.id });
  },

  // With state access
  DELETE_ITEM: ({ action, state, updateState }) => {
    const filtered = state.items.filter(i => i.sys_id !== action.payload.id);
    updateState({ items: filtered });
  },

  // Async with fetch
  SUBMIT_FORM: ({ state, updateState }) => {
    updateState({ submitting: true });
    fetch('/api/endpoint', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(state.formData)
    })
      .then(res => res.json())
      .then(data => updateState({ submitting: false, result: data }))
      .catch(err => updateState({ submitting: false, error: err.message }));
  }
}
```

### Action Handler Parameters

| Param | Description |
|-------|-------------|
| `action` | `{ type, payload, meta }` - the dispatched action |
| `state` | Current component state (read-only) |
| `updateState(partial)` | Merge partial state (shallow) |
| `dispatch(type, payload)` | Dispatch another action |
| `properties` | Current property values |

### Action Naming Convention

- UPPER_SNAKE_CASE
- Past tense for events: `USER_SELECTED`, `DATA_LOADED`, `FORM_SUBMITTED`
- Present tense for commands: `FETCH_DATA`, `SUBMIT_FORM`, `DELETE_ITEM`
- Use constants:

```javascript
const FETCH_USERS = 'FETCH_USERS';
const USERS_LOADED = 'USERS_LOADED';
const USERS_LOAD_FAILED = 'USERS_LOAD_FAILED';
```

## Lifecycle Actions

Import from `actionTypes`:

```javascript
import { actionTypes } from '@servicenow/ui-core';
```

| Action | When | Use For |
|--------|------|---------|
| `COMPONENT_BOOTSTRAPPED` | Component first rendered | Initial data fetch, setup |
| `COMPONENT_PROPERTY_CHANGED` | A property value changed | React to property updates |
| `COMPONENT_CONNECTED` | Added to DOM | Start subscriptions |
| `COMPONENT_DISCONNECTED` | Removed from DOM | Cleanup, cancel timers |

```javascript
actionHandlers: {
  [actionTypes.COMPONENT_BOOTSTRAPPED]: ({ dispatch }) => {
    dispatch('FETCH_INITIAL_DATA');
  },
  [actionTypes.COMPONENT_PROPERTY_CHANGED]: ({ action, dispatch }) => {
    if (action.payload.name === 'userId') {
      dispatch('FETCH_USER', { id: action.payload.value });
    }
  },
  [actionTypes.COMPONENT_DISCONNECTED]: ({ state }) => {
    if (state.timerId) clearInterval(state.timerId);
  }
}
```

## Event Handling

ServiceNow uses hyphenated event names, NOT camelCase.

```javascript
// Mouse events
<button on-click={() => dispatch('CLICKED')}>Click</button>
<div on-dblclick={() => dispatch('DOUBLE_CLICKED')}>Double click</div>
<div on-mouseenter={() => updateState({ hovered: true })}>Hover</div>

// Input events
<input value={state.text}
  on-input={(e) => updateState({ text: e.target.value })} />
<input on-change={(e) => updateState({ value: e.target.value })} />
<input on-keydown={(e) => {
  if (e.key === 'Enter') dispatch('SUBMIT');
}} />

// Form events
<form on-submit={(e) => {
  e.preventDefault();
  dispatch('FORM_SUBMITTED');
}}>
```

### Now Component Events

Now Components emit custom events. Handle with the same `on-` prefix:

```javascript
<now-button label="Save" on-click={() => dispatch('SAVE')} />
<now-dropdown items={items}
  on-now-dropdown--item-clicked={(e) => updateState({ selected: e.detail.item })} />
<now-toggle checked={state.enabled}
  on-now-toggle--toggled={(e) => updateState({ enabled: e.detail.checked })} />
```

## Styles

Styles are scoped to the component. Pass as a CSS/SCSS string:

```javascript
styles: `
  :host {
    display: block;
    font-family: var(--now-font-family, 'Lato', sans-serif);
  }
  .container {
    padding: 16px;
    border: 1px solid var(--now-color--border-primary, #e0e0e0);
    border-radius: 4px;
  }
  .header {
    font-size: var(--now-font-size--lg, 18px);
    font-weight: bold;
    margin-bottom: 12px;
  }
  .item {
    padding: 8px;
    cursor: pointer;
  }
  .item:hover {
    background: var(--now-color--background-secondary, #f5f5f5);
  }
  .error {
    color: var(--now-color--alert-critical-2, #d32f2f);
  }
`
```

### ServiceNow CSS Custom Properties

Use `--now-*` variables for consistent theming:

| Variable | Purpose |
|----------|---------|
| `--now-font-family` | Base font |
| `--now-font-size--sm/md/lg` | Font sizes |
| `--now-color--primary-1/2/3` | Primary colors |
| `--now-color--background-primary/secondary` | Background colors |
| `--now-color--border-primary/secondary` | Border colors |
| `--now-color--alert-critical/warning/info/positive` | Alert colors |
| `--now-color--text-primary/secondary/tertiary` | Text colors |

## Now Components

ServiceNow provides ready-to-use UI components. Install via npm:

```bash
npm install @servicenow/now-button @servicenow/now-input -E
```

### Common Components

| Component | Import | Usage |
|-----------|--------|-------|
| Button | `@servicenow/now-button` | `<now-button label="Save" variant="primary" />` |
| Input | `@servicenow/now-input` | `<now-input value={v} placeholder="Enter..." />` |
| Dropdown | `@servicenow/now-dropdown` | `<now-dropdown items={items} selected={sel} />` |
| Modal | `@servicenow/now-modal` | `<now-modal opened={open} size="md" />` |
| Icon | `@servicenow/now-icon` | `<now-icon icon="check-fill" size="md" />` |
| Loader | `@servicenow/now-loader` | `<now-loader label="Loading" />` |
| Alert | `@servicenow/now-alert` | `<now-alert status="info" header="Note" />` |
| Card | `@servicenow/now-card` | `<now-card size="md" />` |
| Tabs | `@servicenow/now-tabs` | `<now-tabs items={tabs} selected={0} />` |
| Toggle | `@servicenow/now-toggle` | `<now-toggle checked={on} />` |
| Textarea | `@servicenow/now-textarea` | `<now-textarea value={v} rows={5} />` |
| Rich Text | `@servicenow/now-rich-text` | `<now-rich-text html={content} />` |

### Button Variants

`primary`, `secondary`, `tertiary`, `tertiary-destructive`, `bare`, `bare-destructive`, `inherited`

## File Structure

Standard project layout after `snc ui-component create`:

```
x-company-my-component/
├── src/
│   └── x-company-my-component/
│       ├── index.js              # Main component (createCustomElement)
│       ├── __tests__/
│       │   └── index.test.js     # Unit tests
│       └── styles.scss           # Optional external styles
├── now-ui.json                   # Component metadata for UI Builder
├── now-cli.json                  # CLI and proxy configuration
├── package.json
└── README.md
```

### Separation of Concerns (Large Components)

```
src/x-company-my-component/
├── index.js              # createCustomElement registration
├── view.js               # View function
├── actionHandlers.js     # Action handlers
├── constants.js          # Action type constants
├── styles.scss           # Styles
└── __tests__/
    └── index.test.js
```

**index.js:**
```javascript
import { createCustomElement } from '@servicenow/ui-core';
import { view } from './view';
import { actionHandlers } from './actionHandlers';
import styles from './styles.scss';

createCustomElement('x-company-my-component', {
  view,
  initialState: { items: [], loading: false, error: null },
  properties: { title: { default: '', schema: { type: 'string' } } },
  actionHandlers,
  styles
});
```

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Component tag | kebab-case, `x-company-` prefix | `x-mobiz-task-list` |
| Action types | UPPER_SNAKE_CASE | `FETCH_DATA`, `USER_SELECTED` |
| State keys | camelCase | `isLoading`, `selectedItem` |
| Property names | camelCase | `userId`, `maxItems` |
| CSS classes | kebab-case | `.task-list`, `.item-card` |
| Files | kebab-case | `action-handlers.js` |

## Complete Example: Task List Component

```javascript
import { createCustomElement, actionTypes } from '@servicenow/ui-core';
import { createHttpEffect } from '@servicenow/ui-effect-http';
import '@servicenow/now-button';
import '@servicenow/now-input';
import '@servicenow/now-loader';

const TASKS_FETCHED = 'TASKS_FETCHED';
const TASKS_FETCH_FAILED = 'TASKS_FETCH_FAILED';
const TASK_CREATED = 'TASK_CREATED';

createCustomElement('x-company-task-list', {
  view: (state, { updateState, dispatch }) => {
    const { tasks, loading, error, newTaskName } = state;

    if (loading) return <now-loader label="Loading tasks..." />;
    if (error) return <div className="error">{error}</div>;

    return (
      <div className="task-list">
        <h2>Tasks ({tasks.length})</h2>
        <div className="add-task">
          <now-input value={newTaskName} placeholder="New task name"
            on-input={(e) => updateState({ newTaskName: e.target.value })} />
          <now-button label="Add" variant="primary"
            disabled={!newTaskName.trim()}
            on-click={() => dispatch('CREATE_TASK')} />
        </div>
        <ul>
          {tasks.map(task => (
            <li key={task.sys_id} className={task.active ? 'active' : 'done'}>
              <span>{task.short_description}</span>
              <now-button label="Delete" variant="tertiary-destructive" size="sm"
                on-click={() => dispatch('DELETE_TASK', { id: task.sys_id })} />
            </li>
          ))}
        </ul>
      </div>
    );
  },

  initialState: {
    tasks: [],
    loading: false,
    error: null,
    newTaskName: ''
  },

  properties: {
    tableName: { default: 'task', schema: { type: 'string' } },
    limit: { default: 20, schema: { type: 'integer' } }
  },

  actionHandlers: {
    [actionTypes.COMPONENT_BOOTSTRAPPED]: ({ dispatch }) => {
      dispatch('FETCH_TASKS');
    },

    FETCH_TASKS: createHttpEffect('/api/now/table/{{tableName}}', {
      method: 'GET',
      pathParams: [{ name: 'tableName', value: 'tableName' }],
      queryParams: [
        { name: 'sysparm_limit', value: 'limit' },
        { name: 'sysparm_query', value: 'active=true' }
      ],
      successActionType: TASKS_FETCHED,
      errorActionType: TASKS_FETCH_FAILED,
      startActionType: () => ({ loading: true })
    }),

    [TASKS_FETCHED]: ({ action, updateState }) => {
      updateState({ tasks: action.payload.result, loading: false });
    },

    [TASKS_FETCH_FAILED]: ({ action, updateState }) => {
      updateState({ error: 'Failed to load tasks', loading: false });
    },

    CREATE_TASK: ({ state, updateState, dispatch }) => {
      if (!state.newTaskName.trim()) return;
      updateState({ loading: true });
      fetch('/api/now/table/' + state.properties.tableName, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ short_description: state.newTaskName })
      })
        .then(res => res.json())
        .then(() => {
          updateState({ newTaskName: '' });
          dispatch('FETCH_TASKS');
        })
        .catch(err => updateState({ error: err.message, loading: false }));
    },

    DELETE_TASK: ({ action, state, updateState, dispatch }) => {
      fetch('/api/now/table/' + state.properties.tableName + '/' + action.payload.id, {
        method: 'DELETE'
      })
        .then(() => dispatch('FETCH_TASKS'))
        .catch(err => updateState({ error: err.message }));
    }
  },

  styles: `
    .task-list { padding: 16px; }
    .add-task { display: flex; gap: 8px; margin-bottom: 16px; }
    ul { list-style: none; padding: 0; }
    li { display: flex; justify-content: space-between; align-items: center;
         padding: 8px; border-bottom: 1px solid #e0e0e0; }
    .done span { text-decoration: line-through; color: #888; }
    .error { color: red; padding: 16px; }
  `
});
```

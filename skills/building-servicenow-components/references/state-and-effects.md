# State Management and HTTP Effects Reference

## Contents

- [Immutable State Updates](#immutable-state-updates)
- [Nested State Updates](#nested-state-updates)
- [Array Operations](#array-operations)
- [Common State Patterns](#common-state-patterns)
- [HTTP Effects with createHttpEffect](#http-effects-with-createhttpeffect)
- [createHttpEffect API](#createhttpeffect-api)
- [Action Dispatch Patterns](#action-dispatch-patterns)
- [Action Bubbling](#action-bubbling)

## Immutable State Updates

`updateState()` performs a **shallow merge** (like React's `setState` for class components). Never mutate state directly.

```javascript
// CORRECT - shallow merge
updateState({ loading: true });
updateState({ items: newItems, loading: false });

// WRONG - direct mutation
state.loading = true;         // Will NOT trigger re-render
state.items.push(newItem);    // Will NOT trigger re-render
```

### How Shallow Merge Works

```javascript
// State before: { a: 1, b: 2, c: 3 }
updateState({ b: 20 });
// State after:  { a: 1, b: 20, c: 3 }
```

Only top-level keys are merged. Nested objects are **replaced**, not deep-merged:

```javascript
// State before: { user: { name: 'John', age: 30, role: 'admin' } }
updateState({ user: { name: 'Jane' } });
// State after:  { user: { name: 'Jane' } }  -- age and role are LOST!
```

## Nested State Updates

Always spread to preserve nested fields:

```javascript
// Update one field in a nested object
updateState({
  user: { ...state.user, name: 'Jane' }
});
// Result: { user: { name: 'Jane', age: 30, role: 'admin' } }

// Two levels deep
updateState({
  settings: {
    ...state.settings,
    display: {
      ...state.settings.display,
      theme: 'dark'
    }
  }
});

// Update formData field
updateState({
  formData: { ...state.formData, email: newEmail }
});
```

## Array Operations

### Add Item

```javascript
updateState({
  items: [...state.items, newItem]
});

// Add at beginning
updateState({
  items: [newItem, ...state.items]
});

// Add at index
updateState({
  items: [
    ...state.items.slice(0, index),
    newItem,
    ...state.items.slice(index)
  ]
});
```

### Remove Item

```javascript
updateState({
  items: state.items.filter(item => item.sys_id !== idToRemove)
});
```

### Update Item in Array

```javascript
updateState({
  items: state.items.map(item =>
    item.sys_id === targetId
      ? { ...item, name: 'Updated Name' }
      : item
  )
});
```

### Sort Array

```javascript
updateState({
  items: [...state.items].sort((a, b) => a.name.localeCompare(b.name))
});
```

### Toggle Item

```javascript
updateState({
  items: state.items.map(item =>
    item.sys_id === targetId
      ? { ...item, selected: !item.selected }
      : item
  )
});
```

## Common State Patterns

### Loading / Error / Data Pattern

```javascript
initialState: {
  data: null,
  loading: false,
  error: null
}

// In action handlers:
FETCH_START: ({ updateState }) => {
  updateState({ loading: true, error: null });
},
FETCH_SUCCESS: ({ action, updateState }) => {
  updateState({ data: action.payload.result, loading: false });
},
FETCH_ERROR: ({ action, updateState }) => {
  updateState({ error: action.payload.message, loading: false });
}
```

### Pagination Pattern

```javascript
initialState: {
  items: [],
  page: 1,
  pageSize: 20,
  total: 0,
  loading: false
}

// Next page
NEXT_PAGE: ({ state, updateState, dispatch }) => {
  const nextPage = state.page + 1;
  updateState({ page: nextPage });
  dispatch('FETCH_PAGE', { page: nextPage });
}
```

### Form Pattern

```javascript
initialState: {
  formData: { name: '', email: '', description: '' },
  errors: {},
  submitting: false,
  submitted: false
}

// Handlers:
FIELD_CHANGED: ({ action, state, updateState }) => {
  const { field, value } = action.payload;
  updateState({
    formData: { ...state.formData, [field]: value },
    errors: { ...state.errors, [field]: null }
  });
},
VALIDATE_AND_SUBMIT: ({ state, updateState, dispatch }) => {
  const errors = {};
  if (!state.formData.name) errors.name = 'Name is required';
  if (!state.formData.email) errors.email = 'Email is required';

  if (Object.keys(errors).length > 0) {
    updateState({ errors });
    return;
  }
  updateState({ submitting: true, errors: {} });
  dispatch('SUBMIT_FORM');
}
```

### Multi-Selection Pattern

```javascript
initialState: {
  items: [],
  selectedIds: new Set()
}

TOGGLE_SELECTION: ({ action, state, updateState }) => {
  const id = action.payload.id;
  const selected = new Set(state.selectedIds);
  if (selected.has(id)) {
    selected.delete(id);
  } else {
    selected.add(id);
  }
  updateState({ selectedIds: selected });
},
SELECT_ALL: ({ state, updateState }) => {
  updateState({
    selectedIds: new Set(state.items.map(i => i.sys_id))
  });
},
CLEAR_SELECTION: ({ updateState }) => {
  updateState({ selectedIds: new Set() });
}
```

## HTTP Effects with createHttpEffect

`createHttpEffect` from `@servicenow/ui-effect-http` is the recommended way to make HTTP requests in ServiceNow components.

### Setup

```bash
npm install @servicenow/ui-effect-http -E
```

```javascript
import { createHttpEffect } from '@servicenow/ui-effect-http';
```

### Basic GET Request

```javascript
const INCIDENTS_FETCHED = 'INCIDENTS_FETCHED';
const INCIDENTS_FETCH_FAILED = 'INCIDENTS_FETCH_FAILED';

actionHandlers: {
  [actionTypes.COMPONENT_BOOTSTRAPPED]: ({ dispatch }) => {
    dispatch('FETCH_INCIDENTS');
  },

  FETCH_INCIDENTS: createHttpEffect('/api/now/table/incident', {
    method: 'GET',
    queryParams: [
      { name: 'sysparm_limit', value: 20 },
      { name: 'sysparm_query', value: 'active=true^ORDERBYDESCsys_created_on' },
      { name: 'sysparm_fields', value: 'sys_id,number,short_description,priority' }
    ],
    successActionType: INCIDENTS_FETCHED,
    errorActionType: INCIDENTS_FETCH_FAILED
  }),

  [INCIDENTS_FETCHED]: ({ action, updateState }) => {
    updateState({ incidents: action.payload.result, loading: false });
  },

  [INCIDENTS_FETCH_FAILED]: ({ action, updateState }) => {
    updateState({ error: 'Failed to load incidents', loading: false });
  }
}
```

### POST Request (Create Record)

```javascript
const RECORD_CREATED = 'RECORD_CREATED';
const RECORD_CREATE_FAILED = 'RECORD_CREATE_FAILED';

CREATE_RECORD: createHttpEffect('/api/now/table/incident', {
  method: 'POST',
  dataParam: 'record',
  successActionType: RECORD_CREATED,
  errorActionType: RECORD_CREATE_FAILED
})

// Dispatch with data:
dispatch('CREATE_RECORD', {
  record: {
    short_description: 'New incident',
    priority: 3,
    category: 'software'
  }
});
```

### PUT Request (Update Record)

```javascript
UPDATE_RECORD: createHttpEffect('/api/now/table/incident/{{sysId}}', {
  method: 'PUT',
  pathParams: [{ name: 'sysId', value: 'sysId' }],
  dataParam: 'record',
  successActionType: 'RECORD_UPDATED',
  errorActionType: 'RECORD_UPDATE_FAILED'
})

// Dispatch:
dispatch('UPDATE_RECORD', {
  sysId: 'abc123',
  record: { priority: 1 }
});
```

### DELETE Request

```javascript
DELETE_RECORD: createHttpEffect('/api/now/table/incident/{{sysId}}', {
  method: 'DELETE',
  pathParams: [{ name: 'sysId', value: 'sysId' }],
  successActionType: 'RECORD_DELETED',
  errorActionType: 'RECORD_DELETE_FAILED'
})
```

### Dynamic URL with Path Parameters

```javascript
FETCH_RECORD: createHttpEffect('/api/now/table/{{tableName}}/{{sysId}}', {
  method: 'GET',
  pathParams: [
    { name: 'tableName', value: 'tableName' },
    { name: 'sysId', value: 'sysId' }
  ],
  successActionType: 'RECORD_FETCHED',
  errorActionType: 'RECORD_FETCH_FAILED'
})

// Dispatch:
dispatch('FETCH_RECORD', { tableName: 'incident', sysId: 'abc123' });
```

## createHttpEffect API

```javascript
createHttpEffect(url, options)
```

| Option | Type | Description |
|--------|------|-------------|
| `method` | string | HTTP method: `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| `headers` | object | Custom HTTP headers |
| `queryParams` | array | `[{ name, value }]` - URL query parameters |
| `pathParams` | array | `[{ name, value }]` - URL path `{{param}}` replacements |
| `dataParam` | string | Action payload key to use as request body |
| `batch` | boolean | Enable request batching (default: true) |
| `successActionType` | string | Action type dispatched on success |
| `errorActionType` | string | Action type dispatched on error |
| `startActionType` | string | Action type dispatched when request starts |

### Success Action Payload

The success action's `payload` contains the parsed JSON response body. For ServiceNow Table API:

```javascript
action.payload = {
  result: [...] // Array of records (GET list) or single record (GET by id)
}
```

### Error Action Payload

```javascript
action.payload = {
  status: 401,
  message: 'Unauthorized',
  error: { ... }
}
```

## Action Dispatch Patterns

### From View

```javascript
view: (state, { dispatch }) => (
  <now-button label="Save" on-click={() => dispatch('SAVE_CLICKED', { id: 123 })} />
)
```

### From Action Handler (Chaining)

```javascript
actionHandlers: {
  SAVE_CLICKED: ({ state, dispatch }) => {
    if (validate(state.formData)) {
      dispatch('SUBMIT_FORM', { data: state.formData });
    } else {
      dispatch('VALIDATION_FAILED');
    }
  }
}
```

### Dispatch Arguments

```javascript
dispatch(type, payload, meta, error)
```

| Arg | Type | Description |
|-----|------|-------------|
| `type` | string | Action type (UPPER_SNAKE_CASE) |
| `payload` | object | Data associated with the action |
| `meta` | object | Additional metadata |
| `error` | boolean | Whether this is an error action |

## Action Bubbling

Actions bubble up through the DOM hierarchy. Parent components can observe child actions:

```javascript
// Child component dispatches:
dispatch('ITEM_SELECTED', { id: item.sys_id });

// Parent component handles:
actionHandlers: {
  'ITEM_SELECTED': ({ action, updateState }) => {
    // Catches action from child component
    updateState({ selectedItemId: action.payload.id });
  }
}
```

Actions are **unidirectional** - they only bubble up. Parent-to-child communication uses properties.

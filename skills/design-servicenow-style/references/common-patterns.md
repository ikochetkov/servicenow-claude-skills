# Common UX Patterns — Framework-Specific Implementations

This reference covers the shared UX patterns used across ServiceNow and how to implement them in each framework. These patterns represent the expected behavior and layout that ServiceNow users are accustomed to.

## Table of Contents

1. [Form Patterns](#form-patterns)
2. [List / Table Patterns](#list-table-patterns)
3. [Card Patterns](#card-patterns)
4. [Modal & Dialog Patterns](#modal-dialog-patterns)
5. [Navigation Patterns](#navigation-patterns)
6. [Search Patterns](#search-patterns)
7. [Notification Patterns](#notification-patterns)
8. [Status & Priority Indicators](#status-priority)
9. [Empty States](#empty-states)
10. [Loading States](#loading-states)

---

## Form Patterns

ServiceNow forms follow a consistent layout that users expect. When building custom forms, match these patterns.

### Form Layout Rules

- **Label position**: Above the field (not inline or to the left)
- **Required indicator**: Red asterisk (*) before the label
- **Field width**: Full container width for single-column, 50% for two-column layouts
- **Field spacing**: 16px gap between fields
- **Section headers**: 20px semibold, with a subtle bottom border
- **Form actions**: Right-aligned at bottom, primary button rightmost

### Form Field Anatomy

```
┌─────────────────────────────────────┐
│  * Field Label                       │
│  ┌─────────────────────────────────┐ │
│  │ Placeholder text...              │ │
│  └─────────────────────────────────┘ │
│  Helper text or validation message   │
└─────────────────────────────────────┘
```

### Validation States

| State | Border Color | Icon | Message Color |
|-------|-------------|------|--------------|
| Default | `#d9d9d9` | None | — |
| Focus | `#0056b3` (2px) | None | — |
| Valid | `#2e8540` | Checkmark | `#2e8540` |
| Error | `#c8102e` | Alert | `#c8102e` |
| Disabled | `#e8e8e8` | None | `#949494` |
| Read-only | No border | None | `#1e1e1e` |

### Next Experience Form

```html
<!-- UI Builder form using now-* components -->
<div class="form-section">
  <h3 class="form-section__title">Caller Information</h3>

  <div class="form-row">
    <now-input label="Caller"
               required="true"
               placeholder="Search for a user..."
               size="md">
    </now-input>
  </div>

  <div class="form-row form-row--two-col">
    <now-select label="Category" required="true">
      <!-- options -->
    </now-select>
    <now-select label="Subcategory">
      <!-- options -->
    </now-select>
  </div>

  <div class="form-row">
    <now-textarea label="Description"
                  required="true"
                  size="md"
                  placeholder="Describe the issue...">
    </now-textarea>
  </div>
</div>
```

### Service Portal Form

```html
<!-- AngularJS form with Bootstrap -->
<form name="c.form" ng-submit="c.submit()" novalidate>
  <fieldset>
    <legend class="form-section-title">Caller Information</legend>

    <div class="form-group"
         ng-class="{'has-error': c.form.caller.$invalid && c.form.caller.$touched}">
      <label for="caller" class="control-label">
        <span class="text-danger">* </span>Caller
      </label>
      <input type="text"
             class="form-control"
             id="caller"
             name="caller"
             ng-model="c.data.caller"
             placeholder="Search for a user..."
             required>
      <span class="help-block"
            ng-show="c.form.caller.$invalid && c.form.caller.$touched">
        Caller is required
      </span>
    </div>

    <div class="row">
      <div class="col-sm-6">
        <div class="form-group">
          <label class="control-label">
            <span class="text-danger">* </span>Category
          </label>
          <select class="form-control" ng-model="c.data.category" required>
            <option ng-repeat="opt in c.data.categories" value="{{opt.value}}">
              {{opt.label}}
            </option>
          </select>
        </div>
      </div>
      <div class="col-sm-6">
        <div class="form-group">
          <label class="control-label">Subcategory</label>
          <select class="form-control" ng-model="c.data.subcategory">
            <option ng-repeat="opt in c.data.subcategories" value="{{opt.value}}">
              {{opt.label}}
            </option>
          </select>
        </div>
      </div>
    </div>
  </fieldset>

  <div class="form-actions text-right">
    <button type="button" class="btn btn-default" ng-click="c.cancel()">Cancel</button>
    <button type="submit" class="btn btn-primary" ng-disabled="c.form.$invalid">
      Submit
    </button>
  </div>
</form>
```

## List / Table Patterns

ServiceNow lists are the most frequently used UI pattern. They display records with sortable columns, filtering, and row actions.

### List Anatomy

```
┌──────────────────────────────────────────────────┐
│  Filter Bar                         [Actions ▼]  │
│  ┌─ Active filters: Category = Network ──[x]──┐ │
│  └────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────┤
│  □  Number ▲  │ Short Description │ Priority │ St│
├──────────────────────────────────────────────────┤
│  □  INC001    │ Network outage    │ ● P1     │ N │
│  □  INC002    │ Slow VPN          │ ● P2     │ I │
│  □  INC003    │ Email issue       │ ● P3     │ O │
├──────────────────────────────────────────────────┤
│  Showing 1-20 of 156  │  ◄ 1 2 3 4 ... 8 ►     │
└──────────────────────────────────────────────────┘
```

### List Styling Rules

- **Header row**: Light gray background (`#f4f4f4`), semibold text, sortable columns show arrow indicator
- **Row height**: 40-44px for standard density
- **Row hover**: Subtle highlight (`#f4f4f4` or `rgba(0,86,179,0.05)`)
- **Selected row**: Light blue background (`#e6f0fa`)
- **Alternating rows**: Optional zebra striping with very subtle gray
- **Priority indicators**: Colored dot or left border matching priority colors
- **Clickable rows**: Cursor pointer, entire row is clickable (not just the number field)
- **Pagination**: Bottom-right, showing range and page controls

## Card Patterns

Cards are used for dashboards, catalogs, and content summaries.

### Card Anatomy

```
┌──────────────────────────────┐
│  [Icon/Image]                │
│                              │
│  Card Title (semibold)       │
│  Description text that can   │
│  wrap to multiple lines...   │
│                              │
│  ┌────────────────────────┐  │
│  │ Meta info  │  Actions  │  │
│  └────────────────────────┘  │
└──────────────────────────────┘
```

### Card Styling

```css
/* Standard ServiceNow card */
.sn-card {
  background: var(--now-color_surface--primary, #fff);
  border: 1px solid var(--now-border-color--primary, #d9d9d9);
  border-radius: 4px;
  padding: 16px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
  transition: box-shadow 0.2s ease;
}

.sn-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.sn-card__title {
  font-size: 16px;
  font-weight: 600;
  color: #1e1e1e;
  margin-bottom: 8px;
}

.sn-card__description {
  font-size: 14px;
  color: #6b6b6b;
  line-height: 1.5;
}

.sn-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #e8e8e8;
}
```

### Card Grid Layouts

| Layout | Columns | Card Span | Use Case |
|--------|---------|-----------|----------|
| Dashboard | 3-4 | 3-4 col each | KPI cards, metrics |
| Catalog | 3 | 4 col each | Service catalog items |
| Featured | 2 | 6 col each | Highlighted content |
| Compact list | 1 | 12 col | Card as list item (horizontal) |

## Modal & Dialog Patterns

### Modal Rules

These rules are consistent across all ServiceNow frameworks:

1. **One modal at a time** — never stack modals on modals
2. **Center horizontally and vertically** in the viewport
3. **Backdrop overlay**: Semi-transparent dark (`rgba(0,0,0,0.5)`)
4. **Always include a close button** (X in top-right corner)
5. **Footer buttons**: Right-aligned, maximum 1 primary button
6. **Tab navigation**: Focus trapped within modal, Tab moves to first actionable element
7. **Escape key**: Closes the modal
8. **Return focus**: When modal closes, focus returns to the element that opened it

### Modal Sizes

| Size | Width | Use Case |
|------|-------|----------|
| Small | 400px | Confirmations, simple messages |
| Medium | 600px | Forms with a few fields |
| Large | 800px | Complex forms, data review |
| Full-screen | 90vw × 90vh | Multi-step wizards, large data sets |

### Confirmation Dialog Pattern

```
┌─────────────────────────────────────┐
│  Delete Record                   [X] │
├─────────────────────────────────────┤
│                                     │
│  Are you sure you want to delete    │
│  INC0012345? This cannot be undone. │
│                                     │
├─────────────────────────────────────┤
│              [Cancel]  [Delete]     │
└─────────────────────────────────────┘
```

- Title states the action clearly
- Body explains consequences
- Cancel is default/secondary, destructive action is primary with danger color

## Navigation Patterns

### Workspace Navigation (Next Experience)

- **Unified Nav Bar**: Fixed top, brand-colored chrome with app name, global search, notifications, user menu
- **Side Nav**: Collapsible left sidebar with module groups. ~256px open, 48px collapsed (icon-only)
- **Breadcrumbs**: Below the nav bar, showing page hierarchy
- **Tab navigation**: Within content area for record views (Details, Notes, Related Lists)

### Service Portal Navigation

- **Navbar**: Bootstrap navbar component with logo, menu items, search, user menu
- **Mega menu**: For complex navigation hierarchies (categories, subcategories)
- **Sidebar filters**: Left-side faceted navigation for catalog/knowledge base
- **Breadcrumbs**: Below navbar, especially in knowledge base and catalog views

## Search Patterns

### Search Bar Styling

- **Position**: Centered in navigation bar or prominently placed on landing pages
- **Width**: Minimum 300px, can expand to 600px on focus
- **Height**: 40-44px (matching input field height)
- **Placeholder**: "Search" or contextual ("Search incidents...", "How can we help?")
- **Icon**: Magnifying glass on the left side
- **Autocomplete**: Dropdown suggestions appear below as user types

### Search Results

- Display results grouped by source/type
- Show result count prominently
- Highlight matched text in results
- Include faceted filters for refinement
- Paginate or infinite-scroll for large result sets

## Notification Patterns

### Types & Colors

| Type | Color | Icon | Use Case |
|------|-------|------|----------|
| Info | `#0070d2` (blue) | Info circle | General information |
| Success | `#2e8540` (green) | Checkmark | Action completed |
| Warning | `#eeb422` (yellow) | Warning triangle | Caution needed |
| Error | `#c8102e` (red) | Error circle | Action failed |

### Notification Placement

- **Banner (top)**: Full-width, below nav bar. For system-wide announcements.
- **Toast (top-right)**: Slide-in, auto-dismiss after 5s. For action confirmations.
- **Inline**: Within form/content area. For field-level or section-level feedback.
- **Badge**: On icons/nav items. For unread counts.

### Toast Notification Structure

```
┌──────────────────────────────────┐
│  ● Success                    [X] │
│  Record INC0012345 has been       │
│  updated successfully.            │
└──────────────────────────────────┘
```

## Status & Priority Indicators

### Visual Indicators

ServiceNow users are trained to recognize status by color. Always pair color with another indicator (icon, text, or shape) for accessibility.

**Priority dots**: Small filled circle (8px) in the priority color, placed before the priority label.

**State badges**: Rounded pill with light background and darker text:

```css
.state-badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 10px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 600;
}

.state-badge--new       { background: #e6f0fa; color: #0056b3; }
.state-badge--active    { background: #e6f5ea; color: #2e8540; }
.state-badge--pending   { background: #fff4e0; color: #b87200; }
.state-badge--resolved  { background: #e8e8e8; color: #6b6b6b; }
.state-badge--closed    { background: #f4f4f4; color: #949494; }
```

**Severity bars**: Colored left border (4px) on list items or cards.

## Empty States

When no data is available, show a helpful empty state:

```
┌─────────────────────────────────────┐
│                                     │
│         [Illustration/Icon]         │
│                                     │
│       No incidents found            │
│                                     │
│   There are no active incidents     │
│   matching your filters.            │
│                                     │
│       [Clear Filters]               │
│                                     │
└─────────────────────────────────────┘
```

- Center the content vertically and horizontally
- Use a relevant icon (32px) or simple illustration
- Title in 20px semibold
- Description in 14px secondary color
- Optional action button to resolve the empty state

## Loading States

### Skeleton Screens (Preferred)

ServiceNow uses skeleton screens for initial page loads — gray placeholder shapes that match the expected layout:

```css
.skeleton {
  background: linear-gradient(90deg, #e8e8e8 25%, #f4f4f4 50%, #e8e8e8 75%);
  background-size: 200% 100%;
  animation: skeleton-pulse 1.5s ease-in-out infinite;
  border-radius: 4px;
}

@keyframes skeleton-pulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton--text { height: 14px; width: 80%; margin-bottom: 8px; }
.skeleton--heading { height: 24px; width: 40%; margin-bottom: 16px; }
.skeleton--avatar { height: 32px; width: 32px; border-radius: 50%; }
.skeleton--button { height: 36px; width: 120px; }
```

### Spinner (Secondary)

Use spinner for in-place updates (refresh button, form submission):

```css
.sn-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #e8e8e8;
  border-top-color: #0056b3;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

### Loading Best Practices

- Prefer skeleton screens for initial page/section loads
- Use spinner for action-triggered updates (button clicks, refreshes)
- Show loading state immediately — don't wait for a delay threshold
- Disable action buttons during submission to prevent double-clicks
- For long operations (>3s), show progress text ("Loading incidents..." not just a spinner)

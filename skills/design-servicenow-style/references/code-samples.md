# Code Samples — Ready-to-Use Templates

Copy-paste starter templates for building ServiceNow-styled components and pages. Each template includes proper design tokens, accessibility, and follows ServiceNow conventions.

## Table of Contents

1. [CSS Reset / Base Styles](#css-reset)
2. [Next Experience: Custom Component Template](#next-experience-component)
3. [Next Experience: Dashboard Page](#next-experience-dashboard)
4. [Next Experience: Record Form Page](#next-experience-form)
5. [Service Portal: Widget Template](#service-portal-widget)
6. [Service Portal: Catalog Card Grid](#service-portal-catalog)
7. [Standalone SPA: ServiceNow-Styled App Shell](#standalone-spa)
8. [Standalone SPA: Data Table Component](#standalone-data-table)
9. [Utility Classes](#utility-classes)

---

## CSS Reset

Base styles to establish ServiceNow visual language in any project:

```css
/* ServiceNow Design System Reset */
:root {
  /* Brand */
  --sn-brand-dark: #243c3e;
  --sn-brand-light: #82b6a2;

  /* Interactive */
  --sn-interactive: #0056b3;
  --sn-interactive-hover: #00438a;
  --sn-interactive-active: #003267;

  /* Chrome */
  --sn-chrome-bg: #30302f;
  --sn-chrome-text: #ffffff;

  /* Surfaces */
  --sn-surface-primary: #ffffff;
  --sn-surface-secondary: #f4f4f4;
  --sn-surface-tertiary: #e8e8e8;

  /* Text */
  --sn-text-primary: #1e1e1e;
  --sn-text-secondary: #6b6b6b;
  --sn-text-tertiary: #949494;
  --sn-text-inverse: #ffffff;

  /* Status */
  --sn-critical: #c8102e;
  --sn-high: #e86e2c;
  --sn-moderate: #eeb422;
  --sn-success: #2e8540;
  --sn-info: #0070d2;

  /* Borders */
  --sn-border-primary: #d9d9d9;
  --sn-border-secondary: #e8e8e8;

  /* Spacing */
  --sn-space-xs: 4px;
  --sn-space-sm: 8px;
  --sn-space-md: 16px;
  --sn-space-lg: 24px;
  --sn-space-xl: 32px;
  --sn-space-2xl: 48px;

  /* Typography */
  --sn-font-heading: 'Cabin', Arial, 'Helvetica Neue', sans-serif;
  --sn-font-body: 'Lato', Arial, 'Helvetica Neue', sans-serif;
  --sn-font-mono: 'Source Code Pro', 'Courier New', monospace;

  /* Shadows */
  --sn-shadow-low: 0 1px 2px rgba(0,0,0,0.1);
  --sn-shadow-medium: 0 2px 8px rgba(0,0,0,0.15);
  --sn-shadow-high: 0 4px 16px rgba(0,0,0,0.2);

  /* Radius */
  --sn-radius-sm: 4px;
  --sn-radius-md: 8px;
  --sn-radius-full: 9999px;

  /* Focus */
  --sn-focus-ring: 0 0 0 2px var(--sn-interactive);
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: var(--sn-font-body);
  font-size: 16px;
  line-height: 1.5;
  color: var(--sn-text-primary);
  background-color: var(--sn-surface-secondary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--sn-font-heading);
  font-weight: 600;
  margin-top: 0;
  color: var(--sn-text-primary);
}

h1 { font-size: 32px; line-height: 1.25; }
h2 { font-size: 24px; line-height: 1.3; }
h3 { font-size: 20px; line-height: 1.4; }
h4 { font-size: 16px; line-height: 1.5; }

a {
  color: var(--sn-interactive);
  text-decoration: none;
}
a:hover {
  color: var(--sn-interactive-hover);
  text-decoration: underline;
}

/* Focus visible for keyboard navigation */
:focus-visible {
  outline: 2px solid var(--sn-interactive);
  outline-offset: 2px;
  border-radius: var(--sn-radius-sm);
}
```

## Next Experience: Custom Component Template

Complete boilerplate for a UI Builder custom component:

```javascript
// index.js — Component entry point
import { createCustomElement } from '@servicenow/ui-core';
import snabbdom from '@servicenow/ui-renderer-snabbdom';
import styles from './styles.scss';
import { actionTypes } from './actions';

const view = (state, { updateState, dispatch }) => {
  const { properties, loading, error, items } = state;

  return (
    <div className="x-ticket-summary">
      {/* Header */}
      <div className="x-ticket-summary__header">
        <h3 className="x-ticket-summary__title">{properties.title}</h3>
        <button
          className="x-ticket-summary__refresh"
          on-click={() => dispatch(actionTypes.REFRESH)}
          aria-label="Refresh ticket list"
        >
          <now-icon icon="reload-outline" size="md" />
        </button>
      </div>

      {/* Content */}
      <div className="x-ticket-summary__body">
        {loading && (
          <div className="x-ticket-summary__skeleton">
            <div className="skeleton skeleton--text"></div>
            <div className="skeleton skeleton--text"></div>
            <div className="skeleton skeleton--text"></div>
          </div>
        )}

        {error && (
          <div className="x-ticket-summary__error" role="alert">
            <now-icon icon="circle-exclamation-outline" size="md" />
            <span>{error}</span>
          </div>
        )}

        {!loading && !error && items.length === 0 && (
          <div className="x-ticket-summary__empty">
            <now-icon icon="document-outline" size="xl" />
            <p>No tickets found</p>
          </div>
        )}

        {!loading && items.map(item => (
          <div
            className={`x-ticket-summary__item x-ticket-summary__item--p${item.priority}`}
            key={item.sys_id}
            role="button"
            tabIndex="0"
            on-click={() => dispatch(actionTypes.NAVIGATE, { sys_id: item.sys_id })}
            on-keydown={(e) => e.key === 'Enter' && dispatch(actionTypes.NAVIGATE, { sys_id: item.sys_id })}
          >
            <span className="x-ticket-summary__number">{item.number}</span>
            <span className="x-ticket-summary__desc">{item.short_description}</span>
            <now-badge
              label={item.priority_label}
              color={getPriorityColor(item.priority)}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

function getPriorityColor(priority) {
  const colors = { 1: 'critical', 2: 'high', 3: 'warning', 4: 'positive', 5: 'info' };
  return colors[priority] || 'neutral';
}

createCustomElement('x-ticket-summary', {
  renderer: { type: snabbdom },
  view,
  styles,
  properties: {
    title: { default: 'Open Tickets' },
    table: { default: 'incident' },
    limit: { default: 10 }
  },
  initialState: {
    loading: true,
    error: null,
    items: []
  }
});
```

```scss
// styles.scss — Component styles
@import '@servicenow/sass-kit/host';

:host {
  display: block;
  font-family: var(--now-font-family--body, 'Lato', Arial, sans-serif);
}

.x-ticket-summary {
  background: var(--now-color_surface--primary, #fff);
  border: 1px solid var(--now-border-color--primary, #d9d9d9);
  border-radius: var(--now-border-radius--sm, 4px);
  overflow: hidden;

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--now-spacing--sm, 8px) var(--now-spacing--md, 16px);
    border-bottom: 1px solid var(--now-border-color--secondary, #e8e8e8);
    background: var(--now-color_surface--secondary, #f4f4f4);
  }

  &__title {
    font-family: var(--now-font-family--heading, 'Cabin', Arial, sans-serif);
    font-size: var(--now-font-size--lg, 20px);
    font-weight: var(--now-font-weight--semibold, 600);
    color: var(--now-color_text--primary, #1e1e1e);
    margin: 0;
  }

  &__refresh {
    background: none;
    border: none;
    padding: var(--now-spacing--xs, 4px);
    cursor: pointer;
    border-radius: var(--now-border-radius--sm, 4px);
    color: var(--now-color_text--secondary, #6b6b6b);

    &:hover {
      background: var(--now-color_surface--tertiary, #e8e8e8);
      color: var(--now-color_text--primary, #1e1e1e);
    }

    &:focus-visible {
      outline: 2px solid var(--now-color_focus--ring, #0056b3);
      outline-offset: 2px;
    }
  }

  &__body {
    max-height: 400px;
    overflow-y: auto;
  }

  &__item {
    display: flex;
    align-items: center;
    gap: var(--now-spacing--sm, 8px);
    padding: var(--now-spacing--sm, 8px) var(--now-spacing--md, 16px);
    border-bottom: 1px solid var(--now-border-color--secondary, #e8e8e8);
    cursor: pointer;
    transition: background-color 0.15s ease;

    &:hover {
      background: rgba(0, 86, 179, 0.04);
    }

    &:focus-visible {
      outline: 2px solid var(--now-color_focus--ring, #0056b3);
      outline-offset: -2px;
    }

    &:last-child {
      border-bottom: none;
    }

    &--p1 { border-left: 4px solid var(--now-color_alert--critical, #c8102e); }
    &--p2 { border-left: 4px solid var(--now-color_alert--high, #e86e2c); }
    &--p3 { border-left: 4px solid var(--now-color_alert--warning, #eeb422); }
    &--p4 { border-left: 4px solid var(--now-color_alert--positive, #2e8540); }
  }

  &__number {
    font-size: var(--now-font-size--sm, 14px);
    font-weight: var(--now-font-weight--semibold, 600);
    color: var(--now-color_interactive--primary, #0056b3);
    min-width: 90px;
    flex-shrink: 0;
  }

  &__desc {
    flex: 1;
    font-size: var(--now-font-size--sm, 14px);
    color: var(--now-color_text--primary, #1e1e1e);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  &__empty,
  &__error {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: var(--now-spacing--xl, 32px);
    color: var(--now-color_text--secondary, #6b6b6b);
    gap: var(--now-spacing--sm, 8px);
  }

  &__error {
    color: var(--now-color_alert--critical, #c8102e);
    flex-direction: row;
    padding: var(--now-spacing--md, 16px);
  }
}

/* Skeleton loading */
.skeleton {
  background: linear-gradient(90deg, #e8e8e8 25%, #f4f4f4 50%, #e8e8e8 75%);
  background-size: 200% 100%;
  animation: skeleton-pulse 1.5s ease-in-out infinite;
  border-radius: var(--now-border-radius--sm, 4px);

  &--text {
    height: 14px;
    margin: 12px 16px;

    &:nth-child(1) { width: 80%; }
    &:nth-child(2) { width: 60%; }
    &:nth-child(3) { width: 70%; }
  }
}

@keyframes skeleton-pulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

## Service Portal: Widget Template

Complete widget boilerplate for Service Portal:

```html
<!-- HTML Template -->
<div class="sp-ticket-list">
  <!-- Header -->
  <div class="sp-ticket-list__header">
    <h3 class="sp-ticket-list__title">{{c.data.title}}</h3>
    <button class="btn btn-default btn-sm"
            ng-click="c.refresh()"
            ng-disabled="c.loading"
            aria-label="Refresh list">
      <i class="fa fa-refresh" ng-class="{'fa-spin': c.loading}"></i>
      Refresh
    </button>
  </div>

  <!-- Content -->
  <div class="sp-ticket-list__body">
    <!-- Loading -->
    <div ng-if="c.loading" class="sp-ticket-list__loading">
      <i class="fa fa-spinner fa-spin fa-2x"></i>
      <span>Loading tickets...</span>
    </div>

    <!-- Empty state -->
    <div ng-if="!c.loading && c.data.tickets.length === 0"
         class="sp-ticket-list__empty">
      <i class="fa fa-inbox fa-3x"></i>
      <h4>No tickets found</h4>
      <p>There are no open tickets matching your criteria.</p>
    </div>

    <!-- Ticket list -->
    <div ng-if="!c.loading && c.data.tickets.length > 0">
      <div class="sp-ticket-list__item"
           ng-repeat="ticket in c.data.tickets"
           ng-class="'sp-ticket-list__item--p' + ticket.priority"
           ng-click="c.openRecord(ticket)"
           ng-keydown="$event.keyCode === 13 && c.openRecord(ticket)"
           tabindex="0"
           role="button"
           aria-label="Open {{ticket.number}}: {{ticket.short_description}}">
        <span class="sp-ticket-list__number">{{ticket.number}}</span>
        <span class="sp-ticket-list__desc">{{ticket.short_description}}</span>
        <span class="sp-ticket-list__priority priority-badge priority-badge--{{ticket.priority}}">
          {{ticket.priority_label}}
        </span>
        <span class="sp-ticket-list__state state-badge state-badge--{{ticket.state_value}}">
          {{ticket.state}}
        </span>
      </div>
    </div>
  </div>

  <!-- Pagination -->
  <div class="sp-ticket-list__footer" ng-if="c.data.total > c.data.limit">
    <span class="sp-ticket-list__count">
      Showing {{c.data.offset + 1}}-{{Math.min(c.data.offset + c.data.limit, c.data.total)}}
      of {{c.data.total}}
    </span>
    <nav aria-label="Ticket list pagination">
      <ul class="pagination pagination-sm">
        <li ng-class="{disabled: c.data.offset === 0}">
          <a ng-click="c.prevPage()" aria-label="Previous page">&laquo;</a>
        </li>
        <li ng-repeat="page in c.pages" ng-class="{active: page === c.currentPage}">
          <a ng-click="c.goToPage(page)">{{page}}</a>
        </li>
        <li ng-class="{disabled: c.data.offset + c.data.limit >= c.data.total}">
          <a ng-click="c.nextPage()" aria-label="Next page">&raquo;</a>
        </li>
      </ul>
    </nav>
  </div>
</div>
```

```scss
/* Widget SCSS */
$sp-ticket-bg: $color-white !default;
$sp-ticket-border: $color-light !default;
$sp-ticket-hover: $color-lightest !default;
$sp-ticket-header-bg: $color-lightest !default;

.sp-ticket-list {
  background: $sp-ticket-bg;
  border: 1px solid $sp-ticket-border;
  border-radius: $border-radius-base;
  overflow: hidden;

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 16px;
    background: $sp-ticket-header-bg;
    border-bottom: 1px solid $sp-ticket-border;
  }

  &__title {
    font-size: 18px;
    font-weight: 600;
    color: $color-darkest;
    margin: 0;
  }

  &__body {
    max-height: 400px;
    overflow-y: auto;
  }

  &__item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    border-bottom: 1px solid $color-lighter;
    cursor: pointer;
    transition: background-color 0.15s ease;

    &:hover, &:focus {
      background: $sp-ticket-hover;
    }

    &:focus {
      outline: 2px solid $brand-primary;
      outline-offset: -2px;
    }

    &:last-child {
      border-bottom: none;
    }

    &--p1 { border-left: 4px solid $brand-danger; }
    &--p2 { border-left: 4px solid $brand-warning; }
    &--p3 { border-left: 4px solid $brand-info; }
    &--p4 { border-left: 4px solid $brand-success; }
  }

  &__number {
    font-size: $font-size-small;
    font-weight: 600;
    color: $brand-primary;
    min-width: 90px;
    flex-shrink: 0;
  }

  &__desc {
    flex: 1;
    font-size: $font-size-base;
    color: $color-darkest;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  &__loading,
  &__empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 32px;
    color: $color-dark;
    gap: 8px;

    h4 { margin-top: 8px; }
    p { color: $color-medium; }
  }

  &__footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 16px;
    border-top: 1px solid $sp-ticket-border;
    background: $sp-ticket-header-bg;
  }

  &__count {
    font-size: $font-size-small;
    color: $color-dark;
  }
}

/* Priority badges */
.priority-badge {
  font-size: $font-size-small;
  padding: 2px 8px;
  border-radius: $border-radius-small;
  font-weight: 600;

  &--1 { background: lighten($brand-danger, 35%); color: $brand-danger; }
  &--2 { background: lighten($brand-warning, 30%); color: darken($brand-warning, 20%); }
  &--3 { background: lighten($brand-info, 40%); color: $brand-info; }
  &--4 { background: lighten($brand-success, 45%); color: $brand-success; }
}

/* State badges */
.state-badge {
  font-size: $font-size-small;
  padding: 2px 10px;
  border-radius: 16px;
  font-weight: 600;

  &--1 { background: #e6f0fa; color: #0056b3; } /* New */
  &--2 { background: #e6f5ea; color: #2e8540; } /* In Progress */
  &--3 { background: #fff4e0; color: #b87200; } /* On Hold */
  &--6 { background: #e8e8e8; color: #6b6b6b; } /* Resolved */
  &--7 { background: #f4f4f4; color: #949494; } /* Closed */
}
```

## Standalone SPA: ServiceNow-Styled App Shell

For building standalone apps that look like ServiceNow workspaces:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My App — ServiceNow Workspace</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Cabin:wght@400;600;700&family=Lato:wght@400;700&display=swap" rel="stylesheet">
  <style>
    /* Include CSS Reset from above, then add: */

    .app-shell {
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }

    /* Chrome / Navigation Bar */
    .chrome {
      display: flex;
      align-items: center;
      height: 48px;
      padding: 0 var(--sn-space-md);
      background: var(--sn-chrome-bg);
      color: var(--sn-chrome-text);
      flex-shrink: 0;
      z-index: 100;
    }

    .chrome__logo {
      font-family: var(--sn-font-heading);
      font-size: 18px;
      font-weight: 700;
      margin-right: var(--sn-space-lg);
    }

    .chrome__nav {
      display: flex;
      gap: var(--sn-space-md);
      flex: 1;
    }

    .chrome__link {
      color: rgba(255,255,255,0.8);
      text-decoration: none;
      font-size: 14px;
      padding: var(--sn-space-xs) var(--sn-space-sm);
      border-radius: var(--sn-radius-sm);
    }

    .chrome__link:hover,
    .chrome__link--active {
      color: #fff;
      background: rgba(255,255,255,0.1);
      text-decoration: none;
    }

    .chrome__search {
      display: flex;
      align-items: center;
      background: rgba(255,255,255,0.1);
      border-radius: var(--sn-radius-sm);
      padding: var(--sn-space-xs) var(--sn-space-sm);
      margin-left: auto;
    }

    .chrome__search input {
      background: none;
      border: none;
      color: #fff;
      font-size: 14px;
      outline: none;
      width: 200px;
    }

    .chrome__search input::placeholder {
      color: rgba(255,255,255,0.5);
    }

    /* Main Layout */
    .workspace {
      display: flex;
      flex: 1;
    }

    /* Side Navigation */
    .side-nav {
      width: 256px;
      background: var(--sn-surface-primary);
      border-right: 1px solid var(--sn-border-secondary);
      padding: var(--sn-space-md) 0;
      flex-shrink: 0;
      overflow-y: auto;
    }

    .side-nav__group-title {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--sn-text-tertiary);
      padding: var(--sn-space-sm) var(--sn-space-md);
      margin-top: var(--sn-space-sm);
    }

    .side-nav__item {
      display: flex;
      align-items: center;
      gap: var(--sn-space-sm);
      padding: var(--sn-space-sm) var(--sn-space-md);
      color: var(--sn-text-primary);
      text-decoration: none;
      font-size: 14px;
      border-left: 3px solid transparent;
      transition: all 0.15s ease;
    }

    .side-nav__item:hover {
      background: var(--sn-surface-secondary);
      text-decoration: none;
      color: var(--sn-text-primary);
    }

    .side-nav__item--active {
      background: rgba(0, 86, 179, 0.08);
      border-left-color: var(--sn-interactive);
      color: var(--sn-interactive);
      font-weight: 600;
    }

    /* Stage (Main Content) */
    .stage {
      flex: 1;
      padding: var(--sn-space-lg);
      overflow-y: auto;
      background: var(--sn-surface-secondary);
    }

    .stage__header {
      margin-bottom: var(--sn-space-lg);
    }

    .stage__title {
      font-size: 32px;
      margin-bottom: var(--sn-space-xs);
    }

    .stage__breadcrumbs {
      font-size: 14px;
      color: var(--sn-text-secondary);
    }

    .stage__breadcrumbs a {
      color: var(--sn-interactive);
    }

    /* Content Cards */
    .content-grid {
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: var(--sn-space-md);
    }

    .content-card {
      background: var(--sn-surface-primary);
      border: 1px solid var(--sn-border-primary);
      border-radius: var(--sn-radius-sm);
      padding: var(--sn-space-md);
      box-shadow: var(--sn-shadow-low);
    }

    .content-card--span-4 { grid-column: span 4; }
    .content-card--span-6 { grid-column: span 6; }
    .content-card--span-8 { grid-column: span 8; }
    .content-card--span-12 { grid-column: span 12; }

    .content-card__title {
      font-size: 16px;
      font-weight: 600;
      margin-bottom: var(--sn-space-sm);
    }
  </style>
</head>
<body>
  <div class="app-shell">
    <!-- Chrome -->
    <header class="chrome" role="banner">
      <div class="chrome__logo">My App</div>
      <nav class="chrome__nav" role="navigation" aria-label="Main navigation">
        <a href="#" class="chrome__link chrome__link--active">Home</a>
        <a href="#" class="chrome__link">Incidents</a>
        <a href="#" class="chrome__link">Changes</a>
        <a href="#" class="chrome__link">Reports</a>
      </nav>
      <div class="chrome__search">
        <input type="search" placeholder="Search..." aria-label="Search">
      </div>
    </header>

    <!-- Workspace -->
    <div class="workspace">
      <!-- Side Navigation -->
      <nav class="side-nav" aria-label="Module navigation">
        <div class="side-nav__group-title">Incident</div>
        <a href="#" class="side-nav__item side-nav__item--active">All Open</a>
        <a href="#" class="side-nav__item">Assigned to me</a>
        <a href="#" class="side-nav__item">Unassigned</a>
        <div class="side-nav__group-title">Reports</div>
        <a href="#" class="side-nav__item">Dashboard</a>
        <a href="#" class="side-nav__item">Trend Analysis</a>
      </nav>

      <!-- Stage -->
      <main class="stage" role="main">
        <div class="stage__header">
          <div class="stage__breadcrumbs">
            <a href="#">Home</a> / <a href="#">Incident</a> / All Open
          </div>
          <h1 class="stage__title">All Open Incidents</h1>
        </div>

        <div class="content-grid">
          <!-- Your content goes here -->
          <div class="content-card content-card--span-12">
            <div class="content-card__title">Incident List</div>
            <!-- Table/list component -->
          </div>
        </div>
      </main>
    </div>
  </div>
</body>
</html>
```

## Utility Classes

Commonly needed utility classes that match ServiceNow conventions:

```css
/* Text utilities */
.sn-text-primary { color: var(--sn-text-primary); }
.sn-text-secondary { color: var(--sn-text-secondary); }
.sn-text-tertiary { color: var(--sn-text-tertiary); }
.sn-text-critical { color: var(--sn-critical); }
.sn-text-success { color: var(--sn-success); }
.sn-text-info { color: var(--sn-info); }
.sn-text-warning { color: var(--sn-moderate); }

/* Background utilities */
.sn-bg-primary { background-color: var(--sn-surface-primary); }
.sn-bg-secondary { background-color: var(--sn-surface-secondary); }
.sn-bg-tertiary { background-color: var(--sn-surface-tertiary); }

/* Spacing utilities (padding) */
.sn-p-xs { padding: var(--sn-space-xs); }
.sn-p-sm { padding: var(--sn-space-sm); }
.sn-p-md { padding: var(--sn-space-md); }
.sn-p-lg { padding: var(--sn-space-lg); }
.sn-p-xl { padding: var(--sn-space-xl); }

/* Spacing utilities (margin) */
.sn-m-xs { margin: var(--sn-space-xs); }
.sn-m-sm { margin: var(--sn-space-sm); }
.sn-m-md { margin: var(--sn-space-md); }
.sn-m-lg { margin: var(--sn-space-lg); }
.sn-m-xl { margin: var(--sn-space-xl); }

/* Gap utilities */
.sn-gap-xs { gap: var(--sn-space-xs); }
.sn-gap-sm { gap: var(--sn-space-sm); }
.sn-gap-md { gap: var(--sn-space-md); }
.sn-gap-lg { gap: var(--sn-space-lg); }

/* Layout utilities */
.sn-flex { display: flex; }
.sn-flex-col { display: flex; flex-direction: column; }
.sn-flex-center { display: flex; align-items: center; }
.sn-flex-between { display: flex; justify-content: space-between; align-items: center; }
.sn-grid-12 { display: grid; grid-template-columns: repeat(12, 1fr); }

/* Truncation */
.sn-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Screen reader only */
.sn-sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Focus ring */
.sn-focusable:focus-visible {
  outline: 2px solid var(--sn-interactive);
  outline-offset: 2px;
  border-radius: var(--sn-radius-sm);
}
```

# Service Portal (AngularJS) — Detailed Reference

This reference covers the Service Portal framework used for customer-facing portals, self-service catalogs, knowledge bases, and employee-facing request centers. Service Portal is still widely deployed and actively used despite being a legacy framework.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [CSS Architecture & Scoping](#css-architecture)
3. [SCSS Variables](#scss-variables)
4. [Bootstrap 3 Foundation](#bootstrap-3)
5. [Widget CSS Patterns](#widget-css-patterns)
6. [Portal Theming](#portal-theming)
7. [Typography](#typography)
8. [Color System](#color-system)
9. [Layout & Grid](#layout-grid)
10. [Widget Development Best Practices](#widget-development)

---

## Architecture Overview

Service Portal uses:
- **AngularJS 1.x** — Client-side framework
- **Bootstrap 3** — Grid system and base components
- **SCSS/SASS** — CSS preprocessor with variable system
- **jQuery** — DOM manipulation (available but discouraged for new code)

Key difference from Next Experience: Service Portal does NOT use Web Components or Shadow DOM. Styles are global by default, making CSS scoping a critical concern.

## CSS Architecture

### Six Levels of CSS Application

Service Portal applies CSS in a cascading hierarchy. Understanding this hierarchy is essential for predictable styling:

```
1. Portal CSS Variables    ← Global SCSS variables ($brand-primary, etc.)
2. Theme CSS Variables     ← Theme-level SCSS overrides
3. Portal-wide Stylesheets ← Global CSS (use sparingly)
4. Page-specific CSS       ← Scoped to individual pages
5. Widget CSS              ← Scoped to widget via auto-prefixing
6. Widget Instance CSS     ← Override for specific widget instance
```

Each level can override the one above it. Widget CSS is automatically scoped by ServiceNow's build system — it prefixes selectors with the widget's unique class.

### CSS Scoping Rules

**Widget CSS is auto-scoped**: When you write CSS in a widget's CSS field, ServiceNow automatically wraps it with the widget's class selector. This means your widget styles won't leak to other widgets.

**Page CSS affects only that page**: Page-specific CSS is prefixed with the page's class/ID.

**Global CSS is dangerous**: CSS in the portal's global stylesheet applies everywhere. Only use for:
- Bootstrap overrides that apply across all widgets
- External library styling
- Custom layout utilities

**The Golden Rule**: "Code like a lion for widgets (be specific), code like a lamb for themes (minimize interference)."

## SCSS Variables

### Core Brand Variables

These SCSS variables are available in all widget CSS and can be set at the portal or theme level:

```scss
/* Primary brand colors */
$brand-primary: #0056b3 !default;         /* Primary actions, links */
$brand-success: #2e8540 !default;         /* Success states */
$brand-info: #0070d2 !default;            /* Informational */
$brand-warning: #eeb422 !default;         /* Warnings */
$brand-danger: #c8102e !default;          /* Errors, critical */

/* Neutral palette */
$color-darkest: #1e1e1e !default;         /* Primary text */
$color-darker: #444444 !default;          /* Secondary text */
$color-dark: #6b6b6b !default;            /* Captions */
$color-medium: #949494 !default;          /* Placeholders */
$color-light: #d9d9d9 !default;           /* Borders */
$color-lighter: #e8e8e8 !default;         /* Dividers */
$color-lightest: #f4f4f4 !default;        /* Card backgrounds */
$color-white: #ffffff !default;           /* Content background */

/* Typography */
$font-family-base: Arial, 'Helvetica Neue', Helvetica, sans-serif !default;
$font-size-base: 14px !default;           /* Service Portal default */
$font-size-large: 18px !default;
$font-size-small: 12px !default;
$line-height-base: 1.428571429 !default;  /* Bootstrap 3 default (~20/14) */

/* Link colors */
$link-color: $brand-primary !default;
$link-hover-color: darken($brand-primary, 15%) !default;

/* Grid */
$grid-gutter-width: 30px !default;        /* Bootstrap 3 default */

/* Border radius */
$border-radius-base: 4px !default;
$border-radius-large: 6px !default;
$border-radius-small: 3px !default;
```

### The `!default` Flag

Always use `!default` on SCSS variables in widgets. This lets theme-level and portal-level variables override widget defaults:

```scss
/* GOOD — allows theme override */
$my-widget-bg: $color-lightest !default;

/* BAD — hardcoded, ignores theme */
$my-widget-bg: #f4f4f4;
```

### Custom Widget Variables

When creating custom variables for your widgets, prefix them with the widget name to avoid collisions:

```scss
/* Prefix with widget context */
$ticket-card-header-bg: $brand-primary !default;
$ticket-card-border-color: $color-light !default;
$ticket-card-padding: 16px !default;
```

## Bootstrap 3

Service Portal ships with Bootstrap 3. This means:

### Grid Classes

```html
<!-- 12-column responsive grid -->
<div class="container">
  <div class="row">
    <div class="col-xs-12 col-sm-6 col-md-4 col-lg-3">
      <!-- Column content -->
    </div>
  </div>
</div>
```

| Prefix | Breakpoint | Target |
|--------|-----------|--------|
| `col-xs-*` | 0px+ | Phone |
| `col-sm-*` | 768px+ | Tablet |
| `col-md-*` | 992px+ | Desktop |
| `col-lg-*` | 1200px+ | Large desktop |

### Available Bootstrap Components

These Bootstrap 3 components are available and styled by the portal theme:

- `.btn`, `.btn-primary`, `.btn-default`, `.btn-success`, `.btn-danger`, `.btn-warning`, `.btn-info`
- `.panel`, `.panel-default`, `.panel-primary`
- `.form-group`, `.form-control`, `.input-group`
- `.alert`, `.alert-success`, `.alert-danger`, `.alert-warning`, `.alert-info`
- `.label`, `.badge`
- `.table`, `.table-striped`, `.table-bordered`
- `.nav`, `.nav-tabs`, `.nav-pills`
- `.modal`, `.modal-dialog`, `.modal-content`
- `.dropdown`, `.dropdown-menu`

**Warning**: Do NOT modify Bootstrap component classes in global CSS. Changes will leak into every widget on every page. Override only within scoped widget CSS.

## Widget CSS Patterns

### Standard Widget Structure

```html
<!-- Widget HTML template -->
<div class="ticket-list">
  <div class="ticket-list__header">
    <h2 class="ticket-list__title">{{c.data.title}}</h2>
    <div class="ticket-list__actions">
      <button class="btn btn-primary btn-sm" ng-click="c.refresh()">
        Refresh
      </button>
    </div>
  </div>
  <div class="ticket-list__body">
    <div class="ticket-list__item"
         ng-repeat="ticket in c.data.tickets"
         ng-class="{'ticket-list__item--critical': ticket.priority == 1}">
      <span class="ticket-list__number">{{ticket.number}}</span>
      <span class="ticket-list__description">{{ticket.short_description}}</span>
      <span class="ticket-list__priority priority-{{ticket.priority}}">
        {{ticket.priority_label}}
      </span>
    </div>
  </div>
</div>
```

### Widget SCSS

```scss
/* Widget-scoped CSS (auto-prefixed by ServiceNow) */

/* Variables with !default for theme override */
$ticket-list-bg: $color-white !default;
$ticket-list-border: $color-light !default;
$ticket-list-item-hover: $color-lightest !default;

.ticket-list {
  background: $ticket-list-bg;
  border: 1px solid $ticket-list-border;
  border-radius: $border-radius-base;

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-bottom: 1px solid $ticket-list-border;
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
    padding: 10px 16px;
    border-bottom: 1px solid $color-lighter;
    cursor: pointer;
    transition: background-color 0.15s ease;

    &:hover {
      background-color: $ticket-list-item-hover;
    }

    &:last-child {
      border-bottom: none;
    }

    &--critical {
      border-left: 4px solid $brand-danger;
    }
  }

  &__number {
    font-size: $font-size-small;
    color: $brand-primary;
    font-weight: 600;
    min-width: 100px;
  }

  &__description {
    flex: 1;
    font-size: $font-size-base;
    color: $color-darkest;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  &__priority {
    font-size: $font-size-small;
    padding: 2px 8px;
    border-radius: $border-radius-small;
    font-weight: 600;
  }
}

/* Priority color classes */
.priority-1 { background: lighten($brand-danger, 35%); color: $brand-danger; }
.priority-2 { background: lighten($brand-warning, 35%); color: darken($brand-warning, 20%); }
.priority-3 { background: lighten($brand-info, 40%); color: $brand-info; }
.priority-4 { background: lighten($brand-success, 40%); color: $brand-success; }
```

### CSS Best Practices

1. **Use BEM naming**: `block__element--modifier` prevents collisions
2. **Keep selectors shallow**: Maximum 2-3 levels deep
3. **Avoid ID selectors**: Use classes for styling, IDs for JS/AngularJS binding
4. **Use SCSS nesting sparingly**: Match the HTML structure but don't over-nest
5. **Prefix custom classes**: `my-portal-*` or `acme-*` to avoid collisions with ServiceNow's own classes
6. **Never use `!important` in global CSS**: Only acceptable in scoped widget CSS
7. **Use `ng-attr-id` for dynamic IDs**: Instead of static IDs that may collide

## Portal Theming

### Theme Structure

A Service Portal theme consists of:
- **CSS Variables** (SCSS): Override `$brand-*` and neutral variables
- **Header/Footer widgets**: Custom header and footer components
- **Navigation**: Menu structure and behavior
- **Global CSS**: Portal-wide styles (use minimally)

### Creating a Theme

```scss
/* Theme SCSS Variables */
$brand-primary: #0056b3;
$brand-success: #2e8540;
$brand-danger: #c8102e;
$brand-warning: #eeb422;
$brand-info: #0070d2;

/* Custom theme variables */
$navbar-bg: #30302f;
$navbar-text: #ffffff;
$footer-bg: #1e1e1e;

/* Override Bootstrap navbar */
.navbar-default {
  background-color: $navbar-bg;
  border: none;

  .navbar-brand,
  .navbar-nav > li > a {
    color: $navbar-text;
  }
}
```

### Theme vs Portal CSS

| Feature | Portal CSS Variables | Theme CSS Variables |
|---------|---------------------|-------------------|
| Scope | All pages in portal | All pages using theme |
| Purpose | Default brand values | Theme-specific overrides |
| Priority | Lower | Higher (overrides portal) |
| When to use | Base branding | Seasonal/variant themes |

## Typography

Service Portal typography defaults differ from Next Experience:

| Element | Font | Size | Weight |
|---------|------|------|--------|
| H1 | Arial | 36px | 500 |
| H2 | Arial | 30px | 500 |
| H3 | Arial | 24px | 500 |
| H4 | Arial | 18px | 500 |
| Body | Arial | 14px | 400 |
| Small | Arial | 12px | 400 |
| Button | Arial | 14px | 400 |

**Key difference**: Service Portal's base font size is **14px** (vs Next Experience's 16px). This makes the overall UI slightly more compact, which is typical of the Bootstrap 3 era.

## Color System

### Mapping to Next Experience Colors

When building portals that should visually align with Next Experience workspaces:

| SCSS Variable | Next Experience Token | Hex |
|--------------|----------------------|-----|
| `$brand-primary` | `--now-color_interactive--primary` | `#0056b3` |
| `$brand-danger` | `--now-color_alert--critical` | `#c8102e` |
| `$brand-warning` | `--now-color_alert--warning` | `#eeb422` |
| `$brand-success` | `--now-color_alert--positive` | `#2e8540` |
| `$brand-info` | `--now-color_alert--info` | `#0070d2` |
| `$color-darkest` | `--now-color_text--primary` | `#1e1e1e` |
| `$color-dark` | `--now-color_text--secondary` | `#6b6b6b` |
| `$color-lightest` | `--now-color_surface--secondary` | `#f4f4f4` |

## Layout & Grid

### Common Portal Layouts

**Full-width hero + content**:
```html
<div class="container-fluid hero-banner">
  <!-- Full-width hero -->
</div>
<div class="container">
  <div class="row">
    <div class="col-md-8"><!-- Main content --></div>
    <div class="col-md-4"><!-- Sidebar --></div>
  </div>
</div>
```

**Card grid**:
```html
<div class="container">
  <div class="row">
    <div class="col-sm-6 col-md-4" ng-repeat="item in c.data.items">
      <div class="panel panel-default">
        <div class="panel-body">
          {{item.title}}
        </div>
      </div>
    </div>
  </div>
</div>
```

### Responsive Considerations

- Service Portal pages should work at minimum 320px width
- Use `col-xs-12` as mobile default, then specify larger breakpoints
- Test navigation collapse at tablet breakpoints
- Hero banners should scale image/text proportionally

## Widget Development

### Client Script Pattern

```javascript
function($scope, $http, spUtil) {
  var c = this;

  c.refresh = function() {
    c.loading = true;
    c.server.get({ action: 'refresh' }).then(function(response) {
      c.data.tickets = response.data.tickets;
      c.loading = false;
    });
  };

  // Accessibility: announce updates
  c.announceUpdate = function(message) {
    spUtil.addInfoMessage(message);
  };
}
```

### Server Script Pattern

```javascript
(function() {
  if (input && input.action === 'refresh') {
    var gr = new GlideRecord('incident');
    gr.addQuery('active', true);
    gr.orderByDesc('sys_created_on');
    gr.setLimit(20);
    gr.query();

    data.tickets = [];
    while (gr.next()) {
      data.tickets.push({
        sys_id: gr.getUniqueValue(),
        number: gr.getValue('number'),
        short_description: gr.getValue('short_description'),
        priority: parseInt(gr.getValue('priority')),
        priority_label: gr.getDisplayValue('priority'),
        state: gr.getDisplayValue('state')
      });
    }
  }
})();
```

### Key Resources for Service Portal

- **Service Portal CSS Docs**: https://www.servicenow.com/docs/bundle/yokohama-platform-user-interface/page/build/service-portal/concept/portal-css.html
- **Ultimate CSS Guide**: https://www.servicenow.com/community/developer-blog/the-ultimate-service-portal-css-guide/ba-p/2290168
- **Design Guidelines**: https://www.servicenow.com/community/service-portal-articles/service-portal-design-guidelines/ta-p/2476669
- **Development Guidelines**: https://www.servicenow.com/community/service-portal-articles/service-portal-development-guidelines/ta-p/2590661
- **CSS Best Practices**: https://codecreative.io/blog/6-best-practices-for-service-portal-css/
- **SCSS Variables Guide**: https://serviceportal.io/scss-variables-service-portal/
- **AngularJS Style Guide**: https://github.com/platform-experience/serviceportal-best-practice
- **Horizon Portal Framework**: https://horizon.servicenow.com/get-started/app-frameworks/service-portal

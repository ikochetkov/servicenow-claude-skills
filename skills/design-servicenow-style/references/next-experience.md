# Next Experience (Horizon / Polaris) — Detailed Reference

This reference covers the current-generation ServiceNow UI framework used in UI Builder, Workspaces, Employee Center, and all new application development.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [CSS Custom Properties (Design Tokens)](#css-custom-properties)
3. [Color System Deep Dive](#color-system)
4. [Typography System](#typography-system)
5. [Component Architecture](#component-architecture)
6. [Theming](#theming)
7. [Dark Mode](#dark-mode)
8. [Workspace Structure](#workspace-structure)
9. [UI Builder Page Layout](#ui-builder-page-layout)
10. [Building Custom Components](#building-custom-components)

---

## Architecture Overview

Next Experience is built on **Seismic** — ServiceNow's custom web component framework. Key characteristics:

- **Web Components standard**: Custom elements with Shadow DOM encapsulation
- **Custom HTML tags**: All ServiceNow components use `<now-*>` prefix (e.g., `<now-button>`, `<now-icon>`, `<now-input>`)
- **Shadow DOM**: CSS is encapsulated within each component — styles don't leak in or out
- **Slot-based composition**: Components expose slots for flexible content placement
- **Event-driven communication**: Components emit/listen for CustomEvents
- **State management**: Data Resources manage application state

This matters for styling because you cannot override internal component styles from outside. You style through:
1. CSS custom properties (design tokens) that components inherit
2. Theme JSON records that set token values globally
3. Component attributes/properties for variant selection
4. Slot content that you control directly

## CSS Custom Properties

Next Experience uses CSS custom properties extensively for theming. These are the primary styling mechanism — set them at the theme level, and all components inherit the values.

### Color Tokens

```css
/* Brand & Chrome */
--now-color_chrome--brand: rgb(48, 47, 75);      /* Nav bar brand color (Polaris default: purple-black) */
--now-color_chrome--divider: rgb(228, 228, 228);  /* Chrome divider lines */

/* Interactive */
--now-color_interactive--primary: rgb(0, 86, 179);    /* Primary actions, links */
--now-color_interactive--secondary: rgb(71, 71, 71);   /* Secondary actions */
--now-color_interactive--hover: rgb(0, 65, 138);       /* Primary hover state */
--now-color_interactive--active: rgb(0, 50, 107);      /* Primary active/pressed */

/* Selection */
--now-color_selection--primary: rgb(0, 86, 179);       /* Selected items, active tabs */
--now-color_selection--secondary: rgb(230, 240, 250);  /* Selected row highlight */

/* Surface (backgrounds) */
--now-color_surface--primary: rgb(255, 255, 255);      /* Main content area */
--now-color_surface--secondary: rgb(244, 244, 244);    /* Cards, sidebar */
--now-color_surface--tertiary: rgb(232, 232, 232);     /* Dividers, disabled bg */
--now-color_surface--brand: rgb(48, 47, 75);           /* Brand-colored surfaces */

/* Text */
--now-color_text--primary: rgb(30, 30, 30);            /* Main body text */
--now-color_text--secondary: rgb(107, 107, 107);       /* Captions, helpers */
--now-color_text--tertiary: rgb(148, 148, 148);        /* Placeholders, disabled */
--now-color_text--on-primary: rgb(255, 255, 255);      /* Text on primary-colored bg */

/* Status / Alerts */
--now-color_alert--critical: rgb(200, 16, 46);         /* P1, errors */
--now-color_alert--high: rgb(232, 110, 44);            /* P2, warnings */
--now-color_alert--warning: rgb(238, 180, 34);         /* P3, moderate */
--now-color_alert--positive: rgb(46, 133, 64);         /* Success, resolved */
--now-color_alert--info: rgb(0, 112, 210);             /* Informational */

/* Focus */
--now-color_focus--ring: rgb(0, 86, 179);              /* Focus indicator ring */
```

### Typography Tokens

```css
/* Font Families */
--now-font-family--heading: 'Cabin', Arial, Helvetica, sans-serif;
--now-font-family--body: 'Lato', Arial, Helvetica, sans-serif;

/* Font Sizes (modular scale) */
--now-font-size--xs: 12px;    /* Complementary, badges */
--now-font-size--sm: 14px;    /* Small body, button labels */
--now-font-size--md: 16px;    /* Body text (base) */
--now-font-size--lg: 20px;    /* Content headers */
--now-font-size--xl: 24px;    /* Section headers */
--now-font-size--2xl: 32px;   /* Page titles */

/* Font Weights */
--now-font-weight--normal: 400;
--now-font-weight--semibold: 600;
--now-font-weight--bold: 700;

/* Line Heights */
--now-line-height--tight: 1.25;    /* Headings, single lines */
--now-line-height--normal: 1.5;    /* Body text, readable paragraphs */
--now-line-height--button: 1;      /* Button labels */
```

### Spacing Tokens

```css
/* Spacing Scale (4px base) */
--now-spacing--xs: 4px;
--now-spacing--sm: 8px;
--now-spacing--md: 16px;
--now-spacing--lg: 24px;
--now-spacing--xl: 32px;
--now-spacing--2xl: 48px;

/* Component-specific spacing */
--now-spacing--card-padding: 16px;
--now-spacing--form-gap: 16px;
--now-spacing--section-gap: 24px;
```

### Shadow Tokens

```css
--now-shadow--low: 0 1px 2px rgba(0, 0, 0, 0.1);
--now-shadow--medium: 0 2px 8px rgba(0, 0, 0, 0.15);
--now-shadow--high: 0 4px 16px rgba(0, 0, 0, 0.2);
```

### Border Tokens

```css
--now-border-radius--sm: 4px;     /* Buttons, inputs, cards */
--now-border-radius--md: 8px;     /* Modals, dialogs */
--now-border-radius--full: 9999px; /* Pills, avatars */

--now-border-color--primary: rgb(217, 217, 217);   /* Default borders */
--now-border-color--secondary: rgb(232, 232, 232);  /* Subtle dividers */
```

## Color System

### Polaris Theme Colors

The Polaris theme (default since Utah release) uses a purple-black chrome with these characteristics:

- **Chrome (navigation)**: Deep purple-black `rgb(48, 47, 75)` — gives the nav bar its distinctive look
- **App Shell header**: Same chrome color extends across the top
- **Content area**: Clean white `#ffffff` background
- **Cards/panels**: Slight gray `#f4f4f4` for visual separation
- **Primary interactive**: Blue `#0056b3` for all clickable elements

### Status Color Mapping

ServiceNow has a well-established color system for incident/task priority that users expect:

| Priority | Color | Hex | CSS Variable |
|----------|-------|-----|-------------|
| P1 - Critical | Red | `#c8102e` | `--now-color_alert--critical` |
| P2 - High | Orange | `#e86e2c` | `--now-color_alert--high` |
| P3 - Moderate | Yellow | `#eeb422` | `--now-color_alert--warning` |
| P4 - Low | Green | `#2e8540` | `--now-color_alert--positive` |
| P5 - Planning | Blue | `#0070d2` | `--now-color_alert--info` |

### Category Colors (Data Visualization)

When creating charts, dashboards, or any multi-category data visualization, use this palette to maintain consistency with native ServiceNow reporting:

```css
--now-color_grouped--01: #0070d2;  /* Blue */
--now-color_grouped--02: #4bc076;  /* Green */
--now-color_grouped--03: #f49342;  /* Orange */
--now-color_grouped--04: #e6574f;  /* Red */
--now-color_grouped--05: #9050e9;  /* Purple */
--now-color_grouped--06: #17bebb;  /* Teal */
--now-color_grouped--07: #e8a93e;  /* Gold */
--now-color_grouped--08: #f06c9b;  /* Pink */
```

## Typography System

### Heading Hierarchy

Use this hierarchy consistently — page title appears once per page, section headers group content, content headers label individual sections:

```css
/* Page Title — one per page */
.page-title {
  font-family: var(--now-font-family--heading);
  font-size: var(--now-font-size--2xl);  /* 32px */
  font-weight: var(--now-font-weight--semibold);
  line-height: var(--now-line-height--tight);
  color: var(--now-color_text--primary);
}

/* Section Header — groups related content */
.section-header {
  font-family: var(--now-font-family--heading);
  font-size: var(--now-font-size--xl);  /* 24px */
  font-weight: var(--now-font-weight--semibold);
  line-height: 1.3;
  color: var(--now-color_text--primary);
}

/* Content Header — labels a specific block */
.content-header {
  font-family: var(--now-font-family--heading);
  font-size: var(--now-font-size--lg);  /* 20px */
  font-weight: var(--now-font-weight--semibold);
  line-height: 1.4;
  color: var(--now-color_text--primary);
}

/* Body — primary readable content */
.body-text {
  font-family: var(--now-font-family--body);
  font-size: var(--now-font-size--md);  /* 16px */
  font-weight: var(--now-font-weight--normal);
  line-height: var(--now-line-height--normal);
  color: var(--now-color_text--primary);
}

/* Complementary — timestamps, metadata, captions */
.complementary {
  font-family: var(--now-font-family--body);
  font-size: var(--now-font-size--xs);  /* 12px */
  font-weight: var(--now-font-weight--normal);
  line-height: var(--now-line-height--normal);
  color: var(--now-color_text--secondary);
}
```

## Component Architecture

### Now Experience Components

All native components use the `<now-*>` prefix. When building custom components that sit alongside these, match their patterns:

**Button variants:**
- `<now-button>` — Standard button (sizes: sm, md, lg)
- `<now-button-bare>` — Text-only button (sizes: sm, md only)
- `<now-button-iconic>` — Icon-only button
- `<now-button-stateful>` — Button with loading/state indicators
- `<now-split-button>` — Button with dropdown action menu

**Form components:**
- `<now-input>` — Text input
- `<now-textarea>` — Multi-line text
- `<now-select>` — Dropdown select
- `<now-radio-group>` — Radio button group
- `<now-checkbox>` — Checkbox
- `<now-toggle>` — Toggle switch

**Display components:**
- `<now-icon>` — Icon with outline/filled variants
- `<now-avatar>` — User avatar (with initials fallback)
- `<now-badge>` — Status badge
- `<now-card>` — Content card container
- `<now-tooltip>` — Tooltip overlay
- `<now-modal>` — Modal dialog

### Custom Component Structure

When building a UI Builder custom component:

```javascript
import { createCustomElement } from '@servicenow/ui-core';
import snabbdom from '@servicenow/ui-renderer-snabbdom';
import styles from './styles.scss';

const view = (state, { updateState }) => {
  return (
    <div className="my-component">
      <h2 className="my-component__title">{state.properties.title}</h2>
      <div className="my-component__content">
        {/* Component content */}
      </div>
    </div>
  );
};

createCustomElement('x-my-component', {
  renderer: { type: snabbdom },
  view,
  styles,
  properties: {
    title: { default: '' }
  }
});
```

**Naming conventions:**
- Custom component tags: `x-[scope]-[name]` (e.g., `x-acme-ticket-card`)
- CSS classes: BEM methodology — `block__element--modifier`
- Properties: camelCase in JS, kebab-case in HTML attributes

## Theming

### Theme Record Structure

Themes in Next Experience are stored as `sys_ux_theme` records containing JSON that maps CSS custom property names to values:

```json
{
  "--now-color_chrome--brand": "rgb(48, 47, 75)",
  "--now-color_interactive--primary": "rgb(0, 86, 179)",
  "--now-color_surface--primary": "rgb(255, 255, 255)",
  "--now-color_text--primary": "rgb(30, 30, 30)"
}
```

### Creating Custom Themes

1. Create a new `sys_ux_theme` record
2. Set the `extends` field to inherit from the base Polaris theme
3. Override only the tokens you need to change
4. Themes cascade: child theme values override parent values

**Best practice**: Create one master company theme with brand colors, then extend it per workspace/application for specific needs.

### Theme Applicability

Themes can be scoped to specific contexts using the `applicability` field:
- By **role**: Different themes for ITIL users vs. HR agents
- By **application**: Custom theme per workspace
- By **query parameters**: Dynamic theming based on URL

## Dark Mode

### Enabling Dark Mode

Set system property: `glide.ui.polaris.dark_themes_enabled = true`

Users then toggle via: **Themes menu → Dark theme**

### Dark Mode Token Overrides

When dark mode activates, these token values flip:

```css
/* Light → Dark overrides */
--now-color_surface--primary: rgb(30, 30, 30);       /* Was white */
--now-color_surface--secondary: rgb(45, 45, 45);      /* Was light gray */
--now-color_text--primary: rgb(230, 230, 230);         /* Was dark */
--now-color_text--secondary: rgb(180, 180, 180);       /* Was medium gray */
--now-color_chrome--brand: rgb(35, 35, 55);            /* Darker chrome */
```

### Dark Mode Considerations

- All custom components must respect token values (use `var()` references, never hardcode colors)
- Test with both light and dark themes during development
- Avoid using transparency that looks good on white but breaks on dark
- Status colors generally remain the same — they need to be recognizable in both modes
- ServiceNow's APCA (Advanced Perceptual Contrast Algorithm) ensures contrast in dark mode

## Workspace Structure

A standard ServiceNow workspace has this layout:

```
┌─────────────────────────────────────────────────┐
│  Unified Navigation (Chrome)                     │
│  Logo  │  App Name  │  Search  │  User Menu     │
├────┬────────────────────────────────────────────┤
│    │                                             │
│ S  │  Stage (Main Content Area)                  │
│ i  │  ┌──────────────────────────────────┐      │
│ d  │  │  Page Content                     │      │
│ e  │  │  (12-column grid)                 │      │
│    │  │                                   │      │
│ N  │  │  Records, forms, dashboards...    │      │
│ a  │  │                                   │      │
│ v  │  └──────────────────────────────────┘      │
│    │                                             │
├────┴────────────────────────────────────────────┤
│  Contextual Sidebar (optional, right side)       │
└─────────────────────────────────────────────────┘
```

**Chrome**: Always present, provides global navigation. Fixed at top. Customizable brand color only.

**Side Navigation**: Collapsible left sidebar with module links. ~256px wide when open.

**Stage**: Main content area. Contains the page rendered by UI Builder. Uses 12-column grid.

**Contextual Sidebar**: Optional right panel for record details, chat, activity feeds. Slides in/out.

## UI Builder Page Layout

### Layout Containers

UI Builder pages use nested layout containers:

```html
<!-- Page root -->
<sn-canvas-appshell-root>
  <!-- Layout with 12-column grid -->
  <sn-canvas-layout columns="12" gap="16px">
    <!-- Full-width header -->
    <sn-canvas-container span="12">
      <now-heading level="1">Page Title</now-heading>
    </sn-canvas-container>

    <!-- Two-column layout (8 + 4) -->
    <sn-canvas-container span="8">
      <!-- Main content components -->
    </sn-canvas-container>
    <sn-canvas-container span="4">
      <!-- Sidebar content -->
    </sn-canvas-container>
  </sn-canvas-layout>
</sn-canvas-appshell-root>
```

### Common Page Layouts

**Record page (form + sidebar)**:
- Left 8 columns: Form fields, tabs, related lists
- Right 4 columns: Activity stream, attachments, related records

**List page**:
- Full 12 columns: Filter bar + data list/table + pagination

**Dashboard page**:
- Mixed grid: 2-column, 3-column, or 4-column card arrangements
- Cards span 3, 4, or 6 columns depending on content

## Building Custom Components

### Style Guidelines for Custom Components

When creating custom components for UI Builder, follow these rules to ensure visual harmony:

1. **Always use CSS custom properties** — never hardcode colors, fonts, or spacing
2. **Match native component sizing** — your buttons should be the same height as `<now-button>`
3. **Use the same border-radius** — 4px for interactive elements, 8px for containers
4. **Respect the spacing scale** — only use values from the 4/8/16/24/32/48 scale
5. **Follow the shadow hierarchy** — cards get low shadow, popovers get medium, modals get high
6. **Maintain text hierarchy** — page has one title (32px), sections get 24px, content gets 20px, body is 16px

### Component CSS Template

```scss
:host {
  /* Inherit theme tokens */
  font-family: var(--now-font-family--body, 'Lato', Arial, sans-serif);
  color: var(--now-color_text--primary, #1e1e1e);
}

.my-component {
  background: var(--now-color_surface--primary, #fff);
  border: 1px solid var(--now-border-color--primary, #d9d9d9);
  border-radius: var(--now-border-radius--sm, 4px);
  padding: var(--now-spacing--md, 16px);
  box-shadow: var(--now-shadow--low, 0 1px 2px rgba(0,0,0,0.1));
}

.my-component__header {
  font-family: var(--now-font-family--heading, 'Cabin', Arial, sans-serif);
  font-size: var(--now-font-size--lg, 20px);
  font-weight: var(--now-font-weight--semibold, 600);
  margin-bottom: var(--now-spacing--sm, 8px);
}

.my-component__body {
  font-size: var(--now-font-size--md, 16px);
  line-height: var(--now-line-height--normal, 1.5);
}

/* Interactive states */
.my-component__action {
  color: var(--now-color_interactive--primary, #0056b3);
  cursor: pointer;
}

.my-component__action:hover {
  color: var(--now-color_interactive--hover, #00438a);
  text-decoration: underline;
}

.my-component__action:focus-visible {
  outline: 2px solid var(--now-color_focus--ring, #0056b3);
  outline-offset: 2px;
  border-radius: var(--now-border-radius--sm, 4px);
}

/* Status variants */
.my-component--critical {
  border-left: 4px solid var(--now-color_alert--critical, #c8102e);
}

.my-component--success {
  border-left: 4px solid var(--now-color_alert--positive, #2e8540);
}
```

### Key Resources for Next Experience Development

- **Horizon Design System**: https://horizon.servicenow.com/
- **Component Reference**: https://horizon.servicenow.com/workspace/components
- **Typography**: https://horizon.servicenow.com/workspace/foundations/typography/typography-overview
- **Color Palettes**: https://horizon.servicenow.com/workspace/foundations/color/palettes
- **Spacing**: https://horizon.servicenow.com/workspace/foundations/spacing/spacing-overview
- **Icons**: https://horizon.servicenow.com/workspace/foundations/icons/icon-library
- **Accessibility**: https://horizon.servicenow.com/guidelines/accessibility/a11y-overview
- **Polaris Themes Part 1**: https://www.servicenow.com/community/next-experience-articles/all-about-next-experience-polaris-themes-part-1/ta-p/2670725
- **Polaris Themes Part 2**: https://www.servicenow.com/community/next-experience-articles/all-about-next-experience-polaris-themes-part-2-ux-theme-records/ta-p/2687236
- **UI Builder Theming**: https://www.servicenow.com/community/next-experience-articles/ui-builder-theming/ta-p/2331911

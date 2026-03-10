---
name: design-servicenow-style
description: >
  ServiceNow design system guide with real Figma-extracted tokens. Covers Next Experience (Horizon/Polaris), Service Portal, and Classic UI. Includes spacing, colors, typography, 114 component specs, 1973 --now-* CSS properties, and 18 Figma library references. Use for ServiceNow-styled UIs, UI Builder components, Service Portal widgets, or any ServiceNow-matching visual work. Triggers: ServiceNow style, Horizon, Polaris, Next Experience, Service Portal, UI Builder, workspace components, now-experience.
---

# ServiceNow Design System Guide

This skill helps you build UIs that are visually consistent with ServiceNow's native applications. It is grounded in real design tokens and component specifications extracted from ServiceNow's official Figma libraries (Horizon Design System) and the platform's 1,973 CSS custom properties.

## First: Determine the Target Framework

Before writing any code, clarify which ServiceNow experience the user is building for:

| Framework | Era | Tech Stack | When to Use |
|-----------|-----|-----------|-------------|
| **Next Experience (Horizon)** | Current | Web Components (Seismic), `<now-*>` tags | UI Builder pages, Workspaces, Employee Center, new apps |
| **Service Portal** | Legacy (still widely used) | AngularJS, Bootstrap 3 | Portal widgets, self-service catalogs, customer-facing pages |
| **Classic UI (UI16)** | Legacy | jQuery, native | Backend admin views, list/form customizations |

If the user doesn't specify, **default to Next Experience**. Ask if unsure: "Are you building for UI Builder/Workspace (Next Experience) or Service Portal (AngularJS)?"

## Reference Files — Read the Ones Matching Your Task

- `references/design-tokens.md` — **START HERE** — Complete spacing, grid, typography, color, shadow, and border radius tokens extracted from Figma + CSS custom properties, theme JSON format
- `references/figma-libraries.md` — Full catalog of all 18 official Figma libraries with component inventories and direct links
- `references/next-experience.md` — Horizon/Seismic web components, `<now-*>` element catalog, workspace patterns, theming API
- `references/service-portal.md` — Bootstrap/SCSS variables, widget CSS patterns, portal theming
- `references/common-patterns.md` — Shared UX patterns (forms, lists, cards, modals, navigation) with framework-specific implementations
- `references/code-samples.md` — Ready-to-use code templates for both frameworks

**Always read `design-tokens.md` first** — it contains the exact values you need for any ServiceNow-styled code.

## Core Design Principles

ServiceNow's design philosophy:

**Clarity over decoration** — Every visual element serves a purpose. No decorative gradients, shadows, or animations. ServiceNow UIs are clean, functional, and information-dense.

**Consistent density** — ServiceNow apps pack information into screens (lists, forms, dashboards). Use tight, purposeful spacing. The spacing scale starts at 2px (xxs) with md at 12px (not 16px like most systems).

**Neutral palette with purposeful color** — Base UI is white/gray. Color is reserved for interactive elements, status indicators, and brand accents. Never purely decorative.

**Accessible by default** — WCAG 2.1 Level AA minimum. 4.5:1 contrast for normal text, 3:1 for large text.

**Progressive disclosure** — Show what's needed, reveal details on demand. Use collapsible sections, tabs, drill-down patterns.

## Quick Reference: Design Tokens

### Spacing (from Figma component set, verified)

| Token | CSS Property | Value | Usage |
|-------|-------------|-------|-------|
| `xxs` | `--now-spacing-xxs` | 2px | Minimal inline spacing |
| `xs` | `--now-spacing-xs` | 4px | Tight gaps, icon margins |
| `sm` | `--now-spacing-sm` | 8px | Small padding, icon-to-text |
| `md` | `--now-spacing-md` | 12px | Default padding, form gaps |
| `lg` | `--now-spacing-lg` | 16px | Section padding |
| `xl` | `--now-spacing-xl` | 24px | Section separation |
| `xxl` | `--now-spacing-xxl` | 32px | Major breaks |
| `3xl` | `--now-spacing-3xl` | 40px | Page-level spacing |

**Note:** ServiceNow's `md` spacing is 12px, not the typical 16px found in other design systems. This creates the characteristic dense feel.

### Colors (from Figma + CSS hooks)

| Role | Hex | CSS Property |
|------|-----|-------------|
| Brand Dark Teal | `#2a3d40` | `--now-color_brand--primary` |
| Brand Light Green | `#82b6a2` | `--now-color_brand--secondary` |
| Interactive Primary | `#0056b3` | `--now-color--primary-1` |
| Chrome/Nav Background | `#30302f` | `--now-unified-nav_bg` |
| Surface Primary | `#ffffff` | `--now-color_background--primary` |
| Surface Secondary | `#f4f4f4` | `--now-color--neutral-1` |
| Surface Tertiary | `#e8e8e8` | `--now-color--neutral-2` |
| Text Primary | `#1e1e1e` | `--now-color_text--primary` |
| Text Secondary | `#6b6b6b` | `--now-color_text--secondary` |
| Text Tertiary | `#949494` | `--now-color_text--tertiary` |
| Critical | `#c8102e` | `--now-color--alert-critical-2` |
| High/Warning | `#e86e2c` | `--now-color--alert-high-2` |
| Moderate | `#eeb422` | `--now-color--alert-moderate-2` |
| Success | `#2e8540` | `--now-color--alert-positive-2` |
| Info | `#0070d2` | `--now-color--alert-info-2` |

### Typography (Figma → Production mapping)

| Element | Font | Size | Weight | Line Height |
|---------|------|------|--------|-------------|
| Display | Cabin (prod) / Gilroy (Figma) | 64px | 700 | 1.15 |
| Page Title (H1) | Cabin / Arial | 32px | 600 | 1.25 |
| Section Header (H2) | Cabin / Arial | 24px | 600 | 1.3 |
| Content Header (H3) | Cabin / Arial | 20px | 600 | 1.4 |
| Body Large | Lato / Arial | 16px | 400 | 1.5 |
| Body Default | Lato / Arial | 14px | 400 | 1.5 |
| Body Small | Lato / Arial | 12px | 400 | 1.5 |
| Button Label | Lato / Arial | 14px | 600 | 1 |

**Font priority**: Next Experience uses **Cabin** (headings) and **Lato** (body). For standalone apps, use **Arial** as the safe cross-platform fallback.

### Shadows & Elevation

| Level | CSS Property | Value |
|-------|-------------|-------|
| None | — | `none` |
| Low | `--now-shadow--sm` | `0 1px 2px rgba(0,0,0,0.1)` |
| Medium | `--now-shadow--md` | `0 2px 8px rgba(0,0,0,0.15)` |
| High | `--now-shadow--lg` | `0 4px 16px rgba(0,0,0,0.2)` |

### Border Radius

| Element | CSS Property | Value |
|---------|-------------|-------|
| Buttons, Cards, Inputs | `--now-border-radius--sm` | 4px |
| Modals, Dialogs | `--now-border-radius--md` | 8px |
| Large Containers | `--now-border-radius--lg` | 16px |
| Avatars, Tags | `--now-border-radius--circle` | 50% |

### Grid System (from Figma, 14 variants verified)

| Breakpoint | Width | Margins | Gutters | Max Content |
|------------|-------|---------|---------|-------------|
| Standard | 1280px | 24px | 48px | 1232px |
| Wide | 1600px | 24px | 48px | 1552px |

12-column grid. Responsive breakpoints: xs: 0, sm: 576px, md: 768px, lg: 992px, xl: 1200px, 2xl: 1600px.

## Component Inventory (from Figma Libraries)

The complete component set extracted from ServiceNow's official Figma libraries:

### Workspace Components (114 components across 10 categories)

**Containers:** Card, Collapsible Container, Document Display, Evam Card, Modal, Modeless Dialog, Popover, Search Results Container, Template Card, Template Card Omnichannel

**Content:** Analytics Q&A, Avatar, Badge, Contextual Sidebar, Dashboards Overview, Data Row, Data Set, Filter, Form Record Presence, Heading, Highlighted Value, Label Value (Inline/Stacked/Tabbed), Pill List, Presentational List, Record Header, Record Tags, Tooltip

**Controls:** Accordion, Active Call, Button, Button Bare, Button Circular, Button Iconic, Button Stateful, Color Picker, Color Selector, List Selector, Pill, Presence Icon, Search Facets, Select, Split Button, Stepper, Text Link, Typeahead, Typeahead Multi

**Inputs:** Checkbox, Checklist, Date Time Calendar, Date Time Interval, Date Time Picker, Dropdown, Dropdown List, Flyout Menu, Input, Input Password, Input Phone, Input URL, Mini Calendar, Radio Buttons, Text Area, Toggle

**Loaders:** Loader, Progress Bar

**Messaging:** Alert, Alert List, Empty State, Message

**Navigation:** Breadcrumbs, Content Tree, Pagination Control, Tabs, Unified Navigation

**Experience Shell:** Page Navigation, Primary Navigation

**Other (30+):** Activity Stream, Agent Chat, Appointment Calendar, Attachments, Carousel, Code Editor, Condition Builder, Confirmation Message, Contact Card, Digital Signature, Display Value Block, Email Composer, Form, Field Service Google Maps, Inbox, Kanban Board, Knowledge Content, KPI Details, Link Set, Link Set Group, Login, Lookup, Nested Comments, Node Map, MFA Setup, Playbook, Quick Filter, Related Content, Resizable Panes, SLA Timer, Star Rating, Timeline, Visualization Share Dialog, Workspace Global Search Tab, Workspace Notification

### Conversational Interfaces (2 product groups)

**Agent Chat:** Agent Chat Panel, Agent Chat Controls, Agent Chat Cards, Agent Chat Messages, Agent Chat System/Time Stamp

**Virtual Agent:** Virtual Agent Header, Web Client Frame, Input States, Bot Messages, Requestor Messages, Timestamp, Avatar, Media Card, Q&A Card, Record Card, Link, Table Card, Button, New Messages, Service Portal Icon, Support Menu, Modal

### Data Visualizations (24 pages of chart/graph components)

Chart types, data grids, KPI widgets, and analytics components for dashboards and reporting.

### Icons (826+ icons in Workspace library)

Outline and filled variants. Sizes: 12px (sm), 16px (md), 24px (lg), 32px (xl).

### Additional Libraries

- **Employee Center (EC):** Components and templates for employee-facing portals
- **Customer Portal (CP):** Components for customer-facing service portals
- **Core Components:** Foundational UI kit shared across all experiences
- **Core Icons:** Base icon set used across the platform
- **Core Templates:** Layout and page templates
- **Now Assist:** AI/GenAI UI components for Now Assist features
- **Workspace Risk:** Risk management-specific components
- **Workspace Dashboards:** Dashboard layout and widget components
- **Workspace Templates:** Pre-built workspace page templates
- **Accessibility:** Accessibility patterns, focus management, screen reader support

## CSS Custom Properties (--now-* Namespace)

ServiceNow uses **1,973 CSS custom properties** for theming. All follow the `--now-*` prefix. Key categories:

| Category | Prefix | Count | Purpose |
|----------|--------|-------|---------|
| Colors | `--now-color--*` | ~200 | Color scales (primary, neutral, alert) |
| Text Colors | `--now-color_text--*` | ~50 | Text-specific colors |
| Background | `--now-color_background--*` | ~50 | Background colors |
| Border | `--now-color_border--*` | ~30 | Border colors |
| Surface | `--now-color_surface--*` | ~20 | Card/panel surfaces |
| Chrome | `--now-color_chrome--*` | ~30 | Navigation chrome |
| Brand | `--now-color_brand--*` | ~10 | Brand identity colors |
| Unified Nav | `--now-unified-nav--*` | ~40 | Navigation-specific |
| Font | `--now-font--*` | ~30 | Typography system |
| Spacing | `--now-spacing--*` | 8 | Spacing scale |
| Shadow | `--now-shadow--*` | 4 | Elevation system |
| Border Radius | `--now-border-radius--*` | 4 | Corner rounding |

Full reference: https://theme.deoprototypes.com/hooks

## Theme JSON Format

When creating custom themes, use this JSON format:
```json
{
  "--now-color--primary-1": "0,86,179",
  "--now-color_background--primary": "255,255,255",
  "--now-color_text--primary": "30,30,30"
}
```

**CRITICAL:** Values are RGB triplets WITHOUT spaces: `"0,86,179"` not `"0, 86, 179"`. Spaces cause blank-page rendering failures.

## Accessibility Checklist

Every ServiceNow-styled component must meet:

- Color contrast: 4.5:1 for normal text (<18pt), 3:1 for large text (18pt+ or 14pt+ bold)
- All interactive elements focusable via keyboard (Tab/Shift+Tab)
- Visible focus indicator (minimum 2px outline, contrasting color)
- ARIA labels on icon-only buttons and non-text interactive elements
- Form fields have associated `<label>` elements or `aria-label`
- Status communicated by more than color alone (icons, text, patterns)
- Modals trap focus and return focus to trigger on close
- `aria-live` regions for dynamic content updates

## Figma Library Links

For detailed component specifications, variant properties, and visual references, see `references/figma-libraries.md` which contains direct links to all 18 official ServiceNow Figma community files.

## Key Resources

- **Horizon Design System**: https://horizon.servicenow.com/
- **Figma Libraries**: https://www.figma.com/@servicenow
- **Component Playground**: https://horizon.servicenow.com/workspace/components
- **Theming Hooks**: https://theme.deoprototypes.com/hooks (1,973 CSS properties)
- **ServiceNow Docs**: https://www.servicenow.com/docs/
- **Community**: https://www.servicenow.com/community/

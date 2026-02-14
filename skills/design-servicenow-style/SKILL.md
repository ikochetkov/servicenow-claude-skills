---
name: design-servicenow-style
description: >
  ServiceNow design system guide for building apps that look and feel native to the ServiceNow platform.
  Covers Next Experience (Horizon/Polaris) workspace components, Service Portal (AngularJS) widgets,
  and Classic UI styling. Provides colors, typography, spacing, component patterns, accessibility
  guidelines, and code samples for each framework variant.
  Use this skill whenever building ServiceNow-styled UIs, creating UI Builder components,
  developing Service Portal widgets, building SPAs that integrate with ServiceNow, or any
  coding task that should match ServiceNow's visual language. Trigger on mentions of
  "ServiceNow style", "ServiceNow design", "Horizon", "Polaris", "Next Experience",
  "Service Portal", "UI Builder", "workspace components", "now-experience", or any
  request to make something look like ServiceNow. Even if the user just says "make it match
  our ServiceNow instance" or "ServiceNow-like UI", use this skill.
---

# ServiceNow Design System Guide

This skill helps you build UIs that are visually consistent with ServiceNow's native applications. ServiceNow has multiple design frameworks — the right styling depends on which part of the platform you're targeting.

## First: Determine the Target Framework

Before writing any code, clarify which ServiceNow experience the user is building for. Each has distinct styling rules:

| Framework | Era | Tech Stack | When to Use |
|-----------|-----|-----------|-------------|
| **Next Experience (Horizon)** | Current | Web Components, Seismic | UI Builder pages, Workspaces, Employee Center, new apps |
| **Service Portal** | Legacy (still widely used) | AngularJS, Bootstrap 3 | Portal widgets, self-service catalogs, customer-facing pages |
| **Classic UI (UI16)** | Legacy | jQuery, native | Backend admin views, list/form customizations |

If the user doesn't specify, **default to Next Experience** — it's ServiceNow's current strategic direction. Ask if unsure: "Are you building for UI Builder/Workspace (Next Experience) or Service Portal (AngularJS)?"

**Detailed reference files** — read the one matching the target framework:

- `references/next-experience.md` — Horizon design tokens, Seismic components, workspace patterns, theming
- `references/service-portal.md` — Bootstrap/SCSS variables, widget CSS patterns, portal theming
- `references/common-patterns.md` — Shared UX patterns (forms, lists, cards, modals, navigation) with framework-specific implementations
- `references/code-samples.md` — Ready-to-use code templates for both frameworks

## Core Design Principles (All Frameworks)

ServiceNow's design philosophy centers on these principles regardless of framework:

**Clarity over decoration** — Every visual element should serve a purpose. Avoid decorative gradients, shadows, or animations that don't communicate state or hierarchy. ServiceNow UIs are clean, functional, and information-dense.

**Consistent density** — ServiceNow apps pack a lot of information into screens (lists, forms, dashboards). Don't over-space things. Use tight, purposeful spacing that lets users scan efficiently.

**Neutral palette with purposeful color** — The base UI is predominantly white/gray with color reserved for interactive elements (links, buttons), status indicators (critical/high/medium/low), and brand accents. Color should never be purely decorative.

**Accessible by default** — WCAG 2.1 Level AA minimum. 4.5:1 contrast for normal text, 3:1 for large text and non-text elements. All interactive elements must be keyboard-accessible with visible focus indicators.

**Progressive disclosure** — Show what's needed, reveal details on demand. Use collapsible sections, tabs, and drill-down patterns rather than overwhelming with everything at once.

## Quick Reference: Brand Colors

These are ServiceNow's core brand and UI colors used across all frameworks:

| Role | Hex | Usage |
|------|-----|-------|
| Brand Dark Green | `#243c3e` | Brand identity, premium accents |
| Brand Light Green | `#82b6a2` | Secondary brand, illustrations |
| Interactive Primary | `#0056b3` | Links, primary buttons, active states |
| Chrome/Nav Background | `#30302f` | Unified navigation bar, app shell |
| Surface Primary | `#ffffff` | Main content background |
| Surface Secondary | `#f4f4f4` | Card backgrounds, sidebar, secondary areas |
| Surface Tertiary | `#e8e8e8` | Dividers, borders, disabled backgrounds |
| Text Primary | `#1e1e1e` | Body text, headings |
| Text Secondary | `#6b6b6b` | Captions, timestamps, helper text |
| Text Tertiary | `#949494` | Placeholders, disabled text |
| Status Critical | `#c8102e` | Errors, critical incidents (P1) |
| Status High | `#e86e2c` | Warnings, high priority (P2) |
| Status Moderate | `#eeb422` | Moderate priority (P3) |
| Status Success | `#2e8540` | Success states, resolved items |
| Status Info | `#0070d2` | Informational badges, links |

## Quick Reference: Typography

| Element | Font | Size | Weight | Line Height |
|---------|------|------|--------|-------------|
| Page Title | Cabin / Arial | 32px | 600 (Semibold) | 1.25 |
| Section Header (H2) | Cabin / Arial | 24px | 600 | 1.3 |
| Content Header (H3) | Cabin / Arial | 20px | 600 | 1.4 |
| Body Text | Lato / Arial | 16px | 400 (Regular) | 1.5 |
| Body Small | Lato / Arial | 14px | 400 | 1.5 |
| Complementary | Lato / Arial | 12px | 400 | 1.5 |
| Button Label | Lato / Arial | 14px | 600 | 1 |

**Font priority**: Next Experience uses **Cabin** (headings) and **Lato** (body). Service Portal and Classic UI default to **Arial**. When building standalone apps that should feel like ServiceNow, use Arial as the safe cross-platform choice — it closely matches what most ServiceNow instances render.

## Quick Reference: Spacing Scale

ServiceNow uses an 8px baseline grid with 4px for fine adjustments:

| Token | Value | Usage |
|-------|-------|-------|
| `--xs` | 4px | Inline icon gaps, tight padding |
| `--sm` | 8px | Compact padding, small gaps between elements |
| `--md` | 16px | Default padding, form field gaps, card padding |
| `--lg` | 24px | Section separation, card margins |
| `--xl` | 32px | Major section breaks, page margins |
| `--2xl` | 48px | Hero spacing, page-level vertical rhythm |

## Quick Reference: Shadows & Elevation

| Level | CSS | Usage |
|-------|-----|-------|
| None | `none` | Flat elements, inline content |
| Low | `0 1px 2px rgba(0,0,0,0.1)` | Cards, dropdowns at rest |
| Medium | `0 2px 8px rgba(0,0,0,0.15)` | Elevated cards, popovers |
| High | `0 4px 16px rgba(0,0,0,0.2)` | Modals, dialogs, overlays |

## Quick Reference: Border Radius

| Element | Radius | Notes |
|---------|--------|-------|
| Buttons | 4px | Slight rounding, not pill-shaped |
| Cards | 4px | Consistent with buttons |
| Input fields | 4px | Matches button/card radius |
| Modals/Dialogs | 8px | Slightly more rounding for larger surfaces |
| Avatars/Tags | 50% / 16px | Fully rounded |

## Grid & Layout

ServiceNow uses a **12-column grid** system across all modern frameworks:

- **Workspace layouts**: Chrome (nav) + Stage (main content area) with configurable column spans
- **UI Builder pages**: CSS Grid with 12-column default, configurable via layout containers
- **Service Portal**: Bootstrap 3 grid (`col-xs-*`, `col-sm-*`, `col-md-*`, `col-lg-*`)
- **Breakpoints**: Follow standard responsive tiers (xs: 0, sm: 576px, md: 768px, lg: 992px, xl: 1200px)

## Icon System

ServiceNow's icons follow these specifications:

| Size Name | Pixels | Usage |
|-----------|--------|-------|
| Small (sm) | 12px | Inline text indicators, badges |
| Medium (md) | 16px | Form field icons, list indicators, default |
| Large (lg) | 24px | Navigation icons, action buttons |
| Extra Large (xl) | 32px | Feature icons, empty states |

**Style**: Outline by default, Filled for active/selected states. Minimal, modern, rounded corners. For custom icons, follow ServiceNow's grid and radius guidelines documented at `horizon.servicenow.com/workspace/foundations/icons`.

## Accessibility Checklist

Every ServiceNow-styled component must meet these requirements:

- Color contrast: 4.5:1 for normal text (<18pt), 3:1 for large text (18pt+ or 14pt+ bold)
- All interactive elements focusable via keyboard (Tab/Shift+Tab navigation)
- Visible focus indicator (minimum 2px outline, contrasting color)
- ARIA labels on icon-only buttons and non-text interactive elements
- Form fields have associated `<label>` elements or `aria-label`
- Status communicated by more than color alone (icons, text, patterns)
- Modals trap focus and return focus to trigger on close
- `aria-live` regions for dynamic content updates (notifications, search results)

## What to Read Next

After determining the framework, read the appropriate reference file for detailed implementation guidance:

1. **Read** `references/next-experience.md` for UI Builder/Workspace development
2. **Read** `references/service-portal.md` for Service Portal widget development
3. **Read** `references/common-patterns.md` for UX pattern implementations
4. **Read** `references/code-samples.md` for copy-paste starter templates

These files contain the CSS custom properties, component APIs, theming configurations, and code patterns specific to each framework.

## Key Resources

- **Horizon Design System**: https://horizon.servicenow.com/ (primary source of truth)
- **Figma Libraries**: https://www.figma.com/@servicenow (component kits, UI Kit 1.0)
- **ServiceNow Docs**: https://www.servicenow.com/docs/ (platform documentation)
- **Component Playground**: https://horizon.servicenow.com/workspace/components (live component demos)
- **Community**: https://www.servicenow.com/community/ (articles, examples, best practices)

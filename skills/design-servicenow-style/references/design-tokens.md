# ServiceNow Horizon Design System — Design Tokens Reference

This is a comprehensive reference guide for all design tokens extracted from ServiceNow's Horizon Design System, including Figma component libraries and CSS theming hooks. Use this as the authoritative source when building ServiceNow-styled user interfaces.

---

## Table of Contents

1. [Spacing Tokens](#spacing-tokens)
2. [Grid System](#grid-system)
3. [Typography](#typography)
4. [Color System](#color-system)
5. [Shadows & Elevation](#shadows--elevation)
6. [Border Radius](#border-radius)
7. [Icon System](#icon-system)
8. [CSS Custom Properties Reference](#css-custom-properties-reference)
9. [Theme JSON Structure](#theme-json-structure)
10. [Implementation Guidelines](#implementation-guidelines)

---

## Spacing Tokens

ServiceNow uses a consistent spacing scale based on a 4px foundation. These tokens are extracted from the Figma "Spacing" component set (node 798:64726).

| Token | Value | Use Case |
|-------|-------|----------|
| `xxs` | 2px | Minimal spacing for inline elements, icon margins |
| `xs` | 4px | Tight spacing between related elements |
| `sm` | 8px | Small spacing, icon-to-text gaps |
| `md` | 12px | **ServiceNow standard** (unique from typical 16px base) |
| `lg` | 16px | Standard spacing between content blocks |
| `xl` | 24px | Large spacing for section separation |
| `xxl` | 32px | Extra-large spacing between major sections |
| `3xl` | 40px | Maximum spacing for visual separation |

### CSS Custom Properties

Use the following CSS custom properties for spacing:

```css
--now-spacing-xxs: 2px;
--now-spacing-xs: 4px;
--now-spacing-sm: 8px;
--now-spacing-md: 12px;
--now-spacing-lg: 16px;
--now-spacing-xl: 24px;
--now-spacing-xxl: 32px;
--now-spacing-3xl: 40px;
```

**Implementation Example:**
```css
.component {
  padding: var(--now-spacing-md);
  margin-bottom: var(--now-spacing-lg);
  gap: var(--now-spacing-sm);
}
```

---

## Grid System

ServiceNow's grid system supports two breakpoints with consistent margin and gutter values. This is extracted from Figma node 798:64725.

### Layout Specifications

#### Standard Breakpoint (1280px)
- Margins: 24px
- Gutters: 48px
- Max Content Width: 1232px
- Column Range: 1–12 columns

#### Wide Breakpoint (1600px)
- Margins: 24px
- Gutters: 48px
- Max Content Width: 1552px
- Column Range: 1–12 columns

### Column Variants

The system provides 14 layout variants across 2 breakpoints:
- **1 Column** – Full-width layouts, single content stream
- **2 Columns** – Two-column layouts, sidebar + content
- **3 Columns** – Dashboard or card grid layouts
- **4 Columns** – Feature grids, icon cards
- **5 Columns** – Tile-based layouts
- **6 Columns** – Card grids, product displays
- **7–12 Columns** – Advanced layouts for flexible content placement

### Grid CSS Variables

```css
/* Breakpoints */
--now-grid-breakpoint-standard: 1280px;
--now-grid-breakpoint-wide: 1600px;

/* Spacing */
--now-grid-margin: 24px;
--now-grid-gutter: 48px;

/* Max widths */
--now-grid-max-width-standard: 1232px;
--now-grid-max-width-wide: 1552px;
```

**Implementation Example:**
```css
.grid-container {
  max-width: var(--now-grid-max-width-standard);
  margin: 0 auto;
  padding: 0 var(--now-grid-margin);
  display: grid;
  gap: var(--now-grid-gutter);
}

@media (min-width: 1600px) {
  .grid-container {
    max-width: var(--now-grid-max-width-wide);
  }
}
```

---

## Typography

ServiceNow typography uses a carefully curated type scale with specific font families and weights for hierarchy and readability.

### Font Families

| Context | Figma Font | Production Font | Fallback |
|---------|------------|-----------------|----------|
| Headings & Display | Gilroy | Cabin | System sans-serif |
| Body & Paragraph | Lato | Lato | Arial |

### Type Scale

| Style | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| Display | 64px | 700 | 1.15 (73.6px) | Page titles, hero content |
| H1 | 32px | 600 | 1.25 (40px) | Major section headings |
| H2 | 24px | 600 | 1.3 (31.2px) | Subheadings, card titles |
| H3 | 20px | 600 | 1.4 (28px) | Tertiary headings |
| Body (Large) | 16px | 400 | 1.5 (24px) | Primary body text, callouts |
| Body (Medium) | 14px | 400 | 1.5 (21px) | Standard body text |
| Body (Small) | 12px | 400 | 1.5 (18px) | Helper text, labels |
| Button Label | 14px | 600 | 1 (14px) | Button text, compact labels |

### CSS Custom Properties

```css
/* Font families */
--now-font-family-heading: 'Cabin', sans-serif;
--now-font-family-body: 'Lato', Arial, sans-serif;

/* Display */
--now-font-size-display: 64px;
--now-font-weight-display: 700;
--now-line-height-display: 1.15;

/* Heading 1 */
--now-font-size-h1: 32px;
--now-font-weight-h1: 600;
--now-line-height-h1: 1.25;

/* Heading 2 */
--now-font-size-h2: 24px;
--now-font-weight-h2: 600;
--now-line-height-h2: 1.3;

/* Heading 3 */
--now-font-size-h3: 20px;
--now-font-weight-h3: 600;
--now-line-height-h3: 1.4;

/* Body Large */
--now-font-size-body-lg: 16px;
--now-font-weight-body-lg: 400;
--now-line-height-body-lg: 1.5;

/* Body Medium */
--now-font-size-body-md: 14px;
--now-font-weight-body-md: 400;
--now-line-height-body-md: 1.5;

/* Body Small */
--now-font-size-body-sm: 12px;
--now-font-weight-body-sm: 400;
--now-line-height-body-sm: 1.5;

/* Button Label */
--now-font-size-button: 14px;
--now-font-weight-button: 600;
--now-line-height-button: 1;
```

**Implementation Example:**
```css
h1 {
  font: var(--now-font-weight-h1) var(--now-font-size-h1) / var(--now-line-height-h1) var(--now-font-family-heading);
}

body {
  font: var(--now-font-weight-body-md) var(--now-font-size-body-md) / var(--now-line-height-body-md) var(--now-font-family-body);
}

button {
  font: var(--now-font-weight-button) var(--now-font-size-button) / var(--now-line-height-button) var(--now-font-family-heading);
}
```

---

## Color System

ServiceNow's color system is comprehensive, featuring brand colors, neutral scales, interactive states, and semantic alert colors. All colors are defined as CSS custom properties using the `--now-color--*` namespace.

### Brand Colors

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| Brand Dark Teal | #2a3d40 | 42,61,64 | Primary brand color, dark mode primary |
| Brand Dark Teal (Alt) | #243c3e | 36,60,62 | Secondary brand variant |
| Brand Light Green | #82b6a2 | 130,182,162 | Accent, complementary brand color |

### Neutral Scale

ServiceNow's neutral scale provides the foundation for all non-semantic colors:

| Token | Hex | RGB | Luminance | Usage |
|-------|-----|-----|-----------|-------|
| 0 | #ffffff | 255,255,255 | Lightest | Primary backgrounds, light surfaces |
| 1 | #f4f4f4 | 244,244,244 | | Secondary backgrounds |
| 2 | #e8e8e8 | 232,232,232 | | Hover states, dividers |
| 3 | #d4d4d4 | 212,212,212 | | Borders, subtle separators |
| 5 | #949494 | 148,148,148 | | Disabled text, secondary labels |
| 7 | #6b6b6b | 107,107,107 | | Secondary text |
| 9 | #3e3e3e | 62,62,62 | | Primary text on light backgrounds |
| 11 | #2a2a2a | 42,42,42 | | Dark text, emphasis |
| 12 | #1e1e1e | 30,30,30 | | Very dark text |
| 18 | #000000 | 0,0,0 | Darkest | Maximum contrast, pure black |

**CSS Custom Properties:**
```css
--now-color--neutral-0: 255,255,255;
--now-color--neutral-1: 244,244,244;
--now-color--neutral-2: 232,232,232;
--now-color--neutral-3: 212,212,212;
--now-color--neutral-5: 148,148,148;
--now-color--neutral-7: 107,107,107;
--now-color--neutral-9: 62,62,62;
--now-color--neutral-11: 42,42,42;
--now-color--neutral-12: 30,30,30;
--now-color--neutral-18: 0,0,0;
```

### Interactive & Primary Colors

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| Primary 1 | #0056b3 | 0,86,179 | `--now-color--primary-1` – Links, primary buttons, active states |

**CSS Custom Property:**
```css
--now-color--primary-1: 0,86,179;
```

### Chrome & Navigation Colors

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| Unified Navigation Background | #30302f | 48,48,47 | `--now-unified-nav-bg` – Main navigation chrome |

**CSS Custom Property:**
```css
--now-unified-nav-bg: 48,48,47;
```

### Semantic Alert Colors

ServiceNow provides semantic colors for status communication. Each alert type has a 4-level scale (0 = lightest, 3 = darkest).

#### Critical Alerts (Error/Danger)

| Scale | Hex | RGB | Token | Usage |
|-------|-----|-----|-------|-------|
| 0 (Light BG) | — | — | `--now-color--alert-critical-0` | Light critical background |
| 1 (Medium) | — | — | `--now-color--alert-critical-1` | Medium critical background |
| 2 (Default) | #c8102e | 200,16,46 | `--now-color--alert-critical-2` | Critical text, error indicators |
| 3 (Dark) | — | — | `--now-color--alert-critical-3` | Dark critical foreground |

#### High/Warning Alerts

| Scale | Hex | RGB | Token | Usage |
|-------|-----|-----|-------|-------|
| 0 (Light BG) | — | — | `--now-color--alert-high-0` | Light warning background |
| 1 (Medium) | — | — | `--now-color--alert-high-1` | Medium warning background |
| 2 (Default) | #e86e2c | 232,110,44 | `--now-color--alert-high-2` | Warning text, caution indicators |
| 3 (Dark) | — | — | `--now-color--alert-high-3` | Dark warning foreground |

#### Moderate Alerts (Caution)

| Scale | Hex | RGB | Token | Usage |
|-------|-----|-----|-------|-------|
| 0 (Light BG) | — | — | `--now-color--alert-moderate-0` | Light moderate background |
| 1 (Medium) | — | — | `--now-color--alert-moderate-1` | Medium moderate background |
| 2 (Default) | #eeb422 | 238,180,34 | `--now-color--alert-moderate-2` | Moderate text, attention indicators |
| 3 (Dark) | — | — | `--now-color--alert-moderate-3` | Dark moderate foreground |

#### Success Alerts (Positive)

| Scale | Hex | RGB | Token | Usage |
|-------|-----|-----|-------|-------|
| 0 (Light BG) | — | — | `--now-color--alert-positive-0` | Light success background |
| 1 (Medium) | — | — | `--now-color--alert-positive-1` | Medium success background |
| 2 (Default) | #2e8540 | 46,133,64 | `--now-color--alert-positive-2` | Success text, confirmation icons |
| 3 (Dark) | — | — | `--now-color--alert-positive-3` | Dark success foreground |

#### Info Alerts (Informational)

| Scale | Hex | RGB | Token | Usage |
|-------|-----|-----|-------|-------|
| 0 (Light BG) | — | — | `--now-color--alert-info-0` | Light info background |
| 1 (Medium) | — | — | `--now-color--alert-info-1` | Medium info background |
| 2 (Default) | #0070d2 | 0,112,210 | `--now-color--alert-info-2` | Info text, informational icons |
| 3 (Dark) | — | — | `--now-color--alert-info-3` | Dark info foreground |

**Alert Color CSS Custom Properties:**
```css
/* Critical */
--now-color--alert-critical-0: /* light bg */;
--now-color--alert-critical-1: /* medium */;
--now-color--alert-critical-2: 200,16,46;
--now-color--alert-critical-3: /* dark */;

/* High/Warning */
--now-color--alert-high-0: /* light bg */;
--now-color--alert-high-1: /* medium */;
--now-color--alert-high-2: 232,110,44;
--now-color--alert-high-3: /* dark */;

/* Moderate */
--now-color--alert-moderate-0: /* light bg */;
--now-color--alert-moderate-1: /* medium */;
--now-color--alert-moderate-2: 238,180,34;
--now-color--alert-moderate-3: /* dark */;

/* Positive/Success */
--now-color--alert-positive-0: /* light bg */;
--now-color--alert-positive-1: /* medium */;
--now-color--alert-positive-2: 46,133,64;
--now-color--alert-positive-3: /* dark */;

/* Info */
--now-color--alert-info-0: /* light bg */;
--now-color--alert-info-1: /* medium */;
--now-color--alert-info-2: 0,112,210;
--now-color--alert-info-3: /* dark */;
```

### Color Categories in CSS

ServiceNow organizes colors by semantic purpose:

```css
/* Primary colors */
--now-color--primary-1: 0,86,179;

/* Text-specific colors */
--now-color_text--primary: 30,30,30;
--now-color_text--secondary: 107,107,107;
--now-color_text--disabled: 148,148,148;

/* Background colors */
--now-color_background--primary: 255,255,255;
--now-color_background--secondary: 244,244,244;

/* Border colors */
--now-color_border--primary: 212,212,212;
--now-color_border--secondary: 232,232,232;

/* Surface colors (cards, panels) */
--now-color_surface--primary: 255,255,255;
--now-color_surface--secondary: 244,244,244;

/* Chrome colors (navigation) */
--now-color_chrome--primary: 48,48,47;

/* Brand colors */
--now-color_brand--primary: 42,61,64;
--now-color_brand--accent: 130,182,162;
```

**Implementation Example:**
```css
.alert-critical {
  background-color: rgba(var(--now-color--alert-critical-0), 0.15);
  color: rgb(var(--now-color--alert-critical-2));
  border-left: 4px solid rgb(var(--now-color--alert-critical-2));
}

.button-primary {
  background-color: rgb(var(--now-color--primary-1));
  color: rgb(var(--now-color--neutral-0));
}

.text-secondary {
  color: rgb(var(--now-color_text--secondary));
}
```

---

## Shadows & Elevation

ServiceNow uses a three-level shadow system to indicate depth and elevation. These are defined as `--now-shadow--*` custom properties.

| Token | Shadow Value | CSS Property | Usage |
|-------|--------------|--------------|-------|
| None | `none` | `--now-shadow--none` | Flat surfaces, no elevation |
| Low | `0 1px 2px rgba(0,0,0,0.1)` | `--now-shadow--sm` | Subtle elevation, hover states |
| Medium | `0 2px 8px rgba(0,0,0,0.15)` | `--now-shadow--md` | Cards, modals, dropdowns |
| High | `0 4px 16px rgba(0,0,0,0.2)` | `--now-shadow--lg` | Floating panels, top-level modals |

**CSS Custom Properties:**
```css
--now-shadow--none: none;
--now-shadow--sm: 0 1px 2px rgba(0,0,0,0.1);
--now-shadow--md: 0 2px 8px rgba(0,0,0,0.15);
--now-shadow--lg: 0 4px 16px rgba(0,0,0,0.2);
```

**Implementation Example:**
```css
.card {
  box-shadow: var(--now-shadow--md);
}

.card:hover {
  box-shadow: var(--now-shadow--lg);
}

.button {
  box-shadow: var(--now-shadow--none);
}

button:active {
  box-shadow: var(--now-shadow--sm);
}
```

---

## Border Radius

ServiceNow provides a controlled set of border radius values for consistent corner styling across components.

| Token | Value | CSS Property | Usage |
|-------|-------|--------------|-------|
| Small | 4px | `--now-border-radius--sm` | Buttons, small inputs, form controls |
| Medium | 8px | `--now-border-radius--md` | Modals, dialogs, large cards |
| Large | 16px | `--now-border-radius--lg` | Large containers, feature sections |
| Circle | 50% | `--now-border-radius--circle` | Avatars, circular badges, circular icons |

**CSS Custom Properties:**
```css
--now-border-radius--sm: 4px;
--now-border-radius--md: 8px;
--now-border-radius--lg: 16px;
--now-border-radius--circle: 50%;
```

**Implementation Example:**
```css
button {
  border-radius: var(--now-border-radius--sm);
}

.modal {
  border-radius: var(--now-border-radius--md);
}

.card {
  border-radius: var(--now-border-radius--lg);
}

.avatar {
  border-radius: var(--now-border-radius--circle);
}
```

---

## Icon System

ServiceNow includes a comprehensive icon system with size tokens and style variants.

### Icon Sizes

| Token | Size | CSS Property | Usage |
|-------|------|--------------|-------|
| Small | 12px | `--now-icon-size--sm` | Inline indicators, small text-adjacent icons |
| Medium | 16px | `--now-icon-size--md` | Default size, form fields, inline usage |
| Large | 24px | `--now-icon-size--lg` | Navigation, action icons, section headers |
| Extra Large | 32px | `--now-icon-size--xl` | Feature icons, empty states, large buttons |

**CSS Custom Properties:**
```css
--now-icon-size--sm: 12px;
--now-icon-size--md: 16px;
--now-icon-size--lg: 24px;
--now-icon-size--xl: 32px;
```

### Icon Styles

| Style | Usage |
|-------|-------|
| **Outline** | Default state, non-interactive, secondary actions |
| **Filled** | Active state, selected items, primary actions |

**Implementation Example:**
```css
.icon-default {
  width: var(--now-icon-size--md);
  height: var(--now-icon-size--md);
  /* Use outline icon variant */
}

.icon-active {
  width: var(--now-icon-size--md);
  height: var(--now-icon-size--md);
  /* Use filled icon variant */
}

.icon-large {
  width: var(--now-icon-size--lg);
  height: var(--now-icon-size--lg);
}

.avatar-icon {
  width: var(--now-icon-size--xl);
  height: var(--now-icon-size--xl);
  border-radius: var(--now-border-radius--circle);
}
```

---

## CSS Custom Properties Reference

ServiceNow's theming system uses CSS custom properties with the `--now-*` namespace. The complete theming system includes 1,973 CSS custom properties. Below is a categorized reference of the major property groups.

### Property Naming Conventions

All custom properties follow the `--now-{category}--{subcategory}` or `--now-{category}_{subcategory}--{value}` pattern.

### Color Properties (`--now-color--*` namespace)

```
--now-color--primary-1
--now-color--neutral-0 through --now-color--neutral-18
--now-color--alert-critical-0 through --now-color--alert-critical-3
--now-color--alert-high-0 through --now-color--alert-high-3
--now-color--alert-moderate-0 through --now-color--alert-moderate-3
--now-color--alert-positive-0 through --now-color--alert-positive-3
--now-color--alert-info-0 through --now-color--alert-info-3
```

### Semantic Color Properties

```
--now-color_text--primary
--now-color_text--secondary
--now-color_text--disabled
--now-color_background--primary
--now-color_background--secondary
--now-color_border--primary
--now-color_border--secondary
--now-color_surface--primary
--now-color_surface--secondary
--now-color_chrome--primary
--now-color_brand--primary
--now-color_brand--accent
```

### Typography Properties

```
--now-font-family-heading
--now-font-family-body
--now-font-size-display
--now-font-size-h1 through --now-font-size-h3
--now-font-size-body-lg, --now-font-size-body-md, --now-font-size-body-sm
--now-font-size-button
--now-font-weight-display
--now-font-weight-h1 through --now-font-weight-h3
--now-font-weight-body-lg, --now-font-weight-body-md, --now-font-weight-body-sm
--now-font-weight-button
--now-line-height-display
--now-line-height-h1 through --now-line-height-h3
--now-line-height-body-lg, --now-line-height-body-md, --now-line-height-body-sm
--now-line-height-button
```

### Spacing Properties

```
--now-spacing-xxs through --now-spacing-3xl
```

### Shadow Properties

```
--now-shadow--none
--now-shadow--sm
--now-shadow--md
--now-shadow--lg
```

### Border Radius Properties

```
--now-border-radius--sm
--now-border-radius--md
--now-border-radius--lg
--now-border-radius--circle
```

### Icon Size Properties

```
--now-icon-size--sm
--now-icon-size--md
--now-icon-size--lg
--now-icon-size--xl
```

### Navigation Properties

```
--now-unified-nav-bg
--now-unified-nav--* (additional navigation-specific tokens)
```

### Complete Property Directory

For the exhaustive list of all 1,973 CSS custom properties, refer to the official ServiceNow theming documentation at **theme.deoprototypes.com/hooks**.

---

## Theme JSON Structure

ServiceNow themes are defined using JSON configuration files that map CSS custom property names to RGB triplet values. Understanding this structure is critical for programmatic theme generation and modification.

### JSON Format Specification

**Critical Rule:** All RGB values MUST be formatted as `"R,G,B"` (comma-separated integers WITHOUT spaces). Spaces in RGB triplets will cause blank-page rendering errors.

### Correct vs. Incorrect Format

**CORRECT:**
```json
{
  "--now-color--primary-1": "0,86,179",
  "--now-color--neutral-0": "255,255,255",
  "--now-color_text--primary": "30,30,30"
}
```

**INCORRECT (will break):**
```json
{
  "--now-color--primary-1": "0, 86, 179",
  "--now-color--neutral-0": "255, 255, 255",
  "--now-color_text--primary": "30, 30, 30"
}
```

### Example Theme JSON Structure

```json
{
  "_metadata": {
    "name": "ServiceNow Horizon Light",
    "version": "1.0.0",
    "variant": "light"
  },
  "colors": {
    "--now-color--primary-1": "0,86,179",
    "--now-color--neutral-0": "255,255,255",
    "--now-color--neutral-1": "244,244,244",
    "--now-color--neutral-2": "232,232,232",
    "--now-color--neutral-3": "212,212,212",
    "--now-color--neutral-5": "148,148,148",
    "--now-color--neutral-7": "107,107,107",
    "--now-color--neutral-9": "62,62,62",
    "--now-color--neutral-11": "42,42,42",
    "--now-color--neutral-12": "30,30,30",
    "--now-color--neutral-18": "0,0,0",
    "--now-color--alert-critical-2": "200,16,46",
    "--now-color--alert-high-2": "232,110,44",
    "--now-color--alert-moderate-2": "238,180,34",
    "--now-color--alert-positive-2": "46,133,64",
    "--now-color--alert-info-2": "0,112,210"
  },
  "semanticColors": {
    "--now-color_text--primary": "30,30,30",
    "--now-color_text--secondary": "107,107,107",
    "--now-color_text--disabled": "148,148,148",
    "--now-color_background--primary": "255,255,255",
    "--now-color_background--secondary": "244,244,244",
    "--now-color_border--primary": "212,212,212",
    "--now-color_border--secondary": "232,232,232",
    "--now-color_surface--primary": "255,255,255",
    "--now-color_surface--secondary": "244,244,244",
    "--now-color_chrome--primary": "48,48,47",
    "--now-color_brand--primary": "42,61,64",
    "--now-color_brand--accent": "130,182,162"
  },
  "typography": {
    "--now-font-family-heading": "'Cabin', sans-serif",
    "--now-font-family-body": "'Lato', Arial, sans-serif",
    "--now-font-size-display": "64px",
    "--now-font-weight-display": "700",
    "--now-line-height-display": "1.15"
  },
  "spacing": {
    "--now-spacing-xxs": "2px",
    "--now-spacing-xs": "4px",
    "--now-spacing-sm": "8px",
    "--now-spacing-md": "12px",
    "--now-spacing-lg": "16px",
    "--now-spacing-xl": "24px",
    "--now-spacing-xxl": "32px",
    "--now-spacing-3xl": "40px"
  },
  "elevation": {
    "--now-shadow--none": "none",
    "--now-shadow--sm": "0 1px 2px rgba(0,0,0,0.1)",
    "--now-shadow--md": "0 2px 8px rgba(0,0,0,0.15)",
    "--now-shadow--lg": "0 4px 16px rgba(0,0,0,0.2)"
  },
  "borders": {
    "--now-border-radius--sm": "4px",
    "--now-border-radius--md": "8px",
    "--now-border-radius--lg": "16px",
    "--now-border-radius--circle": "50%"
  },
  "icons": {
    "--now-icon-size--sm": "12px",
    "--now-icon-size--md": "16px",
    "--now-icon-size--lg": "24px",
    "--now-icon-size--xl": "32px"
  }
}
```

### Applying Theme JSON

To apply a theme JSON to your application, inject the values as CSS custom properties:

```javascript
function applyTheme(themeJson) {
  const root = document.documentElement;

  Object.entries(themeJson.colors || {}).forEach(([property, value]) => {
    root.style.setProperty(property, value);
  });

  Object.entries(themeJson.semanticColors || {}).forEach(([property, value]) => {
    root.style.setProperty(property, value);
  });

  // Apply typography, spacing, elevation, etc.
  Object.entries(themeJson.typography || {}).forEach(([property, value]) => {
    root.style.setProperty(property, value);
  });
}
```

---

## Implementation Guidelines

### General Best Practices

1. **Always Use CSS Custom Properties**: Never hardcode color, spacing, or typography values. Always reference the appropriate `--now-*` custom property.

2. **RGB Format in Themes**: When working with theme JSON, always use the RGB triplet format without spaces: `"R,G,B"` not `"R, G, B"`.

3. **Semantic Color Usage**: Use semantic color properties (`--now-color_text--*`, `--now-color_background--*`, etc.) when possible for better maintainability and theme switching.

4. **Responsive Grids**: Always respect the grid system's margin (24px) and gutter (48px) values. Adjust column count based on breakpoints.

5. **Typography Hierarchy**: Use the defined type scale consistently. Don't create custom font sizes between the defined tokens.

6. **Spacing Scale Adherence**: Use only the defined spacing tokens (xxs through 3xl). This ensures visual consistency.

### Color Implementation Patterns

**Status/Alert Patterns:**
```css
/* Critical alert */
.alert-critical {
  background-color: rgba(var(--now-color--alert-critical-0), 0.2);
  border-left: 4px solid rgb(var(--now-color--alert-critical-2));
  color: rgb(var(--now-color--alert-critical-2));
}

/* Success confirmation */
.alert-success {
  background-color: rgba(var(--now-color--alert-positive-0), 0.2);
  border-left: 4px solid rgb(var(--now-color--alert-positive-2));
  color: rgb(var(--now-color--alert-positive-2));
}

/* Info message */
.alert-info {
  background-color: rgba(var(--now-color--alert-info-0), 0.2);
  border-left: 4px solid rgb(var(--now-color--alert-info-2));
  color: rgb(var(--now-color--alert-info-2));
}
```

**Interaction Patterns:**
```css
/* Primary button - default state */
.button-primary {
  background-color: rgb(var(--now-color--primary-1));
  color: rgb(var(--now-color--neutral-0));
  border-radius: var(--now-border-radius--sm);
  padding: var(--now-spacing-sm) var(--now-spacing-md);
  font: var(--now-font-weight-button) var(--now-font-size-button) / var(--now-line-height-button) var(--now-font-family-heading);
}

/* Primary button - hover state */
.button-primary:hover {
  box-shadow: var(--now-shadow--sm);
  /* darken or adjust background */
}

/* Primary button - active state */
.button-primary:active {
  box-shadow: var(--now-shadow--md);
}

/* Primary button - disabled state */
.button-primary:disabled {
  background-color: rgb(var(--now-color_text--disabled));
  color: rgb(var(--now-color_background--secondary));
  cursor: not-allowed;
  opacity: 0.6;
}
```

**Card/Surface Patterns:**
```css
.card {
  background-color: rgb(var(--now-color_surface--primary));
  border: 1px solid rgb(var(--now-color_border--primary));
  border-radius: var(--now-border-radius--lg);
  padding: var(--now-spacing-lg);
  box-shadow: var(--now-shadow--md);
}

.card:hover {
  box-shadow: var(--now-shadow--lg);
  background-color: rgb(var(--now-color_surface--secondary));
}
```

**Text Patterns:**
```css
.text-primary {
  color: rgb(var(--now-color_text--primary));
  font-size: var(--now-font-size-body-md);
  font-weight: var(--now-font-weight-body-md);
  line-height: var(--now-line-height-body-md);
}

.text-secondary {
  color: rgb(var(--now-color_text--secondary));
  font-size: var(--now-font-size-body-sm);
  font-weight: var(--now-font-weight-body-md);
  line-height: var(--now-line-height-body-md);
}

.text-disabled {
  color: rgb(var(--now-color_text--disabled));
}
```

### Layout Implementation Patterns

**Grid Container:**
```css
.container {
  max-width: var(--now-grid-max-width-standard);
  margin: 0 auto;
  padding: 0 var(--now-grid-margin);
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--now-grid-gutter);
}

@media (min-width: 1600px) {
  .container {
    max-width: var(--now-grid-max-width-wide);
  }
}
```

**Spacing Utilities:**
```css
.p-sm { padding: var(--now-spacing-sm); }
.p-md { padding: var(--now-spacing-md); }
.p-lg { padding: var(--now-spacing-lg); }

.m-bottom-sm { margin-bottom: var(--now-spacing-sm); }
.m-bottom-md { margin-bottom: var(--now-spacing-md); }
.m-bottom-lg { margin-bottom: var(--now-spacing-lg); }

.gap-sm { gap: var(--now-spacing-sm); }
.gap-md { gap: var(--now-spacing-md); }
.gap-lg { gap: var(--now-spacing-lg); }
```

### Accessibility Considerations

1. **Color Contrast**: Always verify that text and interactive elements meet WCAG AA contrast ratios (4.5:1 for body text, 3:1 for large text).

2. **Semantic Meaning**: Don't rely solely on color to convey information. Use icons, text labels, and patterns in addition to color.

3. **Focus States**: Always provide visible focus indicators for interactive elements using sufficient contrast.

4. **Typography Scale**: The defined type scale is designed for readability. Don't deviate from these sizes.

### Testing & Validation

1. **Theme Validation**: Ensure theme JSON uses correct RGB format without spaces.
2. **Color Contrast Testing**: Use tools like WebAIM's Contrast Checker for critical interfaces.
3. **Responsive Testing**: Test grid layouts at both 1280px and 1600px breakpoints.
4. **Browser Compatibility**: CSS custom properties are widely supported but ensure fallbacks for older browsers if needed.

---

## Quick Reference Tables

### Spacing Token Quick Reference

| xxxs | xs | sm | md | lg | xl | xxl | 3xl |
|------|----|----|----|----|----|----|-----|
| 2px | 4px | 8px | 12px | 16px | 24px | 32px | 40px |

### Color Palette Quick Reference

**Neutrals:** #ffffff, #f4f4f4, #e8e8e8, #d4d4d4, #949494, #6b6b6b, #3e3e3e, #2a2a2a, #1e1e1e, #000000

**Primary:** #0056b3

**Semantic (Alert):**
- Critical: #c8102e
- High: #e86e2c
- Moderate: #eeb422
- Positive: #2e8540
- Info: #0070d2

### Typography Sizes

| Display | H1 | H2 | H3 | Body LG | Body MD | Body SM | Button |
|---------|----|----|----|---------|---------|---------| -------|
| 64px | 32px | 24px | 20px | 16px | 14px | 12px | 14px |

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-11 | Initial comprehensive reference document extracted from ServiceNow Horizon Design System |

---

**Document Classification:** Design System Reference
**Last Updated:** 2026-03-11
**Data Source:** ServiceNow Horizon Design System, Figma Component Libraries, CSS Theming Hooks

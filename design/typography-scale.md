# Sovereign CRM Typography Scale

## Core Philosophy
Typography is the voice of our interface. We use **Inter** - a typeface specifically designed for computer screens - to achieve crystal-clear readability, professional sophistication, and subtle warmth. Our typographic system creates instant visual hierarchy while maintaining the calm, luxurious feel essential for prolonged professional use.

## Typeface Selection: Inter

### Why Inter?
- **Designed for Screens**: Optimized for pixel grids and rendering technologies
- **Excellent Legibility**: Large x-height, open apertures, distinct letterforms
- **Versatile Family**: 9 weights from Thin to Black for nuanced hierarchy
- **Numerical Clarity**: Distinguished numerals (langing figures option) for data density
- **Neutral Personality**: Professional without being cold, modern without trendiness
- **Open Source**: Free for commercial use, excellent community support

### Characteristics Supporting Our Goals:
- **Calm**: Even stroke weights, minimal contrast, restrained personality
- **Clarity**: Open counters, clear distinctions between similar characters (IL1, 0O)
- **Professional**: Geometric precision with humanist touches
- **Luxury**: Refined details visible at larger sizes, substantial presence in weights
- **Curiosity**: Inviting readability encourages exploration of content

## Typographic Scale

Our scale follows a **modular ratio** based on the minor third (1.2x) for harmonious progression, with special consideration for data-dense contexts.

### Base Size: 16px
All other sizes are derived from this foundation for consistent vertical rhythm.

| Token | Size (px) | Size (rem) | Weight | Use Case | Psychological Effect |
|-------|-----------|------------|--------|----------|----------------------|
| **--text-display** | 48px | 3rem | Black 900 | Dashboard titles, major section headers | Authority, presence, importance |
| **--text-heading-xl** | 40px | 2.5rem | Black 900 | Report titles, major dashboard widgets | Significance, focus, establishment |
| **--text-heading-lg** | 32px | 2rem | ExtraBold 800 | Section headers, card titles | Structure, organization, clarity |
| **--text-heading-md** | 24px | 1.5rem | SemiBold 600 | Widget headers, table headers, form sections | Guidance, categorization, hierarchy |
| **--text-heading-sm** | 20px | 1.25rem | Medium 500 | Subsection headers, detailed labels | Definition, specificity, detail |
| **--text-body-lg** | 18px | 1.125rem | Regular 400 | Body text (preferred for reading blocks) | Comfort, accessibility, readability |
| **--text-body** | 16px | 1rem | Regular 400 | Primary body text, form labels, help text | Standard, neutral, dependable |
| **--text-body-sm** | 14px | 0.875rem | Regular 400 | Metadata, captions, auxiliary text | Supporting, contextual, unobtrusive |
| **--text-label** | 12px | 0.75rem | Medium 500 | Form field labels, table column headers | Precision, instruction, clarity |
| **--text-caption** | 11px | 0.6875rem | Light 300 | Fine print, timestamps, status tags | Discreet, supplementary, de-emphasized |
| **--text-overline** | 9px | 0.5625rem | Regular 400 | Data prefixes, unit labels, codes | Technical, precise, minimal |

### Data-Specific Typography
For optimal readability of numerical and technical information.

| Token | Size (px) | Size (rem) | Weight | Use Case | Notes |
|-------|-----------|------------|--------|----------|-------|
| **--text-data-lg** | 24px | 1.5rem | Medium 500 | Key metrics, KPIs, major numbers | Prominent, scannable |
| **--text-data** | 20px | 1.25rem | Medium 500 | Regular data points, table values | Clear, readable |
| **--text-data-sm** | 18px | 1.125rem | Regular 400 | Secondary data, detailed values | Comfortable for dense tables |
| **--text-data-xs** | 16px | 1rem | Regular 400 | Tertiary data, footnotes, details | Space-efficient readability |
| **--text-mono** | 14px | 0.875rem | Regular 400 | Codes, IDs, timestamps, technical data | Inter Mono for alignment |

## Typographic Properties

### Line Heights (Leading)
Proper vertical spacing enhances readability and creates rhythmic vertical flow.

| Context | Line Height | Ratio to Font Size | Use Case |
|---------|-------------|-------------------|----------|
| **Display/Heading** | 1.1 | Tight for impact | Short texts needing prominence |
| **Body Text** | 1.6 | Open for readability | Paragraphs, long-form content |
| **Body Compact** | 1.4 | Balanced efficiency | Forms, tables, data grids |
| **Label/Captions** | 1.2 | Minimal for density | Metadata, forms, tables |
| **Data/Numbers** | 1.3 | Slightly open for clarity | Numerical readability |
| **Mono/Code** | 1.5 | Open for character distinction | Technical accuracy |

### Letter Spacing (Tracking)
Subtle adjustments for optimal appearance at different sizes.

| Size Range | Letter Spacing | Purpose |
|------------|----------------|---------|
| **Display (24px+)** | -0.5px | Tighten for impact and cohesion |
| **Heading (18-23px)** | 0px | Natural spacing |
| **Body (16px)** | 0px | Standard readability |
| **Small Text (<16px)** | +0.25px | Compensate for perceived tightness |
| **Uppercase/Labels** | +0.5px | Enhance legibility of caps |
| **Numbers/Data** | 0px | Maintain alignment integrity |

### Font Weight Guidelines
Strategic use of weight creates hierarchy without visual noise.

| Weight | Use Case | Psychological Effect |
|--------|----------|----------------------|
| **Black 900** | Display titles, critical headers | Authority, importance, permanence |
| **ExtraBold 800** | Major section headers, report titles | Significance, establishment |
| **SemiBold 600** | Widget headers, form sections, labels | Guidance, structure, clarity |
| **Medium 500** | Data points, key metrics, interactive labels | Precision, readability, engagement |
| **Regular 400** | Body text, paragraphs, detailed content | Neutrality, readability, comfort |
| **Light 300** | Captions, metadata, supporting text | Subtlety, context, de-emphasis |

## Hierarchy & Application Principles

### Visual Hierarchy Through Typography
Create instant understanding of information importance and relationships.

1. **Primary Hierarchy** (What to read first)
   - Display > Heading XL > Heading LG > Heading MD
   - Uses size and weight jumps for clear separation

2. **Secondary Hierarchy** (Supporting information)
   - Heading SM > Body LG > Body > Body SM
   - Gradual progression for comfortable reading

3. **Tertiary Hierarchy** (Metadata, context)
   - Label > Caption > Overline
   - Smaller sizes, lighter weights for de-emphasis

### Specific Component Applications

#### Navigation
- **Sidebar Items**: `--text-body` (16px, Regular) for items, `--text-label` (12px, Medium) for section headers
- **Active States**: Use `--text-heading-sm` (20px, Medium) for emphasis when needed
- **Icons + Text**: Maintain baseline alignment, 4px spacing between icon and text

#### Dashboards
- **Widget Titles**: `--text-heading-md` (24px, SemiBold) - Clear section identification
- **Metric Values**: `--text-data-lg` (24px, Medium) or `--text-heading-lg` (32px, ExtraBold) for KPIs
- **Metric Labels**: `--text-body-sm` (14px, Regular) - Context without competition
- **Trend Indicators**: `--text-caption` (11px, Light) - Supplementary direction arrows
- **Section Dividers**: Use spacing rather than lines; when needed, `--text-overline` (9px) for subtle separation

#### Forms & Data Entry
- **Field Labels**: `--text-label` (12px, Medium) - Clear instruction, top-aligned
- **Input Text**: `--text-body` (16px, Regular) - Standard readability
- **Placeholder Text**: `--text-body-sm` (14px, Regular) at 60% opacity - Instructional but not dominant
- **Help Text**: `--text-caption` (11px, Light) - Available but unobtrusive
- **Validation States**: 
  - Error: `--text-body-sm` (14px, Regular) in Error Red (`#EF4444`)
  - Success: `--text-body-sm` (14px, Regular) in Success Green (`#10B981`)
  - Warning: `--text-body-sm` (14px, Regular) in Warning Amber (`#F59E0B`)

#### Tables & Data Grids
- **Header Cells**: `--text-heading-sm` (20px, Medium, 600) - Clear column definition
- **Body Cells**: `--text-body` (16px, Regular) - Readable data presentation
- **Numeric Cells**: `--text-data` (20px, Medium) - Enhanced numerical clarity
- **Timestamp Cells**: `--text-caption` (11px, Light) - Unobtrusive metadata
- **Status Cells**: `--text-label` (12px, Medium) with appropriate status color
- **Row Height**: Minimum 48px (3x base size) for touch comfort and readability

#### Cards & Containers
- **Card Title**: `--text-heading-md` (24px, SemiBold) - Section identification within card
- **Card Body**: `--text-body` (16px, Regular) - Primary content area
- **Card Footer**: `--text-body-sm` (14px, Regular) - Actions, metadata, supplementary info
- **Badges/Tags**: `--text-label` (12px, Medium, 500) - Compact information display

#### Modals & Overlays
- **Modal Title**: `--text-heading-lg` (32px, ExtraBold) - Clear purpose establishment
- **Modal Body**: `--text-body-lg` (18px, Regular) - Comfortable reading for explanations
- **Form Fields**: Same as main form standards
- **Action Buttons**: Follow button typography guidelines below

#### Reports & Analytics
- **Report Title**: `--text-display` (48px, Black 900) - Document-level importance
- **Section Headers**: `--text-heading-xl` (40px, Black 900) - Major breakdowns
- **Subsection Headers**: `--text-heading-lg` (32px, ExtraBold) - Detailed divisions
- **Chart Titles**: `--text-heading-md` (24px, SemiBold) - Axis-free identification
- **Axis Labels**: `--text-body-sm` (14px, Regular) - Clear but not dominant
- **Data Labels**: `--text-caption` (11px, Regular) - Precise when needed
- **Legend Text**: `--text-body` (16px, Regular) - Readable reference
- **Footnotes/Source**: `--text-overline` (9px, Light) - Attribution without distraction

#### Buttons & Interactive Elements
- **Primary Button Text**: `--text-body` (16px, Medium 500) - Clear call-to-action
- **Secondary Button Text**: `--text-body` (16px, Regular 400) - Neutral action
- **Icon Buttons**: Ensure icon size matches text height for balance
- **Link Text**: `--text-body` (16px, Regular 400) - Standard paragraph integration
- **Link Hover**: Underline or slight weight increase to Medium 500
- **Badge/Text on Buttons**: `--text-label` (12px, Medium 500) - Compact supplementary info

#### Notifications & Alerts
- **Notification Title**: `--text-heading-sm` (20px, SemiBold 600) - Clear, scannable
- **Notification Body**: `--text-body` (16px, Regular 400) - Readable message
- **Notification Timestamp**: `--text-caption` (11px, Light 300) - Unobtrusive timing
- **Alert Banner**: Same as notification but full-width
- **Toast Messages**: `--text-body-sm` (14px, Regular 400) - Brief, temporary info

## Spacing & Rhythm

### Vertical Rhythm
Maintain consistent vertical spacing based on our 8pt grid system.

| Space Token | Size (px) | Use Case |
|-------------|-----------|----------|
| **--space-2xs** | 4px | Tight coupling (label to input) |
| **--space-xs** | 8px | Related elements, dense layouts |
| **--space-sm** | 12px | Standard paragraph spacing |
| **--space-md** | 16px | Section separation, card padding |
| **--space-lg** | 24px | Major section breaks, card margins |
| **--space-xl** | 32px | Page margins, major component separation |
| **--space-2xl** | 48px | Major content divisions, dashboard widget spacing |
| **--space-3xl** | 64px | Page sections, major content blocks |

### Paragraph Spacing
- **Paragraph Margin Bottom**: `--space-sm` (12px) or `--space-md` (16px) depending on density
- **Heading Margin Top**: `--space-lg` (24px) to separate from previous content
- **Heading Margin Bottom**: `--space-sm` (12px) to connect to following content
- **List Item Spacing**: `--space-xs` (8px) between items, `--space-sm` (12px) after list

### Horizontal Spacing
- **Input Padding**: `--space-sm` (12px) vertical, `--space-md` (16px) horizontal
- **Button Padding**: `--space-sm` (12px) vertical, `--space-lg` (24px) horizontal
- **Card Padding**: `--space-lg` (24px) all sides for balanced breathing room
- **Table Cell Padding**: `--space-sm` (12px) all sides for data readability
- **Menu Item Padding**: `--space-xs` (8px) vertical, `--space-sm` (12px) horizontal

## Implementation Guidelines for Developers

### CSS Custom Properties
```css
:root {
  /* Font Family */
  --font-family-base: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-family-mono: 'Inter Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  
  /* Font Weights */
  --font-weight-light: 300;
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --font-weight-extrabold: 800;
  --font-weight-black: 900;
  
  /* Font Sizes */
  --text-display: 48px;
  --text-heading-xl: 40px;
  --text-heading-lg: 32px;
  --text-heading-md: 24px;
  --text-heading-sm: 20px;
  --text-body-lg: 18px;
  --text-body: 16px;
  --text-body-sm: 14px;
  --text-label: 12px;
  --text-caption: 11px;
  --text-overline: 9px;
  
  /* Data-specific sizes */
  --text-data-lg: 24px;
  --text-data: 20px;
  --text-data-sm: 18px;
  --text-data-xs: 16px;
  
  /* Line Heights */
  --leading-tight: 1.1;
  --leading-snug: 1.2;
  --leading-normal: 1.4;
  --leading-relaxed: 1.6;
  --leading-loose: 1.8;
  
  /* Letter Spacing */
  --tracking-tighter: -0.5px;
  --tracking-tight: -0.25px;
  --tracking-normal: 0px;
  --tracking-wide: 0.25px;
  --tracking-wider: 0.5px;
  --tracking-widest: 0.5px; /* for uppercase */
}
```

### Usage Examples
```css
/* Dashboard title */
.dashboard-title {
  font-size: var(--text-display);
  font-weight: var(--font-weight-black);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tighter);
  margin-bottom: var(--space-lg);
}

/* Widget header */
.widget-header {
  font-size: var(--text-heading-md);
  font-weight: var(--font-weight-semibold);
  line-height: var(--leading-snug);
  margin-bottom: var(--space-sm);
}

/* Body text */
.body-text {
  font-size: var(--text-body);
  font-weight: var(--font-weight-regular);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-sm);
}

/* Data metric */
.data-metric {
  font-size: var(--text-data-lg);
  font-weight: var(--font-weight-medium);
  line-height: var(--leading-snug);
}

/* Form label */
.form-label {
  font-size: var(--text-label);
  font-weight: var(--font-weight-medium);
  text-transform: uppercase;
  letter-spacing: var(--tracking-widest);
  margin-bottom: var(--space-2xs);
}

/* Caption text */
.caption-text {
  font-size: var(--text-caption);
  font-weight: var(--font-weight-light);
  line-height: var(--leading-snug);
}

/* Monospace data */
.mono-data {
  font-family: var(--font-family-mono);
  font-size: var(--text-data-sm);
  font-weight: var(--font-weight-regular);
  letter-spacing: var(--tracking-normal);
}
```

### Component-Specific CSS
```css
/* Navigation */
.nav-item {
  font-size: var(--text-body);
  font-weight: var(--font-weight-regular);
  line-height: var(--leading-snug);
}

.nav-item.active {
  font-weight: var(--font-weight-semibold);
}

.nav-section-header {
  font-size: var(--text-label);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-widest);
}

/* Forms */
.form-field-label {
  font-size: var(--text-label);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-2xs);
}

.form-input {
  font-size: var(--text-body);
  font-weight: var(--font-weight-regular);
  padding: var(--space-sm) var(--space-md);
}

.form-help-text {
  font-size: var(--text-caption);
  font-weight: var(--font-weight-light);
  margin-top: var(--space-2xs);
}

/* Tables */
.table-header {
  font-size: var(--text-heading-sm);
  font-weight: var(--font-weight-semibold);
  text-align: left;
  padding: var(--space-sm);
}

.table-cell {
  font-size: var(--text-body);
  font-weight: var(--font-weight-regular);
  padding: var(--space-sm);
}

.table-cell.numeric {
  font-family: var(--font-family-mono);
  font-size: var(--text-data);
  font-weight: var(--font-weight-medium);
}

/* Cards */
.card-title {
  font-size: var(--text-heading-md);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-sm);
}

.card-body {
  font-size: var(--text-body);
  font-weight: var(--font-weight-regular);
  line-height: var(--leading-relaxed);
}

.card-footer {
  font-size: var(--text-body-sm);
  font-weight: var(--font-weight-regular);
  margin-top: var(--space-lg);
}

/* Buttons */
.button-primary {
  font-size: var(--text-body);
  font-weight: var(--font-weight-medium);
  padding: var(--space-sm) var(--space-lg);
}

.button-secondary {
  font-size: var(--text-body);
  font-weight: var(--font-weight-regular);
  padding: var(--space-sm) var(--space-lg);
}

/* Notifications */
.notification-title {
  font-size: var(--text-heading-sm);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-2xs);
}

.notification-body {
  font-size: var(--text-body);
  font-weight: var(--font-weight-regular);
  line-height: var(--leading-relaxed);
}

.notification-timestamp {
  font-size: var(--text-caption);
  font-weight: var(--font-weight-light);
}

/* Reports */
.report-title {
  font-size: var(--text-display);
  font-weight: var(--font-weight-black);
  line-height: var(--leading-tight);
  margin-bottom: var(--space-lg);
}

.report-section-title {
  font-size: var(--text-heading-xl);
  font-weight: var(--font-weight-black);
  margin-bottom: var(--space-md);
}

.chart-title {
  font-size: var(--text-heading-md);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-sm);
}

.axis-label {
  font-size: var(--text-body-sm);
  font-weight: var(--font-weight-regular);
}

.legend-item {
  font-size: var(--text-body);
  font-weight: var(--font-weight-regular);
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}

.footnote {
  font-size: var(--text-overline);
  font-weight: var(--font-weight-light);
  margin-top: var(--space-lg);
}
```

## Accessibility Considerations

### Font Size Minimums
- **Minimum body text**: 16px (our base) - Ensures readability without zoom
- **Minimum labels/captions**: 12px - Still readable with good contrast
- **Never go below 10px** for any functional text

### Contrast & Legibility
- All text sizes paired with appropriate weights for 4.5:1 contrast minimum
- Avoid Light 300 weights below 16px on complex backgrounds
- Use Medium 500 or better for small text (<14px) requiring legibility

### Dyslexia & Readability Features
- Inter's open apertures help distinguish similar characters
- Consistent letterforms reduce cognitive load
- Proper spacing prevents crowding and word shape confusion
- Consider offering alternative fonts (OpenDyslexic) as user preference

### Internationalization & Localization
- **Text Expansion**: Design for up to 30% expansion (German, Finnish)
- **Vertical Scripts**: Ensure components accommodate vertical layout when needed
- **CJK Support**: Inter includes good CJK fallback; test with target languages
- **Right-to-Left**: Mirror horizontal spacing, maintain typographic proportions

## Implementation Notes

### Web Font Loading Strategy
For optimal performance and minimal layout shift:

```css
/* Preload critical font weights */
<link rel="preload" href="/fonts/Inter-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/Inter-Medium.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/Inter-SemiBold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/Inter-ExtraBold.woff2" as="font" type="font/woff2" crossorigin>

/* Define font faces */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 300;
  font-display: swap;
  src: url('/fonts/Inter-Light.woff2') format('woff2');
}

@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('/fonts/Inter-Regular.woff2') format('woff2');
}

/* ... continue for other weights */
```

### Fallback Strategy
```css
body {
  font-family: var(--font-family-base);
  /* Safe fallbacks in order of preference */
  /* System UI fonts first for native feel */
  /* Then widely available sans-serifs */
}

/* For mono */
.mono-element {
  font-family: var(--font-family-mono);
}
```

### Variable Fonts (Future Consideration)
If adopting variable fonts:
```css
@font-face {
  font-family: 'Inter Variable';
  font-style: normal;
  font-weight: 1 999;
  font-display: swap;
  src: url('/fonts/Inter-Variable.woff2') format('woff2-variations');
}

:root {
  --font-family-base: 'Inter Variable', fallback-fonts;
}
```

## Maintenance & Evolution

### Typography Governance
1. **Weight Justification** - New weights must solve specific hierarchy problems
2. **Size Consistency** - New sizes must fit the modular scale or justify deviation
3. **Accessibility Check** - New combinations tested for contrast and readability
4. **Performance Impact** - Additional font weights measured for loading impact

### Future-Proofing
- **Modular Scale** - Easy to extend while maintaining harmony
- **CSS Variables** - Simple to update values site-wide
- **Font Loading** - Strategy supports progressive enhancement
- **Component Tokens** - Semantic usage allows evolution without breaking changes

### Partnership with Color System
Typography works hand-in-hand with our color system:
- **Weight + Color** - Semantic Bold + Accent Gold for primary actions
- **Size + Color** - Larger sizes with muted colors for hierarchy
- **Spacing + Color** - Proper separation enhances color-defined sections

---
*Typography scale document for Sovereign CRM design reference. Stored in Sovereign Vault as design/typography-scale.md
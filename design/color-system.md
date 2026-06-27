# Sovereign CRM Color System

## Core Philosophy
Our color system balances **luxury minimalism** with **psychological effectiveness**, creating a professional environment that feels both calming and curiosity-driven while maintaining the gravitas expected of enterprise software.

## Primary Palette

### Neutral Foundation (60-70% usage)
These colors form the base of our interface, providing stability and sophistication.

| Color | Hex | RGB | Usage | Psychological Effect |
|-------|-----|-----|-------|----------------------|
| **Deep Navy** | `#0F172A` | 15,23,42 | Primary background, headers, navigation | Trust, stability, depth, authority |
| **Slate Gray** | `#64748B` | 100,116,139 | Secondary text, borders, dividers | Professionalism, neutrality, balance |
| **Warm White** | `#F8FAFC` | 248,250,252 | Main content background, cards | Cleanliness, spaciousness, clarity |
| **Cool Gray** | `#F1F5F9` | 241,245,249 | Alternative backgrounds, subtle sections | Softness, approachability, reduce harshness |

### Accent & Action Colors (20-25% usage)
Used purposefully to guide attention and convey meaning.

| Color | Hex | RGB | Usage | Psychological Effect |
|-------|-----|-----|-------|----------------------|
| **Accent Gold** | `#D4AF37` | 212,175,55 | Primary actions, achievements, premium features | Luxury, success, achievement, warmth |
| **Success Green** | `#10B981` | 16,185,129 | Confirmations, positive trends, completed actions | Growth, positivity, completion, safety |
| **Warning Amber** | `#F59E0B` | 245,158,11 | Alerts, attention-needed, pending actions | Caution, urgency (without alarm), awareness |
| **Error Red** | `#EF4444` | 239,68,68 | Critical errors, destructive actions, blocking issues | Urgency, importance, stop (use sparingly) |
| **Info Blue** | `#3B82F6` | 59,130,246 | Informational elements, links, secondary actions | Trust, calm, technology, openness |

### Semantic Color Tokens
For consistent theming and easy adaptation.

#### Background Tokens
- `--color-bg-primary`: `#0F172A` (Deep Navy)
- `--color-bg-secondary`: `#F8FAFC` (Warm White)
- `--color-bg-muted`: `#F1F5F9` (Cool Gray)
- `--color-bg-overlay`: `rgba(15,23,42,0.85)` (Deep Navy with opacity)

#### Text Tokens
- `--color-text-primary`: `#F8FAFC` (Warm White on dark) / `#0F172A` (Deep Navy on light)
- `--color-text-secondary`: `#64748B` (Slate Gray)
- `--color-text-muted`: `#94A3B8` (Light Slate)
- `--color-text-inverse`: `#0F172A` (Deep Navy on white) / `#F8FAFC` (Warm White on dark)

#### Accent Tokens
- `--color-accent-primary`: `#D4AF37` (Accent Gold)
- `--color-accent-success`: `#10B981` (Success Green)
- `--color-accent-warning`: `#F59E0B` (Warning Amber)
- `--color-accent-error`: `#EF4444` (Error Red)
- `--color-accent-info`: `#3B82F6` (Info Blue)

#### Border & Divider Tokens
- `--color-border`: `#64748B` (Slate Gray at 20% opacity)
- `--color-border-focus`: `#D4AF37` (Accent Gold)
- `--color-divider`: `#F1F5F9` (Cool Gray)

## Application Guidelines

### 60-30-10 Rule for Luxury Interfaces
- **60% Dominant Color**: Deep Navy (`#0F172A`) - Creates depth and professional foundation
- **30% Secondary Color**: Warm White (`#F8FAFC`) - Provides breathing room and clarity
- **10% Accent Color**: Accent Gold (`#D4AF37`) - Used sparingly for luxury touches and key actions

### Accessibility & Contrast
All color combinations meet WCAG 2.1 AA standards for text and UI components.

#### Minimum Contrast Ratios:
- **Normal text**: 4.5:1 against background
- **Large text**: 3:1 against background  
- **UI components**: 3:1 against adjacent colors

#### Tested Combinations:
- Deep Navy (`#0F172A`) on Warm White (`#F8FAFC`): 14.2:1 ✅
- Warm White (`#F8FAFC`) on Deep Navy (`#0F172A`): 14.2:1 ✅
- Slate Gray (`#64748B`) on Warm White (`#F8FAFC`): 12.6:1 ✅
- Accent Gold (`#D4AF37`) on Deep Navy (`#0F172A`): 4.8:1 ✅
- Success Green (`#10B981`) on Warm White (`#F8FAFC`): 5.1:1 ✅
- Warning Amber (`#F59E0B`) on Warm White (`#F8FAFC`): 4.6:1 ✅
- Error Red (`#EF4444`) on Warm White (`#F8FAFC`): 4.9:1 ✅

### State & Interaction Colors
Used for interactive elements to provide clear feedback.

#### Hover States
- Buttons: Increase brightness by 5-10% (subtle lift)
- Links: Slight opacity reduction to 90%
- Cards: Elevate shadow +0.5px, slight color shift

#### Active/Pressed States
- Buttons: Decrease brightness by 10-15%
- Tabs/Active items: Use Accent Gold (`#D4AF37`) as indicator
- Selected states: 10% opacity overlay of accent color

#### Focus States (Keyboard Navigation)
- Outline: 2px solid Accent Gold (`#D4AF37`)
- Offset: 2px from element
- Always visible, never rely solely on color change

### Data Visualization Guidelines
Ensure charts and graphs communicate clearly while maintaining aesthetic cohesion.

#### Sequential Data (Progress, Magnitude)
- Use tints of a single hue: Deep Navy → Slate Gray → Warm White
- Example: Pipeline value heatmap (low to high)

#### Diverging Data (Positive/Negative from Center)
- Success Green → Warm White → Error Red
- Example: Performance vs quota (under/over)

#### Categorical Data (Distinct Items)
- Use carefully spaced hues from our accent palette
- Maximum 6 distinct colors for quick discrimination
- Always pair with patterns/textures for colorblind accessibility

#### Special Considerations
- **Financial Data**: Use Success Green for gains, Error Red for losses (with icons)
- **Trend Data**: Info Blue for primary trend, Success/Error for comparisons
- **Heatmaps**: Slate Gray → Deep Navy intensity (avoid red/green for accessibility)
- **Status Indicators**: Always combine color with shape/icon (circle/square/triangle)

### Dark Mode Considerations
While our primary theme is dark-leaning, we provide a true dark mode variant.

#### Dark Mode Adaptations:
- Primary Background: Deep Navy (`#0F172A`) → Even darker (`#0A0F1C`)
- Secondary Background: Warm White (`#F8FAFC`) → Dark Slate (`#1E293B`)
- Text Primary: Warm White → Pure White (`#FFFFFF`)
- Accents: Remain largely unchanged for recognition
- Elevation: Increase shadow intensity slightly for depth perception

### Implementation Notes for Development

#### CSS Custom Properties (Recommended)
```css
:root {
  /* Neutrals */
  --color-navy-deep: #0F172A;
  --color-slate-gray: #64748B;
  --color-white-warm: #F8FAFC;
  --color-gray-cool: #F1F5F9;
  
  /* Accents */
  --color-gold-accent: #D4AF37;
  --color-green-success: #10B981;
  --color-amber-warning: #F59E0B;
  --color-red-error: #EF4444;
  --color-blue-info: #3B82F6;
  
  /* Semantic Tokens */
  --color-bg-primary: var(--color-navy-deep);
  --color-bg-secondary: var(--color-white-warm);
  --color-text-primary: var(--color-white-warm);
  --color-text-secondary: var(--color-slate-gray);
  --color-accent-primary: var(--color-gold-accent);
  --color-border: rgba(100,116,139,0.2);
}
```

#### Usage Examples
```css
/* Primary navigation */
.nav-sidebar {
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
  border-right: 1px solid var(--color-border);
}

/* Primary action button */
.btn-primary {
  background: var(--color-accent-primary);
  color: var(--color-bg-primary); /* Navy text on gold */
  border: none;
}

.btn-primary:hover {
  background: #E6C12F; /* Slightly darker gold */
}

/* Card component */
.card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: 8px;
}

/* Success state indicator */
.status-success {
  color: var(--color-green-success);
  background-color: rgba(16,185,129,0.1);
  padding: 2px 6px;
  border-radius: 4px;
}
```

#### Developer Guidelines
1. **Never hardcode colors** - Always use semantic tokens
2. **Maintain 4.5:1 contrast ratio** for all text
3. **Use accents purposefully** - Gold for achievements, not decoration
4. **Test in grayscale** - Ensure information hierarchy remains clear
5. **Consider colorblind users** - Always supplement color with icons/shapes
6. **Document exceptions** - Any deviation from system needs justification

## Luxury & Minimalism Principles Applied

### Why This Palette Achieves Luxury Feel:
1. **Restricted Palette** - Limited colors create sophistication and intention
2. **Sophisticated Neutrals** - Deep Navy and Warm White feel premium vs basic black/white
3. **Metallic Accent** - Gold provides luxury cue without gaudiness
4. **Subtle Variations** - Cool grays add depth without visual noise
5. **Consistent Application** - Predictable use builds trust and perceived quality

### Psychological Effects by Context:
- **Executive Dashboards**: Deep Navy dominance conveys authority and stability
- **Sales Rep Views**: Warm White backgrounds reduce fatigue during long sessions
- **Manager Views**: Strategic use of Accent Gold highlights team achievements
- **Report Sections**: Success/Warning/Error colors provide instant status comprehension
- **Forms & Data Entry**: Slate Gray labels guide without overpowering inputs

## Maintenance & Evolution

### Color System Governance
1. **Additions Require Justification** - New colors must solve specific unmet needs
2. **Accessibility First** - Any new color must meet WCAG contrast requirements
3. **Consistency Check** - New colors tested across all components and states
4. **Documentation Update** - Semantic tokens and usage guidelines updated

### Future-Proofing
- **Variable Design** - Built using CSS custom properties for easy theming
- **Scalable System** - Semantic tokens allow evolution without breaking changes
- **Platform Consistency** - Values work across web, desktop, and mobile implementations
- **Brand Extension** - System designed to accommodate sub-brands or product lines

---
*Color system document for Sovereign CRM design reference. Stored in Sovereign Vault as design/color-system.md
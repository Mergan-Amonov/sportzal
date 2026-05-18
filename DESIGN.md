# Design System — FitClub

## Product Context
- **What this is:** Sport zal a'zo va abonement boshqaruv tizimi (Gym membership management)
- **Who it's for:** Gym owner va adminlar (Uzbekistan)
- **Space/industry:** Gym / Fitness management SaaS
- **Project type:** Internal dashboard / admin tool
- **Stack:** Django + Bootstrap 5, Uzbek language interface

## Memorable Thing
> "Bu professional, tez va ishonchli dastur"
Every design decision must serve this. Clarity over decoration. Data before beauty.

## Aesthetic Direction
- **Direction:** Industrial / Utilitarian
- **Decoration level:** Minimal — typography and spacing do all the work
- **Mood:** Dark, precise, trustworthy. A tool that gym owners open every morning and immediately see what matters. No fluff, no animations for animation's sake.
- **Category differentiation:** Every gym management tool in the market uses a light theme. FitClub is dark-first — making the red accent and monospace numbers pop with authority.

## Typography

### Font Stack
- **Display / Headers:** Satoshi (weights 500, 600, 700, 900)
  - Why: Geometric grotesque with personality. Same legibility as Inter but not the default SaaS choice. Feels premium without trying.
  - Load: `https://api.fontshare.com/v2/css?f[]=satoshi@400,500,600,700,900&display=swap`
- **Body / UI:** Geist (weights 300, 400, 500, 600)
  - Why: Excellent for small UI text. High legibility at 12-13px. Clean at all sizes.
  - Load: `https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600&display=swap`
- **Numbers / Stats / Tables:** Geist Mono (weights 400, 500)
  - Why: All stats (member count, days remaining, prices) should feel precise and technical. Monospace numbers avoid layout shift and reinforce the "reliable tool" feeling.
  - Load: `https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&display=swap`
- **Code (if needed):** JetBrains Mono

### Scale
| Level      | Font    | Size | Weight | Use                          |
|------------|---------|------|--------|------------------------------|
| hero       | Satoshi | 32px | 700    | Page titles, hero headings   |
| h2         | Satoshi | 20px | 600    | Section headings             |
| h3         | Satoshi | 16px | 600    | Card titles, subsections     |
| body       | Geist   | 14px | 400    | Paragraph, descriptions      |
| ui         | Geist   | 13px | 400    | Table cells, form values     |
| label      | Geist   | 11px | 500    | Form labels, table headers   |
| caption    | Geist   | 11px | 400    | Helper text, timestamps      |
| stat       | Geist Mono | 28px | 500 | Dashboard stat numbers       |
| mono-data  | Geist Mono | 13px | 400 | Dates, prices, IDs in tables |

## Color System

### Approach
Restrained — one accent color (#e63946 red) used for brand identity and CTAs only. Red is NOT used for errors (that's the category cliché). Errors use warning-red-orange. The red is FitClub's identity.

### Dark Theme (primary)
```css
:root {
  --bg:          #0d0d14;  /* main page background */
  --surface:     #171722;  /* cards, tables, modals */
  --sidebar:     #0a0a12;  /* sidebar navigation */
  --border:      #2a2a3a;  /* dividers, input borders */
  --text:        #f0f0f8;  /* primary text */
  --muted:       #6b6b85;  /* secondary text, labels, placeholders */
  --accent:      #e63946;  /* brand — CTA buttons, active nav, logo */
  --accent-dim:  #c1121f;  /* hover state for accent */
  --success:     #22c55e;  /* active subscriptions, saved states */
  --warning:     #f59e0b;  /* expiring soon (≤3 days), caution */
  --error:       #ef4444;  /* expired subscriptions, destructive actions */
  --info:        #3b82f6;  /* informational alerts, auto-calculated fields */
}
```

### Light Theme (toggle)
```css
[data-theme="light"] {
  --bg:         #f4f4f8;
  --surface:    #ffffff;
  --sidebar:    #1a1a22;  /* sidebar stays dark */
  --border:     #e2e2ec;
  --text:       #111118;
  --muted:      #7777a0;
  --accent:     #e63946;  /* accent same */
  --accent-dim: #c1121f;
}
```

### Semantic Color Usage Rules
- `--accent` (#e63946): brand logo, sidebar active highlight border, primary CTA buttons ("Saqlash", "Qo'shish"). NEVER for errors.
- `--success` (#22c55e): "Faol" badge, active subscription indicators
- `--warning` (#f59e0b): subscriptions with ≤3 days remaining, caution states
- `--error` (#ef4444): expired subscriptions, delete confirmations
- `--info` (#3b82f6): auto-calculated field hints, informational notices

## Spacing

- **Base unit:** 4px
- **Density:** Compact (this is a data tool, not a landing page)
- **Scale:**
  - 2xs: 2px
  - xs:  4px
  - sm:  8px
  - md:  16px
  - lg:  24px
  - xl:  32px
  - 2xl: 48px
  - 3xl: 64px

### Component Spacing
- Table row height: 44px
- Card padding: 16-20px
- Form field gap: 14px
- Section gap: 32-40px
- Sidebar nav item padding: 9px 16px

## Layout

- **Approach:** Grid-disciplined
- **Sidebar width:** 240px (fixed)
- **Main content:** `margin-left: 240px`, padding 28px
- **Max content width:** 1280px
- **Columns:** 12-column grid within content area
- **Border-radius:**
  - sm: 4px (badges, small tags)
  - md: 6px (inputs, small buttons)
  - lg: 8px (cards, modals, buttons)
  - xl: 12px (top-level containers)
  - full: 9999px (avatar circles)
  - NO: 20px+ bubble radius anywhere

## Motion

- **Approach:** Minimal-functional
- **Easing:** enter: ease-out, exit: ease-in, move: ease-in-out
- **Duration:**
  - micro: 50ms (hover color changes, badge transitions)
  - short: 150ms (button hover, nav highlight)
  - medium: 250ms (sidebar collapse if added, modal open)
- **What NOT to animate:** table row content, stat numbers, form labels. Only state transitions (hover, active, open/close).

## Component Patterns

### Status Badges
```
Active (Faol):      bg rgba(34,197,94,.15)  · color #4ade80
Expiring (N kun):   bg rgba(245,158,11,.15) · color #fbbf24
Expired (Tugagan):  bg rgba(239,68,68,.15)  · color #f87171
Inactive (Nofaol):  bg rgba(107,107,133,.15)· color #6b6b85
```
Font: Geist, 11px, weight 600, padding 3px 8px, border-radius 4px.

### Buttons
- Primary: `bg: var(--accent)`, white text, Geist 13px 500
- Secondary: `bg: var(--surface)`, border `var(--border)`, `color: var(--text)`
- Ghost: transparent, `color: var(--muted)`, hover → `var(--text)`
- Danger: `bg: rgba(239,68,68,.15)`, `color: #f87171`, border `rgba(239,68,68,.2)`
- All buttons: border-radius 8px, padding 8px 16px

### Tables
- Header: Geist 10px, weight 500, uppercase, letter-spacing 0.04em, color `var(--muted)`
- Row height: 44px, padding 9px 14px
- Row hover: `background rgba(255,255,255,.02)`
- Row border: `1px solid rgba(42,42,58,.5)` (lighter than card border)
- Member names: Geist weight 500, `var(--text)`
- Secondary info (plan name, dates): Geist Mono 12px, `var(--muted)`

### Forms
- Label: Geist 11px weight 500, uppercase, letter-spacing 0.03em, `var(--muted)`
- Input: background `var(--bg)`, border `var(--border)`, focus border `var(--accent)`
- Input font: Geist 13px
- Border-radius: 6-8px

## Decisions Log

| Date       | Decision                                         | Rationale                                                                 |
|------------|--------------------------------------------------|---------------------------------------------------------------------------|
| 2026-05-18 | Dark-first theme                                 | Every competitor is light. Dark makes red accent and mono numbers pop. Signals professional tool. |
| 2026-05-18 | Satoshi for headings (not Inter/Roboto)          | Same geometric legibility but with personality. Avoids the default SaaS look. |
| 2026-05-18 | Geist Mono for all stats and data values         | Reinforces "precise, reliable" — numbers feel technical, not decorative.  |
| 2026-05-18 | #e63946 red as brand accent (not just danger)    | Category uses red only for errors. Using it as the primary brand color is deliberate differentiation. Errors use orange-red (#ef4444). |
| 2026-05-18 | Border-radius max 12px                           | Avoids bubble-radius trend. Sharp corners = precision tool.               |
| 2026-05-18 | Minimal motion                                   | Data tools should feel fast. Unnecessary animation adds latency perception. |

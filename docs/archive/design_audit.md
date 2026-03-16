---
Status: Active
Last Audited: 2026-03-14
Drift Aversion: REQUIRED
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding code or system behavior MUST be reflected here immediately.
> 3. **AI Agent Compliance**: Agents MUST verify the current implementation against this document before proposing changes.
> 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# Bxthre3 Homepage Design Audit

## Current Version Assessment

### ✅ What's Working

- Clean, modular component structure
- Consistent dark theme (zinc-950 base)
- Accurate FarmSense data from docs
- Good information hierarchy

### ⚠️ Issues Found

#### 1. **Tailwind Dynamic Classes (BROKEN)**

**Problem**: `bg-${color}-500/10` doesn't work — Tailwind needs full literal class names.
**Affected**: VALUES cards, WHY_NOW cards

#### 2. **Missing "Our Approach" Section**

**Problem**: The Identify → Research → Launch flow with arrows was removed.
**Impact**: Loses the core B3 methodology narrative.

#### 3. **Inconsistent Spacing**

**Problem**: Section margins vary (`mx-4 lg:mx-8 px-4` vs different patterns)
**Fix**: Standardize to `max-w-7xl mx-auto px-6 lg:px-8`

#### 4. **Timeline Color Logic**

**Problem**: Manual ternary color mapping is brittle.
**Fix**: Add color to timeline data, use colorClasses map.

#### 5. **Card Hover States**

**Problem**: Simple `hover:border-white/10` is subtle.
**Fix**: Add elevation, glow effects, micro-movements.

### 🎯 Proposed Improvements

#### Color System Fix

```javascript
const colorClasses = {
  emerald: { bg: 'bg-emerald-500/10', border: 'border-emerald-500/20', text: 'text-emerald-400' },
  violet: { bg: 'bg-violet-500/10', border: 'border-violet-500/20', text: 'text-violet-400' },
  // ... etc
};
```

#### Add "Our Approach" Section

```javascript
const APPROACH = [
  { icon: Search, title: 'Identify', desc: 'Civilizational challenges others ignore' },
  { icon: Microscope, title: 'Research', desc: 'First-principles deep dives' },
  { icon: Rocket, title: 'Launch', desc: 'Original technology solutions' }
];
```

#### Enhanced Hover Effects

- Scale: `hover:scale-[1.02]`
- Glow: `hover:shadow-lg hover:shadow-emerald-500/10`
- Border: `hover:border-emerald-500/30`

#### Typography Polish

- Hero: `text-6xl md:text-8xl` (more impact)
- Section titles: Add gradient text option
- Stats: Larger numbers, tighter tracking

### 🎨 Color Palette Audit

| Element | Current | Proposed |
|---------|---------|----------|
| Primary | violet/fuchsia/pink | Keep — good distinctiveness |
| Success | emerald-400 | Keep — matches FarmSense |
| Background | zinc-950 | Keep — excellent dark base |
| Cards | zinc-900/50 | Slightly lighter for depth |
| Text | zinc-400/zinc-500 | Good hierarchy |

### 📐 Spacing Standards

```css
/* Container */
max-w-7xl mx-auto px-6 lg:px-8

/* Section padding */
py-16 lg:py-24

/* Grid gaps */
gap-6 (standard)
gap-8 (featured sections)

/* Card padding */
p-6 (standard)
p-8 (featured)
```

### ✨ Animation Recommendations

1. **Stagger entrance** — sections fade in as you scroll
2. **Number count-up** — stats animate from 0
3. **Gradient shift** — background orbs slowly move
4. **Card lift** — subtle Y translation on hover

---

*Audit Date: 2026-03-09*
*Next: Implement fixes based on priorities*

# Canonical Template Token Reference

**Version 1.0 — April 2026**

This document defines every `{{TOKEN}}` in `templates/canonical-template.html`. Use this as the fill-in checklist when building a new report. Populate all tokens before deploying.

---

## How to Use

1. Copy `canonical-template.html` to `/home/ubuntu/scroll-reports-repo/[CLIENT_SLUG]/[monthyear]/index.html`
2. Fill in every token below using the data sources listed
3. Run `verify_report_data.py` to confirm all metric values match the master sheet
4. Run the QA script before deploying

---

## Token Groups

### Group 1 — Client Identity

| Token | Description | Source |
|---|---|---|
| `{{CLIENT_NAME}}` | Full display name (e.g., "DEFINE Oakley") | Master Client Roster |
| `{{CLIENT_NAME_H1}}` | H1 format — may use `<span>` for accent color (e.g., `DEFINE <span>Oakley</span>`) | Master Client Roster |
| `{{CLIENT_HANDLE}}` | Instagram handle without @ (e.g., `defineoakley`) | Master Client Roster |
| `{{CLIENT_SLUG}}` | URL slug (e.g., `defineoakley`) | SKILL.md client slugs table |
| `{{CLIENT_NICHE_DESCRIPTOR}}` | Short niche description (e.g., "High-Energy, Low-Impact Group Fitness") | Account Homebase |
| `{{CLIENT_AM_NAME}}` | Account manager first name (e.g., "Emily") | Master Client Roster |
| `{{CLIENT_STAGE}}` | Growth stage (Spark / Lift / Rise / Thrive) + "Stage" (e.g., "Lift Stage") | Master Client Roster |
| `{{CLIENT_MONTH_NUMBER}}` | How many months the client has been active (e.g., "26") | Master Client Roster |

---

### Group 2 — Report Period

| Token | Description | Source |
|---|---|---|
| `{{REPORT_MONTH_YEAR}}` | Full month + year (e.g., "March 2026") | Reporting period |
| `{{REPORT_MONTH}}` | Month name only (e.g., "March") | Reporting period |
| `{{REPORT_DATE_RANGE}}` | Date range (e.g., "March 1–30, 2026") | Reporting period |
| `{{NEXT_MONTH}}` | Following month name (e.g., "April") | Reporting period |
| `{{PREV_MONTH_SHORT}}` | Prior month abbreviation (e.g., "Feb") | Reporting period |
| `{{MONTH_SLUG}}` | URL-safe month+year (e.g., "march2026") | Reporting period |

---

### Group 3 — Score Card

| Token | Description | Source / Calculation |
|---|---|---|
| `{{SCORE}}` | Monthly score to 1 decimal (e.g., "8.2") | Scoring engine (process-v7.0.md §5) |
| `{{SCORE_LABEL}}` | Score label (e.g., "Building Month", "Solid Month") | Scoring engine output |
| `{{SCORE_DELTA_DIR}}` | CSS class for delta direction: `up` / `dn` / `fl` | Compare to prior month score |
| `{{SCORE_DELTA_ARROW}}` | Arrow character: `▲` (up) or `▼` (dn) or `—` (flat) | Compare to prior month score |
| `{{SCORE_DELTA_TEXT}}` | Delta text (e.g., "+0.2") | Current score minus prior month score |
| `{{SCORE_EXCEED_COUNT}}` | Number of metrics with Exceeding status | Scoring engine output |
| `{{SCORE_ONTRACK_COUNT}}` | Number of metrics with On Track status | Scoring engine output |
| `{{SCORE_WATCH_COUNT}}` | Number of metrics with Watch status | Scoring engine output |
| `{{SCORE_TREND_BARS_HTML}}` | Full HTML for 6-bar trend chart | Master Scoring Sheet — last 6 months |

**Score Trend Bars HTML format:**
```html
<div class="tc"><div class="tbw"><div class="tb" style="height:XX%;background:rgba(255,255,255,0.28)"></div></div><div class="ts">X.X</div><div class="tm">Mon</div></div>
```
Current month uses `background:#e2ed7a` and adds `curr` class to `.ts` and `.tm`. Height = `(score / max_score_in_range) * 100%`.

---

### Group 4 — Hero Bullets

| Token | Description | Source |
|---|---|---|
| `{{HERO_BULLET_1_HEADLINE}}` | Bold headline for bullet 1 (e.g., "Content is holding attention.") | Written by agent from data |
| `{{HERO_BULLET_1_BODY}}` | 1-2 sentence insight for bullet 1 | Written by agent from data |
| `{{HERO_BULLET_2_HEADLINE}}` | Bold headline for bullet 2 | Written by agent from data |
| `{{HERO_BULLET_2_BODY}}` | 1-2 sentence insight for bullet 2 | Written by agent from data |
| `{{HERO_BULLET_3_HEADLINE}}` | Bold headline for bullet 3 | Written by agent from data |
| `{{HERO_BULLET_3_BODY}}` | 1-2 sentence insight for bullet 3 | Written by agent from data |

**Hero bullet rules:** Each bullet must reference a specific metric value. One exceeding metric, one on-track metric, one watch/growth lever. No generic observations.

---

### Group 5 — Followers Banner

| Token | Description | Source |
|---|---|---|
| `{{TOTAL_FOLLOWERS}}` | Total follower count (e.g., "3,673") | Master Performance Data Sheet |
| `{{TOTAL_FOLLOWERS_MOM_ARROW}}` | `▲` or `▼` | Compare to prior month |
| `{{TOTAL_FOLLOWERS_MOM_PCT}}` | MoM % (e.g., "-12.0") — include sign | Calculate from sheet data |
| `{{TOTAL_FOLLOWERS_MOM_DIR}}` | `up` / `dn` / `fl` | Compare to prior month |
| `{{FOLLOWERS_TARGET_RANGE}}` | Stage target range (e.g., "1,000 – 5,000") | KPI Target Ranges Framework |

---

### Group 6 — Performance Metrics (10 metrics)

For each metric, three tokens: value, status, and MoM (MoM tokens are inline in the HTML — verify they match the sheet).

| Metric | Value Token | Status Token | Status Values |
|---|---|---|---|
| New Followers | `{{NEW_FOLLOWERS}}` | `{{NEW_FOLLOWERS_STATUS}}` | `exceed` / `ontrack` / `watch` |
| Shares | `{{SHARES}}` | `{{SHARES_STATUS}}` | same |
| Total Views | `{{TOTAL_VIEWS}}` | `{{TOTAL_VIEWS_STATUS}}` | same |
| Profile Visits | `{{PROFILE_VISITS}}` | `{{PROFILE_VISITS_STATUS}}` | same |
| Retention % | `{{RETENTION_PCT}}` | `{{RETENTION_STATUS}}` | same |
| Saves | `{{SAVES}}` | `{{SAVES_STATUS}}` | same |
| Comments | `{{COMMENTS}}` | `{{COMMENTS_STATUS}}` | same |
| CTR | `{{CTR}}` | `{{CTR_STATUS}}` | same |
| Link Taps | `{{LINK_TAPS}}` | `{{LINK_TAPS_STATUS}}` | same |
| Profile Conversion Rate | `{{PCR}}` | `{{PCR_STATUS}}` | same |

**Status logic:** Compare metric value to KPI Target Range for the client's stage. Exceeding = above upper bound. On Track = within range. Watch = below lower bound.

**MoM delta tokens** are inline in the metric cards (not separate tokens) — the agent must calculate and write them directly. Formula: `(current - prior) / prior * 100`. Round to 1 decimal. Use `▲` for positive, `▼` for negative.

---

### Group 7 — Dynamic Content Blocks

These tokens represent entire HTML blocks generated by the agent. Each has a comment in the template explaining the expected structure.

| Token | Description | Source |
|---|---|---|
| `{{BUSINESS_GOALS_CARDS_HTML}}` | 3 goal cards (TOFU/MOFU/BOFU) | Master Goals Sheet + scoring engine |
| `{{TOP_POSTS_CARDS_HTML}}` | 2–4 post cards from outlier engine | `scripts/outlier_engine.py` output |
| `{{WHAT_WE_LEARNED_CARDS_HTML}}` | 3 insight cards | Written by agent from data |
| `{{STRATEGY_ADJUSTMENTS_CARDS_HTML}}` | 3 adjustment cards (Doubling Down / Testing / Fixing) | Written by agent from data |
| `{{SCORE_TREND_BARS_HTML}}` | 6-bar score trend chart | Master Scoring Sheet history |
| `{{PREV_REPORTS_CARDS_HTML}}` | 2–4 previous month report cards | Master Scoring Sheet history |

---

### Group 8 — CTA Section

| Token | Description | Source |
|---|---|---|
| `{{CTA_PRIMARY_OBJECTIVE}}` | Primary CTA goal (e.g., "Drive First Class Bookings") | Account Homebase |
| `{{CTA_PRIMARY_TYPE}}` | CTA type (e.g., "Booking CTA") | Account Homebase |
| `{{CTA_PRIMARY_MECHANISM}}` | How it works (e.g., "Link in Bio → Class Booking Page") | Account Homebase |
| `{{CTA_PRIMARY_KPI}}` | KPI to track (e.g., "Link Taps / CTR") | Account Homebase |
| `{{CTA_PRIMARY_COPY}}` | Exact CTA copy (e.g., "Try your first class free — book now. Link in bio.") | Account Homebase |
| `{{CTA_PRIMARY_RATIONALE}}` | 2-3 sentence rationale grounded in data | Written by agent |
| `{{CTA_TOFU_TYPE}}` | TOFU CTA type (e.g., "Share CTA") | Account Homebase |
| `{{CTA_TOFU_COPY}}` | TOFU CTA copy | Account Homebase |
| `{{CTA_TOFU_KPI}}` | TOFU KPI + mechanism | Account Homebase |
| `{{CTA_MOFU_TYPE}}` | MOFU CTA type (e.g., "Save CTA") | Account Homebase |
| `{{CTA_MOFU_COPY}}` | MOFU CTA copy | Account Homebase |
| `{{CTA_MOFU_KPI}}` | MOFU KPI + mechanism | Account Homebase |
| `{{CTA_BOFU_TYPE}}` | BOFU CTA type (e.g., "Booking CTA") | Account Homebase |
| `{{CTA_BOFU_COPY}}` | BOFU CTA copy | Account Homebase |
| `{{CTA_BOFU_KPI}}` | BOFU KPI + mechanism | Account Homebase |

---

## Pre-Deployment Checklist

- [ ] All 64 unique tokens replaced (no `{{` remaining in output file)
- [ ] `verify_report_data.py` passes all checks
- [ ] QA script passes all 19 checks
- [ ] Score trend bars use correct heights and current month styling
- [ ] Post cap IDs use `{{CLIENT_SLUG}}` prefix (e.g., `capdefineoakley0`)
- [ ] All Instagram post URLs are live and correct
- [ ] Previous reports section shows correct months and scores from Master Scoring Sheet

---

## Token Count Summary

| Group | Token Count |
|---|---|
| Client Identity | 8 |
| Report Period | 6 |
| Score Card | 9 |
| Hero Bullets | 6 |
| Followers Banner | 5 |
| Performance Metrics | 20 |
| Dynamic Content Blocks | 6 |
| CTA Section | 15 |
| **Total** | **75** |

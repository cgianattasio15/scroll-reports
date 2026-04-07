# Scroll Media Monthly Performance Reporting Process

**Last Updated:** March 31, 2026 (v7.1 patch)
**Version:** 7.1
**Framework Owner:** Chase (Chief Strategist)

This document is the **single source of truth** for creating, QA-ing, and deploying monthly client performance reports. It serves as both a technical instruction set for AI agents and a standard operating procedure (SOP) for the Scroll Media team.

---

## WHAT CHANGED IN v7.1

**Instagram embeds removed from Top 3 Posts.** Embeds are replaced with a clean, styled "View on Instagram" link button per post. This is cleaner, simpler, and more professional — no iframe load dependency, no embed rendering issues, no broken posts if content is archived. The button links directly to the Instagram post URL and opens in a new tab.

**Mandatory: Reference client Account Homebase page before building every report.** Before writing any narrative copy (hero bullets, goal summaries, strategy adjustments, CTAs, post insights), the agent MUST visit the client's Account Homebase page at `https://tools.scrollmedia.co/clients/[client-slug]/` (password: `scrollies`). This page contains the client's active strategy, content priorities, active CTAs, and campaign context. All report copy must be grounded in this source — not generic assumptions.

---

## WHAT CHANGED IN v7.0

**Canonical template updated to DEFINE Oakley March 2026.** The DEFINE Oakley March 2026 report is the new canonical template for all reports. All design, section structure, metric selection, and UX decisions documented in this version are derived from and validated against that report.

**Customer-facing metrics reduced and simplified.** Two metrics have been removed from all customer-facing sections: `Avg Reach / Day` (TOFU) and `Avg Watch Time` (MOFU). Both are still tracked in the Master Performance Data Sheet as internal metrics but are no longer shown in reports. This simplifies the performance story and removes duplication with Views (TOFU) and Retention % (MOFU).

**Customer-facing metric sets are now:**
- **TOFU:** New Followers, Shares, Views (3 metrics)
- **MOFU:** Profile Visits, Retention %, Saves, Comments (4 metrics)
- **BOFU:** Link Taps, CTR, PCR (3 metrics)
- **Total: 10 customer-facing metrics** (down from 12)

**Scoring framework updated to reflect 10-metric model.** `Avg Reach / Day` and `Avg Watch Time` are excluded from the weighted score calculation. See Section 5 for the updated formula.

**Unified Scoring Framework v3.0 (new in v7.3):** Both the monthly account score and the top post outlier engine now use the same intent-weighted hierarchy. Tier structure simplified: T1-High removed, all highest-intent metrics unified at T1 (1.5x). Shares moved to T2 (1.0x). Comments moved to T3 (0.75x). Link Taps promoted to T1. CTR retained at T1. Denominator updated to 13.25.

**Hero section updated: bullet-point format.** The hero summary is now 3 bullet points — each with a **bold title** followed by a short, direct explanation. No paragraph copy in the hero. No score numbers in the hero.

**Lift Stage badge added to hero.** The client's stage (Spark / Lift / Rise / Thrive) must be prominently displayed in the hero as a badge. Required element alongside the eyebrow label.

**Score Card: methodology note removed.** The "Score calculated using the Scroll Media Weighted Performance Framework" note is no longer included in the Score Card section. The score stands on its own.

**Total Followers banner added.** A dedicated followers banner appears above the metric grid in the Performance Dashboard section. It shows: Total Followers count, MoM delta, and the Target Range for the client's stage. Label is "Target Range" — not "Lift Target" or "Stage Target."

**Funnel label updates:**
- TOFU: "Awareness & Authority" (previously "Awareness & Discovery")
- BOFU: "Consideration & Conversion" (previously "Conversion")

**All "Lift Target" labels → "Target Range."** Throughout the Performance Dashboard, all target labels read "Target Range" regardless of client stage.

**Business Goals section: progress bar format.** Each goal card now shows a color-coded progress bar representing the % of metrics on track for that funnel stage, plus a brief summary explaining what success means for that goal. Individual metrics are NOT shown in this section (they appear in the Performance Dashboard). The goal card is cleaner and higher-level.

**Top Posts of the Month: final card structure (v7.2).** Each post card contains the following elements in order:
1. **Rank header** — `#1 / #2 / #3 Top Post` + format badge (e.g., `REEL`, `STATIC IMAGE`, `CAROUSEL`)
2. **Post date** — full date (e.g., March 14, 2026)
3. **Format tag** — prominent pill badge showing the content type (e.g., `Humor / Trend Reel`).
4. **Hook** — the actual on-screen text or opening line of the caption, in italic quotes.
5. **Caption** — full caption text. If > 180 chars, truncate and add a "Show more / Show less" toggle to keep cards symmetrical.
6. **Standout Metrics** — 2–3 specific metrics that made the post an outlier, showing the absolute value and the multiplier vs. account average (e.g., "14 Shares — 3.0x account avg"). Badges are green for ≥2.0x and blue for ≥1.5x. Absolute floors apply (Saves ≥4, Shares ≥4).
7. **Retention row** — ONLY shown if Retention % is one of the standout outlier metrics. Do not show a default retention row for all Reels.
8. **Why It Worked** — a data-backed strategic learning note explaining what made this post perform, referencing the specific standout metrics.
9. **View on Instagram button** — a clean, styled CTA button linking to the post URL. Opens in a new tab. No Instagram embed. No iframe.

**No Instagram embeds.** Do not use `<blockquote class="instagram-media">` or the Instagram embed script. Replace with a clean link button only.

**No `.post-caption` element.** Do not duplicate the caption. The hook line is sufficient.

**Button design:** Styled as a pill button — `background: var(--azure)`, white text, `border-radius: 999px`, `padding: 10px 24px`. Label: "View on Instagram →". Opens in `_blank`.

**Top 3 Posts: accurate format and hook data required.** Always visit the actual Instagram post URL before writing the format tag, hook, and Why It Worked copy. Do not use generic assumptions. Pull the real on-screen text and caption from the live post.

**Mandatory: Visit the client Account Homebase page before writing any report copy.** URL pattern: `https://tools.scrollmedia.co/clients/[client-slug]/` (password: `scrollies`). This page contains the client's active strategy, content priorities, active CTAs, and campaign context. All narrative copy — hero bullets, goal summaries, strategy adjustments, CTAs, and post insights — must be grounded in this source.

**Per-post Retention % source.** Pull from the `march_top3.json` file (or equivalent monthly top3 data file) which stores `retention` per reel calculated as `avgPlaybackTime ÷ videoDuration × 100`. If this data is unavailable for a specific post, use the account-level Retention % as a fallback and note it as an estimate.

**CTA section renamed.** "April CTA Strategy" → "Next Month's CTAs" (and updated dynamically to the actual next month name).

**Strategy Adjustments simplified.** Three cards only. Each card has: a type badge (Doubling Down / Testing Next / Fixing), a headline, a one-line context note, and a single action statement. The detailed "Why" and "What This Moves" blocks from v6.3 have been removed. The goal is maximum scannability for the client.

**Scroll Media branding applied.** All reports must use the full Scroll Media brand system: navy/lime dark mode aesthetic, Source Sans 3 typography, white-on-transparent logo in the hero, navy-on-transparent logo in the footer, favicon, and scroll progress bar.

**Footer updated: white background.** Footer background is `#ffffff` (white). The Scroll Media logo in the footer uses the navy-on-transparent variant. All footer text is dark.

**Full mobile optimization required.** All reports must be fully responsive. Breakpoints at 640px, 580px, 480px, and 760px. Viewport meta includes `maximum-scale=5.0`. Tap targets sized correctly for mobile.

**Previous Reports section added.** A new section at the bottom of every report (above the footer) shows links to all prior months' reports as cards. Each card shows: month/year, score, and score label. This is a dark card-grid section.

**Data pipeline updated.** The primary data source for all metrics is the **Master Performance Data Sheet** (Google Sheets). Metricool API is used to pull post-level data for Top 3 Posts. IG Insights metrics (New Followers, Profile Visits, Link Taps, Total Followers) must be entered manually by the team each month — the Meta API does not reliably expose these via Metricool.

**Active client list updated.** 7 active clients as of March 2026. See Section 7.2 for full slug list.

---

## WHAT CHANGED IN v6.4

**Top Posts of the Month: 3-Column Layout (v7.2).** The canonical layout for the Top Posts section is a 3-column horizontal grid (`grid-template-columns: repeat(3, 1fr)`). It collapses to a single column on mobile (`@media(max-width: 900px)`).

**Top 3 Posts: Post Embed Container (codified).** Each Instagram embed must be wrapped in `<div class="post-embed">` with `display: flex; justify-content: center`. The embed `<blockquote>` must have `max-width: 400px`. `.post-card` must have `overflow: visible`.

**Dashboard & Archive Update Process (new).** After deploying individual client reports, the main dashboard and each client's archive page must be updated.

**Instagram Permalink Case-Sensitivity Protocol (new).** Instagram post IDs are case-sensitive. A single incorrect character case will cause the embed to silently fail.

---

## 1. System Overview & Purpose

The monthly performance report is Scroll Media's most critical client-facing deliverable. It is not a data dump. It is a strategic narrative — a document that tells the story of the month, connects performance to business goals, and builds the client's confidence in Scroll Media's direction.

Reports are delivered as a single, self-contained HTML file, hosted on `reports.scrollmedia.co`. The URL structure is: `https://reports.scrollmedia.co/[client-slug]/[monthyear]/` (e.g., `https://reports.scrollmedia.co/defineoakley/march2026/`).

---

## 2. Audience & Roles

| Audience | Role & Directives |
|---|---|
| **AI Agents (Manus)** | This is your primary instruction manual. The rules, structures, and formats defined here are non-negotiable and must be followed exactly. Your function is to build the report with precision, deploy it to GitHub, and verify it is live before marking the task complete. |
| **Scroll Media Team** | This is your operational playbook. Use it to understand the 'why' behind the report structure, the logic of the scoring framework, and the standards for client-facing communication. Your function is to provide the data and strategic context that Manus needs to build the report. |

---

## 3. Prerequisites: What You Need Before Starting

### 3.1. Client Metadata (from Master Client Roster)

Pull from the Master Client Roster Google Sheet (link in project files). **Never copy metadata from a prior report — always pull fresh from the roster.**

| Field | Notes |
|---|---|
| Client Name | |
| Instagram Handle | |
| Niche | Broad category (e.g., "Group Fitness Studio") |
| Subniche | Specific positioning (e.g., "High-Energy, Low-Impact Group Fitness") |
| Account Manager | First name only in the report |
| Stage | Spark / Lift / Rise / Thrive |
| Package | Signature / Custom / A La Carte |
| Posts Per Week | |
| Start Date | Used to calculate Month # |
| MRR | Internal only — do not include in report |

### 3.2. Performance Data — Sources & Priority

**Primary source: Master Performance Data Sheet** (Google Sheets). The March tab (or current month tab) is the authoritative source for all 10 customer-facing metrics plus the 2 internal-only metrics.

| Priority | Source | Used For |
|---|---|---|
| 1 (highest) | Master Performance Data Sheet — current month tab | All 10 customer-facing metrics + 2 internal metrics |
| 2 | IG Insights (manual entry by team) | New Followers, Profile Visits, Link Taps, Total Followers |
| 3 (lowest) | Metricool API | Post-level data for Top 3 Posts only |

**IG Insights metrics must be entered manually by the team each month.** The Meta API does not reliably expose these via Metricool due to known sync delays. The team pulls these from Instagram Insights directly (Settings → Insights → Overview, date range = 1st through 2nd-to-last day of the month).

**Date range for all monthly data:** First day of the month through the **second-to-last day** of the month (e.g., March 1–30 for a March report run on March 31). This avoids incomplete data for the final day.

**Customer-facing metrics (10 total):**

| Metric | Funnel Stage | Tier | Source |
|---|---|---|---|
| New Followers | TOFU | T2 | IG Insights (manual) |
| Shares | TOFU | **T2** | Metricool API / Master Sheet |
| Total Views | TOFU | T2 | Metricool API / Master Sheet |
| Profile Visits | MOFU | T2 | IG Insights (manual) |
| Retention % | MOFU | **T1** | Metricool API / Master Sheet |
| Saves | MOFU | **T1** | Metricool API / Master Sheet |
| Comments | MOFU | **T3** | Metricool API / Master Sheet |
| Link Taps | BOFU | **T1** | IG Insights (manual) |
| CTR | BOFU | **T1** | Calculated: Link Taps ÷ Profile Visits × 100 |
| PCR | BOFU | **T1** | Calculated: New Followers ÷ Profile Visits × 100 |

**Internal-only metrics (tracked in Master Sheet, NOT shown in reports):**

| Metric | Why Internal |
|---|---|
| Avg Reach / Day | Duplicative with Views; adds complexity without clarity |
| Avg Watch Time | Duplicative with Retention %; not meaningful to clients |

**Total Followers:** Shown in the Followers Banner above the metric grid. Source: IG Insights (manual). Not scored.

### 3.3. Top 3 Posts

Top 3 posts are ranked by Total Views from the Metricool API for the report month. For each post:
1. Pull the post URL from Metricool data.
2. **Visit the actual Instagram post URL** to pull the real caption and confirm the post format.
3. Write the post type label (e.g., "Behind-the-Scenes / Personality Reel") based on actual content.
4. Include the actual caption text as the `.post-caption` element.
5. Write the post insight based on what the content actually is — not a generic assumption.

**Post stats to show:** Total Views and Total Interactions (likes + comments + shares + saves combined). No other per-post metrics.

### 3.4. Score History

Score trend history is pulled from the **Monthly Scorecard Google Sheet** (link in project files). Show the last 3–4 months. If a client has fewer than 3 months of history, show all available months (minimum 2 bars).

### 3.5. Client Goals

Client goals are sourced from the **Master Goals Sheet** (Google Sheets, link in project files). Three goals per client, one per funnel stage (TOFU / MOFU / BOFU). Always use the exact goal language from the sheet — do not paraphrase.

### 3.6. Client Account Homebase (MANDATORY)

Before writing any narrative copy, visit the client's Account Homebase page:
- **URL:** `https://tools.scrollmedia.co/clients/[client-slug]/`
- **Password:** `scrollies`
- **What to extract:** Active strategy, content priorities, active CTAs, campaign context, tone/voice notes
- **Where it informs the report:** Hero bullets, goal summaries, strategy adjustments, Next Month's CTAs, post insights

This step is non-negotiable. Reports built without homebase context will produce generic copy that does not reflect the client's actual strategy.

### 3.7. Strategic Context (from Account Manager)

Before writing narrative copy, the AM should provide: any major events, campaigns, or one-off occurrences during the report month; any specific client questions or concerns; any context that explains unusual metric movements. Not required to start building, but improves narrative quality.

---

## 4. Report Architecture: Section-by-Section Build Guide

Every report is built in the following order. **Do not skip sections or reorder them.**

1. Hero Header
2. Monthly Score Card
3. Business Goals (Funnel Health Check)
4. Performance Dashboard
5. Top 3 Posts
6. What We Learned (Insights)
7. Next Month's CTAs
8. Strategy Adjustments
9. Previous Reports
10. Footer

---

### Section 1: Hero Header

**Required elements:**
- Scroll Media logo (white-on-transparent PNG from `https://reports.scrollmedia.co/assets/scroll-logo-white.png`)
- Eyebrow label: "Monthly Performance Report" (with a yellow dot accent)
- **Stage badge** (new in v7.0): Prominently displayed — e.g., "Lift Stage · Month 26" — pill shape, lime/yellow border
- Client Name (H1) with the month/year highlighted in lime
- Hero meta row: niche, date range, AM name
- **3 bullet points** (new in v7.0): Each bullet has a **bold title** followed by a short, direct explanation. Highlight the top 3 signals from the month. No paragraph copy. No score numbers.

**Design rules:**
- Hero background: `linear-gradient(140deg, #0a0f1e 0%, #0d1a3a 55%, #151f3d 100%)`
- Logo: white-on-transparent, no background box
- Stage badge: `background: rgba(226,237,122,.18)`, `border: 1.5px solid rgba(226,237,122,.5)`, text color `var(--hl)` (lime)
- **Critical:** Hero must NOT contain a score number or score narrative paragraph.

---

### Section 2: Monthly Score Card

**Required elements:**
- Score eyebrow: "Monthly Performance Score"
- Score number: `X.X / 10`
- Score title: The month's narrative label (e.g., "Solid Month")
- Score delta: MoM change (e.g., "▲ +0.7 vs. February")
- Score badges: Exceeding / On Track / Watch counts (must match actual metric statuses in the Performance Dashboard)
- Score Trend bar chart: 3–4 months of history, chronological left-to-right (oldest → newest)

**Removed in v7.0:** The "Score calculated using the Scroll Media Weighted Performance Framework" methodology note. Do not include it.

**Score Trend Bar Chart:**
- Container: dark gradient background (`linear-gradient(135deg, #1a1f3a, #0c1a3a)`), `border-radius: 10px`
- Prior month bars: `background: rgba(255,255,255,0.28)`
- Current month bar: `background: var(--hl)` (lime), score text in lime
- Bar height formula: `height_pct = 20 + ((score - min_score) / (max_score - min_score)) * 72`. If all scores equal, set all to 50%.
- Bars must be in chronological order: Jan → Feb → Mar (left to right)

---

### Section 3: Business Goals (Funnel Health Check)

This section answers: *"Is this actually helping my business?"*

**Section header:**
- Label: "Business Goals"
- Title: "Funnel Health Check"
- Sub: "How [Month] performance mapped to your three core business goals."

**Each goal card contains:**
1. **Progress bar** — color-coded based on % of metrics on track for that funnel stage:
   - Purple: Exceeding (>80% on track or exceeding)
   - Navy: On Track (50–80% on track)
   - Amber: Watch (<50% on track)
2. **Status badge** — Exceeding / On Track / Watch
3. **Goal title** — exact language from the Content Strategy Map
4. **Brief summary** — 1–2 sentences explaining what success means for this goal (plain English, no jargon)

**Removed in v7.0:** Individual metric KPI blocks inside goal cards. These are duplicative with the Performance Dashboard. The goal card is now high-level only.

**Tone rules:** Always positive and action-oriented. Frame challenges as "building toward." Never use "missed" or "failed."

---

### Section 4: Performance Dashboard

**Section header:**
- Label: "Performance Dashboard"
- Title: "[Month] Metrics"
- Sub: "All tracked metrics grouped by funnel stage. Targets reflect the [Stage] stage range. Progress bars show actual vs. the high target."

**Followers Banner (new in v7.0):** A dedicated banner appears ABOVE the metric grid. It shows:
- Total Followers count (large, prominent)
- MoM delta (e.g., "+31 vs. February")
- **Target Range** for the client's stage (e.g., "1,000 – 5,000")
- Label: "Target Range" (not "Lift Target" or "Stage Target")

**Funnel groups:**
- **Top of Funnel — Awareness & Authority** (TOFU): New Followers, Shares, Views
- **Middle of Funnel — Engagement & Trust** (MOFU): Profile Visits, Retention %, Saves, Comments
- **Bottom of Funnel — Consideration & Conversion** (BOFU): Link Taps, CTR, PCR

**Each metric card contains:**
- Metric name
- Status badge: Exceeding / On Track / Watch
- Actual value (color-coded to match badge)
- **Target Range** (not "Lift Target")
- MoM delta
- Progress bar (fill color matches badge class)
- Contextual note: 1–2 sentences specific to this account and this month

**Grid layout:**
- TOFU (3 metrics): `grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))`
- MOFU (4 metrics): `grid-template-columns: repeat(2, 1fr)`
- BOFU (3 metrics): `grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))`
- Tablet (≤900px): All grids → 2 columns
- Mobile (≤600px): All grids → 1 column

---

### Section 5: Top 3 Posts

**Posts grid:** 3-column layout. `grid-template-columns: repeat(3, 1fr)`, `gap: 1.25rem`, `align-items: start`. Collapses to 1-column on mobile via `@media(max-width: 900px){.posts-grid{grid-template-columns:1fr}}`. No max-width constraint. Card internals are tighter than single-column version (body padding: 1rem, hook font: .875rem, pstat-val: 1.125rem).

**Each post card contains (v7.1):**
- Rank bar (`.post-rank.r1/r2/r3`): gradient background, rank number, format badge
- Post date + format type (e.g., "March 12, 2026 · Behind-the-Scenes / Personality Reel")
- Post hook: the actual opening line or hook from the post (pulled by visiting the live Instagram post)
- Stats: **Total Views** and **Total Interactions** only (likes + comments + shares + saves combined)
- Retention %: per-reel only (from Metricool). For carousels/static posts, show: "Carousel — no retention metric."
- Why It Worked: 2–3 sentence strategic insight. Lime-tinted background. `▲ Why It Worked` label.
- **"View on Instagram →" button**: clean pill button, `background: var(--azure)`, white text, links to the post URL, `target="_blank"`

**Critical rules (v7.1):**
- **No Instagram embeds.** Do not use `<blockquote class="instagram-media">` or load the Instagram embed script (`//www.instagram.com/embed.js`). This has been removed permanently.
- **Always visit the actual Instagram post URL** before writing post copy — pull the real hook and confirm the format
- Post type label must reflect actual content format — not a generic assumption
- Post insight must be written based on what the content actually is
- `.post-card` should have `overflow: hidden` (embeds no longer present — the overflow:visible workaround is no longer needed)

---

### Section 6: What We Learned (Insights)

4 insight cards summarizing the key signals from the month's data.

**Each card contains:**
- Flag badge: Win (green), Watch (amber), or Signal (blue)
- Title: Specific and opinionated — e.g., "Retention at 72% Signals Content Quality Is Working"
- Body: 2–3 sentences naming the specific data point and what it means strategically

**Tone:** Every insight must name a specific number or post. "The March 12 reel drove 116 interactions — the highest of the month" is good. "Engagement was strong" is not.

---

### Section 7: Next Month's CTAs

**Section name:** "Next Month's CTAs" (previously "April CTA Strategy" — updated dynamically to the actual next month name).

**Structure:**
- Section header with icon (🎯), title "[Next Month] CTA Strategy", sub "Call-to-Action Plan · Aligned to Funnel & Goals"
- Primary CTA Card: The single most important CTA for next month
- Funnel CTA Grid: 3 cards — one per funnel stage (TOFU / MOFU / BOFU)

This section appears *before* Strategy Adjustments.

---

### Section 8: Strategy Adjustments

**Simplified in v7.0.** Three cards only. Maximum scannability.

**Section header:**
- Label: "[Next Month] Direction"
- Title: "Strategy Adjustments"
- Sub: "Three moves for [Next Month] — grounded in [Current Month]'s data."

**Each card contains (simplified from v6.3):**
- Type badge: "Doubling Down" (green) / "Testing Next" (navy) / "Fixing" (amber)
- Headline: Plain-English "What we're doing" — specific and action-oriented
- One-line context: The metric and goal it impacts (e.g., "Reach & Shares · Awareness Goal")
- Single action statement: One sentence on what specifically is being done

**Removed in v7.0:** The detailed "Why" block and "What This Moves" block from v6.3. These added length without adding clarity for the client.

---

### Section 9: Previous Reports

**New in v7.0.** A dark card-grid section showing links to all prior months' reports.

**Placement:** Between Strategy Adjustments and the Footer.

**Structure:**
- Section label: "Report History"
- Title: "Previous Reports"
- Sub: "Compare performance month over month."
- Card grid: One card per prior month, showing month/year, score, score label, and a link to the report

**Design:** Dark background (`#1a1f3a` or similar), card grid layout, clean and minimal.

---

### Section 10: Footer

**Updated in v7.0:**
- Background: `#ffffff` (white) — previously `#151516` (dark)
- Scroll Media logo: navy-on-transparent variant (`scroll-logo-navy.png`)
- Text: dark (`var(--shadow)` or `#151516`)
- "Prepared by Scroll Media — [Month] [Year] Performance Report"
- "Data sources: Instagram Insights, Metricool · Scoring: Scroll Media Weighted Performance Framework v2.0"

---

## 5. Scoring Framework (v7.2 — Unified Intent-Weighted Model)

Both the monthly account score and the top post outlier engine use the same intent-weighted hierarchy. The core principle: the goal of organic social is to reach the highest-quality audience (buyers), not the widest audience.

**Tier Weights:**

| Tier | Weight | Metrics | Rationale |
|---|---|---|---|
| T1 | 1.5x | Saves, Retention %, Link Taps, PCR, CTR | Highest-intent buyer signals. All require a deliberate viewer decision. Saves = pre-purchase bookmarking. Link Taps & CTR = BOFU action. Retention % = content resonance. PCR = profile-to-follower conversion. |
| T2 | 1.0x | Profile Visits, New Followers, Total Views, Shares | Growth and distribution signals. Meaningful but quality-agnostic. Shares drive reach but don't confirm purchase intent. |
| T3 | 0.75x | Comments | Supporting signal. Valuable context but highly variable by niche and content type. |

**Removed from scoring in v7.0:** `Avg Reach / Day` (was T2) and `Avg Watch Time` (was T3). These are internal-only metrics.

**Max weighted points (denominator): 13.25**
- T1 metrics (5): 5 × 1.5 = 7.5
- T2 metrics (4): 4 × 1.0 = 4.0
- T3 metrics (1): 1 × 0.75 = 0.75
- **Total: 13.25** (use 13.25 as denominator)

**Comments data quality rule:** `avg_comments` is floored at 1 (Metricool does not track comments). Comments ratio is capped at 5.0x to prevent inflation from milestone posts.

**Status Points:**

| Status | Condition | T1 (1.5x) | T2 (1.0x) | T3 (0.75x) |
|---|---|---|---|---|
| EXCEEDING | Above high target | 1.5 | 1.0 | 0.75 |
| ON TRACK | Within target range | 0.9 | 0.6 | 0.45 |
| WATCH | Below low target | 0.3 | 0.2 | 0.15 |

**Score Formula:**
1. Sum all 10 weighted points.
2. Raw Score = `(Sum / 13.25) × 10`
3. Apply MoM Trend Credit:
   - 8+ metrics improved MoM: +0.5
   - 5–7 metrics improved: +0.25
   - 3–4 metrics improved: 0
   - <3 metrics improved: −0.25
4. Compressed Score = `6.0 + (Raw Score with Credit × 0.4)`
5. Round to nearest 0.1.

**Score Interpretation:**

| Score | Label |
|---|---|
| 9.5–10.0 | Breakthrough Month |
| 9.0–9.4 | Exceptional Month |
| 8.5–8.9 | Strong Month |
| 8.0–8.4 | Solid Month |
| 7.5–7.9 | Building Month |
| 7.0–7.4 | Progressing Month |
| 6.5–6.9 | Mixed Month |
| 6.0–6.4 | Foundation Month |
| 5.5–5.9 | Early Stage |
| < 5.5 | Baseline |

---

## 6. HTML Report: Technical Standards

### 6.1. Brand Assets

| Asset | Path | Use |
|---|---|---|
| White logo (hero) | `https://reports.scrollmedia.co/assets/scroll-logo-white.png` | Hero header |
| Navy logo (footer) | `https://reports.scrollmedia.co/assets/scroll-logo-navy.png` | Footer |
| Favicon | PNG from `https://files.manuscdn.com/...` or inline base64 | `<link rel="icon">` |

**Logo rules:**
- Hero: white-on-transparent PNG, no background box, `height: 28px`
- Footer: navy-on-transparent PNG, no background box

### 6.2. CSS Variables

```css
:root {
  --shadow: #151516;
  --azure: #0e3387;
  --hl: #e2ed7a;
  --lucid: #cbe9ff;
  --porcelain: #f2f3f4;
  --ghost: #f7f8fc;
  --text: #151516;
  --muted: #6b7280;
  --border: rgba(21,21,22,.09);
  --exceed: #7c3aed;
  --ontrack: #0e3387;
  --watch: #d97706;
  --tofu: #0e3387;
  --mofu: #7c3aed;
  --bofu: #059669;
  --radius: 12px;
  --radius-sm: 8px;
}
```

### 6.3. Typography

**Source Sans 3** from Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
```

### 6.4. Scroll Progress Bar

A fixed progress bar at the top of the page must be included:
```html
<div id="progress-bar"></div>
```
```css
#progress-bar { position: fixed; top: 0; left: 0; height: 3px; width: 0%; background: linear-gradient(90deg, var(--azure), #4f6ef7, var(--hl)); z-index: 9999; transition: width .1s linear; pointer-events: none; }
```
```js
window.addEventListener('scroll', () => {
  const pct = window.scrollY / (document.body.scrollHeight - window.innerHeight) * 100;
  document.getElementById('progress-bar').style.width = pct + '%';
});
```

### 6.5. Responsive Breakpoints

| Breakpoint | Behavior |
|---|---|
| `max-width: 760px` | Hero layout adjusts, stage badge wraps |
| `max-width: 640px` | Metric grids → 2 columns, `.sec` padding reduces |
| `max-width: 580px` | Posts grid adjustments |
| `max-width: 480px` | Score trend bars reduce, single column everywhere |

Viewport meta: `<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=5.0">`

### 6.6. Print Styles

```css
@media print {
  .hero { background: #0c3387 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .wrap { max-width: 100%; }
  .metric-grid { grid-template-columns: repeat(2,1fr) !important; }
}
```

---

## 7. Deployment Process

### 7.1. Repository Structure

GitHub repo: `cgianattasio15/scroll-reports`. Hosted at `reports.scrollmedia.co` via Netlify. File path: `[client-slug]/[monthyear]/index.html`.

### 7.2. Client Slugs (Active as of March 2026)

| Client | Slug | Archive URL |
|---|---|---|
| Launch Party | `shoplaunchparty` | `reports.scrollmedia.co/shoplaunchparty/` |
| Lane & Kate | `laneandkate` | `reports.scrollmedia.co/laneandkate/` |
| Skin by Brownlee & Co | `skinbybrownleeandco` | `reports.scrollmedia.co/skinbybrownleeandco/` |
| MEAS Active | `measactive` | `reports.scrollmedia.co/measactive/` |
| Up and Running OH | `upandrunningoh` | `reports.scrollmedia.co/upandrunningoh/` |
| DEFINE Oakley | `defineoakley` | `reports.scrollmedia.co/defineoakley/` |
| Ombre Gallery | `ombregallery` | `reports.scrollmedia.co/ombregallery/` |

### 7.3. Deployment Steps

1. Build the report HTML and save to `/home/ubuntu/scroll-reports-repo/[client-slug]/[monthyear]/index.html`
2. Commit and push:
```bash
cd /home/ubuntu/scroll-reports-repo
git add [client-slug]/[monthyear]/index.html
git commit -m "Deploy [Client] [Month] [Year] report"
git push origin main
```
3. Verify live (wait 15–30 seconds for Netlify to deploy).
4. Update the main dashboard and client archive page (see Section 7.4).

### 7.4. Dashboard & Archive Update Process

After all reports are deployed, update:
- `/home/ubuntu/scroll-reports-repo/index.html` — main dashboard
- `/home/ubuntu/scroll-reports-repo/[client-slug]/index.html` — each client's archive page

For each client:
- Update the score value, score label, and "Latest Report" month on the dashboard card
- Add a new report card to the archive page (month/year, score, label, link)
- Commit and push all changes together

---

## 8. QA Checklist

### 8.1. Content QA

- [ ] Score calculated using the v3.0 unified intent-weighted scoring model (denominator: 13.25)
- [ ] All 10 customer-facing metrics present and correctly assigned to funnel stage
- [ ] Avg Reach/Day and Avg Watch Time are NOT shown in the report (internal only)
- [ ] MoM deltas accurate (current month vs. prior month)
- [ ] Score trend bars in chronological order (oldest left → newest right)
- [ ] Score badge counts (Exceeding / On Track / Watch) match actual metric statuses
- [ ] Total Followers banner shows correct count, MoM delta, and Target Range
- [ ] All "Target Range" labels used (not "Lift Target" or "Stage Target")
- [ ] TOFU label: "Awareness & Authority"
- [ ] BOFU label: "Consideration & Conversion"
- [ ] Business Goals section: 3 goal cards with progress bars, no individual metrics
- [ ] Top Posts: dynamically selected by Outlier Engine (2-4 posts)
- [ ] Top Posts: 3-column horizontal layout
- [ ] Top Posts: 2-3 standout metrics per post with multiplier vs. account average
- [ ] Top Posts: actual Instagram captions included with Show More toggle for long text
- [ ] Top Posts: Retention % only shown when it is a standout outlier metric
- [ ] Top Posts: insights written based on actual standout metrics (data-backed)
- [ ] CTA section title: "Next Month's CTAs" (not "[Month] CTA Strategy")
- [ ] Strategy Adjustments: 3 simplified cards (no "Why" block, no "What This Moves" block)
- [ ] Previous Reports section present with correct prior month cards
- [ ] Hero: 3 bullet points with bold titles (no paragraph copy, no score number)
- [ ] Stage badge visible in hero
- [ ] Score methodology note NOT present in Score Card
- [ ] Narrative tone positive and action-oriented throughout

### 8.2. Technical QA

- [ ] Scroll Media white logo in hero (no background box)
- [ ] Scroll Media navy logo in footer (no background box)
- [ ] Footer background is white (`#ffffff`)
- [ ] Favicon renders correctly (not a gray globe)
- [ ] Scroll progress bar present and functional
- [ ] No horizontal overflow at 390px mobile viewport
- [ ] Progress bars animate on page load
- [ ] Badge color and bar fill color match on every metric card
- [ ] Each post card has `overflow: visible`
- [ ] All Instagram embeds wrapped in `.post-embed` container
- [ ] Instagram post IDs verified character-by-character for case-sensitivity
- [ ] All external links include `target="_blank" rel="noopener"`
- [ ] Report renders correctly at 1440px, 768px, and 390px

### 8.3. Post-Deployment QA

- [ ] Main dashboard score matches deployed report score
- [ ] Client archive page has new card with correct score and link
- [ ] All archive card scores match deployed report scores

---

## 9. Copy & Tone Standards

**Always lead with the strongest signal.** Hero bullets, insight cards, and goal cards should all open with the most important thing.

**Be specific, not general.** "Retention hit 72% — 7 points above the Lift ceiling" is good. "Retention was strong" is not.

**Positive and action-oriented, always.** Frame challenges as "building toward" — never as failures. Every challenge must be paired with a specific action.

**No internal framework language in client-facing copy.** Do not write "Tier 1 metrics," "TOFU," "IVP," or any internal terminology. Write what it means in plain English.

**No hype.** No exclamation points. No "amazing" or "incredible." Let the data speak.

---

## 10. Data Pipeline: Monthly Workflow

### Step 1: Pull Metricool API Data
- Date range: 1st through 2nd-to-last day of the month
- Endpoints: `/v2/analytics/reels/instagram`, `/v2/analytics/posts/instagram`
- Extract: Views, Shares, Saves, Comments, Retention %, post URLs for Top 3

### Step 2: Confirm IG Insights Data in Master Sheet
- Verify the current month tab in the Master Performance Data Sheet is populated
- IG Insights fields (New Followers, Profile Visits, Link Taps, Total Followers) must be entered manually by the team
- If any IG Insights fields are missing, flag to the team before building reports

### Step 3: Run Top Post Outlier Engine
- Run `python3 /home/ubuntu/skills/performance-reports/scripts/outlier_engine.py`
- This script automatically pulls all posts/reels from Metricool, calculates composite outlier scores, and selects 2-4 top posts.
- It identifies the 2-3 standout metrics for each post and generates the data-backed "Why It Worked" narrative.
- Ensure floor thresholds are met (Saves ≥4, Shares ≥4) for standout metrics.

### Step 4: Calculate Scores
- Use the v3.0 unified intent-weighted scoring model (Section 5) — denominator: 13.25, T1: Saves/Retention/Link Taps/PCR/CTR at 1.5x, T2: Profile Visits/New Followers/Total Views/Shares at 1.0x, T3: Comments at 0.75x
- Pull prior month data from the Master Sheet for MoM deltas and trend credit
- Pull score history from the Monthly Scorecard sheet

### Step 5: Pull Client Goals
- Source from the Account Homebase reference spreadsheet
- Three goals per client (TOFU / MOFU / BOFU)

### Step 6: Build Reports
- Follow Section 4 section-by-section build guide
- Use DEFINE Oakley March 2026 as the canonical design reference

### Step 7: Deploy and Update
- Follow Section 7 deployment process
- Update dashboard and archive pages after all reports are deployed

### Step 8: Post-Reporting Documentation (v7.2)
- Fill out the **Master Client Performance Feedback Sheet** (`13YmL11vuLX3e_bT51ORjqUSgS7stKRiLJR1rQ7AmVMQ`) documenting the most notable takeaways for each part of the funnel (TOFU, MOFU, BOFU) for each client.
- **Format Rule:** Each cell must start with a **Bold Title** capturing the overall theme, followed by a short summary describing the point.
- Update any documentation or skills connected to this performance reporting process to capture all latest refinements.

---

## 11. Starting a New Report: Copy-Paste Prompts

### Default Monthly Batch Prompt (All Active Clients)

```
I need the [Month] [Year] performance reports for all active clients.

Please read the Scroll Media Monthly Performance Reporting Process v7.2 from the skills/performance-reports/references/ directory before starting. Follow it exactly.

MASTER PERFORMANCE DATA SHEET: [Google Sheets link — current month tab must be populated]
MONTHLY SCORECARD SHEET: [Google Sheets link]
ACCOUNT HOMEBASE REFERENCE: [Google Sheets link]

For each client:
- Pull metrics from the Master Performance Data Sheet (current month tab)
- Confirm IG Insights fields are populated; flag any missing values before building
- Pull top 3 posts from Metricool API, then visit each post URL on Instagram to get the actual caption and format
- Pull score history from the Monthly Scorecard sheet
- Pull client goals from the Account Homebase reference sheet

Use DEFINE Oakley March 2026 as the canonical design template.

Once all reports are built:
1. Deploy all reports to reports.scrollmedia.co
2. Update all client archive pages with the new report card and correct scores
3. Update the main dashboard with new scores and report links
4. Run QA checklist (Section 8) and fix any issues before confirming
5. Confirm all live URLs
```

### Single Client Report Prompt

```
I need to build the [Month] [Year] performance report for [Client Name].

Please read the Scroll Media Monthly Performance Reporting Process v7.2 before starting. Follow it exactly.

MASTER PERFORMANCE DATA SHEET: [Google Sheets link]
MONTHLY SCORECARD SHEET: [Google Sheets link]
ACCOUNT HOMEBASE REFERENCE: [Google Sheets link]

Use DEFINE Oakley March 2026 as the canonical design template.
```

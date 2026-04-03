# Scroll Media Monthly Performance Reporting Process — v6.4

**Last Updated:** March 6, 2026
**Version:** 6.4
**Framework Owner:** Chase (Chief Strategist)

This document is the **single source of truth** for creating, QA-ing, and deploying monthly client performance reports. It serves as both a technical instruction set for AI agents and a standard operating procedure (SOP) for the Scroll Media team.

---

## WHAT CHANGED IN v6.4

**Top 3 Posts: Single-Column Layout (codified).** The canonical layout for the Top 3 Posts section is now explicitly defined as a single-column, centered layout. The posts grid must use `grid-template-columns: 1fr` with a `max-width: 580px` centered container — not a multi-column `auto-fill` grid. This standard was confirmed during the February 2026 reporting cycle and is now the required layout for all reports, including retroactive fixes to prior months. The full CSS spec is documented in Section 5.

**Top 3 Posts: Post Embed Container (codified).** Each Instagram embed must be wrapped in a `<div class="post-embed">` container that uses `display: flex; justify-content: center`. The embed `<blockquote>` must have `max-width: 400px`. The `.post-card` parent must have `overflow: visible` — not `overflow: hidden`. These rules prevent embed clipping and rendering failures. The full HTML structure is documented in Section 5.

**Dashboard & Archive Update Process (new).** After deploying individual client reports, the main dashboard (`index.html`) and each client's archive page (`[client-slug]/index.html`) must be updated to reflect the new report's score and link. This step was previously undocumented. The full update process, including which fields to change and in what order, is documented in Section 7.4.

**Instagram Permalink Case-Sensitivity Protocol (new).** Instagram post IDs are case-sensitive. A single incorrect uppercase or lowercase character in the post ID will cause the embed to silently fail — the blockquote renders as a blank card with no error. When an embed fails to load and the fallback protocol does not apply (i.e., the post is public and not collaborative), the first diagnostic step is to verify the exact post ID character-by-character against the original Instagram share link. The QA checklist in Section 8 has been updated to include this check.

**Client Metadata Corrections (updated).** The Master Client Roster is the authoritative source for niche, subniche, and stage values. During the February 2026 cycle, two clients had incorrect niche labels in their archive pages (MEAS Active was labeled "Jewelry / Retail" instead of "Athletic Wear"; Skin by Brownlee & Co was labeled "Fine Jewelry / Custom Engagement Rings" instead of "Med Spa / Aesthetics"). These have been corrected. When building or updating any report or archive page, always pull niche and stage values from the Master Client Roster — never copy from a prior report.

## WHAT CHANGED IN v6.3

**Section Order Change (confirmed).** The canonical report section order has been updated. The **CTA Strategy** section now appears as its own standalone dark section *before* the **Strategy Adjustments** section. This is the confirmed order for all reports going forward.

**CTA Strategy Section (new full spec).** The CTA section is now a standalone dark-themed section (`<section class="cta-section">`) with a dedicated header, a primary CTA card, and a 3-card funnel-stage CTA grid. The full HTML structure, CSS classes, and content spec are documented in Section 4.

**Strategy Adjustments Section (complete rebuild).** The previous "Month Ahead" section has been replaced with a new, highly-structured 3-card grid. The old format (bulleted rationale, effective date, phase) has been retired. The new format uses a numbered priority circle, a badge type, a plain-English headline, a data-grounded "Why" block, and a goal-mapped "What This Moves" block. The full spec is documented in Section 4.

**Business Goals Formatting (standardized).** The Business Goals section design is now strictly standardized. Each goal card must have a top border color-coded to its status, a funnel-stage dot, a status badge, a KPI block, a narrative paragraph, and a "Mar Focus" action line. The full CSS class spec is documented in Section 6.

**Embed Fallback Protocol (new).** A formal protocol for handling broken Instagram embeds has been added to Section 4. Any post embed that fails to render (typically collaborative posts, private accounts, or restricted posts) must include a styled "View on Instagram" fallback link button inside the `<blockquote>`.

**QA Process Formalized (updated).** The QA process is now a two-step process: (1) run the automated `qa_audit.py` Python script to verify structural and data integrity, then (2) perform the manual visual audit. The QA checklist in Section 8 has been updated to reflect both steps.

## WHAT CHANGED IN v6.2

**Multi-Client Batch Prompt (new).** A new one-shot prompt has been added (Prompt 4) for building all active client reports in a single task. This is now the default workflow for monthly reporting. All data sources are provided upfront as Google Sheet and Google Drive links — no manual metric entry required.

**Data Source Hierarchy Clarified (updated).** The Account Homebase and IG Insights Google Sheet are the authoritative sources for all account-level metrics. Metricool CSVs are used for post-level data only (top 3 posts). This distinction is now explicit in Section 3.

**Top 3 Posts Sourcing (updated).** Top 3 posts are now pulled automatically from **Tab 6 (Content Archive)** of each client's Account Homebase. No manual post data entry is required.

**Score History Sourcing (updated).** Score trend history is pulled automatically from the **Score History Google Sheet**. No manual score entry is required.

**5-Stat Reel Grid (new).** Reels with retention data now display a 5-stat grid (3-column layout: Views / Saves / Comments on row 1, Shares / Retention on row 2) instead of the standard 4-stat 2×2 grid.

**Hero Text Rule (new).** The hero section must NOT contain a score narrative paragraph or score summary text. The score narrative lives exclusively in the Monthly Score Card section. The hero contains only: client name, niche/subniche badges, and the pills row.

**Outlier Post Handling (new).** When a post is flagged as an outlier in the Content Archive (e.g., anomalously high views with low engagement quality), include it as the #1 post but label it with an "Outlier Post" badge and note in the "Why It Worked" copy that the metrics are not representative of baseline performance.

---

## 1. System Overview & Purpose

The monthly performance report is Scroll Media's most critical client-facing deliverable. It is not a data dump. It is a strategic narrative — a document that tells the story of the month, connects performance to business goals, and builds the client's confidence in Scroll Media's direction.

The report serves four functions simultaneously. It **communicates performance** by showing the client exactly how their social media presence is performing against their goals, with every metric in context. It **demonstrates value** by connecting social media metrics to the client's specific business outcomes — not just vanity numbers, but signals that map to their purchasing journey. It **builds trust** through transparent, data-driven analysis that never hides problems and always pairs challenges with a clear action plan. And it **drives strategy** by using performance data to justify the following month's adjustments, making the report the foundation of the monthly recap call.

Reports are delivered as a single, self-contained HTML file, hosted on `reports.scrollmedia.co`. The URL structure is: `https://reports.scrollmedia.co/[client-slug]/[monthyear]/` (e.g., `https://reports.scrollmedia.co/shoplaunchparty/february2026/`).

---

## 2. Audience & Roles

| Audience | Role & Directives |
|---|---|
| **AI Agents (Manus)** | This is your primary instruction manual. The rules, structures, and formats defined here are non-negotiable and must be followed exactly. Your function is to build the report with precision, deploy it to GitHub, and verify it is live before marking the task complete. |
| **Scroll Media Team** | This is your operational playbook. Use it to understand the 'why' behind the report structure, the logic of the scoring framework, and the standards for client-facing communication. Your function is to provide the data and strategic context that Manus needs to build the report. |

---

## 3. Prerequisites: What You Need Before Starting

Before building any report, the following information must be gathered. The Master Client Roster (`Client_Roster__Master.xlsx`) in the project files is the primary source for client metadata. Pull from there first before asking the user.

### 3.1. Client Metadata (from Master Client Roster)

| Field | Where to Find It | Notes |
|---|---|---|
| Client Name | Master Client Roster, Column A | |
| Instagram Handle | Master Client Roster, Column N | |
| Niche | Master Client Roster, Column D | Broad category (e.g., "Athletic Wear") |
| Subniche | Master Client Roster, Column E | Specific positioning (e.g., "Women's Athletic & Lifestyle Apparel") |
| Account Manager | Master Client Roster, Column B | First name only in the report |
| Stage | Master Client Roster, Column C | Spark / Lift / Rise / Thrive |
| Package | Master Client Roster, Column I | Signature / Custom / A La Carte |
| Posts Per Week | Master Client Roster, Column K | |
| Start Date | Master Client Roster, Column F | Used to calculate Month # |
| MRR | Master Client Roster, Column H | Internal only — do not include in report |

**Critical rule:** Always pull niche, subniche, and stage values directly from the Master Client Roster. Never copy these values from a prior report or archive page — they may be stale or incorrect.

### 3.2. Performance Data — Sources & Calculation

**Data Source Hierarchy (critical):** The following priority order must be followed when sourcing metrics. Higher-priority sources override lower-priority sources.

| Priority | Source | Used For |
|---|---|---|
| 1 (highest) | Account Homebase — Tab 05 (Performance Data) | All 12 account-level KPIs |
| 2 | IG Insights Google Sheet | New Followers, Profile Visits, Link Taps |
| 3 (lowest) | Metricool CSV | Post-level data only (Top 3 Posts section) |

All 12 KPIs are sourced from the Account Homebase and IG Insights sheet. **No manual metric entry is required.** CTR and PCR are calculated automatically from the data in those files. Metricool CSVs are used exclusively for individual post stats in the Top 3 Posts section.

**Data Source 1: Metricool CSV Export**

The Metricool CSV contains the following 7 metrics. Export the CSV for the full report month and attach it to the task.

| Metric | Funnel Stage | Tier | Metricool Column Name |
|---|---|---|---|
| Avg Reach / Day | TOFU | T2 | Daily Reach (average across the month) |
| Shares | TOFU | T1 | Shares |
| Total Views | TOFU | T2 | Impressions / Views |
| Avg Watch Time | MOFU | T3 | Avg. Playback Time (seconds) |
| Retention % | MOFU | T1 | Avg. Watch Time ÷ Reel Length × 100 |
| Saves | MOFU | T1 | Saves |
| Comments | MOFU | T3 | Comments |

**Data Source 2: IG Insights Google Sheet**

The IG Insights sheet is a monthly tracker maintained by the team. It contains metrics that Instagram does not expose via Metricool. The sheet has one row per client and the following columns: Account, Status, Total Followers, New Followers, Profile Visits, Link Taps. Attach the sheet (or a screenshot/export of it) for the report month.

| Metric | Funnel Stage | Tier | Sheet Column |
|---|---|---|---|
| New Followers | TOFU | T2 | New Followers |
| Profile Visits | MOFU | T2 | Profile Visits |
| Link Taps | BOFU | T2 | Link Taps |

**Calculated Metrics (no input required)**

The following 2 metrics are derived automatically from the IG Insights data:

| Metric | Funnel Stage | Tier | Formula |
|---|---|---|---|
| CTR (Click-Through Rate) | BOFU | T1 | Link Taps ÷ Profile Visits × 100 |
| PCR (Profile Conversion Rate) | BOFU | T1 | New Followers ÷ Profile Visits × 100 |

**Prior Month Data:** Attach the Metricool CSV and IG Insights sheet for the prior month as well. All MoM delta calculations and the MoM trend credit require both months.

**Top 3 Posts:** Pulled automatically from **Tab 6 (Content Archive)** of each client's Account Homebase. Posts are ranked by total views. No manual post data entry is required. See outlier handling rule in the "What Changed" section above.

**Score Trend History:** Pulled automatically from the **Score History Google Sheet** (provided as a link in the task). No manual score entry is required. If a client has fewer than 4 months of history, show only the available months (minimum 2 bars).

### 3.3. Client Goals (from Content Strategy Map)

The client's 3 business goals are sourced from the **Content Strategy Map** (Tab 03 of the Account Homebase, or the standalone Content Strategy Map document). The "Goals" column contains the 3 goal titles. Read the full row for each goal to understand the funnel stage, KPI mapping, and strategic intent.

**Goal-to-KPI Mapping Logic:**

| Funnel Stage | Goal Type | Primary KPI to Feature in Report |
|---|---|---|
| TOFU | Discoverability / Awareness | Avg Reach/Day or New Followers |
| MOFU | Community / Trust | Saves or Comments |
| BOFU | Conversion / Sales | CTR or Link Taps |

### 3.4. Strategic Context (from Account Manager)

Before writing any narrative copy, the Account Manager should provide: any major events, campaigns, or one-off occurrences during the report month; any specific client questions or concerns from the last recap call; and any context that explains unusual metric movements (e.g., a viral post, a product launch, a platform algorithm change).

---

## 4. Report Architecture: Section-by-Section Build Guide

Every report is built in the following order. **Do not skip sections or reorder them.** This order is non-negotiable as of v6.3.

1. Hero Header
2. Monthly Score Card
3. Business Goals
4. Performance Dashboard
5. Top 3 Posts
6. What We Learned (Insights)
7. CTA Strategy
8. Strategy Adjustments
9. Footer

---

### Section 1: Hero Header

The hero is the first thing the client sees. It must establish identity, context, and tone in under 5 seconds.

**Required elements:**
- Scroll Media logo (linked from `https://reports.scrollmedia.co/assets/scroll-media-logo-white.png` with `onerror="this.style.display='none'"` fallback)
- Eyebrow label: "Monthly Performance Report" (with a yellow dot accent)
- Niche and subniche badge row (`.hero-niche-row`)
- Client Name + Month + Year (H1)
- Hero tagline (`.hero-tagline`): The month's narrative label — e.g., "Lift Stage — Consistent Performer"
- Hero sub paragraph (`.hero-sub`): 1–2 sentences summarizing the month's most important signal. Lead with the strongest metric. Do NOT include a score number here.
- Pills row (`.hero-pills`): Total Followers, Total Views, Posts Published, Date Range

**Design rules:**
- Hero background is always dark gradient: `linear-gradient(135deg, #151516 0%, #1a1a1c 100%)`
- Niche badge (`.hero-niche-badge.niche`): white/frosted background
- Subniche badge (`.hero-niche-badge.subniche`): yellow-tinted background with yellow border
- The hero tagline pill uses the same narrative label as the Score Card title (keep them consistent)
- **Critical rule:** The hero must NOT contain a score number or score narrative paragraph. The score lives exclusively in the Score Card section.

---

### Section 2: Monthly Score Card

The score card is the quantitative anchor of the report. It must be calculated using the Scoring Framework (see Section 5) before any narrative copy is written.

**HTML structure:** The score card is wrapped in a `.score-wrap.wrap` div that has `margin: -3.5rem auto 2rem` — this pulls it up to overlap the hero's bottom padding, creating a visual connection between the hero and the score card.

**Required elements inside `.score-card`:**
- Score eyebrow: "February 2026 Monthly Score" (`.score-eyebrow`)
- Score number: `X.X / 10` (`.score-num` with `.score-denom` for the "/10")
- Score title: The month's story in 5–8 words (`.score-title`)
- Score description: 2–3 sentences in strategic context (`.score-desc`). Lead with the strongest signal. Explain the gap. End with forward momentum.
- Framework note (`.score-note`): Small-print italic text explaining the scoring methodology and any MoM credits applied.
- Score trend section (`.score-trend-section`): Dark background bar chart showing 3–4 months of history.
- Score trend delta (`.score-trend-delta`): MoM change statement, placed immediately after the trend section, inside the `.score-card` div.

**Score Trend Bar Chart spec:**
- Container background: `#111112` (near-black), `border-radius: 10px`, `padding: 2.5rem 1.5rem 1rem`
- Label: "Score Trend" (`.score-trend-label`), all-caps, very small, low-opacity white
- Bars container (`.score-trend-bars`): `display: flex`, `align-items: flex-end`, `height: 140px`
- Each column (`.trend-col`): contains a `.trend-bar-wrap` (width 40px, height 120px), a `.trend-score`, and a `.trend-month`
- Prior month bars: `background: rgba(255,255,255,0.45)`, score text in muted white
- Current month bar: `background: #3b82f6` (blue), score text in full white, bold
- **Bar height scaling formula:** `height_pct = 20 + ((score - min_score) / (max_score - min_score)) * 72`. If all scores are equal, set all bars to 50%.
- **Critical:** `.trend-bar-wrap` background must be `transparent` — a semi-transparent background creates a visible cap artifact above the bars.
- **Critical:** `.score-card` must NOT have `overflow: hidden` — this clips the bar tops.

**Score Badges:** Placed in a separate `.score-badges` div *outside and below* the `.score-card` div. Three badges: Exceeding (purple), On Track (green), Watch (amber). The counts must match the actual metric statuses in the Performance Dashboard.

---

### Section 3: Business Goals

This section directly answers the question every client has when they open a performance report: *"Is this actually helping my business?"*

**HTML structure:** Wrapped in `<div class="goals-section wrap">`. This section sits between the Score Card and the Performance Dashboard.

**Section header:**
- Label (`.goals-section-label`): "Business Goals"
- Title (`.goals-section-title`): "How [Month] Moves the Needle"
- Sub (`.goals-section-sub`): "Your three core business goals, mapped to [Month]'s social performance."

**Grid:** `<div class="goals-grid">` — 3 columns at desktop, 1 column at mobile.

**Each goal card (`.goal-card`) contains:**

1. **Top border color** (via `::before` pseudo-element, height 3px):
   - `.goal-card.goal-exceed::before` → `background: var(--green)` (#10b981)
   - `.goal-card.goal-ontrack::before` → `background: var(--azure)` (#0c3387)
   - `.goal-card.goal-building::before` → `background: #f59e0b`
   - `.goal-card.goal-watch::before` → `background: #ef4444`

2. **Funnel Stage Tag (`.goal-funnel-tag`):** A row with a colored dot (`.goal-funnel-dot`) and the funnel stage label. Dot colors: `.tofu` = `var(--azure)` (navy), `.mofu` = `var(--purple)`, `.bofu` = `var(--green)`.

3. **Goal Title (`.goal-title`):** The exact goal language from the Content Strategy Map.

4. **Status & KPI Row (`.goal-status-row`):** A flex row containing:
   - **KPI Block (`.goal-kpi-block`, `flex: 1`):** Contains the KPI label (`.goal-kpi-label`), the current value (`.goal-kpi-value`), and the MoM delta (`.goal-kpi-delta.pos` for positive, `.goal-kpi-delta.neg` for negative).
   - **Status Badge (`.goal-status-badge`):** One of four statuses:
     - `.exceed` → green background, "Exceeding"
     - `.ontrack` → navy background, "On Track"
     - `.building` → amber background, "Building"
     - `.watch` → red background, "Watch"

5. **Narrative (`.goal-narrative`):** 2–3 sentences explaining what the KPI result means for this client's business. Always positive and action-oriented. Never use "missed" or "failed."

6. **Mar Focus (`.goal-action`):** A row with a label (`.goal-action-label`: "Mar Focus") and a specific action sentence (`.goal-action-text`). Must be specific and action-oriented — not vague.

**Tone rules:**
- Always positive and action-oriented, even when a goal is in "Building" status.
- The next-month focus line must name a specific format, content type, or tactic — not a generic commitment.
- Frame challenges as "building toward" or "normalizing from" — never as failures.
- Scroll Media does not promise sales. Frame progress in terms of metrics that signal movement through the customer journey.

---

### Section 4: Performance Dashboard

The dashboard is the data layer of the report. It shows all 12 KPIs grouped by funnel stage.

**Structure:**
- Section label: "Performance Dashboard"
- Section title: "[Month] Metrics"
- Section description: "All 12 tracked metrics grouped by funnel stage. Targets reflect the [Stage] stage range. Progress bars show actual vs. the high target."
- Three funnel groups: TOFU, MOFU, BOFU — each with a colored header bar (`.funnel-header`) and a metric card grid.

**Funnel header colors:**
- `.funnel-header.tofu`: `background: rgba(12,51,135,.06)`, `border-left: 3px solid var(--tofu)` (navy)
- `.funnel-header.mofu`: `background: rgba(124,58,237,.06)`, `border-left: 3px solid var(--mofu)` (purple)
- `.funnel-header.bofu`: `background: rgba(16,185,129,.06)`, `border-left: 3px solid var(--bofu)` (green)

**Metric card structure (each of the 12 cards):**
- Metric name (`.mc-name`)
- Status badge (`.mc-badge`): `.exceed`, `.ontrack`, or `.watch`
- Actual value (`.mc-actual`): color-coded to match badge — `.exceed` = purple, `.ontrack` = green, `.watch` = amber
- Target range (`.mc-target`)
- MoM delta (`.mc-mom`): `.mom-up` = green, `.mom-down` = amber, `.mom-flat` = muted
- Progress bar (`.bar-track` > `.bar-fill`): color class must match the badge class (`.exceed`, `.ontrack`, or `.watch`). **The bar fill color class must always match the badge class — mismatches are a QA error.**
- `data-w` attribute on `.bar-fill`: the percentage width to animate to (capped at 100). Formula: `(actual / high_target) * 100`.
- Contextual note (`.mc-note`): 1–2 sentences specific to this account and this month.

**Grid layout rules:**
- TOFU: 4 metrics — `grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))`
- MOFU: 5 metrics — `grid-template-columns: repeat(2, 1fr)` (explicit 2-column to avoid unbalanced layout)
- BOFU: 3 metrics — `grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))`
- Tablet (≤900px): All grids collapse to 2 columns
- Mobile (≤600px): All grids collapse to 1 column

**Progress bar animation:** Bars animate on page load via a JavaScript snippet at the bottom of the `<body>`:
```js
document.querySelectorAll('.bar-fill[data-w]').forEach(el => {
  setTimeout(() => { el.style.width = el.dataset.w + '%'; }, 200);
});
```

---

### Section 5: Top 3 Posts

This section surfaces the 3 posts that drove the most strategic value during the month.

**Posts grid layout (critical — confirmed standard as of v6.4):**

The posts grid must use a single-column, centered layout. This is the only accepted layout.

```css
.posts-grid {
  display: grid;
  grid-template-columns: 1fr;
  max-width: 580px;
  margin: 0 auto;
  gap: 2rem;
}
```

Do NOT use `grid-template-columns: repeat(auto-fill, minmax(300px, 1fr))` or any multi-column layout for the posts grid. Multi-column layouts cause cards to render cramped and side-by-side, which is incorrect.

**Each post card (`.post-card`) contains:**
- Rank bar (`.post-rank-bar.rank1/2/3`): gradient background, rank number, format badge
- Format badge (`.post-fmt-badge`): `.reel` (navy), `.carousel` (purple), `.static` (green)
- Post body (`.post-body`): content pillar (`.post-pillar`), title (`.post-title`), date (`.post-date`), hook (`.post-hook`), stats grid, "Why It Worked" copy (`.post-why`), and link (`.post-link`)
- Instagram embed: `<div class="post-embed">` containing the `<blockquote class="instagram-media">` element

**Critical `.post-card` CSS rules:**
```css
.post-card {
  overflow: visible; /* MUST be visible — overflow: hidden clips Instagram embed iframes */
}
```

**Post stats grid layout:**
- Standard posts (Carousels, Statics): 2×2 grid — Views/Saves on row 1, Comments/Shares on row 2
- Reels with Retention %: 5-stat 3-column grid — Views/Saves/Comments on row 1, Shares/Retention on row 2
- Use `grid-template-columns: 1fr 1fr` for standard, `grid-template-columns: 1fr 1fr 1fr` for Reels with retention

**Instagram Embed Structure (required):**

Each embed must be wrapped in a `.post-embed` container. The blockquote must have `max-width: 400px`. Do not place a separate "View on Instagram" text link outside the blockquote — the embed itself handles the link.

```html
<div class="post-embed">
  <blockquote class="instagram-media"
    data-instgrm-captioned
    data-instgrm-permalink="https://www.instagram.com/reel/[POST_ID]/?utm_source=ig_embed&amp;utm_campaign=loading"
    data-instgrm-version="14"
    style="background:#FFF;border:0;border-radius:3px;box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15);margin:1px;max-width:400px;min-width:326px;padding:0;width:99.375%;width:-webkit-calc(100% - 2px);width:calc(100% - 2px);">
    <div style="padding:16px;">
      <a href="https://www.instagram.com/reel/[POST_ID]/" style="background:#FFFFFF;line-height:0;padding:0 0;text-align:center;text-decoration:none;width:100%;" target="_blank">View on Instagram</a>
    </div>
  </blockquote>
</div>
```

**Required CSS for `.post-embed`:**
```css
.post-embed {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
}
```

**Instagram Post ID Case-Sensitivity Protocol (critical — new in v6.4):**

Instagram post IDs are case-sensitive. A single incorrect character case will cause the embed to silently fail — the blockquote renders as a blank or broken card with no browser error. This is the most common cause of embed failures on non-collaborative, public posts.

**Diagnostic steps when an embed fails to load:**
1. Confirm the post is public and not a collaborative post (co-authored). If it is collaborative or private, use the Fallback Protocol below instead.
2. If the post is public and non-collaborative, open the original Instagram share link provided by the Account Manager.
3. Extract the post ID from the URL (the alphanumeric string between `/reel/` or `/p/` and the next `/`).
4. Compare the post ID character-by-character against the `data-instgrm-permalink` value in the HTML. Pay particular attention to letters that are visually similar in different cases (e.g., `I` vs `l`, `j` vs `J`, `k` vs `K`).
5. Replace the incorrect post ID in both the `data-instgrm-permalink` attribute and the `<a href>` fallback link inside the blockquote.

**Example of a case-sensitivity error:**
- Incorrect: `data-instgrm-permalink="https://www.instagram.com/reel/DTS4AtdIXXk/..."` (capital `I`, lowercase `k`)
- Correct: `data-instgrm-permalink="https://www.instagram.com/reel/DTS4AtdjXXK/..."` (lowercase `j`, uppercase `K`)

**Instagram Embed Fallback Protocol (critical):**
If an Instagram post embed fails to load because the post is a collaborative post (co-authored), from a private account, or has been archived, the `<blockquote>` must include a fallback link button. This prevents a blank or broken embed from appearing in the report.

```html
<blockquote class="instagram-media" data-instgrm-permalink="[POST_URL]" ...>
  <div style="padding:16px;text-align:center">
    <a href="[POST_URL]" target="_blank" rel="noopener" class="post-link"
       style="display:inline-flex;align-items:center;gap:.375rem;font-size:.75rem;font-weight:600;color:#0c3387;text-decoration:none;border:1px solid rgba(12,51,135,.2);padding:.375rem .75rem;border-radius:4px">
      &#8599;&nbsp;View on Instagram
    </a>
  </div>
</blockquote>
```

**When to use the fallback:** Any time a post is a collaborative post (co-authored), from a private account, or has been archived. If unsure, add the fallback — it renders invisibly when the embed loads successfully.

The Instagram embed script must be included at the bottom of the `<body>`:
```html
<script async src="//www.instagram.com/embed.js"></script>
```

---

### Section 6: What We Learned (Insights)

4 insight cards summarizing the key signals from the month's data. These are strategic takeaways, not metric recaps.

**Grid:** `<div class="insights-grid">` — `grid-template-columns: repeat(auto-fill, minmax(320px, 1fr))`

**Each card (`.insight-card`) contains:**
- Flag badge (`.insight-flag`): `.win` (green), `.watch` (amber), or `.signal` (blue)
- Title (`.insight-title`): Specific and opinionated — e.g., "Trend-Forward Content Is the Shares Engine", not "Shares Were High"
- Body (`.insight-body`): 2–3 sentences naming the specific data point and what it means strategically

**Tone rules:** Insights must be opinionated and specific. Every insight must name a specific number or post. "The Feb 26 Reel drove 112 shares — more than the rest of the month combined" is good. "Engagement was strong this month" is not.

---

### Section 7: CTA Strategy

This section appears *before* Strategy Adjustments. It is a standalone dark section — it sits *outside* the `.wrap.main-content` div and is rendered at full width.

**HTML placement:**
```html
</div><!-- close .wrap.main-content -->
<section class="cta-section">
  <div class="cta-section-inner">
    ...
  </div>
</section>
<div class="wrap">
  <section class="sec"><!-- Strategy Adjustments -->
```

**Section structure:**

**Header (`.cta-section-header`):**
- Icon div (`.cta-section-icon`): 44×44px rounded square, dark background, emoji icon (🎯)
- Title (`.cta-section-title`): "[Next Month] CTA Strategy"
- Sub (`.cta-section-sub`): "Call-to-Action Plan · Aligned to Funnel & Goals"

**Primary CTA Card (`.cta-primary-card`):**
- Top border: 3px gradient (`linear-gradient(90deg, #6366f1, #8b5cf6, #a78bfa)`)
- Label pill (`.cta-primary-label`): "★ Primary Monthly CTA" — purple-tinted background
- Objective (`.cta-primary-objective`): The primary conversion goal in plain English
- Meta chips (`.cta-primary-meta` > `.cta-meta-chip`): Type, Mechanism, Primary KPI
- Copy block (`.cta-primary-copy-block`): Suggested caption copy in italic, with a left border accent
- Rationale (`.cta-primary-rationale`): 2–3 sentences explaining why this CTA is the primary focus for this client's niche and business model

**Funnel CTA Grid (`.cta-funnel-grid`):** 3 columns at desktop, 1 column at mobile (≤768px).

**Each funnel card (`.cta-funnel-card`) contains:**
- Header row: Stage badge (`.cta-stage-badge.tofu/mofu/bofu`) and icon
- CTA type (`.cta-funnel-type`): e.g., "Save CTA", "Question CTA", "Book / Inquire CTA"
- Copy example (`.cta-funnel-copy`): Italic suggested caption copy
- Meta rows (`.cta-funnel-meta`): Mechanism and Primary KPI
- Rationale (`.cta-funnel-rationale`): 1–2 sentences explaining why this CTA fits this funnel stage for this client

**Stage badge colors:**
- `.cta-stage-badge.tofu`: green-tinted (`rgba(16,185,129,0.15)`, color `#34d399`)
- `.cta-stage-badge.mofu`: amber-tinted (`rgba(245,158,11,0.15)`, color `#fbbf24`)
- `.cta-stage-badge.bofu`: red-tinted (`rgba(239,68,68,0.15)`, color `#f87171`)

---

### Section 8: Strategy Adjustments

This is the final content section before the footer. It has been completely redesigned for clarity and client readability.

**HTML placement:** Inside a `<div class="wrap">` wrapper, as a standard `<section class="sec">`.

**Section header:**
- Label (`.sec-label`): "[Next Month] Direction"
- Title (`.sec-title`): "Strategy Adjustments"
- Sub (`.sec-sub`): "Three high-priority moves for [Next Month] — grounded in [Current Month]'s data and mapped to your core business goals."

**Grid:** `<div class="adj-grid">` — `grid-template-columns: repeat(3, 1fr)` at desktop, `1fr` at tablet/mobile (≤900px).

**Exactly 3 cards per report. No more, no fewer.**

**Each card (`.adj-card`) structure:**

**Top section (`.adj-card-top`):**
- Numbered circle (`.adj-num`): 32×32px circle with priority number (1, 2, or 3). Color class must match the badge type:
  - `.adj-num.doubling` → green circle (`rgba(16,185,129,.12)`, color `#059669`)
  - `.adj-num.fixing` → amber circle (`rgba(245,158,11,.12)`, color `#d97706`)
  - `.adj-num.testing` → navy circle (`rgba(12,51,135,.1)`, color `var(--azure)`)
- Badge (`.adj-type-badge`): One of three types. Color class must match the numbered circle:
  - `.adj-type-badge.doubling` → "Doubling Down" (green)
  - `.adj-type-badge.fixing` → "Fixing" (amber)
  - `.adj-type-badge.testing` → "Testing Next" (navy)
- Headline (`.adj-headline`): Plain-English "What we're doing" summary. Should be specific and action-oriented.
- Context (`.adj-context`): Sub-line indicating the metric and goal it impacts (e.g., "Reach & Shares · Awareness Goal").

**Body section (`.adj-body`):**
- Why block (`.adj-why-block`): Gray background block. Contains a label (`.adj-why-label`: "Why") and a paragraph (`.adj-why-text`) grounded in specific data — must name a specific metric, post, or data point.
- What This Moves block (`.adj-moves-block`): Bordered block with an arrow icon (`.adj-moves-icon`: "↗"). Contains a label (`.adj-moves-label`: "What This Moves") and a paragraph (`.adj-moves-text`) explaining the goal-oriented outcome.

**Framing rules:**
- Each adjustment must be grounded in a specific data point from the current month's performance.
- The "What This Moves" outcome must map back to one of the client's 3 business goals.
- Never write "we will post X times per week." Write "we are prioritizing X format" or "we are shifting focus toward Y content type."
- The 3 adjustments should represent the 3 highest-leverage moves — not a comprehensive list of everything being done.

---

## 5. Scoring Framework (Summary)

The full scoring methodology is documented in `Scroll Media — Monthly Performance Scoring Framework v2.0.md`. The following is a summary for quick reference.

**Tier Weights:**

| Tier | Weight | Metrics |
|---|---|---|
| T1 | 1.5x | Saves, Shares, Retention %, CTR, PCR |
| T2 | 1.0x | Avg Reach/Day, New Followers, Total Views, Profile Visits, Link Taps |
| T3 | 0.75x | Comments, Avg Watch Time |

**Status Points:**

| Status | Condition | T1 | T2 | T3 |
|---|---|---|---|---|
| EXCEEDING | Above high target | 1.5 | 1.0 | 0.75 |
| ON TRACK | Within target range | 0.9 | 0.6 | 0.45 |
| WATCH | Below low target | 0.3 | 0.2 | 0.15 |

**Score Formula:**
1. Sum all 12 weighted points.
2. Raw Score = `(Sum / 14.0) × 10`
3. Apply MoM Trend Credit (±0.25 or ±0.5 based on how many metrics improved vs. declined).
4. Compressed Score = `6.0 + (Raw Score with Credit × 0.4)`
5. Round to nearest 0.1.
6. Apply AM Stage-Context Adjustment if the compressed score sits outside the expected range for the client's stage and month number.

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

The report is a single, self-contained HTML file. The following technical rules are non-negotiable.

### 6.1. File Structure

The file must be a complete, valid HTML5 document. All CSS is written in a `<style>` block in the `<head>`. No external CSS or JavaScript files are referenced. No CDN dependencies. The file must render correctly when opened directly in a browser from the local filesystem (i.e., `file://` protocol). The only exception is the Google Fonts import and the Instagram embed script, both of which require internet access.

### 6.2. Favicon

The favicon is embedded as an inline base64 SVG data URI in the `<head>`:

```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiI+CiAgPHJlY3Qgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiByeD0iNCIgZmlsbD0iIzBjMzM4NyIvPgogIDx0ZXh0IHg9IjE2IiB5PSIyMiIgZm9udC1mYW1pbHk9Ikdlb3JnaWEsIHNlcmlmIiBmb250LXNpemU9IjE2IiBmb250LXdlaWdodD0iYm9sZCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0id2hpdGUiPnNtPC90ZXh0Pgo8L3N2Zz4K">
```

The favicon SVG is a navy (`#0c3387`) rounded square with white "sm" text. Do not use an SVG favicon that contains embedded raster images via `xlink:href` — Chrome will silently drop these and fall back to the gray globe icon.

### 6.3. CSS Variables

The following CSS variables must be defined in `:root` and used consistently throughout:

```css
:root {
  --shadow: #151516;
  --azure: #0c3387;
  --hl: #e2ed7a;
  --ink-mid: rgba(255,255,255,.65);
  --ink-light: rgba(255,255,255,.35);
  --porcelain: #f2f3f4;
  --ghost: #fafdff;
  --border: rgba(21,21,22,.08);
  --text: #151516;
  --text-muted: #5a5a5c;
  --green: #10b981;
  --amber: #f59e0b;
  --red: #ef4444;
  --purple: #7c3aed;
  --tofu: #0c3387;
  --mofu: #7c3aed;
  --bofu: #10b981;
}
```

### 6.4. Typography

The report uses **Source Sans 3** from Google Fonts:

```html
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
```

Body font: `font-family: 'Source Sans 3', sans-serif`. Font smoothing: `-webkit-font-smoothing: antialiased`.

### 6.5. Layout & Spacing

The `.wrap` container has `max-width: 1100px`, `margin: 0 auto`, and `padding: 0 1.5rem`.

The `.main-content` class adds `padding-top: 2rem; padding-bottom: 2rem` to the main content wrapper.

All standard sections use the `.sec` class:
```css
.sec { margin-top: 2rem; margin-bottom: 2rem; background: #fff; border-radius: 12px; border: 1px solid var(--border); padding: 2.5rem 2.5rem 2.5rem; }
@media(max-width:900px) { .sec { padding: 2rem 2rem; } }
@media(max-width:600px) { .sec { padding: 1.5rem 1.25rem; } }
```

The CTA section is a full-width dark section and does NOT use the `.sec` class. It uses `.cta-section` with `background: #0f172a; padding: 3.5rem 2rem`.

### 6.6. Score Trend Section

The score trend section is a dark-background card inside the score card. Key rules:

- Background: `#111112` (near-black)
- The `.score-trend-section` must have `padding: 2.5rem 1.5rem 1rem` (2.5rem top is required for the label to have breathing room)
- The `.score-card` parent must NOT have `overflow: hidden` — this clips the tops of the bars
- The `.trend-bar-wrap` background must be `transparent` — a semi-transparent background creates a dark cap artifact above the bars
- The `score-trend-delta` div must appear exactly once, inside the `.score-card` div, immediately after the `.score-trend-section`. A duplicate is a known bug — do not introduce it.

### 6.7. Responsive Breakpoints

Three breakpoints are required:

| Breakpoint | Behavior |
|---|---|
| `max-width: 900px` (tablet) | All metric grids collapse to 2 columns. `.sec` padding reduces to 2rem. `.adj-grid` collapses to 1 column. `.goals-grid` collapses to 1 column. |
| `max-width: 768px` | `.cta-funnel-grid` collapses to 1 column. |
| `max-width: 600px` (mobile) | All metric grids collapse to 1 column. MOFU grid explicitly overridden to 1 column. `.sec` padding reduces to 1.5rem 1.25rem. Score trend bars reduce in size. `.goals-grid` gap reduces to 1rem. `.goal-card` padding reduces to 1.25rem. |
| `max-width: 480px` | Score trend bar wraps reduce further: `width: 28px; height: 60px`. |

### 6.8. Print Styles

A `@media print` block must be included:

```css
@media print {
  .hero { background: #0c3387 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .score-trend-section { background: #111112 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .footer { background: #151516 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .wrap { max-width: 100%; }
  .metric-grid { grid-template-columns: repeat(2,1fr) !important; }
  .insights-grid { grid-template-columns: repeat(2,1fr) !important; }
}
```

### 6.9. Footer

The footer (`<footer class="footer">`) must include:
- Scroll Media logo (same linked image as the hero, with `filter: brightness(0) invert(1)` and `opacity: .6`)
- "Prepared by [Scroll Media link] — [Month] [Year] Performance Report"
- "Data sources: Metricool, Instagram Insights · Scoring: Scroll Media Weighted Performance Framework v2.0"
- Footer background: `#151516`

---

## 7. Deployment Process

### 7.1. Repository Structure

The GitHub repository is `cgianattasio15/scroll-reports`. The site is hosted at `reports.scrollmedia.co` via Netlify (DNS points to the repo). The file path for each report follows this pattern:

```
[client-slug]/[monthyear]/index.html
```

Examples:
- `shoplaunchparty/february2026/index.html`
- `laneandkate/february2026/index.html`
- `skinbybrownleeandco/february2026/index.html`
- `measactive/february2026/index.html`
- `upandrunningoh/february2026/index.html`

### 7.2. Client Slugs

| Client | Slug |
|---|---|
| Launch Party | `shoplaunchparty` |
| Lane & Kate | `laneandkate` |
| Skin by Brownlee & Co | `skinbybrownleeandco` |
| MEAS Active | `measactive` |
| Up & Running OH | `upandrunningoh` |

### 7.3. Deployment Steps

The preferred deployment method is via `git` directly in the sandbox, not the GitHub API. The repo is cloned at `/home/ubuntu/scroll-reports-repo`.

1. **Build the report HTML** and save it to the correct path in the local repo: `/home/ubuntu/scroll-reports-repo/[client-slug]/[monthyear]/index.html`

2. **Commit and push:**
```bash
cd /home/ubuntu/scroll-reports-repo
git add [client-slug]/[monthyear]/index.html
git commit -m "Deploy [Client] [Month] [Year] report"
git push origin main
```

3. **Verify live.** After pushing, wait 15–30 seconds for Netlify to deploy, then visit the live URL and confirm:
   - The favicon is rendering (not a gray globe)
   - The score trend section has proper padding
   - No horizontal overflow at mobile viewport
   - All 9 sections render correctly in the correct order

### 7.4. Dashboard & Archive Update Process (new in v6.4)

After all individual reports are deployed and verified live, the main dashboard and each client's archive page must be updated. **This step is required after every monthly report cycle.** Skipping it leaves the dashboard and archive pages showing stale scores.

**Files to update:**

| File | Purpose |
|---|---|
| `/home/ubuntu/scroll-reports-repo/index.html` | Main dashboard at `reports.scrollmedia.co` — shows all active clients |
| `/home/ubuntu/scroll-reports-repo/[client-slug]/index.html` | Client archive page — shows all reports for that client |

**Step 1: Update the main dashboard (`index.html`)**

For each client, locate their client card in the dashboard and update:
- The **score value** displayed on the card (e.g., `8.3` → `7.7`)
- The **score label** if the interpretation tier changed (e.g., "Solid Month" → "Building Month")
- The **report link** if a new month's report was added (update the "View Report" `href` to the new month's URL)
- The **"Latest Report" month label** if displayed

The dashboard score must exactly match the score in the deployed report. Mismatches are a QA error.

**Step 2: Update each client's archive page (`[client-slug]/index.html`)**

For each client, the archive page lists all historical reports as cards. When a new report is deployed:

1. **Add a new report card** for the current month at the top of the report list. Each card must include:
   - Month and year label
   - Score badge (the numerical score)
   - Score interpretation label (e.g., "Building Month")
   - A link to the live report URL

2. **Verify all existing report cards** have correct scores. The archive is the historical record — all scores must match the scores in the deployed reports. If a score was corrected in a deployed report, update the archive card to match.

**Step 3: Commit and push all dashboard and archive changes together**

```bash
cd /home/ubuntu/scroll-reports-repo
git add index.html [client-slug-1]/index.html [client-slug-2]/index.html ...
git commit -m "Update dashboard and archive pages — [Month] [Year] scores"
git push origin main
```

**Step 4: Verify live.** After pushing, visit `reports.scrollmedia.co` and each client's archive URL to confirm the scores are correct and the new report card links to the correct live report.

### 7.5. GitHub API Alternative

If the git CLI is unavailable, use the GitHub API with a Personal Access Token (PAT):

1. **Get the file SHA:** `GET https://api.github.com/repos/cgianattasio15/scroll-reports/contents/[path]`
2. **Push the file:** `PUT https://api.github.com/repos/cgianattasio15/scroll-reports/contents/[path]` with base64-encoded content and the current SHA.
3. **Revoke the PAT** after deployment is confirmed.

---

## 8. QA Checklist

Before marking any report as complete, it must pass both the automated and manual QA checks.

### 8.1. Automated QA Script

Run the `qa_audit.py` script from the sandbox:
```bash
cd /home/ubuntu && python3 qa_audit.py
```

The script checks all 5 active client reports and flags:
- HTML structural validity (unclosed tags, mismatched divs)
- Presence of all 9 required sections in the correct order
- Presence of the Score Trend chart
- Correctness of score badge counts vs. actual metric statuses
- Structural integrity of the Business Goals grid (3 cards)
- Structural integrity of the Strategy Adjustments grid (3 cards, new format)
- Badge/bar color consistency (`.mc-badge` class must match `.bar-fill` class)
- Presence of the Instagram embed script
- Presence of the viewport meta tag

Any `ISSUES` reported by the script must be fixed before proceeding to the visual audit.

### 8.2. Manual Visual Audit Checklist

After the automated check passes, perform a visual audit of each report in a live browser.

**Content QA:**
- [ ] Score is calculated using the official Scoring Framework (v2.0)
- [ ] All 12 metrics are present and correctly assigned to their funnel stage
- [ ] MoM deltas are accurate (current month vs. prior month)
- [ ] Score trend bar chart shows 3–4 months of history with correct values
- [ ] Score badge counts (Exceeding / On Track / Watch) match the actual metric statuses
- [ ] Business Goals section has all 3 goals with correct funnel stage, KPI, status badge, and next-month focus action
- [ ] Top 3 posts have stats and "Why It Worked" copy
- [ ] All 4 insight cards are specific and data-backed (no generic statements)
- [ ] CTA section appears before Strategy Adjustments
- [ ] Strategy Adjustments has exactly 3 cards in the new format (numbered circle, badge, headline, Why, What This Moves)
- [ ] Narrative tone is positive and action-oriented throughout — no apologies, no hedging
- [ ] Client name, handle, AM name, stage, and month are all correct
- [ ] Niche and subniche values match the Master Client Roster (not copied from a prior report)
- [ ] Hero does NOT contain a score number or score narrative paragraph

**Technical QA:**
- [ ] Favicon renders as the "sm" logo (not a gray globe) — verify in an incognito window
- [ ] No horizontal overflow at 390px mobile viewport
- [ ] Score trend label ("SCORE TREND") has proper top padding inside the dark container
- [ ] Performance Dashboard section has proper top spacing (no tight flush against score card)
- [ ] All external links include `target="_blank" rel="noopener"`
- [ ] Progress bars animate on page load
- [ ] Badge color and bar fill color match on every metric card
- [ ] CTA section renders as a dark full-width section
- [ ] Strategy Adjustments renders as a 3-column grid at desktop, 1 column at mobile
- [ ] Business Goals top border colors match the goal status (green = Exceeding, navy = On Track, amber = Building, red = Watch)
- [ ] Top 3 Posts section uses single-column layout (`grid-template-columns: 1fr`, max-width 580px centered)
- [ ] Each post card has `overflow: visible` (not `overflow: hidden`)
- [ ] Each Instagram embed is wrapped in a `<div class="post-embed">` container
- [ ] All Instagram embeds load correctly in a live browser — if an embed fails on a public, non-collaborative post, verify the post ID character-by-character for case-sensitivity errors before applying the fallback protocol
- [ ] Report renders correctly at 1440px desktop, 768px tablet, and 390px mobile
- [ ] File is a single, self-contained HTML document

**Post-Deployment QA (dashboard & archive):**
- [ ] Main dashboard score for this client matches the deployed report score
- [ ] Client archive page has a new card for this month with the correct score and link
- [ ] All archive card scores match the scores in the deployed reports (no stale values)

---

## 9. Copy & Tone Standards

The following rules apply to all copy written for the report. They are consistent with the Scroll Media Copywriting Guidelines.

**Always lead with the strongest signal.** The narrative paragraph, the insight cards, and the goal cards should all open with the most important thing — not a preamble.

**Be specific, not general.** "Saves jumped from 23 to 63, a 174% increase" is good. "Engagement was strong" is not. Every claim must be backed by a specific number or observation.

**Positive and action-oriented, always.** Even in a low-scoring month, the report must feel like a confident strategic partner, not an apology. Frame challenges as "building toward" or "normalizing from" — never as failures. Every challenge must be paired with a specific action.

**No internal framework language.** Do not write "Tier 1 metrics," "IVP," "TOFU," or any internal terminology in client-facing copy. Write what it means in plain English. (Exception: funnel stage labels in the Business Goals section are acceptable as they are visually presented as context, not as jargon.)

**No hype.** No exclamation points. No "amazing," "incredible," "we're thrilled." Let the data speak. The report's authority comes from specificity, not enthusiasm.

---

## 10. Starting a New Report: Copy-Paste Prompts

### Prompt 4: Full Batch Build (All Active Clients — Monthly Default)

**This is the default prompt for monthly reporting.** Use this at the start of each new month to build all active client reports in a single task.

```
I need the [Month] [Year] performance reports for all active clients.

Please read the Scroll Media Monthly Performance Reporting Process v6.4 from the project files before starting. Follow it exactly.

ACCOUNT HOMEBASE LINKS:
- [Client 1]: [Google Sheets link]
- [Client 2]: [Google Sheets link]
- [Client 3]: [Google Sheets link]
- [Client 4]: [Google Sheets link]
- [Client 5]: [Google Sheets link]

METRICOOL CSV EXPORTS (Google Drive links — 2 files per client per month):
[Client 1] [Month]: [link 1], [link 2]
[Client 1] [Prior Month]: [link 1], [link 2]
[Client 2] [Month]: [link 1], [link 2]
[Client 2] [Prior Month]: [link 1], [link 2]
... (repeat for all clients)

IG INSIGHTS SHEET: [Google Sheets link]
SCORE HISTORY SHEET: [Google Sheets link]

For each client:
- Pull all metrics from the Account Homebase (Tab 05) and IG Insights sheet
- Pull top 3 posts from Tab 6 (Content Archive) of the Account Homebase
- Pull score trend history from the Score History sheet
- Do not ask me to provide any metric values, post data, or scores manually

Once all reports are built:
1. Deploy all reports to reports.scrollmedia.co (replace any existing [Month] [Year] reports)
2. Update all client archive pages with the new report card and correct scores
3. Update the main dashboard with new scores and report links
4. Run the qa_audit.py script and fix any issues before confirming
5. Confirm all live URLs
```

### Prompt 1: Full Report Build (New Month) — Single Client

```
I need to build the [Month] [Year] performance report for [Client Name].

Please read the Scroll Media Monthly Performance Reporting Process v6.4 from the project files before starting. Follow it exactly.

DATA SOURCES:
1. Account Homebase: [Google Sheets link]
2. Metricool CSV — [Month] [Year]: [Google Drive link 1], [Google Drive link 2]
3. Metricool CSV — [Prior Month] [Year]: [Google Drive link 1], [Google Drive link 2]
4. IG Insights Sheet: [Google Sheets link]
5. Score History Sheet: [Google Sheets link]

Pull all metrics from the Account Homebase (Tab 05) and IG Insights sheet.
Pull top 3 posts from Tab 6 (Content Archive) of the Account Homebase.
Pull score trend history from the Score History sheet.
Do not ask me to provide any metric values, post data, or scores manually.

Once built:
1. Deploy to reports.scrollmedia.co at [client-slug]/[monthyear]/index.html
2. Update the client's archive page with the new report card
3. Update the main dashboard score for this client
4. Run the qa_audit.py script, fix any issues, and confirm the live URL
```

### Prompt 2: Update an Existing Report (Revisions)

```
I need to update the [Client Name] [Month] [Year] performance report.

The live URL is: https://reports.scrollmedia.co/[client-slug]/[monthyear]/

Changes needed:
1. [Describe change 1]
2. [Describe change 2]
3. [Describe change 3]

The report HTML is at /home/ubuntu/scroll-reports-repo/[client-slug]/[monthyear]/index.html. Make the changes, push to GitHub, and confirm the updated live URL.

If the score changes, also update the client's archive page and the main dashboard to reflect the new score.
```

### Prompt 3: Roll Out a Template Change to All Active Reports

```
I need to apply the following change to all 5 active [Month] [Year] reports:

Change: [Describe the change]

Reports to update:
- https://reports.scrollmedia.co/shoplaunchparty/[monthyear]/
- https://reports.scrollmedia.co/laneandkate/[monthyear]/
- https://reports.scrollmedia.co/skinbybrownleeandco/[monthyear]/
- https://reports.scrollmedia.co/measactive/[monthyear]/
- https://reports.scrollmedia.co/upandrunningoh/[monthyear]/

The report files are at /home/ubuntu/scroll-reports-repo/[client-slug]/[monthyear]/index.html. Apply the change to all 5, push all to GitHub, and confirm all 5 live URLs are updated.
```

---

## 11. Version History

| Version | Date | Changes |
|---|---|---|
| v6.4 | Mar 6, 2026 | Codified single-column Top 3 Posts layout (`grid-template-columns: 1fr`, max-width 580px, centered). Codified `.post-embed` wrapper structure and `overflow: visible` requirement on `.post-card`. Added Dashboard & Archive Update Process as a required post-deployment step (Section 7.4). Added Instagram Permalink Case-Sensitivity Protocol with diagnostic steps (Section 5). Added metadata accuracy rule — niche/subniche/stage must always be pulled from the Master Client Roster, never copied from prior reports. Updated QA checklist with post-deployment dashboard/archive checks and embed case-sensitivity check. Updated all prompts to reference v6.4 and include dashboard/archive update steps. |
| v6.3 | Mar 3, 2026 | Full rewrite. Rebuilt Strategy Adjustments section spec (new 3-card format with numbered circle, badge, headline, Why block, What This Moves block). Moved CTA Strategy before Strategy Adjustments and documented full CTA section spec. Standardized Business Goals formatting (top border, funnel dot, status badge, KPI block, Mar Focus). Added embed fallback protocol. Formalized two-step QA process (automated script + manual visual audit). Updated all prompts to reference v6.3. |
| v6.2 | Mar 2, 2026 | Added Prompt 4 (batch build for all clients). Clarified data source hierarchy (Homebase > IG Insights > Metricool). Top 3 posts now auto-sourced from Tab 6 (Content Archive). Score history now auto-sourced from Score History sheet. Added 5-stat Reel grid spec. Added hero text rule (no score narrative in hero). Added outlier post handling rule. |
| v6.1 | Mar 2, 2026 | Updated data input workflow. Replaced manual metric entry with Metricool CSV + IG Insights Google Sheet as the two data sources. Added CTR and PCR calculation formulas. Revised Prompt 1 to require only 4 file attachments instead of 24 manual metric fields. |
| v6.0 | Mar 2, 2026 | Full rewrite. Added Business Goals section spec, Niche/Subniche badge spec, complete HTML technical standards, deployment script guidance, full QA checklist, and 3 copy-paste prompts. Reflects all design decisions from January 2026 report build cycle. |
| v5.2 | Feb 27, 2026 | Added Score Trend section with relative scaling spec. Removed AM-specific callout. Removed accordion from Performance Dashboard. |
| v5.1 | Feb 27, 2026 | Added strategic framing guidance for adjustments, bullet formatting spec, and automated archive/dashboard update workflow. |
| v5.0 | Feb 27, 2026 | Major structural and content update. Funnel-based dashboard, simplified insights, homebase-aligned strategy section, animated progress bars, PAT deployment. |
| v4.3 | Initial | Original version of this document. |

---

**END OF DOCUMENT**

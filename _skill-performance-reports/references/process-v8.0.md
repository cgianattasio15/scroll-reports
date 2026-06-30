# Performance Report — Process Spec v8.0

**Supersedes:** process-v7.0.md (retained as the carried-section reference for unchanged mechanics).
**Effective:** June 2026 reporting cycle (built first week of July 2026).
**Plan of record:** `00_Strategic_Plan/performance_reporting_improvements_plan_v1.md` (§3 the eight changes, §7 outlier dissection, §12 scoring alignment, §13 voice canon, §14 SBBL learnings).
**Scoring:** Unified Scoring Framework v1.3 (denominator 13.25; Saves + CTR T1-High at 2.0×; 6.0 floor; compression `Final = 6.0 + ((Raw + MoM credit) × 0.4)`).

---

## What changed from v7.0 → v8.0

v8 does not replace the v7.5 report, it extends it. Every carried v7.5 section stays; eight monthly changes plus the All Posts table are layered in. The scoring math, data pull, validation, outlier engine, deploy, email, and logging steps are **unchanged** from process-v7.0.md and are not re-documented here. Read v7.0 for those. This spec documents the v8 build architecture.

The May 2026 reports already shipped two v8 Tier 1 elements (the methodology one-liner and the 10 metric callouts). v8 keeps those and adds the rest.

---

## The v8 10-section IA (build order)

Clone `_skill-performance-reports/templates/canonical-template-v8.html` (token-based) and fill it. `build_v8_report.py` fills the template from a token map and reports unfilled tokens; `v8-worked-example.html` is the rendered reference.

### 0. Loom walkthrough layer (Change 7)
Embed band above the hero. Paste the Loom share id into `data-loom-id` on `#loom-embed`; the band auto-activates. If empty, it renders nothing (no broken player, no placeholder). The AM records a 3–5 min walkthrough: 30s score + headline outcome, 60s Goal Tracker, 90s top post + why it worked, 60s next month's focus. Anti-meta-narration QA per voice canon Rule 3 (no "wanted to share," "real reason for the recording").

### 1. Hero + paired block (Change 1) + methodology one-liner (Change 5)
- **Left panel:** composite score (large), score label, MoM delta, status badge counts (Exceeding / On Track / Watch).
- **Right panel:** the client-specific headline business outcome. The metric is locked per client at strategy build (Workstream A). Examples: a consultation business = link taps; a deli = catering inquiry DMs + link taps; a product brand = shop link taps or quiz completions. Big number + label + one-line sub.
- **Summary line:** one plain-English sentence, "Here's what [Month] means for [Client]: ..." Chase fills per report.
- **Methodology one-liner:** locked copy from `v8_callout_library_v1.md`, renders directly under the paired block. Same line every report. (No em-dash; the locked version is two sentences.)

### 2. Score Card + quarterly snapshot (Change 6)
- Carried: score number + label + delta + badge counts + score trend bars.
- **Quarterly snapshot block:** trailing-3-month score sparkline + 3-month average + trajectory label + one-line narrative. Trajectory labels: Strong, Steady, Building, Recovering, Soft, Mixed. Pick the label and narrative from the 3-month deltas (e.g., current month highest of three AND 3-mo avg ≥0.4 above the prior 3-mo avg → Strong/Pattern A).
  - **Skip rule:** SKIP the block in QBR months (Mar / Jun / Sep / Dec) from **September 2026 onward**, when the QBR artifact owns the snapshot.
  - **2026 exception:** the QBR artifact does not ship until Aug 31, 2026, so **surface the block for June 2026 reports** (treat June as a non-QBR month this once). From September 2026 the normal skip applies.
- **Dip-month locked line:** add class `active` to `#dip-line` when the score drops >0.5 from the prior month. Frame: expected volatility, strategy holds, decision at quarter-close.

### 3. Goal Tracker (Change 2)
Replaces the v7.5 "Funnel Health Check / % of metrics on track." Three rows, one per funnel stage. Each row: descriptive customer-readable goal title, baseline → current → target, lime progress bar with %, 3-month trend sparkline, one-line narrative. Quantified data from the **Goals Quantification Pass** (Workstream A, ~60–90 min/client; lands at `06_Clients/[client]/goals_v1.md`). Goal titles are plain English ("Drive qualified consultation bookings"), never internal jargon.

### 4. Performance Breakdown
Carried v7.5: followers banner + 3 funnel groups + 10 metric cards (TOFU: New Followers, Shares, Views · MOFU: Profile Visits, Retention, Saves, Comments · BOFU: CTR, Link Taps, PCR). Each card carries the locked buyer-translation callout (Change 3, `v8_callout_library_v1.md`): swap `[X]` for the month's movement (MoM % for counts, the rate value for Retention/CTR/PCR); flip "up→down" and "more→fewer" on a down month, the significance line stays.
- **Conditional Watch Time (Tier 1.5):** the Retention card carries a hidden `.mc-watchtime` append. Add class `active` only when avg watch time is meaningful and worth surfacing per client.

### 5. Lead Signal (Change 4)
New section after the dashboard. Opens with the locked 3-sentence "How we measure leads in organic" POV block (Lane B, Measured register). Then a 3-layer attribution stack with **graceful degradation**:
- **Layer 1 — Direct interest signals (always populates):** Saves + Shares + Profile Visits totals.
- **Layer 2 — Conversion path taps:** Link Taps + CTR via UTM-tracked links. If the client has no UTM data, render the empty-state soft prompt ("UTM tracking rolls out this quarter. We'll surface the data here as soon as the links are tagged.") and add class `empty`.
- **Layer 3 — Self-reported attribution (HDYHAU):** survey responses from the client's intake form. Default state is the empty soft prompt ("Adding the 'How did you hear about us?' question to your intake form? We'll fold the responses in here."). Populate with an `.ls-stats` block when the client has HDYHAU data.
Render only the layers that have data; empty layers show the soft prompt, never blank space. Codifies Locked Principle 3.6 (soft-ROI delivery model) in client-facing language.

### 6. Top 3 Posts
Unchanged from v7.5. Outlier-engine selection + standout metrics + Why It Worked + IG link button.

### 7. All Posts This Month (Change 9)
New section after Top 3 Posts. Sortable, filterable table of every published post.
- **Columns:** Date · Format · Caption (60-char preview, expands on hover) · Views · Saves · Shares · Comments · Retention (`—` for non-video) · Link Taps (`—` where none) · CTR (`—` where unmeasurable) · IG link.
- **Interactions:** click any header to sort (toggle asc/desc); format filter chips (All / Reels / Carousels / Static / Stories); hover expands the caption; below 640px the table collapses to stacked cards with a dropdown sort.
- **Outlier highlighting:** rows over-indexing on Saves or CTR (the T1-High signals) at ≥1.5× the account month average get a lime left-edge. Same threshold and floors as the Top Posts outlier engine.
- **Data:** pulled by `all_posts_data.py --client [slug] --month M --year Y --inject [report path]` (extends the outlier engine; no outlier threshold). Rendered **statically** into the `ALL_POSTS` array at build time. NO runtime API calls. Thumbnails deferred to v8.1 (August).
- Add the client's Metricool blog id to `outlier_engine.CLIENT_BLOG_IDS` if it is not already there.

### 8. This Month's Tests + Posts We're Watching (Change 8)
Replaces the v7.5 "Strategy Forward / Doubling Down · Fixing · Testing Next."
- **1–2 Top Performer Patterns:** pattern-level observations from the month's overperformer data ("POV-format Reels hit the T1-High thresholds two months running. Doubling down in [month].").
- **1–2 Posts We're Watching:** one client-facing line per underperforming post with a hypothesis ("This format dipped. Testing X in [month]."). NO deep public dissection of failures (Locked Principle 3.6).
- **2–3 Tactical Tests:** what we test next month inside the locked quarterly strategy. Tactical iteration, not strategy changes.
- **Dip-month narrative block:** when the score drops >0.5 MoM, add class `active` to `#dip-narr`. Three elements: what drove the dip, why we're not changing strategy this month, what we watch at quarter-close.

### 9. Next Month CTAs · Previous Reports · Footer
Unchanged from v7.5. 1 primary CTA + 3 funnel-stage CTAs; prior-month cards; footer carries v1.3 framework attribution.

---

## First-report handling

A client's first-ever monthly report (e.g., Carl's Deli June 2026) has no prior month. Drop MoM deltas (or mark "first month"), show a single-bar score trend, omit the quarterly snapshot block (no 3-month trail), and use single-point or omitted goal sparklines. Create the archive page (clone the Lane & Kate pattern) with the inaugural month as the only card, and add the client's card to the main dashboard.

---

## Pre-deploy validation (v8 gates, in addition to v7.0 gates)

1. **5-breakpoint mobile audit** (1440 / 1100 / 768 / 414 / 375px): paired hero stacks; All Posts table collapses to cards below 640px and the sort becomes a dropdown; Loom embed scales; no horizontal overflow; all touch targets ≥44px (filter chips included); no body text under 14px.
2. **All Posts table:** renders statically (no runtime API calls); outlier highlighting matches the Top Posts outlier engine; null fields show `—`; 1-post and 25+-post sets both render.
3. **Graceful degradation:** Lead Signal renders correctly with Layer 1 only, Layer 1+2, Layer 1+3, and all three; quarterly snapshot renders each trajectory pattern.
4. **Voice canon QA** on all new locked copy and per-client narrative: read-aloud test, zero em-dashes in prose, no banned phrases, no AI-isms, no hedging, sentence case, no internal jargon. (Inside the All Posts JS, `&mdash;` is the null-cell placeholder only.)
5. **Token completeness:** `build_v8_report.py` reports zero unfilled `{{TOKENS}}`.
6. **Security:** report carries `noindex, nofollow` meta (Tier 3 client-data, CLAUDE.md §5).

---

## Tooling

- `templates/canonical-template-v8.html` — token template (clone source).
- `scripts/build_v8_report.py` — token fill + HTML-blob builders (trend bars, sparklines, top-post cards, prev-report cards) + token-completeness check.
- `scripts/all_posts_data.py` — All Posts pull + outlier flagging + static `ALL_POSTS` injection.
- `scripts/outlier_engine.py` — Top Posts selection (unchanged).
- `v8_callout_library_v1.md` — locked methodology one-liner + 10 metric callouts.

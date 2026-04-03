---
name: performance-reports
description: Build, deploy, and maintain Scroll Media monthly client performance reports. Use for any task involving creating new reports, updating existing reports, fixing report design or data, updating the reports.scrollmedia.co dashboard, or updating client archive pages. The full process spec (v7.2) is in references/process-v7.0.md — always read it before starting any report task. Scoring uses the Unified Framework v1.2 — saves-first intent hierarchy applies to both monthly account scores and top post outlier engine.
---

# Performance Reports Skill

## Overview

Monthly performance reports are Scroll Media's primary client-facing deliverable. They are single-file HTML documents hosted at `reports.scrollmedia.co` via a GitHub → Netlify pipeline. The repo is cloned at `/home/ubuntu/scroll-reports-repo`.

**Always read `references/process-v7.0.md` (v7.2) before starting any report task.** It is the single source of truth for section specs, HTML/CSS standards, scoring, deployment, QA, and copy tone.

**Canonical design template:** DEFINE Oakley March 2026 (`/home/ubuntu/scroll-reports-repo/defineoakley/march2026/index.html`). All new reports must match this template's design, structure, and UX decisions.

---

## Workflow

### Building a New Report

1. Read `references/process-v7.0.md` (v7.2) in full before writing any HTML.
2. Pull client metadata from the **Master Client Roster** Google Sheet (link in project files). Never copy from a prior report.
3. **Visit the client Account Homebase page** at `https://tools.scrollmedia.co/clients/[client-slug]/` (password: `scrollies`). Extract: active strategy, content priorities, active CTAs, campaign context. This informs all narrative copy.
4. **Master Data Workflow:** The user (Chase) manually inputs the raw performance data into the **Master Performance Data Sheet** (`1VTTbhyoAe0utuNmig4h5760MyjxMJng86elJi7mV98w`). You must pull metrics from this sheet to build the reports. Confirm all fields are populated before building.
5. **Run the Outlier Engine** to identify top posts: `python3 /home/ubuntu/skills/performance-reports/scripts/outlier_engine.py`. This pulls all posts + reels from Metricool for the reporting month, calculates composite outlier scores, and returns 2–4 top posts with standout metrics, captions, retention %, and Why It Worked narratives. Correct blog IDs are in `CLIENT_BLOG_IDS` inside the script — verify they match `pull_march_data.py` before running. See `references/top-post-outlier-framework.md` for the full framework.
6. Pull score history from the **Master Scoring Sheet** (`18r3NzvG09ngVsEYdDWoN5JEUW-yo_mvoAA2rgdTzfy4`). After building the reports, you must populate the new monthly scores back into this sheet.
7. Pull client goals from the **Master Goals Sheet** (Google Sheets, link in project files).
8. Calculate the score using the v7.2 10-metric scoring model (Section 5 of the process doc).
9. Build the HTML in the canonical 10-section order. Save to `/home/ubuntu/scroll-reports-repo/[client-slug]/[monthyear]/index.html`.
10. Deploy, update dashboard and archive, run QA, verify live. See Sections 7 and 8 of the process doc.
11. **Post-Reporting Documentation:** Fill out the **Master Client Performance Feedback Sheet** (`13YmL11vuLX3e_bT51ORjqUSgS7stKRiLJR1rQ7AmVMQ`) documenting the most notable takeaways for each part of the funnel (TOFU, MOFU, BOFU) for each client based on the performance analysis. **Format Rule:** Each cell must start with a **Bold Title** capturing the overall theme, followed by a short summary describing the point. Update any documentation or skills connected to this performance reporting process to capture all latest refinements.

### Updating an Existing Report

1. Read the specific section spec in `references/process-v7.0.md` for the area being changed.
2. Edit the file at `/home/ubuntu/scroll-reports-repo/[client-slug]/[monthyear]/index.html`.
3. If the score changes, also update the client archive page and the main dashboard.
4. Push, verify live.

### Updating the Dashboard or Archive Pages

- **Main dashboard:** `/home/ubuntu/scroll-reports-repo/index.html`
- **Client archive:** `/home/ubuntu/scroll-reports-repo/[client-slug]/index.html`

See Section 7.4 of the process doc for the full field-by-field update instructions.

---

## Critical Rules (Quick Reference)

**Customer-facing metrics (10 total — v7.0):**
- TOFU: New Followers, Shares, Views
- MOFU: Profile Visits, Retention %, Saves, Comments
- BOFU: Link Taps, CTR, PCR
- **Avg Reach/Day and Avg Watch Time are internal only — do NOT show in reports**

**Unified Scoring Framework v1.2 (Monthly Account Score + Outlier Engine — same hierarchy):**
Both the monthly account score and the top post outlier engine use the same intent-weighted metric hierarchy. The core principle: the goal of organic social is to reach the highest-quality audience (buyers), not the widest audience.
- **T1-High (2.0x):** Saves, CTR — highest-intent buyer signals. Saves = bookmarked for future reference (pre-purchase behavior). CTR = strongest BOFU conversion signal.
- **T1 (1.5x):** Retention %, PCR, Link Taps — content depth, profile-to-follower conversion, BOFU action signals.
- **T2 (1.0x):** Profile Visits, Comments, New Followers, Total Views — consideration and community signals, quality-agnostic.
- **T3 (0.75x):** Shares — awareness amplifier, noisy audience quality. Shares indicate content is funny/relatable/useful-for-others, not that the sharer is a buyer. Downgraded from T1.
- **Denominator:** 13.75 (2×2.0 + 4×1.5 + 3×1.0 + 1×0.75)
- **Comments floor:** avg_comments is floored at 1 (Metricool does not track comments — prevents division-by-zero inflation). Comments ratio is capped at 5.0x.
- **Outlier engine weights (mirrors same hierarchy):** Saves 35%, Retention 25%, Views 20%, Comments 10%, Shares 10%. For non-Reels: Saves 50%, Views 25%, Comments 15%, Shares 10%.

**Hero section:** 3 bullet points with bold titles. No paragraph copy. No score numbers. Stage badge required.

**Score Card:** No methodology note. Score trend bars must be chronological (oldest left → newest right).

**Business Goals:** Progress bars only — no individual metric KPI blocks.

**Top Posts of the Month (v7.2 — Outlier Framework):** Dynamic 2–4 posts (minimum 2, maximum 4) selected by the **Outlier Scoring Engine** (`scripts/outlier_engine.py`). See `references/top-post-outlier-framework.md` for the full framework spec. Each card: Rank header → Date → Format tag (pill badge) → Hook (first line of caption) → **Caption with expand/collapse toggle** ("Show more / Show less" for captions > 180 chars) → **2–3 standout metrics specific to that post** (the metrics that made it an outlier, each showing value + multiplier vs. account average; green badge for ≥2.0x, blue for ≥1.5x). Absolute floors apply (Saves ≥4, Shares ≥4). → Per-post Retention % (ONLY shown if it is a standout outlier metric, do not show a default retention row for all Reels) → Why It Worked (data-backed, references the specific standout metrics) → **"View on Instagram →" full-width button** (navy, white text, fully visible without hover). **No Instagram embeds.** The 2–3 standout metrics must be different for each card — do not show the same metrics on every post. Always run the outlier engine to determine which posts are top performers; do not manually select by views alone.

**All target labels:** "Target Range" — never "Lift Target" or "Stage Target."

**TOFU label:** "Awareness & Authority" | **BOFU label:** "Consideration & Conversion"

**CTA section name:** "Next Month's CTAs"

**Strategy Adjustments:** 3 simplified cards — no "Why" block, no "What This Moves" block.

**Previous Reports section:** Required in every report, above the footer.

**Footer:** White background (`#ffffff`), navy logo.

**Logo — hero:** White-on-transparent PNG (`scroll-logo-white.png`), no background box.

**Logo — footer:** Navy-on-transparent PNG (`scroll-logo-navy.png`), no background box.

**Post card overflow:** `.post-card` uses `overflow: hidden` (embeds removed — the overflow:visible workaround is no longer needed).

**Posts grid layout:** 3-column grid (`grid-template-columns: repeat(3, 1fr)`), no max-width constraint, collapsing to 1-column on mobile (`@media(max-width: 900px)`). All post data (hook, stats, retention, learning, button) is preserved in a tighter, cleaner card.

**Per-post Retention % styling:** Purple (MOFU color `#7c3aed`), labeled "Retention" with note "Avg % of reel watched".

**Post type labels — two buckets only (non-negotiable):** All post type labels in the card header badge and the in-card pill must use exactly two values: `Reel` (for all video content) and `Carousel / Image` (for all static graphics, still images, and carousels). Never use "Static Image", "Carousel", "Video", or any other variant. CSS class: `reel-badge` for Reels, `post-badge` for Carousel / Image.

**Post Score badge (required on every top post card):** Each post card header must include a `Post Score: XX/100` badge rendered as a frosted-glass pill (`post-score` CSS class: `font-size:.72rem; font-weight:700; color:#fff; background:rgba(255,255,255,.18); border:1px solid rgba(255,255,255,.35); border-radius:20px; padding:.2rem .65rem; letter-spacing:.04em; margin-left:auto; white-space:nowrap`). Scores are normalized per client: the top post = 100, others scaled proportionally from their raw outlier composite scores. Formula: `round((post_raw_score / max_raw_score) * 100)`. The `post-score` CSS rule must be included in the report stylesheet.

**Why It Worked styling:** Lime-tinted background (`rgba(226,237,122,.06)`), lime border, `▲ Why It Worked` label in `#8a9a2a`.

**Client Homebase (MANDATORY):** Before writing any narrative copy, visit `https://tools.scrollmedia.co/clients/[client-slug]/` (pw: `scrollies`). All hero bullets, goal summaries, strategy adjustments, CTAs, and post insights must be grounded in the client's active strategy from this page.

**Collab Post Rule (CRITICAL):** Metricool excludes any collab post where the client is NOT designated as the main/primary creator in Instagram. These posts will be completely absent from the Metricool API pull and therefore missed by the outlier engine. **Before finalizing the top posts section, cross-reference the engine output against the client's actual IG Insights data for the month.** If a collab post appears in IG Insights with strong performance but is missing from the engine output, include it manually using the IG Insights metrics as the source of truth. **Going forward, all client collab posts must be set up with the client as the main creator in Instagram** to ensure Metricool captures the data correctly.

**Section order (non-negotiable):** Hero → Score Card → Business Goals → Performance Dashboard → Top 3 Posts → What We Learned → Next Month's CTAs → Strategy Adjustments → Previous Reports → Footer

---

## Data Sources

| Source | Used For | Notes |
|---|---|---|
| Master Performance Data Sheet | All 10 customer-facing metrics | ID: `1VTTbhyoAe0utuNmig4h5760MyjxMJng86elJi7mV98w`. Manually populated by user before reporting begins. |
| IG Insights (manual) | New Followers, Profile Visits, Link Taps, Total Followers | Must be entered by team each month — Meta API unreliable |
| Metricool API | Post-level data for Top 3 Posts | Views, Interactions, per-post Retention % per reel. **Known gap: Metricool excludes collab posts where the client is NOT the main creator.** These posts will be missing from the API pull entirely — see Collab Post Rule below. |
| Master Scoring Sheet | Score trend history | ID: `18r3NzvG09ngVsEYdDWoN5JEUW-yo_mvoAA2rgdTzfy4`. Pull history, then write new scores back after building reports. |
| Master Goals Sheet | Client goals (3 per client) | TOFU / MOFU / BOFU — use exact goal language from sheet |
| Master Client Performance Feedback Sheet | TOFU/MOFU/BOFU takeaways | ID: `13YmL11vuLX3e_bT51ORjqUSgS7stKRiLJR1rQ7AmVMQ`. Must be filled out by AI after reports are built. Use Bold Title + short summary format for each cell. |
| Client Account Homebase (`tools.scrollmedia.co/clients/[slug]/`) | Active strategy, CTAs, content priorities | MANDATORY — visit before writing any narrative copy |
| Master Client Roster | Client metadata | Stage, niche, AM, handle, start date |

---

## Client Slugs (Active as of March 2026)

| Client | Slug | Archive URL |
|---|---|---|
| Launch Party | `shoplaunchparty` | `reports.scrollmedia.co/shoplaunchparty/` |
| Lane & Kate | `laneandkate` | `reports.scrollmedia.co/laneandkate/` |
| Skin by Brownlee & Co | `skinbybrownleeandco` | `reports.scrollmedia.co/skinbybrownleeandco/` |
| MEAS Active | `measactive` | `reports.scrollmedia.co/measactive/` |
| Up & Running OH | `upandrunningoh` | `reports.scrollmedia.co/upandrunningoh/` |
| DEFINE Oakley | `defineoakley` | `reports.scrollmedia.co/defineoakley/` |
| Ombre Gallery | `ombregallery` | `reports.scrollmedia.co/ombregallery/` |

---

## Reference Files

- `references/process-v7.0.md` — **Current spec (v7.2).** Full process: section-by-section build guide, HTML/CSS standards, 10-metric scoring framework, deployment steps, QA checklist, copy tone rules, and copy-paste prompts.
- `references/top-post-outlier-framework.md` — **Top Post Outlier Detection Framework (v1.2).** Composite scoring model for identifying genuine outlier content from Metricool API data. Covers metric weights, outlier thresholds, standout metric selection, and Why It Worked narrative logic. Always run `scripts/outlier_engine.py` to generate top posts data before building the Top Posts section.
- `scripts/outlier_engine.py` — **Outlier scoring engine.** Pulls all posts + reels from Metricool for a given client/month, calculates composite outlier scores, selects 2–4 top posts, identifies standout metrics, and returns structured data for report building. Correct blog IDs are hardcoded in the script — verify before running.
- `references/process-v6.4.md` — Previous spec (v6.4). Retained for historical reference only. Do not use for new reports.
- `templates/canonical-template.html` — **Canonical HTML template (DEFINE Oakley March 2026).** Use as the starting point for all new reports. Copied from the live report at `/home/ubuntu/scroll-reports-repo/defineoakley/march2026/index.html`.
- `references/next-month-readiness-checklist.md` — **Month-start checklist.** What Chase must provide (manual inputs) vs. what the agent handles automatically. Includes all file locations, Metricool blog IDs, Google Sheet IDs, and known manual steps.

## QA

A reusable QA script is at `/home/ubuntu/qa_define_final.py`. Run it against any new report by updating the file path at the top. It runs 102 checks across: DOCTYPE/meta, branding, section structure, accessibility, mobile, performance, content accuracy, and links. All checks should pass before deploying. The one known false positive is the `}}` CSS check — all `}}` in reports are valid CSS media query closings, not template artifacts.

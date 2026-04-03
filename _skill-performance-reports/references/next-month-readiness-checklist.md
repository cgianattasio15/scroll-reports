# Scroll Media — Monthly Performance Report: Next-Month Readiness Checklist
**Version:** April 2026 Cycle (v7.2 Process)
**Last Updated:** April 1, 2026

---

## What Chase Needs to Do (Manual Inputs Only)

Before the agent can run the full reporting workflow, Chase must complete the following:

1. **Populate the Master Performance Data Sheet** (`1VTTbhyoAe0utuNmig4h5760MyjxMJng86elJi7mV98w`)
   - Add a new tab for the reporting month (e.g., "April 2026")
   - Enter all 10 customer-facing metrics for each active client
   - **IG Insights fields must be manually entered** (Meta API is unreliable):
     - New Followers
     - Profile Visits
     - Link Taps
     - Total Followers (end of month)
   - Metricool-sourced fields (agent can pull via API if needed):
     - Views, Shares, Saves, Comments, Retention %, CTR, PCR

2. **Confirm the active client roster** — if any clients have been added, paused, or offboarded, note this before the agent starts.

3. **Confirm reporting month** — the agent will default to the most recent completed calendar month.

---

## What the Agent Does (Fully Automated)

Once the Master Data Sheet is populated, the agent handles everything else in this order:

### Phase 1: Data Collection
- [ ] Pull all 10 metrics per client from the Master Performance Data Sheet
- [ ] Pull score history from the Master Scoring Sheet (`18r3NzvG09ngVsEYdDWoN5JEUW-yo_mvoAA2rgdTzfy4`)
- [ ] Pull client goals from the Master Goals Sheet
- [ ] Visit each client's Account Homebase (`tools.scrollmedia.co/clients/[slug]/`, pw: `scrollies`) to extract active strategy, CTAs, and content priorities

### Phase 2: Top Post Outlier Detection
- [ ] Run `python3 /home/ubuntu/skills/performance-reports/scripts/outlier_engine.py` for each client
- [ ] Confirm 2–4 top posts selected per client
- [ ] Verify standout metrics meet floor thresholds (Saves ≥4, Shares ≥4)
- [ ] Confirm Retention % is only flagged as standout if it genuinely over-indexes

### Phase 3: Score Calculation
- [ ] Calculate the 10-metric composite score for each client (v7.2 model, Section 5 of process doc)
- [ ] Calculate MoM delta vs. prior month score
- [ ] Determine score trend direction (up / down / flat)

### Phase 4: Report Building
- [ ] Build HTML report for each client using `templates/canonical-template.html` as the base
- [ ] Follow the 10-section order: Hero → Score Card → Business Goals → Performance Dashboard → Top Posts → What We Learned → Next Month's CTAs → Strategy Adjustments → Previous Reports → Footer
- [ ] Save to `/home/ubuntu/scroll-reports-repo/[client-slug]/[monthyear]/index.html`
- [ ] Verify all section IDs are present (for sticky nav)
- [ ] Verify 3-column top posts grid collapses correctly on mobile

### Phase 5: QA
- [ ] Run QA script (`/home/ubuntu/qa_define_final.py`) against each report
- [ ] All 102 checks should pass (known false positive: `}}` CSS check is valid)
- [ ] Manually verify IG buttons are visible (navy background, white text, no hover-only visibility)
- [ ] Verify no duplicate retention rows (only show when retention is a standout metric)
- [ ] Verify strategy adjustment headlines are specific (not generic "Doubling Down / Testing / Fixing")

### Phase 6: Deployment
- [ ] Push all reports to GitHub (`git add . && git commit -m "Add [Month] 2026 reports" && git push`)
- [ ] Netlify auto-deploys within ~60 seconds
- [ ] Verify all 7 reports are live at `reports.scrollmedia.co/[client-slug]/[monthyear]/`
- [ ] Update main dashboard (`reports.scrollmedia.co/index.html`) with new report cards
- [ ] Update each client archive page with the new month's report card

### Phase 7: Post-Reporting Documentation
- [ ] Update Master Scoring Sheet with new monthly scores for all clients
- [ ] Fill out Master Client Performance Feedback Sheet (`13YmL11vuLX3e_bT51ORjqUSgS7stKRiLJR1rQ7AmVMQ`)
  - Format: **Bold Title** + short summary for each TOFU/MOFU/BOFU cell
- [ ] Update skill documentation if any new process refinements were discovered

---

## Key File Locations

| Asset | Location |
|---|---|
| Skill documentation | `/home/ubuntu/skills/performance-reports/SKILL.md` |
| Process spec (v7.2) | `/home/ubuntu/skills/performance-reports/references/process-v7.0.md` |
| Outlier framework | `/home/ubuntu/skills/performance-reports/references/top-post-outlier-framework.md` |
| Outlier engine script | `/home/ubuntu/skills/performance-reports/scripts/outlier_engine.py` |
| Canonical HTML template | `/home/ubuntu/skills/performance-reports/templates/canonical-template.html` |
| QA script | `/home/ubuntu/qa_define_final.py` |
| Report repo | `/home/ubuntu/scroll-reports-repo/` |
| March 2026 canonical report | `/home/ubuntu/scroll-reports-repo/defineoakley/march2026/index.html` |

---

## Metricool Blog IDs (Active as of March 2026)

| Client | Slug | Blog ID |
|---|---|---|
| DEFINE Oakley | `defineoakley` | 5321970 |
| Lane & Kate | `laneandkate` | 5321978 |
| Launch Party | `shoplaunchparty` | 5321935 |
| MEAS Active | `measactive` | 5321975 |
| Ombre Gallery | `ombregallery` | 5321966 |
| Skin by Brownlee | `skinbybrownleeandco` | 5408849 |
| Up & Running | `upandrunningoh` | 5506230 |

---

## Google Sheet IDs

| Sheet | ID |
|---|---|
| Master Performance Data Sheet | `1VTTbhyoAe0utuNmig4h5760MyjxMJng86elJi7mV98w` |
| Master Scoring Sheet | `18r3NzvG09ngVsEYdDWoN5JEUW-yo_mvoAA2rgdTzfy4` |
| Master Client Performance Feedback Sheet | `13YmL11vuLX3e_bT51ORjqUSgS7stKRiLJR1rQ7AmVMQ` |

---

## Known Gaps / Manual Steps Still Required

| Step | Status | Notes |
|---|---|---|
| IG Insights data entry | **Manual (Chase)** | Meta API unreliable; must be entered by team before agent starts |
| Client Homebase narrative context | **Agent visits live** | Agent visits `tools.scrollmedia.co/clients/[slug]/` before writing copy |
| New client onboarding | **Manual setup** | New clients need: Metricool blog ID, slug, goals entered in Master Goals Sheet, Account Homebase page created |
| Post captions / hooks | **Agent pulls from Instagram** | Agent visits live post URLs to pull actual caption text |

---

## What "Bulletproof" Looks Like for Next Month

The process is ready for a fully automated run when:
1. Chase has populated the Master Data Sheet with all 10 metrics per client
2. The agent reads `SKILL.md` → reads `process-v7.0.md` → runs the outlier engine → builds reports → deploys → updates sheets
3. No manual HTML editing or debugging is required
4. All 7 reports are live within a single session

**Current status as of April 1, 2026:** ✅ Ready. All systems are in place. The only required input from Chase is the raw performance data in the Master Data Sheet.

# v8 Callout Library v1

**Version:** 1.0
**Created:** June 2, 2026
**Owner:** Chase. Chase owns report build and paste-in. AMs are awareness-only (they share and present the finished report to the client, they do not build it).
**Status:** Locked copy. Chase pastes into May 2026 reports during the build (ships first week of June). Two Tier 1 v8 changes only.
**Source plan:** `00_Strategic_Plan/performance_reporting_improvements_plan_v1.md` §3 (Change 3 + Change 5), §11, §12, §13
**Voice canon:** `01_Strategy/frameworks/brand_system.md` §3.3 (Lane B Scroll agency voice, Measured register per `scroll_voice_os.md`)

---

## Intent

Two locked copy artifacts for the May 2026 monthly performance reports. These are the ONLY v8 changes shipping in May reports. Full v8 launches with June data reports first week of July.

1. **Methodology one-liner** — pastes under the score number in the hero. Same line every report, every client.
2. **10-metric callout library** — one italicized buyer-translation sentence under each metric card body. Same language family across all 10. Chase swaps the `[X]` placeholder for the actual movement from that month's data during the build.

Both directly attack the three recurring report objections: readability (Objection 1), goal tracking (Objection 2), and business-outcome attribution (Objection 3). The callouts translate raw metric movement into plain-English buyer meaning without overclaiming last-click attribution.

## Voice canon constraints applied

- No em-dashes in prose. Periods, commas, parentheses, or line breaks only.
- No banned phrases, AI-isms, or hedging (full list at `brand_system.md` §3.3). Note: "genuinely" avoided per Pending Decision #10.
- Sentence case in body copy.
- No internal jargon. No TOFU/MOFU/BOFU, no "Tier 1," no framework names. Customer-readable language only.
- Soft-ROI delivery model per CLAUDE.md §5 Locked Principle 3.6. Metrics are framed as buyer signals, never as confirmed sales or last-click conversions.
- Read-aloud test run on every line.

## Usage note (Chase, during report build)

The callout is a single italicized sentence (rendered in italics under each metric card body in the HTML report). Swap `[X]` for the actual percentage from that month's data. For count metrics (Shares, Views, New Followers, Profile Visits, Comments, Saves, Link Taps), `[X]%` is the month-over-month change and the lead reads "up [X]%." For rate metrics (Retention, CTR, Profile Conversion), `[X]%` is the rate value itself and the lead reads "came in at [X]%."

**Down-month swap:** when a count metric drops, flip the lead from "up" to "down" and the translation clause from "more" to "fewer." The significance line (the closing framing) stays the same in both directions. The dip itself gets addressed in the report narrative per Change 8's dip-month discipline, not inside the metric callout.

**AM awareness:** AMs do not build or paste anything. They present the finished report to the client and field questions. They should read these callouts and the methodology one-liner ahead of the recap call so the language is familiar and they can speak to it, but the build and paste-in stay with Chase.

---

## Section 1 — Methodology one-liner (locked, validated)

**Locked copy (voice-canon-compliant):**

> *Your score reflects how this month performed against your stage targets, weighted by what predicts buyer behavior. Monthly score is a snapshot. Strategy decisions are made on quarterly trend, not single-month signal.*

**Change from the plan draft + rationale:**

The plan draft used an em-dash in "Monthly score is a snapshot — strategy decisions are made on quarterly trend." That violates `brand_system.md` §3.3 Rule 1 (no em-dashes in client-facing prose). Fix: replaced the em-dash with a period, splitting into two short sentences. The two-sentence cadence actually reads sharper than the spliced version and lands the snapshot-vs-trend contract with more weight. No other words changed. "Stage targets" preserved as locked because the report already establishes the client's stage elsewhere, so it reads as plain language to the client, not internal jargon.

**Placement:** Directly under the score number in the report hero. Same line every report.

---

## Section 2 — 10-metric callout library

Ordered by funnel position (awareness, then consideration, then conversion). Framing strength tracks metric weight: the strongest buyer language sits on Saves and click-through rate (the highest-intent signals), the lightest on Shares (an amplification signal).

### Awareness signals

**1. Shares** *(lightest framing — amplification signal, not a buyer signal)*

> *Shares up [X]%. Translation: [X]% more people sent your content to someone else. Shares put you in front of new audiences your posts wouldn't reach on their own.*

**2. Total Views** *(reach signal)*

> *Views up [X]%. Translation: your content reached [X]% more screens this month. Views are the widest measure of how many people you got in front of, and everything downstream starts here.*

**3. New Followers** *(discovery converting to audience)*

> *New followers up [X]%. Translation: [X]% more people chose to keep seeing your content after finding you. A new follow is someone deciding you are worth coming back to.*

### Consideration signals

**4. Profile Visits** *(deliberate consideration action)*

> *Profile visits up [X]%. Translation: [X]% more people tapped through to look closer at who you are. A profile visit is a deliberate step toward becoming a customer, not a passive scroll.*

**5. Comments** *(community engagement)*

> *Comments up [X]%. Translation: [X]% more people stopped to start a conversation with you. Comments are public proof that your audience is engaged, and they pull in the people watching from the sidelines.*

**6. Retention %** *(content depth — rate metric)*

> *Retention came in at [X]%. Translation: on average, people watched [X]% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences.*

**7. Saves** *(strongest framing — pre-purchase intent signal)*

> *Saves up [X]%. Translation: [X]% more people bookmarked your posts to act on later. Saves are the strongest signal of a future buyer.*

### Conversion signals

**8. Link Taps** *(direct conversion action)*

> *Link taps up [X]%. Translation: [X]% more people tapped the link in your bio to move toward your site, booking, or offer. A link tap is one of the clearest actions someone takes when they are ready to do business.*

**9. Click-Through Rate** *(strongest framing — conversion efficiency, rate metric)*

> *Click-through rate came in at [X]%. Translation: of everyone who saw your link, [X]% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers.*

**10. Profile Conversion Rate** *(discovery-to-follower conversion — rate metric)*

> *Profile conversion came in at [X]%. Translation: [X]% of the people who visited your profile chose to follow. A strong profile conversion rate means your page is doing its job, turning curious visitors into an audience you can nurture toward buying.*

---

## Validation log

- **Voice canon QA:** Read-aloud test run on all 11 lines (one-liner + 10 callouts). Em-dash audit passed, zero em-dashes in any client-facing line. Banned-phrase, AI-ism, and hedging checks passed. "Genuinely" avoided per Pending Decision #10. Sentence case throughout. No internal jargon (no TOFU/MOFU/BOFU, no tier labels, no framework names).
- **Stage-agnostic check:** Leading every count callout with a percentage swing (not an absolute number) keeps each line correct for a Spark client (small numbers, building) and a Thrive client (large numbers, sustained). Rate-metric callouts lead with the rate value, which is already stage-agnostic. No callout depends on a specific number range.
- **Buyer-intent tier alignment:** Framing strength tracks metric weight. Saves ("strongest signal of a future buyer") and CTR ("moving toward becoming customers") carry the strongest buyer language. Shares carries the lightest ("new audiences," no buyer claim). Consideration and conversion metrics sit in between.
- **Locked Principle 3.6 (soft-ROI) check:** No callout claims a confirmed sale or last-click conversion. Every line frames the metric as a signal of intent or movement ("toward," "predicts," "signal of"), never as attributed revenue.
- **Length consistency:** Every callout is three short sentences (movement, translation, significance). Consistent rhythm across all 10.

**Open flag for Chase:** The `KPI_Target_Ranges_Framework.csv` tier column disagrees with the framing tiers used here for Shares, Comments, and CTR (CSV: Shares=Tier 1, Comments=Tier 3, CTR=Tier 2; framework/brief: Shares=T3, Comments=T2, CTR=T1-High). Framing in this library follows the brief and the Scoring Framework v1.3 lock ("Saves and CTR are T1-High at 2.0×"). Does not affect scoring math. Recommend reconciling the CSV tier column in a later cleanup pass so the resource files agree.

---

## Implementation note (Chase owns the build)

Chase pastes the relevant callout under each metric card body in the HTML report during the build. The `[X]` placeholder gets replaced with the actual percentage movement from that month's data (month-over-month change for count metrics, the rate value for Retention, CTR, and Profile Conversion). For a down month on a count metric, flip "up" to "down" and "more" to "fewer" in the translation clause; the significance line stays the same. The methodology one-liner pastes under the score in the hero, unchanged, on every report. Both ship for May 2026 reports first week of June across 5 reports (Lane & Kate, Up & Running, DEFINE Oakley, Launch Party, MEAS Active).

AMs do not touch the build. Their role is to share the finished report with the client and present it on the recap call. They should review this library beforehand so the callout language is familiar, but ownership of report construction stays with Chase.

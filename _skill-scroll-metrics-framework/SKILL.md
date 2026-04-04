---
name: scroll-metrics-framework
description: Scroll Media's canonical metric tier structure, KPI target ranges, and performance scoring model. Use for any task that involves evaluating client performance, calculating scores, interpreting metrics, assigning growth stages, building the client-facing metrics explainer page, or making strategic recommendations based on Instagram data.
---

# Scroll Media — Metrics & Scoring Framework (v3.0)

**Version:** 3.0 | **Effective:** April 2026  
**Master Document:** `Scroll Media — Master Metrics & Scoring Framework v3.0.md` in project files  
**Canonical KPI Table:** `KPI_Target_Ranges_Framework_v3.0.csv` in project files

---

## The Core Philosophy

The goal of organic social for service-based businesses is to reach the **highest-quality audience (buyers)**, not the widest audience. Every metric in this framework is evaluated through the lens of **buyer intent** — how strongly does this metric signal that the viewer is a potential client?

**The T1 Definition:** T1 metrics share one characteristic — they require the viewer to make a deliberate decision. Saving a post, watching it to completion, tapping a link, or converting from a profile visit are all active choices that signal genuine interest. These are the behaviors that precede a purchase inquiry.

---

## The Intent-Weighted Metric Tiers

| Tier | Weight | Metrics (10 Scored) | Rationale |
|---|---|---|---|
| **T1** | **1.5x** | Saves, Retention %, Link Taps, PCR, CTR | Highest-intent buyer signals. All require a deliberate viewer decision. |
| **T2** | **1.0x** | Profile Visits, New Followers, Total Views, Shares | Growth and distribution signals. Meaningful but quality-agnostic. |
| **T3** | **0.75x** | Comments | Supporting signal. Highly variable by niche and content type. |

**Internal-only (NOT shown in client reports):** Avg Reach/Day, Avg Watch Time

**Denominator:** 13.25 `(5 × 1.5) + (4 × 1.0) + (1 × 0.75)`

---

## The 4 Growth Stages & KPI Target Ranges

| Metric | Tier | Spark | Lift | Rise | Thrive |
|---|---|---|---|---|---|
| New Followers | T2 | 40–90 | 100–270 | 300–2,500 | 750–10,000 |
| Shares | T2 | 15–60 | 60–300 | 200–2,000 | 750–2,500 |
| Total Views | T2 | 10K–40K | 40K–150K | 150K–800K | 650K–3M |
| Profile Visits | T2 | 50–500 | 300–2,000 | 1,500–10,000 | 8,000–40,000 |
| Retention % | T1 | 35%–50% | 50%–65% | 65%–80% | 80%–95% |
| Saves | T1 | 20–80 | 80–400 | 300–2,500 | 950–5,000 |
| Comments | T3 | 15–75 | 75–250 | 250–900 | 900–3,500 |
| Link Taps | T1 | 5–40 | 30–180 | 350–3,000 | 3,000–15,000 |
| CTR | T1 | 3%–8% | 3%–6% | 2%–5% | 1%–4% |
| PCR | T1 | 10%–18% | 10%–16% | 8%–14% | 5%–12% |

**Stage Assignment:**
- **Spark:** < 1,500 followers. Establishing foundation.
- **Lift:** 1,500–8,000 followers. IVP validated, focusing on conversion efficiency.
- **Rise:** 10,000–40,000 followers. Scaling reach while maintaining engagement quality.
- **Thrive:** 50,000+ followers. Authority established, optimizing retention and brand equity.
- Strong or weak engagement quality can override follower count for stage assignment.

---

## Monthly Account Scoring Model

### Status Points
| Status | Condition | T1 (1.5x) | T2 (1.0x) | T3 (0.75x) |
|---|---|---|---|---|
| EXCEEDING | Above high target | 1.5 | 1.0 | 0.75 |
| ON TRACK | Within target range | 0.9 | 0.6 | 0.45 |
| WATCH | Below low target | 0.3 | 0.2 | 0.15 |

### Score Formula
1. Sum all 10 weighted points.
2. **Raw Score:** `(Sum / 13.25) × 10`
3. **MoM Trend Credit:**
   - 8+ metrics improved: +0.5
   - 5–7 improved: +0.25
   - 3–4 improved: 0
   - <3 improved: −0.25
4. **Final Score:** `6.0 + (Raw Score with Credit × 0.4)`
5. Round to nearest 0.1. Minimum score: 5.0.

### Score Interpretation
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
| 5.0–5.9 | Baseline Month |

---

## Top Post Outlier Engine (Quick Reference)

Every post is scored against the account's own monthly average. Top posts are selected by composite outlier score — NOT by views alone.

**Reel weights:** Saves 35%, Retention 25%, Views 20%, Comments 10%, Shares 10%  
**Carousel/Image weights:** Saves 50%, Views 25%, Comments 15%, Shares 10%

A score of 100 = performed at account average. Minimum threshold for top post selection: 80+.

---

## When to Use This Skill

- Calculating or verifying a client's monthly performance score
- Assigning or reviewing a client's growth stage
- Interpreting metric performance against target ranges
- Building or updating the client-facing metrics explainer HTML page
- Making strategic recommendations based on metric data
- Any task where you need to know what a metric tier means or how it's weighted
- Answering client questions about how we measure performance

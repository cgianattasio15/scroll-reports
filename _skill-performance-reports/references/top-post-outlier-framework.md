# Scroll Media: Top Post Outlier Detection Framework (v1.2)

## 1. The Philosophy of Outlier Detection

The goal of organic social media for service-based businesses is not to reach the widest audience — it is to reach the **highest-quality audience**: the people most likely to care about what you're selling and take action toward a purchase.

This means the metrics that matter most are the ones that signal **buyer intent**, not just volume. A post with 3,000 views and 12 saves is more valuable than a post with 10,000 views and 2 saves. Saves indicate the viewer found the content worth returning to — a pre-purchase behavior. Views alone are quality-agnostic.

The Scroll Media Outlier Framework uses a **Composite Weighted Scoring Model** that evaluates every post against the account's own monthly average, identifying posts that over-index on the specific metrics that drive business outcomes. The weighting hierarchy reflects the intent ladder: saves and conversion signals are weighted highest; shares (noisy, audience-quality-agnostic) are weighted lowest.

## 2. The Unified Scoring Hierarchy

Both the monthly account score and the top post outlier engine use the same intent-weighted metric hierarchy.

| Tier | Metrics | Weight | Rationale |
|---|---|---|---|
| T1-High | Saves, CTR | Highest | Saves = bookmarked for future reference (pre-purchase behavior). CTR = strongest BOFU conversion signal. |
| T1 | Retention %, PCR, Link Taps | High | Content depth, profile-to-follower conversion, BOFU action signals. |
| T2 | Profile Visits, Comments, New Followers, Total Views | Medium | Consideration and community signals. Meaningful but quality-agnostic. |
| T3 | Shares | Low | Awareness amplifier. Noisy audience quality. Content gets shared when it's funny, relatable, or useful-for-others — not necessarily when the sharer is a buyer. |

**Why Shares are T3:** High shares can mean the content is funny, relatable, or shareable-for-others — not that the sharer is a buyer. Shares amplify reach but don't guarantee quality audience distribution. Saves are the inverse: they require the viewer to actively decide this content is worth keeping — a much stronger signal of purchase consideration.

## 3. The Composite Scoring Model (Outlier Engine)

Every post published in the reporting month receives an Outlier Score based on its performance against the account's monthly average for that specific format.

### Reel Scoring Formula
```
score = (views / avg_views) * 20
      + (saves / avg_saves) * 35
      + (retention / avg_retention) * 25
      + min(comments / avg_comments, 5.0) * 10
      + (shares / avg_shares) * 10
```

### Carousel / Image Scoring Formula (no retention)
```
score = (views / avg_views) * 25
      + (saves / avg_saves) * 50
      + min(comments / avg_comments, 5.0) * 15
      + (shares / avg_shares) * 10
```

### Score Interpretation
- A score of **100** means the post performed exactly at the account average across all metrics.
- A score of **80+** is the minimum threshold for selection as a top post.
- A score of **150+** indicates a strong performer.
- A score of **200+** is a true **Outlier** (2x+ composite baseline).

### Data Quality Rules
- **Comments floor:** `avg_comments` is floored at 1 (Metricool does not track comments — prevents division-by-zero inflation).
- **Comments cap:** Comments ratio is capped at 5.0x to prevent outlier inflation from milestone posts with unusually high comment counts on accounts with near-zero comment averages.
- **Saves floor (standout display):** Saves must be ≥4 to appear as a standout metric in the post card. A post with "1 save = 5x avg" on an account averaging 0.2 saves per post is not a meaningful signal.
- **Shares floor (standout display):** Shares must be ≥4 to appear as a standout metric.

## 4. Post Selection Rules

1. **Calculate Baseline:** Compute the average Views, Shares, Saves, and Retention for all posts published in the reporting month.
2. **Score All Posts:** Run every post through the Composite Scoring Model.
3. **Rank and Filter:** Sort posts by Outlier Score in descending order.
4. **Dynamic Selection:**
   - Select the top 3 posts by default.
   - If the #4 post has an Outlier Score > 150, include it (max 4 posts).
   - If the #3 post has an Outlier Score < 80, exclude it (min 2 posts).
   - **Always include at least 2 posts regardless of score.**
5. **Cross-reference IG Insights (CRITICAL):** Before finalizing, compare engine output against the client's actual IG Insights data for the month. Metricool excludes collab posts where the client is not the main creator — these will be missing from the engine entirely. If a collab post shows strong IG Insights performance, include it manually using IG Insights as the source of truth.

## 5. Post Score Badge (Normalized 0–100)

Each post card in the report displays a `Post Score: XX/100` badge. This is a **normalized** score — the top post for each client always scores 100, and others are scaled proportionally.

**Formula:** `round((post_raw_score / max_raw_score) * 100)`

This makes the score client-friendly and immediately readable without exposing raw composite numbers.

## 6. Standout Metrics and "Why It Worked" Copy

The engine identifies the specific metrics that drove each post's high score and generates data-backed "Why It Worked" copy.

**Standout metric rules:**
- Flag any metric that performed at ≥1.5x the account average (subject to absolute floor thresholds).
- Show 2–3 standout metrics per card — the specific metrics that drove the outlier score.
- Standout metrics must differ between cards — do not show the same metrics on every post.
- If a post scores in the top 3 but no individual metric clears the floor threshold, show a composite copy: "Scored in the top 3 this month on composite performance. [Metric A] at [Xz] and [Metric B] at [Yz] indicate [insight]. No single metric broke out at scale, but the combination placed it here."

**Why It Worked copy hierarchy:**
- **Saves outlier:** "Driven by save density at Xx the account average. Saves this high indicate viewers found the content worth returning to — a strong indicator of consideration-stage intent and educational value."
- **Retention outlier (Reels):** "Anchored by exceptional retention at Xx the account average. Viewers watched a disproportionate amount of this Reel, signaling the hook delivered on its promise and the pacing held attention throughout."
- **Views outlier:** "A reach outlier at Xx the account's average views. The hook successfully broke content out of the core audience and into the wider algorithm."
- **Shares outlier:** "Driven by share velocity at Xx the account average. High shares indicate the content tapped into a universal emotion or pain point the audience wanted to pass along — the strongest organic amplification signal available."
- **Comments outlier:** "Drove Xx comments at Xx the account average — the highest community response signal of the month. High-emotion or milestone content drives this type of response; it builds trust and signals the brand has an engaged, invested audience."

## 7. Post Type Labels (Non-Negotiable)

All post type labels use exactly two values:
- **Reel** — all video content
- **Carousel / Image** — all static graphics, still images, and carousels

Never use "Static Image", "Carousel", "Video", or any other variant.

## References
[1] Leen Studio. "How to Read Your Instagram Analytics Like a Data Scientist." https://leen.studio/blog/read-instagram-analytics-like-data-scientist
[2] Kallaway. "Sandcastles AI - Viral Outlier Detection." https://www.sandcastles.ai/
[3] Mailchimp. "A Guide to Content Scoring for Smarter Strategies." https://mailchimp.com/resources/content-scoring/

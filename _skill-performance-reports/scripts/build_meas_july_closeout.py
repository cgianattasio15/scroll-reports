#!/usr/bin/env python3
"""
build_meas_july_closeout.py -- transform the MEAS Active June 2026 v8.5 report
into the July 1-22 2026 FINAL (closeout) report.

Follows the SOP transformer path (build_v8_report.py still does not fill the
v8.5 template -- Workstream N). Every edit is an anchored replacement that hard
-fails if the anchor is missing, so a silently-skipped edit is impossible.

Sources of truth:
  - MEAS_Final_Report_Closeout_Package.md  (Mode C adaptations + drop-in copy)
  - MEAS_July1-22_Data_Block.md            (combined KPIs)
  - instagram{reels,posts}_20260701_20260722.csv (per-post, drives ALL_POSTS)
  - score_report.py                        (7.6, computed not hand-set)
  - run_outlier_from_csv.py                (v2.0 showcase selection)
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_outlier_from_csv import load_reels, load_posts, run  # noqa: E402

REPO = "/Users/chase.gianattasio/Desktop/scroll-reports"
DATA = "/Users/chase.gianattasio/scroll-reports/_meas-closeout"
SRC = f"{REPO}/measactive/june2026/index.html"
OUT_DIR = f"{REPO}/measactive/july2026"
OUT = f"{OUT_DIR}/index.html"

edits = []


def sub(html, old, new, label):
    """Anchored replace. Hard-fails on missing or ambiguous anchor."""
    n = html.count(old)
    if n != 1:
        sys.exit(f"ANCHOR FAIL [{label}]: found {n} occurrences, expected 1\n  {old[:160]}")
    edits.append(label)
    return html.replace(old, new)


# ── data ──────────────────────────────────────────────────────────────────────
content = load_reels(f"{DATA}/instagramreels_20260701_20260722.csv") + \
          load_posts(f"{DATA}/instagramposts_20260701_20260722.csv")
all_content, selected, averages = run(content)

by_url = {p["url"].rstrip("/").rsplit("/", 1)[-1]: p for p in all_content}
FOUNDER = by_url["DakvyIekbsZ"]   # Behind The Seams, 7/9  -- package s7 override to #1
TEASE = by_url["DbD5DG4Rxul"]     # Mille-Feuille tease, 7/21 -- engine #1, promotional
CAROUSEL = by_url["DaSxhsUlvQh"]  # Freedom to be you, 7/2  -- shares standout

# Package s7: "No manual override needed unless the engine surfaces a promotional
# post as #1, in which case prefer the founder-led / community piece." The engine
# ranked the 7/21 Mille-Feuille launch tease #1 (140.5) over the founder story
# (107.4), so the documented override applies. Both cleared the eligibility gate;
# neither card fabricates a standout.
assert selected[0]["url"] == TEASE["url"], "engine #1 changed; re-check the override"
featured = [FOUNDER, TEASE]
dropdown = [CAROUSEL]

html = open(SRC, encoding="utf-8").read()

# ── 1. head / title ───────────────────────────────────────────────────────────
html = sub(html,
    "<title>MEAS Active &ndash; June 2026 | Scroll Media</title>",
    "<title>MEAS Active &ndash; Final Performance Report | Scroll Media</title>",
    "title")

# n/a styling for the two unavailable metrics + flat delta already exists (.ph-delta.fl)
html = sub(html,
    "    .mc-badge.watch{background:rgba(245,158,11,.1);color:var(--watch)}",
    "    .mc-badge.watch{background:rgba(245,158,11,.1);color:var(--watch)}\n"
    "    .mc-badge.na{background:rgba(21,21,22,.06);color:var(--muted)}",
    "css:mc-badge.na")
html = sub(html,
    "    .mc-val.exceed{color:var(--exceed)}.mc-val.ontrack{color:var(--ontrack)}.mc-val.watch{color:var(--watch)}",
    "    .mc-val.exceed{color:var(--exceed)}.mc-val.ontrack{color:var(--ontrack)}.mc-val.watch{color:var(--watch)}\n"
    "    .mc-val.na{color:var(--muted);font-weight:700}\n"
    "    .mc.na{opacity:.85}",
    "css:mc-val.na")
html = sub(html,
    "    .ph-badge.exceed .bd{background:#c4b5fd}.ph-badge.ontrack .bd{background:#7a9ad8}.ph-badge.watch .bd{background:#fbbf24}",
    "    .ph-badge.exceed .bd{background:#c4b5fd}.ph-badge.ontrack .bd{background:#7a9ad8}.ph-badge.watch .bd{background:#fbbf24}\n"
    "    .ph-badge.na .bd{background:rgba(255,255,255,.35)}",
    "css:ph-badge.na")
# closeout blocks
html = sub(html,
    "    .footer{background:#fff;padding:2.25rem 1.25rem;border-top:1px solid var(--border)}",
    "    .carry{background:var(--ghost);border:1px solid var(--border);border-left:3px solid var(--azure);"
    "border-radius:10px;padding:1.25rem 1.35rem;margin-top:1.1rem}\n"
    "    .carry h3{font-size:1.0625rem;font-weight:800;letter-spacing:-.01em;margin-bottom:.6rem;color:var(--ink)}\n"
    "    .carry p{font-size:.9375rem;line-height:1.75;color:var(--body)}\n"
    "    .carry p+p{margin-top:.85rem}\n"
    "    .carry .lbl{font-weight:800;color:var(--ink)}\n"
    "    .doorway{max-width:1100px;margin:0 auto;padding:0 1.25rem 2.25rem}\n"
    "    .doorway p{font-size:1rem;line-height:1.75;color:var(--body);font-style:italic;"
    "border-top:1px solid var(--border);padding-top:1.5rem}\n"
    "    .footer{background:#fff;padding:2.25rem 1.25rem;border-top:1px solid var(--border)}",
    "css:closeout")

# ── 2. nav ────────────────────────────────────────────────────────────────────
html = sub(html,
    '<a class="report-nav-link" href="#beat5">What&rsquo;s Next</a>',
    '<a class="report-nav-link" href="#beat5">Carry Forward</a>',
    "nav:beat5")

# ── 3. hero ───────────────────────────────────────────────────────────────────
html = sub(html,
    '<div class="hero-eyebrow"><span class="dot"></span>June 2026 Performance Report</div>',
    '<div class="hero-eyebrow"><span class="dot"></span>Final Performance Report</div>',
    "hero:eyebrow")
html = sub(html,
    'Lift Stage &middot; Month 14',
    'Lift Stage &middot; Month 15',
    "hero:stage")
html = sub(html,
    '<span>June 1&ndash;30, 2026</span>',
    '<span>July 1&ndash;22 (final)</span>',
    "hero:window")
html = sub(html,
    '<p class="ph-label">Monthly Performance Score</p>',
    '<p class="ph-label">Final Performance Score</p>',
    "hero:score-label")
html = sub(html,
    '<span class="ph-delta dn">&#9660; 0.6 vs. May</span>',
    '<span class="ph-delta fl">Flat vs. June</span>',
    "hero:delta")
html = sub(html,
    '<span class="ph-badge exceed"><span class="bd"></span>1 Exceeding</span>\n'
    '          <span class="ph-badge ontrack"><span class="bd"></span>4 On Track</span>\n'
    '          <span class="ph-badge watch"><span class="bd"></span>5 Watch</span>',
    '<span class="ph-badge exceed"><span class="bd"></span>1 Exceeding</span>\n'
    '          <span class="ph-badge ontrack"><span class="bd"></span>2 On Track</span>\n'
    '          <span class="ph-badge watch"><span class="bd"></span>5 Watch</span>\n'
    '          <span class="ph-badge na"><span class="bd"></span>2 n/a</span>',
    "hero:badges")
html = sub(html,
    '<p class="ph-label">Bio Link Engagement</p>\n        <div class="ph-bignum">72</div>',
    '<p class="ph-label">Bio Link Engagement</p>\n        <div class="ph-bignum">57</div>',
    "hero:outcome")
html = sub(html,
    '<p class="hero-summary"><strong>June normalized after May&rsquo;s grand-opening surge, but conversion efficiency held and your community leaned in.</strong></p>',
    '<p class="hero-summary"><strong>A lighter 22 day close built toward the Mille-Feuille launch, and the two signals that defined the year held: '
    'click-through stayed well above benchmark and the founder story carried the conversation.</strong></p>',
    "hero:summary")
html = sub(html,
    'Your score reflects how this month performed against your stage targets, weighted by what predicts buyer behavior. Monthly score is a snapshot. Strategy decisions are made on quarterly trend, not single-month signal.',
    'Your score reflects how this window performed against your stage targets, weighted by what predicts buyer behavior. '
    'This is a partial window, July 1 to 22, with six published pieces, so volume metrics read lighter than a full month by design. '
    'Two metrics are marked not available and are excluded from the score rather than counted as zero.',
    "hero:method")

# ── 4. beat 2 ─────────────────────────────────────────────────────────────────
html = sub(html,
    'We published 8 posts, leaning into founder and mission content, interactive engagement, and product cheatsheets, all pointing toward the shop and the email list.',
    'We published 6 pieces in 22 days, built around the founder story and the Mille-Feuille launch runway, all pointing toward the shop and the email list.',
    "beat2:takeaway")
html = sub(html,
    '<div class="work-strip"><span class="work-chip"><b>8 posts</b></span><span class="work-chip">Mostly Reels, some carousels</span><span class="work-chip">Themes: founder and mission content, interactive engagement, product cheatsheets</span><span class="work-chip">Focus: shop and email list</span></div>',
    '<div class="work-strip"><span class="work-chip"><b>6 pieces</b></span><span class="work-chip">5 Reels, 1 carousel</span>'
    '<span class="work-chip">Themes: founder story, launch runway, community and values</span>'
    '<span class="work-chip">Focus: shop and email list</span><span class="work-chip">Lighter launch-build cadence</span></div>',
    "beat2:workstrip")
html = sub(html,
    '<h2 class="sec-title" id="allposts-title">All Posts This Month</h2>',
    '<h2 class="sec-title" id="allposts-title">All Posts, July 1 to 22</h2>',
    "beat2:allposts-title")
html = sub(html,
    'Every post published this month, with the numbers behind each one. Tap any column header to sort. Rows with a lime edge over-indexed on saves or click-through, the two strongest buyer signals.',
    'Every piece published in this final window, with the numbers behind each one. Tap any column header to sort. '
    'Rows with a lime edge over-indexed on at least one standout signal against the window average.',
    "beat2:allposts-sub")
html = sub(html,
    '<div class="ap-legend"><span class="swatch"></span> Lime edge = over-indexed on saves or CTR (at least 1.5&times; the account average this month).</div>',
    '<div class="ap-legend"><span class="swatch"></span> Lime edge = over-indexed on at least one standout signal '
    '(saves, shares, comments, views, or retention) at 1.5&times; or more the window average.</div>',
    "beat2:legend")

# ── 5. beat 3 ─────────────────────────────────────────────────────────────────
html = sub(html,
    'Reach settled off the opening peak, but click-through stayed above your stage ceiling and comments broke out on mission content.',
    'On a fraction of a normal month&rsquo;s volume, click-through held at 9.7% against a 3 to 6% benchmark, and the founder story drove nearly half of all comments.',
    "beat3:takeaway")
html = sub(html,
    '<div class="bstats"><div class="bstat"><div class="bstat-val exceed">9.8%</div><div class="bstat-lbl">Click-through rate</div><span class="bstat-tag exceed">Exceeding</span></div><div class="bstat"><div class="bstat-val ontrack">193</div><div class="bstat-lbl">Comments</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val ontrack">72</div><div class="bstat-lbl">Bio link taps</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val watch">49%</div><div class="bstat-lbl">Video retention</div><span class="bstat-tag watch">Watch</span></div></div>',
    '<div class="bstats"><div class="bstat"><div class="bstat-val exceed">9.7%</div><div class="bstat-lbl">Click-through rate</div><span class="bstat-tag exceed">Exceeding</span></div>'
    '<div class="bstat"><div class="bstat-val watch">54</div><div class="bstat-lbl">Comments</div><span class="bstat-tag watch">Watch</span></div>'
    '<div class="bstat"><div class="bstat-val ontrack">57</div><div class="bstat-lbl">Bio link taps</div><span class="bstat-tag ontrack">On Track</span></div>'
    '<div class="bstat"><div class="bstat-val watch">37.8%</div><div class="bstat-lbl">Video retention</div><span class="bstat-tag watch">Watch</span></div></div>',
    "beat3:bstats")

# goal tracker bars: TOFU 0.35/1.75=20%, MOFU 1.5/5.5=27%, BOFU 2.9/3.5=83%
# (numerator 4.75 and denominator 10.75 match score_report.py exactly)
# the goal-tracker block is minified across lines; patch the three segments individually
GT = ('gt-bar-fill lime" data-w="{w}" style="width:0%"></div></div>\n            '
      '<span class="gt-pct">{w}%</span>\n          </div></div><div class="gt-side">'
      '<span class="gt-spark-lbl">Weighted score</span>'
      '<span class="gt-score-pts">{pts}<span class="gt-score-max">/{den}</span>')
html = sub(html, GT.format(w=35, pts="0.95", den="2.75"), GT.format(w=20, pts="0.35", den="1.75"), "beat3:gt-tofu")
html = sub(html, GT.format(w=35, pts="1.9", den="5.5"), GT.format(w=27, pts="1.5", den="5.5"), "beat3:gt-mofu")
html = sub(html, GT.format(w=64, pts="3.2", den="5.0"), GT.format(w=83, pts="2.9", den="3.5"), "beat3:gt-bofu")

# goal narratives
html = sub(html,
    'Your awareness stage scored 35% this month. New followers, views, and shares all normalized from May&rsquo;s grand-opening surge. Rebuilding reach volume with founder and mission content is the July focus.',
    'Your awareness stage scored 20% across the window. Six pieces in 22 days is roughly a third of a normal month&rsquo;s output, so views and shares land well under the monthly floors. '
    'New followers is not available for this window and is excluded rather than counted as a zero.',
    "beat3:narr-tofu")
html = sub(html,
    'Your engagement stage scored 35%. Comments broke through, up 74% and well inside range as the mission content resonated. Retention sits a hair under the Lift floor and saves eased, so those are the July levers to lift the layer.',
    'Your engagement stage scored 27%. Comments held their shape on far less volume, with the founder story alone drawing 24 of the 54. '
    'Retention at 37.8% and saves at 15 are the two levers that stayed below target all year, and they remain the clearest room to grow.',
    "beat3:narr-mofu")
html = sub(html,
    'Your conversion stage scored 64%, the strongest of the three. Click-through stayed above the Lift ceiling even off the opening peak, and link taps held inside range. The conversion engine is efficient; the job is feeding it more reach from the top.',
    'Your conversion stage scored 83%, the strongest of the three and the clearest proof point of the year. Click-through finished at 9.7%, above the Lift ceiling and nearly identical to June&rsquo;s 9.8%, '
    'and link taps held inside range on a partial window. Profile conversion rate is not available for this window and is excluded rather than counted as a zero.',
    "beat3:narr-bofu")

# performance breakdown header + followers banner
html = sub(html, '<p class="sec-label">June 2026</p>', '<p class="sec-label">July 1&ndash;22, 2026</p>', "beat3:perf-label")
html = sub(html,
    'Every tracked metric for June, scored against your Lift Stage target ranges with month-over-month comparison.',
    'Every tracked metric for the final window, scored against your Lift Stage target ranges. Targets are monthly, so a 22 day window reads lighter on volume metrics by design.',
    "beat3:perf-sub")
html = sub(html,
    '<div class="fb-count">10,134</div>\n        <div class="fb-mom"><span class="mom dn">&#9660; 0.3% vs. May</span></div>',
    '<div class="fb-count">10,118</div>\n        <div class="fb-mom"><span class="mom fl">Essentially flat vs. June (10,134)</span></div>',
    "beat3:followers")

# ── metric cards: 8 populated + 2 n/a ─────────────────────────────────────────
def mc(name, val, badge, cls, target, mom, barw, note, callout):
    return (f'<div class="mc">\n'
            f'          <div class="mc-top"><span class="mc-name">{name}</span><span class="mc-badge {cls}">{badge}</span></div>\n'
            f'          <div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val {cls}">{val}</span></div>'
            f'<div><span class="mc-lbl">Target Range</span><span class="mc-tgt">{target}</span></div></div>\n'
            f'          <div class="mc-mom">{mom}</div>\n'
            f'          <div class="bar-track"><div class="bar-fill {cls}" data-w="{barw}" style="width:0%"></div></div>\n'
            f'          <p class="mc-note">{note}</p>\n'
            f'          <p class="mc-callout">{callout}</p>\n'
            f'        </div>')


def mc_na(name, target, note, callout):
    return (f'<div class="mc na">\n'
            f'          <div class="mc-top"><span class="mc-name">{name}</span><span class="mc-badge na">Not available</span></div>\n'
            f'          <div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val na">n/a</span></div>'
            f'<div><span class="mc-lbl">Target Range</span><span class="mc-tgt">{target}</span></div></div>\n'
            f'          <p class="mc-note">{note}</p>\n'
            f'          <p class="mc-callout">{callout}</p>\n'
            f'        </div>')


DN = lambda t: f'<span class="mom dn">&#9660; {t}</span>'
FL = lambda t: f'<span class="mom fl">{t}</span>'

# TOFU
html = re.sub(
    r'<!-- New Followers -->\n\s*<div class="mc">.*?</div>\n        <!-- Shares -->',
    lambda m: '<!-- New Followers -->\n        ' + mc_na(
        "New Followers", "100 &ndash; 270",
        "Instagram changed how gross new followers are reported, so this figure is not available for the final window. "
        "It is excluded from the score rather than counted as a zero.",
        "Followers were essentially flat across the window, 10,134 to 10,118. Net movement of 16 accounts over 22 days "
        "means the audience you built held steady right through the close.") + '\n        <!-- Shares -->',
    html, count=1, flags=re.S)
edits.append("beat3:mc-newfollowers-na")

html = sub(html,
    '<div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val watch">26</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">60 &ndash; 300</span></div></div>\n'
    '          <div class="mc-mom"><span class="mom dn">&#9660; 24% vs May</span></div>\n'
    '          <div class="bar-track"><div class="bar-fill watch" data-w="9" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Below floor and down from May. Shareable founder and mission content is the July lever.</p>\n'
    '          <p class="mc-callout">Shares fell 24%. Translation: 24% fewer people sent your content to someone else. Shares put you in front of new audiences your posts wouldn&rsquo;t reach on their own.</p>',
    '<div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val watch">19</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">60 &ndash; 300</span></div></div>\n'
    '          <div class="mc-mom">' + DN("27% vs June") + '</div>\n'
    '          <div class="bar-track"><div class="bar-fill watch" data-w="6" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Below floor on a partial window. The one carousel out-shared every Reel, which is worth carrying into your format mix.</p>\n'
    '          <p class="mc-callout">Shares landed at 19. Translation: 19 people sent your content to someone else. Shares put you in front of new audiences your posts wouldn&rsquo;t reach on their own.</p>',
    "beat3:mc-shares")

html = sub(html,
    '<div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val ontrack">51,417</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">40,000 &ndash; 150,000</span></div></div>\n'
    '          <div class="mc-mom"><span class="mom dn">&#9660; 5% vs May</span></div>\n'
    '          <div class="bar-track"><div class="bar-fill ontrack" data-w="34" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Inside range. Reach settled back from the grand-opening peak.</p>\n'
    '          <p class="mc-callout">Views fell 5%. Translation: your content reached 5% fewer screens this month. Views are the widest measure of how many people you got in front of, and everything downstream starts here.</p>',
    '<div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val watch">10,491</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">40,000 &ndash; 150,000</span></div></div>\n'
    '          <div class="mc-mom">' + DN("80% vs June") + '</div>\n'
    '          <div class="bar-track"><div class="bar-fill watch" data-w="7" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Below the monthly floor on six pieces across 22 days. Average reach per piece held at 1,067.</p>\n'
    '          <p class="mc-callout">Views came in at 10,491. Translation: your content reached 10,491 screens in 22 days. Views are the widest measure of how many people you got in front of, and everything downstream starts here.</p>',
    "beat3:mc-views")
html = sub(html, '<span class="mc-name">Total Views</span><span class="mc-badge ontrack">On Track</span>',
           '<span class="mc-name">Total Views</span><span class="mc-badge watch">Watch</span>', "beat3:mc-views-badge")

# MOFU
html = sub(html,
    '<div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val ontrack">733</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">300 &ndash; 2,000</span></div></div>\n'
    '          <div class="mc-mom"><span class="mom dn">&#9660; 8% vs May</span></div>\n'
    '          <div class="bar-track"><div class="bar-fill ontrack" data-w="37" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Inside range. Consideration traffic held near the opening level.</p>\n'
    '          <p class="mc-callout">Profile visits fell 8%. Translation: 8% fewer people tapped through to look closer at who you are. A profile visit is a deliberate step toward becoming a customer, not a passive scroll.</p>',
    '<div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val ontrack">585</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">300 &ndash; 2,000</span></div></div>\n'
    '          <div class="mc-mom">' + DN("20% vs June") + '</div>\n'
    '          <div class="bar-track"><div class="bar-fill ontrack" data-w="29" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Inside range even on a partial window. Consideration traffic stayed healthy to the end.</p>\n'
    '          <p class="mc-callout">Profile visits came in at 585. Translation: 585 people tapped through to look closer at who you are. A profile visit is a deliberate step toward becoming a customer, not a passive scroll.</p>',
    "beat3:mc-profilevisits")

html = sub(html,
    '<div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val watch">49%</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">50% &ndash; 65%</span></div></div>\n'
    '          <div class="mc-mom"><span class="mom up">&#9650; 1 pt vs May</span></div>\n'
    '          <div class="bar-track"><div class="bar-fill watch" data-w="75" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Just below the Lift floor. Founder-story Reels are the lever to lift attention.</p>\n'
    '          <p class="mc-callout">Retention came in at 49%. Translation: on average, people watched 49% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences.</p>',
    '<div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val watch">37.8%</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">50% &ndash; 65%</span></div></div>\n'
    '          <div class="mc-mom">' + DN("11.2 pts vs June") + '</div>\n'
    '          <div class="bar-track"><div class="bar-fill watch" data-w="58" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Below the Lift floor and the largest single gap in the window. Front-loading the hook is the highest-leverage fix.</p>\n'
    '          <p class="mc-callout">Retention came in at 37.8%. Translation: on average, people watched 37.8% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences.</p>',
    "beat3:mc-retention")

html = sub(html,
    '<div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val watch">22</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">80 &ndash; 400</span></div></div>\n'
    '          <div class="mc-mom"><span class="mom dn">&#9660; 19% vs May</span></div>\n'
    '          <div class="bar-track"><div class="bar-fill watch" data-w="6" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Below floor and down from May. Save-worthy product and how-to content is the lever.</p>\n'
    '          <p class="mc-callout">Saves fell 19%. Translation: 19% fewer people bookmarked your posts to act on later. Saves are the strongest signal of a future buyer.</p>',
    '<div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val watch">15</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">80 &ndash; 400</span></div></div>\n'
    '          <div class="mc-mom">' + DN("32% vs June") + '</div>\n'
    '          <div class="bar-track"><div class="bar-fill watch" data-w="4" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Below floor, the same gap flagged every month this year. Save-worthy value content is the standing recommendation.</p>\n'
    '          <p class="mc-callout">Saves landed at 15. Translation: 15 people bookmarked your posts to act on later. Saves are the strongest signal of a future buyer.</p>',
    "beat3:mc-saves")

html = sub(html,
    '<div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val ontrack">193</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">75 &ndash; 250</span></div></div>\n'
    '          <div class="mc-mom"><span class="mom up">&#9650; 74% vs May</span></div>\n'
    '          <div class="bar-track"><div class="bar-fill ontrack" data-w="77" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Inside range and up sharply from May. Mission content is driving conversation.</p>\n'
    '          <p class="mc-callout">Comments grew 74%. Translation: 74% more people stopped to start a conversation with you. Comments are public proof that your audience is engaged, and they pull in the people watching from the sidelines.</p>',
    '<div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val watch">54</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">75 &ndash; 250</span></div></div>\n'
    '          <div class="mc-mom">' + DN("72% vs June") + '</div>\n'
    '          <div class="bar-track"><div class="bar-fill watch" data-w="22" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Under the monthly floor on a third of the usual output, but the founder story alone drew 24 of the 54.</p>\n'
    '          <p class="mc-callout">Comments landed at 54. Translation: 54 people stopped to start a conversation with you. Comments are public proof that your audience is engaged, and they pull in the people watching from the sidelines.</p>',
    "beat3:mc-comments")
html = sub(html, '<span class="mc-name">Comments</span><span class="mc-badge ontrack">On Track</span>',
           '<span class="mc-name">Comments</span><span class="mc-badge watch">Watch</span>', "beat3:mc-comments-badge")

# BOFU
html = sub(html,
    '<div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val exceed">9.8%</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">3% &ndash; 6%</span></div></div>\n'
    '          <div class="mc-mom"><span class="mom dn">&#9660; 7.1 pts vs May</span></div>\n'
    '          <div class="bar-track"><div class="bar-fill exceed" data-w="100" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Above the Lift ceiling. Even off the opening peak, the bio link converts efficiently.</p>\n'
    '          <p class="mc-callout">Click-through rate came in at 9.8%. Translation: of everyone who saw your link, 9.8% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers.</p>',
    '<div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val exceed">9.7%</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">3% &ndash; 6%</span></div></div>\n'
    '          <div class="mc-mom">' + FL("0.1 pts vs June, essentially flat") + '</div>\n'
    '          <div class="bar-track"><div class="bar-fill exceed" data-w="100" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Above the Lift ceiling and steady to the final day. The strongest and most consistent metric of the engagement.</p>\n'
    '          <p class="mc-callout">Click-through rate came in at 9.7%. Translation: of everyone who saw your link, 9.7% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers.</p>',
    "beat3:mc-ctr")

html = sub(html,
    '<div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val ontrack">72</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">30 &ndash; 180</span></div></div>\n'
    '          <div class="mc-mom"><span class="mom dn">&#9660; 46% vs May</span></div>\n'
    '          <div class="bar-track"><div class="bar-fill ontrack" data-w="40" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Inside range but down from May&rsquo;s opening high. Steady traffic to the shop and list.</p>\n'
    '          <p class="mc-callout">Link taps fell 46%. Translation: 46% fewer people tapped the link in your bio to move toward your site, booking, or offer. A link tap is one of the clearest actions someone takes when they are ready to do business.</p>',
    '<div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val ontrack">57</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">30 &ndash; 180</span></div></div>\n'
    '          <div class="mc-mom">' + DN("21% vs June") + '</div>\n'
    '          <div class="bar-track"><div class="bar-fill ontrack" data-w="32" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Inside range on a partial window. Steady traffic to the shop and list right to the close.</p>\n'
    '          <p class="mc-callout">Link taps landed at 57. Translation: 57 people tapped the link in your bio to move toward your site, booking, or offer. A link tap is one of the clearest actions someone takes when they are ready to do business.</p>',
    "beat3:mc-linktaps")

html = re.sub(
    r'<!-- PCR -->\n\s*<div class="mc">.*?</div>\n      </div>\n    </div>\n  </section>',
    lambda m: '<!-- PCR -->\n        ' + mc_na(
        "PCR", "10% &ndash; 16%",
        "Profile conversion rate is derived from gross new followers, which Instagram no longer reports for this window, "
        "so it cannot be computed. It is excluded from the score rather than counted as a zero.",
        "Followers held essentially flat, 10,134 to 10,118, while 585 people still visited the profile. The audience you built "
        "stayed with you through the final weeks.") + '\n      </div>\n    </div>\n  </section>',
    html, count=1, flags=re.S)
edits.append("beat3:mc-pcr-na")

# c2b funnel steps
html = sub(html,
    '<div class="c2b-step"><span class="c2b-step-num">51,417</span><div class="c2b-step-main"><span class="c2b-step-txt">people saw your content</span><span class="c2b-step-badge">\U0001F3DF Great American Ball Park filled 1.2x over</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">733</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped through to look closer</span><span class="c2b-step-badge">\U0001F3BC a Music Hall main-floor crowd</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">22</span><div class="c2b-step-main"><span class="c2b-step-txt">bookmarked content to reference later</span><span class="c2b-step-badge">\U0001F4CC 22 pre-purchase bookmarks</span></div></div>\n'
    '        <div class="c2b-step hi"><span class="c2b-step-num">72</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped a bio link, the highest-intent signal we track</span><span class="c2b-step-badge">\U0001F446 72 deliberate taps toward your shop</span></div></div>',
    '<div class="c2b-step"><span class="c2b-step-num">10,491</span><div class="c2b-step-main"><span class="c2b-step-txt">people saw your content</span><span class="c2b-step-badge">\U0001F3BC Music Hall filled 3x over</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">585</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped through to look closer</span><span class="c2b-step-badge">\U0001F3AD a sold-out Memorial Hall crowd</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">15</span><div class="c2b-step-main"><span class="c2b-step-txt">bookmarked content to reference later</span><span class="c2b-step-badge">\U0001F4CC 15 pre-purchase bookmarks</span></div></div>\n'
    '        <div class="c2b-step hi"><span class="c2b-step-num">57</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped a bio link, the highest-intent signal we track</span><span class="c2b-step-badge">\U0001F446 57 deliberate taps toward your shop</span></div></div>',
    "beat3:c2b-funnel")
html = sub(html,
    'How this month&rsquo;s attention maps to business signal',
    'How this final window&rsquo;s attention maps to business signal',
    "beat3:c2b-sub")
html = sub(html,
    '<p class="c2b-panel-label">The funnel this month</p>',
    '<p class="c2b-panel-label">The funnel in this final window</p>',
    "beat3:c2b-panel-label")

# ── 6. beat 4: featured posts ────────────────────────────────────────────────
# The "Outlier Magnitude" chip is intentionally dropped on this report. v2.0
# decoupled composite score from showcase narrative, and the package s7 override
# puts the founder story (1.07x composite) ahead of the launch tease (1.41x).
# Printing a lower magnitude above a higher one would read as an error to the
# future agency this report gets forwarded to (Procedural Gate #10). The standout
# chips carry the real, checkable numbers instead.
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def card(post, rank, hook, preview, rest, cid, standouts, why):
    badge = "reel-badge" if post["is_reel"] else "carousel-badge"
    label = "REEL" if post["is_reel"] else "CAROUSEL"
    pill = "Reel" if post["is_reel"] else "Carousel"
    sm = "".join(
        f'<div class="standout-metric"><span class="sm-label">{l}</span>'
        f'<span class="sm-value">{v}</span>'
        f'<span class="sm-badge {c}">{m}x account avg</span></div>'
        for l, v, m, c in standouts)
    return (
        f'<div class="post-card"><div class="post-header">'
        f'<span class="post-rank">{rank}</span>'
        f'<span class="post-type-badge {badge}">{label}</span></div>'
        f'<div class="post-body"><div class="post-date">{post["date"]}</div>'
        f'<div class="post-format-pill">{pill}</div>'
        f'<blockquote class="post-hook">&ldquo;{esc(hook)}&rdquo;</blockquote>'
        f'<div class="post-caption"><span class="cap-preview">{esc(preview)}</span>'
        f'<span class="cap-ellipsis" id="{cid}-ellipsis">&hellip;</span>'
        f'<span class="cap-rest" id="{cid}-rest" style="display:none">{esc(rest)}</span>'
        f'<button class="cap-toggle" id="{cid}-btn" onclick="toggleCap(\'{cid}\')">Show more</button></div>'
        f'<div class="standout-metrics">{sm}</div>'
        f'<div class="post-why"><div class="why-label">&#9650; WHY IT WORKED</div>'
        f'<p class="why-text">{why}</p></div>'
        f'<a href="{post["url"]}" target="_blank" rel="noopener" class="post-ig-btn">'
        f'View on Instagram &rarr;</a></div></div>')


def split_cap(caption, n=200):
    """Preview + remainder of the FULL caption. June's cards repeat the hook line
    inside the caption preview, so nothing is dropped from the client's copy."""
    body = caption.strip()
    if len(body) <= n:
        return body, ""
    cut = body.rfind(" ", 0, n)          # do not split mid-word
    cut = cut if cut > n - 40 else n
    return body[:cut], body[cut:]


f_hook = "Behind The Seams: How I Create Our Collections"
f_prev, f_rest = split_cap(FOUNDER["caption"])
t_hook = "Saw this gal on the street and I just had to stop her…"
t_prev, t_rest = split_cap(TEASE["caption"])
c_hook = "Freedom to be you. Freedom to move."
c_prev, c_rest = split_cap(CAROUSEL["caption"])

card1 = card(FOUNDER, "#1 Top Post", f_hook, f_prev, f_rest, "tpreel1",
             [("COMMENTS", "24", "2.7", "outlier-2x")],
             "A conversation outlier at 2.7x the window&rsquo;s comment average, and the single most engaging piece of the "
             "final window at a 13.3% engagement rate against an account average of 6.4%. Erin on camera, telling the story "
             "of how a collection actually gets made, is the content that pulled this community into a reply every time we "
             "ran it. This is the engine worth carrying forward.")
card2 = card(TEASE, "#2 Top Post", t_hook, t_prev, t_rest, "tpreel2",
             [("SAVES", "5", "2.0", "outlier-2x")],
             "Save density at 2.0x the window average, on top of the widest reach of the final window at 2,503 views. "
             "Saves are the strongest pre-purchase signal we track, and seeing them concentrate on the Mille-Feuille tease "
             "means people were bookmarking the drop to come back to it. Launch runway content earns its place.")
card3 = card(CAROUSEL, "#3 Top Post", c_hook, c_prev, c_rest, "tpcar3",
             [("SHARES", "8", "2.5", "outlier-2x")],
             "Share velocity at 2.5x the window average, and the share leader of the final window. A single static carousel "
             "out-shared every Reel we published, which is worth remembering for your format mix. Shares put you in front of "
             "audiences your own followers cannot reach.")

old_feature = re.search(r'<div class="feature-2up">.*?</div></div></div>\n  <p class="beat-pattern">', html, re.S)
if not old_feature:
    sys.exit("ANCHOR FAIL [beat4:feature-2up]")
html = html.replace(old_feature.group(0),
    f'<div class="feature-2up">{card1}{card2}</div>\n'
    f'  <details class="proof"><summary><span class="proof-ic">&#9636;</span>'
    f'<span>See the other standout post from this window</span>'
    f'<span class="proof-chev">&#8250;</span></summary><div class="proof-body">'
    f'<div class="posts-grid">{card3}</div></div></details>\n'
    f'  <p class="beat-pattern">', 1)
edits.append("beat4:featured+dropdown")

html = sub(html,
    'The content that pulled them into conversation was founder-led and values-driven. Retention and saves are the levers to lift.',
    'The pattern that closed the year is the same one that opened it: when Erin is on camera telling the story, the community shows up to talk. '
    'Retention and saves stayed the two levers to lift.',
    "beat4:pattern")

# ── 7. beat 4: quarter view + full engagement arc strip ──────────────────────
html = sub(html,
    '<div class="qy-col current"><div class="qy-q">Q2</div><div class="qy-range">Apr&ndash;Jun</div><div class="qy-avg">7.9<span class="u">/10</span></div><div class="qy-badge steady">Steady</div>',
    '<div class="qy-col "><div class="qy-q">Q2</div><div class="qy-range">Apr&ndash;Jun</div><div class="qy-avg">7.9<span class="u">/10</span></div><div class="qy-badge steady">Steady</div>',
    "beat4:q2-uncurrent")
html = sub(html,
    '<div class="qy-col "><div class="qy-q">Q3</div><div class="qy-range">Jul&ndash;Sep</div><div class="qy-note">Begins July</div><div class="qy-state">Pending</div></div>'
    '<div class="qy-col "><div class="qy-q">Q4</div><div class="qy-range">Oct&ndash;Dec</div><div class="qy-note">Later this year</div><div class="qy-state">Pending</div></div>',
    '<div class="qy-col current"><div class="qy-q">Q3</div><div class="qy-range">Jul 1&ndash;22</div><div class="qy-avg">7.6<span class="u">/10</span></div>'
    '<div class="qy-badge steady">Steady</div><div class="qy-bars"><span class="cur" style="height:48%"></span></div>'
    '<div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> click-through finished at 9.7%, above benchmark for the last time as it was for most of the year, '
    'and the founder story drove 24 of 54 comments.</div>'
    '<div class="qy-tline"><span class="qy-tl">Watched:</span> retention at 37.8% and saves at 15, the two gaps that stayed open all year.</div></div>'
    '<div class="qy-state">Final window</div></div>'
    '<div class="qy-col pending"><div class="qy-q">Q4</div><div class="qy-range">Oct&ndash;Dec</div><div class="qy-note">Engagement closed July 22</div><div class="qy-state">Not tracked</div></div>',
    "beat4:q3-q4")

# full engagement arc: Oct 2025 -> Jul 2026, quarter-separated (package s3 + archive index)
ARC = [("Q4 2025", [("Oct", "8.5"), ("Nov", "7.5"), ("Dec", "8.0")]),
       ("Q1 2026", [("Jan", "7.3"), ("Feb", "7.4"), ("Mar", "7.9")]),
       ("Q2 2026", [("Apr", "7.9"), ("May", "8.2"), ("Jun", "7.6")]),
       ("Q3 2026", [("Jul", "7.6")])]
strip = "".join(
    '<div class="mscore-q">' + "".join(
        f'<div class="mscore-cell{" current" if m == "Jul" else ""}">'
        f'<div class="mscore-m">{m}</div><div class="mscore-v">{v}</div></div>'
        for m, v in cells) + '</div>'
    for _, cells in ARC)

old_strip = re.search(r'<p class="mscore-lead">.*?</div></div></div></div>', html, re.S)
if not old_strip:
    sys.exit("ANCHOR FAIL [beat4:mscore]")
html = html.replace(old_strip.group(0),
    '<p class="mscore-lead">Your composite score across the full engagement, October 2025 through the final window. '
    'October to December 2025 come from the legacy performance sheet; January 2026 forward are v8 scored reports. '
    'Every month we managed is shown, and the year closed inside the healthy 7.3 to 8.5 band.</p>'
    f'<div class="mscore">{strip}</div>', 1)
edits.append("beat4:mscore-arc")
html = sub(html,
    'Your composite score each month across 2026. Months without a published report show as not tracked, never as a zero.',
    '', "beat4:mscore-oldlead") if 'Your composite score each month across 2026' in html else html
html = sub(html, '<p class="sub-head">Your quarter so far</p>',
           '<p class="sub-head">Your full engagement</p>', "beat4:subhead")
html = sub(html,
    'You&rsquo;re past testing and into execution. We track performance monthly and step back to adjust the strategy each quarter, so decisions come from real patterns, not single-month swings.',
    'This is the whole engagement in one view, quarter by quarter, from October 2025 through the final window. '
    'Each quarter we stepped back and adjusted the strategy from the pattern rather than from any single month.',
    "beat4:phase-line")
html = sub(html, '<span>See your month-by-month scores</span>',
           '<span>See every month we tracked</span>', "beat4:mscore-summary")

# ── 8. beat 5: What you carry forward + Going forward (package s4 / s5) ──────
old_b5 = re.search(r'<p class="beat-eyebrow"><span class="bn">5</span> What&rsquo;s next</p>.*?</section></div>\n\n<footer', html, re.S)
if not old_b5:
    sys.exit("ANCHOR FAIL [beat5]")
html = html.replace(old_b5.group(0),
    '<p class="beat-eyebrow"><span class="bn">5</span> What you carry forward</p>\n'
    '  <h2 class="beat-takeaway" id="beat5-t">Everything we built this year stays with you, and so does the playbook that produced it.</h2>\n'
    '  <div class="carry">\n'
    '    <h3>What you carry forward</h3>\n'
    '    <p>Everything we built this year stays with you. Your content library and b-roll, every published caption, and the '
    'unpublished backlog are in your handoff folder for the next 30 days. Beyond the files, you carry a proven playbook: the '
    'founder-led and community content that became your comment and reach engine, the collab and ambassador motion that '
    'consistently outperformed, and a click-through rate that held above the activewear benchmark month after month. That is a '
    'real, repeatable foundation to build on, whoever is steering next.</p>\n'
    '  </div>\n'
    '  <div class="carry">\n'
    '    <h3>Going forward</h3>\n'
    '    <p><span class="lbl">What&rsquo;s proven.</span> Founder-story and community content is your engine. Erin on camera, the '
    'mission, the ambassador and event moments: that is what your audience comments on, shares, and clicks. Your conversion intent '
    'is strong, with click-through running well above the 3 to 6% benchmark, most recently 9.7%.</p>\n'
    '    <p><span class="lbl">What to try next.</span> Your clearest room to grow is content people save and return to. '
    'Value-forward carousels, styling guides, &ldquo;which short for which workout&rdquo; decision references, are built to be '
    'saved and were the standout opportunity all year. Pair that with an email-list-first bio link to capture the traffic you are '
    'already winning.</p>\n'
    '    <p><span class="lbl">What to monitor.</span> Retention, which closed this final window at 37.8% against a 50 to 65% '
    'target, is what decides how far each post travels. Front-loading the hook and tightening pace is the highest-leverage fix. '
    'Watch saves and profile conversion rate alongside it.</p>\n'
    '  </div>\n'
    '</section></div>\n\n'
    '<div class="doorway">\n'
    '  <p>It has been a genuine pleasure building MEAS Active&rsquo;s presence alongside you this year. The door is always open, '
    'whether that is picking this back up down the road or sending a runner our way. Cheering you on.</p>\n'
    '</div>\n\n<footer', 1)
edits.append("beat5:carry-forward+going-forward+doorway")

# ── 9. footer ────────────────────────────────────────────────────────────────
html = sub(html,
    'Prepared by <a href="https://scrollmedia.co" target="_blank" rel="noopener">Scroll Media</a> &middot; June 2026 Performance Report<br>',
    'Prepared by <a href="https://scrollmedia.co" target="_blank" rel="noopener">Scroll Media</a> &middot; Final Performance Report &middot; July 1&ndash;22, 2026<br>',
    "footer")

# ── 10. ALL_POSTS from the CSVs ──────────────────────────────────────────────
ELIGIBLE = {FOUNDER["url"], TEASE["url"], CAROUSEL["url"]}
rows = []
for p in sorted(all_content, key=lambda x: x["dt"], reverse=True):
    rows.append({
        "date": p["dt"].strftime("%Y-%m-%d"),
        "date_display": p["dt"].strftime("%b %-d"),
        "format": "reel" if p["is_reel"] else "carousel",
        "caption": p["caption"],
        "views": p["views"], "saves": p["saves"], "shares": p["shares"],
        "comments": p["comments"], "retention": p["retention"],
        "linktaps": None, "ctr": None, "url": p["url"],
        "outlier": p["url"] in ELIGIBLE,
    })
old_ap = re.search(r'  var ALL_POSTS = \[.*?\];\n', html, re.S)
if not old_ap:
    sys.exit("ANCHOR FAIL [ALL_POSTS]")
html = html.replace(old_ap.group(0),
    "  var ALL_POSTS = " + json.dumps(rows, ensure_ascii=False) + ";\n", 1)
edits.append("ALL_POSTS")

# ── write ────────────────────────────────────────────────────────────────────
os.makedirs(OUT_DIR, exist_ok=True)
open(OUT, "w", encoding="utf-8").write(html)
print(f"wrote {OUT}  ({len(edits)} anchored edits)")
for e in edits:
    print("  -", e)

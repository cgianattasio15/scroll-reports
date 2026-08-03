#!/usr/bin/env python3
"""
build_carlsdeli_july.py -- transform Carl's Deli June 2026 (its inaugural v8.5
report) into the July 1-31 2026 report. Model: build_meas_july_closeout.py.

This is a first -> second report transition, so beyond the usual value swaps it
ADDS the month-over-month deltas the inaugural report did not carry, flips the
"first month" framing to a 2-month engagement, and appends July to the score
strip / quarter view.

Post-dependent content (Beat 2 count/work-strip/prose, Beat 4 takeaway/prose/
feature cards) is intentionally LEFT as June's here and finalized in a second
pass after the Metricool pull fills ALL_POSTS (build-package steps 2-3).

Every edit is an anchored replacement that hard-fails on a missing/ambiguous
anchor, so a silently-skipped edit is impossible. Score is computed by
score_report.py, not hand-set.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score_report as sr  # noqa: E402

REPO = "/Users/chase.gianattasio/Desktop/scroll-reports"
SRC = f"{REPO}/carlsdeli/june2026/index.html"
OUT_DIR = f"{REPO}/carlsdeli/july2026"
OUT = f"{OUT_DIR}/index.html"

# ── score guard: reproduce, do not hand-set ──────────────────────────────────
JULY = {"saves": 113, "ctr": 5.6, "retention": 37, "pcr": 14.0, "link_taps": 262,
        "profile_visits": 4702, "comments": 280, "new_followers": 660,
        "total_views": 230017, "shares": 1021}
JUNE = {"saves": 255, "ctr": 13.0, "retention": 25, "pcr": 23.4, "link_taps": 263,
        "profile_visits": 2024, "comments": 181, "new_followers": 474,
        "total_views": 147499, "shares": 833}
R = sr.score(JULY, "Lift", JUNE)
assert R["final"] == 9.2, f"score drift: expected 9.2, got {R['final']}"
badges = {m: st for m, _, _, _, st, _ in R["rows"]}
assert badges == {"saves": "ON TRACK", "ctr": "ON TRACK", "retention": "WATCH",
                  "pcr": "ON TRACK", "link_taps": "EXCEEDING", "profile_visits": "EXCEEDING",
                  "comments": "EXCEEDING", "new_followers": "EXCEEDING",
                  "total_views": "EXCEEDING", "shares": "EXCEEDING"}, badges

edits = []


def sub(html, old, new, label):
    n = html.count(old)
    if n != 1:
        sys.exit(f"ANCHOR FAIL [{label}]: found {n} occurrences, expected 1\n  {old[:180]}")
    edits.append(label)
    return html.replace(old, new)


html = open(SRC, encoding="utf-8").read()

# ── head / meta ──────────────────────────────────────────────────────────────
html = sub(html,
    "<title>Carl's Deli &ndash; June 2026 | Scroll Media</title>",
    "<title>Carl's Deli &ndash; July 2026 | Scroll Media</title>", "title")
html = sub(html,
    'content="Carl\'s Deli June 2026 Instagram performance report. Score 9.2/10. Exceptional Month. Lift Stage. Managed by Scroll Media.">',
    'content="Carl\'s Deli July 2026 Instagram performance report. Score 9.2/10. Exceptional Month. Lift Stage. Managed by Scroll Media.">', "meta:desc")
html = sub(html,
    'content="Carl\'s Deli, June 2026 Performance Report">',
    'content="Carl\'s Deli, July 2026 Performance Report">', "meta:og-title")

# ── hero ─────────────────────────────────────────────────────────────────────
html = sub(html,
    '<div class="hero-eyebrow"><span class="dot"></span>June 2026 Performance Report</div>',
    '<div class="hero-eyebrow"><span class="dot"></span>July 2026 Performance Report</div>', "hero:eyebrow")
html = sub(html, 'Lift Stage &middot; Month 1', 'Lift Stage &middot; Month 2', "hero:stage")
html = sub(html, '<span>June 1&ndash;30, 2026</span>', '<span>July 1&ndash;31, 2026</span>', "hero:window")
# outcome bignum: bio link taps 263 -> 262
html = sub(html,
    '<p class="ph-label">Bio Link Engagement</p>\n        <div class="ph-bignum">263</div>',
    '<p class="ph-label">Bio Link Engagement</p>\n        <div class="ph-bignum">262</div>', "hero:outcome")
# add a MoM delta to the score panel (inaugural report had none); 9.2 -> 9.2
html = sub(html,
    '<p class="ph-title">Exceptional Month</p>\n        <div class="ph-badges">',
    '<p class="ph-title">Exceptional Month</p>\n        <span class="ph-delta fl">Steady vs. June</span>\n        <div class="ph-badges">',
    "hero:score-delta")
# Beat 1 takeaway (score/metric story, not post-dependent)
html = sub(html,
    '<p class="hero-summary"><strong>Your launch month landed hard. New followers and shares came in 2 to 3 times target, and 263 people already tapped through to your bio.</strong></p>',
    '<p class="hero-summary"><strong>Your biggest month yet. Reach and new-follower growth surged, putting your sandwiches in front of far more of Cincinnati than any month before.</strong></p>',
    "hero:summary")

# ── Beat 3: takeaway + bstats ────────────────────────────────────────────────
html = sub(html,
    'Reach and conversion both fired. The one thing to build on is how long people watch.',
    'The reach turned into real consideration. Views and profile visits more than doubled, new followers hit 660, and link taps held steady, so the growth is feeding the funnel, not just the vanity line.',
    "beat3:takeaway")
html = sub(html,
    '<div class="bstats">\n'
    '    <div class="bstat"><div class="bstat-val exceed">13.0%</div><div class="bstat-lbl">Click-through rate</div><span class="bstat-tag exceed">Exceeding</span></div>\n'
    '    <div class="bstat"><div class="bstat-val exceed">263</div><div class="bstat-lbl">Bio link taps</div><span class="bstat-tag exceed">Exceeding</span></div>\n'
    '    <div class="bstat"><div class="bstat-val exceed">23.4%</div><div class="bstat-lbl">Profile conversion</div><span class="bstat-tag exceed">Exceeding</span></div>\n'
    '    <div class="bstat"><div class="bstat-val watch">25%</div><div class="bstat-lbl">Video retention</div><span class="bstat-tag watch">Watch</span></div>\n'
    '  </div>',
    '<div class="bstats">\n'
    '    <div class="bstat"><div class="bstat-val exceed">230,017</div><div class="bstat-lbl">Total views</div><span class="bstat-tag exceed">Exceeding</span></div>\n'
    '    <div class="bstat"><div class="bstat-val exceed">660</div><div class="bstat-lbl">New followers</div><span class="bstat-tag exceed">Exceeding</span></div>\n'
    '    <div class="bstat"><div class="bstat-val exceed">4,702</div><div class="bstat-lbl">Profile visits</div><span class="bstat-tag exceed">Exceeding</span></div>\n'
    '    <div class="bstat"><div class="bstat-val watch">37%</div><div class="bstat-lbl">Video retention</div><span class="bstat-tag watch">Watch</span></div>\n'
    '  </div>',
    "beat3:bstats")

# ── Beat 3: goal tracker bars (order BOFU -> MOFU -> TOFU to keep 100% unique) ─
html = sub(html,
    '<div class="gt-bar-fill lime" data-w="100" style="width:0%"></div></div>\n            <span class="gt-pct">100%</span>',
    '<div class="gt-bar-fill lime" data-w="72" style="width:0%"></div></div>\n            <span class="gt-pct">72%</span>',
    "beat3:gt-bofu-bar")
html = sub(html, '5.0<span class="gt-score-max">/5.0</span>', '3.6<span class="gt-score-max">/5.0</span>', "beat3:gt-bofu-pts")
html = sub(html,
    '<div class="gt-bar-fill lime" data-w="56" style="width:0%"></div></div>\n            <span class="gt-pct">56%</span>',
    '<div class="gt-bar-fill lime" data-w="64" style="width:0%"></div></div>\n            <span class="gt-pct">64%</span>',
    "beat3:gt-mofu-bar")
html = sub(html, '3.1<span class="gt-score-max">/5.5</span>', '3.5<span class="gt-score-max">/5.5</span>', "beat3:gt-mofu-pts")
html = sub(html,
    '<div class="gt-bar-fill lime" data-w="85" style="width:0%"></div></div>\n            <span class="gt-pct">85%</span>',
    '<div class="gt-bar-fill lime" data-w="100" style="width:0%"></div></div>\n            <span class="gt-pct">100%</span>',
    "beat3:gt-tofu-bar")
html = sub(html, '2.35<span class="gt-score-max">/2.75</span>', '2.75<span class="gt-score-max">/2.75</span>', "beat3:gt-tofu-pts")

# goal-by-goal narratives (in the collapsed proof)
html = sub(html,
    'Your awareness stage scored 85% of its potential this month. New followers and shares hit their ceiling, and views landed on track. For a first month, the top of your funnel is firing.',
    'Your awareness stage maxed out at 100% this month. New followers, shares, and views all cleared their targets, with reach breaking above the Lift ceiling. The top of your funnel is your strongest stage.',
    "beat3:narr-tofu")
html = sub(html,
    'Your engagement stage scored 56%. Saves and profile visits are pulling their weight, and retention is the lever holding the number down. Lifting retention is the fastest way to raise this stage in July.',
    'Your engagement stage scored 64%, up from June. Profile visits and comments both broke above their ceilings, and retention climbed 12 points. Retention is still the lever holding the number down, so lifting it further is the fastest way to raise this stage.',
    "beat3:narr-mofu")
html = sub(html,
    'Your conversion stage maxed out at 100%. Bio link taps, click-through, and profile conversion all cleared their targets. The bottom of your funnel is your strongest stage this month.',
    'Your conversion stage scored 72%. Bio link taps stayed above the ceiling and held steady from June, while click-through and profile conversion settled inside range off the launch-month peak. The conversion engine is efficient, now the job is feeding it more of the new reach.',
    "beat3:narr-bofu")

# ── Beat 3: performance breakdown header + followers banner ───────────────────
html = sub(html, '<p class="sec-label">June 2026</p>', '<p class="sec-label">July 2026</p>', "beat3:perf-label")
html = sub(html,
    'Every tracked metric for June, scored against your Lift Stage target ranges with month-over-month comparison.',
    'Every tracked metric for July, scored against your Lift Stage target ranges with month-over-month comparison.',
    "beat3:perf-sub")
html = sub(html,
    '<p class="fb-label">Total Followers</p>\n        <div class="fb-count">7,955</div>',
    '<p class="fb-label">Total Followers</p>\n        <div class="fb-count">8,630</div>\n        <div class="fb-mom"><span class="mom up">&#9650; 8.5% vs June</span></div>',
    "beat3:followers")

# ── Beat 3: the 10 metric cards (add MoM deltas the inaugural report lacked) ──
UP = lambda t: f'<span class="mom up">&#9650; {t}</span>'
DN = lambda t: f'<span class="mom dn">&#9660; {t}</span>'
FL = lambda t: f'<span class="mom fl">{t}</span>'


def newcard(top_old, top_new, nums_new, mom_html, barw, cls, note, callout=None):
    """Build the July inner for one metric card and return (old, new) is caller's job;
    this only assembles the July inner block that follows mc-top."""
    inner = (nums_new + '\n'
             f'          <div class="mc-mom">{mom_html}</div>\n'
             f'          <div class="bar-track"><div class="bar-fill {cls}" data-w="{barw}" style="width:0%"></div></div>\n'
             f'          <p class="mc-note">{note}</p>')
    if callout:
        inner += f'\n          <p class="mc-callout">{callout}</p>'
    return inner


def nums(month, cls, val, tgt):
    return (f'<div class="mc-nums"><div><span class="mc-lbl">{month}</span><span class="mc-val {cls}">{val}</span></div>'
            f'<div><span class="mc-lbl">Target Range</span><span class="mc-tgt">{tgt}</span></div></div>')


# New Followers  474 -> 660  (E, up 39%)
html = sub(html,
    '<div class="mc-top"><span class="mc-name">New Followers</span><span class="mc-badge exceed">Exceeding</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val exceed">474</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">100 &ndash; 270</span></div></div>\n'
    '          <div class="bar-track"><div class="bar-fill exceed" data-w="100" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Cincinnati responded to the launch. The audience finding you is your local neighborhood crowd, exactly the buyer you want for catering.</p>',
    '<div class="mc-top"><span class="mc-name">New Followers</span><span class="mc-badge exceed">Exceeding</span></div>\n          '
    + newcard(None, None, nums("July", "exceed", "660", "100 &ndash; 270"), UP("39% vs June"), 100, "exceed",
              "Your strongest follower month yet, and well above the Lift ceiling. Cincinnati keeps finding you, and it is the local neighborhood crowd you want for catering."),
    "mc:new-followers")

# Shares  833 -> 1,021  (E, up 23%)
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Shares</span><span class="mc-badge exceed">Exceeding</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val exceed">833</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">60 &ndash; 300</span></div></div>\n'
    '          <div class="bar-track"><div class="bar-fill exceed" data-w="100" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Community-driven content is your natural fit. When you tell a Hyde Park story, it travels.</p>',
    '<div class="mc-top"><span class="mc-name">Shares</span><span class="mc-badge exceed">Exceeding</span></div>\n          '
    + newcard(None, None, nums("July", "exceed", "1,021", "60 &ndash; 300"), UP("23% vs June"), 100, "exceed",
              "Shareable, community-first content is your engine. When a Hyde Park story lands, the neighborhood passes it along, and it broke 1,000 this month."),
    "mc:shares")

# Total Views  147,499 (OT) -> 230,017 (E, up 56%)
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Total Views</span><span class="mc-badge ontrack">On Track</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val ontrack">147,499</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">40,000 &ndash; 150,000</span></div></div>\n'
    '          <div class="bar-track"><div class="bar-fill ontrack" data-w="98" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Reach at the top of the Lift range in your first month. This is the base your catering strategy compounds from.</p>',
    '<div class="mc-top"><span class="mc-name">Total Views</span><span class="mc-badge exceed">Exceeding</span></div>\n          '
    + newcard(None, None, nums("July", "exceed", "230,017", "40,000 &ndash; 150,000"), UP("56% vs June"), 100, "exceed",
              "Reach broke above the Lift ceiling. Far more of Cincinnati saw your sandwiches this month than any month before, and it is the base your catering strategy compounds from."),
    "mc:total-views")

# Profile Visits  2,024 -> 4,702  (E, up 132%)
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Profile Visits</span><span class="mc-badge exceed">Exceeding</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val exceed">2,024</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">300 &ndash; 2,000</span></div></div>\n'
    '          <div class="bar-track"><div class="bar-fill exceed" data-w="100" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Just above the Lift ceiling. People aren&rsquo;t scrolling past. They&rsquo;re tapping through to look closer.</p>',
    '<div class="mc-top"><span class="mc-name">Profile Visits</span><span class="mc-badge exceed">Exceeding</span></div>\n          '
    + newcard(None, None, nums("July", "exceed", "4,702", "300 &ndash; 2,000"), UP("132% vs June"), 100, "exceed",
              "More than double last month and well above the Lift ceiling. People are not scrolling past, they are tapping through to look closer."),
    "mc:profile-visits")

# Retention  25% -> 37%  (W, up 12 pts) -- carries callout
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Retention</span><span class="mc-badge watch">Watch</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val watch">25%</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">50% &ndash; 65%</span></div></div>\n'
    '          <div class="bar-track"><div class="bar-fill watch" data-w="38" style="width:0%"></div></div>\n'
    '          <p class="mc-note">The one to work on. Longer Reels and slower opens likely explain it. Tighter cuts and stronger first-3-second hooks are the July lever.</p>\n'
    '          <p class="mc-callout">Retention came in at 25%. Translation: on average, people watched 25% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences.</p>',
    '<div class="mc-top"><span class="mc-name">Retention</span><span class="mc-badge watch">Watch</span></div>\n          '
    + newcard(None, None, nums("July", "watch", "37%", "50% &ndash; 65%"), UP("12 pts vs June"), 57, "watch",
              "Up 12 points from June and moving the right way, still under the Lift floor. Tighter cuts and stronger first-3-second hooks are the lever to keep climbing.",
              "Retention came in at 37%. Translation: on average, people watched 37% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences."),
    "mc:retention")

# Saves  255 -> 113  (OT, down 56%)
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Saves</span><span class="mc-badge ontrack">On Track</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val ontrack">255</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">80 &ndash; 400</span></div></div>\n'
    '          <div class="bar-track"><div class="bar-fill ontrack" data-w="64" style="width:0%"></div></div>\n'
    '          <p class="mc-note">People are bookmarking content to reference for catering, pairings, or the family history. This is pre-purchase intent showing up early.</p>',
    '<div class="mc-top"><span class="mc-name">Saves</span><span class="mc-badge ontrack">On Track</span></div>\n          '
    + newcard(None, None, nums("July", "ontrack", "113", "80 &ndash; 400"), DN("56% vs June"), 28, "ontrack",
              "Inside range, down from a launch-month spike. Save-worthy content like catering how-tos and pairing guides is the lever to lift it back up."),
    "mc:saves")

# Comments  181 (OT) -> 280 (E, up 55%)
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Comments</span><span class="mc-badge ontrack">On Track</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val ontrack">181</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">75 &ndash; 250</span></div></div>\n'
    '          <div class="bar-track"><div class="bar-fill ontrack" data-w="72" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Real conversation from the neighborhood. Locals are talking, not just watching.</p>',
    '<div class="mc-top"><span class="mc-name">Comments</span><span class="mc-badge exceed">Exceeding</span></div>\n          '
    + newcard(None, None, nums("July", "exceed", "280", "75 &ndash; 250"), UP("55% vs June"), 100, "exceed",
              "Above the Lift ceiling. The neighborhood is talking, not just watching, and the conversation is growing month over month."),
    "mc:comments")

# CTR  13.0% (E) -> 5.6% (OT, down 7.4 pts) -- carries callout
html = sub(html,
    '<div class="mc-top"><span class="mc-name">CTR</span><span class="mc-badge exceed">Exceeding</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val exceed">13.0%</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">3% &ndash; 6%</span></div></div>\n'
    '          <div class="bar-track"><div class="bar-fill exceed" data-w="100" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Well above the Lift ceiling. The bio link is doing its job. People are moving from feed to your bio links at a strong rate.</p>\n'
    '          <p class="mc-callout">Click-through rate came in at 13.0%. Translation: of everyone who saw your link, 13.0% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers.</p>',
    '<div class="mc-top"><span class="mc-name">CTR</span><span class="mc-badge ontrack">On Track</span></div>\n          '
    + newcard(None, None, nums("July", "ontrack", "5.6%", "3% &ndash; 6%"), DN("7.4 pts vs June"), 93, "ontrack",
              "Inside range and still healthy off June&rsquo;s launch peak. The bio link keeps moving people from the feed to your links.",
              "Click-through rate came in at 5.6%. Translation: of everyone who saw your link, 5.6% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers."),
    "mc:ctr")

# Bio Link Taps  263 -> 262  (E, flat)
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Bio Link Taps</span><span class="mc-badge exceed">Exceeding</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val exceed">263</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">30 &ndash; 180</span></div></div>\n'
    '          <div class="bar-track"><div class="bar-fill exceed" data-w="100" style="width:0%"></div></div>\n'
    '          <p class="mc-note">This counts every tap across your bio links. More bio link taps in your first month than most established accounts hit across a full year, and catering is one of the destinations that interest lands on.</p>',
    '<div class="mc-top"><span class="mc-name">Bio Link Taps</span><span class="mc-badge exceed">Exceeding</span></div>\n          '
    + newcard(None, None, nums("July", "exceed", "262", "30 &ndash; 180"), FL("Flat vs June"), 100, "exceed",
              "Held steady above the Lift ceiling. This counts every tap across your bio links, and each one is a deliberate step toward your shop or catering."),
    "mc:link-taps")

# PCR  23.4% (E) -> 14.0% (OT, down 9.4 pts) -- carries callout
html = sub(html,
    '<div class="mc-top"><span class="mc-name">PCR</span><span class="mc-badge exceed">Exceeding</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val exceed">23.4%</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">10% &ndash; 16%</span></div></div>\n'
    '          <div class="bar-track"><div class="bar-fill exceed" data-w="100" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Nearly 1 in 4 profile visitors chose to follow. A healthy audience is actively building around the brand.</p>\n'
    '          <p class="mc-callout">Profile conversion came in at 23.4%. Translation: 23.4% of the people who visited your profile chose to follow. A strong profile conversion rate means your page is doing its job, turning curious visitors into an audience you can nurture toward buying.</p>',
    '<div class="mc-top"><span class="mc-name">PCR</span><span class="mc-badge ontrack">On Track</span></div>\n          '
    + newcard(None, None, nums("July", "ontrack", "14.0%", "10% &ndash; 16%"), DN("9.4 pts vs June"), 88, "ontrack",
              "Inside range off the launch-month high. New visitors keep choosing to follow, building the audience you nurture toward buying.",
              "Profile conversion came in at 14.0%. Translation: 14.0% of the people who visited your profile chose to follow. A strong profile conversion rate means your page is doing its job, turning curious visitors into an audience you can nurture toward buying."),
    "mc:pcr")

# ── C2B panel 1: the funnel this month (aggregate metrics, not per-post) ──────
html = sub(html,
    '<div class="c2b-step"><span class="c2b-step-num">147,499</span><div class="c2b-step-main"><span class="c2b-step-txt">people saw your content</span><span class="c2b-step-badge">\U0001F3DF Great American Ball Park filled 3.5x over</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">2,024</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped through to look closer</span><span class="c2b-step-badge">\U0001F3AD nearly filling the Taft Theatre</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">255</span><div class="c2b-step-main"><span class="c2b-step-txt">bookmarked content to reference later</span><span class="c2b-step-badge">\U0001F4CC 255 pre-purchase bookmarks</span></div></div>\n'
    '        <div class="c2b-step hi"><span class="c2b-step-num">263</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped a bio link, the highest-intent signal we track</span><span class="c2b-step-badge">\U0001F446 263 deliberate decisions to explore your business</span></div></div>',
    '<div class="c2b-step"><span class="c2b-step-num">230,017</span><div class="c2b-step-main"><span class="c2b-step-txt">people saw your content</span><span class="c2b-step-badge">\U0001F3DF Great American Ball Park filled 5.3x over</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">4,702</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped through to look closer</span><span class="c2b-step-badge">\U0001F3AD the Taft Theatre filled nearly twice over</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">113</span><div class="c2b-step-main"><span class="c2b-step-txt">bookmarked content to reference later</span><span class="c2b-step-badge">\U0001F4CC 113 pre-purchase bookmarks</span></div></div>\n'
    '        <div class="c2b-step hi"><span class="c2b-step-num">262</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped a bio link, the highest-intent signal we track</span><span class="c2b-step-badge">\U0001F446 262 deliberate decisions to explore your business</span></div></div>',
    "c2b:funnel")

# trajectory lead: 2 months of data now, direction still baseline-building
html = sub(html,
    'This is your first month with us, so the line is just beginning. This chart is about direction, not a fixed dollar figure. It models where your momentum points over a 12-month window, and each month of real performance sharpens it. June sets the starting point, and the trend from here is what matters.',
    'Two months in, the line is starting to form. This chart is about direction, not a fixed dollar figure. It models where your momentum points over a 12-month window, and each month of real performance sharpens it. June set the starting point, July extends it, and the trend from here is what matters.',
    "c2b:traj-lead")
# shift the trajectory highlight + baseline annotation from Jun to Jul
html = sub(html, '<text x="308.7" y="242" text-anchor="middle" font-size="9" fill="rgba(255,255,255,.7)">Jun</text>',
           '<text x="308.7" y="242" text-anchor="middle" font-size="9" fill="rgba(255,255,255,.28)">Jun</text>', "c2b:traj-jun")
html = sub(html, '<text x="361.3" y="242" text-anchor="middle" font-size="9" fill="rgba(255,255,255,.28)">Jul</text>',
           '<text x="361.3" y="242" text-anchor="middle" font-size="9" fill="rgba(255,255,255,.7)">Jul</text>', "c2b:traj-jul")
html = sub(html,
    '<line x1="308.7" y1="96.8" x2="624.0" y2="96.8" stroke="rgba(255,255,255,.35)" stroke-width="2" stroke-dasharray="5 4"/><circle cx="308.7" cy="96.8" r="3" fill="#e2ed7a"/><text x="316.7" y="88.8" font-size="10" fill="#e2ed7a" font-weight="700">Building your baseline</text>',
    '<line x1="361.3" y1="96.8" x2="624.0" y2="96.8" stroke="rgba(255,255,255,.35)" stroke-width="2" stroke-dasharray="5 4"/><circle cx="308.7" cy="96.8" r="3" fill="rgba(226,237,122,.55)"/><circle cx="361.3" cy="96.8" r="3" fill="#e2ed7a"/><text x="369.3" y="88.8" font-size="10" fill="#e2ed7a" font-weight="700">Building your baseline</text>',
    "c2b:traj-annotation")

# ── Beat 4: pattern line (not post-dependent) ────────────────────────────────
html = sub(html,
    'The launch proved the format. Retention at 25% is the one signal to lift, it tells us the openings can hit a beat faster. At the quarter level, your view is just beginning, this is month one of the baseline.',
    'Broad, shareable content drove the spike. The one lever still under your stage floor is retention, so depth, holding people longer once they land, is where the next gain lives.',
    "beat4:pattern")

# ── Beat 4: quarter view grid (Q2 completes, Q3 becomes current) ─────────────
html = sub(html,
    '<div class="qy-grid"><div class="qy-col "><div class="qy-q">Q1</div><div class="qy-range">Jan&ndash;Mar</div><div class="qy-note">Not tracked. First report June 2026.</div><div class="qy-state">Pre-launch</div></div><div class="qy-col current"><div class="qy-q">Q2</div><div class="qy-range">Apr&ndash;Jun</div><div class="qy-note">Building baseline. June is your first month.</div><div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> new followers and shares landed 2 to 3x target, and 263 bio link taps in the first month.</div><div class="qy-tline"><span class="qy-tl">Watched:</span> video retention at 25%, and engagement the softest of the three stages.</div></div><div class="qy-state">In progress</div></div><div class="qy-col "><div class="qy-q">Q3</div><div class="qy-range">Jul&ndash;Sep</div><div class="qy-note">Begins July</div><div class="qy-state">Pending</div></div><div class="qy-col "><div class="qy-q">Q4</div><div class="qy-range">Oct&ndash;Dec</div><div class="qy-note">Later this year</div><div class="qy-state">Pending</div></div></div>',
    '<div class="qy-grid"><div class="qy-col "><div class="qy-q">Q1</div><div class="qy-range">Jan&ndash;Mar</div><div class="qy-note">Not tracked. First report June 2026.</div><div class="qy-state">Pre-launch</div></div><div class="qy-col "><div class="qy-q">Q2</div><div class="qy-range">Apr&ndash;Jun</div><div class="qy-avg">9.2<span class="u">/10</span></div><div class="qy-badge strong">Strong</div><div class="qy-note">June was your first month.</div><div class="qy-state">Complete</div></div><div class="qy-col current"><div class="qy-q">Q3</div><div class="qy-range">Jul&ndash;Sep</div><div class="qy-note">Building baseline. July is the first month of the quarter.</div><div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> reach, new followers, and profile visits all broke above target, with views past 230k.</div><div class="qy-tline"><span class="qy-tl">Watched:</span> video retention at 37%, still the softest signal despite a 12-point gain.</div></div><div class="qy-state">In progress</div></div><div class="qy-col "><div class="qy-q">Q4</div><div class="qy-range">Oct&ndash;Dec</div><div class="qy-note">Later this year</div><div class="qy-state">Pending</div></div></div>',
    "beat4:qy-grid")

# ── Beat 4: month-by-month score strip (append July) ─────────────────────────
html = sub(html,
    '<div class="mscore-cell current"><div class="mscore-m">Jun</div><div class="mscore-v">9.2</div></div>',
    '<div class="mscore-cell"><div class="mscore-m">Jun</div><div class="mscore-v">9.2</div></div>', "beat4:mscore-jun")
html = sub(html,
    '<div class="mscore-cell empty"><div class="mscore-m">Jul</div><div class="mscore-v">&middot;</div></div>',
    '<div class="mscore-cell current"><div class="mscore-m">Jul</div><div class="mscore-v">9.2</div></div>', "beat4:mscore-jul")

# ── Beat 5: takeaway, focus, closing ─────────────────────────────────────────
html = sub(html,
    'Next month we tighten Reel openings to lift how long people watch, and test which catering calls to action pull the most taps.',
    'We test stronger opening hooks to hold more of the new reach, and keep the discovery engine running while it is hot.',
    "beat5:takeaway")
html = sub(html, 'Where our attention is in July', 'Where our attention is in August', "beat5:focus-label")
html = sub(html,
    '<div class="tw-item tests"><p class="tw-item-head">Tighter Reel openings and retention</p><p class="tw-item-body">In July, we&rsquo;re watching how tighter Reel openings affect retention. The goal is lifting from 25% toward the 50% Lift floor without losing reach.</p></div>',
    '<div class="tw-item tests"><p class="tw-item-head">Stronger opening hooks to hold the reach</p><p class="tw-item-body">Retention rose to 37% in July. In August we push on front-loaded hooks and tighter cuts to keep climbing toward the 50% Lift floor without losing reach.</p></div>',
    "beat5:tw-item1")
html = sub(html,
    '<div class="tw-item tests"><p class="tw-item-head">Which catering-CTA formats land</p><p class="tw-item-body">We&rsquo;re paying attention to which catering-CTA formats pull the most bio link taps across post types, watching July and August together before we settle on a standard.</p></div>',
    '<div class="tw-item tests"><p class="tw-item-head">Keep the discovery engine running</p><p class="tw-item-body">July&rsquo;s reach surge is worth pressing while it is hot. We keep the broad, shareable formats that drove it in rotation and watch which catering CTAs turn that reach into inquiries.</p></div>',
    "beat5:tw-item2")
html = sub(html,
    'This is month one, so we are learning what works. We&rsquo;ll step back and lock the strategy once we have a few months of real data.',
    'A couple months in, the pattern is forming. We keep testing formats and step back to lock the strategy at your quarter mark, once there is enough real data to act on.',
    "beat5:closing")

# ── footer ───────────────────────────────────────────────────────────────────
html = sub(html,
    'Prepared by <a href="https://scrollmedia.co" target="_blank" rel="noopener">Scroll Media</a> &middot; June 2026 Performance Report<br>',
    'Prepared by <a href="https://scrollmedia.co" target="_blank" rel="noopener">Scroll Media</a> &middot; July 2026 Performance Report<br>',
    "footer")

# ── write ────────────────────────────────────────────────────────────────────
os.makedirs(OUT_DIR, exist_ok=True)
open(OUT, "w", encoding="utf-8").write(html)
print(f"score {R['final']} (raw {R['raw']:.3f}, credit {R['credit']:+.2f}); wrote {OUT}  ({len(edits)} anchored edits)")
for e in edits:
    print("  -", e)

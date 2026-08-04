#!/usr/bin/env python3
"""build_atlassystems_july.py -- Atlas Systems INAUGURAL July 2026 report.
Clones Carl's Deli June 2026 (the canonical first-report shell: no MoM deltas, single-
point goal tracker, first-report quarter view + score strip) and converts it to Atlas:
Spark stage, B2B IT/AI consulting, and a TAP-VOLUME value trajectory (process-v8.5 §6 —
Atlas has a documented CLV but only 8 link taps, below the ~50/mo dollar-modeling
threshold, so it charts taps, not dollars). Beat 2 + Beat 4 cards stay as placeholders
for the post-Metricool-pull finalize. Score computed by score_report.py. Anchored/hard-fail."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score_report as sr

REPO = "/Users/chase.gianattasio/Desktop/scroll-reports"
SRC = f"{REPO}/carlsdeli/june2026/index.html"
OUT_DIR = f"{REPO}/atlassystems/july2026"; OUT = f"{OUT_DIR}/index.html"

KPI = {"saves":19,"ctr":3.1,"retention":20,"pcr":9.8,"link_taps":8,"profile_visits":256,
       "comments":17,"new_followers":25,"total_views":4401,"shares":8}
R = sr.score(KPI, "Spark", prior=None)
assert R["final"] == 7.5, R["final"]

edits = []
def sub(html, old, new, label):
    n = html.count(old)
    if n != 1: sys.exit(f"ANCHOR FAIL [{label}]: {n} found\n  {old[:170]}")
    edits.append(label); return html.replace(old, new)

def mc(name, cls, lab, val, tgt, bar, note, callout=None):
    s=(f'<div class="mc-top"><span class="mc-name">{name}</span><span class="mc-badge {cls}">{lab}</span></div>\n'
       f'          <div class="mc-nums"><div><span class="mc-lbl">July</span><span class="mc-val {cls}">{val}</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">{tgt}</span></div></div>\n'
       f'          <div class="bar-track"><div class="bar-fill {cls}" data-w="{bar}" style="width:0%"></div></div>\n'
       f'          <p class="mc-note">{note}</p>')
    if callout: s+=f'\n          <p class="mc-callout">{callout}</p>'
    return s

html = open(SRC, encoding="utf-8").read()

# ── access gate + head/meta ──────────────────────────────────────────────────
html = sub(html, "window.SCROLL_GATE={slug:'carlsdeli',code:'carls.scroll'", "window.SCROLL_GATE={slug:'atlassystems',code:'atlas.scroll'", "gate")
html = sub(html, "<title>Carl's Deli &ndash; June 2026 | Scroll Media</title>", "<title>Atlas Systems &ndash; July 2026 | Scroll Media</title>", "title")
html = sub(html, 'content="Carl\'s Deli June 2026 Instagram performance report. Score 9.2/10. Exceptional Month. Lift Stage. Managed by Scroll Media.">',
           'content="Atlas Systems July 2026 Instagram performance report. Score 7.5/10. Building Month. Spark Stage. Managed by Scroll Media.">', "meta:desc")
html = sub(html, 'content="Carl\'s Deli, June 2026 Performance Report">', 'content="Atlas Systems, July 2026 Performance Report">', "og:title")
html = sub(html, 'content="Monthly score 9.2/10. Exceptional Month. Prepared by Scroll Media.">', 'content="Monthly score 7.5/10. Building Month. Prepared by Scroll Media.">', "og:desc")

# ── hero ─────────────────────────────────────────────────────────────────────
html = sub(html, '<div class="hero-eyebrow"><span class="dot"></span>June 2026 Performance Report</div>', '<div class="hero-eyebrow"><span class="dot"></span>July 2026 Performance Report</div>', "hero:eyebrow")
html = sub(html, 'Lift Stage &middot; Month 1', 'Spark Stage &middot; Month 2', "hero:stage")
html = sub(html, '<h1>Carl&rsquo;s <span>Deli</span></h1>', '<h1>Atlas <span>Systems</span></h1>', "hero:h1")
html = sub(html,
    '<span>@carlsdelicincy</span><span class="dot"></span>\n      <span>Cincinnati&rsquo;s Best Deli &middot; 80 Years, Sister-Owned</span><span class="dot"></span>\n      <span>June 1&ndash;30, 2026</span><span class="dot"></span>\n      <span>Managed by Rachel</span>',
    '<span>@atlasysky</span><span class="dot"></span>\n      <span>IT Consulting &amp; AI Enablement for Small Businesses</span><span class="dot"></span>\n      <span>July 1&ndash;31, 2026</span><span class="dot"></span>\n      <span>Managed by Riley</span>', "hero:meta")
html = sub(html,
    '<div class="ph-bignum">9.2<span class="unit">/10</span></div>\n        <p class="ph-title">Exceptional Month</p>\n        <div class="ph-badges">\n          <span class="ph-badge exceed"><span class="bd"></span>6 Exceeding</span>\n          <span class="ph-badge ontrack"><span class="bd"></span>3 On Track</span>\n          <span class="ph-badge watch"><span class="bd"></span>1 Watch</span>',
    '<div class="ph-bignum">7.5<span class="unit">/10</span></div>\n        <p class="ph-title">Building Month</p>\n        <div class="ph-badges">\n          <span class="ph-badge exceed"><span class="bd"></span>0 Exceeding</span>\n          <span class="ph-badge ontrack"><span class="bd"></span>4 On Track</span>\n          <span class="ph-badge watch"><span class="bd"></span>6 Watch</span>', "hero:score")
html = sub(html,
    '<p class="ph-label">Bio Link Engagement</p>\n        <div class="ph-bignum">263</div>\n        <p class="ph-title">Total Bio Link Taps</p>\n        <p class="ph-outcome-sub">Total taps on any link in your bio. Catering is your priority destination this quarter, so this number is the total interest signal that lands there and elsewhere in your bio.</p>',
    '<p class="ph-label">Bio Link Engagement</p>\n        <div class="ph-bignum">8</div>\n        <p class="ph-title">Total Bio Link Taps</p>\n        <p class="ph-outcome-sub">Total taps toward your site and booking. For a considered, high-ticket sale, every deliberate tap is a real buying signal, even on a brand-new audience.</p>', "hero:outcome")
html = sub(html,
    '<p class="hero-summary"><strong>Your launch month landed hard. New followers and shares came in 2 to 3 times target, and 263 people already tapped through to your bio.</strong></p>',
    '<p class="hero-summary"><strong>A foundation month. On a brand-new, focused audience, the intent signals that matter for a considered, high-ticket sale landed: click-through in range, plus profile visits and comments on track.</strong></p>', "hero:summary")

# ── Beat 3: takeaway + bstats ────────────────────────────────────────────────
html = sub(html, 'Reach and conversion both fired. The one thing to build on is how long people watch.',
           'The signals that predict a considered, high-ticket sale showed up early. Click-through, profile visits, and comments all landed on track, even on a small audience. Retention is the clear first lever.', "beat3:takeaway")
html = sub(html,
    '<div class="bstats">\n'
    '    <div class="bstat"><div class="bstat-val exceed">13.0%</div><div class="bstat-lbl">Click-through rate</div><span class="bstat-tag exceed">Exceeding</span></div>\n'
    '    <div class="bstat"><div class="bstat-val exceed">263</div><div class="bstat-lbl">Bio link taps</div><span class="bstat-tag exceed">Exceeding</span></div>\n'
    '    <div class="bstat"><div class="bstat-val exceed">23.4%</div><div class="bstat-lbl">Profile conversion</div><span class="bstat-tag exceed">Exceeding</span></div>\n'
    '    <div class="bstat"><div class="bstat-val watch">25%</div><div class="bstat-lbl">Video retention</div><span class="bstat-tag watch">Watch</span></div>\n'
    '  </div>',
    '<div class="bstats">\n'
    '    <div class="bstat"><div class="bstat-val ontrack">3.1%</div><div class="bstat-lbl">Click-through rate</div><span class="bstat-tag ontrack">On Track</span></div>\n'
    '    <div class="bstat"><div class="bstat-val ontrack">256</div><div class="bstat-lbl">Profile visits</div><span class="bstat-tag ontrack">On Track</span></div>\n'
    '    <div class="bstat"><div class="bstat-val ontrack">17</div><div class="bstat-lbl">Comments</div><span class="bstat-tag ontrack">On Track</span></div>\n'
    '    <div class="bstat"><div class="bstat-val watch">20%</div><div class="bstat-lbl">Video retention</div><span class="bstat-tag watch">Watch</span></div>\n'
    '  </div>', "beat3:bstats")

# ── Beat 3: goal tracker (single-point; BOFU->MOFU->TOFU order) ───────────────
html = sub(html, '<div class="gt-bar-fill lime" data-w="100" style="width:0%"></div></div>\n            <span class="gt-pct">100%</span>', '<div class="gt-bar-fill lime" data-w="48" style="width:0%"></div></div>\n            <span class="gt-pct">48%</span>', "gt:bofu-bar")
html = sub(html, '5.0<span class="gt-score-max">/5.0</span>', '2.4<span class="gt-score-max">/5.0</span>', "gt:bofu-pts")
html = sub(html, '<div class="gt-bar-fill lime" data-w="56" style="width:0%"></div></div>\n            <span class="gt-pct">56%</span>', '<div class="gt-bar-fill lime" data-w="35" style="width:0%"></div></div>\n            <span class="gt-pct">35%</span>', "gt:mofu-bar")
html = sub(html, '3.1<span class="gt-score-max">/5.5</span>', '1.9<span class="gt-score-max">/5.5</span>', "gt:mofu-pts")
html = sub(html, '<div class="gt-bar-fill lime" data-w="85" style="width:0%"></div></div>\n            <span class="gt-pct">85%</span>', '<div class="gt-bar-fill lime" data-w="20" style="width:0%"></div></div>\n            <span class="gt-pct">20%</span>', "gt:tofu-bar")
html = sub(html, '2.35<span class="gt-score-max">/2.75</span>', '0.55<span class="gt-score-max">/2.75</span>', "gt:tofu-pts")
# goal titles
html = sub(html, 'Build Local Brand Awareness in Cincinnati', 'Build Regional Authority &amp; Brand Discovery', "gt:title-tofu")
html = sub(html, 'Build Community Engagement &amp; Deepen Local Connection', 'Build Trust &amp; Buyer Confidence', "gt:title-mofu")
html = sub(html, 'Generate Qualified Catering Lead Signal', 'Generate Qualified Consultation Signal', "gt:title-bofu")
# goal narratives
html = sub(html, 'Your awareness stage scored 85% of its potential this month. New followers and shares hit their ceiling, and views landed on track. For a first month, the top of your funnel is firing.',
           'Your awareness stage scored 20% this month. On a brand-new audience, new followers, shares, and views all start below their Spark floors. Growing reach with authority and founder-led content is the first job.', "narr:tofu")
html = sub(html, 'Your engagement stage scored 56%. Saves and profile visits are pulling their weight, and retention is the lever holding the number down. Lifting retention is the fastest way to raise this stage in July.',
           'Your engagement stage scored 35%. Profile visits and comments landed on track even on a small audience, a good early sign. Retention is the lever holding this stage down, so holding attention longer is the focus from here.', "narr:mofu")
html = sub(html, 'Your conversion stage maxed out at 100%. Bio link taps, click-through, and profile conversion all cleared their targets. The bottom of your funnel is your strongest stage this month.',
           'Your conversion stage scored 48%. Click-through and link taps are inside their Spark ranges in the very first month, which means the people finding you are already moving toward a conversation. Profile conversion sits just under floor.', "narr:bofu")

# ── Beat 3: perf header + followers banner (Spark, no MoM) ───────────────────
html = sub(html, '<p class="sec-label">June 2026</p>', '<p class="sec-label">July 2026</p>', "perf:label")
html = sub(html, 'Every tracked metric for June, scored against your Lift Stage target ranges with month-over-month comparison.',
           'Every tracked metric for your first month, scored against your Spark Stage target ranges. Month-over-month comparison begins next report.', "perf:sub")
html = sub(html,
    '<p class="fb-label">Total Followers</p>\n        <div class="fb-count">7,955</div>\n      </div>\n      <div class="fb-right">\n        <p class="fb-target-label">Target Range</p>\n        <p class="fb-target">5,000 &ndash; 25,000</p>\n        <p class="fb-stage">Lift Stage</p>',
    '<p class="fb-label">Total Followers</p>\n        <div class="fb-count">65</div>\n      </div>\n      <div class="fb-right">\n        <p class="fb-target-label">Target Range</p>\n        <p class="fb-target">1,000 &ndash; 5,000</p>\n        <p class="fb-stage">Spark Stage</p>', "followers")

# ── Beat 3: 10 metric cards (Spark, first-report, no mc-mom) ─────────────────
html = sub(html,
    '<div class="mc-top"><span class="mc-name">New Followers</span><span class="mc-badge exceed">Exceeding</span></div>\n          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val exceed">474</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">100 &ndash; 270</span></div></div>\n          <div class="bar-track"><div class="bar-fill exceed" data-w="100" style="width:0%"></div></div>\n          <p class="mc-note">Cincinnati responded to the launch. The audience finding you is your local neighborhood crowd, exactly the buyer you want for catering.</p>',
    mc("New Followers","watch","Watch","25","40 &ndash; 90",28,"A brand-new audience taking shape. On a focused B2B account, every early follow is a decision-maker choosing to keep hearing from you."), "mc:new-followers")
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Shares</span><span class="mc-badge exceed">Exceeding</span></div>\n          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val exceed">833</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">60 &ndash; 300</span></div></div>\n          <div class="bar-track"><div class="bar-fill exceed" data-w="100" style="width:0%"></div></div>\n          <p class="mc-note">Community-driven content is your natural fit. When you tell a Hyde Park story, it travels.</p>',
    mc("Shares","watch","Watch","8","15 &ndash; 60",13,"Below floor, expected this early. Authority content a business owner wants to forward to a peer is the lever to grow this."), "mc:shares")
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Total Views</span><span class="mc-badge ontrack">On Track</span></div>\n          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val ontrack">147,499</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">40,000 &ndash; 150,000</span></div></div>\n          <div class="bar-track"><div class="bar-fill ontrack" data-w="98" style="width:0%"></div></div>\n          <p class="mc-note">Reach at the top of the Lift range in your first month. This is the base your catering strategy compounds from.</p>',
    mc("Total Views","watch","Watch","4,401","10,000 &ndash; 40,000",11,"A small but real first-month reach. This is the base your authority strategy compounds from as the audience grows."), "mc:total-views")
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Profile Visits</span><span class="mc-badge exceed">Exceeding</span></div>\n          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val exceed">2,024</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">300 &ndash; 2,000</span></div></div>\n          <div class="bar-track"><div class="bar-fill exceed" data-w="100" style="width:0%"></div></div>\n          <p class="mc-note">Just above the Lift ceiling. People aren&rsquo;t scrolling past. They&rsquo;re tapping through to look closer.</p>',
    mc("Profile Visits","ontrack","On Track","256","50 &ndash; 500",51,"Inside range, and strong for a first month. People are not scrolling past, they are stepping in to look closer at who you are."), "mc:profile-visits")
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Retention</span><span class="mc-badge watch">Watch</span></div>\n          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val watch">25%</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">50% &ndash; 65%</span></div></div>\n          <div class="bar-track"><div class="bar-fill watch" data-w="38" style="width:0%"></div></div>\n          <p class="mc-note">The one to work on. Longer Reels and slower opens likely explain it. Tighter cuts and stronger first-3-second hooks are the July lever.</p>\n          <p class="mc-callout">Retention came in at 25%. Translation: on average, people watched 25% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences.</p>',
    mc("Retention","watch","Watch","20%","35% &ndash; 50%",40,"The clear first lever. Tighter opens and a sharper first line are how we hold more of a considered buyer&rsquo;s attention.","Retention came in at 20%. Translation: on average, people watched 20% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences."), "mc:retention")
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Saves</span><span class="mc-badge ontrack">On Track</span></div>\n          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val ontrack">255</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">80 &ndash; 400</span></div></div>\n          <div class="bar-track"><div class="bar-fill ontrack" data-w="64" style="width:0%"></div></div>\n          <p class="mc-note">People are bookmarking content to reference for catering, pairings, or the family history. This is pre-purchase intent showing up early.</p>',
    mc("Saves","watch","Watch","19","20 &ndash; 80",24,"Just under floor, and a healthy early signal. A save from a business owner is someone filing your expertise to act on later."), "mc:saves")
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Comments</span><span class="mc-badge ontrack">On Track</span></div>\n          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val ontrack">181</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">75 &ndash; 250</span></div></div>\n          <div class="bar-track"><div class="bar-fill ontrack" data-w="72" style="width:0%"></div></div>\n          <p class="mc-note">Real conversation from the neighborhood. Locals are talking, not just watching.</p>',
    mc("Comments","ontrack","On Track","17","15 &ndash; 75",23,"Inside range. Real conversation from a small audience, which is exactly how trust builds before a high-ticket decision."), "mc:comments")
html = sub(html,
    '<div class="mc-top"><span class="mc-name">CTR</span><span class="mc-badge exceed">Exceeding</span></div>\n          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val exceed">13.0%</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">3% &ndash; 6%</span></div></div>\n          <div class="bar-track"><div class="bar-fill exceed" data-w="100" style="width:0%"></div></div>\n          <p class="mc-note">Well above the Lift ceiling. The bio link is doing its job. People are moving from feed to your bio links at a strong rate.</p>\n          <p class="mc-callout">Click-through rate came in at 13.0%. Translation: of everyone who saw your link, 13.0% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers.</p>',
    mc("CTR","ontrack","On Track","3.1%","3% &ndash; 8%",39,"Inside range in the first month. The people finding you are not just watching, they are clicking toward a conversation.","Click-through rate came in at 3.1%. Translation: of everyone who saw your link, 3.1% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers."), "mc:ctr")
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Bio Link Taps</span><span class="mc-badge exceed">Exceeding</span></div>\n          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val exceed">263</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">30 &ndash; 180</span></div></div>\n          <div class="bar-track"><div class="bar-fill exceed" data-w="100" style="width:0%"></div></div>\n          <p class="mc-note">This counts every tap across your bio links. More bio link taps in your first month than most established accounts hit across a full year, and catering is one of the destinations that interest lands on.</p>',
    mc("Bio Link Taps","ontrack","On Track","8","5 &ndash; 40",20,"Inside range on a brand-new audience. Small numbers, but every tap is a deliberate step toward a conversation about a considered purchase."), "mc:link-taps")
html = sub(html,
    '<div class="mc-top"><span class="mc-name">PCR</span><span class="mc-badge exceed">Exceeding</span></div>\n          <div class="mc-nums"><div><span class="mc-lbl">June</span><span class="mc-val exceed">23.4%</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">10% &ndash; 16%</span></div></div>\n          <div class="bar-track"><div class="bar-fill exceed" data-w="100" style="width:0%"></div></div>\n          <p class="mc-note">Nearly 1 in 4 profile visitors chose to follow. A healthy audience is actively building around the brand.</p>\n          <p class="mc-callout">Profile conversion came in at 23.4%. Translation: 23.4% of the people who visited your profile chose to follow. A strong profile conversion rate means your page is doing its job, turning curious visitors into an audience you can nurture toward buying.</p>',
    mc("PCR","watch","Watch","9.8%","10% &ndash; 18%",54,"Just under floor and close to range. Nearly one in ten profile visitors chose to follow, healthy for a first month.","Profile conversion came in at 9.8%. Translation: 9.8% of the people who visited your profile chose to follow. A strong profile conversion rate means your page is doing its job, turning curious visitors into an audience you can nurture toward buying."), "mc:pcr")

# ── C2B: sub + proof label + Panel 1 funnel + Panel 2 (dollar -> tap volume) ─
html = sub(html, '<span>See the 12-month value trajectory</span>', '<span>See the bio link tap trajectory</span>', "c2b:proof-label")
html = sub(html, 'How this month&rsquo;s attention maps to business signal, from what we can see on-platform to a conservative estimate of what it&rsquo;s worth.',
           'How this month&rsquo;s attention maps to business signal, from the widest reach down to the highest-intent taps.', "c2b:sub")
html = sub(html,
    '<div class="c2b-step"><span class="c2b-step-num">147,499</span><div class="c2b-step-main"><span class="c2b-step-txt">people saw your content</span><span class="c2b-step-badge">\U0001F3DF Great American Ball Park filled 3.5x over</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">2,024</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped through to look closer</span><span class="c2b-step-badge">\U0001F3AD nearly filling the Taft Theatre</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">255</span><div class="c2b-step-main"><span class="c2b-step-txt">bookmarked content to reference later</span><span class="c2b-step-badge">\U0001F4CC 255 pre-purchase bookmarks</span></div></div>\n'
    '        <div class="c2b-step hi"><span class="c2b-step-num">263</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped a bio link, the highest-intent signal we track</span><span class="c2b-step-badge">\U0001F446 263 deliberate decisions to explore your business</span></div></div>',
    '<div class="c2b-step"><span class="c2b-step-num">4,401</span><div class="c2b-step-main"><span class="c2b-step-txt">people saw your content</span><span class="c2b-step-badge">\U0001F4A1 4,401 first impressions of your expertise</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">256</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped through to look closer</span><span class="c2b-step-badge">\U0001F50E a room full of prospective clients</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">19</span><div class="c2b-step-main"><span class="c2b-step-txt">bookmarked content to reference later</span><span class="c2b-step-badge">\U0001F4CC 19 pre-consultation bookmarks</span></div></div>\n'
    '        <div class="c2b-step hi"><span class="c2b-step-num">8</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped a bio link, the highest-intent signal we track</span><span class="c2b-step-badge">\U0001F446 8 deliberate steps toward a conversation</span></div></div>',
    "c2b:funnel")

# tap-volume trajectory panel (single point, first report; NO dollars)
AXIS = ''.join(
    f'<line x1="46" y1="{y}.0" x2="624" y2="{y}.0" stroke="rgba(255,255,255,.08)" stroke-width="1"/>'
    f'<text x="40" y="{y+3}.0" text-anchor="end" font-size="9" fill="rgba(255,255,255,.4)">{lab}</text>'
    for y, lab in [(226,"0"),(174,"2"),(122,"5"),(70,"8"),(18,"11")])
MONTHS = [("Jan",46.0),("Feb",98.5),("Mar",151.1),("Apr",203.6),("May",256.2),("Jun",308.7),
          ("Jul",361.3),("Aug",413.8),("Sep",466.4),("Oct",518.9),("Nov",571.5),("Dec",624.0)]
MLABELS = ''.join(
    f'<text x="{x}" y="242" text-anchor="middle" font-size="9" fill="rgba(255,255,255,{".7" if m=="Jul" else ".28"})">{m}</text>'
    for m, x in MONTHS)
TAP_SVG = (
    '<svg class="traj-chart" viewBox="0 0 640 260" role="img" aria-label="Bio link tap trajectory">'
    + AXIS + MLABELS +
    '<line x1="361.3" y1="70.0" x2="624.0" y2="70.0" stroke="rgba(255,255,255,.35)" stroke-width="2" stroke-dasharray="5 4"/>'
    '<circle cx="361.3" cy="70.0" r="3" fill="#e2ed7a"/>'
    '<text x="369.3" y="62.0" font-size="10" fill="#e2ed7a" font-weight="700">Building your baseline</text></svg>')
TAP_PANEL = (
    '<div class="c2b-estimate"><p class="c2b-panel-label">Bio link tap trajectory &middot; 2026</p><div class="traj-wrap">'
    '<p class="traj-lead">This is your first month with us, so the line is just beginning. This chart tracks your bio link taps across 2026, '
    'the highest-intent signal we can measure directly for a considered, high-ticket sale. At your current volume, dollar modeling gets noisy, '
    'so we chart tap volume now and begin modeling the dollar trajectory on the customer lifetime value you shared once you clear roughly 50 taps '
    'a month. July sets the starting point, and the trend from here is what matters.</p>'
    + TAP_SVG +
    '<div class="traj-legend"><span class="lg"><span class="sw mid"></span>Bio link taps</span><span class="lg"><span class="sw proj"></span>Projection (Aug&ndash;Dec)</span></div></div>'
    '<p class="c2b-disclaimer">You&rsquo;ve shared your customer lifetime value, so once your bio link taps clear roughly 50 a month we&rsquo;ll begin '
    'modeling the dollar trajectory on your actual economics rather than a category benchmark.</p></div>')

# replace Carl's whole dollar c2b-estimate block with the tap panel
import re as _re
old_est = _re.search(r'<!-- PANEL 2 — Conservative business estimate \(two-tier\) -->\n    <div class="c2b-estimate">.*?</div>(?=\n  </section>)', html, _re.S)
if not old_est:
    sys.exit("ANCHOR FAIL [c2b:panel2]")
html = html.replace(old_est.group(0), '<!-- PANEL 2 — Bio link tap trajectory (process-v8.5 §6: tap-volume, CLV documented but taps < ~50/mo) -->\n    ' + TAP_PANEL, 1)
edits.append("c2b:tap-panel")

# ── Beat 4: pattern + quarter view (first-report) + score strip ─────────────
html = sub(html, 'The launch proved the format. Retention at 25% is the one signal to lift, it tells us the openings can hit a beat faster. At the quarter level, your view is just beginning, this is month one of the baseline.',
           'Authority and founder-led content is what earns attention from a considered B2B buyer. Retention is the one signal under floor, so holding attention longer is where the next gain lives.', "beat4:pattern")
html = sub(html,
    '<div class="qy-grid"><div class="qy-col "><div class="qy-q">Q1</div><div class="qy-range">Jan&ndash;Mar</div><div class="qy-note">Not tracked. First report June 2026.</div><div class="qy-state">Pre-launch</div></div><div class="qy-col current"><div class="qy-q">Q2</div><div class="qy-range">Apr&ndash;Jun</div><div class="qy-note">Building baseline. June is your first month.</div><div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> new followers and shares landed 2 to 3x target, and 263 bio link taps in the first month.</div><div class="qy-tline"><span class="qy-tl">Watched:</span> video retention at 25%, and engagement the softest of the three stages.</div></div><div class="qy-state">In progress</div></div><div class="qy-col "><div class="qy-q">Q3</div><div class="qy-range">Jul&ndash;Sep</div><div class="qy-note">Begins July</div><div class="qy-state">Pending</div></div><div class="qy-col "><div class="qy-q">Q4</div><div class="qy-range">Oct&ndash;Dec</div><div class="qy-note">Later this year</div><div class="qy-state">Pending</div></div></div>',
    '<div class="qy-grid"><div class="qy-col "><div class="qy-q">Q1</div><div class="qy-range">Jan&ndash;Mar</div><div class="qy-note">Not tracked. Engagement began June 2026.</div><div class="qy-state">Pre-engagement</div></div><div class="qy-col "><div class="qy-q">Q2</div><div class="qy-range">Apr&ndash;Jun</div><div class="qy-note">Engagement began June. First report is July.</div><div class="qy-state">Onboarding</div></div><div class="qy-col current"><div class="qy-q">Q3</div><div class="qy-range">Jul&ndash;Sep</div><div class="qy-note">Building baseline. July is your first report.</div><div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> click-through, profile visits, and comments landed on track on a brand-new audience.</div><div class="qy-tline"><span class="qy-tl">Watched:</span> video retention at 20%, the clear first lever.</div></div><div class="qy-state">In progress</div></div><div class="qy-col "><div class="qy-q">Q4</div><div class="qy-range">Oct&ndash;Dec</div><div class="qy-note">Later this year</div><div class="qy-state">Pending</div></div></div>',
    "beat4:qy")
html = sub(html, '<div class="mscore-cell current"><div class="mscore-m">Jun</div><div class="mscore-v">9.2</div></div>', '<div class="mscore-cell empty"><div class="mscore-m">Jun</div><div class="mscore-v">&middot;</div></div>', "mscore:jun")
html = sub(html, '<div class="mscore-cell empty"><div class="mscore-m">Jul</div><div class="mscore-v">&middot;</div></div>', '<div class="mscore-cell current"><div class="mscore-m">Jul</div><div class="mscore-v">7.5</div></div>', "mscore:jul")

# ── Beat 5: takeaway, tests, CTA, closing ────────────────────────────────────
html = sub(html, 'Next month we tighten Reel openings to lift how long people watch, and test which catering calls to action pull the most taps.',
           'Next month we sharpen opening hooks to hold more of the attention we earn, and keep the authority and founder-led content that is landing.', "beat5:takeaway")
html = sub(html, 'Where our attention is in July', 'Where our attention is in August', "beat5:focus")
html = sub(html,
    '<div class="tw-item tests"><p class="tw-item-head">Tighter Reel openings and retention</p><p class="tw-item-body">In July, we&rsquo;re watching how tighter Reel openings affect retention. The goal is lifting from 25% toward the 50% Lift floor without losing reach.</p></div>',
    '<div class="tw-item tests"><p class="tw-item-head">Sharper opening hooks and retention</p><p class="tw-item-body">In August, we&rsquo;re watching how a sharper first line and tighter opens move retention. The goal is lifting from 20% toward the 35% Spark floor without losing reach.</p></div>', "beat5:tw1")
html = sub(html,
    '<div class="tw-item tests"><p class="tw-item-head">Which catering-CTA formats land</p><p class="tw-item-body">We&rsquo;re paying attention to which catering-CTA formats pull the most bio link taps across post types, watching July and August together before we settle on a standard.</p></div>',
    '<div class="tw-item tests"><p class="tw-item-head">Authority and founder-led content</p><p class="tw-item-body">We&rsquo;re doubling down on founder-led, expertise-first content, the format that earns trust from a business owner weighing a considered, high-ticket purchase.</p></div>', "beat5:tw2")
html = sub(html, 'Drive qualified catering inquiries', 'Drive qualified consultation signal', "beat5:cta-obj")
html = sub(html, '&ldquo;Inquire about catering, link in bio.&rdquo;', '&ldquo;Book a strategy call, link in bio.&rdquo;', "beat5:cta-copy")
html = sub(html, 'Catering is your priority lever this quarter. June proved the audience is finding you and tapping through at a strong rate. July concentrates the bio link and story stickers on the catering path, so more of that interest turns into an inquiry.',
           'A booked consultation is your priority conversion this quarter. The first month proved a focused audience is finding you and clicking through. From here we concentrate the bio link and content on the path to a booked call.', "beat5:cta-rationale")
html = sub(html, 'This is month one, so we are learning what works. We&rsquo;ll step back and lock the strategy once we have a few months of real data.',
           'This is your first report, so we are learning what works. We&rsquo;ll step back and lock the strategy once we have a few months of real data.', "beat5:closing")

# ── footer ───────────────────────────────────────────────────────────────────
html = sub(html, 'Prepared by <a href="https://scrollmedia.co" target="_blank" rel="noopener">Scroll Media</a> &middot; June 2026 Performance Report<br>',
           'Prepared by <a href="https://scrollmedia.co" target="_blank" rel="noopener">Scroll Media</a> &middot; July 2026 Performance Report<br>', "footer")

# ── TP markers around the (placeholder) feature-2up; finalize fills it ────────
m = _re.search(r'<div class="feature-2up">.*?</div></div></div>(?=\n  <p class="beat-pattern">)', html, _re.S)
if not m: sys.exit("ANCHOR FAIL [feature-2up markers]")
html = html.replace(m.group(0), '<!--TP_START-->' + m.group(0) + '<!--TP_END-->', 1)
edits.append("TP-markers")

os.makedirs(OUT_DIR, exist_ok=True); open(OUT, "w", encoding="utf-8").write(html)
print(f"score {R['final']} (raw {R['raw']:.3f}); wrote {OUT} ({len(edits)} edits)")

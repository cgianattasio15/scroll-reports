#!/usr/bin/env python3
"""build_shoplaunchparty_july.py -- Launch Party June 2026 -> July 2026 (standard).
Anchored, hard-fail. Score computed by score_report.py. Post-dependent Beat 2 +
Beat 4 cards left as June's; finalized after the Metricool pull.
Trajectory SVG (panel 2) left as-is per v8.5 ("stays exactly as-is; no new dollar"),
only the current-month funnel (panel 1) updates."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score_report as sr

REPO = "/Users/chase.gianattasio/Desktop/scroll-reports"
SRC = f"{REPO}/shoplaunchparty/june2026/index.html"
OUT_DIR = f"{REPO}/shoplaunchparty/july2026"; OUT = f"{OUT_DIR}/index.html"

JULY = {"saves":111,"ctr":12.3,"retention":36,"pcr":13.0,"link_taps":82,"profile_visits":667,"comments":99,"new_followers":87,"total_views":63924,"shares":89}
JUNE = {"saves":88,"ctr":13.2,"retention":38,"pcr":6.8,"link_taps":72,"profile_visits":546,"comments":114,"new_followers":37,"total_views":54858,"shares":48}
R = sr.score(JULY, "Lift", JUNE)
assert R["final"] == 8.5, R["final"]

edits = []
def sub(html, old, new, label):
    n = html.count(old)
    if n != 1: sys.exit(f"ANCHOR FAIL [{label}]: {n} found\n  {old[:170]}")
    edits.append(label); return html.replace(old, new)

def block(name, tgt, cls, lab, month, val, mcls, mom, bar, note, callout):
    s = (f'<span class="mc-name">{name}</span><span class="mc-badge {cls}">{lab}</span></div>\n'
         f'          <div class="mc-nums"><div><span class="mc-lbl">{month}</span><span class="mc-val {cls}">{val}</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">{tgt}</span></div></div>\n'
         f'          <div class="mc-mom"><span class="mom {mcls}">{mom}</span></div>\n'
         f'          <div class="bar-track"><div class="bar-fill {cls}" data-w="{bar}" style="width:0%"></div></div>\n'
         f'          <p class="mc-note">{note}</p>')
    if callout: s += f'\n          <p class="mc-callout">{callout}</p>'
    return s

html = open(SRC, encoding="utf-8").read()

# head/meta
html = sub(html, "<title>Launch Party &ndash; June 2026 | Scroll Media</title>", "<title>Launch Party &ndash; July 2026 | Scroll Media</title>", "title")
html = sub(html, 'Launch Party June 2026 Instagram performance report. Score 7.9/10. Building Month.', 'Launch Party July 2026 Instagram performance report. Score 8.5/10. Strong Month.', "meta:desc")
html = sub(html, 'content="Launch Party, June 2026 Performance Report">', 'content="Launch Party, July 2026 Performance Report">', "og:title")
html = sub(html, 'content="Monthly score 7.9/10. Building Month. Prepared by Scroll Media.">', 'content="Monthly score 8.5/10. Strong Month. Prepared by Scroll Media.">', "og:desc")

# hero
html = sub(html, '<div class="hero-eyebrow"><span class="dot"></span>June 2026 Performance Report</div>', '<div class="hero-eyebrow"><span class="dot"></span>July 2026 Performance Report</div>', "hero:eyebrow")
html = sub(html, 'Lift Stage &middot; Month 23', 'Lift Stage &middot; Month 24', "hero:stage")
html = sub(html, '<span>June 1&ndash;30, 2026</span>', '<span>July 1&ndash;31, 2026</span>', "hero:window")
html = sub(html, '<div class="ph-bignum">7.9<span class="unit">/10</span></div>\n        <p class="ph-title">Building Month</p>\n        <span class="ph-delta dn">&#9660; 0.9 vs. May</span>',
           '<div class="ph-bignum">8.5<span class="unit">/10</span></div>\n        <p class="ph-title">Strong Month</p>\n        <span class="ph-delta up">&#9650; 0.6 vs. June</span>', "hero:score")
html = sub(html, '<span class="ph-badge exceed"><span class="bd"></span>1 Exceeding</span>\n          <span class="ph-badge ontrack"><span class="bd"></span>5 On Track</span>\n          <span class="ph-badge watch"><span class="bd"></span>4 Watch</span>',
           '<span class="ph-badge exceed"><span class="bd"></span>1 Exceeding</span>\n          <span class="ph-badge ontrack"><span class="bd"></span>7 On Track</span>\n          <span class="ph-badge watch"><span class="bd"></span>2 Watch</span>', "hero:badges")
html = sub(html, '<p class="ph-label">Bio Link Engagement</p>\n        <div class="ph-bignum">72</div>', '<p class="ph-label">Bio Link Engagement</p>\n        <div class="ph-bignum">82</div>', "hero:outcome")
html = sub(html, '<p class="hero-summary"><strong>June was a quieter month inside a strong quarter. Reach softened, but the engine that turns attention into customers held.</strong></p>',
           '<p class="hero-summary"><strong>A strong, well-rounded month. Conversion stayed well above benchmark and both saves and profile conversion climbed.</strong></p>', "hero:summary")

# beat3 takeaway + bstats
html = sub(html, 'Reach dipped, but conversion stayed strong. A 13.2% click-through rate, above your stage ceiling, kept sending people to your shop.',
           'Click-through held at 12.3% against a 3 to 6% benchmark, saves rose to 111, and profile conversion nearly doubled to 13%. The funnel is converting efficiently.', "beat3:takeaway")
html = sub(html, '<div class="bstats"><div class="bstat"><div class="bstat-val exceed">13.2%</div><div class="bstat-lbl">Click-through rate</div><span class="bstat-tag exceed">Exceeding</span></div><div class="bstat"><div class="bstat-val ontrack">72</div><div class="bstat-lbl">Bio link taps</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val ontrack">54,858</div><div class="bstat-lbl">Total views</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val watch">38%</div><div class="bstat-lbl">Video retention</div><span class="bstat-tag watch">Watch</span></div></div>',
           '<div class="bstats"><div class="bstat"><div class="bstat-val exceed">12.3%</div><div class="bstat-lbl">Click-through rate</div><span class="bstat-tag exceed">Exceeding</span></div><div class="bstat"><div class="bstat-val ontrack">111</div><div class="bstat-lbl">Saves</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val ontrack">13.0%</div><div class="bstat-lbl">Profile conversion</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val watch">36%</div><div class="bstat-lbl">Video retention</div><span class="bstat-tag watch">Watch</span></div></div>', "beat3:bstats")

# goal tracker bars (BOFU 64->76, TOFU 35->45; MOFU 49 unchanged) — order BOFU then TOFU
html = sub(html, '<div class="gt-bar-fill lime" data-w="64" style="width:0%"></div></div>\n            <span class="gt-pct">64%</span>', '<div class="gt-bar-fill lime" data-w="76" style="width:0%"></div></div>\n            <span class="gt-pct">76%</span>', "gt:bofu-bar")
html = sub(html, '3.2<span class="gt-score-max">/5.0</span>', '3.8<span class="gt-score-max">/5.0</span>', "gt:bofu-pts")
html = sub(html, '<div class="gt-bar-fill lime" data-w="35" style="width:0%"></div></div>\n            <span class="gt-pct">35%</span>', '<div class="gt-bar-fill lime" data-w="45" style="width:0%"></div></div>\n            <span class="gt-pct">45%</span>', "gt:tofu-bar")
html = sub(html, '0.95<span class="gt-score-max">/2.75</span>', '1.25<span class="gt-score-max">/2.75</span>', "gt:tofu-pts")

# goal narratives
html = sub(html, 'Your awareness stage scored 35% this month. Reach softened across followers, shares, and views at the same time, which is what pulled this stage down. Widening the top of the funnel is the July focus.',
           'Your awareness stage scored 45%, up from June. Shares came back inside range and views grew, while new followers stayed below floor. Widening reach further is the ongoing focus.', "narr:tofu")
html = sub(html, 'Your engagement stage scored 49%. Saves and community held their ground, and retention is the lever holding the number back. Tighter Reel pacing is the July focus.',
           'Your engagement stage scored 49%. Saves and community held their ground and profile visits grew, with retention still the lever holding the number back. Tighter Reel pacing is the focus.', "narr:mofu")
html = sub(html, 'Your conversion stage scored 64%, the strongest of the three. Click-through cleared the Lift ceiling and link taps held steady. The bottom of your funnel stayed dialed even in a quieter month.',
           'Your conversion stage scored 76%, the strongest of the three. Click-through cleared the Lift ceiling, link taps grew, and profile conversion recovered to 13%. The bottom of your funnel is converting efficiently.', "narr:bofu")

# perf label/sub + followers
html = sub(html, '<p class="sec-label">June 2026</p>', '<p class="sec-label">July 2026</p>', "perf:label")
html = sub(html, 'Every tracked metric for June, scored against your Lift Stage target ranges with month-over-month comparison.', 'Every tracked metric for July, scored against your Lift Stage target ranges with month-over-month comparison.', "perf:sub")
html = sub(html, '<div class="fb-count">5,529</div>\n        <div class="fb-mom"><span class="mom dn">&#9660; 0.04% vs. May</span></div>', '<div class="fb-count">5,576</div>\n        <div class="fb-mom"><span class="mom up">&#9650; 0.8% vs. June</span></div>', "followers")

# ── 10 metric cards ──
C = [
 ("New Followers","100 &ndash; 270","watch","Watch","37","dn","&#9660; 62% vs May","14","Below floor. Reach softened, so fewer discovery moments converted to follows.","New followers fell 62%. Translation: 62% fewer people chose to keep seeing your content after finding you. A new follow is someone deciding you are worth coming back to.",
  "watch","Watch","87","up","&#9650; 135% vs June","32","Below floor but up sharply from June. Reach widened, so more discovery moments turned into follows.","New followers rose 135%. Translation: more than twice as many people chose to keep seeing your content after finding you. A new follow is someone deciding you are worth coming back to."),
 ("Shares","60 &ndash; 300","watch","Watch","48","dn","&#9660; 6% vs May","16","Below floor. Discovery-first content that widens reach is the July lever.","Shares fell 6%. Translation: 6% fewer people sent your content to someone else. Shares put you in front of new audiences your posts wouldn&rsquo;t reach on their own.",
  "ontrack","On Track","89","up","&#9650; 85% vs June","30","Back inside range. Relatable, everyday content widened reach again.","Shares rose 85%. Translation: 85% more people sent your content to someone else. Shares put you in front of new audiences your posts wouldn&rsquo;t reach on their own."),
 ("Total Views","40,000 &ndash; 150,000","ontrack","On Track","54,858","dn","&#9660; 8% vs May","37","Inside range but down from May. Reach base intact, just quieter.","Views fell 8%. Translation: your content reached 8% fewer screens this month. Views are the widest measure of how many people you got in front of, and everything downstream starts here.",
  "ontrack","On Track","63,924","up","&#9650; 17% vs June","43","Inside range and up from June. Reach rebuilt this month.","Views rose 17%. Translation: your content reached 17% more screens this month. Views are the widest measure of how many people you got in front of, and everything downstream starts here."),
 ("Profile Visits","300 &ndash; 2,000","ontrack","On Track","546","dn","&#9660; 7% vs May","27","Inside range. Consideration traffic held.","Profile visits fell 7%. Translation: 7% fewer people tapped through to look closer at who you are. A profile visit is a deliberate step toward becoming a customer, not a passive scroll.",
  "ontrack","On Track","667","up","&#9650; 22% vs June","33","Inside range and up from June. Consideration traffic grew.","Profile visits rose 22%. Translation: 22% more people tapped through to look closer at who you are. A profile visit is a deliberate step toward becoming a customer, not a passive scroll."),
 ("Retention","50% &ndash; 65%","watch","Watch","38%","dn","&#9660; 16 pts vs May","58","Below floor and down from May. Content pacing needs tightening to rebuild attention.","Retention came in at 38%. Translation: on average, people watched 38% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences.",
  "watch","Watch","36%","dn","&#9660; 2 pts vs June","55","Below floor and essentially flat. Tighter Reel pacing stays the lever to rebuild attention.","Retention came in at 36%. Translation: on average, people watched 36% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences."),
 ("Saves","80 &ndash; 400","ontrack","On Track","88","dn","&#9660; 20% vs May","22","Inside range but down from May. The education series is still landing at a healthy rate.","Saves fell 20%. Translation: 20% fewer people bookmarked your posts to act on later. Saves are the strongest signal of a future buyer.",
  "ontrack","On Track","111","up","&#9650; 26% vs June","28","Inside range and up from June. The education series keeps earning bookmarks.","Saves rose 26%. Translation: 26% more people bookmarked your posts to act on later. Saves are the strongest signal of a future buyer."),
 ("Comments","75 &ndash; 250","ontrack","On Track","114","dn","&#9660; 3% vs May","46","Inside range. Community held.","Comments fell 3%. Translation: 3% fewer people stopped to start a conversation with you. Comments are public proof that your audience is engaged, and they pull in the people watching from the sidelines.",
  "ontrack","On Track","99","dn","&#9660; 13% vs June","40","Inside range, eased slightly from June. Community stayed engaged.","Comments fell 13%. Translation: 13% fewer people stopped to start a conversation with you. Comments are public proof that your audience is engaged, and they pull in the people watching from the sidelines."),
 ("CTR","3% &ndash; 6%","exceed","Exceeding","13.2%","dn","&#9660; 2 pts vs May","100","Above the Lift ceiling. The bio link keeps doing its job.","Click-through rate came in at 13.2%. Translation: of everyone who saw your link, 13.2% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers.",
  "exceed","Exceeding","12.3%","dn","&#9660; 0.9 pts vs June","100","Above the Lift ceiling. The bio link keeps doing its job.","Click-through rate came in at 12.3%. Translation: of everyone who saw your link, 12.3% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers."),
 ("Bio Link Taps","30 &ndash; 180","ontrack","On Track","72","dn","&#9660; 19% vs May","40","Inside range but down from May&rsquo;s high. Steady traffic to the shop and in-store.","Link taps fell 19%. Translation: 19% fewer people tapped the link in your bio to move toward your site, booking, or offer. A link tap is one of the clearest actions someone takes when they are ready to do business.",
  "ontrack","On Track","82","up","&#9650; 14% vs June","46","Inside range and up from June. Steady, growing traffic to the shop and in-store.","Link taps rose 14%. Translation: 14% more people tapped the link in your bio to move toward your site, booking, or offer. A link tap is one of the clearest actions someone takes when they are ready to do business."),
 ("PCR","10% &ndash; 16%","watch","Watch","6.8%","dn","&#9660; 9.8 pts vs May","42","Below floor. Profile-to-follower conversion softened.","Profile conversion came in at 6.8%. Translation: 6.8% of the people who visited your profile chose to follow. A strong profile conversion rate means your page is doing its job, turning curious visitors into an audience you can nurture toward buying.",
  "ontrack","On Track","13.0%","up","&#9650; 6.2 pts vs June","81","Back inside range and nearly doubled from June. Profile-to-follower conversion recovered strongly.","Profile conversion came in at 13.0%. Translation: 13.0% of the people who visited your profile chose to follow. A strong profile conversion rate means your page is doing its job, turning curious visitors into an audience you can nurture toward buying."),
]
for c in C:
    name,tgt = c[0],c[1]
    old = block(name,tgt,c[2],c[3],"June",c[4],c[5],c[6],c[7],c[8],c[9])
    new = block(name,tgt,c[10],c[11],"July",c[12],c[13],c[14],c[15],c[16],c[17])
    html = sub(html, old, new, f"mc:{name}")

# C2B panel 1 (funnel this month)
html = sub(html,
    '<div class="c2b-step"><span class="c2b-step-num">54,858</span><div class="c2b-step-main"><span class="c2b-step-txt">people saw your content</span><span class="c2b-step-badge">\U0001F3BC the equivalent of filling Music Hall 22 times over</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">546</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped through to look closer</span><span class="c2b-step-badge">\U0001F6B6 a Washington Park summer-evening crowd</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">88</span><div class="c2b-step-main"><span class="c2b-step-txt">bookmarked content to reference later</span><span class="c2b-step-badge">\U0001F4CC 88 pre-purchase bookmarks</span></div></div>\n'
    '        <div class="c2b-step hi"><span class="c2b-step-num">72</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped a bio link, the highest-intent signal we track</span><span class="c2b-step-badge">\U0001F446 72 deliberate taps toward your shop</span></div></div>',
    '<div class="c2b-step"><span class="c2b-step-num">63,924</span><div class="c2b-step-main"><span class="c2b-step-txt">people saw your content</span><span class="c2b-step-badge">\U0001F3BC the equivalent of filling Music Hall 26 times over</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">667</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped through to look closer</span><span class="c2b-step-badge">\U0001F6B6 a Washington Park summer-evening crowd</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">111</span><div class="c2b-step-main"><span class="c2b-step-txt">bookmarked content to reference later</span><span class="c2b-step-badge">\U0001F4CC 111 pre-purchase bookmarks</span></div></div>\n'
    '        <div class="c2b-step hi"><span class="c2b-step-num">82</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped a bio link, the highest-intent signal we track</span><span class="c2b-step-badge">\U0001F446 82 deliberate taps toward your shop</span></div></div>',
    "c2b:funnel")

# Beat 4 pattern (from §4)
html = sub(html, 'The posts that traveled were everyday moments, not polished promos. Relatable and industry-POV content is your reach engine, and conversion holds even when reach dips.',
           'Your audience is clicking and saving. The build is in reach: new-follower volume and retention are the two levers still under target.', "beat4:pattern")

# Beat 4 quarter view: Q2 complete, Q3 current
html = sub(html,
    '<div class="qy-col current"><div class="qy-q">Q2</div><div class="qy-range">Apr&ndash;Jun</div><div class="qy-avg">8.4<span class="u">/10</span></div><div class="qy-badge strong">Strong</div><div class="qy-bars"><span style="height:73%"></span><span style="height:81%"></span><span class="cur" style="height:56%"></span></div><div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> click-through stayed above target all quarter, and April and May were both strong months.</div><div class="qy-tline"><span class="qy-tl">Watched:</span> reach softened into June, and retention slipped to 38%.</div></div><div class="qy-state">Complete</div></div><div class="qy-col "><div class="qy-q">Q3</div><div class="qy-range">Jul&ndash;Sep</div><div class="qy-note">Begins July</div><div class="qy-state">Pending</div></div>',
    '<div class="qy-col "><div class="qy-q">Q2</div><div class="qy-range">Apr&ndash;Jun</div><div class="qy-avg">8.4<span class="u">/10</span></div><div class="qy-badge strong">Strong</div><div class="qy-bars"><span style="height:73%"></span><span style="height:81%"></span><span style="height:56%"></span></div><div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> click-through stayed above target all quarter, April and May both strong.</div><div class="qy-tline"><span class="qy-tl">Watched:</span> reach softened into June before rebuilding in July.</div></div><div class="qy-state">Complete</div></div><div class="qy-col current"><div class="qy-q">Q3</div><div class="qy-range">Jul&ndash;Sep</div><div class="qy-avg">8.5<span class="u">/10</span></div><div class="qy-badge strong">Strong</div><div class="qy-bars"><span class="cur" style="height:85%"></span></div><div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> conversion held above benchmark and profile conversion nearly doubled to 13%.</div><div class="qy-tline"><span class="qy-tl">Watched:</span> new followers and retention are the two levers still under target.</div></div><div class="qy-state">In progress</div></div>',
    "beat4:qy")

# mscore: Jun un-current, Jul -> 8.5 current
html = sub(html, '<div class="mscore-cell current"><div class="mscore-m">Jun</div><div class="mscore-v">7.9</div></div>', '<div class="mscore-cell"><div class="mscore-m">Jun</div><div class="mscore-v">7.9</div></div>', "mscore:jun")
html = sub(html, '<div class="mscore-cell empty"><div class="mscore-m">Jul</div><div class="mscore-v">&middot;</div></div>', '<div class="mscore-cell current"><div class="mscore-m">Jul</div><div class="mscore-v">8.5</div></div>', "mscore:jul")

# Beat 5 takeaway + focus + closing
html = sub(html, 'Next month we widen the top of the funnel with discovery-first Reels and tighter openings to rebuild reach, while the conversion engine keeps running.',
           'We widen top-of-funnel reach to lift new followers, and tighten hooks for retention, while the conversion engine keeps running.', "beat5:takeaway")
html = sub(html, 'Where our attention is in July', 'Where our attention is in August', "beat5:focus")

# footer
html = sub(html, '&middot; June 2026 Performance Report<br>', '&middot; July 2026 Performance Report<br>', "footer")

os.makedirs(OUT_DIR, exist_ok=True); open(OUT,"w",encoding="utf-8").write(html)
print(f"score {R['final']} (raw {R['raw']:.3f}, credit {R['credit']:+.2f}); wrote {OUT} ({len(edits)} edits)")

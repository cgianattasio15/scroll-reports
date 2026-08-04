#!/usr/bin/env python3
"""build_laneandkate_july.py -- Lane & Kate June->July 2026 (standard).
Anchored/hard-fail; score via score_report.py. Post-dependent Beat 2/4 cards
finalized after the pull. Trajectory panel left as-is (v8.5). Calibration: kept
at 8.0 (all 10 metrics up) per package §2; logged in reports_log."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score_report as sr

REPO = "/Users/chase.gianattasio/Desktop/scroll-reports"
SRC = f"{REPO}/laneandkate/june2026/index.html"
OUT_DIR = f"{REPO}/laneandkate/july2026"; OUT = f"{OUT_DIR}/index.html"

JULY = {"saves":42,"ctr":15.6,"retention":28,"pcr":7.3,"link_taps":152,"profile_visits":974,"comments":70,"new_followers":71,"total_views":60725,"shares":72}
JUNE = {"saves":32,"ctr":15.4,"retention":25,"pcr":7.2,"link_taps":133,"profile_visits":866,"comments":59,"new_followers":62,"total_views":53423,"shares":36}
R = sr.score(JULY, "Lift", JUNE); assert R["final"] == 8.0, R["final"]

edits = []
def sub(html, old, new, label):
    n = html.count(old)
    if n != 1: sys.exit(f"ANCHOR FAIL [{label}]: {n} found\n  {old[:170]}")
    edits.append(label); return html.replace(old, new)
def block(name,tgt,cls,lab,month,val,mcls,mom,bar,note,callout):
    s=(f'<span class="mc-name">{name}</span><span class="mc-badge {cls}">{lab}</span></div>\n'
       f'          <div class="mc-nums"><div><span class="mc-lbl">{month}</span><span class="mc-val {cls}">{val}</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">{tgt}</span></div></div>\n'
       f'          <div class="mc-mom"><span class="mom {mcls}">{mom}</span></div>\n'
       f'          <div class="bar-track"><div class="bar-fill {cls}" data-w="{bar}" style="width:0%"></div></div>\n'
       f'          <p class="mc-note">{note}</p>')
    if callout: s+=f'\n          <p class="mc-callout">{callout}</p>'
    return s

html = open(SRC, encoding="utf-8").read()

html = sub(html, "<title>Lane & Kate &ndash; June 2026 | Scroll Media</title>", "<title>Lane & Kate &ndash; July 2026 | Scroll Media</title>", "title")
html = sub(html, 'Lane & Kate June 2026 Instagram performance report. Score 7.5/10. Building Month.', 'Lane & Kate July 2026 Instagram performance report. Score 8.0/10. Solid Month.', "meta:desc")
html = sub(html, 'content="Lane & Kate, June 2026 Performance Report">', 'content="Lane & Kate, July 2026 Performance Report">', "og:title")
html = sub(html, 'content="Monthly score 7.5/10. Building Month. Prepared by Scroll Media.">', 'content="Monthly score 8.0/10. Solid Month. Prepared by Scroll Media.">', "og:desc")

html = sub(html, '<div class="hero-eyebrow"><span class="dot"></span>June 2026 Performance Report</div>', '<div class="hero-eyebrow"><span class="dot"></span>July 2026 Performance Report</div>', "hero:eyebrow")
html = sub(html, 'Lift Stage &middot; Month 14', 'Lift Stage &middot; Month 15', "hero:stage")
html = sub(html, '<span>June 1&ndash;30, 2026</span>', '<span>July 1&ndash;31, 2026</span>', "hero:window")
html = sub(html, '<div class="ph-bignum">7.5<span class="unit">/10</span></div>\n        <p class="ph-title">Building Month</p>\n        <span class="ph-delta dn">&#9660; 0.7 vs. May</span>',
           '<div class="ph-bignum">8.0<span class="unit">/10</span></div>\n        <p class="ph-title">Solid Month</p>\n        <span class="ph-delta up">&#9650; 0.5 vs. June</span>', "hero:score")
html = sub(html, '<span class="ph-badge exceed"><span class="bd"></span>1 Exceeding</span>\n          <span class="ph-badge ontrack"><span class="bd"></span>3 On Track</span>\n          <span class="ph-badge watch"><span class="bd"></span>6 Watch</span>',
           '<span class="ph-badge exceed"><span class="bd"></span>1 Exceeding</span>\n          <span class="ph-badge ontrack"><span class="bd"></span>4 On Track</span>\n          <span class="ph-badge watch"><span class="bd"></span>5 Watch</span>', "hero:badges")
html = sub(html, '<p class="ph-label">Bio Link Engagement</p>\n        <div class="ph-bignum">133</div>', '<p class="ph-label">Bio Link Engagement</p>\n        <div class="ph-bignum">152</div>', "hero:outcome")
html = sub(html, '<p class="hero-summary"><strong>June was a softer month, but your highest-value path held. Click-through climbed to 15.4%, well above target, and 133 people tapped toward booking.</strong></p>',
           '<p class="hero-summary"><strong>Momentum across the board. Every tracked metric improved from June, led by a click-through rate more than double your benchmark.</strong></p>', "hero:summary")

html = sub(html, 'Conversion stayed strong while engagement depth softened. Click-through was your standout, above the stage ceiling.',
           'Click-through held at 15.6% against a 3 to 6% range, link taps rose to 152, and views and profile visits both climbed. Conversion intent is your standout.', "beat3:takeaway")
html = sub(html, '<div class="bstats"><div class="bstat"><div class="bstat-val exceed">15.4%</div><div class="bstat-lbl">Click-through rate</div><span class="bstat-tag exceed">Exceeding</span></div><div class="bstat"><div class="bstat-val ontrack">133</div><div class="bstat-lbl">Bio link taps</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val watch">32</div><div class="bstat-lbl">Saves</div><span class="bstat-tag watch">Watch</span></div><div class="bstat"><div class="bstat-val watch">25%</div><div class="bstat-lbl">Video retention</div><span class="bstat-tag watch">Watch</span></div></div>',
           '<div class="bstats"><div class="bstat"><div class="bstat-val exceed">15.6%</div><div class="bstat-lbl">Click-through rate</div><span class="bstat-tag exceed">Exceeding</span></div><div class="bstat"><div class="bstat-val ontrack">152</div><div class="bstat-lbl">Bio link taps</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val ontrack">974</div><div class="bstat-lbl">Profile visits</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val watch">28%</div><div class="bstat-lbl">Video retention</div><span class="bstat-tag watch">Watch</span></div></div>', "beat3:bstats")

# goal tracker: only TOFU changes (35->45, 0.95->1.25); MOFU 27% / BOFU 64% unchanged
html = sub(html, '<div class="gt-bar-fill lime" data-w="35" style="width:0%"></div></div>\n            <span class="gt-pct">35%</span>', '<div class="gt-bar-fill lime" data-w="45" style="width:0%"></div></div>\n            <span class="gt-pct">45%</span>', "gt:tofu-bar")
html = sub(html, '0.95<span class="gt-score-max">/2.75</span>', '1.25<span class="gt-score-max">/2.75</span>', "gt:tofu-pts")

html = sub(html, 'Your awareness stage scored 35% this month. Reach softened across new followers, shares, and views at the same time, which pulled this stage down. Widening the top of the funnel with discovery-first content is the July focus.',
           'Your awareness stage scored 45%, up from June. Shares came back inside range and views grew, while new followers stayed below floor. Widening reach further is the ongoing focus.', "narr:tofu")
html = sub(html, 'Your engagement stage scored 27%, the lowest of the three. Saves, comments, and retention all sit below their Lift floors, so the consideration layer is the clearest place to build. Education content, the four Cs and custom-design walkthroughs, gives shoppers a reason to save and comment.',
           'Your engagement stage scored 27%, still the lowest of the three but improving. Saves, comments, and retention all rose from June while staying under their Lift floors, so the consideration layer is the clearest place to build. Education content, the four Cs and custom-design walkthroughs, gives shoppers a reason to save and comment.', "narr:mofu")
html = sub(html, 'Your conversion stage scored 64%, the strongest by far. Click-through cleared the Lift ceiling at 15.4% and link taps held inside range at 133. The bottom of your funnel stayed dialed even in a quieter month.',
           'Your conversion stage scored 64%, the strongest by far. Click-through cleared the Lift ceiling at 15.6% and link taps rose to 152. Conversion intent is your standout.', "narr:bofu")

html = sub(html, '<p class="sec-label">June 2026</p>', '<p class="sec-label">July 2026</p>', "perf:label")
html = sub(html, 'Every tracked metric for June, scored against your Lift Stage target ranges with month-over-month comparison.', 'Every tracked metric for July, scored against your Lift Stage target ranges with month-over-month comparison.', "perf:sub")
html = sub(html, '<div class="fb-count">7,253</div>\n        <div class="fb-mom"><span class="mom up">&#9650; 0.2% vs. May</span></div>', '<div class="fb-count">7,288</div>\n        <div class="fb-mom"><span class="mom up">&#9650; 0.5% vs. June</span></div>', "followers")

C = [
 ("New Followers","100 &ndash; 270","watch","Watch","62","dn","&#9660; 42% vs May","23","Below floor. Reach softened, so fewer discovery moments converted to follows.","New followers fell 42%. Translation: 42% fewer people chose to keep seeing your content after finding you. A new follow is someone deciding you are worth coming back to.",
  "watch","Watch","71","up","&#9650; 15% vs June","26","Below floor but up from June. Reach widened, so more discovery turned into follows.","New followers rose 15%. Translation: 15% more people chose to keep seeing your content after finding you. A new follow is someone deciding you are worth coming back to."),
 ("Shares","60 &ndash; 300","watch","Watch","36","dn","&#9660; 5% vs May","12","Below floor. Discovery-first content that widens reach is the July lever.","Shares fell 5%. Translation: 5% fewer people sent your content to someone else. Shares put you in front of new audiences your posts wouldn&rsquo;t reach on their own.",
  "ontrack","On Track","72","up","&#9650; 100% vs June","24","Back inside range and doubled from June. Discovery-first content widened reach.","Shares doubled. Translation: twice as many people sent your content to someone else. Shares put you in front of new audiences your posts wouldn&rsquo;t reach on their own."),
 ("Total Views","40,000 &ndash; 150,000","ontrack","On Track","53,423","dn","&#9660; 25% vs May","36","Inside range but down from May. The reach base is intact, just quieter.","Views fell 25%. Translation: your content reached 25% fewer screens this month. Views are the widest measure of how many people you got in front of, and everything downstream starts here.",
  "ontrack","On Track","60,725","up","&#9650; 14% vs June","40","Inside range and up from June. Reach grew this month.","Views rose 14%. Translation: your content reached 14% more screens this month. Views are the widest measure of how many people you got in front of, and everything downstream starts here."),
 ("Profile Visits","300 &ndash; 2,000","ontrack","On Track","866","dn","&#9660; 11% vs May","43","Inside range. Consideration traffic held.","Profile visits fell 11%. Translation: 11% fewer people tapped through to look closer at who you are. A profile visit is a deliberate step toward becoming a customer, not a passive scroll.",
  "ontrack","On Track","974","up","&#9650; 12% vs June","49","Inside range and up from June. Consideration traffic grew.","Profile visits rose 12%. Translation: 12% more people tapped through to look closer at who you are. A profile visit is a deliberate step toward becoming a customer, not a passive scroll."),
 ("Retention","50% &ndash; 65%","watch","Watch","25%","dn","&#9660; 1 pt vs May","38","Below floor and down from May. Tighter Reel pacing is the lever to rebuild attention.","Retention came in at 25%. Translation: on average, people watched 25% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences.",
  "watch","Watch","28%","up","&#9650; 3 pts vs June","43","Below floor but up from June. Tighter Reel pacing stays the lever to rebuild attention.","Retention came in at 28%. Translation: on average, people watched 28% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences."),
 ("Saves","80 &ndash; 400","watch","Watch","32","dn","&#9660; 11% vs May","8","Below floor. Education content gives shoppers a reason to bookmark.","Saves fell 11%. Translation: 11% fewer people bookmarked your posts to act on later. Saves are the strongest signal of a future buyer.",
  "watch","Watch","42","up","&#9650; 31% vs June","11","Below floor but up from June. Education content gives shoppers a reason to bookmark.","Saves rose 31%. Translation: 31% more people bookmarked your posts to act on later. Saves are the strongest signal of a future buyer."),
 ("Comments","75 &ndash; 250","watch","Watch","59","dn","&#9660; 2% vs May","24","Below floor. Opinion and question prompts are the lever to lift replies.","Comments fell 2%. Translation: 2% fewer people stopped to start a conversation with you. Comments are public proof that your audience is engaged, and they pull in the people watching from the sidelines.",
  "watch","Watch","70","up","&#9650; 19% vs June","28","Just below floor and up from June. Opinion and question prompts are the lever to lift replies.","Comments rose 19%. Translation: 19% more people stopped to start a conversation with you. Comments are public proof that your audience is engaged, and they pull in the people watching from the sidelines."),
 ("CTR","3% &ndash; 6%","exceed","Exceeding","15.4%","up","&#9650; 1.2 pts vs May","100","Above the Lift ceiling, and up from May. The bio link keeps doing its job.","Click-through rate came in at 15.4%. Translation: of everyone who saw your link, 15.4% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers.",
  "exceed","Exceeding","15.6%","up","&#9650; 0.2 pts vs June","100","Above the Lift ceiling and up again. The bio link keeps doing its job.","Click-through rate came in at 15.6%. Translation: of everyone who saw your link, 15.6% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers."),
 ("Bio Link Taps","30 &ndash; 180","ontrack","On Track","133","dn","&#9660; 4% vs May","74","Inside range but down from May&rsquo;s high. Steady traffic to the shop and consultation page.","Link taps fell 4%. Translation: 4% fewer people tapped the link in your bio to move toward your site, booking, or offer. A link tap is one of the clearest actions someone takes when they are ready to do business.",
  "ontrack","On Track","152","up","&#9650; 14% vs June","84","Inside range and up from June. Strong, growing traffic to the shop and consultation page.","Link taps rose 14%. Translation: 14% more people tapped the link in your bio to move toward your site, booking, or offer. A link tap is one of the clearest actions someone takes when they are ready to do business."),
 ("PCR","10% &ndash; 16%","watch","Watch","7.2%","dn","&#9660; 3.8 pts vs May","45","Below floor. Profile-to-follower conversion softened.","Profile conversion came in at 7.2%. Translation: 7.2% of the people who visited your profile chose to follow. A strong profile conversion rate means your page is doing its job, turning curious visitors into an audience you can nurture toward buying.",
  "watch","Watch","7.3%","up","&#9650; 0.1 pts vs June","46","Below floor and essentially flat. Profile-to-follower conversion is the lever to build.","Profile conversion came in at 7.3%. Translation: 7.3% of the people who visited your profile chose to follow. A strong profile conversion rate means your page is doing its job, turning curious visitors into an audience you can nurture toward buying."),
]
for c in C:
    old = block(c[0],c[1],c[2],c[3],"June",c[4],c[5],c[6],c[7],c[8],c[9])
    new = block(c[0],c[1],c[10],c[11],"July",c[12],c[13],c[14],c[15],c[16],c[17])
    html = sub(html, old, new, f"mc:{c[0]}")

# C2B panel 1
html = sub(html,
    '<div class="c2b-step"><span class="c2b-step-num">53,423</span><div class="c2b-step-main"><span class="c2b-step-txt">people saw your content</span><span class="c2b-step-badge">\U0001F3AD the equivalent of filling the Aronoff Center 20 times over</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">866</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped through to look closer</span><span class="c2b-step-badge">\U0001F6B6 a full Saturday crowd browsing Hyde Park Square</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">32</span><div class="c2b-step-main"><span class="c2b-step-txt">bookmarked content to reference later</span><span class="c2b-step-badge">\U0001F4CC 32 pre-purchase bookmarks</span></div></div>\n'
    '        <div class="c2b-step hi"><span class="c2b-step-num">133</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped a bio link, the highest-intent signal we track</span><span class="c2b-step-badge">\U0001F446 133 deliberate taps toward your shop and booking page</span></div></div>',
    '<div class="c2b-step"><span class="c2b-step-num">60,725</span><div class="c2b-step-main"><span class="c2b-step-txt">people saw your content</span><span class="c2b-step-badge">\U0001F3AD the equivalent of filling the Aronoff Center 23 times over</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">974</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped through to look closer</span><span class="c2b-step-badge">\U0001F6B6 a full Saturday crowd browsing Hyde Park Square</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">42</span><div class="c2b-step-main"><span class="c2b-step-txt">bookmarked content to reference later</span><span class="c2b-step-badge">\U0001F4CC 42 pre-purchase bookmarks</span></div></div>\n'
    '        <div class="c2b-step hi"><span class="c2b-step-num">152</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped a bio link, the highest-intent signal we track</span><span class="c2b-step-badge">\U0001F446 152 deliberate taps toward your shop and booking page</span></div></div>',
    "c2b:funnel")

# Beat 4 pattern (§4)
html = sub(html, 'Destination-wedding and custom-ring stories are what they bookmark and act on. Engagement depth (saves, comments, retention) is the layer to lift.',
           'Intent is strong and consistent. The build is in volume, saves, comments, and retention are where the next step up lives.', "beat4:pattern")

# quarter view: Q2 complete, Q3 current
html = sub(html,
    '<div class="qy-col current"><div class="qy-q">Q2</div><div class="qy-range">Apr&ndash;Jun</div><div class="qy-avg">7.9<span class="u">/10</span></div><div class="qy-badge building">Building</div><div class="qy-bars"><span style="height:62%"></span><span style="height:64%"></span><span class="cur" style="height:45%"></span></div><div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> click-through climbed to 15.4%, above target, and conversion was the strongest stage.</div><div class="qy-tline"><span class="qy-tl">Watched:</span> engagement depth softened across saves, comments, and retention, and reach eased in June.</div></div><div class="qy-state">Complete</div></div><div class="qy-col "><div class="qy-q">Q3</div><div class="qy-range">Jul&ndash;Sep</div><div class="qy-note">Begins July</div><div class="qy-state">Pending</div></div>',
    '<div class="qy-col "><div class="qy-q">Q2</div><div class="qy-range">Apr&ndash;Jun</div><div class="qy-avg">7.9<span class="u">/10</span></div><div class="qy-badge building">Building</div><div class="qy-bars"><span style="height:62%"></span><span style="height:64%"></span><span style="height:45%"></span></div><div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> click-through above target all quarter, conversion the strongest stage.</div><div class="qy-tline"><span class="qy-tl">Watched:</span> engagement depth softened before turning back up in July.</div></div><div class="qy-state">Complete</div></div><div class="qy-col current"><div class="qy-q">Q3</div><div class="qy-range">Jul&ndash;Sep</div><div class="qy-avg">8.0<span class="u">/10</span></div><div class="qy-badge building">Building</div><div class="qy-bars"><span class="cur" style="height:70%"></span></div><div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> every tracked metric improved from June, led by a 15.6% click-through rate.</div><div class="qy-tline"><span class="qy-tl">Watched:</span> saves, comments, and retention are the volume metrics still building.</div></div><div class="qy-state">In progress</div></div>',
    "beat4:qy")
html = sub(html, '<div class="mscore-cell current"><div class="mscore-m">Jun</div><div class="mscore-v">7.5</div></div>', '<div class="mscore-cell"><div class="mscore-m">Jun</div><div class="mscore-v">7.5</div></div>', "mscore:jun")
html = sub(html, '<div class="mscore-cell empty"><div class="mscore-m">Jul</div><div class="mscore-v">&middot;</div></div>', '<div class="mscore-cell current"><div class="mscore-m">Jul</div><div class="mscore-v">8.0</div></div>', "mscore:jul")

html = sub(html, 'Next month we widen reach with discovery-first Reels and lean into save-driving education (the four Cs, custom-design walkthroughs) to rebuild engagement, while the conversion path holds.',
           'We lead with save-worthy and comment-driving formats to lift the volume metrics, and keep the conversion engine steady.', "beat5:takeaway")
html = sub(html, 'Where our attention is in July', 'Where our attention is in August', "beat5:focus")
html = sub(html, '&middot; June 2026 Performance Report<br>', '&middot; July 2026 Performance Report<br>', "footer")

os.makedirs(OUT_DIR, exist_ok=True); open(OUT,"w",encoding="utf-8").write(html)
print(f"score {R['final']} (raw {R['raw']:.3f}, credit {R['credit']:+.2f}); wrote {OUT} ({len(edits)} edits)")

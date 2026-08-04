#!/usr/bin/env python3
"""build_defineoakley_july.py -- DEFINE Oakley June->July 2026 (standard, retention-critical rebound).
Anchored/hard-fail; score via score_report.py. Post-dependent Beat 2/4 cards finalized after the pull.
Trajectory panel left as-is (v8.5)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score_report as sr

REPO = "/Users/chase.gianattasio/Desktop/scroll-reports"
SRC = f"{REPO}/defineoakley/june2026/index.html"
OUT_DIR = f"{REPO}/defineoakley/july2026"; OUT = f"{OUT_DIR}/index.html"

JULY = {"saves":68,"ctr":7.7,"retention":47,"pcr":8.1,"link_taps":56,"profile_visits":730,"comments":401,"new_followers":59,"total_views":70666,"shares":466}
JUNE = {"saves":111,"ctr":4.7,"retention":65,"pcr":5.7,"link_taps":29,"profile_visits":616,"comments":67,"new_followers":35,"total_views":68917,"shares":273}
R = sr.score(JULY, "Lift", JUNE); assert R["final"] == 8.3, R["final"]

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

html = sub(html, "<title>DEFINE Oakley &ndash; June 2026 | Scroll Media</title>", "<title>DEFINE Oakley &ndash; July 2026 | Scroll Media</title>", "title")
html = sub(html, 'DEFINE Oakley June 2026 Instagram performance report. Score 7.8/10. Building Month.', 'DEFINE Oakley July 2026 Instagram performance report. Score 8.3/10. Solid Month.', "meta:desc")
html = sub(html, 'content="DEFINE Oakley, June 2026 Performance Report"', 'content="DEFINE Oakley, July 2026 Performance Report"', "og:title")
html = sub(html, 'content="Monthly score 7.8/10. Building Month. Prepared by Scroll Media.">', 'content="Monthly score 8.3/10. Solid Month. Prepared by Scroll Media.">', "og:desc")

html = sub(html, '<div class="hero-eyebrow"><span class="dot"></span>June 2026 Performance Report</div>', '<div class="hero-eyebrow"><span class="dot"></span>July 2026 Performance Report</div>', "hero:eyebrow")
html = sub(html, 'Lift Stage &middot; Month 17', 'Lift Stage &middot; Month 18', "hero:stage")
html = sub(html, '<span>June 1&ndash;30, 2026</span>', '<span>July 1&ndash;31, 2026</span>', "hero:window")
html = sub(html, '<div class="ph-bignum">7.8<span class="unit">/10</span></div>\n        <p class="ph-title">Building Month</p>\n        <span class="ph-delta up">&#9650; 0.1 vs. May</span>',
           '<div class="ph-bignum">8.3<span class="unit">/10</span></div>\n        <p class="ph-title">Solid Month</p>\n        <span class="ph-delta up">&#9650; 0.5 vs. June</span>', "hero:score")
html = sub(html, '<span class="ph-badge exceed"><span class="bd"></span>0 Exceeding</span>\n          <span class="ph-badge ontrack"><span class="bd"></span>6 On Track</span>\n          <span class="ph-badge watch"><span class="bd"></span>4 Watch</span>',
           '<span class="ph-badge exceed"><span class="bd"></span>3 Exceeding</span>\n          <span class="ph-badge ontrack"><span class="bd"></span>3 On Track</span>\n          <span class="ph-badge watch"><span class="bd"></span>4 Watch</span>', "hero:badges")
html = sub(html, '<p class="ph-label">Bio Link Engagement</p>\n        <div class="ph-bignum">29</div>', '<p class="ph-label">Bio Link Engagement</p>\n        <div class="ph-bignum">56</div>', "hero:outcome")
html = sub(html, '<p class="hero-summary"><strong>June held the account at its true baseline after April&rsquo;s viral spike. Retention and saves led the month.</strong></p>',
           '<p class="hero-summary"><strong>A strong rebound. Comments jumped sixfold to 401, shares and click-through both broke above your ceiling, and eight of ten metrics improved from June.</strong></p>', "hero:summary")

html = sub(html, 'Retention held at your stage ceiling and saves came back strong, up sharply. Post-viral traffic settled, so a clearer first-class offer is the lever to rebuild booking taps.',
           'Engagement and conversion led the month. Comments and shares surged, click-through hit 7.7% above your 3 to 6% range, and link taps nearly doubled.', "beat3:takeaway")
html = sub(html, '<div class="bstats"><div class="bstat"><div class="bstat-val ontrack">65%</div><div class="bstat-lbl">Video retention</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val ontrack">111</div><div class="bstat-lbl">Saves</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val ontrack">273</div><div class="bstat-lbl">Shares</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val watch">29</div><div class="bstat-lbl">Bio link taps</div><span class="bstat-tag watch">Watch</span></div></div>',
           '<div class="bstats"><div class="bstat"><div class="bstat-val exceed">401</div><div class="bstat-lbl">Comments</div><span class="bstat-tag exceed">Exceeding</span></div><div class="bstat"><div class="bstat-val exceed">466</div><div class="bstat-lbl">Shares</div><span class="bstat-tag exceed">Exceeding</span></div><div class="bstat"><div class="bstat-val exceed">7.7%</div><div class="bstat-lbl">Click-through rate</div><span class="bstat-tag exceed">Exceeding</span></div><div class="bstat"><div class="bstat-val watch">47%</div><div class="bstat-lbl">Video retention</div><span class="bstat-tag watch">Watch</span></div></div>', "beat3:bstats")

# goal tracker: TOFU 45->56 (1.25->1.55), MOFU 53->42 (2.9->2.3), BOFU 36->64 (1.8->3.2)
html = sub(html, '<div class="gt-bar-fill lime" data-w="45" style="width:0%"></div></div>\n            <span class="gt-pct">45%</span>', '<div class="gt-bar-fill lime" data-w="56" style="width:0%"></div></div>\n            <span class="gt-pct">56%</span>', "gt:tofu-bar")
html = sub(html, '1.25<span class="gt-score-max">/2.75</span>', '1.55<span class="gt-score-max">/2.75</span>', "gt:tofu-pts")
html = sub(html, '<div class="gt-bar-fill lime" data-w="53" style="width:0%"></div></div>\n            <span class="gt-pct">53%</span>', '<div class="gt-bar-fill lime" data-w="42" style="width:0%"></div></div>\n            <span class="gt-pct">42%</span>', "gt:mofu-bar")
html = sub(html, '2.9<span class="gt-score-max">/5.5</span>', '2.3<span class="gt-score-max">/5.5</span>', "gt:mofu-pts")
html = sub(html, '<div class="gt-bar-fill lime" data-w="36" style="width:0%"></div></div>\n            <span class="gt-pct">36%</span>', '<div class="gt-bar-fill lime" data-w="64" style="width:0%"></div></div>\n            <span class="gt-pct">64%</span>', "gt:bofu-bar")
html = sub(html, '1.8<span class="gt-score-max">/5.0</span>', '3.2<span class="gt-score-max">/5.0</span>', "gt:bofu-pts")

html = sub(html, 'Your awareness stage scored 45% this month. Shares climbed and views settled to a healthy post-viral baseline. New followers sit under the Lift floor, and rebuilding reach volume is what pulls the follow along behind it.',
           'Your awareness stage scored 56%, up from June. Shares broke above the ceiling and views held their baseline, while new followers stayed under the Lift floor. Rebuilding follower volume is what pulls the rest along.', "narr:tofu")
html = sub(html, 'Your engagement stage scored 53%, the strongest of the three. Retention held at the Lift ceiling and saves came back strong, up 208% and back inside range. Comments eased as post-viral spikes settled. The engagement core is healthy.',
           'Your engagement stage scored 42%. Comments broke out well above the ceiling, but retention slipped from its June high and saves eased, which pulled the layer down. Rebuilding retention is the clear focus.', "narr:mofu")
html = sub(html, 'Your conversion stage scored 36%. Click-through improved and holds inside range, while link taps and profile conversion slipped just under their Lift floors as post-viral traffic normalized. A clearer first-class offer in the bio is the July lever.',
           'Your conversion stage scored 64%, up sharply from June. Click-through cleared the Lift ceiling at 7.7% and link taps nearly doubled back inside range. A clearer first-class offer keeps that momentum going.', "narr:bofu")

html = sub(html, '<p class="sec-label">June 2026</p>', '<p class="sec-label">July 2026</p>', "perf:label")
html = sub(html, 'Every tracked metric for June, scored against your Lift Stage target ranges with month-over-month comparison.', 'Every tracked metric for July, scored against your Lift Stage target ranges with month-over-month comparison.', "perf:sub")
html = sub(html, '<div class="fb-count">3,806</div>\n        <div class="fb-mom"><span class="mom up">&#9650; 0.2% vs. May</span></div>', '<div class="fb-count">3,839</div>\n        <div class="fb-mom"><span class="mom up">&#9650; 0.9% vs. June</span></div>', "followers")

C = [
 ("New Followers","100 &ndash; 270","watch","Watch","35","dn","&#9660; 20% vs May","13","Below the Lift floor. Reach held, but fewer views converted to follows this month.","New followers fell 20%. Translation: 20% fewer people chose to keep seeing your content after finding you. A new follow is someone deciding you are worth coming back to.",
  "watch","Watch","59","up","&#9650; 69% vs June","22","Below the Lift floor but up from June. Reach grew, and more of it is converting to follows.","New followers rose 69%. Translation: 69% more people chose to keep seeing your content after finding you. A new follow is someone deciding you are worth coming back to."),
 ("Shares","60 &ndash; 300","ontrack","On Track","273","up","&#9650; 31% vs May","91","Inside range and up from May. Shareable content is traveling well.","Shares grew 31%. Translation: 31% more people sent your content to someone else. Shares put you in front of new audiences your posts wouldn&rsquo;t reach on their own.",
  "exceed","Exceeding","466","up","&#9650; 71% vs June","100","Above the Lift ceiling. Shareable content traveled further than any month this quarter.","Shares rose 71%. Translation: 71% more people sent your content to someone else. Shares put you in front of new audiences your posts wouldn&rsquo;t reach on their own."),
 ("Total Views","40,000 &ndash; 150,000","ontrack","On Track","68,917","dn","&#9660; 8% vs May","46","Inside range. Post-viral reach settling to a healthy baseline.","Views fell 8%. Translation: your content reached 8% fewer screens this month. Views are the widest measure of how many people you got in front of, and everything downstream starts here.",
  "ontrack","On Track","70,666","up","&#9650; 3% vs June","47","Inside range and up slightly from June. Reach holding at a healthy baseline.","Views rose 3%. Translation: your content reached 3% more screens this month. Views are the widest measure of how many people you got in front of, and everything downstream starts here."),
 ("Profile Visits","300 &ndash; 2,000","ontrack","On Track","616","dn","&#9660; 7% vs May","31","Inside range. Consideration traffic held near May.","Profile visits fell 7%. Translation: 7% fewer people tapped through to look closer at who you are. A profile visit is a deliberate step toward becoming a customer, not a passive scroll.",
  "ontrack","On Track","730","up","&#9650; 19% vs June","37","Inside range and up from June. Consideration traffic grew.","Profile visits rose 19%. Translation: 19% more people tapped through to look closer at who you are. A profile visit is a deliberate step toward becoming a customer, not a passive scroll."),
 ("Retention","50% &ndash; 65%","ontrack","On Track","65%","up","&#9650; 4 pts vs May","100","At the Lift ceiling and up from May. Retention was a standout this month.","Retention came in at 65%. Translation: on average, people watched 65% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences.",
  "watch","Watch","47%","dn","&#9660; 18 pts vs June","72","Below the Lift floor and down from June&rsquo;s ceiling month. Tighter pacing and front-loaded hooks are the clear focus.","Retention came in at 47%. Translation: on average, people watched 47% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences."),
 ("Saves","80 &ndash; 400","ontrack","On Track","111","up","&#9650; 208% vs May","28","Back inside range and up sharply from May. Save-worthy content landed.","Saves grew 208%. Translation: 208% more people bookmarked your posts to act on later. Saves are the strongest signal of a future buyer.",
  "watch","Watch","68","dn","&#9660; 39% vs June","17","Below floor, eased from June. Save-worthy how-to and class content is the lever to rebuild it.","Saves fell 39%. Translation: 39% fewer people bookmarked your posts to act on later. Saves are the strongest signal of a future buyer."),
 ("Comments","75 &ndash; 250","watch","Watch","67","dn","&#9660; 21% vs May","27","Just below floor and down from May as post-viral spikes settled.","Comments fell 21%. Translation: 21% fewer people stopped to start a conversation with you. Comments are public proof that your audience is engaged, and they pull in the people watching from the sidelines.",
  "exceed","Exceeding","401","up","&#9650; 6x vs June","100","Well above the Lift ceiling. Conversation content broke out this month.","Comments jumped sixfold. Translation: six times as many people stopped to start a conversation with you. Comments are public proof that your audience is engaged, and they pull in the people watching from the sidelines."),
 ("CTR","3% &ndash; 6%","ontrack","On Track","4.7%","up","&#9650; 0.8 pts vs May","78","Inside range and up from May. The bio link converts the traffic it gets.","Click-through rate came in at 4.7%. Translation: of everyone who saw your link, 4.7% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers.",
  "exceed","Exceeding","7.7%","up","&#9650; 3 pts vs June","100","Above the Lift ceiling and up from June. The bio link is converting the traffic it gets.","Click-through rate came in at 7.7%. Translation: of everyone who saw your link, 7.7% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers."),
 ("Bio Link Taps","30 &ndash; 180","watch","Watch","29","up","&#9650; 12% vs May","16","Just under the Lift floor. Traffic normalized post-viral; a clearer offer is the July lever.","Link taps grew 12%. Translation: 12% more people tapped the link in your bio to move toward your site, booking, or offer. A link tap is one of the clearest actions someone takes when they are ready to do business.",
  "ontrack","On Track","56","up","&#9650; 93% vs June","31","Back inside range and nearly doubled from June. Booking-path traffic recovered.","Link taps rose 93%. Translation: 93% more people tapped the link in your bio to move toward your site, booking, or offer. A link tap is one of the clearest actions someone takes when they are ready to do business."),
 ("PCR","10% &ndash; 16%","watch","Watch","5.7%","dn","&#9660; 0.9 pts vs May","36","Below floor. Profile-to-follower conversion softened as reach normalized.","Profile conversion came in at 5.7%. Translation: 5.7% of the people who visited your profile chose to follow. A strong profile conversion rate means your page is doing its job, turning curious visitors into an audience you can nurture toward buying.",
  "watch","Watch","8.1%","up","&#9650; 2.4 pts vs June","51","Below floor but up from June. Profile-to-follower conversion is recovering.","Profile conversion came in at 8.1%. Translation: 8.1% of the people who visited your profile chose to follow. A strong profile conversion rate means your page is doing its job, turning curious visitors into an audience you can nurture toward buying."),
]
for c in C:
    old = block(c[0],c[1],c[2],c[3],"June",c[4],c[5],c[6],c[7],c[8],c[9])
    new = block(c[0],c[1],c[10],c[11],"July",c[12],c[13],c[14],c[15],c[16],c[17])
    html = sub(html, old, new, f"mc:{c[0]}")

html = sub(html,
    '<div class="c2b-step"><span class="c2b-step-num">68,917</span><div class="c2b-step-main"><span class="c2b-step-txt">people saw your content</span><span class="c2b-step-badge">\U0001F3DF Great American Ball Park filled 1.6x over</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">616</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped through to look closer</span><span class="c2b-step-badge">\U0001F3BC a Music Hall main-floor crowd</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">111</span><div class="c2b-step-main"><span class="c2b-step-txt">bookmarked content to reference later</span><span class="c2b-step-badge">\U0001F4CC 111 pre-purchase bookmarks</span></div></div>\n'
    '        <div class="c2b-step hi"><span class="c2b-step-num">29</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped a bio link, the highest-intent signal we track</span><span class="c2b-step-badge">\U0001F446 29 deliberate steps toward booking a class</span></div></div>',
    '<div class="c2b-step"><span class="c2b-step-num">70,666</span><div class="c2b-step-main"><span class="c2b-step-txt">people saw your content</span><span class="c2b-step-badge">\U0001F3DF Great American Ball Park filled 1.6x over</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">730</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped through to look closer</span><span class="c2b-step-badge">\U0001F3BC a Music Hall main-floor crowd</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">68</span><div class="c2b-step-main"><span class="c2b-step-txt">bookmarked content to reference later</span><span class="c2b-step-badge">\U0001F4CC 68 pre-purchase bookmarks</span></div></div>\n'
    '        <div class="c2b-step hi"><span class="c2b-step-num">56</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped a bio link, the highest-intent signal we track</span><span class="c2b-step-badge">\U0001F446 56 deliberate steps toward booking a class</span></div></div>',
    "c2b:funnel")

html = sub(html, 'The save-and-share format is what signals a member about to book.',
           'The conversation content worked. Retention is the one signal that slipped this month, from 65% to 47%, so it is the clear focus.', "beat4:pattern")

# quarter view: Q2 complete, Q3 current
html = sub(html,
    '<div class="qy-col current"><div class="qy-q">Q2</div><div class="qy-range">Apr&ndash;Jun</div><div class="qy-avg">8.2<span class="u">/10</span></div><div class="qy-badge mixed">Mixed</div><div class="qy-bars"><span style="height:89%"></span><span style="height:51%"></span><span class="cur" style="height:54%"></span></div><div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> April was a break-out month, and retention held at ceiling while saves rebounded in June.</div><div class="qy-tline"><span class="qy-tl">Watched:</span> post-viral traffic normalized with link taps and profile conversion below floor, and new followers below floor.</div></div><div class="qy-state">Complete</div></div><div class="qy-col "><div class="qy-q">Q3</div><div class="qy-range">Jul&ndash;Sep</div><div class="qy-note">Begins July</div><div class="qy-state">Pending</div></div>',
    '<div class="qy-col "><div class="qy-q">Q2</div><div class="qy-range">Apr&ndash;Jun</div><div class="qy-avg">8.2<span class="u">/10</span></div><div class="qy-badge mixed">Mixed</div><div class="qy-bars"><span style="height:89%"></span><span style="height:51%"></span><span style="height:54%"></span></div><div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> April was a break-out month, and engagement rebounded into a strong July.</div><div class="qy-tline"><span class="qy-tl">Watched:</span> post-viral traffic normalized with link taps and new followers below floor.</div></div><div class="qy-state">Complete</div></div><div class="qy-col current"><div class="qy-q">Q3</div><div class="qy-range">Jul&ndash;Sep</div><div class="qy-avg">8.3<span class="u">/10</span></div><div class="qy-badge strong">Strong</div><div class="qy-bars"><span class="cur" style="height:83%"></span></div><div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> comments jumped sixfold, shares and click-through broke above the ceiling, and link taps nearly doubled.</div><div class="qy-tline"><span class="qy-tl">Watched:</span> retention slipped from 65% to 47%, the clear focus going forward.</div></div><div class="qy-state">In progress</div></div>',
    "beat4:qy")
html = sub(html, '<div class="mscore-cell current"><div class="mscore-m">Jun</div><div class="mscore-v">7.8</div></div>', '<div class="mscore-cell"><div class="mscore-m">Jun</div><div class="mscore-v">7.8</div></div>', "mscore:jun")
html = sub(html, '<div class="mscore-cell empty"><div class="mscore-m">Jul</div><div class="mscore-v">&middot;</div></div>', '<div class="mscore-cell current"><div class="mscore-m">Jul</div><div class="mscore-v">8.3</div></div>', "mscore:jul")

html = sub(html, 'Next month we sharpen the first-class offer in the bio and test a comment-to-DM trigger, turning the high save and comment volume into booking conversations.',
           'We rebuild retention with tighter pacing and front-loaded hooks, and carry the comment and share momentum forward.', "beat5:takeaway")
html = sub(html, 'Where our attention is in July', 'Where our attention is in August', "beat5:focus")
html = sub(html,
    '<div class="tw-item tests"><p class="tw-item-head">First-class offer in the bio</p><p class="tw-item-body">In July, our attention is on a sharper first-class offer in the bio link, giving the retained attention a clear, low-friction next step toward booking.</p></div>',
    '<div class="tw-item tests"><p class="tw-item-head">Rebuild retention</p><p class="tw-item-body">In August, our attention is on retention: tighter pacing and front-loaded hooks to bring watch-time back toward the 50% Lift floor without losing the reach that is working.</p></div>', "beat5:tw1")
html = sub(html,
    '<div class="tw-item tests"><p class="tw-item-head">ManyChat comment-to-DM trigger</p><p class="tw-item-body">We&rsquo;re testing a comment-to-DM trigger for class inquiries, turning the high comment and save volume into direct booking conversations.</p></div>',
    '<div class="tw-item tests"><p class="tw-item-head">Carry the comment and share momentum</p><p class="tw-item-body">The conversation and share surge is worth pressing. We keep the community and class-culture formats that drove it and turn that volume into booking conversations.</p></div>', "beat5:tw2")

html = sub(html, '&middot; June 2026 Performance Report<br>', '&middot; July 2026 Performance Report<br>', "footer")

os.makedirs(OUT_DIR, exist_ok=True); open(OUT,"w",encoding="utf-8").write(html)
print(f"score {R['final']} (raw {R['raw']:.3f}, credit {R['credit']:+.2f}); wrote {OUT} ({len(edits)} edits)")

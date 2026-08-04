#!/usr/bin/env python3
"""build_upandrunningoh_july.py -- Up and Running June->July 2026 (Spark, honest down month 8.3->7.5).
Anchored/hard-fail; score via score_report.py (Spark ranges). Post-dependent Beat 2/4 finalized after pull.
Trajectory panel left as-is (v8.5). Client name is "Up and Running" (spelled out) per CLAUDE.md."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score_report as sr

REPO = "/Users/chase.gianattasio/Desktop/scroll-reports"
SRC = f"{REPO}/upandrunningoh/june2026/index.html"
OUT_DIR = f"{REPO}/upandrunningoh/july2026"; OUT = f"{OUT_DIR}/index.html"

JULY = {"saves":2,"ctr":3.8,"retention":33,"pcr":8.7,"link_taps":11,"profile_visits":287,"comments":18,"new_followers":25,"total_views":18220,"shares":56}
JUNE = {"saves":11,"ctr":3.9,"retention":66,"pcr":12.5,"link_taps":10,"profile_visits":257,"comments":11,"new_followers":32,"total_views":18506,"shares":56}
R = sr.score(JULY, "Spark", JUNE); assert R["final"] == 7.5, R["final"]

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

html = sub(html, "<title>Up and Running &ndash; June 2026 | Scroll Media</title>", "<title>Up and Running &ndash; July 2026 | Scroll Media</title>", "title")
html = sub(html, 'Up and Running June 2026 Instagram performance report. Score 8.3/10. Solid Month.', 'Up and Running July 2026 Instagram performance report. Score 7.5/10. Building Month.', "meta:desc")
html = sub(html, 'content="Up and Running, June 2026 Performance Report"', 'content="Up and Running, July 2026 Performance Report"', "og:title")
html = sub(html, 'content="Monthly score 8.3/10. Solid Month. Prepared by Scroll Media.">', 'content="Monthly score 7.5/10. Building Month. Prepared by Scroll Media.">', "og:desc")

html = sub(html, '<div class="hero-eyebrow"><span class="dot"></span>June 2026 Performance Report</div>', '<div class="hero-eyebrow"><span class="dot"></span>July 2026 Performance Report</div>', "hero:eyebrow")
html = sub(html, 'Spark Stage &middot; Month 9', 'Spark Stage &middot; Month 10', "hero:stage")
html = sub(html, '<span>June 1&ndash;30, 2026</span>', '<span>July 1&ndash;31, 2026</span>', "hero:window")
html = sub(html, '<div class="ph-bignum">8.3<span class="unit">/10</span></div>\n        <p class="ph-title">Solid Month</p>\n        <span class="ph-delta up">&#9650; 0.4 vs. May</span>',
           '<div class="ph-bignum">7.5<span class="unit">/10</span></div>\n        <p class="ph-title">Building Month</p>\n        <span class="ph-delta dn">&#9660; 0.8 vs. June</span>', "hero:score")
html = sub(html, '<span class="ph-badge exceed"><span class="bd"></span>1 Exceeding</span>\n          <span class="ph-badge ontrack"><span class="bd"></span>6 On Track</span>\n          <span class="ph-badge watch"><span class="bd"></span>3 Watch</span>',
           '<span class="ph-badge exceed"><span class="bd"></span>0 Exceeding</span>\n          <span class="ph-badge ontrack"><span class="bd"></span>6 On Track</span>\n          <span class="ph-badge watch"><span class="bd"></span>4 Watch</span>', "hero:badges")
html = sub(html, '<p class="ph-label">Bio Link Engagement</p>\n        <div class="ph-bignum">10</div>', '<p class="ph-label">Bio Link Engagement</p>\n        <div class="ph-bignum">11</div>', "hero:outcome")
html = sub(html, '<p class="hero-summary"><strong>June was a recovery month. Retention broke through, community re-engaged, and your reach base rebuilt.</strong></p>',
           '<p class="hero-summary"><strong>A softer month. Several signals held steady, but retention and saves dipped and are the focus going into next month.</strong></p>', "hero:summary")

html = sub(html, 'The month recovered across the board. Retention hit 66%, above your stage ceiling, and community engagement climbed sharply.',
           'Six of ten metrics stayed on track, including click-through and link taps, but retention fell from 66% to 33% and saves dropped to 2, which pulled the month down.', "beat3:takeaway")
html = sub(html, '<div class="bstats"><div class="bstat"><div class="bstat-val exceed">66%</div><div class="bstat-lbl">Video retention</div><span class="bstat-tag exceed">Exceeding</span></div><div class="bstat"><div class="bstat-val ontrack">56</div><div class="bstat-lbl">Shares</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val ontrack">257</div><div class="bstat-lbl">Profile visits</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val watch">11</div><div class="bstat-lbl">Saves</div><span class="bstat-tag watch">Watch</span></div></div>',
           '<div class="bstats"><div class="bstat"><div class="bstat-val ontrack">3.8%</div><div class="bstat-lbl">Click-through rate</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val ontrack">11</div><div class="bstat-lbl">Bio link taps</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val watch">33%</div><div class="bstat-lbl">Video retention</div><span class="bstat-tag watch">Watch</span></div><div class="bstat"><div class="bstat-val watch">2</div><div class="bstat-lbl">Saves</div><span class="bstat-tag watch">Watch</span></div></div>', "beat3:bstats")

# goal tracker: TOFU unchanged (45%); MOFU 49->35 (2.7->1.9), BOFU 60->48 (3.0->2.4)
html = sub(html, '<div class="gt-bar-fill lime" data-w="49" style="width:0%"></div></div>\n            <span class="gt-pct">49%</span>', '<div class="gt-bar-fill lime" data-w="35" style="width:0%"></div></div>\n            <span class="gt-pct">35%</span>', "gt:mofu-bar")
html = sub(html, '2.7<span class="gt-score-max">/5.5</span>', '1.9<span class="gt-score-max">/5.5</span>', "gt:mofu-pts")
html = sub(html, '<div class="gt-bar-fill lime" data-w="60" style="width:0%"></div></div>\n            <span class="gt-pct">60%</span>', '<div class="gt-bar-fill lime" data-w="48" style="width:0%"></div></div>\n            <span class="gt-pct">48%</span>', "gt:bofu-bar")
html = sub(html, '3.0<span class="gt-score-max">/5.0</span>', '2.4<span class="gt-score-max">/5.0</span>', "gt:bofu-pts")

html = sub(html, 'Your awareness stage scored 45% this month, up from May. Shares jumped and views rebuilt as community-event content traveled. New followers sit just under the Spark floor, and widening reach is what pulls the follow along behind it.',
           'Your awareness stage scored 45%, level with June. Shares held and views stayed steady, while new followers eased under the Spark floor. Widening reach is what pulls the follow along.', "narr:tofu")
html = sub(html, 'Your engagement stage scored 49%. Retention broke through the Spark ceiling at 66% and carried this stage, while saves and comments still sit below their floors. Save-worthy carousels are the July lever to bring the rest of the layer up.',
           'Your engagement stage scored 35%, down from June. Retention fell from its 66% breakout and saves dropped to 2, which pulled the layer down, though comments recovered. Save-worthy carousels and stronger hooks are the levers to rebuild it.', "narr:mofu")
html = sub(html, 'Your conversion stage scored 60%, the strongest of the three. Click-through, link taps, and profile conversion all held inside their Spark ranges and improved from May. The conversion path is efficient; the job is feeding it more volume from the top.',
           'Your conversion stage scored 48%. Click-through and link taps held inside their Spark ranges, while profile conversion eased under floor as reach softened. The conversion path is efficient; the job is feeding it more volume from the top.', "narr:bofu")

html = sub(html, '<p class="sec-label">June 2026</p>', '<p class="sec-label">July 2026</p>', "perf:label")
html = sub(html, 'Every tracked metric for June, scored against your Spark Stage target ranges with month-over-month comparison.', 'Every tracked metric for July, scored against your Spark Stage target ranges with month-over-month comparison.', "perf:sub")
html = sub(html, '<div class="fb-count">2,372</div>\n        <div class="fb-mom"><span class="mom up">&#9650; 0.7% vs. May</span></div>', '<div class="fb-count">2,380</div>\n        <div class="fb-mom"><span class="mom up">&#9650; 0.3% vs. June</span></div>', "followers")

C = [
 ("New Followers","40 &ndash; 90","watch","Watch","32","dn","&#9660; 9% vs May","36","Just under the Spark floor. Reach and shares climbed, so the follow tends to follow.","New followers fell 9%. Translation: 9% fewer people chose to keep seeing your content after finding you. A new follow is someone deciding you are worth coming back to.",
  "watch","Watch","25","dn","&#9660; 22% vs June","28","Below the Spark floor and down from June. Reach softened, so fewer views converted to follows.","New followers fell 22%. Translation: 22% fewer people chose to keep seeing your content after finding you. A new follow is someone deciding you are worth coming back to."),
 ("Shares","15 &ndash; 60","ontrack","On Track","56","up","&#9650; 229% vs May","93","Inside range and up sharply from May. Community-event content is traveling.","Shares grew 229%. Translation: 229% more people sent your content to someone else. Shares put you in front of new audiences your posts wouldn&rsquo;t reach on their own.",
  "ontrack","On Track","56","fl","Flat vs June","93","Inside range and flat from June. Community-event content keeps traveling.","Shares held flat. Translation: the same number of people sent your content to someone else. Shares put you in front of new audiences your posts wouldn&rsquo;t reach on their own."),
 ("Total Views","10,000 &ndash; 40,000","ontrack","On Track","18,506","up","&#9650; 17% vs May","46","Inside range and up from May. The reach base is rebuilding.","Views grew 17%. Translation: your content reached 17% more screens this month. Views are the widest measure of how many people you got in front of, and everything downstream starts here.",
  "ontrack","On Track","18,220","dn","&#9660; 2% vs June","46","Inside range and essentially flat. The reach base held steady.","Views held about flat. Translation: your content reached about the same number of screens this month. Views are the widest measure of how many people you got in front of, and everything downstream starts here."),
 ("Profile Visits","50 &ndash; 500","ontrack","On Track","257","up","&#9650; 22% vs May","51","Inside range and up from May. More people stepping in to look closer.","Profile visits grew 22%. Translation: 22% more people tapped through to look closer at who you are. A profile visit is a deliberate step toward becoming a customer, not a passive scroll.",
  "ontrack","On Track","287","up","&#9650; 12% vs June","57","Inside range and up from June. More people stepping in to look closer.","Profile visits rose 12%. Translation: 12% more people tapped through to look closer at who you are. A profile visit is a deliberate step toward becoming a customer, not a passive scroll."),
 ("Retention","35% &ndash; 50%","exceed","Exceeding","66%","up","&#9650; 34 pts vs May","100","Above the Spark ceiling. Retention-first Reels were the story of the month.","Retention came in at 66%. Translation: on average, people watched 66% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences.",
  "watch","Watch","33%","dn","&#9660; 33 pts vs June","66","Below the Spark floor and down sharply from June&rsquo;s breakout. Stronger hooks and tighter edits are the clear focus.","Retention came in at 33%. Translation: on average, people watched 33% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences."),
 ("Saves","20 &ndash; 80","watch","Watch","11","dn","&#9660; 15% vs May","14","Below floor. Save-worthy carousels are the July lever to lift this.","Saves fell 15%. Translation: 15% fewer people bookmarked your posts to act on later. Saves are the strongest signal of a future buyer.",
  "watch","Watch","2","dn","&#9660; 82% vs June","3","Well below floor and down from June. Save-worthy fit guides and how-tos are the lever to rebuild it.","Saves fell 82%. Translation: far fewer people bookmarked your posts to act on later. Saves are the strongest signal of a future buyer."),
 ("Comments","15 &ndash; 75","watch","Watch","11","up","&#9650; 267% vs May","15","Below floor but up sharply from May. Conversation is restarting.","Comments grew 267%. Translation: 267% more people stopped to start a conversation with you. Comments are public proof that your audience is engaged, and they pull in the people watching from the sidelines.",
  "ontrack","On Track","18","up","&#9650; 64% vs June","24","Back inside range and up from June. Conversation is picking up.","Comments rose 64%. Translation: 64% more people stopped to start a conversation with you. Comments are public proof that your audience is engaged, and they pull in the people watching from the sidelines."),
 ("CTR","3% &ndash; 8%","ontrack","On Track","3.9%","up","&#9650; 0.6 pts vs May","49","Inside range and up from May. The bio link converts the traffic it gets.","Click-through rate came in at 3.9%. Translation: of everyone who saw your link, 3.9% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers.",
  "ontrack","On Track","3.8%","dn","&#9660; 0.1 pts vs June","48","Inside range and essentially flat. The bio link keeps converting the traffic it gets.","Click-through rate came in at 3.8%. Translation: of everyone who saw your link, 3.8% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers."),
 ("Bio Link Taps","5 &ndash; 40","ontrack","On Track","10","up","&#9650; 43% vs May","25","Inside range and up from May. Still thin, and July reach growth feeds it.","Link taps grew 43%. Translation: 43% more people tapped the link in your bio to move toward your site, booking, or offer. A link tap is one of the clearest actions someone takes when they are ready to do business.",
  "ontrack","On Track","11","up","&#9650; 10% vs June","28","Inside range and up slightly from June. Still thin, and reach growth is what feeds it.","Link taps rose 10%. Translation: 10% more people tapped the link in your bio to move toward your site, booking, or offer. A link tap is one of the clearest actions someone takes when they are ready to do business."),
 ("PCR","10% &ndash; 18%","ontrack","On Track","12.5%","dn","&#9660; 4.2 pts vs May","69","Inside range. Profile-to-follower conversion held healthy.","Profile conversion came in at 12.5%. Translation: 12.5% of the people who visited your profile chose to follow. A strong profile conversion rate means your page is doing its job, turning curious visitors into an audience you can nurture toward buying.",
  "watch","Watch","8.7%","dn","&#9660; 3.8 pts vs June","48","Just below floor, eased from June. Profile-to-follower conversion is the lever to rebuild.","Profile conversion came in at 8.7%. Translation: 8.7% of the people who visited your profile chose to follow. A strong profile conversion rate means your page is doing its job, turning curious visitors into an audience you can nurture toward buying."),
]
for c in C:
    old = block(c[0],c[1],c[2],c[3],"June",c[4],c[5],c[6],c[7],c[8],c[9])
    new = block(c[0],c[1],c[10],c[11],"July",c[12],c[13],c[14],c[15],c[16],c[17])
    html = sub(html, old, new, f"mc:{c[0]}")

html = sub(html,
    '<div class="c2b-step"><span class="c2b-step-num">18,506</span><div class="c2b-step-main"><span class="c2b-step-txt">people saw your content</span><span class="c2b-step-badge">\U0001F3DF more than 2.5 Dayton Dragons sellouts at Fifth Third Field</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">257</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped through to look closer</span><span class="c2b-step-badge">\U0001F3C3 a packed Saturday group-run turnout</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">11</span><div class="c2b-step-main"><span class="c2b-step-txt">bookmarked content to reference later</span><span class="c2b-step-badge">\U0001F4CC 11 pre-purchase bookmarks</span></div></div>\n'
    '        <div class="c2b-step hi"><span class="c2b-step-num">10</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped a bio link, the highest-intent signal we track</span><span class="c2b-step-badge">\U0001F446 10 deliberate taps toward your shop and fittings</span></div></div>',
    '<div class="c2b-step"><span class="c2b-step-num">18,220</span><div class="c2b-step-main"><span class="c2b-step-txt">people saw your content</span><span class="c2b-step-badge">\U0001F3DF more than 2.5 Dayton Dragons sellouts at Fifth Third Field</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">287</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped through to look closer</span><span class="c2b-step-badge">\U0001F3C3 a packed Saturday group-run turnout</span></div></div>\n'
    '        <div class="c2b-step"><span class="c2b-step-num">2</span><div class="c2b-step-main"><span class="c2b-step-txt">bookmarked content to reference later</span><span class="c2b-step-badge">\U0001F4CC 2 pre-purchase bookmarks</span></div></div>\n'
    '        <div class="c2b-step hi"><span class="c2b-step-num">11</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped a bio link, the highest-intent signal we track</span><span class="c2b-step-badge">\U0001F446 11 deliberate taps toward your shop and fittings</span></div></div>',
    "c2b:funnel")

html = sub(html, 'Save-worthy content is the lever to lift saves.',
           'Your audience is stable and still clicking through. Content depth and save-worthiness are what slipped, so that is where the work goes.', "beat4:pattern")

html = sub(html,
    '<div class="qy-col current"><div class="qy-q">Q2</div><div class="qy-range">Apr&ndash;Jun</div><div class="qy-avg">8.0<span class="u">/10</span></div><div class="qy-badge recovering">Recovering</div><div class="qy-bars"><span style="height:56%"></span><span style="height:56%"></span><span class="cur" style="height:67%"></span></div><div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> June recovered with retention at 66%, and community re-engaged as comments and shares climbed.</div><div class="qy-tline"><span class="qy-tl">Watched:</span> saves stayed below the stage floor, and bio link tap volume is still thin.</div></div><div class="qy-state">Complete</div></div><div class="qy-col "><div class="qy-q">Q3</div><div class="qy-range">Jul&ndash;Sep</div><div class="qy-note">Begins July</div><div class="qy-state">Pending</div></div>',
    '<div class="qy-col "><div class="qy-q">Q2</div><div class="qy-range">Apr&ndash;Jun</div><div class="qy-avg">8.0<span class="u">/10</span></div><div class="qy-badge recovering">Recovering</div><div class="qy-bars"><span style="height:56%"></span><span style="height:56%"></span><span style="height:67%"></span></div><div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> June recovered with retention at 66% and community re-engaged.</div><div class="qy-tline"><span class="qy-tl">Watched:</span> retention gave that back in July, and saves stayed below floor.</div></div><div class="qy-state">Complete</div></div><div class="qy-col current"><div class="qy-q">Q3</div><div class="qy-range">Jul&ndash;Sep</div><div class="qy-avg">7.5<span class="u">/10</span></div><div class="qy-badge softening">Softening</div><div class="qy-bars"><span class="cur" style="height:60%"></span></div><div class="qy-theme"><div class="qy-tline"><span class="qy-tl">Worked:</span> profile visits and comments grew, and click-through and link taps held inside range.</div><div class="qy-tline"><span class="qy-tl">Watched:</span> retention fell from 66% to 33% and saves dropped to 2, the two levers to rebuild.</div></div><div class="qy-state">In progress</div></div>',
    "beat4:qy")
html = sub(html, '<div class="mscore-cell current"><div class="mscore-m">Jun</div><div class="mscore-v">8.3</div></div>', '<div class="mscore-cell"><div class="mscore-m">Jun</div><div class="mscore-v">8.3</div></div>', "mscore:jun")
html = sub(html, '<div class="mscore-cell empty"><div class="mscore-m">Jul</div><div class="mscore-v">&middot;</div></div>', '<div class="mscore-cell current"><div class="mscore-m">Jul</div><div class="mscore-v">7.5</div></div>', "mscore:jul")

html = sub(html, 'Next month we hold the short-form Reel cadence that drove retention and test save-worthy fit guides, while feeding more volume to fittings.',
           'We rebuild retention with stronger hooks and tighter edits, and test save-driven formats like fit guides and how-tos.', "beat5:takeaway")
html = sub(html, 'Where our attention is in July', 'Where our attention is in August', "beat5:focus")
html = sub(html,
    '<div class="tw-item tests"><p class="tw-item-head">Short-form Reels cadence</p><p class="tw-item-body">In July, our attention is on holding the short-form Reel cadence that drove retention this month, pairing the strong opens with clear community-event and product hooks.</p></div>',
    '<div class="tw-item tests"><p class="tw-item-head">Rebuild retention</p><p class="tw-item-body">In August, our attention is on retention: stronger hooks and tighter edits to bring watch-time back above the 35% Spark floor after this month&rsquo;s dip.</p></div>', "beat5:tw1")
html = sub(html,
    '<div class="tw-item tests"><p class="tw-item-head">Save-worthy carousels</p><p class="tw-item-body">We&rsquo;re watching how fit guides and shoe-comparison carousels move saves and comments, the two engagement signals still sitting below the Spark floor.</p></div>',
    '<div class="tw-item tests"><p class="tw-item-head">Save-driven formats</p><p class="tw-item-body">We&rsquo;re testing fit guides and shoe-comparison carousels built to be saved, the clearest lever to lift saves back off the floor.</p></div>', "beat5:tw2")

html = sub(html, '&middot; June 2026 Performance Report<br>', '&middot; July 2026 Performance Report<br>', "footer")

os.makedirs(OUT_DIR, exist_ok=True); open(OUT,"w",encoding="utf-8").write(html)
print(f"score {R['final']} (raw {R['raw']:.3f}, credit {R['credit']:+.2f}); wrote {OUT} ({len(edits)} edits)")

#!/usr/bin/env python3
"""build_meas_correct.py -- apply the §3 corrections to the regenerated MEAS
closeout scaffold (measactive/july2026). Fixes account-level data, restores the
two n/a metrics (New Followers 45, PCR 8.1%), prorates the volume targets,
corrects the goal tracker/score/badges, and splices the fresh injected posts.
Anchored/hard-fail. Score verified 7.8 (prorated, MoM suppressed) via score_report."""
import os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score_report as sr

REPO = "/Users/chase.gianattasio/Desktop/scroll-reports"
F = f"{REPO}/measactive/july2026/index.html"

# ── score guard: prorated Lift ranges, MoM suppressed ─────────────────────────
PRO = {"saves": (57, 284), "ctr": (3, 6), "retention": (50, 65), "pcr": (10, 16),
       "link_taps": (21, 128), "profile_visits": (213, 1419), "comments": (53, 177),
       "new_followers": (71, 192), "total_views": (28387, 106452), "shares": (43, 213)}
sr.TARGETS["Lift"] = PRO
MEAS = {"saves": 18, "ctr": 8.8, "retention": 46, "pcr": 8.1, "link_taps": 49,
        "profile_visits": 557, "comments": 66, "new_followers": 45, "total_views": 30641, "shares": 22}
R = sr.score(MEAS, "Lift", prior=None)
assert R["final"] == 7.8, R["final"]

edits = []
def sub(html, old, new, label):
    n = html.count(old)
    if n != 1: sys.exit(f"ANCHOR FAIL [{label}]: {n} found\n  {old[:150]}")
    edits.append(label); return html.replace(old, new)

def mc(name, cls, lab, val, tgt, bar, note, callout):
    return (f'<div class="mc-top"><span class="mc-name">{name}</span><span class="mc-badge {cls}">{lab}</span></div>\n'
            f'          <div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val {cls}">{val}</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">{tgt}</span></div></div>\n'
            f'          <div class="bar-track"><div class="bar-fill {cls}" data-w="{bar}" style="width:0%"></div></div>\n'
            f'          <p class="mc-note">{note}</p>\n'
            f'          <p class="mc-callout">{callout}</p>')

html = open(F, encoding="utf-8").read()

# ── 1. splice fresh injected ALL_POSTS ───────────────────────────────────────
inj = json.load(open("/tmp/meas_allposts.json", encoding="utf-8"))
for p in inj:  # drop the transient 'dt' key if present
    p.pop("dt", None)
html = re.sub(r'var ALL_POSTS = \[.*?\];', 'var ALL_POSTS = ' + json.dumps(inj, ensure_ascii=False) + ';', html, count=1, flags=re.S)
edits.append("ALL_POSTS(injected)")

# ── 2. hero ──────────────────────────────────────────────────────────────────
html = sub(html, '<div class="ph-bignum">7.6<span class="unit">/10</span></div>', '<div class="ph-bignum">7.8<span class="unit">/10</span></div>', "hero:score")
html = sub(html, '<span class="ph-delta fl">Flat vs. June</span>', '<span class="ph-delta fl">Steady vs. June</span>', "hero:delta")
html = sub(html,
    '<span class="ph-badge exceed"><span class="bd"></span>1 Exceeding</span>\n          <span class="ph-badge ontrack"><span class="bd"></span>2 On Track</span>\n          <span class="ph-badge watch"><span class="bd"></span>5 Watch</span>\n          <span class="ph-badge na"><span class="bd"></span>2 n/a</span>',
    '<span class="ph-badge exceed"><span class="bd"></span>1 Exceeding</span>\n          <span class="ph-badge ontrack"><span class="bd"></span>4 On Track</span>\n          <span class="ph-badge watch"><span class="bd"></span>5 Watch</span>', "hero:badges")
html = sub(html, '<div class="ph-bignum">57</div>', '<div class="ph-bignum">49</div>', "hero:outcome")
html = sub(html,
    'Your score reflects how this window performed against your stage targets, weighted by what predicts buyer behavior. This is a partial window, July 1 to 22, with six published pieces, so volume metrics read lighter than a full month by design. Two metrics are marked not available and are excluded from the score rather than counted as zero.',
    'Your score reflects how this window performed against your stage targets, weighted by what predicts buyer behavior. This is a partial window, July 1 to 22, so the volume targets are prorated to 22 days and the badges read fair for a short month. Rate metrics use their normal ranges.', "hero:method")

# ── 3. beat 3 takeaway + bstats ──────────────────────────────────────────────
html = sub(html,
    'On a fraction of a normal month&rsquo;s volume, click-through held at 9.7% against a 3 to 6% benchmark, and the founder story drove nearly half of all comments.',
    'On a partial window, click-through held at 8.8% against a 3 to 6% benchmark, and the founder story drove over a third of all comments.', "beat3:takeaway")
html = sub(html,
    '<div class="bstat"><div class="bstat-val exceed">9.7%</div><div class="bstat-lbl">Click-through rate</div><span class="bstat-tag exceed">Exceeding</span></div><div class="bstat"><div class="bstat-val watch">54</div><div class="bstat-lbl">Comments</div><span class="bstat-tag watch">Watch</span></div><div class="bstat"><div class="bstat-val ontrack">57</div><div class="bstat-lbl">Bio link taps</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val watch">37.8%</div><div class="bstat-lbl">Video retention</div><span class="bstat-tag watch">Watch</span></div>',
    '<div class="bstat"><div class="bstat-val exceed">8.8%</div><div class="bstat-lbl">Click-through rate</div><span class="bstat-tag exceed">Exceeding</span></div><div class="bstat"><div class="bstat-val ontrack">66</div><div class="bstat-lbl">Comments</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val ontrack">49</div><div class="bstat-lbl">Bio link taps</div><span class="bstat-tag ontrack">On Track</span></div><div class="bstat"><div class="bstat-val watch">46%</div><div class="bstat-lbl">Video retention</div><span class="bstat-tag watch">Watch</span></div>', "beat3:bstats")

# ── 4. goal tracker bars + score-pts (restore full denominators) ─────────────
html = sub(html, 'gt-bar-fill lime" data-w="20" style="width:0%"></div></div>\n            <span class="gt-pct">20%</span>', 'gt-bar-fill lime" data-w="35" style="width:0%"></div></div>\n            <span class="gt-pct">35%</span>', "gt:tofu-bar")
html = sub(html, '<span class="gt-score-pts">0.35<span class="gt-score-max">/1.75</span>', '<span class="gt-score-pts">0.95<span class="gt-score-max">/2.75</span>', "gt:tofu-pts")
html = sub(html, 'gt-bar-fill lime" data-w="27" style="width:0%"></div></div>\n            <span class="gt-pct">27%</span>', 'gt-bar-fill lime" data-w="35" style="width:0%"></div></div>\n            <span class="gt-pct">35%</span>', "gt:mofu-bar")
html = sub(html, '<span class="gt-score-pts">1.5<span class="gt-score-max">/5.5</span>', '<span class="gt-score-pts">1.9<span class="gt-score-max">/5.5</span>', "gt:mofu-pts")
html = sub(html, 'gt-bar-fill lime" data-w="83" style="width:0%"></div></div>\n            <span class="gt-pct">83%</span>', 'gt-bar-fill lime" data-w="64" style="width:0%"></div></div>\n            <span class="gt-pct">64%</span>', "gt:bofu-bar")
html = sub(html, '<span class="gt-score-pts">2.9<span class="gt-score-max">/3.5</span>', '<span class="gt-score-pts">3.2<span class="gt-score-max">/5.0</span>', "gt:bofu-pts")

# goal narratives
html = sub(html,
    'Your awareness stage scored 20% across the window. Six pieces in 22 days is roughly a third of a normal month&rsquo;s output, so views and shares land well under the monthly floors. New followers is not available for this window and is excluded rather than counted as a zero.',
    'Your awareness stage scored 35% across the window. Views landed inside the prorated range while shares and new followers stayed under their prorated floors. Reach held to a healthy per-piece level through the close.', "narr:tofu")
html = sub(html,
    'Your engagement stage scored 27%. Comments held their shape on far less volume, with the founder story alone drawing 24 of the 54. Retention at 37.8% and saves at 15 are the two levers that stayed below target all year, and they remain the clearest room to grow.',
    'Your engagement stage scored 35%. Comments landed inside the prorated range, with the founder story alone drawing 24 of the 66. Retention at 46% and saves at 18 are the two levers that stayed below target all year, and they remain the clearest room to grow.', "narr:mofu")
html = sub(html,
    'Your conversion stage scored 83%, the strongest of the three and the clearest proof point of the year. Click-through finished at 9.7%, above the Lift ceiling and nearly identical to June&rsquo;s 9.8%, and link taps held inside range on a partial window. Profile conversion rate is not available for this window and is excluded rather than counted as a zero.',
    'Your conversion stage scored 64%, the strongest of the three and the clearest proof point of the year. Click-through finished at 8.8%, above the Lift ceiling and close to June&rsquo;s 9.8%, and link taps held inside the prorated range. Profile conversion stayed under floor, the standing lever through the engagement.', "narr:bofu")

# ── 5. perf-sub (proration explanation) ──────────────────────────────────────
html = sub(html,
    'Every tracked metric for the final window, scored against your Lift Stage target ranges. Targets are monthly, so a 22 day window reads lighter on volume metrics by design.',
    'Every tracked metric for the final window, scored against your Lift Stage ranges prorated to the 22-day window so the badges are fair for a partial month. Rate metrics (click-through, retention, profile conversion) use their normal ranges.', "perf:sub")

# ── 6. the 10 metric cards ───────────────────────────────────────────────────
# New Followers: n/a card -> real card
html = sub(html,
    '<div class="mc na">\n          <div class="mc-top"><span class="mc-name">New Followers</span><span class="mc-badge na">Not available</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val na">n/a</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">100 &ndash; 270</span></div></div>\n'
    '          <p class="mc-note">Instagram changed how gross new followers are reported, so this figure is not available for the final window. It is excluded from the score rather than counted as a zero.</p>\n'
    '          <p class="mc-callout">Followers were essentially flat across the window, 10,134 to 10,118. Net movement of 16 accounts over 22 days means the audience you built held steady right through the close.</p>\n        </div>',
    '<div class="mc">\n          ' + mc("New Followers", "watch", "Watch", "45", "71 &ndash; 192", 23,
        "Below the prorated floor on a 22-day window. Net follower movement held essentially flat across the close, 10,134 to 10,118.",
        "New followers came in at 45. Translation: 45 people chose to keep seeing your content after finding you. A new follow is someone deciding you are worth coming back to.") + '\n        </div>',
    "mc:new-followers")

# Shares 19->22 (W)
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Shares</span><span class="mc-badge watch">Watch</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val watch">19</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">60 &ndash; 300</span></div></div>\n'
    '          <div class="mc-mom"><span class="mom dn">&#9660; 27% vs June</span></div>\n'
    '          <div class="bar-track"><div class="bar-fill watch" data-w="6" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Below floor on a partial window. The one carousel out-shared every Reel, which is worth carrying into your format mix.</p>\n'
    '          <p class="mc-callout">Shares landed at 19. Translation: 19 people sent your content to someone else. Shares put you in front of new audiences your posts wouldn&rsquo;t reach on their own.</p>',
    mc("Shares", "watch", "Watch", "22", "43 &ndash; 213", 10,
       "Below the prorated floor. The one carousel out-shared every Reel, worth carrying into the format mix.",
       "Shares landed at 22. Translation: 22 people sent your content to someone else. Shares put you in front of new audiences your posts wouldn&rsquo;t reach on their own."),
    "mc:shares")

# Total Views 10,491 (W) -> 30,641 (OT)
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Total Views</span><span class="mc-badge watch">Watch</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val watch">10,491</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">40,000 &ndash; 150,000</span></div></div>\n'
    '          <div class="mc-mom"><span class="mom dn">&#9660; 80% vs June</span></div>\n'
    '          <div class="bar-track"><div class="bar-fill watch" data-w="7" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Below the monthly floor on six pieces across 22 days. Average reach per piece held at 1,067.</p>\n'
    '          <p class="mc-callout">Views came in at 10,491. Translation: your content reached 10,491 screens in 22 days. Views are the widest measure of how many people you got in front of, and everything downstream starts here.</p>',
    mc("Total Views", "ontrack", "On Track", "30,641", "28,387 &ndash; 106,452", 29,
       "Inside the prorated range on six pieces across 22 days. Account reach held to a healthy level through the close.",
       "Views came in at 30,641. Translation: your content reached 30,641 screens across the final window. Views are the widest measure of how many people you got in front of, and everything downstream starts here."),
    "mc:total-views")

# Profile Visits 585->557 (OT)
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Profile Visits</span><span class="mc-badge ontrack">On Track</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val ontrack">585</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">300 &ndash; 2,000</span></div></div>\n'
    '          <div class="mc-mom"><span class="mom dn">&#9660; 20% vs June</span></div>\n'
    '          <div class="bar-track"><div class="bar-fill ontrack" data-w="29" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Inside range even on a partial window. Consideration traffic stayed healthy to the end.</p>\n'
    '          <p class="mc-callout">Profile visits came in at 585. Translation: 585 people tapped through to look closer at who you are. A profile visit is a deliberate step toward becoming a customer, not a passive scroll.</p>',
    mc("Profile Visits", "ontrack", "On Track", "557", "213 &ndash; 1,419", 39,
       "Inside the prorated range. Consideration traffic stayed healthy to the end.",
       "Profile visits came in at 557. Translation: 557 people tapped through to look closer at who you are. A profile visit is a deliberate step toward becoming a customer, not a passive scroll."),
    "mc:profile-visits")

# Retention 37.8%->46% (W)
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Retention</span><span class="mc-badge watch">Watch</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val watch">37.8%</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">50% &ndash; 65%</span></div></div>\n'
    '          <div class="mc-mom"><span class="mom dn">&#9660; 11.2 pts vs June</span></div>\n'
    '          <div class="bar-track"><div class="bar-fill watch" data-w="58" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Below the Lift floor and the largest single gap in the window. Front-loading the hook is the highest-leverage fix.</p>\n'
    '          <p class="mc-callout">Retention came in at 37.8%. Translation: on average, people watched 37.8% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences.</p>',
    mc("Retention", "watch", "Watch", "46%", "50% &ndash; 65%", 71,
       "Below the Lift floor, the largest standing gap. Front-loading the hook was the highest-leverage fix all year.",
       "Retention came in at 46%. Translation: on average, people watched 46% of your videos before moving on. The more of your video people watch, the more the algorithm trusts it and shows it to new audiences."),
    "mc:retention")

# Saves 15->18 (W)
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Saves</span><span class="mc-badge watch">Watch</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val watch">15</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">80 &ndash; 400</span></div></div>\n'
    '          <div class="mc-mom"><span class="mom dn">&#9660; 32% vs June</span></div>\n'
    '          <div class="bar-track"><div class="bar-fill watch" data-w="4" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Below floor, the same gap flagged every month this year. Save-worthy value content is the standing recommendation.</p>\n'
    '          <p class="mc-callout">Saves landed at 15. Translation: 15 people bookmarked your posts to act on later. Saves are the strongest signal of a future buyer.</p>',
    mc("Saves", "watch", "Watch", "18", "57 &ndash; 284", 6,
       "Below the prorated floor, the same gap flagged every month this year. Save-worthy value content is the standing recommendation.",
       "Saves landed at 18. Translation: 18 people bookmarked your posts to act on later. Saves are the strongest signal of a future buyer."),
    "mc:saves")

# Comments 54 (W) -> 66 (OT)
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Comments</span><span class="mc-badge watch">Watch</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val watch">54</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">75 &ndash; 250</span></div></div>\n'
    '          <div class="mc-mom"><span class="mom dn">&#9660; 72% vs June</span></div>\n'
    '          <div class="bar-track"><div class="bar-fill watch" data-w="22" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Under the monthly floor on a third of the usual output, but the founder story alone drew 24 of the 54.</p>\n'
    '          <p class="mc-callout">Comments landed at 54. Translation: 54 people stopped to start a conversation with you. Comments are public proof that your audience is engaged, and they pull in the people watching from the sidelines.</p>',
    mc("Comments", "ontrack", "On Track", "66", "53 &ndash; 177", 37,
       "Inside the prorated range. The founder story alone drew 24 of the 66.",
       "Comments came in at 66. Translation: 66 people stopped to start a conversation with you. Comments are public proof that your audience is engaged, and they pull in the people watching from the sidelines."),
    "mc:comments")

# CTR 9.7%->8.8% (E)
html = sub(html,
    '<div class="mc-top"><span class="mc-name">CTR</span><span class="mc-badge exceed">Exceeding</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val exceed">9.7%</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">3% &ndash; 6%</span></div></div>\n'
    '          <div class="mc-mom"><span class="mom fl">0.1 pts vs June, essentially flat</span></div>\n'
    '          <div class="bar-track"><div class="bar-fill exceed" data-w="100" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Above the Lift ceiling and steady to the final day. The strongest and most consistent metric of the engagement.</p>\n'
    '          <p class="mc-callout">Click-through rate came in at 9.7%. Translation: of everyone who saw your link, 9.7% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers.</p>',
    mc("CTR", "exceed", "Exceeding", "8.8%", "3% &ndash; 6%", 100,
       "Above the Lift ceiling and steady to the final day. The strongest and most consistent metric of the engagement.",
       "Click-through rate came in at 8.8%. Translation: of everyone who saw your link, 8.8% acted on it. A high click-through rate means the people finding you are not just watching, they are moving toward becoming customers."),
    "mc:ctr")

# Bio Link Taps 57->49 (OT)
html = sub(html,
    '<div class="mc-top"><span class="mc-name">Bio Link Taps</span><span class="mc-badge ontrack">On Track</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val ontrack">57</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">30 &ndash; 180</span></div></div>\n'
    '          <div class="mc-mom"><span class="mom dn">&#9660; 21% vs June</span></div>\n'
    '          <div class="bar-track"><div class="bar-fill ontrack" data-w="32" style="width:0%"></div></div>\n'
    '          <p class="mc-note">Inside range on a partial window. Steady traffic to the shop and list right to the close.</p>\n'
    '          <p class="mc-callout">Link taps landed at 57. Translation: 57 people tapped the link in your bio to move toward your site, booking, or offer. A link tap is one of the clearest actions someone takes when they are ready to do business.</p>',
    mc("Bio Link Taps", "ontrack", "On Track", "49", "21 &ndash; 128", 38,
       "Inside the prorated range. Steady traffic to the shop and list right to the close.",
       "Link taps landed at 49. Translation: 49 people tapped the link in your bio to move toward your site, booking, or offer. A link tap is one of the clearest actions someone takes when they are ready to do business."),
    "mc:link-taps")

# PCR: n/a card -> real card
html = sub(html,
    '<div class="mc na">\n          <div class="mc-top"><span class="mc-name">PCR</span><span class="mc-badge na">Not available</span></div>\n'
    '          <div class="mc-nums"><div><span class="mc-lbl">July 1&ndash;22</span><span class="mc-val na">n/a</span></div><div><span class="mc-lbl">Target Range</span><span class="mc-tgt">10% &ndash; 16%</span></div></div>\n'
    '          <p class="mc-note">Profile conversion rate is derived from gross new followers, which Instagram no longer reports for this window, so it cannot be computed. It is excluded from the score rather than counted as a zero.</p>\n'
    '          <p class="mc-callout">Followers held essentially flat, 10,134 to 10,118, while 585 people still visited the profile. The audience you built stayed with you through the final weeks.</p>\n        </div>',
    '<div class="mc">\n          ' + mc("PCR", "watch", "Watch", "8.1%", "10% &ndash; 16%", 51,
        "Below the Lift floor, a standing lever through the engagement.",
        "Profile conversion came in at 8.1%. Translation: 8.1% of the people who visited your profile chose to follow. A strong profile conversion rate means your page is doing its job, turning curious visitors into an audience you can nurture toward buying.") + '\n        </div>',
    "mc:pcr")

# ── 7. C2B funnel ────────────────────────────────────────────────────────────
html = sub(html, '<span class="c2b-step-num">10,491</span><div class="c2b-step-main"><span class="c2b-step-txt">people saw your content</span><span class="c2b-step-badge">\U0001F3BC Music Hall filled 3x over</span>',
           '<span class="c2b-step-num">30,641</span><div class="c2b-step-main"><span class="c2b-step-txt">people saw your content</span><span class="c2b-step-badge">\U0001F3BC Music Hall filled nearly 9 times over</span>', "c2b:views")
html = sub(html, '<span class="c2b-step-num">585</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped through to look closer</span>', '<span class="c2b-step-num">557</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped through to look closer</span>', "c2b:pv")
html = sub(html, '<span class="c2b-step-num">15</span><div class="c2b-step-main"><span class="c2b-step-txt">bookmarked content to reference later</span><span class="c2b-step-badge">\U0001F4CC 15 pre-purchase bookmarks</span>', '<span class="c2b-step-num">18</span><div class="c2b-step-main"><span class="c2b-step-txt">bookmarked content to reference later</span><span class="c2b-step-badge">\U0001F4CC 18 pre-purchase bookmarks</span>', "c2b:saves")
html = sub(html, '<span class="c2b-step-num">57</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped a bio link, the highest-intent signal we track</span><span class="c2b-step-badge">\U0001F446 57 deliberate taps toward your shop</span>', '<span class="c2b-step-num">49</span><div class="c2b-step-main"><span class="c2b-step-txt">tapped a bio link, the highest-intent signal we track</span><span class="c2b-step-badge">\U0001F446 49 deliberate taps toward your shop</span>', "c2b:taps")

# ── 8. full engagement (Q3 + strip) ──────────────────────────────────────────
html = sub(html, '<div class="qy-q">Q3</div><div class="qy-range">Jul 1&ndash;22</div><div class="qy-avg">7.6<span class="u">/10</span></div>', '<div class="qy-q">Q3</div><div class="qy-range">Jul 1&ndash;22</div><div class="qy-avg">7.8<span class="u">/10</span></div>', "qy:q3-avg")
html = sub(html,
    'click-through finished at 9.7%, above benchmark for the last time as it was for most of the year, and the founder story drove 24 of 54 comments.',
    'click-through finished at 8.8%, above benchmark for the last time as it was for most of the year, and the founder story drove 24 of 66 comments.', "qy:q3-worked")
html = sub(html, 'retention at 37.8% and saves at 15, the two gaps that stayed open all year.', 'retention at 46% and saves at 18, the two gaps that stayed open all year.', "qy:q3-watched")
html = sub(html, '<div class="mscore-cell current"><div class="mscore-m">Jul</div><div class="mscore-v">7.6</div></div>', '<div class="mscore-cell current"><div class="mscore-m">Jul</div><div class="mscore-v">7.8</div></div>', "mscore:jul")
# ARC list source (Q3 Jul 7.6 -> 7.8 already covered by mscore cell; the ph title still 7.6? no, hero fixed)

# ── 9. beat 4 feature card magnitudes ────────────────────────────────────────
html = sub(html,
    'A conversation outlier at 2.7x the window&rsquo;s comment average, and the single most engaging piece of the final window at a 13.3% engagement rate against an account average of 6.4%. Erin on camera, telling the story of how a collection actually gets made, is the content that pulled this community into a reply every time we ran it. This is the engine worth carrying forward.',
    'A conversation outlier at 2.6x the window&rsquo;s comment average, and the single most-commented piece of the final window. Erin on camera, telling the story of how a collection actually gets made, is the content that pulled this community into a reply every time we ran it. This is the engine worth carrying forward.', "beat4:founder")
html = sub(html, 'on top of the widest reach of the final window at 2,503 views', 'on top of the widest reach of the final window at 2,945 views', "beat4:tease-reach")

# ── 10. beat 5 carry-forward copy ────────────────────────────────────────────
html = sub(html, 'through running well above the 3 to 6% benchmark, most recently 9.7%.', 'through running well above the 3 to 6% benchmark, most recently 8.8%.', "beat5:ctr")
html = sub(html, 'Retention, which closed this final window at 37.8% against a 50 to 65% target, is what decides how far each post travels', 'Retention, which closed this final window at 46% against a 50 to 65% target, is what decides how far each post travels', "beat5:retention")

# ── write ────────────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(html)
print(f"MEAS corrected: score {R['final']} (raw {R['raw']:.3f}); {len(edits)} edits")
for e in edits: print("  -", e)

#!/usr/bin/env python3
"""finalize_standard_july.py -- fill post-dependent Beat 2 + Beat 4 for the four
standard July reports from the injected ALL_POSTS. Anchored/hard-fail. Feature
top-2 cards (Outlier-Magnitude chip dropped per MEAS precedent; standout chips
carry the checkable numbers). Launch Party keeps its #3 dropdown (genuine share
outlier); the others stay 2-card per their June structure.

Run: python3 finalize_standard_july.py <client>   (or with no arg = all four)
"""
import os, re, sys, json

REPO = "/Users/chase.gianattasio/Desktop/scroll-reports"
MON = {"07": "July"}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def split_cap(caption, n=200):
    body = caption.strip()
    if len(body) <= n:
        return body, ""
    cut = body.rfind(" ", 0, n)
    cut = cut if cut > n - 40 else n
    return body[:cut], body[cut:]


def mclass(x):
    return "outlier-3x" if x >= 3 else ("outlier-2x" if x >= 2 else "outlier-1x")


def date_full(d):
    return f"{MON[d[5:7]]} {int(d[8:10])}, 2026"


BADGE = {"reel": ("reel-badge", "REEL", "Reel"),
         "carousel": ("carousel-badge", "CAROUSEL", "Carousel"),
         "static": ("static-badge", "STATIC IMAGE", "Static")}


def card(post, rank, hook, cid, standouts, why):
    bcls, blab, pill = BADGE[post["format"]]
    prev, rest = split_cap(post["caption"])
    sm = "".join(
        f'<div class="standout-metric"><span class="sm-label">{l}</span>'
        f'<span class="sm-value">{v}</span>'
        f'<span class="sm-badge {mclass(x)}">{x}x account avg</span></div>'
        for l, v, x in standouts)
    return (
        f'<div class="post-card"><div class="post-header"><span class="post-rank">{rank}</span>'
        f'<span class="post-type-badge {bcls}">{blab}</span></div>'
        f'<div class="post-body"><div class="post-date">{date_full(post["date"])}</div>'
        f'<div class="post-format-pill">{pill}</div>'
        f'<blockquote class="post-hook">&ldquo;{esc(hook)}&rdquo;</blockquote>'
        f'<div class="post-caption"><span class="cap-preview">{esc(prev)}</span>'
        f'<span class="cap-ellipsis" id="{cid}-ellipsis">&hellip;</span>'
        f'<span class="cap-rest" id="{cid}-rest" style="display:none">{esc(rest)}</span>'
        f'<button class="cap-toggle" id="{cid}-btn" onclick="toggleCap(\'{cid}\')">Show more</button></div>'
        f'<div class="standout-metrics">{sm}</div>'
        f'<div class="post-why"><div class="why-label">&#9650; WHY IT WORKED</div>'
        f'<p class="why-text">{why}</p></div>'
        f'<a href="{post["url"]}" target="_blank" rel="noopener" class="post-ig-btn">'
        f'View on Instagram &rarr;</a></div></div>')


# ── per-client config ────────────────────────────────────────────────────────
CFG = {
 "shoplaunchparty": {
   "beat2_old": 'We published 14 posts, leaning into relatable everyday-beauty content, industry-take carousels, and tutorials, all pointing shoppers toward the summer drop and the OTR store.',
   "beat2_new": 'We published 15 pieces in July, leaning into quick hair and beauty tutorials, the Final Friday zine event, and relatable everyday-beauty content, all pointing shoppers toward the shop and the OTR store.',
   "work_old": '<div class="work-strip"><span class="work-chip"><b>14 posts</b></span><span class="work-chip">Mostly Reels, three carousels</span><span class="work-chip">Themes: relatable everyday beauty, industry takes, tutorials</span><span class="work-chip">Focus: shop and in-store</span></div>',
   "work_new": '<div class="work-strip"><span class="work-chip"><b>15 posts</b></span><span class="work-chip">11 Reels, four carousels</span><span class="work-chip">Themes: hair and beauty tutorials, the zine event, everyday beauty</span><span class="work-chip">Focus: shop and in-store</span></div>',
   "beat4_old": 'Your audience rewards relatable, real-life content.',
   "beat4_new": 'Quick hair tutorials are what your audience saves, and the zine event is what they share.',
   "cards": [
     dict(uid="DaftrD7uiKN", rank="#1 Top Post", hook="Love a messy bun but want to elevate it?", cid="tpreel1",
          standouts=[("SAVES", "17", 3.3)],
          why="Save density at 3.3 times your average. Quick, do-it-yourself hair tutorials are the format your audience bookmarks to try later, and a save is the strongest early signal of a future shopper. Keep the how-to Reels coming."),
     dict(uid="DbDxOxUuDm-", rank="#2 Top Post", hook="Struggle with claw clips because of long or thick hair?", cid="tpreel2",
          standouts=[("SAVES", "16", 3.1)],
          why="Another save outlier, 3.1 times your average, on the same tutorial format. Two of your top posts this month were quick hair how-tos, which confirms the pattern: teach something useful in a few seconds and your audience keeps it."),
   ],
   "drop_uid": "DbTWzkhDuCw", "drop_rank": "#3 Top Post", "drop_hook": "Volume 4 of our zine is officially dropping!", "drop_cid": "tpcarousel3",
   "drop_standouts": [("SHARES", "23", 7.9)],
   "drop_why": "A share outlier at nearly 8 times your average. The Final Friday zine event pulled the community in and they passed it on. Event and community content is your reach engine, worth pairing with the tutorials that convert.",
 },
 "laneandkate": {
   "beat2_old": 'We published 8 posts, leaning into custom-ring storytelling, jewelry-care education, and in-shop moments, all pointing toward design consultations.',
   "beat2_new": 'We published 9 posts, leaning into custom-design storytelling, client and wedding moments, and in-shop content, all pointing toward design consultations.',
   "work_old": '<div class="work-strip"><span class="work-chip"><b>8 posts</b></span><span class="work-chip">Mostly carousels, some Reels</span><span class="work-chip">Themes: custom-ring storytelling, jewelry-care education, in-shop moments</span><span class="work-chip">Focus: consultation bookings</span></div>',
   "work_new": '<div class="work-strip"><span class="work-chip"><b>9 posts</b></span><span class="work-chip">7 Reels, two photos</span><span class="work-chip">Themes: custom-design storytelling, client moments, in-shop content</span><span class="work-chip">Focus: consultation bookings</span></div>',
   "beat4_old": 'Your audience saves the aspirational custom work.',
   "beat4_new": 'Your audience saves and shares your custom-design storytelling.',
   "cards": [
     dict(uid="DaVuRkiRArq", rank="#1 Top Post", hook="There is nothing quite like seeing a design come to life.", cid="tpreel1",
          standouts=[("SHARES", "14", 3.8), ("SAVES", "7", 3.7)],
          why="A share and save outlier, both around 3.7 times your average. Custom-design storytelling, a one-of-a-kind mosaic ring carrying a client's heritage, is exactly what your audience saves and passes on. This is the highest-intent content you make."),
     dict(uid="DbMC7y9v2MG", rank="#2 Top Post", hook="Our girl Kail is getting married in Jackson Hole next weekend.", cid="tpstatic2",
          standouts=[("TOTAL VIEWS", "3,433", 1.7)],
          why="A reach outlier at 1.7 times your average views. A candid, real-client wedding moment traveled past the core audience. Client and celebration moments keep your custom work in front of the people planning their own."),
   ],
 },
 "defineoakley": {
   "beat2_old": 'We published 8 Reels, leaning into the fun of class culture, instructor spotlights, and welcoming first-timers, all pointing toward class bookings.',
   "beat2_new": 'We published 10 posts, leaning into class-culture and hype content, member and referral moments, and a Christmas-in-July giveaway, all pointing toward class bookings.',
   "work_old": '<div class="work-strip"><span class="work-chip"><b>8 posts</b></span><span class="work-chip">All Reels</span><span class="work-chip">Themes: class culture and fun, instructor spotlights, welcoming first-timers</span><span class="work-chip">Focus: class bookings</span></div>',
   "work_new": '<div class="work-strip"><span class="work-chip"><b>10 posts</b></span><span class="work-chip">8 Reels, two carousels</span><span class="work-chip">Themes: class culture and hype, referral moments, a giveaway</span><span class="work-chip">Focus: class bookings</span></div>',
   "beat4_old": 'Your audience keeps and shares the content that shows the fun of your classes.',
   "beat4_new": 'Your members keep the class-culture content and share the bring-a-friend moments.',
   "cards": [
     dict(uid="DafslbFNZ6S", rank="#1 Top Post", hook="Don't be mad at us when we cue the hard moves pleassseee!!!", cid="tpreel1",
          standouts=[("SAVES", "26", 4.1), ("SHARES", "136", 3.2)],
          why="A save outlier at 4.1 times your average, with shares also over-indexing at 3.2 times. Class-culture content that hypes the workout is what your members keep and pass to a friend, the strongest early signal of a booking. This is the engine to keep running."),
     dict(uid="DaxoXE9N2MU", rank="#2 Top Post", hook="Go besties go!", cid="tpreel2",
          standouts=[("SHARES", "219", 5.1), ("TOTAL VIEWS", "8,606", 2.2)],
          why="A share outlier at 5.1 times your average, on the widest reach of the month at 8,600 views. The guest-pass and bring-a-friend message spread exactly the way you want, putting the studio in front of new people through your members. Community and referral content travels."),
   ],
 },
 "upandrunningoh": {
   "beat2_old": 'We published 9 posts, leaning into summer events and running groups, the juniors program, and product collections, all pointing toward fittings and shop visits.',
   "beat2_new": 'We published 14 posts, leaning into the Juniors program, community events and traditions, and product collections, all pointing toward fittings and shop visits.',
   "work_old": '<div class="work-strip"><span class="work-chip"><b>9 posts</b></span><span class="work-chip">Mostly carousels</span><span class="work-chip">Themes: summer events and groups, juniors program, product collections</span><span class="work-chip">Focus: fittings and shop</span></div>',
   "work_new": '<div class="work-strip"><span class="work-chip"><b>14 posts</b></span><span class="work-chip">6 Reels, six carousels, two photos</span><span class="work-chip">Themes: Juniors program, community events, product collections</span><span class="work-chip">Focus: fittings and shop</span></div>',
   "beat4_old": 'Short-form Reels with a strong open are what hold your audience, and community-event content is what pulls them into conversation.',
   "beat4_new": 'Your community-program and event content is what reaches new people.',
   "cards": [
     dict(uid="DbGo7xUltm9", rank="#1 Top Post", hook="Nearly 200 athletes, countless miles, and one incredible summer.", cid="tpcarousel1",
          standouts=[("TOTAL VIEWS", "1,705", 2.2)],
          why="A reach outlier at 2.2 times your average views. The Juniors summer-camp recap broke past the core audience, exactly the discovery motion a Spark-stage account needs. Community-program content is your widest-reaching format."),
     dict(uid="DaVezWqEbYr", rank="#2 Top Post", hook="Some traditions are simply too special to fade.", cid="tpcarousel2",
          standouts=[("TOTAL VIEWS", "1,189", 1.6)],
          why="A reach outlier at 1.6 times your average. The long-running triathlon tradition carried real community weight and traveled. Local-history and event content keeps widening the top of your funnel."),
   ],
 },
}


def sub(html, old, new, label, path):
    if html.count(old) != 1:
        sys.exit(f"ANCHOR FAIL [{path}:{label}]: found {html.count(old)}\n  {old[:150]}")
    return html.replace(old, new, 1)


def finalize(client):
    path = f"{REPO}/{client}/july2026/index.html"
    html = open(path, encoding="utf-8").read()
    posts = json.loads(re.search(r'var ALL_POSTS = (\[.*?\]);', html, re.S).group(1))
    by = {p["url"].rstrip("/").rsplit("/", 1)[-1]: p for p in posts}
    c = CFG[client]

    html = sub(html, c["beat2_old"], c["beat2_new"], "beat2", client)
    html = sub(html, c["work_old"], c["work_new"], "workstrip", client)
    html = sub(html,
               f'<h2 class="beat-takeaway" id="beat4-t">{c["beat4_old"]}</h2>',
               f'<h2 class="beat-takeaway" id="beat4-t">{c["beat4_new"]}</h2>', "beat4-takeaway", client)

    cards = "".join(card(by[cc["uid"]], cc["rank"], cc["hook"], cc["cid"], cc["standouts"], cc["why"]) for cc in c["cards"])
    # ALWAYS emit the featured block wrapped in TP_START/TP_END. Those markers are the
    # sole injection target for inject_report_data.py (the bare posts-grid fallback was
    # removed, KI-002) — re-emitting them here is what keeps every finalized shell able to
    # pass next month's Metricool pull. Anchor on the markers if the shell already carries
    # them, else fall back to the legacy bare feature-2up (and add the markers).
    new_block = f'<!--TP_START--><div class="feature-2up">{cards}</div><!--TP_END-->'
    m = re.search(r'<!--TP_START-->.*?<!--TP_END-->', html, re.S)
    if not m:
        m = re.search(r'<div class="feature-2up">.*?</div></div></div>(?=\n  <p class="beat-pattern">)', html, re.S)
    if not m:
        sys.exit(f"ANCHOR FAIL [{client}:feature-2up]")
    html = html.replace(m.group(0), new_block, 1)

    if "drop_uid" in c:
        dcard = card(by[c["drop_uid"]], c["drop_rank"], c["drop_hook"], c["drop_cid"], c["drop_standouts"], c["drop_why"])
        m2 = re.search(r'<details class="proof"><summary><span class="proof-ic">&#9733;</span><span>See the other standout posts this month</span>.*?</details>', html, re.S)
        if not m2:
            sys.exit(f"ANCHOR FAIL [{client}:dropdown]")
        new_dd = ('<details class="proof"><summary><span class="proof-ic">&#9733;</span>'
                  '<span>See the other standout posts this month</span><span class="proof-chev">&#8250;</span></summary>'
                  '<div class="proof-body"><div class="posts-grid">' + dcard + '</div></div></details>')
        html = html.replace(m2.group(0), new_dd, 1)

    open(path, "w", encoding="utf-8").write(html)
    print(f"finalized {client} ({len(posts)} posts, {len(c['cards'])} featured{', +dropdown' if 'drop_uid' in c else ''})")


if __name__ == "__main__":
    which = sys.argv[1:] or list(CFG)
    for cl in which:
        finalize(cl)

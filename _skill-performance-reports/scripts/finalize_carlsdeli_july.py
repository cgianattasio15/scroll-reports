#!/usr/bin/env python3
"""
finalize_carlsdeli_july.py -- second pass: fill the post-dependent content the
scaffold left as June's, using the July ALL_POSTS the Metricool pull injected.

Fills Beat 2 (count + format mix + prose + "see all N") and Beat 4 (takeaway +
prose + the two feature cards). Anchored, hard-fail. The "Outlier Magnitude"
chip is intentionally dropped (build_meas_july_closeout.py precedent /
Procedural Gate #10); the standout-metric chips carry the real, checkable
numbers. Dropdown stays hidden: only one post (the flood carousel) clears the
ALL_POSTS outlier gate and it is featured.
"""
import os, re, sys, json

REPO = "/Users/chase.gianattasio/Desktop/scroll-reports"
F = f"{REPO}/carlsdeli/july2026/index.html"
edits = []


def sub(html, old, new, label):
    n = html.count(old)
    if n != 1:
        sys.exit(f"ANCHOR FAIL [{label}]: found {n}, expected 1\n  {old[:160]}")
    edits.append(label)
    return html.replace(old, new)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def split_cap(caption, n=200):
    body = caption.strip()
    if len(body) <= n:
        return body, ""
    cut = body.rfind(" ", 0, n)
    cut = cut if cut > n - 40 else n
    return body[:cut], body[cut:]


html = open(F, encoding="utf-8").read()
posts = json.loads(re.search(r'var ALL_POSTS = (\[.*?\]);', html, re.S).group(1))
by = {p["url"].rstrip("/").rsplit("/", 1)[-1]: p for p in posts}
FLOOD = by["Da8O4C7keOv"]     # #1 — flash-flood community carousel
CATER = by["DbYjsiHRTtz"]     # #2 — catering reel, 91.7% retention

# account averages (all 15 posts) for checkable standout multipliers
def avg(k):
    v = [p[k] for p in posts if p.get(k) is not None]
    return sum(v) / len(v)
A = {k: avg(k) for k in ("views", "saves", "shares", "comments", "retention")}


def card(post, rank, badge_cls, badge_lbl, pill, hook, cid, standouts, why):
    prev, rest = split_cap(post["caption"])
    sm = "".join(
        f'<div class="standout-metric"><span class="sm-label">{l}</span>'
        f'<span class="sm-value">{v}</span>'
        f'<span class="sm-badge {c}">{m}x account avg</span></div>'
        for l, v, m, c in standouts)
    date_full = {"07": "July"}["07"] + " " + str(int(post["date"][-2:])) + ", 2026"
    return (
        f'<div class="post-card"><div class="post-header">'
        f'<span class="post-rank">{rank}</span>'
        f'<span class="post-type-badge {badge_cls}">{badge_lbl}</span></div>'
        f'<div class="post-body"><div class="post-date">{date_full}</div>'
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


sh_x = round(FLOOD["shares"] / A["shares"], 1)     # 12.2
sv_x = round(FLOOD["saves"] / A["saves"], 1)       # 8.5
rt_x = round(CATER["retention"] / A["retention"], 1)  # 2.5

card1 = card(FLOOD, "#1 Top Post", "carousel-badge", "CAROUSEL", "Carousel",
             "Hyde Park woke up to a mess this morning.", "tpcar1",
             [("SHARES", "723", sh_x, "outlier-3x"), ("SAVES", "50", sv_x, "outlier-3x")],
             "A community moment, not a promotion. When Hyde Park flooded, Sydney and Cameron showed up for their "
             "neighbors, and Cincinnati shared it 12 times harder than anything else you posted, on top of 80,000 views "
             "and saves at 8 times your average. This is the neighborhood trust the deli has built for 80 years showing "
             "up as reach no ad could buy. Real, local, human moments are the format to keep ready.")
card2 = card(CATER, "#2 Top Post", "reel-badge", "REEL", "Reel",
             "Guess we’ll figure it out...somehow", "tpreel2",
             [("AVG RETENTION", "91.7%", rt_x, "outlier-2x")],
             "People watched this one almost to the end, at 2.5 times your average retention. A light, funny open earned "
             "the attention, then the reel made the catering pitch while viewers were still there. That is the pattern to "
             "copy: hook first, then the ask, so the catering message lands on an audience that stayed.")

old_feature = re.search(r'<div class="feature-2up">.*?</div></div></div>\n  <p class="beat-pattern">', html, re.S)
if not old_feature:
    sys.exit("ANCHOR FAIL [beat4:feature-2up]")
html = html.replace(old_feature.group(0),
                    f'<div class="feature-2up">{card1}{card2}</div>\n  <p class="beat-pattern">', 1)
edits.append("beat4:feature-2up")

# ── Beat 2 (post-dependent) ──────────────────────────────────────────────────
html = sub(html,
    'We published 13 posts in your first month, introducing the brand and pointing new fans toward catering.',
    'We published 15 pieces in July, 13 Reels and two carousels, all built around the neighborhood and pointing toward catering.',
    "beat2:takeaway")
html = sub(html,
    '<span class="work-chip"><b>13 posts</b></span>\n'
    '    <span class="work-chip">Mostly Reels, two carousels</span>\n'
    '    <span class="work-chip">Themes: a proper welcome, signature-sandwich spotlights, the 80-year family story</span>\n'
    '    <span class="work-chip">Focus: catering inquiries</span>',
    '<span class="work-chip"><b>15 posts</b></span>\n'
    '    <span class="work-chip">13 Reels, two carousels</span>\n'
    '    <span class="work-chip">Themes: neighborhood moments, the 80-year story, catering and menu</span>\n'
    '    <span class="work-chip">Focus: catering inquiries</span>',
    "beat2:workstrip")
html = sub(html,
    'We opened with a welcome Reel, spotlighted signature sandwiches like the College Club and Loud and Layered, and told the Hyde Park family story, all pointing toward catering.',
    'We showed up for the neighborhood after the Hyde Park flooding, told the 80-year story of the deli, and kept the catering message running across the month, all built to travel.',
    "beat2:prose")
html = sub(html, '<span>See all 13 posts and their numbers</span>',
           '<span>See all 15 posts and their numbers</span>', "beat2:allposts-summary")

# ── Beat 4 takeaway + prose (post-dependent) ─────────────────────────────────
html = sub(html,
    'Your audience saves and shares the stories, the welcome, the family history, the neighborhood moments.',
    'When Hyde Park flooded, you showed up for the neighborhood, and Cincinnati shared it 12 times harder than anything else you posted.',
    "beat4:takeaway")
html = sub(html,
    'Your top post this month was the &ldquo;Welcome in!&rdquo; Reel. It was saved 10 times more than an average post and shared 8 times more.',
    'Your top post was the flash-flood community carousel. It was shared 12 times more than an average post and saved 8 times more.',
    "beat4:prose")

open(F, "w", encoding="utf-8").write(html)
print(f"standouts: shares {sh_x}x, saves {sv_x}x, retention {rt_x}x")
print(f"finalized {F}  ({len(edits)} edits)")
for e in edits:
    print("  -", e)

"""
Scroll Media — v8 Report Builder / Worked-Example Generator
Version 1.0 — June 2026

Fills canonical-template-v8.html with a token map and writes a finished report.
Also generates the HTML helper blobs that are tokens in the template:
  - SCORE_TREND_BARS_HTML  (3-4 month score trend bars)
  - QSNAP_SPARKLINE_SVG    (trailing 3-month score sparkline)
  - GOALn_SPARKLINE_SVG    (per-goal 3-month metric sparkline)
  - TOP_POSTS_HTML         (Top 3 post cards)
  - PREV_REPORTS_HTML      (previous-report cards)
  - ALL_POSTS_JSON         (from all_posts_data.py)

Running it with no arguments writes a WORKED EXAMPLE using a hypothetical
Lift-stage client ("Bright Hill Studio") and representative data, so the v8
template can be rendered and mobile-audited end to end. Real reports are built by
swapping the token map for the client/month's verified data.
"""

import os
import json
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "templates", "canonical-template-v8.html")


# ── HTML helper blob builders ────────────────────────────────────────────────
def trend_bars(scores):
    """scores: list of (label, value, is_current). Heights scaled 6.0-10 -> 12-100%."""
    out = []
    for label, val, curr in scores:
        h = max(12, min(100, (val - 6.0) / 4.0 * 100))
        color = "#e2ed7a" if curr else "rgba(255,255,255,0.28)"
        ts = "ts curr" if curr else "ts"
        tm = "tm curr" if curr else "tm"
        out.append(
            f'<div class="tc"><div class="tbw"><div class="tb" style="height:{h:.0f}%;background:{color}"></div></div>'
            f'<div class="{ts}">{val}</div><div class="{tm}">{label}</div></div>'
        )
    return "".join(out)


def sparkline(values, w=84, h=30, color="#0e3387"):
    """Tiny inline SVG polyline sparkline from a list of numbers."""
    if not values:
        return ""
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1
    n = len(values)
    pts = []
    for i, v in enumerate(values):
        x = (i / (n - 1)) * (w - 4) + 2 if n > 1 else w / 2
        y = h - 2 - ((v - lo) / span) * (h - 6)
        pts.append(f"{x:.1f},{y:.1f}")
    last_x, last_y = pts[-1].split(",")
    return (
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" aria-hidden="true">'
        f'<polyline points="{" ".join(pts)}" stroke="{color}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="{last_x}" cy="{last_y}" r="2.6" fill="{color}"/></svg>'
    )


def top_post_card(rank, badge_class, badge_label, score, date, fmt, hook, caption_prev,
                  caption_rest, standout_html, why, url, uid):
    return (
        f'<div class="post-card"><div class="post-header"><span class="post-rank">#{rank} Top Post</span>'
        f'<span class="post-type-badge {badge_class}">{badge_label}</span>'
        f'<span class="post-score">Outlier Magnitude: {score/100:.2f}x</span></div>'
        f'<div class="post-body"><div class="post-date">{date}</div>'
        f'<div class="post-format-pill">{fmt}</div>'
        f'<blockquote class="post-hook">&ldquo;{hook}&rdquo;</blockquote>'
        f'<div class="post-caption"><span class="cap-preview">{caption_prev}</span>'
        f'<span class="cap-ellipsis" id="{uid}-ellipsis">&hellip;</span>'
        f'<span class="cap-rest" id="{uid}-rest" style="display:none">{caption_rest}</span>'
        f'<button class="cap-toggle" id="{uid}-btn" onclick="toggleCap(\'{uid}\')">Show more</button></div>'
        f'<div class="standout-metrics">{standout_html}</div>'
        f'<div class="post-why"><div class="why-label">&#9650; WHY IT WORKED</div><p class="why-text">{why}</p></div>'
        f'<a href="{url}" target="_blank" rel="noopener" class="post-ig-btn">View on Instagram &rarr;</a></div></div>'
    )


def standout(label, value, badge_class, badge_text):
    return (f'<div class="standout-metric"><span class="sm-label">{label}</span>'
            f'<span class="sm-value">{value}</span>'
            f'<span class="sm-badge {badge_class}">{badge_text}</span></div>')


def prev_card(href, month, score, label, color):
    return (f'<a href="{href}" class="prev-card" target="_blank" rel="noopener">'
            f'<div class="prev-month">{month}</div>'
            f'<div class="prev-score" style="color:{color}">{score}<span>/10</span></div>'
            f'<div class="prev-label">{label}</div>'
            f'<div class="prev-link">View Report &#8599;</div></a>')


# ── Worked-example token map (hypothetical Lift-stage client) ────────────────
def worked_example_tokens():
    all_posts = [
        {"date": "2026-06-27", "date_display": "Jun 27", "format": "reel", "caption": "The one styling mistake that flattens every outfit (and the 10-second fix we use on set).", "views": 8420, "saves": 96, "shares": 41, "comments": 33, "retention": 58, "linktaps": 22, "ctr": 9.1, "url": "https://www.instagram.com/p/EXAMPLE1/", "outlier": True},
        {"date": "2026-06-24", "date_display": "Jun 24", "format": "carousel", "caption": "Five pieces, fifteen looks. Save this before your next trip.", "views": 5130, "saves": 71, "shares": 18, "comments": 22, "retention": None, "linktaps": 14, "ctr": 7.4, "url": "https://www.instagram.com/p/EXAMPLE2/", "outlier": True},
        {"date": "2026-06-21", "date_display": "Jun 21", "format": "reel", "caption": "Behind the scenes of the summer shoot. Sound on for the bloopers.", "views": 6240, "saves": 28, "shares": 12, "comments": 41, "retention": 49, "linktaps": 9, "ctr": 4.2, "url": "https://www.instagram.com/p/EXAMPLE3/", "outlier": False},
        {"date": "2026-06-18", "date_display": "Jun 18", "format": "static", "caption": "New arrivals just dropped. Which one are you reaching for first?", "views": 3010, "saves": 19, "shares": 6, "comments": 27, "retention": None, "linktaps": 31, "ctr": 11.8, "url": "https://www.instagram.com/p/EXAMPLE4/", "outlier": True},
        {"date": "2026-06-15", "date_display": "Jun 15", "format": "reel", "caption": "How to build a capsule wardrobe that actually works for your life.", "views": 4720, "saves": 44, "shares": 15, "comments": 19, "retention": 52, "linktaps": 12, "ctr": 5.0, "url": "https://www.instagram.com/p/EXAMPLE5/", "outlier": False},
        {"date": "2026-06-12", "date_display": "Jun 12", "format": "carousel", "caption": "The color palette guide everyone keeps asking for.", "views": 3890, "saves": 53, "shares": 11, "comments": 14, "retention": None, "linktaps": 8, "ctr": 3.9, "url": "https://www.instagram.com/p/EXAMPLE6/", "outlier": False},
        {"date": "2026-06-09", "date_display": "Jun 9", "format": "static", "caption": "A little Monday motivation from the studio.", "views": 2140, "saves": 7, "shares": 3, "comments": 9, "retention": None, "linktaps": None, "ctr": None, "url": "https://www.instagram.com/p/EXAMPLE7/", "outlier": False},
        {"date": "2026-06-06", "date_display": "Jun 6", "format": "reel", "caption": "Three ways to wear the linen set we cannot stop recommending.", "views": 5560, "saves": 38, "shares": 22, "comments": 16, "retention": 55, "linktaps": 18, "ctr": 6.3, "url": "https://www.instagram.com/p/EXAMPLE8/", "outlier": False},
        {"date": "2026-06-03", "date_display": "Jun 3", "format": "story", "caption": "Poll: which print wins for summer?", "views": 1980, "saves": 2, "shares": 1, "comments": 0, "retention": None, "linktaps": 26, "ctr": 13.1, "url": "https://www.instagram.com/p/EXAMPLE9/", "outlier": True},
        {"date": "2026-06-01", "date_display": "Jun 1", "format": "carousel", "caption": "June lookbook is live. Tap to see the full edit.", "views": 4310, "saves": 33, "shares": 9, "comments": 12, "retention": None, "linktaps": 21, "ctr": 8.0, "url": "https://www.instagram.com/p/EXAMPLE10/", "outlier": False},
    ]

    score_trend = trend_bars([("Mar", 7.6, False), ("Apr", 8.0, False), ("May", 8.1, False), ("Jun", 8.3, True)])

    tp1 = top_post_card(
        1, "reel-badge", "REEL", 214, "June 27, 2026", "Reel",
        "The one styling mistake that flattens every outfit",
        "The one styling mistake that flattens every outfit (and the 10-second fix we use on set).",
        " Most people skip this step and wonder why nothing sits right. Here is the fix.",
        standout("SAVES", "96", "outlier-3x", "3.1x account avg") + standout("SHARES", "41", "outlier-2x", "2.4x account avg"),
        "Powered by save density at 3.1x the account average. Saves this high signal that viewers found the content worth returning to, a strong signal of buyer intent. Shares also over-indexed at 2.4x average, compounding the reach effect.",
        "https://www.instagram.com/p/EXAMPLE1/", "tpex1")
    tp2 = top_post_card(
        2, "carousel-badge", "CAROUSEL", 168, "June 24, 2026", "Carousel",
        "Five pieces, fifteen looks",
        "Five pieces, fifteen looks. Save this before your next trip.",
        " Packing light without wearing the same thing twice is a skill. Here is the formula.",
        standout("SAVES", "71", "outlier-2x", "2.3x account avg"),
        "Powered by save density at 2.3x the account average. A practical, reference-style carousel that earns the bookmark, the strongest signal of a future buyer.",
        "https://www.instagram.com/p/EXAMPLE2/", "tpex2")
    tp3 = top_post_card(
        3, "static-badge", "STATIC IMAGE", 142, "June 18, 2026", "Static Image",
        "New arrivals just dropped",
        "New arrivals just dropped. Which one are you reaching for first?",
        " The summer drop is here and it is moving fast.",
        standout("LINK TAPS", "31", "outlier-2x", "2.0x account avg") + standout("COMMENTS", "27", "outlier-1x", "1.6x account avg"),
        "A conversion outlier. Link taps ran at 2.0x the account average, sending high-intent traffic straight to the shop while comments stayed strong at 1.6x.",
        "https://www.instagram.com/p/EXAMPLE4/", "tpex3")

    prevs = (prev_card("/brighthillstudio/may2026/", "May 2026", "8.1", "Solid Month", "#059669") +
             prev_card("/brighthillstudio/april2026/", "April 2026", "8.0", "Solid Month", "#059669") +
             prev_card("/brighthillstudio/march2026/", "March 2026", "7.6", "Progressing Month", "#d97706"))

    return {
        # identity
        "CLIENT_NAME": "Bright Hill Studio", "CLIENT_NAME_H1": "Bright Hill <span>Studio</span>",
        "CLIENT_HANDLE": "brighthillstudio", "CLIENT_SLUG": "brighthillstudio",
        "CLIENT_NICHE_DESCRIPTOR": "Modern Wardrobe Styling for Everyday Life",
        "CLIENT_AM_NAME": "Rachel", "CLIENT_STAGE": "Lift Stage", "CLIENT_MONTH_NUMBER": "9",
        # period
        "REPORT_MONTH_YEAR": "June 2026", "REPORT_MONTH": "June", "REPORT_DATE_RANGE": "June 1&ndash;30, 2026",
        "NEXT_MONTH": "July", "PREV_MONTH": "May", "PREV_MONTH_SHORT": "May", "MONTH_SLUG": "june2026",
        # score
        "SCORE": "8.3", "SCORE_LABEL": "Solid Month", "SCORE_DELTA_DIR": "up",
        "SCORE_DELTA_ARROW": "&#9650;", "SCORE_DELTA_TEXT": "+0.2",
        "SCORE_EXCEED_COUNT": "2", "SCORE_ONTRACK_COUNT": "6", "SCORE_WATCH_COUNT": "2",
        "SCORE_TREND_BARS_HTML": score_trend,
        # paired-hero business outcome
        "OUTCOME_LABEL": "Headline outcome this month", "OUTCOME_VALUE": "163",
        "OUTCOME_TITLE": "Link taps to the shop", "OUTCOME_SUB": "Up from 141 in May. The clearest signal of high-intent traffic moving from the feed toward a purchase.",
        "HERO_SUMMARY": "discovery widened, saves hit their best month of the quarter, and more of that attention turned into shop traffic.",
        # quarterly snapshot (June surfaced AS-IF non-QBR per the 2026 exception)
        "QSNAP_TRAJ_CLASS": "strong", "QSNAP_TRAJ_LABEL": "Strong",
        "QSNAP_SPARKLINE_SVG": sparkline([8.0, 8.1, 8.3], color="#0e3387"),
        "QSNAP_AVG": "8.1",
        "QSNAP_NARRATIVE": "June is the strongest of the last three months and the quarter is trending up. We&rsquo;re building on a steady base, not chasing one good month.",
        # followers banner
        "FOLLOWERS_COUNT": "9,140", "FOLLOWERS_MOM_DIR": "up", "FOLLOWERS_MOM_ARROW": "&#9650;",
        "FOLLOWERS_MOM_TEXT": "+1.8%", "FOLLOWERS_TARGET": "5,000 &ndash; 25,000",
        # metrics: New Followers
        "NF_STATUS": "ontrack", "NF_STATUS_LABEL": "On Track", "NF_VAL": "146", "NF_TARGET": "100 &ndash; 270",
        "NF_MOM_DIR": "up", "NF_MOM_ARROW": "&#9650;", "NF_MOM_TEXT": "+22% vs. May", "NF_BARW": "52",
        "NF_NOTE": "Comfortably inside the Lift range. Discovery content keeps pulling the right audience back.",
        "NF_DIR_WORD": "up", "NF_X": "22", "NF_MORE_FEWER": "more",
        # Shares
        "SH_STATUS": "ontrack", "SH_STATUS_LABEL": "On Track", "SH_VAL": "108", "SH_TARGET": "60 &ndash; 300",
        "SH_MOM_DIR": "up", "SH_MOM_ARROW": "&#9650;", "SH_MOM_TEXT": "+19% vs. May", "SH_BARW": "40",
        "SH_NOTE": "Back inside the Lift range. Styling and packing posts carried the share lift.",
        "SH_DIR_WORD": "up", "SH_X": "19", "SH_MORE_FEWER": "more",
        # Total Views
        "TV_STATUS": "ontrack", "TV_STATUS_LABEL": "On Track", "TV_VAL": "82,140", "TV_TARGET": "40,000 &ndash; 150,000",
        "TV_MOM_DIR": "up", "TV_MOM_ARROW": "&#9650;", "TV_MOM_TEXT": "+16% vs. May", "TV_BARW": "55",
        "TV_NOTE": "Up 16% month over month and inside the Lift range. Reach is expanding steadily.",
        "TV_DIR_WORD": "up", "TV_X": "16", "TV_MORE_FEWER": "more",
        # Profile Visits
        "PV_STATUS": "ontrack", "PV_STATUS_LABEL": "On Track", "PV_VAL": "1,210", "PV_TARGET": "300 &ndash; 2,000",
        "PV_MOM_DIR": "up", "PV_MOM_ARROW": "&#9650;", "PV_MOM_TEXT": "+14% vs. May", "PV_BARW": "57",
        "PV_NOTE": "Strong profile traffic inside the Lift range. Curious browsers are tapping through to look closer.",
        "PV_DIR_WORD": "up", "PV_X": "14", "PV_MORE_FEWER": "more",
        # Retention (+ watch time conditional)
        "RT_STATUS": "watch", "RT_STATUS_LABEL": "Watch", "RT_VAL": "53", "RT_TARGET": "50% &ndash; 65%",
        "RT_MOM_DIR": "up", "RT_MOM_ARROW": "&#9650;", "RT_MOM_TEXT": "+4pp vs. May", "RT_BARW": "53",
        "RT_NOTE": "Just inside the Lift floor. Reels with a tight hook held attention best this month.",
        "WATCHTIME_VAL": "8.4",
        # Saves
        "SV_STATUS": "exceed", "SV_STATUS_LABEL": "Exceeding", "SV_VAL": "421", "SV_TARGET": "80 &ndash; 400",
        "SV_MOM_DIR": "up", "SV_MOM_ARROW": "&#9650;", "SV_MOM_TEXT": "+34% vs. May", "SV_BARW": "100",
        "SV_NOTE": "Above the Lift ceiling and the best save month of the quarter. Reference-style content is landing.",
        "SV_DIR_WORD": "up", "SV_X": "34", "SV_MORE_FEWER": "more",
        # Comments
        "CM_STATUS": "ontrack", "CM_STATUS_LABEL": "On Track", "CM_VAL": "193", "CM_TARGET": "75 &ndash; 250",
        "CM_MOM_DIR": "up", "CM_MOM_ARROW": "&#9650;", "CM_MOM_TEXT": "+11% vs. May", "CM_BARW": "62",
        "CM_NOTE": "Inside the Lift range. Question-led captions kept the conversation going.",
        "CM_DIR_WORD": "up", "CM_X": "11", "CM_MORE_FEWER": "more",
        # CTR
        "CTR_STATUS": "exceed", "CTR_STATUS_LABEL": "Exceeding", "CTR_VAL": "9.6", "CTR_TARGET": "3% &ndash; 6%",
        "CTR_MOM_DIR": "up", "CTR_MOM_ARROW": "&#9650;", "CTR_MOM_TEXT": "+1.1pp vs. May", "CTR_BARW": "100",
        "CTR_NOTE": "Above the Lift ceiling. Visitors who reach the bio are tapping through at an excellent rate.",
        # Link Taps
        "LT_STATUS": "ontrack", "LT_STATUS_LABEL": "On Track", "LT_VAL": "163", "LT_TARGET": "30 &ndash; 180",
        "LT_MOM_DIR": "up", "LT_MOM_ARROW": "&#9650;", "LT_MOM_TEXT": "+16% vs. May", "LT_BARW": "85",
        "LT_NOTE": "Strong and near the top of the Lift range. A steady stream of high-intent traffic to the shop.",
        "LT_DIR_WORD": "up", "LT_X": "16", "LT_MORE_FEWER": "more",
        # PCR
        "PCR_STATUS": "ontrack", "PCR_STATUS_LABEL": "On Track", "PCR_VAL": "12.1", "PCR_TARGET": "10% &ndash; 16%",
        "PCR_MOM_DIR": "up", "PCR_MOM_ARROW": "&#9650;", "PCR_MOM_TEXT": "+1pp vs. May", "PCR_BARW": "70",
        "PCR_NOTE": "Inside the Lift range. Profile visitors are converting to followers at a healthy clip.",
        # goal tracker
        "GOAL1_TITLE": "Widen local discovery", "GOAL1_PCT": "78",
        "GOAL1_BASELINE": "48k views", "GOAL1_CURRENT": "82k views", "GOAL1_TARGET": "95k views",
        "GOAL1_NARRATIVE": "Views climbed for the third month running. On pace to clear the target by quarter-close.",
        "GOAL1_SPARKLINE_SVG": sparkline([61000, 70809, 82140], color="#0e3387"),
        "GOAL2_TITLE": "Build a save-worthy library", "GOAL2_PCT": "100",
        "GOAL2_BASELINE": "210 saves", "GOAL2_CURRENT": "421 saves", "GOAL2_TARGET": "400 saves",
        "GOAL2_NARRATIVE": "Target cleared. Reference carousels and styling Reels are doing the heavy lifting.",
        "GOAL2_SPARKLINE_SVG": sparkline([280, 314, 421], color="#65a30d"),
        "GOAL3_TITLE": "Drive qualified shop traffic", "GOAL3_PCT": "91",
        "GOAL3_BASELINE": "120 taps", "GOAL3_CURRENT": "163 taps", "GOAL3_TARGET": "180 taps",
        "GOAL3_NARRATIVE": "Link taps are the strongest part of the funnel and closing on the target.",
        "GOAL3_SPARKLINE_SVG": sparkline([128, 141, 163], color="#059669"),
        # lead signal
        "LS_SAVES": "421", "LS_SHARES": "108", "LS_PROFILE_VISITS": "1,210",
        "LS_LINK_TAPS": "163", "LS_CTR": "9.6",
        # top posts + all posts + prev
        "TOP_POSTS_HTML": tp1 + "\n" + tp2 + "\n" + tp3,
        "ALL_POSTS_JSON": json.dumps(all_posts, ensure_ascii=False),
        "PREV_REPORTS_HTML": prevs,
        # tests + watching
        "DIP_WHAT": "", "DIP_WATCH": "",
        "PATTERN1_HEAD": "Save-first content is the engine right now.",
        "PATTERN1_BODY": "Reference carousels and “one fix” styling Reels drove the top two posts and the best save month of the quarter. We&rsquo;re building two of these a week into July.",
        "PATTERN2_HEAD": "Tight-hook Reels are lifting retention.",
        "PATTERN2_BODY": "The Reels that opened on a single, specific mistake held attention well above the ones that opened on a soft intro. The hook style carries into next month.",
        "WATCH1_HEAD": "The Monday motivation static underperformed.",
        "WATCH1_BODY": "Soft, non-specific posts aren&rsquo;t earning the save right now. We&rsquo;re testing a sharper, more useful angle for that slot in July.",
        "WATCH2_HEAD": "The bloopers Reel reached well but didn&rsquo;t convert.",
        "WATCH2_BODY": "Strong views, light link taps. Fun reach content has a place, but we&rsquo;re pairing it with a clearer next step next month.",
        "TEST1_HEAD": "Two reference carousels a week.",
        "TEST1_BODY": "Lean into the format that&rsquo;s earning the most saves and see how high the save line can go inside the Lift range.",
        "TEST2_HEAD": "A clearer call to action on reach Reels.",
        "TEST2_BODY": "Add one specific next step to the high-reach, low-tap Reels and watch whether link taps follow the views.",
        "TEST3_HEAD": "Story polls into shop links.",
        "TEST3_BODY": "The June poll story drove a high tap rate. Test a poll-then-shop sequence to turn story engagement into traffic.",
        # CTAs
        "CTA_PRIMARY_OBJ": "Turn save-worthy content into shop visits",
        "CTA_PRIMARY_COPY": "&ldquo;Save this for your next outfit, then tap the link in bio to shop the edit.&rdquo;",
        "CTA_PRIMARY_RATIONALE": "Saves and link taps are both strong. The July priority is connecting the two, so the content people bookmark becomes the content that sends them to the shop.",
        "CTA_TOFU": "<em>“Tag a friend who needs this packing trick.”</em> &middot; Share-driven discovery.",
        "CTA_MOFU": "<em>“Save this edit for later.”</em> &middot; Save-prompted reference.",
        "CTA_BOFU": "<em>“Shop the look, link in bio.”</em> &middot; The conversion handoff.",
    }


def fill(tokens, template_path=TEMPLATE):
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
    for k, v in tokens.items():
        html = html.replace("{{" + k + "}}", str(v))
    return html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "..", "templates", "v8-worked-example.html"))
    ap.add_argument("--tokens", help="path to a JSON token map; defaults to the built-in worked example")
    args = ap.parse_args()

    if args.tokens:
        with open(args.tokens) as f:
            tokens = json.load(f)
    else:
        tokens = worked_example_tokens()

    html = fill(tokens)
    # Report any unfilled tokens (token-completeness check).
    import re
    leftover = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", html)))
    out = os.path.abspath(args.out)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {out}")
    if leftover:
        print(f"WARNING: {len(leftover)} unfilled tokens: {leftover}")
    else:
        print("All tokens filled. Template is render-complete.")


if __name__ == "__main__":
    main()

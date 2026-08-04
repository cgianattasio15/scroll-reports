"""
Scroll Media — Monthly Report Data Injector (v8, CI orchestrator)
Version 1.0 — June 2026

One command that fills BOTH data-heavy sections of a v8 report shell from Metricool,
at build time, with no runtime API calls:

  1. All Posts This Month table  -> the static ALL_POSTS array (via all_posts_data)
  2. Top 3 Posts cards           -> the {{TOP_POSTS_HTML}} slot (via the outlier engine)

It also writes a per-client summary (post count + top 3 posts) for the CI run artifact,
so Chase can draft narrative from the run without opening every shell.

This is the script the monthly GitHub Actions workflow calls per client. Idempotent:
re-running replaces the prior injection (All Posts by its `var ALL_POSTS =` line, Top 3
between HTML markers), so a re-dispatch cleanly refreshes the data.

Usage:
    python3 inject_report_data.py --client laneandkate --month 6 --year 2026 \
        --inject ../../laneandkate/june2026/index.html \
        --summary-out summaries/laneandkate.json
"""

import os
import re
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from outlier_engine import CLIENT_BLOG_IDS, get_top_posts
from build_v8_report import top_post_card, standout
import all_posts_data as apd

TP_START, TP_END = "<!--TP_START-->", "<!--TP_END-->"
BADGE = {"reel": ("reel-badge", "REEL"), "carousel": ("carousel-badge", "CAROUSEL"),
         "static": ("static-badge", "STATIC IMAGE"), "story": ("static-badge", "STORY")}


def _fmt_key(post):
    """Reuse the same precise classifier the All Posts table uses."""
    return apd._fmt_from_post(post)


def _mult_class(m):
    return "outlier-3x" if m >= 3 else ("outlier-2x" if m >= 2 else "outlier-1x")


def _split_caption(cap, n=170):
    cap = (cap or "").strip()
    if len(cap) <= n:
        return cap, ""
    cut = cap.rfind(" ", 0, n)
    cut = cut if cut > 0 else n
    return cap[:cut], cap[cut:]


def _hook(cap):
    cap = (cap or "").strip().replace("\n", " ")
    for stop in [". ", "! ", "? "]:
        i = cap.find(stop)
        if 0 < i < 90:
            return cap[:i + 1].strip()
    return (cap[:80].strip() + ("…" if len(cap) > 80 else "")) or "Top performing post"


def render_top_posts(posts):
    """Render up to 3 outlier-engine posts into post-card HTML (matches the shell)."""
    cards = []
    for i, p in enumerate(posts[:3], 1):
        fk = _fmt_key(p)
        bclass, blabel = BADGE.get(fk, ("static-badge", "STATIC IMAGE"))
        so = ""
        for s in p.get("standout_metrics", [])[:2]:
            m = s["multiplier"]
            so += standout(s["label"].upper(), s["value"], _mult_class(m), f"{m}x account avg")
        if not so:  # composite fallback: no single metric cleared the floor
            so = standout("PERFORMANCE", "Above avg", "outlier-1x", "multi-metric")
        prev, rest = _split_caption(p.get("caption", ""))
        uid = f"tp{fk}{i}"
        cards.append(top_post_card(
            rank=i, badge_class=bclass, badge_label=blabel,
            score=int(round(p.get("outlier_score", 0))),
            date=p.get("date", ""), fmt=blabel.title(),
            hook=_hook(p.get("caption", "")).replace('"', "&quot;"),
            caption_prev=prev, caption_rest=rest, standout_html=so,
            why=p.get("why_it_worked", ""), url=p.get("url", "#"), uid=uid))
    return "\n".join(cards)


def inject_top_posts(report_path, html_block):
    with open(report_path, encoding="utf-8") as f:
        html = f.read()
    wrapped = f"{TP_START}{html_block}{TP_END}"
    if "{{TOP_POSTS_HTML}}" in html:
        html = html.replace("{{TOP_POSTS_HTML}}", wrapped, 1)
    elif TP_START in html:
        region = re.search(re.escape(TP_START) + r"(.*?)" + re.escape(TP_END), html, re.S)
        if region and "post-card" in region.group(1):
            # KI-003: the marked region already holds hand-built Beat-4 cards -- a shell
            # carried over from the prior-month transform, or an already-finalized report.
            # The finalize step owns those cards; overwriting them here means a re-pull (or
            # the monthly pull re-hitting a finalized report, as cf34df9 did to all six July
            # reports) clobbers the crafted feature-2up. Leave it; finalize re-crafts. Only an
            # empty marker pair (a bare scaffold) is filled.
            pass
        else:
            html = re.sub(re.escape(TP_START) + r".*?" + re.escape(TP_END), wrapped, html, count=1, flags=re.S)
    else:
        # The Top-3 slot is a build precondition: the shell must carry either the
        # {{TOP_POSTS_HTML}} slot or a TP_START/TP_END pair. There is no posts-grid
        # fallback -- a bare `<div class="posts-grid">` fill used a greedy regex that
        # ran to the next `</section>`, swallowing the Beat-4 "other standout posts"
        # dropdown AND the quarter view on any report that carried a dropdown (it
        # damaged Launch Party + MEAS in the July 2026 cycle; both needed hand
        # recovery). Hard-fail instead of guessing at a grid. See KNOWN_ISSUES.md.
        sys.exit(f"No {{{{TOP_POSTS_HTML}}}} slot or TP markers in {report_path}; "
                 f"scaffold the shell first (add the Top-3 slot before injecting).")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", required=True)
    ap.add_argument("--blog-id", type=int)
    ap.add_argument("--month", type=int, required=True)
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--inject", required=True, help="path to the report shell")
    ap.add_argument("--summary-out", help="path to write the per-client summary JSON")
    args = ap.parse_args()

    blog_id = args.blog_id or CLIENT_BLOG_IDS.get(args.client)
    if not blog_id or not isinstance(blog_id, int):
        sys.exit(f"No valid blogId for '{args.client}' (got {blog_id!r}). Add it to CLIENT_BLOG_IDS.")

    # 1. All Posts table
    all_posts = apd.build_all_posts(blog_id, args.month, args.year)
    apd.inject(args.inject, all_posts)

    # 2. Top 3 Posts
    top = get_top_posts(blog_id, args.month, args.year, client_name=args.client)
    top_posts = top.get("posts", [])
    inject_top_posts(args.inject, render_top_posts(top_posts))

    # 3. Summary for the CI artifact
    summary = {
        "client": args.client, "month": args.month, "year": args.year,
        "all_posts_count": len(all_posts),
        "outliers_flagged": sum(1 for p in all_posts if p.get("outlier")),
        "top_posts": [{
            "url": p.get("url", ""),
            "type": _fmt_key(p),
            "standout": (f"{p['standout_metrics'][0]['label'].upper()}: "
                         f"{p['standout_metrics'][0]['value']}, "
                         f"{p['standout_metrics'][0]['multiplier']}x account avg"
                         if p.get("standout_metrics") else "composite (multi-metric)"),
            "caption_80": (p.get("caption", "") or "").replace("\n", " ")[:80],
        } for p in top_posts[:3]],
    }
    print("\nSUMMARY: " + json.dumps(summary, ensure_ascii=False))
    if args.summary_out:
        os.makedirs(os.path.dirname(args.summary_out) or ".", exist_ok=True)
        with open(args.summary_out, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"Injected {len(all_posts)} posts + {len(top_posts[:3])} top cards into {args.inject}")


if __name__ == "__main__":
    main()

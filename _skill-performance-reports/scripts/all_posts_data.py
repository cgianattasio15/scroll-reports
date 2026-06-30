"""
Scroll Media — All Posts Data Builder (v8 report, Change 9)
Version 1.0 — June 2026

Extends the Top Post Outlier Engine to pull EVERY post for the reporting month
(no outlier threshold) and emit the ALL_POSTS JavaScript array that the v8
report's "All Posts This Month" table renders STATICALLY at build time.

Why static: the table must make zero runtime API calls on page load. This script
runs once during the report build, caches the month's posts into the HTML, and the
deployed report is fully self-contained.

It reuses the same Metricool fetch + normalize + account-average logic as
`outlier_engine.py`, so the All Posts table's outlier highlighting matches the
Top 3 Posts outlier engine exactly.

Outlier flag (per post): set True when the post over-indexes on one of the two
T1-High buyer signals (Saves, CTR) at >= 1.5x the account month average, subject
to the same absolute floors used in the Top Post engine (prevents 1 save reading
as a 5x signal). CTR is per-post only when the post carries a measurable link;
otherwise the flag rests on Saves.

Usage (live, requires METRICOOL_TOKEN):
    python all_posts_data.py --client laneandkate --month 6 --year 2026 > all_posts.json
    # then paste the JSON in place of {{ALL_POSTS_JSON}} in the report HTML.

Usage (emit a JS-ready array and inject into a report file):
    python all_posts_data.py --client laneandkate --month 6 --year 2026 \
        --inject /workspace/scroll-reports/laneandkate/june2026/index.html
"""

import os
import sys
import json
import argparse

# Reuse the proven fetch/normalize/threshold logic from the outlier engine.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from outlier_engine import (
        fetch_posts, fetch_reels, normalize_post, CLIENT_BLOG_IDS,
        STANDOUT_MULTIPLIER, MIN_SAVES_FOR_STANDOUT,
    )
    _ENGINE = True
except Exception:
    # Engine import is optional for --mock / structural runs.
    _ENGINE = False
    CLIENT_BLOG_IDS = {}
    STANDOUT_MULTIPLIER = 1.5
    MIN_SAVES_FOR_STANDOUT = 4

# CTR is a rate. A 1-tap fluke shouldn't flag; require a small minimum link-tap base.
MIN_LINKTAPS_FOR_CTR_OUTLIER = 5


def _fmt_from_post(p: dict) -> str:
    """Classify a normalized post into the table's format key.

    The outlier engine only labels posts 'Reel' or 'Carousel / Image' and never
    reads the Metricool mediaType, so it can't split carousels from static images.
    We read the raw mediaType (preserved on the normalized post) for an exact call.
    Reels arrive via fetch_reels (is_reel=True). Stories are a separate Metricool
    endpoint the engine does not pull yet, so they won't appear until a story pull
    is added; the 'story' branch is kept so the data is forward-compatible.
    """
    if p.get("is_reel"):
        return "reel"
    raw = p.get("raw") or {}
    mt = str(raw.get("mediaType") or raw.get("type") or "").upper()
    if "CAROUSEL" in mt:
        return "carousel"
    if "VIDEO" in mt:      # feed video that is not a reel
        return "reel"
    if "STORY" in mt:
        return "story"
    if "IMAGE" in mt or "PHOTO" in mt:
        return "static"
    return "static"        # safe default when mediaType is missing


def _date_display(date_str: str) -> str:
    """'June 4, 2026' -> 'Jun 4'. Falls back to the raw string."""
    try:
        from datetime import datetime
        dt = datetime.strptime(date_str, "%B %d, %Y")
        return dt.strftime("%b %-d")
    except Exception:
        return (date_str or "")[:12]


def _iso_date(date_str: str) -> str:
    """'June 4, 2026' -> '2026-06-04' for correct chronological sorting in the table."""
    try:
        from datetime import datetime
        dt = datetime.strptime(date_str, "%B %d, %Y")
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return date_str or ""


def build_all_posts(blog_id: int, month: int, year: int) -> list:
    """Pull every post + reel for the month, compute account averages, flag outliers."""
    if not _ENGINE:
        raise RuntimeError("outlier_engine not importable; cannot run a live pull.")

    raw_posts = fetch_posts(blog_id, month, year)
    raw_reels = fetch_reels(blog_id, month, year)

    content = [normalize_post(p, is_reel=False) for p in raw_posts]
    content += [normalize_post(r, is_reel=True) for r in raw_reels]
    if not content:
        return []

    n = len(content)
    avg_saves = sum(p["saves"] for p in content) / n

    # Per-post CTR / link taps usually come from IG Insights, not Metricool's post API.
    # When present on the normalized post, use them; else leave null.
    ctr_vals = [p.get("ctr") for p in content if p.get("ctr") not in (None, 0)]
    avg_ctr = (sum(ctr_vals) / len(ctr_vals)) if ctr_vals else 0

    rows = []
    for p in content:
        saves = p.get("saves") or 0
        ctr = p.get("ctr")
        linktaps = p.get("linktaps") or p.get("link_taps")

        saves_outlier = (
            avg_saves > 0 and saves >= MIN_SAVES_FOR_STANDOUT
            and (saves / avg_saves) >= STANDOUT_MULTIPLIER
        )
        ctr_outlier = (
            ctr is not None and avg_ctr > 0
            and (linktaps or 0) >= MIN_LINKTAPS_FOR_CTR_OUTLIER
            and (ctr / avg_ctr) >= STANDOUT_MULTIPLIER
        )

        rows.append({
            "date": _iso_date(p["date"]),
            "date_display": _date_display(p["date"]),
            "format": _fmt_from_post(p),
            "caption": (p.get("caption") or "").replace("\n", " ").strip(),
            "views": int(p.get("views") or 0),
            "saves": int(saves),
            "shares": int(p.get("shares") or 0),
            "comments": int(p.get("comments") or 0),
            "retention": p.get("retention"),          # null for non-video
            "linktaps": linktaps if linktaps else None,
            "ctr": round(ctr, 1) if ctr is not None else None,
            "url": p.get("url") or "",
            "outlier": bool(saves_outlier or ctr_outlier),
        })

    rows.sort(key=lambda r: r["date"], reverse=True)
    return rows


def inject(report_path: str, posts: list) -> None:
    """Replace the {{ALL_POSTS_JSON}} token (or a prior array) in a report file."""
    with open(report_path, "r", encoding="utf-8") as f:
        html = f.read()
    payload = json.dumps(posts, ensure_ascii=False)
    marker = "var ALL_POSTS = "
    start = html.find(marker)
    if start == -1:
        sys.exit("Could not find 'var ALL_POSTS =' in the report.")
    end = html.find(";", start)
    html = html[:start] + marker + payload + html[end:]
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Injected {len(posts)} posts into {report_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", help="client slug, e.g. laneandkate")
    ap.add_argument("--blog-id", type=int)
    ap.add_argument("--month", type=int, required=True)
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--inject", help="path to a report HTML to inject the array into")
    args = ap.parse_args()

    blog_id = args.blog_id or CLIENT_BLOG_IDS.get(args.client or "")
    if not blog_id:
        sys.exit(f"Unknown client slug '{args.client}'. Pass --blog-id or a known slug: {list(CLIENT_BLOG_IDS)}")

    posts = build_all_posts(blog_id, args.month, args.year)
    if args.inject:
        inject(args.inject, posts)
    else:
        print(json.dumps(posts, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

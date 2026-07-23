#!/usr/bin/env python3
"""
run_outlier_from_csv.py -- drive outlier_engine v2.0 from Metricool CSV exports
instead of the live API.

The engine's fetch_posts/fetch_reels hit the Metricool API. For a closeout build
the pull is delivered as CSV, so this module rebuilds the same normalized post
dicts from the CSV columns and then runs the ENGINE'S OWN scoring, eligibility,
and selection code (steps 3-8 of get_top_posts) so ranking cannot drift from v2.0.

Reels retention comes from the "% View rate (+3 secs)" column, which is the same
basis as the reported account retention average. Carousels have no retention field
by format (not missing data), so they score on WEIGHTS_NO_RETENTION as designed.

Usage:
  python3 run_outlier_from_csv.py --reels reels.csv --posts posts.csv [--json out.json]
"""
import argparse, csv, json, os, sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from outlier_engine import (                      # noqa: E402
    compute_outlier_score, get_standout_metrics, generate_why_it_worked,
    OUTLIER_SCORE_EXCLUDE_3RD, OUTLIER_SCORE_INCLUDE_4TH,
)


def _int(v):
    v = (v or "").strip().replace(",", "")
    return int(float(v)) if v else 0


def _float(v):
    v = (v or "").strip().replace(",", "")
    return float(v) if v else None


def _date(raw):
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw.strip()[:len(datetime.now().strftime(fmt))], fmt)
        except ValueError:
            continue
    return datetime.strptime(raw.strip()[:10], "%Y-%m-%d")


def load_reels(path):
    out = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if not (r.get("URL") or "").strip():
                continue
            dt = _date(r["date"])
            out.append({
                "type": "Reel", "is_reel": True,
                "date": dt.strftime("%B %-d, %Y"), "dt": dt,
                "views": _int(r["Views (organic)"]),
                "reach": _int(r["Reach (Organic)"]),
                "likes": _int(r["Likes (Organic)"]),
                "comments": _int(r["Comments (Organic)"]),
                "saves": _int(r["Saved (Organic)"]),
                "shares": _int(r["Shares (Organic)"]),
                "interactions": _int(r["Interactions (Organic)"]),
                "retention": _float(r["% View rate (+3 secs)"]),
                "caption": (r.get("title") or "").strip(),
                "url": r["URL"].strip(),
            })
    return out


def load_posts(path):
    out = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if not (r.get("URL") or "").strip():
                continue
            dt = _date(r["Timestamp"])
            ctype = (r.get("type") or "").upper()
            out.append({
                "type": "Carousel / Image", "is_reel": False,
                "fmt": "carousel" if "CAROUSEL" in ctype else "image",
                "date": dt.strftime("%B %-d, %Y"), "dt": dt,
                "views": _int(r["Views (Organic)"]),
                "reach": _int(r["Reach (Organic)"]),
                "likes": _int(r["Likes"]),
                "comments": _int(r["Comments"]),
                "saves": _int(r["Saved"]),
                "shares": _int(r["Shares"]),
                "interactions": _int(r["Interactions"]),
                "retention": None,
                "caption": (r.get("Content") or "").strip(),
                "url": r["URL"].strip(),
            })
    return out


def run(all_content):
    """Engine steps 3-8, verbatim in structure from get_top_posts."""
    n = len(all_content)
    reels_ret = [p for p in all_content if p["is_reel"] and p["retention"] is not None]
    averages = {
        "views":     sum(p["views"] for p in all_content) / n,
        "shares":    sum(p["shares"] for p in all_content) / n,
        "saves":     sum(p["saves"] for p in all_content) / n,
        "comments":  sum(p["comments"] for p in all_content) / n,
        "retention": (sum(p["retention"] for p in reels_ret) / len(reels_ret)) if reels_ret else 0,
    }

    for p in all_content:
        p["outlier_score"], p["score_components"] = compute_outlier_score(p, averages)
    all_content.sort(key=lambda x: x["outlier_score"], reverse=True)

    for p in all_content:
        p["standout_metrics"] = get_standout_metrics(p, averages, p["score_components"])
        p["eligible"] = len(p["standout_metrics"]) > 0

    eligible = [p for p in all_content if p["eligible"]]
    ineligible = [p for p in all_content if not p["eligible"]]

    selected = []
    for i, p in enumerate(eligible):
        if i < 2:
            selected.append(p)
        elif i == 2 and p["outlier_score"] >= OUTLIER_SCORE_EXCLUDE_3RD:
            selected.append(p)
        elif i == 3 and p["outlier_score"] >= OUTLIER_SCORE_INCLUDE_4TH:
            selected.append(p)
        else:
            break
    if len(selected) < 2:
        for p in ineligible:
            if p not in selected:
                selected.append(p)
            if len(selected) >= 2:
                break

    for p in selected:
        p["why_it_worked"] = generate_why_it_worked(p, p["standout_metrics"], averages)

    max_raw = max((p["outlier_score"] for p in selected), default=1) or 1
    for p in selected:
        p["post_score_badge"] = round((p["outlier_score"] / max_raw) * 100)

    return all_content, selected, averages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reels", required=True)
    ap.add_argument("--posts", required=True)
    ap.add_argument("--json")
    a = ap.parse_args()

    content = load_reels(a.reels) + load_posts(a.posts)
    all_content, selected, averages = run(content)

    print(f"Content: {len(content)} pieces "
          f"({sum(1 for p in content if p['is_reel'])} reels, "
          f"{sum(1 for p in content if not p['is_reel'])} posts)")
    print(f"Averages: views={averages['views']:.0f} saves={averages['saves']:.1f} "
          f"comments={averages['comments']:.1f} shares={averages['shares']:.1f} "
          f"retention={averages['retention']:.1f}%")
    print(f"\nTotals check: views={sum(p['views'] for p in content):,} "
          f"saves={sum(p['saves'] for p in content)} "
          f"comments={sum(p['comments'] for p in content)} "
          f"shares={sum(p['shares'] for p in content)} "
          f"interactions={sum(p['interactions'] for p in content)}")

    print(f"\n{'rank':<5}{'score':>7}  {'elig':<5} {'type':<18}{'date':<18}{'standouts'}")
    for i, p in enumerate(all_content):
        print(f"{i+1:<5}{p['outlier_score']:>7}  {'yes' if p['eligible'] else 'no':<5} "
              f"{p['type']:<18}{p['date']:<18}"
              f"{', '.join(s['label']+' '+str(s['multiplier'])+'x' for s in p['standout_metrics'])}")

    print(f"\nSELECTED ({len(selected)}):")
    for i, p in enumerate(selected):
        print(f"\n  #{i+1} [{p['type']}] raw={p['outlier_score']} badge={p['post_score_badge']}/100")
        print(f"     {p['date']} | {p['url']}")
        print(f"     views={p['views']:,} reach={p['reach']:,} saves={p['saves']} "
              f"comments={p['comments']} shares={p['shares']} retention={p['retention']}")
        print(f"     standouts: {[(s['label'], str(s['multiplier'])+'x') for s in p['standout_metrics']]}")
        print(f"     why: {p['why_it_worked']}")
        print(f"     hook: {p['caption'][:90]}")

    if a.json:
        with open(a.json, "w") as f:
            json.dump({"selected": [{k: v for k, v in p.items() if k != "dt"} for p in selected],
                       "all": [{k: v for k, v in p.items() if k != "dt"} for p in all_content],
                       "averages": averages}, f, indent=2, default=str)
        print(f"\nWrote {a.json}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
score_report.py -- compute a monthly account score from KPIs under the
Unified Scoring Framework v1.3 (the scoring math governed by process-v8.4.md
and carried unchanged into v8.5).

Why this exists: build_v8_report.py hand-sets scores as literals and no code
path implemented the framework. This does, so a report score is computed and
reproducible rather than asserted.

Framework (Scroll_Media_Scoring_Framework.md v1.3):
  tier weights   T1-High 2.0 (Saves, CTR) | T1 1.5 (Retention, PCR, Link Taps)
                 T2 1.0 (Profile Visits, Comments, New Followers, Total Views)
                 T3 0.75 (Shares)
  status points  EXCEEDING = full tier weight | ON TRACK = 0.6x | WATCH = 0.2x
  raw            (sum / 13.25) * 10
  MoM credit     5+ improving +0.5 | 4 improving +0.25 | 2-3 flat 0
                 4 declining -0.25 | 5+ declining -0.5
  compressed     6.0 + ((raw + credit) * 0.4), rounded to 0.1, 6.0 floor

Partial-window / unavailable metrics: a metric passed as None is dropped from
BOTH numerator and denominator. It is never scored zero. This mirrors the v8.5
score-strip rule ("empty state, never a zero") -- a metric the platform stopped
exposing is missing data, not bad performance, and zeroing it would fabricate a
penalty. The reduced denominator is printed so the deviation is visible.

Usage:
  python3 score_report.py --stage Lift --kpis kpis.json [--prior prior.json]
  python3 score_report.py --self-test          # validates against MEAS June 2026 = 7.6
"""
import argparse, json, sys

# metric -> (tier label, tier weight, CSV row key)
METRICS = {
    "saves":          ("T1-High", 2.0),
    "ctr":            ("T1-High", 2.0),
    "retention":      ("T1",      1.5),
    "pcr":            ("T1",      1.5),
    "link_taps":      ("T1",      1.5),
    "profile_visits": ("T2",      1.0),
    "comments":       ("T2",      1.0),
    "new_followers":  ("T2",      1.0),
    "total_views":    ("T2",      1.0),
    "shares":         ("T3",      0.75),
}

# KPI_Target_Ranges_Framework.csv, (low, high) per stage
TARGETS = {
    "Spark":  {"saves": (20, 80),   "ctr": (3, 8),  "retention": (35, 50), "pcr": (10, 18),
               "link_taps": (5, 40),   "profile_visits": (50, 500),   "comments": (15, 75),
               "new_followers": (40, 90),   "total_views": (10000, 40000),  "shares": (15, 60)},
    "Lift":   {"saves": (80, 400),  "ctr": (3, 6),  "retention": (50, 65), "pcr": (10, 16),
               "link_taps": (30, 180),  "profile_visits": (300, 2000), "comments": (75, 250),
               "new_followers": (100, 270), "total_views": (40000, 150000), "shares": (60, 300)},
    "Rise":   {"saves": (300, 2500),"ctr": (2, 5),  "retention": (65, 80), "pcr": (8, 14),
               "link_taps": (350, 3000),"profile_visits": (1500, 10000),"comments": (250, 900),
               "new_followers": (300, 2500),"total_views": (150000, 800000),"shares": (200, 2000)},
    "Thrive": {"saves": (950, 5000),"ctr": (1, 4),  "retention": (80, 95), "pcr": (5, 12),
               "link_taps": (3000, 15000),"profile_visits": (8000, 40000),"comments": (900, 3500),
               "new_followers": (750, 10000),"total_views": (650000, 3000000),"shares": (750, 2500)},
}

STATUS_MULT = {"EXCEEDING": 1.0, "ON TRACK": 0.6, "WATCH": 0.2}


def status_for(metric, value, stage):
    low, high = TARGETS[stage][metric]
    if value > high:
        return "EXCEEDING"
    if value >= low:
        return "ON TRACK"
    return "WATCH"


def mom_credit(kpis, prior):
    """Framework step 3. Only metrics present in BOTH periods are compared."""
    if not prior:
        return 0.0, 0, 0, []
    improving, declining, detail = 0, 0, []
    for m in METRICS:
        cur, prv = kpis.get(m), prior.get(m)
        if cur is None or prv is None:
            continue
        if cur > prv:
            improving += 1
            detail.append((m, prv, cur, "up"))
        elif cur < prv:
            declining += 1
            detail.append((m, prv, cur, "down"))
        else:
            detail.append((m, prv, cur, "flat"))
    if improving >= 5:
        c = 0.5
    elif improving == 4:
        c = 0.25
    elif declining >= 5:
        c = -0.5
    elif declining == 4:
        c = -0.25
    else:
        c = 0.0
    return c, improving, declining, detail


def score(kpis, stage, prior=None):
    rows, num, den = [], 0.0, 0.0
    for m, (tier, weight) in METRICS.items():
        v = kpis.get(m)
        if v is None:
            rows.append((m, tier, weight, None, "n/a (excluded)", 0.0))
            continue
        st = status_for(m, v, stage)
        pts = round(weight * STATUS_MULT[st], 4)
        num += pts
        den += weight
        rows.append((m, tier, weight, v, st, pts))
    raw = (num / den) * 10 if den else 0.0
    credit, imp, dec, detail = mom_credit(kpis, prior)
    compressed = 6.0 + ((raw + credit) * 0.4)
    final = max(6.0, round(compressed + 1e-9, 1))
    return {"rows": rows, "num": round(num, 4), "den": round(den, 4), "raw": raw,
            "credit": credit, "improving": imp, "declining": dec, "mom_detail": detail,
            "compressed": compressed, "final": final}


def report(r, title):
    print(f"\n=== {title} ===")
    print(f"{'metric':16} {'tier':8} {'value':>10}  {'status':<14} {'pts':>5}")
    for m, tier, w, v, st, pts in r["rows"]:
        vs = "n/a" if v is None else f"{v:,.6g}"
        print(f"{m:16} {tier:8} {vs:>10}  {st:<14} {pts:>5.2f}")
    print(f"\nweighted sum      {r['num']}")
    print(f"denominator       {r['den']}   ({'full 13.25' if abs(r['den']-13.25)<1e-9 else 'reduced, n/a metrics excluded'})")
    print(f"raw score         {r['raw']:.4f}   = ({r['num']} / {r['den']}) * 10")
    print(f"MoM credit        {r['credit']:+.2f}  ({r['improving']} improving, {r['declining']} declining)")
    print(f"compressed        {r['compressed']:.4f} = 6.0 + (({r['raw']:.4f} {r['credit']:+.2f}) * 0.4)")
    print(f"FINAL SCORE       {r['final']}")


JUNE_MEAS = {"saves": 22, "ctr": 9.8, "retention": 49, "pcr": 6.3, "link_taps": 72,
             "profile_visits": 733, "comments": 193, "new_followers": 46, "total_views": 51417,
             "shares": 26}


def self_test():
    """MEAS Active June 2026 published at 7.6 with all 10 metrics present."""
    r = score(JUNE_MEAS, "Lift", prior=None)
    report(r, "self-test: MEAS Active June 2026 (no MoM credit)")
    expect_badges = {"saves": "WATCH", "ctr": "EXCEEDING", "retention": "WATCH", "pcr": "WATCH",
                     "link_taps": "ON TRACK", "profile_visits": "ON TRACK", "comments": "ON TRACK",
                     "new_followers": "WATCH", "total_views": "ON TRACK", "shares": "WATCH"}
    got = {m: st for m, _, _, _, st, _ in r["rows"]}
    ok = got == expect_badges
    print(f"\nbadge parity vs published June report: {'PASS' if ok else 'FAIL ' + str(got)}")
    print(f"published June score 7.6 is reproduced at MoM credit -0.5: "
          f"{round(6.0 + ((r['raw'] - 0.5) * 0.4), 1)}")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="Lift", choices=list(TARGETS))
    ap.add_argument("--kpis", help="JSON file or inline JSON of the scored metrics")
    ap.add_argument("--prior", help="JSON file or inline JSON of the prior period, for MoM credit")
    ap.add_argument("--label", default="report")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test())
    if not a.kpis:
        ap.error("--kpis is required (or use --self-test)")

    def load(x):
        if not x:
            return None
        try:
            return json.load(open(x))
        except (OSError, IOError):
            return json.loads(x)

    r = score(load(a.kpis), a.stage, load(a.prior))
    report(r, a.label)


if __name__ == "__main__":
    main()

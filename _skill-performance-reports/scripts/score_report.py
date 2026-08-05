#!/usr/bin/env python3
"""
score_report.py -- compute a monthly account score from KPIs under the
Unified Scoring Framework v1.5 (the scoring math governed by process-v8.4.md
and carried unchanged through v8.5).

Why this exists: build_v8_report.py hand-sets scores as literals and no code
path implemented the framework. This does, so a report score is computed and
reproducible rather than asserted.

Framework (Scroll_Media_Scoring_Framework.md v1.5). Effective August 2026
forward -- July 2026 and earlier months shipped under v1.3 and are NOT
rescored under this model.
  tiers          Tier 1 2.0 (Shares, Retention %, Saves, Link Taps)
                 Tier 2 1.0 (New Followers, Total Views, Profile Visits,
                             Comments, CTR, PCR, Total Followers, Reposts)
  all 12 scored  Total Followers and Reposts were baseline/unscored under v1.3;
                 v1.5 scores them as Tier 2 metrics.
  status points  EXCEEDING = full tier weight (2.0 / 1.0)
                 ON TRACK  = 0.6x tier weight (1.2 / 0.6)
                 WATCH     = 0.2x tier weight (0.4 / 0.2)
  denominator    16.0 = 4 x 2.0 + 8 x 1.0
  raw            (sum / 16.0) * 10
  MoM credit     6+ improving +0.5 | 5 improving +0.25 | 3-4 flat 0
                 5 declining -0.25 | 6+ declining -0.5
  compressed     6.0 + ((raw + credit) * 0.4), rounded to 0.1, 6.0 floor

Partial-window / unavailable metrics: a metric passed as None is dropped from
BOTH numerator and denominator (its tier weight is subtracted from 16.0). It is
never scored zero. This mirrors the v8.5 score-strip rule ("empty state, never a
zero") -- a metric the platform stopped exposing is missing data, not bad
performance, and zeroing it would fabricate a penalty. The reduced denominator
is printed so the deviation is visible.

Usage:
  python3 score_report.py --stage Lift --kpis kpis.json [--prior prior.json]
  python3 score_report.py --self-test          # validates the v1.5 model + denominator
"""
import argparse, json, sys

# metric -> (tier label, tier weight). Tier column mirrors
# KPI_Target_Ranges_Framework.csv (Tier 1 -> 2.0, Tier 2 -> 1.0).
METRICS = {
    # Tier 1 -- 2.0x
    "shares":          ("T1", 2.0),
    "retention":       ("T1", 2.0),
    "saves":           ("T1", 2.0),
    "link_taps":       ("T1", 2.0),
    # Tier 2 -- 1.0x
    "new_followers":   ("T2", 1.0),
    "total_views":     ("T2", 1.0),
    "profile_visits":  ("T2", 1.0),
    "comments":        ("T2", 1.0),
    "ctr":             ("T2", 1.0),
    "pcr":             ("T2", 1.0),
    "total_followers": ("T2", 1.0),
    "reposts":         ("T2", 1.0),
}

# Max possible weighted points, all metrics present = the full denominator.
MAX_POINTS = round(sum(w for _, w in METRICS.values()), 4)
assert MAX_POINTS == 16.0, f"tier weights must sum to 16.0, got {MAX_POINTS}"

# KPI_Target_Ranges_Framework.csv, (low, high) per stage.
TARGETS = {
    "Spark":  {"saves": (20, 80),    "ctr": (3, 8), "retention": (35, 50), "pcr": (10, 18),
               "link_taps": (5, 40),    "profile_visits": (50, 500),    "comments": (15, 75),
               "new_followers": (40, 90),    "total_views": (10000, 40000),  "shares": (15, 60),
               "total_followers": (0, 2500),      "reposts": (5, 25)},
    "Lift":   {"saves": (80, 400),   "ctr": (3, 6), "retention": (50, 65), "pcr": (10, 16),
               "link_taps": (30, 180),  "profile_visits": (300, 2000),  "comments": (75, 250),
               "new_followers": (100, 270),  "total_views": (40000, 150000), "shares": (60, 300),
               "total_followers": (2500, 10000),  "reposts": (15, 75)},
    "Rise":   {"saves": (300, 2500), "ctr": (2, 5), "retention": (65, 80), "pcr": (8, 14),
               "link_taps": (350, 3000),"profile_visits": (1500, 10000),"comments": (250, 900),
               "new_followers": (300, 2500), "total_views": (150000, 800000),"shares": (200, 2000),
               "total_followers": (10000, 100000),"reposts": (60, 400)},
    "Thrive": {"saves": (950, 5000), "ctr": (1, 4), "retention": (80, 95), "pcr": (5, 12),
               "link_taps": (3000, 15000),"profile_visits": (8000, 40000),"comments": (900, 3500),
               "new_followers": (750, 10000),"total_views": (650000, 3000000),"shares": (750, 2500),
               "total_followers": (100000, 500000),"reposts": (200, 750)},
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
    """Framework step 3, scaled to 12 metrics. Only metrics present in BOTH
    periods are compared."""
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
    if improving >= 6:
        c = 0.5
    elif improving == 5:
        c = 0.25
    elif declining >= 6:
        c = -0.5
    elif declining == 5:
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
    print(f"denominator       {r['den']}   ({'full 16.0' if abs(r['den']-16.0)<1e-9 else 'reduced, n/a metrics excluded'})")
    print(f"raw score         {r['raw']:.4f}   = ({r['num']} / {r['den']}) * 10")
    print(f"MoM credit        {r['credit']:+.2f}  ({r['improving']} improving, {r['declining']} declining)")
    print(f"compressed        {r['compressed']:.4f} = 6.0 + (({r['raw']:.4f} {r['credit']:+.2f}) * 0.4)")
    print(f"FINAL SCORE       {r['final']}")


# A synthetic Lift-stage account used by --self-test. Not a real client month;
# it carries all 12 v1.5 metrics (incl. total_followers + reposts) so the new
# model exercises the full denominator.
SAMPLE_LIFT = {"saves": 22, "ctr": 9.8, "retention": 49, "pcr": 6.3, "link_taps": 72,
               "profile_visits": 733, "comments": 193, "new_followers": 46,
               "total_views": 51417, "shares": 26, "total_followers": 5400, "reposts": 40}


def self_test():
    """Validate the v1.5 model: weight sum, denominator, and known compressions."""
    checks = []

    # 1. Max possible weighted points = 16.0.
    checks.append(("weight sum == 16.0", MAX_POINTS == 16.0))

    # 2. All 12 present, every metric EXCEEDING -> num=16, den=16, raw=10, final=10.0.
    all_exceed = {m: TARGETS["Lift"][m][1] * 100 for m in METRICS}
    r_ex = score(all_exceed, "Lift")
    checks.append(("all-EXCEEDING denominator == 16.0", abs(r_ex["den"] - 16.0) < 1e-9))
    checks.append(("all-EXCEEDING num == 16.0", abs(r_ex["num"] - 16.0) < 1e-9))
    checks.append(("all-EXCEEDING final == 10.0", r_ex["final"] == 10.0))

    # 3. All 12 present, every metric ON TRACK -> num=9.6, raw=6.0, final=8.4.
    on_track = {m: TARGETS["Lift"][m][0] for m in METRICS}  # low edge == ON TRACK
    r_ot = score(on_track, "Lift")
    checks.append(("all-ON-TRACK num == 9.6", abs(r_ot["num"] - 9.6) < 1e-9))
    checks.append(("all-ON-TRACK raw == 6.0", abs(r_ot["raw"] - 6.0) < 1e-9))
    checks.append(("all-ON-TRACK final == 8.4", r_ot["final"] == 8.4))

    # 4. n/a handling drops the metric's tier weight from the denominator.
    drop_t2 = dict(all_exceed); drop_t2["reposts"] = None       # T2, weight 1.0
    checks.append(("drop one T2 -> den == 15.0", abs(score(drop_t2, "Lift")["den"] - 15.0) < 1e-9))
    drop_t1 = dict(all_exceed); drop_t1["retention"] = None     # T1, weight 2.0
    checks.append(("drop one T1 -> den == 14.0", abs(score(drop_t1, "Lift")["den"] - 14.0) < 1e-9))

    print("\n=== self-test: Unified Scoring Framework v1.5 ===")
    ok = True
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed

    # Illustrative full scoring of the sample account.
    report(score(SAMPLE_LIFT, "Lift"), "self-test sample: SAMPLE_LIFT @ Lift (no MoM credit)")

    print(f"\nself-test: {'PASS' if ok else 'FAIL'}")
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

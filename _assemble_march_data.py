"""
Assemble final March 2026 data for all 7 clients.
- Metricool data: views, shares, saves, comments, watch time, retention, reach
- February IG Insights (from sheet): followers, new_followers, profile_visits, link_taps
  (used as proxy for March IG Insights since that endpoint isn't available via API)
- NOTE: March IG Insights (followers, new_followers, profile_visits, link_taps) 
  need to be entered manually from IG Insights. We use Feb as placeholder and flag.
- Calculates scores using Scroll Media Weighted Performance Framework v2.0
"""

import json

# ── MARCH METRICOOL DATA (from API pull) ──────────────────────────────────
march_metricool = {
    "Launch Party": {
        "total_views": 26961, "total_shares": 50, "total_saves": 37,
        "total_comments": 161, "avg_reach_per_day": 537,
        "avg_watch_time": 0.0, "avg_retention_pct": 0.0,
    },
    "Lane & Kate": {
        "total_views": 12277, "total_shares": 26, "total_saves": 4,
        "total_comments": 43, "avg_reach_per_day": 218,
        "avg_watch_time": 0.0, "avg_retention_pct": 0.0,
    },
    "Skin by Brownlee": {
        "total_views": 21435, "total_shares": 30, "total_saves": 73,
        "total_comments": 154, "avg_reach_per_day": 426,
        "avg_watch_time": 0.0, "avg_retention_pct": 0.0,
    },
    "MEAS Active": {
        "total_views": 17018, "total_shares": 31, "total_saves": 7,
        "total_comments": 64, "avg_reach_per_day": 294,
        "avg_watch_time": 0.0, "avg_retention_pct": 0.0,
    },
    "Up & Running": {
        "total_views": 19518, "total_shares": 11, "total_saves": 5,
        "total_comments": 9, "avg_reach_per_day": 102,
        "avg_watch_time": 0.0, "avg_retention_pct": 0.0,
    },
    "DEFINE Oakley": {
        "total_views": 21778, "total_shares": 20, "total_saves": 5,
        "total_comments": 67, "avg_reach_per_day": 422,
        "avg_watch_time": 0.0, "avg_retention_pct": 0.0,
    },
    "Ombre Gallery": {
        "total_views": 12284, "total_shares": 52, "total_saves": 24,
        "total_comments": 107, "avg_reach_per_day": 239,
        "avg_watch_time": 0.0, "avg_retention_pct": 0.0,
    },
}

# Load watch time / retention from the raw data
try:
    with open("/home/ubuntu/march_raw.json") as f:
        march_raw = json.load(f)
    for name, d in march_raw.items():
        if name in march_metricool:
            march_metricool[name]["avg_watch_time"] = d.get("avg_watch_time", 0.0)
            march_metricool[name]["avg_retention_pct"] = d.get("avg_retention_pct", 0.0)
            march_metricool[name]["avg_reach_per_day"] = d.get("avg_reach_per_day", march_metricool[name]["avg_reach_per_day"])
except:
    pass

# ── FEBRUARY IG INSIGHTS (from Performance Data Sheet) ────────────────────
# These are the IG Insights metrics that require manual input.
# March values are estimated from February as placeholder — flag for manual update.
feb_ig_insights = {
    "Launch Party":     {"total_followers": 5373,  "new_followers": 69,  "profile_visits": 621,  "link_taps": 94},
    "Lane & Kate":      {"total_followers": 7143,  "new_followers": 79,  "profile_visits": 761,  "link_taps": 138},
    "Skin by Brownlee": {"total_followers": 32866, "new_followers": 481, "profile_visits": 3083, "link_taps": 401},
    "MEAS Active":      {"total_followers": 10200, "new_followers": 84,  "profile_visits": 1015, "link_taps": 132},
    "Up & Running":     {"total_followers": 2307,  "new_followers": 27,  "profile_visits": 249,  "link_taps": 6},
    "DEFINE Oakley":    {"total_followers": 3655,  "new_followers": 31,  "profile_visits": 584,  "link_taps": 24},
    "Ombre Gallery":    {"total_followers": 0,     "new_followers": 0,   "profile_visits": 0,    "link_taps": 0},
}

# ── FEBRUARY METRICOOL (from API pull) ────────────────────────────────────
feb_metricool = {
    "Launch Party":     {"total_views": 30418, "total_shares": 61, "total_saves": 55, "total_comments": 125, "avg_reach_per_day": 594},
    "Lane & Kate":      {"total_views": 12776, "total_shares": 39, "total_saves": 6,  "total_comments": 27,  "avg_reach_per_day": 241},
    "Skin by Brownlee": {"total_views": 23165, "total_shares": 40, "total_saves": 103,"total_comments": 114, "avg_reach_per_day": 471},
    "MEAS Active":      {"total_views": 22608, "total_shares": 40, "total_saves": 3,  "total_comments": 120, "avg_reach_per_day": 326},
    "Up & Running":     {"total_views": 24524, "total_shares": 44, "total_saves": 3,  "total_comments": 24,  "avg_reach_per_day": 877},
    "DEFINE Oakley":    {"total_views": 13778, "total_shares": 27, "total_saves": 3,  "total_comments": 25,  "avg_reach_per_day": 493},
    "Ombre Gallery":    {"total_views": 4729,  "total_shares": 6,  "total_saves": 12, "total_comments": 19,  "avg_reach_per_day": 169},
}

# ── KPI TARGETS BY STAGE ──────────────────────────────────────────────────
KPI_TARGETS = {
    "Spark": {
        "avg_reach_per_day": {"low": 300,  "high": 1200},
        "new_followers":     {"low": 40,   "high": 90},
        "shares":            {"low": 15,   "high": 60},
        "total_views":       {"low": 10000,"high": 40000},
        "profile_visits":    {"low": 50,   "high": 500},
        "avg_watch_time":    {"low": 3,    "high": 6},
        "retention_pct":     {"low": 35,   "high": 50},
        "saves":             {"low": 20,   "high": 80},
        "comments":          {"low": 15,   "high": 75},
        "ctr":               {"low": 3,    "high": 8},
        "link_taps":         {"low": 5,    "high": 40},
        "pcr":               {"low": 10,   "high": 18},
    },
    "Lift": {
        "avg_reach_per_day": {"low": 1500, "high": 5000},
        "new_followers":     {"low": 100,  "high": 270},
        "shares":            {"low": 60,   "high": 300},
        "total_views":       {"low": 40000,"high": 150000},
        "profile_visits":    {"low": 300,  "high": 2000},
        "avg_watch_time":    {"low": 6,    "high": 10},
        "retention_pct":     {"low": 50,   "high": 65},
        "saves":             {"low": 80,   "high": 400},
        "comments":          {"low": 75,   "high": 250},
        "ctr":               {"low": 3,    "high": 6},
        "link_taps":         {"low": 30,   "high": 180},
        "pcr":               {"low": 10,   "high": 16},
    },
    "Rise": {
        "avg_reach_per_day": {"low": 5000, "high": 20000},
        "new_followers":     {"low": 300,  "high": 2500},
        "shares":            {"low": 200,  "high": 2000},
        "total_views":       {"low": 150000,"high": 800000},
        "profile_visits":    {"low": 1500, "high": 10000},
        "avg_watch_time":    {"low": 10,   "high": 15},
        "retention_pct":     {"low": 65,   "high": 80},
        "saves":             {"low": 300,  "high": 2500},
        "comments":          {"low": 250,  "high": 900},
        "ctr":               {"low": 2,    "high": 5},
        "link_taps":         {"low": 350,  "high": 3000},
        "pcr":               {"low": 8,    "high": 14},
    },
}

# ── TIER WEIGHTS — Unified Scoring Framework v1.2 ────────────────────────────
# Buyer Intent Hierarchy:
#   T1H (2.0x): Saves, CTR — highest-intent buyer-adjacent signals
#   T1  (1.5x): Retention, PCR, Link Taps — strong intent/conversion signals
#   T2  (1.0x): Profile Visits, Comments, New Followers, Total Views — engagement/reach
#   T3  (0.75x): Shares — awareness amplifier, noisy audience quality
#
# Removed from scoring (internal-only metrics):
#   avg_reach_per_day, avg_watch_time
#
# Max denominator: (2 x 2.0) + (3 x 1.5) + (4 x 1.0) + (1 x 0.75) = 13.25
TIER_WEIGHTS = {
    "T1H": 2.0,  # saves, ctr — highest-intent buyer signals
    "T1":  1.5,  # retention_pct, pcr, link_taps
    "T2":  1.0,  # profile_visits, comments, new_followers, total_views
    "T3":  0.75, # shares — awareness amplifier, noisy quality
}

METRIC_TIERS = {
    "saves":          "T1H",  # Highest-intent buyer-adjacent behavior
    "ctr":            "T1H",  # Strongest BOFU conversion signal
    "retention_pct":  "T1",   # Hook quality + content depth
    "pcr":            "T1",   # Profile-to-follower conversion
    "link_taps":      "T1",   # BOFU action signal
    "profile_visits": "T2",   # MOFU consideration signal
    "comments":       "T2",   # Community signal — meaningful but not buyer-specific
    "new_followers":  "T2",   # Audience growth — quality-agnostic
    "total_views":    "T2",   # Reach — necessary but quality-agnostic
    "shares":         "T3",   # Awareness amplifier — noisy audience quality
}

STATUS_POINTS = {
    "EXCEEDING": {"T1H": 2.0, "T1": 1.5, "T2": 1.0, "T3": 0.75},
    "ON_TRACK":  {"T1H": 1.2, "T1": 0.9, "T2": 0.6, "T3": 0.45},
    "WATCH":     {"T1H": 0.4, "T1": 0.3, "T2": 0.2, "T3": 0.15},
}

def get_status(value, low, high):
    if value >= high:
        return "EXCEEDING"
    elif value >= low:
        return "ON_TRACK"
    else:
        return "WATCH"

def calculate_score(metrics, stage, prev_metrics=None):
    targets = KPI_TARGETS[stage]
    metric_statuses = {}
    total_weighted = 0.0
    
    for metric, tier in METRIC_TIERS.items():
        val = metrics.get(metric, 0)
        if val is None:
            val = 0
        low = targets[metric]["low"]
        high = targets[metric]["high"]
        status = get_status(val, low, high)
        weight = TIER_WEIGHTS[tier]
        points = STATUS_POINTS[status][tier]
        weighted = points
        total_weighted += weighted
        metric_statuses[metric] = {
            "value": val, "status": status, "tier": tier,
            "low": low, "high": high, "points": weighted
        }
    
    # Raw score: sum / 13.25 * 10
    # Denominator = (2 x 2.0) + (3 x 1.5) + (4 x 1.0) + (1 x 0.75) = 13.25
    raw = (total_weighted / 13.25) * 10
    
    # MoM trend credit
    trend_credit = 0.0
    if prev_metrics:
        improved = 0
        declined = 0
        for metric in METRIC_TIERS:
            curr = metrics.get(metric, 0) or 0
            prev = prev_metrics.get(metric, 0) or 0
            if curr > prev:
                improved += 1
            elif curr < prev:
                declined += 1
        net = improved - declined
        if net >= 6:
            trend_credit = 0.5
        elif net >= 3:
            trend_credit = 0.25
        elif net <= -6:
            trend_credit = -0.5
        elif net <= -3:
            trend_credit = -0.25
    
    raw_with_credit = raw + trend_credit
    compressed = 6.0 + (raw_with_credit * 0.4)
    compressed = round(compressed, 1)
    compressed = max(5.0, min(10.0, compressed))
    
    exceeding = sum(1 for m in metric_statuses.values() if m["status"] == "EXCEEDING")
    on_track  = sum(1 for m in metric_statuses.values() if m["status"] == "ON_TRACK")
    watch     = sum(1 for m in metric_statuses.values() if m["status"] == "WATCH")
    
    return {
        "score": compressed,
        "raw": round(raw, 2),
        "trend_credit": trend_credit,
        "exceeding": exceeding,
        "on_track": on_track,
        "watch": watch,
        "metrics": metric_statuses,
    }

def score_label(score):
    if score >= 9.5: return "Breakthrough Month"
    if score >= 9.0: return "Exceptional Month"
    if score >= 8.5: return "Strong Month"
    if score >= 8.0: return "Solid Month"
    if score >= 7.5: return "Building Month"
    if score >= 7.0: return "Progressing Month"
    if score >= 6.5: return "Mixed Month"
    if score >= 6.0: return "Foundation Month"
    if score >= 5.5: return "Early Stage"
    return "Baseline"

# ── CLIENT METADATA ───────────────────────────────────────────────────────
CLIENT_META = {
    "Launch Party":     {"stage": "Lift",  "slug": "shoplaunchparty",    "am": "Riley", "handle": "@shoplaunchparty",    "niche": "Indie Beauty Retail", "subniche": "Curated Indie Beauty & Clean Makeup", "start": "2024-08-06", "posts_per_week": 3},
    "Lane & Kate":      {"stage": "Lift",  "slug": "laneandkate",        "am": "Rachel","handle": "@laneandkate",        "niche": "Jewelry / Retail",    "subniche": "Custom & Fine Jewelry for Modern Heirlooms", "start": "2024-05-17", "posts_per_week": 2},
    "Skin by Brownlee": {"stage": "Rise",  "slug": "skinbybrownleeandco","am": "Riley", "handle": "@skinbybrownleeandco","niche": "Med Spas / Aesthetics","subniche": "Clinical Skincare for Acne & Hyperpigmentation", "start": "2025-10-07", "posts_per_week": 3},
    "MEAS Active":      {"stage": "Lift",  "slug": "measactive",         "am": "Riley", "handle": "@meas_active",        "niche": "Athletic Wear",       "subniche": "Fashion-Forward Performance Activewear", "start": "2025-05-22", "posts_per_week": 2},
    "Up & Running":     {"stage": "Spark", "slug": "upandrunningoh",     "am": "Rachel","handle": "@upandrunningoh",     "niche": "Running / Retail",    "subniche": "Performance Running Gear & Expert Shoe Fittings", "start": "2025-10-29", "posts_per_week": 2},
    "DEFINE Oakley":    {"stage": "Lift",  "slug": "defineoakley",       "am": "Emily", "handle": "@defineoakley",       "niche": "Fitness Studios",     "subniche": "High-Energy, Low-Impact Group Fitness", "start": "2024-02-05", "posts_per_week": 2},
    "Ombre Gallery":    {"stage": "Lift",  "slug": "ombregallery",       "am": "Emily", "handle": "@ombregallery",       "niche": "Jewelry / Retail",    "subniche": "Contemporary Craft & Artist-Made Jewelry", "start": "2024-07-11", "posts_per_week": 2},
}

# ── GOALS ─────────────────────────────────────────────────────────────────
CLIENT_GOALS = {
    "Launch Party": {
        "tofu": {"title": "Grow Digital Community & Drive Brand Discovery",       "funnel": "TOFU", "kpi": "total_views"},
        "mofu": {"title": "Build Trust Through Education & Deepen Community Connection", "funnel": "MOFU", "kpi": "saves"},
        "bofu": {"title": "Drive E-Commerce Sales & In-Store Traffic",            "funnel": "BOFU", "kpi": "link_taps"},
    },
    "Lane & Kate": {
        "tofu": {"title": "Boost Local Discoverability & Establish Engagement Ring Authority", "funnel": "TOFU", "kpi": "new_followers"},
        "mofu": {"title": "Increase Community Participation & Build Purchase Confidence",     "funnel": "MOFU", "kpi": "saves"},
        "bofu": {"title": "Drive Qualified Consultation Bookings",                            "funnel": "BOFU", "kpi": "link_taps"},
    },
    "Skin by Brownlee": {
        "tofu": {"title": "Establish Sylvia as the Perimenopause Skin Authority & Drive New Audience Discovery", "funnel": "TOFU", "kpi": "avg_reach_per_day"},
        "mofu": {"title": "Build Trust Through Education & Drive Skin Quiz Completions",                         "funnel": "MOFU", "kpi": "saves"},
        "bofu": {"title": "Drive Skin Quiz Completions & E-Commerce Product Sales",                              "funnel": "BOFU", "kpi": "link_taps"},
    },
    "MEAS Active": {
        "tofu": {"title": "Grow New Audience & Build Brand Identity Around the MEAS Mission", "funnel": "TOFU", "kpi": "new_followers"},
        "mofu": {"title": "Nurture Community & Convert Followers into Email Subscribers",     "funnel": "MOFU", "kpi": "saves"},
        "bofu": {"title": "Drive E-Commerce Shop Traffic & Email List Sign-Ups",              "funnel": "BOFU", "kpi": "link_taps"},
    },
    "Up & Running": {
        "tofu": {"title": "Build Regional Brand Presence & Grow Wellness Partnership Visibility", "funnel": "TOFU", "kpi": "avg_reach_per_day"},
        "mofu": {"title": "Build Trust Through Expertise & Improve Customer Retention",          "funnel": "MOFU", "kpi": "saves"},
        "bofu": {"title": "Drive E-Commerce Shop Traffic & In-Store Fit Bookings",               "funnel": "BOFU", "kpi": "link_taps"},
    },
    "DEFINE Oakley": {
        "tofu": {"title": "Drive New Audience Discovery & Brand Awareness",  "funnel": "TOFU", "kpi": "total_views"},
        "mofu": {"title": "Build Trust & Deepen Community Connection",       "funnel": "MOFU", "kpi": "saves"},
        "bofu": {"title": "Drive Class Bookings & New Member Sign-Ups",      "funnel": "BOFU", "kpi": "link_taps"},
    },
    "Ombre Gallery": {
        "tofu": {"title": "Expand Artist Advocacy Reach & Build a Worldwide Audience",       "funnel": "TOFU", "kpi": "total_views"},
        "mofu": {"title": "Build Trust Through Education & Drive Newsletter Sign-Ups",       "funnel": "MOFU", "kpi": "saves"},
        "bofu": {"title": "Drive Qualified E-Commerce Traffic & Newsletter Subscriber Growth","funnel": "BOFU", "kpi": "link_taps"},
    },
}

# ── ASSEMBLE FINAL DATA ───────────────────────────────────────────────────
from datetime import date

def months_since(start_str):
    start = date.fromisoformat(start_str)
    today = date(2026, 3, 31)
    return (today.year - start.year) * 12 + (today.month - start.month)

final_data = {}

for name, meta in CLIENT_META.items():
    mc = march_metricool[name]
    ig = feb_ig_insights.get(name, {})
    feb_mc = feb_metricool.get(name, {})
    
    # Build full metric set
    new_followers = ig.get("new_followers", 0)
    profile_visits = ig.get("profile_visits", 0)
    link_taps = ig.get("link_taps", 0)
    total_followers = ig.get("total_followers", 0)
    
    ctr = round((link_taps / profile_visits * 100), 1) if profile_visits > 0 else 0
    pcr = round((new_followers / profile_visits * 100), 1) if profile_visits > 0 else 0
    
    march_metrics = {
        "avg_reach_per_day": mc["avg_reach_per_day"],
        "new_followers":     new_followers,
        "shares":            mc["total_shares"],
        "total_views":       mc["total_views"],
        "profile_visits":    profile_visits,
        "avg_watch_time":    mc["avg_watch_time"],
        "retention_pct":     mc["avg_retention_pct"],
        "saves":             mc["total_saves"],
        "comments":          mc["total_comments"],
        "ctr":               ctr,
        "link_taps":         link_taps,
        "pcr":               pcr,
        "total_followers":   total_followers,
    }
    
    # February metrics for MoM
    feb_metrics = {
        "avg_reach_per_day": feb_mc.get("avg_reach_per_day", 0),
        "new_followers":     ig.get("new_followers", 0),  # same source
        "shares":            feb_mc.get("total_shares", 0),
        "total_views":       feb_mc.get("total_views", 0),
        "profile_visits":    ig.get("profile_visits", 0),
        "avg_watch_time":    0,
        "retention_pct":     0,
        "saves":             feb_mc.get("total_saves", 0),
        "comments":          feb_mc.get("total_comments", 0),
        "ctr":               ctr,
        "link_taps":         link_taps,
        "pcr":               pcr,
    }
    
    score_result = calculate_score(march_metrics, meta["stage"], feb_metrics)
    
    final_data[name] = {
        "meta": meta,
        "month_num": months_since(meta["start"]),
        "march_metrics": march_metrics,
        "feb_metrics": feb_metrics,
        "score": score_result,
        "score_label": score_label(score_result["score"]),
        "goals": CLIENT_GOALS[name],
    }

# ── PRINT SUMMARY ─────────────────────────────────────────────────────────
print("\n" + "="*70)
print("MARCH 2026 — FINAL METRICS & SCORES")
print("="*70)
print(f"{'Client':<20} {'Stage':<6} {'Score':>6} {'Label':<22} {'E':>3} {'OT':>3} {'W':>3}")
print("-"*70)
for name, d in final_data.items():
    s = d["score"]
    print(f"{name:<20} {d['meta']['stage']:<6} {s['score']:>6.1f} {d['score_label']:<22} {s['exceeding']:>3} {s['on_track']:>3} {s['watch']:>3}")

print("\nDETAILED METRICS:")
print(f"{'Client':<20} {'Views':>8} {'Shares':>7} {'Saves':>6} {'Comments':>9} {'Reach/D':>8} {'Watch':>6} {'Ret%':>5} {'CTR':>5} {'PCR':>5}")
print("-"*90)
for name, d in final_data.items():
    m = d["march_metrics"]
    print(f"{name:<20} {m['total_views']:>8,} {m['shares']:>7,} {m['saves']:>6,} {m['comments']:>9,} {m['avg_reach_per_day']:>8,.0f} {m['avg_watch_time']:>6.1f} {m['retention_pct']:>5.1f} {m['ctr']:>5.1f} {m['pcr']:>5.1f}")

# Save final data
with open("/home/ubuntu/march_final.json", "w") as f:
    json.dump(final_data, f, indent=2, default=str)
print(f"\n✅ Saved to /home/ubuntu/march_final.json")

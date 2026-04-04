"""
Scroll Media — Top Post Outlier Detection Engine
Version 1.2 — Unified Scoring Framework

Pulls all posts and reels for a given client from Metricool for the reporting month,
scores each post using the Scroll Media Composite Outlier Scoring Model, and returns
the top 2-4 outlier posts with their standout metrics and auto-generated insights.

Unified Scoring Philosophy (v1.2):
  Primary goal of organic social = get in front of the highest-quality audience
  (buyers), not the widest audience. Metric weights reflect buyer-intent hierarchy.

Usage:
    from outlier_engine import get_top_posts
    results = get_top_posts(blog_id=5321970, month=3, year=2026)
"""

import requests
import json
from datetime import datetime
from typing import Optional

# ── METRICOOL CONFIG ──────────────────────────────────────────────────────────
METRICOOL_TOKEN = "HNYJZNBHPSWJYCSSLWTMFDPTQAYIFEMWAJAYBVLVLVYSLBTXLYRLZDKHCJWVZIWL"
METRICOOL_USER_ID = 3745914
HEADERS = {"X-Mc-Auth": METRICOOL_TOKEN, "Accept": "application/json"}
BASE_URL = "https://app.metricool.com/api/v2"

# ── CLIENT BLOG IDS ───────────────────────────────────────────────────────────
CLIENT_BLOG_IDS = {
    "defineoakley": 5321970,
    "laneandkate": 5321978,
    "shoplaunchparty": 5321935,
    "measactive": 5321975,
    "ombregallery": 5321966,
    "skinbybrownleeandco": 5408849,
    "upandrunningoh": 5506230,
}

# ── METRIC WEIGHTS (must sum to 100) ─────────────────────────────────────────
# Unified Scoring Framework v1.2 — Buyer Intent Hierarchy:
#
#   SAVES (35%) — Highest-intent buyer-adjacent behavior. Viewer stopped and
#       bookmarked for future reference. Trains algorithm toward high-quality
#       buyer audiences. Closest organic signal to purchase intent.
#
#   RETENTION (25%) — Hook quality + content depth (Reels only). High retention
#       signals the algorithm to push content to higher-quality audiences.
#       Confirms the hook delivered and the pacing held attention.
#
#   REACH/VIEWS (20%) — Necessary but quality-agnostic. High views alone don't
#       guarantee the right audience. Important for algorithmic distribution.
#
#   COMMENTS (10%) — Community signal. Meaningful engagement that indicates
#       content resonated emotionally, but not a buyer-specific signal.
#
#   SHARES (10%) — Awareness amplifier but noisy. Shared content often reaches
#       non-buyer audiences (funny, relatable, "thought of you" content).
#       Lowest weight — reach without quality guarantee.
WEIGHTS = {
    "reach": 20,       # Views vs account avg views (TOFU — reach but quality-agnostic)
    "saves": 35,       # Saves vs account avg saves (highest-intent, buyer-adjacent signal)
    "retention": 25,   # Retention % vs account avg retention (Reels only — hook + depth quality)
    "comments": 10,    # Comments vs account avg comments (community signal, not buyer-specific)
    "shares": 10,      # Shares vs account avg shares (awareness amplifier, noisy audience quality)
}

# For non-Reel posts, redistribute retention weight to saves
WEIGHTS_NO_RETENTION = {
    "reach": 25,
    "saves": 50,
    "retention": 0,
    "comments": 15,
    "shares": 10,
}

# ── OUTLIER THRESHOLDS ────────────────────────────────────────────────────────
OUTLIER_SCORE_INCLUDE_4TH = 150   # Include 4th post if score >= this
OUTLIER_SCORE_EXCLUDE_3RD = 80    # Exclude 3rd post if score < this
STANDOUT_MULTIPLIER = 1.5         # Flag metric as standout if >= 1.5x account avg

# ── MINIMUM ABSOLUTE VALUE FLOORS ────────────────────────────────────────────
# A metric must meet BOTH the multiplier threshold AND the absolute minimum
# to be called out as a standout. This prevents flagging 1 save or 1 share
# as a meaningful signal (AMs saving posts, etc. can inflate low-volume metrics).
MIN_SAVES_FOR_STANDOUT = 4        # Saves must be >= 4 to be a standout metric
MIN_SHARES_FOR_STANDOUT = 4       # Shares must be >= 4 to be a standout metric
MIN_VIEWS_FOR_STANDOUT = 500      # Views must be >= 500 to be a standout metric
MIN_RETENTION_FOR_STANDOUT = 30.0 # Retention must be >= 30% to be a standout metric
MIN_COMMENTS_FOR_STANDOUT = 5     # Comments must be >= 5 to be a standout metric


def fetch_posts(blog_id: int, month: int, year: int) -> list:
    """Fetch all posts (non-Reel) for the given month from Metricool."""
    from_date = f"{year}-{month:02d}-01T00:00:00"
    import calendar
    last_day = calendar.monthrange(year, month)[1] - 1
    to_date = f"{year}-{month:02d}-{last_day:02d}T23:59:59"
    
    try:
        r = requests.get(
            f"{BASE_URL}/analytics/posts/instagram",
            headers=HEADERS,
            params={
                "userId": METRICOOL_USER_ID,
                "blogId": blog_id,
                "from": from_date,
                "to": to_date,
                "timezone": "America/New_York"
            },
            timeout=30
        )
        data = r.json()
        return data.get("data", [])
    except Exception as e:
        print(f"  Error fetching posts for blog {blog_id}: {e}")
        return []


def fetch_reels(blog_id: int, month: int, year: int) -> list:
    """Fetch all Reels for the given month from Metricool."""
    import calendar
    last_day = calendar.monthrange(year, month)[1] - 1
    from_date = f"{year}-{month:02d}-01T00:00:00"
    to_date = f"{year}-{month:02d}-{last_day:02d}T23:59:59"
    
    try:
        r = requests.get(
            f"{BASE_URL}/analytics/reels/instagram",
            headers=HEADERS,
            params={
                "userId": METRICOOL_USER_ID,
                "blogId": blog_id,
                "from": from_date,
                "to": to_date,
                "timezone": "America/New_York"
            },
            timeout=30
        )
        data = r.json()
        return data.get("data", [])
    except Exception as e:
        print(f"  Error fetching reels for blog {blog_id}: {e}")
        return []


def normalize_post(raw: dict, is_reel: bool) -> dict:
    """Normalize a raw Metricool post/reel into a standard format."""
    views = raw.get("views", 0) or raw.get("impressions", 0) or 0
    likes = raw.get("likes", 0) or 0
    comments = raw.get("comments", 0) or 0
    saves = raw.get("saved", 0) or raw.get("saves", 0) or raw.get("bookmarks", 0) or 0
    shares = raw.get("shares", 0) or 0
    
    # Calculate retention for Reels
    retention = None
    if is_reel:
        avg_watch = raw.get("averageWatchTime", 0) or 0
        duration = raw.get("durationSeconds", 0) or 0
        if duration > 0 and avg_watch > 0:
            retention = round((avg_watch / duration) * 100, 1)
    
    # Determine post type — two buckets only: Reel or Carousel / Image
    if is_reel:
        post_type = "Reel"
    else:
        post_type = "Carousel / Image"
    
    # Parse date — Metricool uses publishedAt.dateTime
    date_raw = raw.get("publishedAt") or raw.get("date") or ""
    if isinstance(date_raw, dict):
        date_raw = date_raw.get("dateTime", "") or date_raw.get("date", "") or date_raw.get("$date", "")
    try:
        if "T" in str(date_raw):
            dt = datetime.fromisoformat(str(date_raw).replace("Z", "+00:00"))
        else:
            dt = datetime.strptime(str(date_raw)[:10], "%Y-%m-%d")
        date_str = dt.strftime("%B %-d, %Y")
    except:
        date_str = str(date_raw)[:10]
    
    # Caption
    caption = raw.get("content", "") or raw.get("caption", "") or ""
    if isinstance(caption, dict):
        caption = ""
    caption = str(caption).strip()
    
    # URL
    url = raw.get("url", "") or raw.get("link", "") or ""
    if isinstance(url, dict):
        url = ""
    
    # Interactions = likes + comments + saves + shares
    interactions = likes + comments + saves + shares
    
    return {
        "type": post_type,
        "is_reel": is_reel,
        "date": date_str,
        "views": int(views),
        "likes": int(likes),
        "comments": int(comments),
        "saves": int(saves),
        "shares": int(shares),
        "interactions": int(interactions),
        "retention": retention,
        "caption": caption,
        "url": url,
        "raw": raw,
    }


def compute_outlier_score(post: dict, averages: dict) -> tuple[float, dict]:
    """
    Compute the Composite Outlier Score for a post.
    Returns (score, component_scores).
    A score of 100 = performing exactly at account average.
    
    Unified Scoring Framework v1.2:
    Saves (35%) > Retention (25%) > Reach (20%) > Comments (10%) > Shares (10%)
    """
    weights = WEIGHTS if post["is_reel"] else WEIGHTS_NO_RETENTION
    
    components = {}
    total = 0.0
    
    # Reach component
    avg_views = averages.get("views", 1) or 1
    reach_ratio = post["views"] / avg_views
    components["reach"] = round(reach_ratio * weights["reach"], 1)
    total += components["reach"]
    
    # Saves component
    avg_saves = averages.get("saves", 1) or 1
    save_ratio = post["saves"] / avg_saves
    components["saves"] = round(save_ratio * weights["saves"], 1)
    total += components["saves"]
    
    # Retention component (Reels only)
    if post["is_reel"] and post["retention"] is not None:
        avg_ret = averages.get("retention", 1) or 1
        ret_ratio = post["retention"] / avg_ret
        components["retention"] = round(ret_ratio * weights["retention"], 1)
        total += components["retention"]
    else:
        components["retention"] = 0
    
    # Comments component
    # Cap ratio at 5x to prevent division-by-zero inflation when avg_comments is 0
    avg_comments = averages.get("comments", 1) or 1
    comment_ratio = min(post["comments"] / avg_comments, 5.0)
    components["comments"] = round(comment_ratio * weights["comments"], 1)
    total += components["comments"]
    
    # Shares component
    avg_shares = averages.get("shares", 1) or 1
    share_ratio = post["shares"] / avg_shares
    components["shares"] = round(share_ratio * weights["shares"], 1)
    total += components["shares"]
    
    return round(total, 1), components


def get_standout_metrics(post: dict, averages: dict, components: dict) -> list[dict]:
    """
    Identify the 2-3 metrics that made this post stand out.
    Returns a list of {metric, value, avg, multiplier} dicts.
    Only flags metrics that clear BOTH the multiplier threshold AND the absolute floor.
    """
    standouts = []
    
    checks = [
        ("views",     "Total Views",   f"{post['views']:,}",     f"{int(averages.get('views',0)):,}"),
        ("saves",     "Saves",         str(post["saves"]),       str(int(averages.get("saves", 0)))),
        ("comments",  "Comments",      str(post["comments"]),    str(int(averages.get("comments", 0)))),
        ("shares",    "Shares",        str(post["shares"]),      str(int(averages.get("shares", 0)))),
    ]
    
    if post["is_reel"] and post["retention"] is not None:
        checks.append(
            ("retention", "Avg Retention", f"{post['retention']}%", f"{averages.get('retention', 0):.1f}%")
        )
    
    # Minimum absolute value floors
    abs_floors = {
        "saves":     MIN_SAVES_FOR_STANDOUT,
        "shares":    MIN_SHARES_FOR_STANDOUT,
        "views":     MIN_VIEWS_FOR_STANDOUT,
        "retention": MIN_RETENTION_FOR_STANDOUT,
        "comments":  MIN_COMMENTS_FOR_STANDOUT,
    }
    
    for key, display_name, val_str, avg_str in checks:
        avg = averages.get(key, 0) or 0
        actual = post.get(key, 0) or 0
        floor = abs_floors.get(key, 0)
        if avg > 0 and actual > 0 and actual >= floor:
            multiplier = actual / avg
            if multiplier >= STANDOUT_MULTIPLIER:
                standouts.append({
                    "metric": key,
                    "label": display_name,
                    "value": val_str,
                    "avg": avg_str,
                    "multiplier": round(multiplier, 1),
                })
    
    # Sort by multiplier descending, take top 3
    standouts.sort(key=lambda x: x["multiplier"], reverse=True)
    return standouts[:3]


def generate_why_it_worked(post: dict, standouts: list[dict], averages: dict) -> str:
    """Generate a data-backed 'Why It Worked' insight based on standout metrics."""
    if not standouts:
        # Composite fallback — data-informed but no single metric cleared the floor
        views_mult = round(post["views"] / max(averages.get("views", 1), 1), 1)
        saves_mult = round(post["saves"] / max(averages.get("saves", 1), 1), 1)
        shares_mult = round(post["shares"] / max(averages.get("shares", 1), 1), 1)
        
        parts = []
        if views_mult >= 1.2:
            parts.append(f"views at {views_mult}x average")
        if saves_mult >= 1.2:
            parts.append(f"saves at {saves_mult}x average")
        if shares_mult >= 1.2:
            parts.append(f"shares at {shares_mult}x average")
        
        if parts:
            metric_str = ", ".join(parts)
            return (
                f"Scored in the top posts this month on composite performance — "
                f"{metric_str}. No single metric broke out at scale, but the "
                f"combination of above-average signals across the board placed it here. "
                f"Consistent multi-metric performance is a strong indicator of content-market fit."
            )
        else:
            return (
                "Scored in the top posts this month on composite performance. "
                "Above-average results across multiple signals indicate this content "
                "resonated with the core audience — a reliable foundation to build on."
            )
    
    top = standouts[0]
    multiplier_str = f"{top['multiplier']}x"
    
    insight_map = {
        "views": (
            f"A reach outlier at {multiplier_str} the account's average views. "
            f"The hook successfully broke content out of the core audience and into the wider algorithm "
            f"— a strong signal to double down on this format and topic."
        ),
        "saves": (
            f"Powered by save density at {multiplier_str} the account average. "
            f"Saves this high signal that viewers found the content worth returning to "
            f"— the strongest indicator of consideration-stage intent and buyer-adjacent behavior. "
            f"This content is training the algorithm toward your highest-quality audience."
        ),
        "retention": (
            f"Anchored by exceptional retention at {multiplier_str} the account average. "
            f"Viewers watched a disproportionate amount of this Reel, signaling the hook delivered "
            f"on its promise and the pacing held attention throughout. "
            f"High retention trains the algorithm to push this content to higher-quality audiences."
        ),
        "comments": (
            f"Driven by community response at {multiplier_str} the account average in comments. "
            f"This level of engagement signals the content triggered an emotional reaction "
            f"— the audience didn't just watch, they showed up to participate. "
            f"High-emotion content like this builds the trust that converts followers into buyers."
        ),
        "shares": (
            f"Driven by share velocity at {multiplier_str} the account average. "
            f"High shares indicate the content tapped into a universal emotion or pain point "
            f"the audience wanted to pass along — a strong organic amplification signal "
            f"that extends reach beyond the existing follower base."
        ),
    }
    
    primary = insight_map.get(top["metric"], f"Strong {top['label']} performance at {multiplier_str} the account average.")
    
    # Add secondary metric context if available
    if len(standouts) >= 2:
        sec = standouts[1]
        secondary_map = {
            "views":     f"Reach also over-indexed at {sec['multiplier']}x average — confirming broad algorithmic distribution.",
            "saves":     f"Saves also over-indexed at {sec['multiplier']}x average — a dual signal of reach and buyer intent.",
            "retention": f"Retention also over-indexed at {sec['multiplier']}x average — confirming strong content quality throughout.",
            "comments":  f"Comments also over-indexed at {sec['multiplier']}x average — compounding the community engagement signal.",
            "shares":    f"Shares also over-indexed at {sec['multiplier']}x average — compounding the reach effect.",
        }
        secondary = secondary_map.get(sec["metric"], f"{sec['label']} also over-indexed at {sec['multiplier']}x.")
        return f"{primary} {secondary}"
    
    return primary


def get_top_posts(blog_id: int, month: int, year: int, client_name: str = "") -> dict:
    """
    Main function: pull all posts and reels for the month, score them,
    and return the top 2-4 outlier posts with insights.
    """
    print(f"\n{'='*60}")
    print(f"Analyzing: {client_name or blog_id} — {datetime(year, month, 1).strftime('%B %Y')}")
    print(f"{'='*60}")
    
    # 1. Fetch all content
    raw_posts = fetch_posts(blog_id, month, year)
    raw_reels = fetch_reels(blog_id, month, year)
    print(f"  Fetched: {len(raw_posts)} posts, {len(raw_reels)} reels")
    
    # 2. Normalize
    all_content = []
    for p in raw_posts:
        all_content.append(normalize_post(p, is_reel=False))
    for r in raw_reels:
        all_content.append(normalize_post(r, is_reel=True))
    
    if not all_content:
        print("  No content found for this period.")
        return {"posts": [], "averages": {}}
    
    # 3. Compute account averages
    total_posts = len(all_content)
    avg_views    = sum(p["views"]    for p in all_content) / total_posts
    avg_shares   = sum(p["shares"]   for p in all_content) / total_posts
    avg_saves    = sum(p["saves"]    for p in all_content) / total_posts
    avg_comments = sum(p["comments"] for p in all_content) / total_posts
    
    reels_with_retention = [p for p in all_content if p["is_reel"] and p["retention"] is not None]
    avg_retention = (
        sum(p["retention"] for p in reels_with_retention) / len(reels_with_retention)
        if reels_with_retention else 0
    )
    
    averages = {
        "views":     avg_views,
        "shares":    avg_shares,
        "saves":     avg_saves,
        "comments":  avg_comments,
        "retention": avg_retention,
    }
    
    print(f"  Account Averages: Views={avg_views:.0f}, Shares={avg_shares:.1f}, Saves={avg_saves:.1f}, Comments={avg_comments:.1f}, Retention={avg_retention:.1f}%")
    
    # 4. Score all posts
    for post in all_content:
        score, components = compute_outlier_score(post, averages)
        post["outlier_score"] = score
        post["score_components"] = components
    
    # 5. Sort by outlier score
    all_content.sort(key=lambda x: x["outlier_score"], reverse=True)
    
    # 6. Dynamic selection (2-4 posts)
    selected = []
    for i, post in enumerate(all_content):
        if i == 0:
            selected.append(post)
        elif i == 1:
            selected.append(post)
        elif i == 2:
            if post["outlier_score"] >= OUTLIER_SCORE_EXCLUDE_3RD:
                selected.append(post)
        elif i == 3:
            if post["outlier_score"] >= OUTLIER_SCORE_INCLUDE_4TH:
                selected.append(post)
        else:
            break
    
    # 7. Generate standout metrics and insights
    for post in selected:
        post["standout_metrics"] = get_standout_metrics(post, averages, post["score_components"])
        post["why_it_worked"]    = generate_why_it_worked(post, post["standout_metrics"], averages)
    
    # 8. Print results
    print(f"\n  Top {len(selected)} Posts Selected:")
    for i, post in enumerate(selected):
        print(f"\n  #{i+1} [{post['type']}] Score: {post['outlier_score']}")
        print(f"    Date: {post['date']}")
        print(f"    Views: {post['views']:,} ({post['views']/avg_views:.1f}x avg)")
        print(f"    Shares: {post['shares']} ({post['shares']/max(avg_shares,0.1):.1f}x avg)")
        print(f"    Saves: {post['saves']} ({post['saves']/max(avg_saves,0.1):.1f}x avg)")
        print(f"    Comments: {post['comments']} ({post['comments']/max(avg_comments,0.1):.1f}x avg)")
        if post["retention"]:
            print(f"    Retention: {post['retention']}%")
        print(f"    Standout: {[s['label'] for s in post['standout_metrics']]}")
        print(f"    Caption: {post['caption'][:80]}...")
    
    return {
        "posts": selected,
        "averages": averages,
        "total_posts_analyzed": total_posts,
    }


if __name__ == "__main__":
    # Test with DEFINE Oakley
    result = get_top_posts(
        blog_id=5321970,
        month=3,
        year=2026,
        client_name="DEFINE Oakley"
    )
    
    # Save results
    with open("/home/ubuntu/outlier_test_result.json", "w") as f:
        clean = {
            "posts": [{k: v for k, v in p.items() if k != "raw"} for p in result["posts"]],
            "averages": result["averages"],
            "total_posts_analyzed": result["total_posts_analyzed"],
        }
        json.dump(clean, f, indent=2)
    print("\n\nResults saved to /home/ubuntu/outlier_test_result.json")

#!/usr/bin/env python3
"""
build_month_report.py -- generate a month's v8.4/v8.5 report from the prior month's
shipped report plus a per-client config.

This is Workstream N, scoped to what the monthly cycle actually needs. `build_v8_report.py`
still points at the v8.3.5 template and uses pre-v8.4 token names, so it cannot fill the
storytelling template; the July 2026 set was built by hand. Hand-editing a 106KB file per
client per month is where transcription errors get into client-facing reports.

WHY IT TRANSFORMS THE PRIOR REPORT RATHER THAN FILLING THE TEMPLATE
The prior month's shipped report is a known-good artifact: correct gate code, correct
archive links, correct structure, already passed the 5-breakpoint audit. Cloning it and
changing only what should change preserves all of that, and any diff is reviewable as
"what actually moved this month". Filling a blank template regenerates every one of those
details and risks silently losing one. (Same reasoning as the retroactive-migration recipe
in process-v8.3.2.)

WHAT IT REWRITES
  - hero: score, label, MoM delta line, badge counts, engagement month, date range
  - the 12-metric Performance Breakdown, regenerated wholesale from the scorer (v1.5 adds
    Total Followers + Reposts, so a v1.3-era report has 10 cards and needs 12)
  - the 5 beat takeaways + Beat 2 prose + Beat 4 pattern line
  - the work strip (post count, format mix, themes, focus)
  - month/date labels throughout, and the <title>

WHAT IT DOES NOT TOUCH
  Top posts and the All Posts table -- those are injected separately by
  inject_report_data.py from Metricool, and overwriting them here would clobber that.

Usage:
  python3 build_month_report.py --config august/carlsdeli.json --verify
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STATUS_CLS = {"EXCEEDING": "exceed", "ON TRACK": "ontrack", "WATCH": "watch"}
STATUS_TXT = {"EXCEEDING": "Exceeding", "ON TRACK": "On Track", "WATCH": "Watch"}

# The breakdown renders as three funnel groups, not one flat grid. Band membership mirrors
# the FUNNEL row of the Master Performance Data Sheet, so the report and the sheet always
# agree about which metric belongs where. v1.5 adds Total Followers (TOFU) and Reposts
# (MOFU), which a v1.3-era report does not have cards for.
FUNNEL_BANDS = [
    ("tofu", [("total_followers", "Total Followers"), ("new_followers", "New Followers"),
              ("shares", "Shares"), ("total_views", "Total Views")]),
    ("mofu", [("profile_visits", "Profile Visits"), ("retention", "Retention"),
              ("saves", "Saves"), ("comments", "Comments"), ("reposts", "Reposts")]),
    ("bofu", [("ctr", "CTR"), ("link_taps", "Bio Link Taps"), ("pcr", "PCR")]),
]
PCT_METRICS = {"retention", "ctr", "pcr"}


def fmt(metric, v):
    if v is None:
        return "n/a"
    if metric in PCT_METRICS:
        return f"{v:g}%"
    return f"{v:,.0f}" if float(v) >= 1000 else f"{v:g}"


def bar_width(value, low, high):
    """Fill proportion for the metric bar: floor at the low end, full at the ceiling."""
    if value is None or low is None or high is None or high <= low:
        return 0
    return max(4, min(100, round((value - low) / (high - low) * 100)))


def metric_card(key, label, value, status, low, high, mom_pct, cur_month, prior_month, callout):
    cls = STATUS_CLS[status]
    tgt = f"{fmt(key, low)} &ndash; {fmt(key, high)}"
    if mom_pct is None:
        mom = f'<div class="mc-mom"><span class="mom flat">First month tracked</span></div>'
    else:
        arrow = "&#9650;" if mom_pct > 0 else ("&#9660;" if mom_pct < 0 else "&#9654;")
        direction = "up" if mom_pct > 0 else ("down" if mom_pct < 0 else "flat")
        mom = (f'<div class="mc-mom"><span class="mom {direction}">{arrow} '
               f'{abs(mom_pct):.0f}% vs {prior_month}</span></div>')
    co = f'\n          <p class="mc-callout">{callout}</p>' if callout else ""
    return (
        '        <div class="mc">\n'
        f'          <div class="mc-top"><span class="mc-name">{label}</span>'
        f'<span class="mc-badge {cls}">{STATUS_TXT[status]}</span></div>\n'
        f'          <div class="mc-nums"><div><span class="mc-lbl">{cur_month}</span>'
        f'<span class="mc-val {cls}">{fmt(key, value)}</span></div>'
        f'<div><span class="mc-lbl">Target Range</span><span class="mc-tgt">{tgt}</span></div></div>\n'
        f'{mom}\n'
        f'          <div class="bar-track"><div class="bar-fill {cls}" '
        f'data-w="{bar_width(value, low, high)}" style="width:0%"></div></div>{co}\n'
        '        </div>'
    )


def build_breakdown(cfg, scorer):
    """Regenerate every metric card from the scorer's own rows, grouped by funnel band, so
    the report can never disagree with the computed score."""
    kpis, prior = cfg["kpis"], cfg.get("prior_kpis") or {}
    res = scorer.score(kpis, cfg["stage"], prior or None)
    by_metric = {m: (tier, w, v, st, pts) for m, tier, w, v, st, pts in res["rows"]}
    targets = scorer.TARGETS[cfg["stage"]]
    callouts = cfg.get("callouts", {})
    grids = {}
    for band, metrics in FUNNEL_BANDS:
        cards = []
        for key, label in metrics:
            if key not in by_metric:
                continue
            _t, _w, value, status, _p = by_metric[key]
            if value is None:
                continue
            low, high = targets[key]
            pv = prior.get(key)
            mom = None if not pv else ((value - pv) / pv * 100)
            cards.append(metric_card(key, label, value, status, low, high, mom,
                                     cfg["month_label"], cfg["prior_month_label"],
                                     callouts.get(key)))
        grids[band] = "\n".join(cards)
    counts = {}
    for _m, _t, _w, _v, st, _p in res["rows"]:
        counts[st] = counts.get(st, 0) + 1
    return grids, counts, res


def grid_span(html, after_open):
    """Return (start, end) of the metrics-grid's INNER content, found by walking div depth.

    A non-greedy regex cannot do this: every metric card ends in </div> too, so
    `(.*?)</div></div>` matches the last CARD's closing tag rather than the grid's, and the
    generated replacement then contributes one closing div too many. That shipped a report
    with 3 unbalanced divs on the first pilot build -- caught by qa_report.py's div-balance
    check, which is exactly why that check exists.
    """
    depth, i, n = 1, after_open, len(html)
    while i < n and depth:
        nxt_open = html.find("<div", i)
        nxt_close = html.find("</div>", i)
        if nxt_close == -1:
            raise SystemExit("FATAL: unbalanced divs while scanning the metrics grid.")
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            i = nxt_open + 4
        else:
            depth -= 1
            if depth == 0:
                return after_open, nxt_close
            i = nxt_close + 6
    raise SystemExit("FATAL: could not find the metrics-grid close.")


def sub_once(html, pattern, repl, what, flags=0, wrap=None):
    """Replace exactly once, and fail loudly otherwise. A silently-missed replacement ships
    last month\'s number on a client-facing page, which is the failure mode that matters.

    `repl` is inserted literally (via a lambda), never as a regex template, so a narrative
    line containing a backslash or a \\g sequence cannot corrupt the output."""
    body = (wrap[0] + repl + wrap[1]) if wrap else repl
    new, n = re.subn(pattern, lambda _m: body, html, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"FATAL: expected 1 match for {what}, got {n}")
    return new


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--scorer", default=os.path.join(HERE, "score_report.py"))
    ap.add_argument("--out")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()

    cfg = json.load(open(a.config))

    import importlib.util
    spec = importlib.util.spec_from_file_location("score_report", a.scorer)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    if round(sum(w for _, w in scorer.METRICS.values()), 4) != 16.0:
        sys.exit("FATAL: scorer is not v1.5 (denominator != 16.0). Refusing to build.")

    src = cfg["prior_report"]
    html = open(src, encoding="utf-8").read()

    grids, counts, res = build_breakdown(cfg, scorer)
    final = cfg.get("final_score_override", res["final"])

    # --- the three funnel grids, wholesale ---
    # Match each band's <div class="metrics-grid"> ... </div> by walking from the band's
    # funnel-header. Replacing the whole grid is what lets v1.5 add cards a v1.3-era report
    # never had, rather than trying to patch individual values in place.
    for band, _metrics in FUNNEL_BANDS:
        m = re.search(rf'<div class="funnel-header {band}".*?<div class="metrics-grid">',
                      html, re.S)
        if not m:
            sys.exit(f"FATAL: could not locate the {band.upper()} metrics-grid.")
        inner_start, inner_end = grid_span(html, m.end())
        html = html[:inner_start] + "\n" + grids[band] + "\n      " + html[inner_end:]

    # --- hero ---
    html = sub_once(html, r'<div class="ph-bignum">[\d.]+<span class="unit">/10</span></div>',
                    f'<div class="ph-bignum">{final}<span class="unit">/10</span></div>', "hero score")
    html = sub_once(html, r'<p class="ph-title">[^<]*</p>',
                    f'<p class="ph-title">{cfg["score_label"]}</p>', "score label")
    html = sub_once(html, r'<span class="ph-delta[^"]*">[^<]*</span>',
                    f'<span class="ph-delta {cfg["delta_class"]}">{cfg["delta_text"]}</span>', "MoM delta")
    badges = (f'<span class="ph-badge exceed"><span class="bd"></span>{counts.get("EXCEEDING",0)} Exceeding</span>\n'
              f'<span class="ph-badge ontrack"><span class="bd"></span>{counts.get("ON TRACK",0)} On Track</span>\n'
              f'<span class="ph-badge watch"><span class="bd"></span>{counts.get("WATCH",0)} Watch</span>')
    html = sub_once(html, r'<span class="ph-badge exceed">.*?Watch</span>', badges, "hero badges", re.S)

    # --- labels ---
    html = sub_once(html, r'<title>[^<]*</title>',
                    f'<title>{cfg["client_name_html"]} &ndash; {cfg["month_label"]} {cfg["year"]} | Scroll Media</title>',
                    "title")
    html = sub_once(html, r'(<div class="hero-eyebrow"><span class="dot"></span>)[^<]*(</div>)',
                    f'<div class="hero-eyebrow"><span class="dot"></span>{cfg["month_label"]} {cfg["year"]} Performance Report</div>',
                    "hero eyebrow")
    html = sub_once(html, r'<div class="hero-stage-badge"><span class="stage-icon"></span>[^<]*</div>',
                    f'<div class="hero-stage-badge"><span class="stage-icon"></span>{cfg["stage"]} Stage &middot; Month {cfg["month_num"]}</div>',
                    "stage badge")
    html = sub_once(html, r'<span>[A-Z][a-z]+ \d+&ndash;\d+, \d{4}</span>',
                    f'<span>{cfg["date_range"]}</span>', "date range")
    # og/twitter description carry the score; a stale one shows in the link preview.
    html = re.sub(r'(content="[^"]*?)\b\d\.\d/10\b', lambda mm: mm.group(1) + f"{final}/10", html)
    html = re.sub(r'(content="[^"]*?Monthly score [\d.]+/10\. )[^"]*?(")',
                  lambda mm: mm.group(1) + cfg["score_label"] + "." + mm.group(2), html)

    # --- paired-hero outcome panel ---
    # The client-specific business-outcome metric. It is NOT one of the 12 scored metrics, so
    # nothing else in this script would touch it -- the first pilot build left July's 262 bio
    # link taps sitting next to August's score, which is the single most visible wrong number
    # a report could carry.
    if cfg.get("outcome_value"):
        html, n = re.subn(
            r'(<div class="ph-panel outcome">.*?<div class="ph-bignum">)[^<]*(</div>)',
            lambda m: m.group(1) + str(cfg["outcome_value"]) + m.group(2),
            html, count=1, flags=re.S)
        if n != 1:
            sys.exit(f"FATAL: expected 1 match for outcome value, got {n}")
    if cfg.get("outcome_sub"):
        html = sub_once(html, r'<p class="ph-outcome-sub">.*?</p>', cfg["outcome_sub"],
                        "outcome sub", re.S,
                        wrap=('<p class="ph-outcome-sub">', "</p>"))

    # --- Beat 1 hero summary ---
    if cfg.get("beat1_summary"):
        html = sub_once(html, r'(<p class="hero-summary"[^>]*>)<strong>.*?</strong>(</p>)',
                        cfg["beat1_summary"], "beat1 summary", re.S,
                        wrap=('<p class="hero-summary"><strong>', "</strong></p>"))

    # --- Beat 2 work strip ---
    if cfg.get("work_chips"):
        chips = "\n".join(f'      <span class="work-chip">{c}</span>' for c in cfg["work_chips"])
        html = sub_once(html, r'<div class="work-strip">.*?</div>\s*\n', chips,
                        "work strip", re.S,
                        wrap=('<div class="work-strip">\n', "\n    </div>\n"))
    # There are TWO .beat-prose elements (Beat 2 and Beat 4). Replacing "the first one" left
    # Beat 4 describing JULY's top post -- a stale narrative claim about content that was not
    # even published this month, which preflight's corroboration check caught. Scope each
    # replacement to its own beat section.
    for bi in (2, 4):
        key = f"beat{bi}_prose"
        if not cfg.get(key):
            continue
        anchor = re.search(rf'id="beat{bi}"', html)
        if not anchor:
            sys.exit(f"FATAL: no beat{bi} section found")
        seg = html[anchor.end():]
        m = re.search(r'<p class="beat-prose">.*?</p>', seg, re.S)
        if not m:
            sys.exit(f"FATAL: no .beat-prose inside beat{bi}")
        lo = anchor.end() + m.start(); hi = anchor.end() + m.end()
        html = html[:lo] + f'<p class="beat-prose">{cfg[key]}</p>' + html[hi:]

    # --- Beat 3 result stat tiles ---
    # Four of the 12 metrics, chosen to match the month's story. Separate markup from the
    # metric cards, so regenerating the breakdown does not touch them.
    if cfg.get("bstats"):
        tiles = []
        for t in cfg["bstats"]:
            cls = STATUS_CLS[t["status"]]
            tiles.append(f'<div class="bstat"><div class="bstat-val {cls}">{t["value"]}</div>'
                         f'<div class="bstat-lbl">{t["label"]}</div>'
                         f'<span class="bstat-tag {cls}">{STATUS_TXT[t["status"]]}</span></div>')
        html = sub_once(html, r'<div class="bstats">.*?</div>\s*(?=<p class="sub-head")',
                        "\n      ".join(tiles), "beat3 stat tiles", re.S,
                        wrap=('<div class="bstats">\n      ', "\n    </div>\n    "))

    # --- the "See all N posts" proof label ---
    if cfg.get("post_count"):
        html = re.sub(r'(<span>See all )\d+( posts and their numbers</span>)',
                      lambda m: m.group(1) + str(cfg["post_count"]) + m.group(2), html, count=1)

    # --- followers banner ---
    if cfg.get("followers_banner"):
        fb = cfg["followers_banner"]
        html, n = re.subn(r'(<div class="fb-count">)[^<]*(</div>)',
                          lambda m: m.group(1) + fb["count"] + m.group(2), html, count=1)
        if n != 1:
            sys.exit("FATAL: followers-banner count not found")
        html = sub_once(html, r'<div class="fb-mom">.*?</div>', fb["mom"], "followers MoM",
                        re.S, wrap=('<div class="fb-mom">', "</div>"))

    # --- Content-to-Business funnel walk ---
    # Four absolute volumes plus their analogy badges. The badges are COPY, not arithmetic --
    # "the Taft Theatre filled nearly twice over" only works at certain magnitudes -- so they
    # are authored per month rather than computed, and reviewed with Chase like the rest of
    # the modeled layer (process-v8.5 gate).
    if cfg.get("c2b_steps"):
        steps = []
        for st in cfg["c2b_steps"]:
            badge = (f'<span class="c2b-step-badge">{st["badge"]}</span>' if st.get("badge") else "")
            steps.append(f'<div class="c2b-step{" hi" if st.get("hi") else ""}">'
                         f'<span class="c2b-step-num">{st["num"]}</span>'
                         f'<div class="c2b-step-main"><span class="c2b-step-txt">{st["text"]}</span>'
                         f'{badge}</div></div>')
        m = re.search(r'<div class="c2b-steps">', html)
        if not m:
            sys.exit("FATAL: could not locate the c2b funnel steps.")
        # Depth-scan again: each step is itself nested divs, so a non-greedy regex stops at
        # the FIRST step and silently leaves the rest of last month's funnel in place.
        inner_start, inner_end = grid_span(html, m.end())
        html = (html[:inner_start] + "\n        " + "\n        ".join(steps)
                + "\n      " + html[inner_end:])

    # --- logos ---
    # The hero and footer logos pointed at expiring files.manuscdn.com session-file URLs.
    # All three return 403, across 44 shipped report files, so every live client report has
    # been rendering a broken logo in its hero. The repo already ships the real assets.
    # Hero sits on dark navy -> white mark; footer is #fff -> navy mark.
    if cfg.get("fix_logos", True):
        html = re.sub(r'(<img src=")https://files\.manuscdn\.com[^"]*("[^>]*class="hero-logo")',
                      lambda m: m.group(1) + "/assets/scroll-logo-white.png" + m.group(2), html)
        html = re.sub(r'(<img src=")https://files\.manuscdn\.com[^"]*("[^>]*class="footer-logo")',
                      lambda m: m.group(1) + "/assets/scroll-logo-navy.png" + m.group(2), html)
        # The favicon points at the same dead CDN.
        html = re.sub(r'(<link rel="icon"[^>]*href=")https://files\.manuscdn\.com[^"]*(")',
                      lambda m: m.group(1) + "/assets/favicon.svg" + m.group(2), html)
        html = html.replace('<link rel="icon" type="image/png" href="/assets/favicon.svg"',
                            '<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"')

    # --- mobile body-text floor: FLAGGED, NOT FIXED ---
    # CLAUDE.md Locked Principle 3.12 bans body text under 14px on mobile, and Procedural
    # Gate #6 says every sub-14px body selector must join the 480px floor list before deploy.
    # Only .mc-callout ever did (v8.3.3). A live audit at 375px found ~15 more selectors
    # under 14px on both the August build AND July's shipped report -- .work-chip, .gt-narr,
    # .why-text, .qyear-intro, .mscore-lead, .tw-item-body, .beat-cta-rationale and others.
    #
    # Deliberately NOT auto-fixed here. Deciding which of those are body copy and which are
    # chrome (.funnel-lbl, .sec-label and the caption spans are arguably labels/quotes) is a
    # design decision affecting every shipped report, and a partial fix ships inconsistent
    # typography inside a single strip. A first attempt also proved the naive fix does not
    # even work: injecting the floor next to the .mc-callout rule puts it BEFORE the base
    # .work-chip rule in source order, so equal specificity means the base rule wins. Any
    # real fix must append at the END of the stylesheet.
    #
    # Tracked for Chase as a bulk decision alongside the broken-logo fix.

    # --- narrative ---
    for i in (1, 2, 3, 4, 5):
        key = f"beat{i}_takeaway"
        if cfg.get(key):
            if f'id="beat{i}-t"' in html:
                html = sub_once(
                    html,
                    rf'(<h2 class="beat-takeaway"[^>]*id="beat{i}-t"[^>]*>).*?(</h2>)',
                    cfg[key], f"beat{i} takeaway", re.S,
                    wrap=(f'<h2 class="beat-takeaway" id="beat{i}-t">', "</h2>"))

    # Ignore comments: the template's own CSS comment mentions {{TOKEN}} while explaining
    # the overflow safety net, and flagging it every build trains people to ignore the warning.
    scan = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    scan = re.sub(r"/\*.*?\*/", " ", scan, flags=re.S)
    leftover = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", scan)))
    out = a.out or cfg["out"]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)

    print(f"wrote {out}")
    print(f"  score {final}  ({cfg['score_label']})  "
          f"{counts.get('EXCEEDING',0)}E/{counts.get('ON TRACK',0)}OT/{counts.get('WATCH',0)}W")
    print(f"  computed raw {res['raw']:.2f}, MoM {res['credit']:+.2f} "
          f"({res['improving']}up/{res['declining']}dn), scorer final {res['final']}")
    if final != res["final"]:
        print(f"  NOTE: shipping {final}, not the scorer's {res['final']} "
              f"-- {cfg.get('override_reason','NO REASON GIVEN')}")
    if leftover:
        print(f"  WARNING: unfilled tokens: {leftover}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

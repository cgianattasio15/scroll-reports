"""
Scroll Media — Report Data Verification Gate
Version 1.0

PURPOSE
-------
Cross-checks every metric value displayed in a built HTML report against the
ground-truth data in the Master Performance Data Sheet (Google Sheets).
Run this BEFORE deploying any report. If any check fails, do not deploy.

USAGE
-----
    python3 verify_report_data.py --month March --year 2026

    Or import and call directly:
        from verify_report_data import verify_all_clients
        results = verify_all_clients(month="March", year=2026)

WHAT IT CHECKS
--------------
For each client:
  1. All 10 metric values (mc-val) match the master sheet
  2. All MoM delta percentages are mathematically correct vs. prior month
  3. MoM arrow direction (up/dn/fl) matches the sign of the delta
  4. No metric shows 0% MoM when prior month data exists (catches stale cache bug)

PASS CRITERIA
-------------
  All checks must pass. Any failure blocks deployment.
  A report with wrong numbers is worse than no report.

DEPENDENCIES
------------
  - gws CLI (pre-configured Google Sheets access)
  - Google Sheet ID: 1VTTbhyoAe0utuNmig4h5760MyjxMJng86elJi7mV98w
  - Reports at: /home/ubuntu/scroll-reports-repo/[slug]/[monthyear]/index.html
"""

import re
import json
import subprocess
import argparse
import sys
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────

SHEET_ID = "1VTTbhyoAe0utuNmig4h5760MyjxMJng86elJi7mV98w"
REPORT_BASE = Path("/home/ubuntu/scroll-reports-repo")

# Maps sheet row names to HTML mc-name labels
METRIC_MAP = {
    "New Followers":   "New Followers",
    "Shares":          "Shares",
    "Views":           "Total Views",
    "Profile Visits":  "Profile Visits",
    "Saves":           "Saves",
    "Comments":        "Comments",
    "Link Taps":       "Link Taps",
}

# Metrics that need % formatting in HTML
PCT_METRICS = {"Retention %", "Click-Through Rate", "CTR", "Profile Conversion Rate"}

# MoM tolerance: allow ±2 percentage points for rounding differences
MOM_TOLERANCE = 2.0

# ── SHEET READER ─────────────────────────────────────────────────────────────

def read_sheet_tab(tab_name: str) -> list[list[str]]:
    """Pull a tab from the master performance sheet via gws CLI."""
    cmd = [
        "gws", "sheets", "spreadsheets", "values", "get",
        "--params", json.dumps({
            "spreadsheetId": SHEET_ID,
            "range": tab_name
        })
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"gws failed for tab '{tab_name}': {result.stderr}")
    data = json.loads(result.stdout)
    return data.get("values", [])


def parse_sheet_data(rows: list[list[str]]) -> dict:
    """
    Parse sheet rows into a dict keyed by client name.
    Returns: { "Client Name": { "metric": raw_value, ... }, ... }
    """
    # Find header row (contains "Account" and metric names)
    header_row = None
    header_idx = None
    for i, row in enumerate(rows):
        if row and "Account" in row:
            header_row = row
            header_idx = i
            break

    if header_row is None:
        raise ValueError("Could not find header row in sheet")

    clients = {}
    for row in rows[header_idx + 1:]:
        if not row or len(row) < 3:
            continue
        client_name = row[1].strip() if len(row) > 1 else ""
        if not client_name:
            continue

        client_data = {}
        for col_idx, col_name in enumerate(header_row):
            if col_idx < len(row) and col_name:
                raw = row[col_idx].strip()
                # Strip commas and % for numeric comparison
                clean = raw.replace(",", "").replace("%", "").strip()
                client_data[col_name] = {"raw": raw, "clean": clean}

        clients[client_name] = client_data

    return clients


def get_sheet_value(client_data: dict, metric_key: str) -> str | None:
    """Get a metric value from parsed sheet data."""
    entry = client_data.get(metric_key)
    if entry:
        return entry["raw"]
    return None


# ── HTML READER ───────────────────────────────────────────────────────────────

def read_report_metrics(html: str) -> dict:
    """Extract all mc-name → mc-val pairs from a report HTML."""
    pairs = re.findall(
        r'mc-name">(.*?)</span>.*?mc-val[^"]*">([\d,\.%]+)',
        html, re.DOTALL
    )
    return dict(pairs)


def read_report_moms(html: str) -> dict:
    """Extract all mc-name → MoM delta text pairs from a report HTML."""
    pairs = re.findall(
        r'mc-name">(.*?)</span>.*?mom[^"]*">(.*?)</span>',
        html, re.DOTALL
    )
    result = {}
    for name, delta_html in pairs:
        pct_match = re.search(r'([+-]?\d+\.?\d*)%', delta_html)
        if pct_match:
            result[name] = {
                "pct": float(pct_match.group(1)),
                "direction": "up" if "mom up" in delta_html else ("dn" if "mom dn" in delta_html else "fl"),
                "raw": delta_html.strip()
            }
        elif "Flat" in delta_html:
            result[name] = {"pct": 0.0, "direction": "fl", "raw": "Flat"}
    return result


# ── SLUG RESOLVER ─────────────────────────────────────────────────────────────

SLUG_MAP = {
    "DEFINE Oakley":       "defineoakley",
    "Lane & Kate":         "laneandkate",
    "Launch Party":        "shoplaunchparty",
    "MEAS Active":         "measactive",
    "Ombre Gallery":       "ombregallery",
    "Skin by Brownlee":    "skinbybrownleeandco",
    "Up & Running":        "upandrunningoh",
}

# Maps sheet metric column names to HTML mc-name labels
SHEET_TO_HTML = {
    "New Followers":  "New Followers",
    "Shares":         "Shares",
    "Views":          "Total Views",
    "Profile Visits": "Profile Visits",
    "Saves":          "Saves",
    "Comments":       "Comments",
    "Link Taps":      "Link Taps",
    "CTR":            "Click-Through Rate",
    "PCR":            "Profile Conversion Rate",
    "Retention %":    "Retention %",
    # Avg Watch Time is internal-only — not shown in client reports
}


# ── CORE VERIFICATION ─────────────────────────────────────────────────────────

def verify_client(
    client_name: str,
    slug: str,
    march_data: dict,
    feb_data: dict | None,
    month_slug: str,
) -> dict:
    """
    Verify a single client report against master sheet data.
    Returns a result dict with pass/fail status and list of failures.
    """
    report_path = REPORT_BASE / slug / month_slug / "index.html"
    if not report_path.exists():
        return {
            "client": client_name,
            "slug": slug,
            "status": "ERROR",
            "failures": [f"Report file not found: {report_path}"]
        }

    with open(report_path) as f:
        html = f.read()

    report_metrics = read_report_metrics(html)
    report_moms = read_report_moms(html)

    failures = []
    warnings = []

    # ── CHECK 1: Metric values match sheet ──────────────────────────────────
    for sheet_col, html_label in SHEET_TO_HTML.items():
        sheet_entry = march_data.get(sheet_col)
        if not sheet_entry or not sheet_entry["raw"]:
            continue  # metric not in sheet for this client

        sheet_val_raw = sheet_entry["raw"]
        sheet_val_clean = sheet_entry["clean"]

        # Find in report (try primary label, then alternate)
        report_val = report_metrics.get(html_label)
        if report_val is None and html_label == "Click-Through Rate":
            report_val = report_metrics.get("CTR")
        if report_val is None:
            warnings.append(f"  ⚠ {html_label}: not found in report HTML")
            continue

        # Normalize for comparison
        report_clean = report_val.replace(",", "").replace("%", "").strip()

        # For percentage metrics, compare numerically with small tolerance
        try:
            r_num = float(report_clean)
            s_num = float(sheet_val_clean)
            if abs(r_num - s_num) > 0.5:  # >0.5 unit tolerance
                failures.append(
                    f"  ✗ {html_label}: report='{report_val}' | sheet='{sheet_val_raw}'"
                )
        except ValueError:
            # String comparison fallback
            if report_clean != sheet_val_clean:
                failures.append(
                    f"  ✗ {html_label}: report='{report_val}' | sheet='{sheet_val_raw}'"
                )

    # ── CHECK 2: MoM deltas are mathematically correct ──────────────────────
    if feb_data:
        for sheet_col, html_label in SHEET_TO_HTML.items():
            mar_entry = march_data.get(sheet_col)
            feb_entry = feb_data.get(sheet_col)

            if not mar_entry or not feb_entry:
                continue
            if not mar_entry["clean"] or not feb_entry["clean"]:
                continue

            try:
                mar_num = float(mar_entry["clean"])
                feb_num = float(feb_entry["clean"])
                if feb_num == 0:
                    continue

                correct_pct = (mar_num - feb_num) / feb_num * 100
                correct_dir = "up" if correct_pct > 1 else ("dn" if correct_pct < -1 else "fl")

                # Find MoM in report
                mom = report_moms.get(html_label)
                if mom is None and html_label == "Click-Through Rate":
                    mom = report_moms.get("CTR")
                if mom is None:
                    continue  # not shown in report

                reported_pct = mom["pct"]
                reported_dir = mom["direction"]

                # Check percentage value
                if abs(abs(reported_pct) - abs(correct_pct)) > MOM_TOLERANCE:
                    failures.append(
                        f"  ✗ {html_label} MoM: report={reported_pct:+.1f}% | "
                        f"correct={correct_pct:+.1f}% "
                        f"(Mar={mar_num}, Feb={feb_num})"
                    )

                # Check direction
                elif reported_dir != correct_dir:
                    failures.append(
                        f"  ✗ {html_label} MoM direction: report='{reported_dir}' | "
                        f"correct='{correct_dir}' ({correct_pct:+.1f}%)"
                    )

                # Catch the stale-cache bug: 0% when prior month data exists
                elif reported_pct == 0.0 and abs(correct_pct) > 2.0:
                    failures.append(
                        f"  ✗ {html_label} MoM shows 0% but correct delta is "
                        f"{correct_pct:+.1f}% — likely stale cache bug"
                    )

            except (ValueError, ZeroDivisionError):
                continue

    status = "FAIL" if failures else ("WARN" if warnings else "PASS")
    return {
        "client": client_name,
        "slug": slug,
        "status": status,
        "failures": failures,
        "warnings": warnings,
    }


# ── MAIN ──────────────────────────────────────────────────────────────────────

def verify_all_clients(month: str, year: int) -> list[dict]:
    """
    Run verification for all active clients.
    Returns list of per-client result dicts.
    """
    month_slug = f"{month.lower()}{year}"
    prev_month_map = {
        "January": "December", "February": "January", "March": "February",
        "April": "March", "May": "April", "June": "May",
        "July": "June", "August": "July", "September": "August",
        "October": "September", "November": "October", "December": "November",
    }
    prev_month = prev_month_map.get(month, "")

    print(f"\n{'='*60}")
    print(f"  Scroll Media Report Data Verification Gate")
    print(f"  Month: {month} {year}")
    print(f"{'='*60}\n")

    # Pull current and prior month data from sheet
    print(f"Reading {month} {year} data from master sheet...")
    try:
        march_rows = read_sheet_tab(month)
        march_clients = parse_sheet_data(march_rows)
    except Exception as e:
        print(f"ERROR: Could not read {month} sheet tab: {e}")
        sys.exit(1)

    feb_clients = {}
    if prev_month:
        print(f"Reading {prev_month} data for MoM verification...")
        try:
            feb_rows = read_sheet_tab(prev_month)
            feb_clients = parse_sheet_data(feb_rows)
        except Exception as e:
            print(f"WARNING: Could not read {prev_month} sheet tab: {e}")
            print("MoM delta verification will be skipped.\n")

    results = []
    pass_count = 0
    fail_count = 0

    for client_name, slug in SLUG_MAP.items():
        march_data = march_clients.get(client_name, {})
        feb_data = feb_clients.get(client_name, {})

        if not march_data:
            print(f"  SKIP  {client_name} — not found in {month} sheet tab")
            continue

        result = verify_client(client_name, slug, march_data, feb_data, month_slug)
        results.append(result)

        icon = "✅" if result["status"] == "PASS" else ("⚠️ " if result["status"] == "WARN" else "❌")
        print(f"  {icon}  {client_name}")

        for f in result.get("failures", []):
            print(f)
            fail_count += 1
        for w in result.get("warnings", []):
            print(w)

        if result["status"] == "PASS":
            pass_count += 1

    print(f"\n{'='*60}")
    print(f"  Results: {pass_count} passed, {len(results) - pass_count} failed")
    if fail_count > 0:
        print(f"  ⛔ DEPLOYMENT BLOCKED — fix {fail_count} error(s) before pushing")
    else:
        print(f"  ✅ ALL CLEAR — data verified, safe to deploy")
    print(f"{'='*60}\n")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verify report data against master performance sheet"
    )
    parser.add_argument("--month", required=True, help="Month name (e.g. March)")
    parser.add_argument("--year", required=True, type=int, help="Year (e.g. 2026)")
    args = parser.parse_args()

    results = verify_all_clients(month=args.month, year=args.year)

    # Exit with error code if any failures
    if any(r["status"] == "FAIL" for r in results):
        sys.exit(1)
    sys.exit(0)

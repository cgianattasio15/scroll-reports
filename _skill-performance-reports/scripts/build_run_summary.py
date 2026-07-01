"""Build a human-readable SUMMARY.md from the per-client summary JSON files
produced by inject_report_data.py. Used by the Monthly Metricool Pull workflow
to make the run artifact scannable (post counts + top 3 posts per client).

Usage:  python3 build_run_summary.py <summaries_dir>
"""
import sys, os, json, glob

d = sys.argv[1] if len(sys.argv) > 1 else "summaries"
files = sorted(glob.glob(os.path.join(d, "*.json")))
lines = ["# Metricool pull summary", ""]
if not files:
    lines.append("_No client summaries were produced (all pulls skipped or failed)._")
for f in files:
    try:
        j = json.load(open(f, encoding="utf-8"))
    except Exception as e:
        lines.append(f"## {os.path.basename(f)}\n- could not read: {e}\n")
        continue
    lines.append(f"## {j.get('client','?')} — {j.get('month','?')}/{j.get('year','?')}")
    lines.append(f"- Posts: {j.get('all_posts_count',0)} | outliers flagged: {j.get('outliers_flagged',0)}")
    for i, t in enumerate(j.get("top_posts", []), 1):
        lines.append(f"- Top {i} ({t.get('type','?')}): {t.get('standout','')} — "
                     f"{t.get('caption_80','')} — {t.get('url','')}")
    lines.append("")
out = "\n".join(lines)
with open(os.path.join(d, "SUMMARY.md"), "w", encoding="utf-8") as fh:
    fh.write(out)
print(out)

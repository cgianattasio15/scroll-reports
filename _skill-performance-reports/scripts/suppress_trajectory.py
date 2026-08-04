#!/usr/bin/env python3
"""suppress_trajectory.py -- apply the process-v8.5 §6 value-trajectory inclusion gate to a
July 2026 report that has no documented client CLV: remove the dollar 12-month value
trajectory (Panel 2, the modeled SVG + per-visit/per-customer dollar method + disclaimer),
keep Panel 1 (the funnel walk in counts/taps) and everything else in Beat 3, relabel the
collapsible + section sub away from dollar framing, and (for active clients) leave a one-line
no-dollar forward note. Anchored/hard-fail. Rendered content otherwise unchanged.

Usage: suppress_trajectory.py <client> <window_word:'month'|'final window'> <note:1|0>
"""
import os, re, sys

REPO = "/Users/chase.gianattasio/Desktop/scroll-reports"

NOTE = ('<p style="font-size:.8125rem;color:var(--muted);line-height:1.6;font-style:italic;'
        'margin-top:1rem">Once you share your real numbers (average sale, repeat rate, and typical '
        'customer lifetime value), we&rsquo;ll add a value view here built on your actual economics.</p>')


def suppress(client, window_word, add_note):
    p = f"{REPO}/{client}/july2026/index.html"
    h = open(p, encoding="utf-8").read()

    # 1. relabel the collapsible summary (drop "12-month value trajectory")
    a = "<span>See the 12-month value trajectory</span>"
    if h.count(a) != 1:
        sys.exit(f"{client}: proof-summary anchor x{h.count(a)}")
    h = h.replace(a, f"<span>See how this {window_word}&rsquo;s attention maps to business signal</span>", 1)

    # 2. drop the dollar framing from the section sub (shared tail across all five)
    b = ", from what we can see on-platform to a conservative estimate of what it&rsquo;s worth."
    if h.count(b) != 1:
        sys.exit(f"{client}: sec-sub anchor x{h.count(b)}")
    h = h.replace(b, ", from the widest reach down to the highest-intent taps.", 1)

    # 3. remove Panel 2 (c2b-estimate + optional PANEL 2 comment), keep </section>. The only
    #    </div> followed by "\n  </section>" is the c2b-estimate close, so the non-greedy match
    #    spans exactly the dollar panel.
    pat = re.compile(r'(?:\n\s*<!-- PANEL 2[^\n]*-->)?\s*<div class="c2b-estimate">.*?</div>(?=\n  </section>)', re.S)
    n = len(pat.findall(h))
    if n != 1:
        sys.exit(f"{client}: c2b-estimate block x{n}")
    replacement = ("\n\n    " + NOTE) if add_note else ""
    h = pat.sub(replacement, h, count=1)

    open(p, "w", encoding="utf-8").write(h)
    # verify: zero dollar-figure projections remain
    dollars = re.findall(r'\$[0-9][0-9.,]*[kK]?', h)
    print(f"{client}: suppressed dollar trajectory; forward-note={'yes' if add_note else 'no'}; "
          f"dollar-figures-remaining={len(dollars)} {dollars if dollars else ''}")
    return len(dollars)


if __name__ == "__main__":
    client, window_word, note = sys.argv[1], sys.argv[2], sys.argv[3] == "1"
    sys.exit(1 if suppress(client, window_word, note) else 0)

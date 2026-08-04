# Scroll Media Performance Reports — Known Issues

Open defects in shipped reports. One entry per issue. Close an entry by deleting it in the
commit that fixes it.

---

## KI-001 — Mobile type and touch-target floors are under spec fleet-wide

**Status:** OPEN · **Found:** July 23, 2026 (MEAS July closeout build) · **Severity:** low-medium
**Scope:** all six June 2026 v8.5 reports + `measactive/july2026` + the canonical template

### What

The v8.5 process spec states two mobile gates (process-v8.5.md, "Constraints", and
process-v8.4.md, "Pre-deploy validation"):

- **14px body floor** on mobile
- **44px touch targets**

Measured on live reports at 375px, four classes sit under those floors:

| Selector | Measured @375px | Gate | Delta |
|---|---|---|---|
| `.mc-note` | 11px | 14px | −3px |
| `.gt-narr` | 13px | 14px | −1px |
| `.mscore-lead` | 13px | 14px | −1px |
| `.why-text` | 12.8px | 14px | −1.2px |
| `.cap-toggle` ("Show more") | 32px tall | 44px | −12px |
| `details summary` | 43px tall | 44px | −1px |

### What is NOT affected

- `.mc-callout` renders at exactly **14px** on mobile and passes. The v8.5 note about the
  callout floor is accurate; the gap is in the *other* body classes, which the v8.5 mobile
  pass did not measure.
- `.report-nav-link` is **44px** at ≤700px. The v8.5 nav fix (commits `28fb9b0` … `f7ec024`)
  holds.
- **Zero horizontal overflow** at 1440/1100/768/414/375, collapsed and expanded.

### Why this is filed rather than fixed

Confirmed identical in `measactive/june2026` and `measactive/july2026`, so it is **inherited,
not a July regression**. Fixing it touches all six live June reports plus the canonical
template, which is a fleet-wide change that wants its own build, its own 5-breakpoint
re-audit, and its own commit per report (v8.5 constraint: sequential, one commit per report,
never parallel subagents).

This qualifies the v8.5 claim "Zero known mobile violations; distribution-ready" — that
statement is true for horizontal overflow and for nav touch targets, not for body type.

### Fix sketch

In the `@media(max-width:700px)` block, raise `.mc-note`, `.gt-narr`, `.mscore-lead` and
`.why-text` to `14px`, and give `.cap-toggle` `min-height:44px; display:inline-flex;
align-items:center` (the deterministic border-box approach used for the nav fix, not padding
math). `details summary` needs +1px. Then re-run the 5-breakpoint audit on every report.

### Verify

```js
// at 375px, past the access gate
const px = s => Math.min(...[...document.querySelectorAll(s)].map(e => parseFloat(getComputedStyle(e).fontSize)));
const h  = s => Math.min(...[...document.querySelectorAll(s)].map(e => e.getBoundingClientRect().height).filter(x => x > 0));
({ mcNote: px('.mc-note'), gtNarr: px('.gt-narr'), mscoreLead: px('.mscore-lead'),
   whyText: px('.why-text'), capToggle: h('.cap-toggle'), summary: h('details summary') })
```

---

## KI-002 — inject_top_posts() greedy posts-grid fallback damaged Beat-4 dropdowns — FIXED

**Status:** FIXED (this commit) · **Found:** Aug 4, 2026 (July 2026 build) · **Severity:** high (silent HTML corruption)

`inject_report_data.py::inject_top_posts()` had a last-resort branch that filled `<div class="posts-grid">` with a greedy regex running to the next `</section>`; on any report carrying a Beat-4 "other standout posts" dropdown it swallowed the dropdown **and** the quarter-view / month-score strip (hit Launch Party + MEAS this cycle, both hand-recovered). Fixed by removing the fallback entirely — Top-3 injection now targets only the `{{TOP_POSTS_HTML}}` slot or `TP_START`/`TP_END` markers and **hard-fails** ("no {{TOP_POSTS_HTML}} slot or TP markers in <path>; scaffold the shell first") if neither is present, making the marker a build precondition per the SOP.

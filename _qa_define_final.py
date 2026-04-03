"""
Comprehensive web dev QA for DEFINE Oakley March 2026 report.
Checks: HTML validity, accessibility, mobile, branding, content, links, performance, UX.
"""
import re

with open('/home/ubuntu/scroll-reports-repo/defineoakley/march2026/index.html', 'r') as f:
    html = f.read()

checks = []

def check(label, condition, fix=None):
    checks.append((label, bool(condition), fix))

# ── 1. DOCTYPE & META ──
check("DOCTYPE declared", html.strip().startswith('<!DOCTYPE html') or html.strip().startswith('<html'))
check("charset UTF-8", 'charset="UTF-8"' in html or "charset='UTF-8'" in html)
check("viewport meta present", 'name="viewport"' in html)
check("maximum-scale=5.0 in viewport", 'maximum-scale=5.0' in html)
check("theme-color meta present", 'name="theme-color"' in html)
check("OG title present", 'property="og:title"' in html)
check("OG description present", 'property="og:description"' in html)
check("Favicon link present", 'rel="icon"' in html)
check("Google Fonts loaded", 'fonts.googleapis.com' in html)
check("Source Sans 3 font", 'Source+Sans+3' in html or 'Source Sans 3' in html)

# ── 2. BRANDING ──
check("Scroll Media logo in hero", 'hero-logo' in html)
check("Scroll Media logo in footer", 'footer-logo' in html)
check("Azure color var defined", '--azure:#0e3387' in html or '--azure: #0e3387' in html)
check("Highlight color var defined", '--hl:#e2ed7a' in html or '--hl: #e2ed7a' in html)
check("Shadow color var defined", '--shadow:#151516' in html or '--shadow: #151516' in html)
check("White footer background", 'background:#ffffff' in html.lower() or 'background: #ffffff' in html.lower() or '.footer{background:#ffffff' in html or '.footer{background:#fff' in html)
check("Scroll progress bar present", 'id="progress-bar"' in html)
check("Progress bar gradient uses brand colors", '--azure' in html and '--hl' in html and 'progress-bar' in html)

# ── 3. STRUCTURE & SECTIONS ──
check("Hero section present", 'class="hero"' in html)
check("Stage badge present", 'hero-stage-badge' in html)
check("Lift Stage text in badge", 'Lift Stage' in html)
check("Hero bullet points present", 'hero-bullets' in html)
check("Exactly 3 hero bullets", html.count('class="hero-bullet"') == 3)
check("Score card present", 'class="score-card"' in html or 'score-card' in html)
check("Score 8.2 shown", '8.2' in html)
check("Solid Month label", 'Solid Month' in html)
check("Score delta shown", 'score-delta' in html)
check("Trend bars present", 'trend-bars' in html)
check("Trend shows Jan Feb Mar", 'Jan' in html and 'Feb' in html and 'Mar' in html)
check("Followers banner present", 'followers-banner' in html)
check("Total followers 3,673", '3,673' in html)
check("Target Range label (not Lift Target)", 'Target Range' in html and 'Lift Target' not in html)
check("Business Goals section present", 'goals-grid' in html)
check("3 goal cards present", html.count('goal-card') >= 3)
check("Progress bars in goals", 'goal-bar-fill' in html)
check("Performance Dashboard section", 'funnel-group' in html)
check("TOFU: Awareness & Authority", 'Awareness &amp; Authority' in html or 'Awareness & Authority' in html)
check("MOFU: Engagement & Trust", 'Engagement' in html and 'Trust' in html)
check("BOFU: Consideration & Conversion", 'Consideration' in html and 'Conversion' in html)
check("TOFU metrics: New Followers, Shares, Views", 'New Followers' in html and 'Shares' in html and 'Total Views' in html)
check("MOFU metrics: Profile Visits, Retention, Saves, Comments", 'Profile Visits' in html and 'Retention %' in html and 'Saves' in html and 'Comments' in html)
check("BOFU metrics: CTR, Link Taps, PCR", 'Click-Through Rate' in html and 'Link Taps' in html and 'Profile Conversion Rate' in html)
check("Avg Reach/Day NOT in report", 'Avg Reach' not in html and 'avg_reach' not in html and 'Reach/Day' not in html)
check("Avg Watch Time NOT in report", 'Avg Watch Time' not in html and 'Watch Time' not in html)
check("Top 3 Posts section present", 'posts-grid' in html)
check("Exactly 3 post cards", html.count('class="post-card"') == 3)
check("Post format tags present", 'post-format-tag' in html)
check("Per-post retention present", 'post-retention-row' in html)
check("Post 1 retention 77.6%", '77.6%' in html)
check("Post 2 retention 92.0%", '92.0%' in html)
check("Post 3 retention 41.6%", '41.6%' in html)
check("WHY IT WORKED sections present", 'WHY IT WORKED' in html)
check("Post hook blockquotes present (3)", html.count('post-hook') >= 3)
check("Post caption sections present", 'post-caption' in html)
check("Post caption label present", 'post-caption-label' in html)
check("No duplicate View on Instagram text links", 'class="post-link"' not in html)
check("Strategy Adjustments section present", 'adj-grid' in html)
check("30:30 reference removed", '30:30' not in html)
check("Doubling Down card present", 'Doubling Down' in html)
check("Testing card present", 'Testing' in html)
check("Fixing card present", 'Fixing' in html)
check("Next Month's CTAs section", "Next Month" in html and "CTA" in html)
check("Previous Reports section present", 'prev-section' in html)
check("Feb 2026 previous report card", 'february2026' in html)
check("Footer present", 'class="footer"' in html)

# ── 4. ACCESSIBILITY ──
check("Lang attribute on html", 'lang="en"' in html)
check("Alt text on hero logo", 'alt="Scroll Media"' in html)
check("aria-labelledby on sections", 'aria-labelledby' in html)
check("role=region on key sections", 'role="region"' in html)
check("aria-label on followers banner", 'aria-label="Total Followers"' in html)
check("aria-hidden on decorative numbers", 'aria-hidden="true"' in html)

# ── 5. MOBILE ──
check("Media query 640px", '640px' in html)
check("Media query 580px", '580px' in html)
check("Media query 480px", '480px' in html)
check("Media query 760px", '760px' in html)
check("overflow-x hidden on body", 'overflow-x:hidden' in html or 'overflow-x: hidden' in html)
check("clamp() for responsive font sizes", 'clamp(' in html)
check("min() for responsive sizes", 'min(' in html)
check("Tap highlight removed", '-webkit-tap-highlight-color:transparent' in html or '-webkit-tap-highlight-color: transparent' in html)

# ── 6. PERFORMANCE ──
check("Font preconnect present", 'rel="preconnect"' in html)
check("Passive scroll listener", "passive: true" in html or "{passive: true}" in html)
check("IntersectionObserver for bar animations", 'IntersectionObserver' in html)
check("View on Instagram buttons present", html.count('post-ig-btn') >= 3)
check("No inline style on body", '<body style=' not in html)

# ── 7. CONTENT ACCURACY ──
check("Client name: DEFINE Oakley", 'DEFINE Oakley' in html)
check("Month: March 2026", 'March 2026' in html)
check("Score 8.2/10", '8.2' in html)
check("Stage: Lift", 'Lift' in html)
check("Total Views 63,133", '63,133' in html)
check("New Followers 46", '>46<' in html)
check("Retention 72.0%", '72.0%' in html)
check("Comments 67", '>67<' in html)
check("CTR 6.9%", '6.9%' in html)
check("Link Taps 49", '>49<' in html)

# ── 8. LINKS & EMBEDS ──
ig_urls = re.findall(r'instagram\.com/(?:reel|p)/([A-Za-z0-9_-]+)', html)
check("3 unique Instagram post URLs (reel or /p/)", len(set(ig_urls)) >= 3)
check("Post 1 URL: DWEbxXFjTdi", 'DWEbxXFjTdi' in html)
check("Post 2 URL: DVgdzqnDURd", 'DVgdzqnDURd' in html)
check("Post 3 URL: DVydQw8DZtC", 'DVydQw8DZtC' in html)
# Check for template artifacts only outside <style> blocks
non_style_html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
template_artifacts = re.findall(r'\{\{.*?\}\}', non_style_html)
check("No template vars {{ }} in content", len(template_artifacts) == 0)
check("Favicon URL is CDN URL", 'manuscdn.com' in html or 'scrollmedia' in html.lower())
check("Logo URLs are CDN URLs", 'manuscdn.com' in html)

# ── RESULTS ──
passed = sum(1 for _, p, _ in checks if p)
failed = sum(1 for _, p, _ in checks if not p)
total = len(checks)

print(f"\n{'='*60}")
print(f"QA RESULTS: {passed}/{total} passed  |  {failed} failed")
print(f"{'='*60}\n")

if failed > 0:
    print("❌ FAILED CHECKS:")
    for label, passed_check, fix in checks:
        if not passed_check:
            print(f"  ✗ {label}")
            if fix:
                print(f"    → Fix: {fix}")
    print()

print("✅ PASSED CHECKS:")
for label, passed_check, _ in checks:
    if passed_check:
        print(f"  ✓ {label}")

print(f"\n{'='*60}")
print(f"FINAL: {'✅ ALL CLEAR' if failed == 0 else f'❌ {failed} ISSUE(S) TO FIX'}")
print(f"{'='*60}")

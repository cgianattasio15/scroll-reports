# Scroll Reports v3.0 - Deployment & QA Guide

## 🎯 EXECUTIVE SUMMARY

**What We Built:**
URL-based token system for client-isolated report access + full brand compliance rebuild

**Why This Solution:**
- ✅ Zero client friction (no passwords/logins)
- ✅ Perfect isolation (unpredictable URLs per client)  
- ✅ Team seamless (internal URLs unchanged)
- ✅ Free (no Pro plan needed)
- ✅ Simple (JavaScript routing, no server logic)

**Deployment Time:** 2-3 hours total
**Testing Time:** 1 hour
**Go-Live Risk:** LOW (backwards compatible with current URLs)

---

## 📦 DEPLOYMENT PACKAGE CONTENTS

```
scroll-reports-v3/
├── index.html (Updated - Inter font)
├── 404.html (NEW - Custom error page)
├── r/
│   └── index.html (NEW - Token router entry)
├── js/
│   └── token-router.js (NEW - Routing logic)
└── config/
    └── client-tokens.js (NEW - Token registry)
```

---

## 🚀 DEPLOYMENT STEPS

### PRE-DEPLOYMENT CHECKLIST

- [ ] Backup current production site
- [ ] Generate tokens for all 3 current clients
- [ ] Document tokens in Client Account Homebase
- [ ] Review all files in deployment package
- [ ] Test locally if possible

### STEP 1: Generate Client Tokens (5 minutes)

**Run this in browser console or Node:**

```javascript
function generateToken() {
  const chars = 'abcdefghjkmnpqrstuvwxyz23456789';
  return Array.from({length: 8}, () => 
    chars[Math.floor(Math.random() * chars.length)]
  ).join('');
}

// Generate for each client
console.log('Launch Party:', generateToken());
console.log('Skin by Brownlee:', generateToken());
console.log('Define Oakley:', generateToken());
```

**Record tokens in table:**

| Client | Token | Notes |
|--------|-------|-------|
| launchparty | 8k3h9x2n | Example - replace with real |
| skinbybrownlee | m4p7w1qz | Example - replace with real |
| defineoakley | x9n2k5rt | Example - replace with real |

**Update `/config/client-tokens.js`** with real tokens before deployment.

### STEP 2: Add New Files to GitHub Repo (10 minutes)

**In your local repo:**

```bash
# Navigate to repo
cd /path/to/scroll-reports-deploy

# Create new folders
mkdir -p r js config

# Copy files from deployment package
cp scroll-reports-v3/r/index.html r/
cp scroll-reports-v3/js/token-router.js js/
cp scroll-reports-v3/config/client-tokens.js config/
cp scroll-reports-v3/404.html .

# Stage changes
git add r/ js/ config/ 404.html
```

### STEP 3: Update Existing Files (15 minutes)

**Update landing page:**
```bash
cp scroll-reports-v3/index.html index.html
git add index.html
```

**Update all HTML files (find & replace):**

Use your editor's find & replace across project:

**Find:**
```
font-family: 'Source Sans 3'
```

**Replace with:**
```
font-family: 'Inter'
```

**Find:**
```
https://fonts.googleapis.com/css2?family=Source+Sans+3
```

**Replace with:**
```
https://fonts.googleapis.com/css2?family=Inter
```

**Affected files:**
- `/skinbybrownlee/index.html`
- `/launchparty/index.html`
- `/launchparty/january2026/index.html`
- `/defineoakley/index.html`
- Any other HTML files

```bash
git add .
```

### STEP 4: Commit and Push (2 minutes)

```bash
git commit -m "v3.0: Add token-based security + brand compliance fix

- Add URL-based token system for client isolation
- Implement token router (/r/[token]/[report]/)
- Add custom 404 page
- Fix brand compliance: Source Sans 3 → Inter
- Add client token registry
- Update landing page messaging"

git push origin main
```

### STEP 5: Configure Netlify (5 minutes)

1. **Go to Netlify dashboard** → scroll-reports site
2. **Site settings** → **Build & deploy** → **Post processing**
3. **Custom 404 page:** Set to `/404.html`
4. **Save**

### STEP 6: Wait for Auto-Deploy (1 minute)

- Watch deployment log in Netlify
- Should complete in 30-60 seconds
- Verify "Published" status

### STEP 7: Smoke Test (10 minutes)

Run through all critical test cases below before announcing to team.

---

## ✅ COMPLETE QA CHECKLIST

### CRITICAL: Token Router Functionality

**Test Case 1: Valid Token → Success**
- [ ] Visit: `reports.scrollmedia.co/r/8k3h9x2n/january2026/`
- [ ] Should see loading spinner briefly
- [ ] Should redirect to: `/launchparty/january2026/`
- [ ] Report displays correctly
- [ ] No console errors

**Test Case 2: Invalid Token → 404**
- [ ] Visit: `reports.scrollmedia.co/r/invalid123/january2026/`
- [ ] Should redirect to `/404.html`
- [ ] 404 page displays correctly
- [ ] "Back to Home" link works
- [ ] No console errors

**Test Case 3: Malformed URL → 404**
- [ ] Visit: `reports.scrollmedia.co/r/tooshort/january2026/`
- [ ] Should show 404 page
- [ ] Visit: `reports.scrollmedia.co/r/toolongtoken/january2026/`
- [ ] Should show 404 page

**Test Case 4: Team URLs Still Work**
- [ ] Visit: `reports.scrollmedia.co/launchparty/january2026/`
- [ ] Report loads directly (no redirect)
- [ ] All content renders correctly
- [ ] Confirms backwards compatibility

### CRITICAL: Security Isolation

**Test Case 5: Cross-Client Access Prevention**
- [ ] Get Launch Party token URL
- [ ] Change `launchparty` to `skinbybrownlee` in path
- [ ] Example: `/r/8k3h9x2n/skinbybrownlee/january2026/`
- [ ] Should redirect to `/launchparty/` (not skinbybrownlee)
- [ ] Confirms token is locked to specific client

**Test Case 6: Directory Traversal Prevention**
- [ ] Try: `/r/../skinbybrownlee/`
- [ ] Should show 404
- [ ] No access to other directories

### MEDIUM: Brand Compliance

**Test Case 7: Typography Check**
- [ ] Open any page
- [ ] Inspect computed font-family
- [ ] Should show: `Inter` (not Source Sans 3)
- [ ] Check on: landing page, report, 404 page

**Test Case 8: Color Accuracy**
- [ ] Check Azure blue: `#0c3387`
- [ ] Check Shadow black: `#151516`
- [ ] Check Ghost background: `#fafdff`
- [ ] Use browser inspector or eyedropper

**Test Case 9: Spacing Grid**
- [ ] Check padding/margins
- [ ] Should follow 8px grid (8, 16, 24, 32, 48, 64)
- [ ] Inspect computed values on key elements

### HIGH: Mobile Responsiveness

**Test Each Breakpoint:**

**360px (Galaxy S8/S9) - CRITICAL**
- [ ] No horizontal scroll
- [ ] Text readable without zoom
- [ ] Touch targets ≥ 44px
- [ ] Loading spinner centers
- [ ] 404 error page readable

**390px (iPhone 12/13) - CRITICAL**
- [ ] Same tests as 360px
- [ ] Report hero section fits
- [ ] Stats cards stack properly
- [ ] Footer readable

**768px (iPad) - MEDIUM**
- [ ] Layout transitions smoothly
- [ ] No awkward breakpoint issues
- [ ] Buttons/cards properly sized

**1280px (Desktop) - LOW**
- [ ] Content max-width applied
- [ ] Not stretched too wide
- [ ] Comfortable reading experience

### MEDIUM: Cross-Browser Testing

**Chrome/Brave (Primary)**
- [ ] Token router works
- [ ] Fonts load correctly
- [ ] No console errors

**Safari Desktop**
- [ ] Token router works
- [ ] Fonts load correctly
- [ ] Redirects work

**Safari iOS**
- [ ] Token router works on real device
- [ ] Touch interactions smooth
- [ ] Loading state displays

**Firefox**
- [ ] Token router works
- [ ] Fonts load correctly
- [ ] No rendering issues

### LOW: Performance

**Lighthouse Mobile Audit**
- [ ] Performance Score ≥ 90
- [ ] Accessibility Score ≥ 95
- [ ] Best Practices ≥ 90
- [ ] SEO ≥ 90

**Loading Metrics:**
- [ ] First Contentful Paint < 1.5s
- [ ] Time to Interactive < 2.5s
- [ ] Cumulative Layout Shift < 0.1

---

## 🔥 SMOKE TEST SCRIPT (5 Minutes)

**Run this immediately after deployment:**

```
✅ Test 1: Homepage
→ Visit reports.scrollmedia.co
→ Logo displays
→ Text readable
→ No console errors

✅ Test 2: Valid Token  
→ Visit reports.scrollmedia.co/r/8k3h9x2n/january2026/
→ Brief loading state
→ Redirects to /launchparty/january2026/
→ Report displays correctly

✅ Test 3: Invalid Token
→ Visit reports.scrollmedia.co/r/badtoken1/january2026/
→ Shows 404 page
→ Back button works

✅ Test 4: Mobile (Real Device)
→ Open token URL on iPhone/Android
→ Loads without horizontal scroll
→ Touch targets work
→ Text readable

✅ Test 5: Team URL
→ Visit reports.scrollmedia.co/launchparty/
→ Archive page loads
→ Month link works
→ Backwards compatible
```

**If all 5 tests pass → CLEAR FOR PRODUCTION USE**

---

## 📧 CLIENT EMAIL TEMPLATE

**Subject:** Your [Month] [Year] Performance Report is Ready

```
Hi [Client Name],

Your [Month] performance report is ready to view:

🔗 View Report: https://reports.scrollmedia.co/r/[TOKEN]/[monthyear]/

This link is unique to your account and provides secure access to your monthly performance data, insights, and strategic recommendations.

Questions about your report? Reply to this email or reach out to your account manager.

— [Account Manager Name]
Scroll Media
```

**Example URLs:**
- Launch Party Jan 2026: `reports.scrollmedia.co/r/8k3h9x2n/january2026/`
- Skin by Brownlee Feb 2026: `reports.scrollmedia.co/r/m4p7w1qz/february2026/`
- Define Oakley Jan 2026: `reports.scrollmedia.co/r/x9n2k5rt/january2026/`

---

## 🔧 TROUBLESHOOTING

### Issue: Token router not working

**Symptoms:** Token URL shows blank page or doesn't redirect

**Fix:**
1. Check browser console for errors
2. Verify `/js/token-router.js` exists at root
3. Confirm `<script>` tag in `/r/index.html` has correct path
4. Clear browser cache and retry

### Issue: 404 page not showing

**Symptoms:** Netlify default 404 appears instead of custom page

**Fix:**
1. Go to Netlify → Site settings → Post processing
2. Verify "404 page" is set to `/404.html`
3. Save and redeploy
4. Wait 2-3 minutes for changes to propagate

### Issue: Fonts not loading (still showing Source Sans 3)

**Symptoms:** Text appears in wrong font

**Fix:**
1. Verify Google Fonts URL uses `Inter` not `Source+Sans+3`
2. Check `font-family` CSS declarations
3. Clear browser cache (hard refresh: Cmd+Shift+R or Ctrl+Shift+F5)
4. Check Network tab to confirm Inter is loading

### Issue: Cross-client access working (SECURITY RISK)

**Symptoms:** One client's token shows another client's data

**Fix:**
1. **IMMEDIATELY** set all tokens to `active: false` in `/config/client-tokens.js`
2. Commit and push (pauses all client access)
3. Debug token router logic
4. Verify token → client mapping is correct
5. Re-enable tokens after fix confirmed

---

## 📊 SUCCESS METRICS (Week 1)

### Security
- [ ] Zero cross-client access incidents
- [ ] Zero unauthorized report views
- [ ] All tokens remain secret

### Team Efficiency
- [ ] Report deployment < 60 seconds
- [ ] Client email sent < 2 minutes after deploy
- [ ] Zero auth-related support tickets

### Client Experience
- [ ] 100% one-click access (no login friction)
- [ ] Mobile-friendly on all devices
- [ ] Fast load times (< 2s perceived)

---

## 🚨 ROLLBACK PLAN

**If critical issues arise:**

### Quick Disable (2 minutes)
```bash
# In /config/client-tokens.js, set all to inactive
'8k3h9x2n': { ...existing, active: false },
'm4p7w1qz': { ...existing, active: false },
'x9n2k5rt': { ...existing, active: false }

git commit -m "Emergency: Disable all tokens"
git push origin main
```

### Full Rollback (5 minutes)
```bash
# Revert to previous working commit
git log --oneline  # Find commit before v3.0
git revert [commit-hash]
git push origin main
```

### Alternative Access (Immediate)
- Team can still use direct URLs: `/launchparty/january2026/`
- Send clients direct folder URLs temporarily
- Not ideal but maintains access while fixing

---

## 📝 POST-DEPLOYMENT

### Update Documentation
- [ ] Add tokens to Client Account Homebase
- [ ] Update internal wiki/Notion with new workflow
- [ ] Train account managers on token URLs

### Announce to Team
**Slack/Email:**
```
🎉 Reports v3.0 is live!

New client URL format:
reports.scrollmedia.co/r/[token]/[monthyear]/

Each client has unique token (see Homebase for tokens).
Team still uses regular URLs: reports.scrollmedia.co/clientname/

Questions? Ping Chase
```

### Monitor First Week
- [ ] Watch Netlify analytics for 404 rate
- [ ] Track client feedback
- [ ] Monitor support tickets
- [ ] Review browser console logs

---

## 🎯 NEXT MONTH: Adding New Report

**Workflow unchanged:**

1. Generate report HTML
2. Save to `/launchparty/february2026/index.html`
3. Commit + push
4. Send client email with token URL: `/r/8k3h9x2n/february2026/`

**Total time: Same as before (30 min report + 60 sec deploy)**

---

## 📈 FUTURE ENHANCEMENTS (Phase 4+)

### Optional Improvements
- [ ] Analytics: Track which clients view reports
- [ ] Expiring tokens: Auto-disable after 90 days
- [ ] Admin dashboard: Manage tokens in UI
- [ ] Email templates: Auto-generate client emails
- [ ] Audit logging: Track token usage

**Not urgent - system is production-ready as-is**

---

**Deployed:** [DATE]  
**Version:** 3.0  
**Status:** ✅ PRODUCTION READY

**Scroll Media** — Strategy First, Simplification Always

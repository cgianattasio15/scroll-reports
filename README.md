# Scroll Reports v3.0 - Complete Deployment Package

## 🎯 WHAT THIS IS

This folder contains **everything you need** to replace your current GitHub repo with the updated v3.0 system.

**What's included:**
- ✅ All new security files (token system)
- ✅ All existing client files (with Inter font fix)
- ✅ Updated landing page
- ✅ Custom 404 page
- ✅ All documentation

---

## 🚀 DEPLOYMENT STEPS (10 Minutes)

### Step 1: Backup Current Repo

Before doing anything, create a backup:

```bash
# In your current repo folder
git add .
git commit -m "Backup before v3.0 upgrade"
git push origin main
```

Or just make sure everything is committed so you can roll back if needed.

---

### Step 2: Replace Repo Contents

**Option A: GitHub Desktop (Easiest)**

1. Open your `scroll-reports-deploy` repo folder
2. **Delete everything EXCEPT the `.git` folder** (hidden folder - don't delete it!)
3. Copy everything from this `scroll-reports-complete` folder into your repo
4. Open GitHub Desktop
5. You'll see all changes
6. Review to make sure `.git` folder still exists
7. Commit with message: "v3.0: Token security + brand compliance"
8. Push to deploy

**Option B: Command Line**

```bash
# Navigate to your current repo
cd /path/to/scroll-reports-deploy

# Backup first
git add . && git commit -m "Backup before v3.0" && git push

# Remove all files EXCEPT .git
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +

# Copy new files from this package
cp -r /path/to/scroll-reports-complete/* .

# Verify .git folder still exists
ls -la | grep .git

# Commit and push
git add .
git commit -m "v3.0: Token security + brand compliance"
git push origin main
```

---

### Step 3: Configure Netlify (2 Minutes)

1. Go to Netlify dashboard → your site
2. Site settings → Build & deploy → Post processing
3. Custom 404 page: Set to `/404.html`
4. Save

---

### Step 4: Generate Real Client Tokens (5 Minutes)

**Run this in browser console:**

```javascript
function generateToken() {
  const chars = 'abcdefghjkmnpqrstuvwxyz23456789';
  return Array.from({length: 8}, () => 
    chars[Math.floor(Math.random() * chars.length)]
  ).join('');
}

console.log('Launch Party:', generateToken());
console.log('Skin by Brownlee:', generateToken());
console.log('Define Oakley:', generateToken());
```

**Update `/config/client-tokens.js` with real tokens:**

Replace the example tokens (8k3h9x2n, m4p7w1qz, x9n2k5rt) with the ones you just generated.

```bash
# Edit the file
nano config/client-tokens.js

# Update tokens, save

# Commit and push
git add config/client-tokens.js
git commit -m "Update with real client tokens"
git push origin main
```

---

### Step 5: Test Everything (10 Minutes)

**Critical Tests:**

1. Visit `reports.scrollmedia.co` - Landing page loads ✅
2. Visit `reports.scrollmedia.co/r/[YOUR_TOKEN]/january2026/` - Redirects correctly ✅
3. Visit `reports.scrollmedia.co/r/badtoken1/january2026/` - Shows 404 ✅
4. Visit `reports.scrollmedia.co/launchparty/january2026/` - Team URL works ✅
5. Test on mobile device - Responsive and readable ✅

**If all 5 pass → ✅ READY FOR PRODUCTION**

---

## 📁 FOLDER STRUCTURE

```
scroll-reports-complete/
├── index.html                          (Landing page - Inter font)
├── 404.html                           (NEW - Custom error page)
├── README.md                          (This file)
├── DEPLOYMENT_GUIDE.md                (Full QA checklist)
├── r/
│   └── index.html                     (NEW - Token router entry)
├── js/
│   └── token-router.js               (NEW - Routing logic)
├── config/
│   └── client-tokens.js              (NEW - Token registry - UPDATE THIS)
├── assets/
│   └── favicon.svg                    (Scroll Media logo)
├── launchparty/
│   ├── index.html                     (Archive page - Inter font)
│   └── january2026/
│       └── index.html                 (Report - Inter font)
├── skinbybrownlee/
│   └── index.html                     (Archive page - Inter font)
└── defineoakley/
    └── index.html                     (Archive page - Inter font)
```

---

## ⚠️ CRITICAL: UPDATE TOKENS

**BEFORE sending to clients, you MUST:**

1. Generate real tokens (see Step 4 above)
2. Update `/config/client-tokens.js` with real tokens
3. Update `/js/token-router.js` with same tokens (line 15)
4. Commit and push changes

**Current tokens are EXAMPLES ONLY** (8k3h9x2n, m4p7w1qz, x9n2k5rt)

---

## 📧 CLIENT EMAIL TEMPLATE

**Subject:** Your January 2026 Performance Report is Ready

```
Hi [Client Name],

Your January performance report is ready to view:

🔗 View Report: https://reports.scrollmedia.co/r/[TOKEN]/january2026/

This link is unique to your account and provides secure access to your monthly performance data.

Questions? Reply to this email.

— [Account Manager]
Scroll Media
```

**Token URLs:**
- Launch Party: `reports.scrollmedia.co/r/[THEIR_TOKEN]/january2026/`
- Skin by Brownlee: `reports.scrollmedia.co/r/[THEIR_TOKEN]/february2026/`
- Define Oakley: `reports.scrollmedia.co/r/[THEIR_TOKEN]/january2026/`

---

## 🎯 WHAT CHANGED

### Security (NEW)
- ✅ Token-based client isolation
- ✅ Unique URLs per client
- ✅ Cannot access other clients' data
- ✅ Custom 404 page

### Brand Compliance (FIXED)
- ✅ Inter font (was Source Sans 3)
- ✅ All pages updated
- ✅ Mobile-optimized
- ✅ Scroll brand colors

### Team Workflow (UNCHANGED)
- ✅ Still use clean URLs internally
- ✅ Same deployment process
- ✅ Same folder structure
- ✅ Backwards compatible

---

## 🔧 TROUBLESHOOTING

### Issue: Token router not working

1. Check browser console for errors
2. Verify `/js/token-router.js` exists
3. Clear browser cache (Cmd+Shift+R)

### Issue: 404 not showing

1. Netlify → Site settings → Post processing
2. Set "404 page" to `/404.html`
3. Wait 2-3 minutes

### Issue: Fonts still wrong

1. Hard refresh browser (Cmd+Shift+R or Ctrl+Shift+F5)
2. Check Network tab - verify Inter is loading
3. Inspect element - confirm font-family shows "Inter"

---

## 🚨 ROLLBACK PLAN

If something breaks:

```bash
# Revert to previous commit
git log --oneline  # Find last good commit
git revert [commit-hash]
git push origin main
```

Or restore from backup you made in Step 1.

---

## 📊 ADDING NEW REPORTS (Future)

**Process unchanged:**

1. Generate report HTML
2. Save to `/clientname/monthyear/index.html`
3. Commit + push
4. Send client token URL: `reports.scrollmedia.co/r/[token]/monthyear/`

**Time: Same as before (30 min + 60 sec deploy)**

---

## ✅ CHECKLIST BEFORE GO-LIVE

- [ ] Backed up current repo
- [ ] Replaced all files in repo
- [ ] `.git` folder still exists
- [ ] Generated real client tokens
- [ ] Updated `/config/client-tokens.js` with real tokens
- [ ] Updated `/js/token-router.js` with real tokens
- [ ] Committed and pushed all changes
- [ ] Configured Netlify 404 page
- [ ] Tested valid token URL
- [ ] Tested invalid token URL
- [ ] Tested team URL (backwards compatible)
- [ ] Tested on mobile device
- [ ] Documented tokens in Client Account Homebase

---

## 📞 QUESTIONS?

**Technical Details:** See `DEPLOYMENT_GUIDE.md`  
**Full Specification:** See `IMPLEMENTATION_COMPLETE.md`  
**Issues:** Roll back using git revert

---

**Deployed:** [DATE]  
**Version:** 3.0  
**Status:** Ready for Production

**Scroll Media** — Strategy First, Simplification Always

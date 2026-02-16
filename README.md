# Scroll Reports System v2.0

## Overview
Monthly client performance report hosting system for Scroll Media. Built with GitHub + Netlify auto-deploy workflow.

## What Changed (v2.0)

### ✅ Security Update
- **Removed Basic Auth password protection**
- Rationale: Too manual, requires Pro plan, clunky UX
- Current approach: Security through obscurity (unlisted URLs)
- Future: Migrate to Netlify Identity with magic links

### ✅ Branding Updates
- Added Scroll Media monogram favicon (navy "sm")
- Added full Scroll Media wordmark to landing page header
- Added logo to client archive pages
- All logos use transparent backgrounds for seamless integration

### ✅ UI/UX Improvements
- Cleaner header with integrated logo
- Better visual hierarchy
- Improved spacing and typography
- Mobile-optimized layouts

## File Structure

```
scroll-reports-deploy/
├── index.html                  (landing page - client directory)
├── assets/
│   └── favicon.svg            (Scroll Media monogram)
├── skinbybrownlee/
│   └── index.html             (client archive)
├── launchparty/
│   └── index.html             (client archive)
├── defineoakley/
│   └── index.html             (client archive)
├── TESTING_CHECKLIST.md       (QA checklist)
└── README.md                  (this file)
```

## Deployment Workflow

### Adding Monthly Reports (10 seconds)

1. **Generate report** using Monthly Report template (30 min)
2. **Save as:** `clientname/monthyear/index.html`
   - Example: `skinbybrownlee/feb2026/index.html`
3. **In GitHub Desktop:**
   - See changes appear automatically
   - Summary: "Add Feb 2026 report for Skin by Brownlee"
   - Click "Commit to main"
   - Click "Push origin"
4. **Done!** Auto-deploys in 30 seconds

### Adding New Clients

1. **Create folder:** `mkdir newclient`
2. **Copy archive template:** `cp skinbybrownlee/index.html newclient/`
3. **Update client name** in the HTML
4. **Add client card** to landing page `index.html`
5. **Commit and push**

## Security Approach

### Current: Security Through Obscurity
- No password protection
- Site is technically public at reports.scrollmedia.co
- Relies on URLs not being shared publicly
- No search engine indexing (robots.txt)

**Pros:**
- Zero friction for team
- Instant access, no login
- Simple to manage

**Cons:**
- If URL leaks, anyone can access
- Not suitable for highly sensitive data

### Recommended: Netlify Identity (Future)

**Why:**
- Professional auth with magic links
- Session persistence (7-day tokens)
- Easy user management from Netlify dashboard
- Free on Pro plan

**Setup (15 minutes):**
1. Netlify dashboard → Site settings → Identity
2. Enable Identity
3. Set registration to "Invite only"
4. Invite team members
5. Add Identity widget to pages

## Brand Compliance

All pages follow Scroll Media Brand Guidelines v2.0:

- **Colors:** Shadow, Azure, Lucid Dreams, Highlighter
- **Typography:** Inter (web), Visby CF equivalent
- **Voice:** Direct, strategic, confident
- **Design:** Clean, minimal, professional

## Testing

Run through `TESTING_CHECKLIST.md` before major releases.

**Quick test:**
1. Visit reports.scrollmedia.co
2. Click each client card
3. Verify breadcrumbs work
4. Test on mobile device

## Support

Questions? Contact Chase Donovan · chase@getscrollmedia.com

---

**Scroll Media** — Strategy First, Simplification Always

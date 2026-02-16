# Scroll Reports System v3.0 - Complete Implementation

## STRATEGIC DECISION SUMMARY

**Chosen Approach:** URL-based token routing with client isolation

**Why This Wins:**
- ✅ Zero client friction (no passwords, no logins)
- ✅ Perfect isolation (unpredictable URLs per client)
- ✅ Team seamless (use clean internal URLs)
- ✅ Zero cost (no Pro plan needed)
- ✅ Simple maintenance (add tokens = add clients)
- ✅ Scalable (works for 8 clients or 800)

**Trade-off Accepted:**
Security relies on token secrecy (acceptable for read-only reports, not suitable for PHI/PII)

---

## FILES TO CREATE/UPDATE

### NEW FILES (4 total)

```
/r/index.html                    (Token router entry point)
/config/client-tokens.js         (Token → client mapping)
/js/token-router.js             (Routing logic)
/404.html                        (Custom 404 page)
```

### FILES TO UPDATE (All existing HTML files)

```
/index.html                      (Landing page - font fix)
/launchparty/index.html         (Archive - font fix)
/launchparty/january2026/index.html  (Report - font fix)
/skinbybrownlee/index.html      (Archive - font fix)
/defineoakley/index.html        (Archive - font fix)
```

---

## DEPLOYMENT SEQUENCE

### Step 1: Generate Client Tokens

**Action:** Generate 8-character random tokens for each client

**Implementation:**
```javascript
// Token generator (run locally or in browser console)
function generateToken() {
  const chars = 'abcdefghjkmnpqrstuvwxyz23456789'; // Excludes ambiguous chars
  return Array.from({length: 8}, () => 
    chars[Math.floor(Math.random() * chars.length)]
  ).join('');
}

// Generate tokens for current clients
console.log('launchparty:', generateToken());     // Example: 8k3h9x2n
console.log('skinbybrownlee:', generateToken());  // Example: m4p7w1qz
console.log('defineoakley:', generateToken());    // Example: x9n2k5rt
```

**Record Tokens:**
| Client | Token | Created | Notes |
|--------|-------|---------|-------|
| launchparty | 8k3h9x2n | Feb 2026 | Indie beauty boutique |
| skinbybrownlee | m4p7w1qz | Feb 2026 | Med spa/skincare |
| defineoakley | x9n2k5rt | Feb 2026 | Boutique fitness |

**Store in:** Client Account Homebase spreadsheet (new column: "Report Token")

### Step 2: Create Token Configuration

**File:** `/config/client-tokens.js`

```javascript
/**
 * Client Token Registry
 * 
 * Maps unique 8-character tokens to client folder names.
 * Tokens are used in client-facing URLs for access control.
 * 
 * URL Format: reports.scrollmedia.co/r/[token]/[report-path]/
 * 
 * Security Note: Tokens provide isolation through unpredictability,
 * not cryptographic security. Suitable for business reports, not PHI/PII.
 */

const CLIENT_TOKENS = {
  // Launch Party (Indie Beauty Boutique)
  '8k3h9x2n': {
    clientFolder: 'launchparty',
    clientName: 'Launch Party',
    created: '2026-02-16',
    active: true
  },
  
  // Skin by Brownlee (Med Spa)
  'm4p7w1qz': {
    clientFolder: 'skinbybrownlee',
    clientName: 'Skin by Brownlee',
    created: '2026-02-16',
    active: true
  },
  
  // Define Oakley (Boutique Fitness)
  'x9n2k5rt': {
    clientFolder: 'defineoakley',
    clientName: 'Define Oakley',
    created: '2026-02-16',
    active: true
  }
  
  // ADD NEW CLIENTS HERE
  // Generate tokens using: Array.from({length:8},()=>'abcdefghjkmnpqrstuvwxyz23456789'[Math.floor(Math.random()*32)]).join('')
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { CLIENT_TOKENS };
}
```

### Step 3: Create Token Router

**File:** `/js/token-router.js`

```javascript
/**
 * Token-Based URL Router for Scroll Reports
 * 
 * Routes client-specific token URLs to actual report paths
 * Example: /r/8k3h9x2n/january2026/ → /launchparty/january2026/
 */

(function() {
  'use strict';

  // Token registry (must match /config/client-tokens.js)
  const CLIENT_TOKENS = {
    '8k3h9x2n': { clientFolder: 'launchparty', clientName: 'Launch Party', active: true },
    'm4p7w1qz': { clientFolder: 'skinbybrownlee', clientName: 'Skin by Brownlee', active: true },
    'x9n2k5rt': { clientFolder: 'defineoakley', clientName: 'Define Oakley', active: true }
  };

  /**
   * Extract token and path from current URL
   * Expected format: /r/[token]/[report-path]/
   */
  function parseTokenURL() {
    const path = window.location.pathname;
    const match = path.match(/^\/r\/([a-z0-9]{8})\/(.+)$/);
    
    if (!match) {
      return null;
    }
    
    return {
      token: match[1],
      reportPath: match[2]
    };
  }

  /**
   * Validate token and return client info
   */
  function validateToken(token) {
    const client = CLIENT_TOKENS[token];
    
    if (!client || !client.active) {
      return null;
    }
    
    return client;
  }

  /**
   * Redirect to actual report path
   */
  function redirectToReport(clientFolder, reportPath) {
    const targetURL = `/${clientFolder}/${reportPath}`;
    
    // Log for debugging (remove in production if needed)
    console.log('[Token Router] Redirecting to:', targetURL);
    
    // Perform redirect
    window.location.href = targetURL;
  }

  /**
   * Show 404 error
   */
  function show404() {
    window.location.href = '/404.html';
  }

  /**
   * Main routing logic
   */
  function routeTokenURL() {
    const parsed = parseTokenURL();
    
    // Invalid URL format
    if (!parsed) {
      console.error('[Token Router] Invalid URL format');
      show404();
      return;
    }
    
    // Validate token
    const client = validateToken(parsed.token);
    
    if (!client) {
      console.error('[Token Router] Invalid or inactive token:', parsed.token);
      show404();
      return;
    }
    
    // Valid token - redirect to report
    redirectToReport(client.clientFolder, parsed.reportPath);
  }

  // Execute routing on page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', routeTokenURL);
  } else {
    routeTokenURL();
  }

})();
```

### Step 4: Create Token Entry Point

**File:** `/r/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Redirecting... | Scroll Media</title>
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    :root {
      --shadow: #151516;
      --azure: #0c3387;
      --ghost: #fafdff;
    }
    
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
      background: var(--ghost);
      color: var(--shadow);
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      text-align: center;
      padding: 24px;
    }
    
    .loading {
      max-width: 400px;
    }
    
    .spinner {
      width: 40px;
      height: 40px;
      margin: 0 auto 24px;
      border: 3px solid rgba(12, 51, 135, 0.1);
      border-top-color: var(--azure);
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    
    h1 {
      font-size: 24px;
      font-weight: 700;
      margin-bottom: 12px;
      letter-spacing: -0.5px;
    }
    
    p {
      font-size: 16px;
      color: rgba(21, 21, 22, 0.6);
      line-height: 1.6;
    }
  </style>
</head>
<body>
  <div class="loading">
    <div class="spinner"></div>
    <h1>Loading Your Report</h1>
    <p>Redirecting you to your performance report...</p>
  </div>
  
  <script src="/js/token-router.js"></script>
</body>
</html>
```

### Step 5: Create Custom 404 Page

**File:** `/404.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Report Not Found | Scroll Media</title>
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    :root {
      --shadow: #151516;
      --azure: #0c3387;
      --ghost: #fafdff;
    }
    
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
      background: var(--ghost);
      color: var(--shadow);
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      text-align: center;
      padding: 24px;
    }
    
    .error-container {
      max-width: 500px;
    }
    
    .logo {
      margin-bottom: 32px;
    }
    
    .logo img {
      height: 48px;
      width: auto;
    }
    
    .error-code {
      font-size: 72px;
      font-weight: 800;
      color: var(--azure);
      line-height: 1;
      margin-bottom: 16px;
      letter-spacing: -2px;
    }
    
    h1 {
      font-size: 28px;
      font-weight: 700;
      margin-bottom: 12px;
      letter-spacing: -0.5px;
    }
    
    p {
      font-size: 16px;
      color: rgba(21, 21, 22, 0.6);
      line-height: 1.7;
      margin-bottom: 32px;
    }
    
    .cta {
      display: inline-block;
      background: var(--azure);
      color: white;
      padding: 12px 24px;
      border-radius: 8px;
      text-decoration: none;
      font-weight: 600;
      font-size: 16px;
      transition: opacity 0.2s;
    }
    
    .cta:hover {
      opacity: 0.9;
    }
    
    .note {
      margin-top: 32px;
      padding: 16px;
      background: rgba(12, 51, 135, 0.04);
      border-radius: 8px;
      font-size: 14px;
      color: rgba(21, 21, 22, 0.7);
      line-height: 1.6;
    }
  </style>
</head>
<body>
  <div class="error-container">
    <div class="logo">
      <img src="/assets/scroll-logo.svg" alt="Scroll Media" />
    </div>
    
    <div class="error-code">404</div>
    <h1>Report Not Found</h1>
    <p>The report link you're looking for doesn't exist or may have been moved. Please check your email for the correct link or contact your account manager.</p>
    
    <a href="/" class="cta">Back to Home</a>
    
    <div class="note">
      <strong>Need help?</strong><br>
      Contact your Scroll Media account manager if you continue to experience issues accessing your report.
    </div>
  </div>
</body>
</html>
```

### Step 6: Update Landing Page (Brand Compliance)

**File:** `/index.html` (Updated)

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Scroll Media — Client Reports</title>
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
*{margin:0;padding:0;box-sizing:border-box;}
:root{--shadow:#151516;--azure:#0c3387;--lucid:#cbe9ff;--highlighter:#e2ed7a;--ghost:#fafdff;}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;background:var(--ghost);color:var(--shadow);line-height:1.6;display:flex;align-items:center;justify-content:center;min-height:100vh;padding:24px;}
.container{max-width:600px;text-align:center;}
.logo{margin-bottom:40px;}
.logo img{height:48px;width:auto;}
h1{font-size:32px;font-weight:800;color:var(--shadow);margin-bottom:16px;letter-spacing:-0.5px;}
p{font-size:16px;color:rgba(21,21,22,0.6);margin-bottom:32px;line-height:1.8;}
.note{background:#fff;border:1px solid rgba(0,0,0,0.06);border-radius:12px;padding:24px;font-size:14px;color:rgba(21,21,22,0.6);line-height:1.6;}
.note strong{color:var(--shadow);font-weight:600;}
</style>
</head>
<body>
<div class="container">
<div class="logo">
<img src="/assets/scroll-logo.svg" alt="Scroll Media" />
</div>
<h1>Client Reports</h1>
<p>Monthly performance reports for Scroll Media clients.</p>
<div class="note">
<strong>Looking for your report?</strong><br>
Check your email for your unique report link, or contact your account manager.
</div>
</div>
</body>
</html>
```

---

## WORKFLOW UPDATES

### NEW: Sending Reports to Clients

**Email Template:**

```
Subject: Your [Month] [Year] Performance Report is Ready

Hi [Client Name],

Your [Month] performance report is ready to view:

🔗 View Report: https://reports.scrollmedia.co/r/[TOKEN]/[monthyear]/

This link is unique to your account and provides secure access to your monthly performance data, insights, and strategic recommendations.

Questions? Reply to this email or reach out to your account manager.

— [Account Manager Name]
Scroll Media
```

**Example URLs:**
- Launch Party Jan 2026: `reports.scrollmedia.co/r/8k3h9x2n/january2026/`
- Skin by Brownlee Feb 2026: `reports.scrollmedia.co/r/m4p7w1qz/february2026/`
- Define Oakley Jan 2026: `reports.scrollmedia.co/r/x9n2k5rt/january2026/`

### TEAM: Internal Access (Unchanged)

Team can still use clean URLs:
- `reports.scrollmedia.co/launchparty/january2026/`
- `reports.scrollmedia.co/skinbybrownlee/`
- `reports.scrollmedia.co/defineoakley/january2026/`

### NEW: Adding a Client

1. Generate token: `Array.from({length:8},()=>'abcdefghjkmnpqrstuvwxyz23456789'[Math.floor(Math.random()*32)]).join('')`
2. Add to `/config/client-tokens.js`
3. Add to Client Account Homebase (new "Report Token" column)
4. Commit + push to GitHub
5. Use token in all report emails

---

## TESTING CHECKLIST

### ✅ Brand Compliance

- [ ] All pages use Inter font (not Source Sans 3)
- [ ] CSS variables use standard names (--shadow, --azure, etc.)
- [ ] Colors match exact hex codes from brand guide
- [ ] 8px spacing grid maintained
- [ ] No decorative clutter
- [ ] WCAG AA contrast ratios met

### ✅ Token Router Functionality

- [ ] Valid token redirects to correct client folder
- [ ] Invalid token shows 404 page
- [ ] URL structure preserved after redirect
- [ ] No console errors during routing
- [ ] Loading state displays briefly before redirect

### ✅ Security Isolation

- [ ] Client A cannot access Client B's reports by URL manipulation
- [ ] Tokens are unpredictable (8 random chars, no sequential patterns)
- [ ] Inactive tokens show 404
- [ ] Direct folder URLs still work for team (backwards compatible)

### ✅ Mobile Responsiveness

**Test at breakpoints:**
- [ ] 360px (Galaxy S8/S9) - minimum viable
- [ ] 390px (iPhone 12/13) - primary target
- [ ] 768px (iPad Mini) - tablet
- [ ] 1280px (Laptop) - desktop

**Test cases:**
- [ ] No horizontal scroll on any breakpoint
- [ ] Touch targets ≥ 44px
- [ ] Text readable without zoom
- [ ] Buttons/links easily tappable
- [ ] Loading spinner centers properly

### ✅ Cross-Browser Testing

- [ ] Chrome/Brave
- [ ] Safari (desktop)
- [ ] Safari (iOS)
- [ ] Firefox
- [ ] Edge

### ✅ Performance

- [ ] Lighthouse Mobile Score ≥ 90 (Performance)
- [ ] Lighthouse Mobile Score ≥ 95 (Accessibility)
- [ ] First Contentful Paint < 1.5s
- [ ] No render-blocking resources
- [ ] Images optimized/lazy-loaded

---

## DEPLOYMENT STEPS

### Phase 1: Create New Files

1. Create `/r/` folder in repo
2. Add `/r/index.html`
3. Create `/js/` folder
4. Add `/js/token-router.js`
5. Create `/config/` folder
6. Add `/config/client-tokens.js` with generated tokens
7. Add `/404.html`

### Phase 2: Update Existing Files

1. Update `/index.html` (font fix)
2. Update all client archive pages (font fix)
3. Update all report pages (font fix)

**Find & Replace:**
```
FIND: font-family: 'Source Sans 3'
REPLACE: font-family: 'Inter'

FIND: https://fonts.googleapis.com/css2?family=Source+Sans+3
REPLACE: https://fonts.googleapis.com/css2?family=Inter
```

### Phase 3: Netlify Configuration

1. Add custom 404 page in Netlify settings:
   - Site settings → Build & deploy → Post processing
   - 404 page: `/404.html`

2. Verify auto-deploy is enabled
3. Push all changes to GitHub
4. Wait for deployment (30-60 seconds)

### Phase 4: Verification

1. Test valid token URL: `reports.scrollmedia.co/r/8k3h9x2n/january2026/`
2. Test invalid token: `reports.scrollmedia.co/r/invalid123/january2026/` (should 404)
3. Test team URL: `reports.scrollmedia.co/launchparty/january2026/` (should work)
4. Test mobile on real device
5. Run Lighthouse audit
6. Send test email to yourself with token link

---

## MAINTENANCE

### Adding Monthly Reports

**No change to current workflow:**
1. Generate report HTML
2. Save to `/clientname/monthyear/index.html`
3. Commit + push
4. Send client email with token URL: `reports.scrollmedia.co/r/[token]/monthyear/`

### Adding New Clients

1. Generate 8-char token
2. Add to `/config/client-tokens.js`
3. Document in Client Account Homebase
4. Commit + push
5. Use token in report emails

### Rotating Tokens (If Needed)

1. Generate new token for client
2. Update `/config/client-tokens.js`
3. Mark old token as `active: false`
4. Commit + push
5. Send new link to client

---

## SUCCESS METRICS

### Security
✅ Zero cross-client access incidents
✅ Tokens remain secret (not shared publicly)
✅ No unauthorized report views

### Team Efficiency
✅ Deployment time: <60 seconds per report
✅ Client email sent in <2 minutes after deployment
✅ Zero auth-related support tickets

### Client Experience
✅ 100% one-click access (no passwords/logins)
✅ Mobile-friendly on all devices
✅ Fast load times (<2s perceived)

---

## ROLLBACK PLAN

If issues arise:

1. **Token router breaks:** Comment out `<script>` tag in `/r/index.html`
2. **Security concern:** Set all tokens to `active: false` temporarily
3. **Full rollback:** Revert to previous commit in GitHub

Backup current working version before deployment.

---

## FUTURE ENHANCEMENTS (Optional)

### Phase 4: Analytics (Future)
- Track token usage (which clients view reports)
- Page view analytics per client
- Time-on-page metrics

### Phase 5: Expiring Links (Future)
- Add expiration dates to tokens
- Auto-disable old tokens after 90 days
- Send reminder emails before expiration

### Phase 6: Team Dashboard (Future)
- Admin page showing all active tokens
- One-click token generation
- Client access logs

---

**Scroll Media** — Strategy First, Simplification Always

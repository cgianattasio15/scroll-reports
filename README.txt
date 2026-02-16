SCROLL REPORTS - PRO PLAN DEPLOYMENT

✓ Brand Guidelines Compliant
✓ Basic Auth Configured (Pro Plan)
✓ Two-Tier Password System

PASSWORDS CONFIGURED:
Landing Page: scrollteam / scrollteam2026
Skin by Brownlee: skinbybrownlee / skinbybrownlee
Launch Party: launchparty / launchparty
Define Oakley: defineoakley / defineoakley

DEPLOYMENT STEPS:
1. Drag this entire folder to Netlify
2. Wait for deployment (~30 seconds)
3. Test password protection:
   - Visit site URL
   - Should prompt for username/password
   - Enter: scrollteam / scrollteam2026
   - Should see client directory

4. Test client folder protection:
   - Click any client
   - Should prompt for new password
   - Enter client-specific password
   - Should see archive page

IMPORTANT:
- Basic Auth requires Netlify Pro plan ($19/month)
- _headers file format is critical (no extra spaces/lines)
- Password protection may take 1-2 minutes to activate after deploy
- Test in incognito window to avoid cached auth

NEXT STEPS:
1. Deploy this folder
2. Set up custom domain (reports.scrollmedia.co)
3. Generate first monthly report
4. Add to client folder as monthyear/index.html

See REPORTS_SYSTEM_SETUP_FINAL.md for full workflow.

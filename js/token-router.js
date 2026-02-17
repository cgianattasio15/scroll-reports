/**
 * Token-Based URL Router for Scroll Reports
 * 
 * Routes client-specific token URLs to actual report paths
 * Example: /r/r8kh3m2p/january2026/ → /launchparty/january2026/
 */

(function() {
  'use strict';

  // Token registry (must match /config/client-tokens.js)
  const CLIENT_TOKENS = {
    'r8kh3m2p': { clientFolder: 'launchparty', clientName: 'Launch Party', active: true },
    't4nw9x5q': { clientFolder: 'skinbybrownlee', clientName: 'Skin by Brownlee', active: true },
    'v7bj2k6n': { clientFolder: 'defineoakley', clientName: 'Define Oakley', active: true }
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

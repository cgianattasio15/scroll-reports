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
  'r8kh3m2p': {
    clientFolder: 'launchparty',
    clientName: 'Launch Party',
    created: '2026-02-16',
    active: true
  },
  
  // Skin by Brownlee (Med Spa)
  't4nw9x5q': {
    clientFolder: 'skinbybrownlee',
    clientName: 'Skin by Brownlee',
    created: '2026-02-16',
    active: true
  },
  
  // Define Oakley (Boutique Fitness)
  'v7bj2k6n': {
    clientFolder: 'defineoakley',
    clientName: 'Define Oakley',
    created: '2026-02-16',
    active: true
  }
  
  // ADD NEW CLIENTS HERE
  // Generate tokens using:
  // Array.from({length:8},()=>'abcdefghjkmnpqrstuvwxyz23456789'[Math.floor(Math.random()*32)]).join('')
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { CLIENT_TOKENS };
}

/* ──────────────────────────────────────────────────────────────
   Scroll Media — reports.scrollmedia.co access-code gate (Tier 3)
   Client-side gate. Replicates the proposal access-code pattern.

   Per-page config (set BEFORE this script loads):
     window.SCROLL_GATE = {
       slug:  'laneandkate',          // localStorage scope (one per client)
       code:  'laneandkate.reports',  // access code, case-insensitive
       title: 'Private report',       // optional heading override
       sub:   '...',                  // optional sub-copy override
       button:'View report'           // optional button-label override
     };

   One code per client unlocks every report + archive page for that
   client. Auth persists in localStorage scoped to the client slug,
   so a client never re-enters the code across their own pages, and
   one client's code never unlocks another client's pages.
   ────────────────────────────────────────────────────────────── */
(function () {
  var cfg = window.SCROLL_GATE || {};
  var SLUG = cfg.slug || 'reports';
  var CODE = (cfg.code || '').toLowerCase();
  var KEY = 'scroll_reports_' + SLUG;
  var TITLE = cfg.title || 'Private report';
  var SUB = cfg.sub || 'This report is private. Enter your access code to continue.';
  var BTN = cfg.button || 'View report';

  // Already unlocked on this device → render the page, do nothing.
  try {
    if (window.localStorage && localStorage.getItem(KEY) === '1') return;
  } catch (e) { /* localStorage blocked — fall through and show gate */ }

  // Hide page content immediately (no flash of the report behind the gate).
  document.documentElement.classList.add('sm-gate-locked');

  var css = ''
    + 'html.sm-gate-locked body{visibility:hidden!important}'
    + '#sm-gate{visibility:visible;position:fixed;inset:0;z-index:99999;'
    +   'background:#f7f8fc;display:flex;align-items:center;justify-content:center;'
    +   'padding:24px;font-family:"Source Sans 3",system-ui,-apple-system,sans-serif}'
    + '.sm-gate-card{background:#fff;border:1px solid rgba(21,21,22,.09);border-radius:16px;'
    +   'padding:44px 36px;width:100%;max-width:400px;text-align:center;'
    +   'box-shadow:0 8px 32px rgba(14,51,135,.10)}'
    + '.sm-gate-logo{height:30px;width:auto;margin:0 auto 26px;display:block}'
    + '.sm-gate-title{font-size:22px;font-weight:800;letter-spacing:-.02em;color:#151516;margin:0 0 6px}'
    + '.sm-gate-sub{font-size:14px;line-height:1.5;color:#6b7280;margin:0 0 26px}'
    + '.sm-gate-input-wrap{position:relative;margin-bottom:12px}'
    + '.sm-gate-input{width:100%;background:#f2f3f4;border:1.5px solid rgba(21,21,22,.12);'
    +   'border-radius:8px;padding:13px 48px 13px 16px;font-size:16px;font-family:inherit;'
    +   'color:#151516;outline:none;transition:border-color .2s;letter-spacing:.04em}'
    + '.sm-gate-input:focus{border-color:#0e3387}'
    + '.sm-gate-input::placeholder{letter-spacing:0;color:#9aa0aa}'
    + '.sm-gate-toggle{position:absolute;right:10px;top:50%;transform:translateY(-50%);'
    +   'background:none;border:none;cursor:pointer;color:#9aa0aa;padding:6px;'
    +   'display:flex;align-items:center;min-width:44px;min-height:44px;justify-content:center}'
    + '.sm-gate-btn{width:100%;background:#0e3387;color:#fff;border:none;border-radius:8px;'
    +   'padding:14px;font-size:15px;font-weight:700;font-family:inherit;cursor:pointer;'
    +   'transition:background .2s,transform .1s;min-height:48px}'
    + '.sm-gate-btn:hover{background:#0a276a}'
    + '.sm-gate-btn:active{transform:scale(.99)}'
    + '.sm-gate-error{font-size:13px;color:#dc2626;margin-top:12px;min-height:16px;'
    +   'opacity:0;transition:opacity .2s}'
    + '.sm-gate-error.visible{opacity:1}'
    + '.sm-gate-forgot{display:inline-block;margin-top:18px;font-size:13px;color:#6b7280;'
    +   'text-decoration:none;border-bottom:1px solid rgba(21,21,22,.18);padding-bottom:1px}'
    + '.sm-gate-forgot:hover{color:#0e3387;border-color:#0e3387}'
    + '@media(max-width:420px){.sm-gate-card{padding:36px 22px}}';

  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  var eyeOpen = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>';
  var eyeOff = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>';

  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  var gate = document.createElement('div');
  gate.id = 'sm-gate';
  gate.innerHTML = ''
    + '<div class="sm-gate-card">'
    +   '<img class="sm-gate-logo" src="/assets/scroll-logo-navy.png" alt="Scroll Media" />'
    +   '<h1 class="sm-gate-title">' + esc(TITLE) + '</h1>'
    +   '<p class="sm-gate-sub">' + esc(SUB) + '</p>'
    +   '<div class="sm-gate-input-wrap">'
    +     '<input class="sm-gate-input" id="sm-gate-input" type="password" placeholder="Access code" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" />'
    +     '<button class="sm-gate-toggle" id="sm-gate-toggle" type="button" aria-label="Show or hide access code">' + eyeOpen + '</button>'
    +   '</div>'
    +   '<button class="sm-gate-btn" id="sm-gate-btn" type="button">' + esc(BTN) + '</button>'
    +   '<div class="sm-gate-error" id="sm-gate-error">That access code is not right. Try again.</div>'
    +   '<a class="sm-gate-forgot" href="mailto:chase@getscrollmedia.com?subject=Reports%20access%20code">Forgot your code?</a>'
    + '</div>';

  function mount() {
    document.body.appendChild(gate);
    var inp = document.getElementById('sm-gate-input');
    var btn = document.getElementById('sm-gate-btn');
    var err = document.getElementById('sm-gate-error');
    var tog = document.getElementById('sm-gate-toggle');
    var errTimer;

    inp.focus();

    function unlock() {
      if (inp.value.trim().toLowerCase() === CODE && CODE !== '') {
        try { localStorage.setItem(KEY, '1'); } catch (e) {}
        document.documentElement.classList.remove('sm-gate-locked');
        gate.style.opacity = '0';
        gate.style.transition = 'opacity .3s';
        setTimeout(function () { if (gate.parentNode) gate.parentNode.removeChild(gate); }, 300);
      } else {
        err.classList.add('visible');
        inp.style.borderColor = '#dc2626';
        clearTimeout(errTimer);
        errTimer = setTimeout(function () {
          err.classList.remove('visible');
          inp.style.borderColor = '';
        }, 3000);
      }
    }

    btn.addEventListener('click', unlock);
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') unlock(); });
    tog.addEventListener('click', function () {
      var isPw = inp.type === 'password';
      inp.type = isPw ? 'text' : 'password';
      tog.innerHTML = isPw ? eyeOff : eyeOpen;
      inp.focus();
    });
  }

  if (document.body) {
    mount();
  } else {
    document.addEventListener('DOMContentLoaded', mount);
  }
})();

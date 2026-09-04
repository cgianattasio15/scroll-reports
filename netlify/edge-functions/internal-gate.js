// Server-side gate for the internal reports dashboard on reports.scrollmedia.co (root only).
// Same function and same env var name as scroll-media-tools; per-client report pages keep
// their own per-client access-code gate (access-gate.js) and are NOT covered here.
// Replaces the client-side JavaScript password overlay (sessionStorage 'sm_tools_auth'),
// which compared a plaintext string in the page source and was defeated by view-source.
// Added 2026-09-04 (security_protocol INC-2026-09-04-01 follow-up).
//
// The password lives ONLY in the Netlify env var INTERNAL_GATE_PASSWORD (site settings,
// marked secret). Rotate it there; nothing in this repo changes on rotation.
// Fail closed: if the env var is unset the gated paths return 503, never open.

function safeEqual(a, b) {
  if (typeof a !== "string" || typeof b !== "string") return false;
  const enc = new TextEncoder();
  const x = enc.encode(a), y = enc.encode(b);
  let diff = x.length ^ y.length;
  const n = Math.max(x.length, y.length);
  for (let i = 0; i < n; i++) diff |= (x[i % x.length] ?? 0) ^ (y[i % y.length] ?? 0);
  return diff === 0;
}

export default async (request, context) => {
  const expected = Netlify.env.get("INTERNAL_GATE_PASSWORD");
  if (!expected) {
    return new Response("Scroll Media internal gate is not configured.", {
      status: 503, headers: { "Cache-Control": "no-store" },
    });
  }
  const auth = request.headers.get("authorization") || "";
  if (auth.startsWith("Basic ")) {
    try {
      const decoded = atob(auth.slice(6));
      const i = decoded.indexOf(":");
      const supplied = i >= 0 ? decoded.slice(i + 1) : decoded;
      if (safeEqual(supplied, expected)) {
        const res = await context.next();
        res.headers.set("Cache-Control", "private, no-store");
        return res;
      }
    } catch (_) { /* malformed header falls through to 401 */ }
  }
  return new Response("Scroll Media internal. Sign in required.", {
    status: 401,
    headers: {
      "WWW-Authenticate": 'Basic realm="Scroll Media internal", charset="UTF-8"',
      "Cache-Control": "no-store",
    },
  });
};

// Exact root only ("/" does not match "/foo"); the wildcards cover the internal sections.
// Public pages on this site (lead magnets, /scroll-system/, /thanks, client Homebases with
// their own per-client gate, token-gated playbooks) are deliberately NOT listed.
export const config = {
  path: ["/", "/index.html"],
  cache: "manual",
};

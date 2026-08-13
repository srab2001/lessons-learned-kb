// KB access control — two valid entry paths:
//   1. SA proxy: sends x-kb-token header with shared secret
//   2. Direct browser: has a valid kb_session cookie (set by /api/auth/callback)
//
// Everything else redirects to the KB's own Google sign-in.

export const config = { matcher: "/:path*" };

const KB_SIGNIN = "/api/auth/signin";
const AUTH_PREFIX = "/api/auth/";
const COOKIE_NAME = "kb_session";

export default async function middleware(request) {
  const { pathname } = new URL(request.url);

  // Auth API routes are always public
  if (pathname.startsWith(AUTH_PREFIX)) return;

  // SA proxy: shared secret in request header
  const expected = process.env.KB_ACCESS_TOKEN;
  if (expected) {
    const provided = request.headers.get("x-kb-token");
    if (provided === expected) return;
  }

  // Direct browser: parse cookie header manually (plain Request, not NextRequest)
  const cookieHeader = request.headers.get("cookie") || "";
  const cookieValue = parseCookie(cookieHeader, COOKIE_NAME);
  if (cookieValue && (await isValidSession(cookieValue))) return;

  // No valid auth — redirect to KB sign-in
  return Response.redirect(new URL(KB_SIGNIN, request.url), 302);
}

function parseCookie(header, name) {
  for (const part of header.split(";")) {
    const [k, ...rest] = part.trim().split("=");
    if (k.trim() === name) return rest.join("=").trim();
  }
  return null;
}

async function isValidSession(cookieValue) {
  try {
    const dot = cookieValue.lastIndexOf(".");
    if (dot === -1) return false;
    const payload = cookieValue.slice(0, dot);
    const sig = cookieValue.slice(dot + 1);

    const secret = process.env.AUTH_SECRET;
    if (!secret) return false;

    const key = await crypto.subtle.importKey(
      "raw",
      new TextEncoder().encode(secret),
      { name: "HMAC", hash: "SHA-256" },
      false,
      ["verify"],
    );

    const sigBytes = hexToBytes(sig);
    if (!sigBytes) return false;

    const valid = await crypto.subtle.verify(
      "HMAC",
      key,
      sigBytes,
      new TextEncoder().encode(payload),
    );
    if (!valid) return false;

    // base64url → base64 before decoding
    const base64 = payload.replace(/-/g, "+").replace(/_/g, "/");
    const padded = base64 + "=".repeat((4 - (base64.length % 4)) % 4);
    const data = JSON.parse(atob(padded));
    return typeof data.exp === "number" && data.exp > Date.now();
  } catch {
    return false;
  }
}

function hexToBytes(hex) {
  if (!hex || hex.length % 2 !== 0) return null;
  const bytes = new Uint8Array(hex.length / 2);
  for (let i = 0; i < hex.length; i += 2) {
    bytes[i / 2] = parseInt(hex.slice(i, i + 2), 16);
  }
  return bytes;
}

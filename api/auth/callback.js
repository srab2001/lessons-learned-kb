import { createHmac } from "node:crypto";

const SESSION_DAYS = 7;
const COOKIE_NAME = "kb_session";

// Exchange Google auth code → email → signed session cookie.
export default async function handler(req, res) {
  const base = process.env.KB_BASE_URL || "https://lessons-learned-kb.vercel.app";
  const { code, error } = req.query;

  if (error || !code) {
    return res.status(400).send(`<h2>Sign-in failed: ${error || "missing code"}</h2>`);
  }

  // Exchange code for tokens
  let idToken;
  try {
    const tokenRes = await fetch("https://oauth2.googleapis.com/token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        code,
        client_id: process.env.GOOGLE_CLIENT_ID,
        client_secret: process.env.GOOGLE_CLIENT_SECRET,
        redirect_uri: `${base}/api/auth/callback`,
        grant_type: "authorization_code",
      }),
    });
    const data = await tokenRes.json();
    if (!data.id_token) throw new Error(data.error_description || "no id_token");
    idToken = data.id_token;
  } catch (err) {
    return res.status(500).send(`<h2>Token exchange failed: ${err.message}</h2>`);
  }

  // Decode JWT payload (we trust Google's TLS — skip signature verification)
  let email, name;
  try {
    const payload = JSON.parse(Buffer.from(idToken.split(".")[1], "base64url").toString());
    email = payload.email?.toLowerCase();
    name = payload.name;
    if (!email) throw new Error("no email in token");
  } catch (err) {
    return res.status(400).send(`<h2>Invalid token: ${err.message}</h2>`);
  }

  // Optional allow-list (ALLOWED_KB_EMAILS env var, comma-separated).
  // If unset, any Google-authenticated user is allowed.
  const allowed = (process.env.ALLOWED_KB_EMAILS || "")
    .split(",")
    .map((e) => e.trim().toLowerCase())
    .filter(Boolean);
  if (allowed.length > 0 && !allowed.includes(email)) {
    return res.status(403).send(`
      <html><body style="font-family:system-ui;text-align:center;padding:4rem">
        <h2>Access denied</h2>
        <p>${email} is not on the approved list. Contact the KB administrator.</p>
      </body></html>
    `);
  }

  // Build signed cookie: base64(payload).hmac
  const exp = Date.now() + SESSION_DAYS * 86400 * 1000;
  const payloadStr = Buffer.from(JSON.stringify({ email, name, exp })).toString("base64url");
  const sig = createHmac("sha256", process.env.AUTH_SECRET || "fallback-secret")
    .update(payloadStr)
    .digest("hex");
  const cookieValue = `${payloadStr}.${sig}`;

  const cookieOpts = [
    `${COOKIE_NAME}=${cookieValue}`,
    `Path=/`,
    `Max-Age=${SESSION_DAYS * 86400}`,
    `HttpOnly`,
    `SameSite=Lax`,
    `Secure`,
  ].join("; ");

  res.setHeader("Set-Cookie", cookieOpts);
  res.setHeader("Location", "/");
  res.status(302).end();
}

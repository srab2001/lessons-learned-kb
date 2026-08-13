// Redirect to Google OAuth — entry point for direct KB sign-in.
export default function handler(req, res) {
  const base = process.env.KB_BASE_URL || "https://lessons-learned-kb.vercel.app";
  const params = new URLSearchParams({
    client_id: process.env.GOOGLE_CLIENT_ID,
    redirect_uri: `${base}/api/auth/callback`,
    response_type: "code",
    scope: "openid email profile",
    access_type: "online",
  });
  res.setHeader("Location", `https://accounts.google.com/o/oauth2/v2/auth?${params}`);
  res.status(302).end();
}

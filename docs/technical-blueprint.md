---
title: "Lessons Learned KB — Technical Blueprint"
sources: []
source_count: 0
as_of_date: "2026-08-13"
last_compiled: "2026-08-13"
lifecycle: active
confidence: high
sensitivity: internal
lesson_type: []
lifecycle_history:
  - date: "2026-08-13"
    from: ""
    to: active
    reason: "written for this KB after the proposal-intelligence-kb bootstrap; the source template's technical-blueprint.md described a different app's Neon/RAG integration and was not ported (see docs/design.md)"
---

# Lessons Learned KB — Technical Blueprint

This is the request-by-request, pipeline-by-pipeline companion to `docs/design.md`. `design.md` says what each component is for; this says how they actually connect, so a maintainer can trace a bug or a build failure to the right file without re-deriving the system from scratch.

## Read/write paths through the app

There are exactly two things a visitor can do: sign in, and view a wiki page. Everything else is build-time.

### 1. Sign-in

```
Browser → GET /                          → middleware.js: no session cookie, no x-kb-token
                                            → 302 → /api/auth/signin
GET /api/auth/signin (api/auth/signin.js) → 302 → accounts.google.com/o/oauth2/v2/auth
                                              (client_id, redirect_uri=/api/auth/callback, scope=openid email profile)
User approves in Google's consent screen
Google → GET /api/auth/callback?code=... (api/auth/callback.js)
  1. POST code to oauth2.googleapis.com/token with GOOGLE_CLIENT_ID/SECRET → id_token
  2. Decode the JWT payload directly (no signature check — Google's TLS is the trust boundary)
  3. Check email against ALLOWED_KB_EMAILS (comma-separated); empty list = allow any Google account
  4. Build kb_session = base64url(JSON{email,name,exp}) + "." + HMAC-SHA256(AUTH_SECRET)
  5. Set-Cookie: kb_session=...; HttpOnly; Secure; SameSite=Lax; Max-Age=7 days
  6. 302 → /
```

### 2. Every subsequent request

`middleware.js` runs on every path (`matcher: "/:path*"`) except `/api/auth/*`, in this order:

1. **Shared-secret bypass** — if `KB_ACCESS_TOKEN` is set and the request carries a matching `x-kb-token` header, allow through unauthenticated. This is the only path a server-to-server caller (e.g., a future companion app) can use; there is no OAuth client-credentials flow.
2. **Session cookie** — parse `kb_session` from the raw `Cookie` header (middleware runs on a plain `Request`, not a framework request object, so cookie parsing is hand-rolled — see `parseCookie()`), then verify the HMAC signature and `exp` timestamp with the Web Crypto `subtle` API (`isValidSession()`).
3. **Neither** — 302 to `/api/auth/signin`.

There is no server-side session store. The cookie *is* the session; revoking access means removing an email from `ALLOWED_KB_EMAILS` (existing cookies for that email stay valid until they expire, up to 7 days) or rotating `AUTH_SECRET` (invalidates every outstanding session at once).

## Content pipeline: context/ → docs/ → wiki/site/

```
context/<folder>/new-file.md  (human adds; updates manifest.yaml)
        │
        ▼
KB synthesis session — either:
  (a) a maintainer-run Claude session (agent/agents.md workflow: branch → PR → review → merge), or
  (b) .github/workflows/kb-synthesis.yml, workflow_dispatch, commits straight to main (no PR)
        │
        ▼
docs/<section>/<slug>.md created/updated (frontmatter + footnoted claims, per CLAUDE.md)
docs/_kb-index.yaml catalog entry added/updated
        │
        ▼
For each NEW docs/ page: wiki/mkdocs.yml nav gets an entry, and
wiki/docs/<section>/<slug>.md is created as a relative symlink to ../../docs/<section>/<slug>.md
(single source of truth stays in docs/; the wiki tree never forks a copy)
        │
        ▼
Push to main touching docs/** or wiki/** → .github/workflows/build-wiki.yml:
  1. pip install -r wiki/requirements.txt
  2. cd wiki && mkdocs build            (NOT --strict — see "Build warnings" below)
  3. commit wiki/site/ back to main ("chore: rebuild wiki site [skip ci]")
  4. vercel deploy --prod --cwd wiki/site
```

`wiki/site/` is a committed build artifact, not a Vercel build step — `vercel.json` sets `framework: null`, `buildCommand: ""`, `outputDirectory: "wiki/site"`, so Vercel just serves whatever the GitHub Action last committed there. This means the wiki is always exactly one CI run behind `main`, and a broken `mkdocs build` blocks the site update but does not take the *previous* deployed site down.

## Build-time sensitivity enforcement

`wiki/hooks/sensitivity_filter.py` runs on every page during `mkdocs build` and replaces the content of any page whose frontmatter `sensitivity` is not `public` with a generic "Access Restricted" notice — regardless of what `wiki/mkdocs.yml`'s `nav` references. This is explicitly defense-in-depth (see the hook's own docstring): the nav is expected to only ever list public pages, and the hook is what actually enforces that at build time.

**Scope of the rule:** this applies to individual KB content pages (`docs/<section>/<slug>.md` and their `wiki/docs/<section>/<slug>.md` symlinks) — e.g., a specific incident review is `restricted` by default per `structure.md`. It does **not** apply to the seven section *index* pages (`wiki/docs/<section>/index.md`), which are static nav-tree landing text with no client- or incident-specific content and should stay `sensitivity: public` across all seven sections. Three of them (`anti-patterns`, `client-context`, `incident-reviews`) were incorrectly left at `sensitivity: internal` from the initial bootstrap, which made `mkdocs build --strict` flag them and made the live pages show "Access Restricted" instead of their actual (harmless) description text — fixed 2026-08-13. If a future maintainer adds real sensitive detail directly to a section `index.md` instead of a dedicated slug page, flip it back to `internal`/`restricted` at that point, not before.

`wiki/hooks/lifecycle_banners.py` is the sibling hook — it injects a visible banner for non-`active` lifecycle states (draft/stale/contradicted/archived) so a reader never mistakes a draft or stale page for reviewed content.

## Deployment topology

- **One Vercel project**, static output only (see above). No `DATABASE_URL`, no serverless runtime beyond the two auth routes in `api/auth/`.
- **GitHub Actions** owns the only mutation path to `main`'s `wiki/site/` — there is no manual `mkdocs gh-deploy` or local publish step.
- **Two independent triggers** can update KB content: a human-reviewed PR (default), or `kb-synthesis.yml`'s `workflow_dispatch` for direct-to-main synthesis of a single newly-added context file. Both eventually converge on the same `build-wiki.yml` rebuild.

## Local testing

```bash
pip install -r wiki/requirements.txt
cd wiki && mkdocs build        # matches CI exactly (no --strict)
# mkdocs build --strict will additionally fail on any non-public section index page —
# useful as a lint, but do not add --strict to build-wiki.yml without first auditing
# every wiki/docs/**/index.md sensitivity field, or a legitimately-restricted content
# page will break the production build instead of just blanking itself.
```

There is no way to locally exercise the Google OAuth flow without real `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET` values and a redirect URI Google will accept (`KB_BASE_URL` + `/api/auth/callback`, registered in the Google Cloud OAuth client's Authorized redirect URIs) — see `.env.example` for the full variable list.

## What this document is not

This is not a KB content page — it is not tracked in `docs/_kb-index.yaml`, is not subject to `structure.md`'s section rules, and is not published to the wiki nav (same treatment as `docs/design.md`). It documents the repo's own engineering, not a lesson learned from a delivery engagement.

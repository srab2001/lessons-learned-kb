---
title: "Anti-Pattern: ESM-Only Dependency Crashes a Vercel Serverless Function After a Clean Build"
sources:
  - context/engagement-notes/consolidated-lessons-learned-2026-08-13.md
  - context/anti-patterns-raw/raven-demo-lessons-learned.md
source_count: 2
as_of_date: "2026-08-13"
last_compiled: "2026-08-13"
lifecycle: draft
confidence: low
sensitivity: internal
lesson_type: [technical]
lifecycle_history:
  - date: "2026-08-13"
    from: ""
    to: draft
    reason: "initial synthesis from consolidated-lessons-learned-2026-08-13.md"
  - date: "2026-08-13"
    from: draft
    to: draft
    reason: "attribution resolved and enriched via raven_demo's own lessons-learned doc (context/anti-patterns-raw/raven-demo-lessons-learned.md), which is the detailed original this incident was summarized from -- not independent corroboration, so confidence stays low despite the second source"
---

# Anti-Pattern: ESM-Only Dependency Crashes a Vercel Serverless Function After a Clean Build

**Attribution:** [`raven_demo`](https://github.com/srab2001/raven_demo) — encountered while building Google OAuth + admin-approval gating for three demo apps.[^4] Previously listed as an attribution gap in this page; resolved once the project's own, more detailed lessons-learned document was located and ingested.

> **Sensitivity note:** the source file this page now also draws from (`context/anti-patterns-raw/raven-demo-lessons-learned.md`) defaults to `sensitivity: restricted` per its folder — but its actual content is purely technical debugging detail (no personnel, client, or dispute material) and includes only public GitHub links. Per `structure.md`'s promotion pattern for abstracted lessons, this page stays `internal` rather than inheriting `restricted`.

## What the pattern looks like

A serverless function builds and deploys successfully ("Ready" status in Vercel), but crashes at request time. The build succeeding gives false confidence that the deployed function actually works.

## Failure mode / symptom

After shipping the Google OAuth + admin-approval feature, production returned `FUNCTION_INVOCATION_FAILED` — Vercel's generic function-crashed page — on `/api/auth/google/start` and related `/api/*` routes, with an error log of `Cannot use import statement outside a module`.[^1][^4] Three layered root causes were identified: (1) a database client module (`lib/db.ts`) threw an error at module-import time when `DATABASE_URL` was missing; (2) the corresponding API route had no `try`/`catch` wrapper around its initialization code (specifically, around `buildGoogleAuthUrl()`, which throws if `GOOGLE_CLIENT_ID` is missing) so the error was unhandled;[^2][^4] and (3) the actual proximate cause — the `jose` JWT library is ESM-only, and Vercel's Node-function bundler was not reliably propagating the `"type": "module"` signal from `package.json` into the runtime context.[^1][^4]

**A documented false-fix signal:** adding `"type": "module"` to `package.json` appeared to fix the problem — the deploy went out cleanly — but on the next fresh redeploy with no build cache, the identical crash came back. The source calls this out explicitly as a diagnostic heuristic: *a "fix" that works once and then reappears means the config change isn't the actual lever.*[^1]

## Root cause categories to check together

This incident is really two related root causes compounding each other, documented in two different sections of the source:

- Lazy vs. eager initialization: the database client was constructed at module import time rather than on first use, so any missing configuration threw before the handler even ran.[^3]
- Missing error handling: the route handler had no `try`/`catch` around initialization or request logic, so any thrown error became an unhandled `FUNCTION_INVOCATION_FAILED` instead of a clean error response.[^2]
- The ESM-only dependency itself, which is bundler-format-sensitive in a way that ordinary CommonJS/ESM interop configuration did not reliably fix.[^1]

## What to do instead

1. Treat "Ready" build status and "the deployed function actually works at request time" as two separate things to verify — a clean build does not confirm runtime behavior.[^1][^4]
2. If an ESM-only dependency is implicated in a bundler-format crash, don't keep tuning module-format config — replace the dependency. In this case, `lib/jwt.ts` was rewritten to use only the Web Crypto API (`crypto.subtle`, `TextEncoder`/`TextDecoder`, `btoa`/`atob` — zero third-party imports, zero Node-specific APIs) instead of the `jose` library; `tsconfig.json`'s `"module"` was set back to `CommonJS` and `"type": "module"` reverted out of `package.json`, restoring one unambiguous module format end to end.[^1][^4]
3. Prefer Web APIs available in both Node.js and Edge Runtime (`crypto.subtle`, `fetch`, `TextEncoder`) over Node-specific or ESM-only libraries in functions that might run in either context; avoid `node:*` imports specifically in code that must also work in Edge Middleware (the fix above also had to run in `middleware.ts`'s Edge Runtime, which has no `node:crypto`).[^1][^4]
4. To verify a suspected module-format issue directly, don't reason about bundler behavior abstractly — compile with `tsc -p tsconfig.json --outDir <tmp>` and inspect the actual emitted JS for `require()`/`exports.default` versus `import`/`export` statements.[^1][^4]
5. Lazy-initialize database (and similar) clients inside the function body, not at module load time, so a missing environment variable fails inside a `try`/`catch` rather than at import time.[^3]
6. Wrap all API handler bodies in error handling (directly or via a shared helper) so an unexpected throw returns a clean error response instead of an unhandled invocation failure.[^2]
7. Verify the fix at more than one layer, not just a green deploy: unit-test the replacement code directly (e.g., sign/verify roundtrip, wrong-secret rejection, tampered- and expired-token rejection, and — for a JWT/OIDC fix specifically — the full ID-token verification path against a locally generated keypair with `fetch` stubbed to serve a fake JWKS), and confirm the real endpoint returns its expected success response (a `302`, not a `500`) in production afterward.[^4]
8. **Two Vercel projects can track the same GitHub repo with completely separate environment variables and separate "production" branch bindings.** Before concluding an env var is missing or a fix didn't ship, confirm which project's domain is actually being tested. The source lists this as a general takeaway from the same feature-building effort as this incident, without stating that it was specifically part of this incident's own debugging — recorded here at the same confidence level as the rest of this page, not as a confirmed detail of this specific crash.[^4]

> **Gap:** No metric is available for how long this was live in production, how many requests failed, or how it was first detected — only the debugging narrative and code-level resolution.

---

[^1]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Deployment & Vercel > Issue: ESM-Only Dependency Crashes in Vercel Serverless.
[^2]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — API & Backend > Issue: Missing Try/Catch on API Routes.
[^3]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — API & Backend > Issue: Lazy Initialization of Database Clients.
[^4]: context/anti-patterns-raw/raven-demo-lessons-learned.md — "Vercel Node function crash: ESM-only dependency survives a `"type": "module"` fix" (full incident) and "Source" section (repo attribution).

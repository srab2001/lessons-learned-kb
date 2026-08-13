---
title: "Anti-Pattern: ESM-Only Dependency Crashes a Vercel Serverless Function After a Clean Build"
sources:
  - context/engagement-notes/consolidated-lessons-learned-2026-08-13.md
source_count: 1
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
---

# Anti-Pattern: ESM-Only Dependency Crashes a Vercel Serverless Function After a Clean Build

> **Attribution gap:** The source does not name which of the three repositories (`meal_planner_app`, `travel-deal-finder`, `raven_demo`) this incident occurred in — it is documented under general "Deployment & Vercel" and "API & Backend" headings with no project label or contextual naming clue (no fitness/meal-planner URLs, no travel/flight domain terms, no `raven_demo` reference). It is presented here as a cross-project pattern rather than attributed to a specific project retrospective, per this session's scoping guidance to not guess repo attribution without a stated or contextual basis.

## What the pattern looks like

A serverless function builds and deploys successfully ("Ready" status in Vercel), but crashes at request time. The build succeeding gives false confidence that the deployed function actually works.

## Failure mode / symptom

After shipping Google OAuth, production returned `FUNCTION_INVOCATION_FAILED` on auth routes, with an error log of `Cannot use import statement outside a module`.[^1] Three layered root causes were identified: (1) a database client module (`lib/db.ts`) threw an error at module-import time when `DATABASE_URL` was missing; (2) the corresponding API route (`/api/auth/google/start`) had no `try`/`catch` wrapper around that initialization code, so the error was unhandled;[^2] and (3) the actual proximate cause — the `jose` JWT library is ESM-only, and Vercel's Node-function bundler was not reliably propagating the `"type": "module"` signal from `package.json` into the runtime context.[^1]

**A documented false-fix signal:** adding `"type": "module"` to `package.json` appeared to fix the problem — the deploy went out cleanly — but on the next fresh redeploy with no build cache, the identical crash came back. The source calls this out explicitly as a diagnostic heuristic: *a "fix" that works once and then reappears means the config change isn't the actual lever.*[^1]

## Root cause categories to check together

This incident is really two related root causes compounding each other, documented in two different sections of the source:

- Lazy vs. eager initialization: the database client was constructed at module import time rather than on first use, so any missing configuration threw before the handler even ran.[^3]
- Missing error handling: the route handler had no `try`/`catch` around initialization or request logic, so any thrown error became an unhandled `FUNCTION_INVOCATION_FAILED` instead of a clean error response.[^2]
- The ESM-only dependency itself, which is bundler-format-sensitive in a way that ordinary CommonJS/ESM interop configuration did not reliably fix.[^1]

## What to do instead

1. Treat "Ready" build status and "the deployed function actually works at request time" as two separate things to verify — a clean build does not confirm runtime behavior.[^1]
2. If an ESM-only dependency is implicated in a bundler-format crash, don't keep tuning module-format config — replace the dependency. In this case, `lib/jwt.ts` was rewritten to use the Web Crypto API (`crypto.subtle`) instead of the `jose` library, which behaves identically under CommonJS, ESM, and Edge Runtime and has zero dependency on bundler module-format handling.[^1]
3. Prefer Web APIs available in both Node.js and Edge Runtime (`crypto.subtle`, `fetch`, `TextEncoder`) over Node-specific or ESM-only libraries in functions that might run in either context; avoid `node:*` imports specifically in code that must also work in Edge Middleware.[^1]
4. To verify a suspected module-format issue directly, compile with `tsc --outDir <tmp>` and inspect the actual emitted JavaScript rather than reasoning about bundler behavior abstractly.[^1]
5. Lazy-initialize database (and similar) clients inside the function body, not at module load time, so a missing environment variable fails inside a `try`/`catch` rather than at import time.[^3]
6. Wrap all API handler bodies in error handling (directly or via a shared helper) so an unexpected throw returns a clean error response instead of an unhandled invocation failure.[^2]

> **Gap:** No metric is available for how long this was live in production, how many requests failed, or how it was first detected — only the debugging narrative and code-level resolution.

---

[^1]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Deployment & Vercel > Issue: ESM-Only Dependency Crashes in Vercel Serverless.
[^2]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — API & Backend > Issue: Missing Try/Catch on API Routes.
[^3]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — API & Backend > Issue: Lazy Initialization of Database Clients.

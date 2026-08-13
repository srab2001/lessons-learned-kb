---
title: "Meal Planner App — Project Retrospective"
sources:
  - context/engagement-notes/consolidated-lessons-learned-2026-08-13.md
source_count: 1
as_of_date: "2026-08-13"
last_compiled: "2026-08-13"
lifecycle: draft
confidence: low
sensitivity: internal
lesson_type: [technical, process]
lifecycle_history:
  - date: "2026-08-13"
    from: ""
    to: draft
    reason: "initial synthesis from consolidated-lessons-learned-2026-08-13.md"
---

# Meal Planner App — Project Retrospective

> **Framing note:** The source document lists `meal_planner_app` as one of three repositories it consolidates debugging lessons from, but the document reads as a personal/practice project rather than an Ad Hoc client engagement — there is no client name, contract period, or engagement value anywhere in the source.[^1] This page uses neutral project-retrospective language rather than the client/engagement framing `structure.md` otherwise assumes. See the PR description for this session for the maintainer-facing flag on this mismatch.

## Summary

`meal_planner_app` is a multi-app system (a meal-planning frontend plus an associated "fitness" module/app) with Google/SSO-style authentication, a Vercel-hosted frontend, and a Render-hosted PostgreSQL backend, with a separate Neon database also in play at some point.[^2] The source document does not name this repository again in body text — the issues below are attributed to it based on contextual identifiers in the source (the `meal-planner-gold-one.vercel.app` and `meal-planner-app-8hnw.vercel.app` "fitness app" URLs, the `fitness/frontend` Vercel root directory, and the `FRONTEND_BASE` / `FITNESS_DATABASE_URL` environment variable names), not an explicit in-text repo label.[^1] Every issue below recurs around cross-app configuration drift: two Vercel-hosted frontends (meal planner and fitness) sharing one backend, and two databases (Render PostgreSQL and Neon) in play at once.

> **Gap:** No scope, client, delivery period, or approximate value is available in the source material. This page cannot populate the "Project name, client, period, engagement type, approximate scope/value" fields `structure.md` calls out as part of a minimum viable retrospective page.

## Key issues and root causes

### Authentication / SSO configuration drift

- **OAuth return-to parameter loss.** A `?returnTo=fitness` URL parameter was not cleared after the OAuth callback, so every login — not just the one that originally set the parameter — redirected to the fitness app instead of its intended destination.[^3]
- **Auth hash format mismatch.** The fitness app expected an auth callback hash of the form `#auth=token=xxx&user=xxx`, but the backend was sending `#token=xxx` only, causing silent auth failures with no fallback handling.[^4]
- **`FRONTEND_BASE` pointed at the wrong app.** A copy/paste error during Render setup — two visually similar Render/Vercel URLs — set the backend's `FRONTEND_BASE` to the fitness app's URL instead of the meal planner's, so all OAuth logins redirected to the wrong app. There was no startup validation of the variable to catch this.[^5]
- **Stale transient state.** A `sso_return_to` value written to `localStorage` was not reliably cleared after being consumed (multiple code paths could set it; no cleanup on error paths), causing repeated unwanted redirects on later, unrelated visits.[^6]
- **Admin role granted in the wrong database.** A user was given the `admin` role in a Neon database, but the production backend actually authenticated against a separate Render PostgreSQL instance, so the admin privilege never took effect. The two databases were not clearly documented or separated.[^7]

### Deployment configuration drift

- **Vercel Root Directory misconfiguration.** In this monorepo layout, Vercel repeatedly failed to find the `fitness/frontend` subdirectory, traced to Root Directory settings conflicting with custom build commands and cached configuration from prior deployments.[^8]
- **CORS allowlist not updated on redeploy.** The fitness app's new URL was not added to the backend's CORS allowlist after the project was recreated, and the previous URL had been deleted in the process, breaking all API calls from the fitness app.[^9]

### Database / environment variable mismatch

- **`DATABASE_URL` vs. a module-specific variable.** The fitness module used `FITNESS_DATABASE_URL`, but the Prisma schema was hardcoded to read `DATABASE_URL`, so `prisma migrate deploy` failed with an authentication error until the schema or the shell environment was reconciled.[^10]

### Possibly related, not confidently attributable to this project

- **Empty-array Postgres cast failure.** A migration failed with "cannot determine type of empty array" on an `INSERT` into an `exercise_definitions` table with a `secondary_muscles` column.[^11] The table/column names match this project's fitness/exercise domain, which is the basis for including it here — but the source text does not explicitly name a repository for this issue, unlike the items above. Treat this attribution as inferred, not stated; see the PR description for this editorial call.
- **Template literal not evaluated in a `className`.** A rendered class name used `difficulty-{exercise.difficulty_level}` instead of a template literal, so the literal text rendered rather than the interpolated value.[^12] Same caveat: `exercise.difficulty_level` suggests the fitness/exercise domain, but no repository is named in the source for this issue.

> **Gap:** Several other issues in the source (migration-tracking-state inconsistency, a missing unique constraint on a `subscriptions.user_id` column, a `null`-vs-`undefined` validation bug, a frontend/backend API payload mismatch, a React 17+ unused-import warning) have no domain or naming clue tying them to this project specifically, and are not included here. They are captured without project attribution in `docs/best-practices/database-migration-hygiene.md` and `docs/best-practices/frontend-api-integration-hygiene.md` instead of being guessed into this page.

## Root-cause themes

Across the attributable issues, three recurring root causes stand out: (1) two parallel frontends (meal planner, fitness) and two databases (Render, Neon) were not clearly documented as to which served which purpose, so configuration was copy/pasted or set against the wrong target repeatedly;[^5][^7][^10] (2) transient auth state (URL params, `localStorage`) was set without a reliable, error-path-inclusive clearing step;[^3][^6] and (3) Vercel/CORS configuration was not re-verified as a checklist item after redeploys or project recreation.[^8][^9]

> **Gap:** No outcome metrics (defect counts, time-to-resolution, downtime) are available for any of these issues — the source documents root cause and resolution, not measured impact. Confidence is capped at `low` accordingly.

## Key personnel

> **Gap:** No individuals are named or citable in the source material for this project.

---

[^1]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — document header ("Repositories Analyzed").
[^2]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Authentication & SSO > Admin Role in Wrong Database; Deployment & Vercel > Vercel Root Directory Misconfiguration; Deployment & Vercel > CORS Configuration.
[^3]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Authentication & SSO > URL Parameter Persistence Through OAuth.
[^4]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Authentication & SSO > URL Hash Format Mismatch Between Systems.
[^5]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Authentication & SSO > Environment Variable Misconfiguration (FRONTEND_BASE).
[^6]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Authentication & SSO > State Not Cleared After Use (Stale localStorage).
[^7]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Authentication & SSO > Admin Role in Wrong Database.
[^8]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Deployment & Vercel > Vercel Root Directory Misconfiguration.
[^9]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Deployment & Vercel > CORS Configuration.
[^10]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Database & Migrations > Database URL Environment Variable Confusion.
[^11]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Database & Migrations > Empty Array Type Inference in PostgreSQL.
[^12]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Frontend Development > Template Literal Not Evaluated in className.

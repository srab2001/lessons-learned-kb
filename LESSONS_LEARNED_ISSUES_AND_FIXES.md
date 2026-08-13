# Consolidated Lessons Learned: Issues and Fixes (srab2001)

**Compiled:** 2026-08-13  
**Scope:** Public repositories under `srab2001` containing lessons-learned/troubleshooting writeups.  
**Note:** No GitHub Issues matching a lessons-learned dataset were found; entries below are copied from repository lesson documents.

## Repositories Reviewed

- `meal_planner_app`
- `travel-deal-finder`
- `raven_demo`
- `myteacher`
- `mhv_demo` (no lessons-learned issue/fix document found)
- `claude_testing` (no lessons-learned issue/fix document found)
- `lessons-learned-kb` (target repository)

---

## meal_planner_app

### Source: `docs/LESSONS_LEARNED_SSO.md`

1. **Issue:** OAuth `returnTo` URL parameter persisted and forced wrong redirects.  
   **Fix:** Store transient redirect state in `localStorage`, clear URL params, then continue OAuth callback flow.

2. **Issue:** URL hash mismatch between apps (`#auth=...` vs `#token=...`).  
   **Fix:** Support both formats with fallback parsing and token verification.

3. **Issue:** Environment variable misconfiguration (`VITE_API_BASE_URL`/frontend base mix-up).  
   **Fix:** Validate env vars at startup and log safe diagnostics.

4. **Issue:** Stale localStorage state caused repeated redirect loops.  
   **Fix:** Remove transient state immediately after read (including error paths).

5. **Issue:** Vercel root directory config caused repeated build failures.  
   **Fix:** Recreate/repair Vercel project config with correct monorepo root settings.

6. **Issue:** CORS blocked new frontend app URL.  
   **Fix:** Update backend CORS allowlist whenever frontend origins change.

### Source: `fitness/LESSONS_LEARNED.md`

1. **Issue:** PostgreSQL empty array type inference error in migration.  
   **Fix:** Cast empty arrays explicitly (for example `ARRAY[]::TEXT[]`).

2. **Issue:** Prisma database URL variable mismatch for fitness module.  
   **Fix:** Ensure Prisma uses the intended DB URL and environment mapping.

3. **Issue:** Prisma migration state out of sync with actual DB.  
   **Fix:** Execute migration SQL directly and re-verify schema state.

4. **Issue:** Unused React import warnings with modern JSX transform.  
   **Fix:** Remove unnecessary `import React` in JSX-only files.

5. **Issue:** Dynamic className template literal bug.  
   **Fix:** Use proper template literal interpolation for class names.

6. **Issue:** AI Coach request payload mismatch frontend vs backend contract.  
   **Fix:** Rebuild frontend payload to match backend-required shape.

7. **Issue:** Design token import inconsistencies.  
   **Fix:** Standardize token import/use pattern.

8. **Issue:** Missing production API URL env var broke runtime API calls.  
   **Fix:** Define environment-specific `.env` values and validate at build/runtime.

9. **Issue:** Prisma client module resolution failures in tests.  
   **Fix:** Correct import path/resolution strategy for generated Prisma client.

10. **Issue:** Local Store Finder endpoints were lost during context switch.  
    **Fix:** Re-implement endpoints in one pass and verify file state before proceeding.

11. **Issue:** Node↔Python inter-process integration reliability concerns.  
    **Fix:** Use `spawn` with structured stdin/stdout JSON, buffering/timeout handling, and schema validation.

12. **Issue:** AI price normalization risked inventing prices.  
    **Fix:** Enforce strict prompt constraints plus fallback validation (`not available`).

13. **Issue:** DB logging could block request response path.  
    **Fix:** Isolate logging failures in `try/catch` and keep response flow non-blocking.

---

## raven_demo

### Source: `docs/LESSONS-LEARNED.md`

1. **Issue:** Vercel serverless auth routes crashed with ESM/CommonJS mismatch symptoms.  
   **Fix:** Remove ESM-only `jose` dependency, reimplement JWT with Web Crypto API, and standardize module format.

2. **Issue:** Verification was run against stale build artifact, masking true UI bug.  
   **Fix:** Rebuild before each verification cycle and avoid clearing success status during background refresh side effects.

---

## myteacher

### Source: `docs/deployment-troubleshooting.md` (Lessons Learned + linked deployment issues)

1. **Issue:** Production used `prisma db push`, causing schema drift/data-risk behavior.  
   **Fix:** Use `prisma migrate deploy` in production workflows.

2. **Issue:** Migration directories drifted between app/package locations.  
   **Fix:** Synchronize migrations and maintain one canonical migration source.

3. **Issue:** Generic UI/API errors obscured actual Prisma failures.  
   **Fix:** Diagnose using Vercel function logs and root-cause DB/schema error directly.

4. **Issue:** Vercel build cache served stale Prisma artifacts.  
   **Fix:** Redeploy without cache when debugging schema/client mismatches.

5. **Issue:** `migrate resolve --applied` marked migrations done without running SQL.  
   **Fix:** Run missing SQL explicitly and reserve resolve for true manual baseline scenarios.

6. **Issue:** Migrations were not bundled into serverless build.  
   **Fix:** Add Prisma schema/migrations/generated client to `includeFiles`.

7. **Issue:** Troubleshooting focused on app code before DB connectivity/state checks.  
   **Fix:** Verify migration status and live schema first during incident response.

8. **Issue:** Seed scripts referenced removed schema models.  
   **Fix:** Update seed scripts alongside every schema change.

9. **Issue:** Partial migration retries failed due non-idempotent SQL.  
   **Fix:** Make migration SQL idempotent (`IF NOT EXISTS`, guarded blocks).

---

## travel-deal-finder

### Source: `docs/LESSONS_LEARNED.md`

1. **Issue:** Node test invocation attempted directory target and failed discovery.  
   **Fix:** Use explicit test file globs (`node --test tests/*.test.js`).

2. **Issue:** Scheduler next-run estimate ignored timezone/DST (status display drift).  
   **Fix:** Keep runtime cron scheduling authoritative and treat estimate as known limitation pending timezone-aware enhancement.

3. **Issue:** External API dependency risk for local setup/CI.  
   **Fix:** Implement deterministic fallback/mock data path so flow works without API credentials.

---

## Primary Source Files

- `srab2001/meal_planner_app/docs/LESSONS_LEARNED_SSO.md`
- `srab2001/meal_planner_app/fitness/LESSONS_LEARNED.md`
- `srab2001/raven_demo/docs/LESSONS-LEARNED.md`
- `srab2001/myteacher/docs/deployment-troubleshooting.md`
- `srab2001/travel-deal-finder/docs/LESSONS_LEARNED.md`

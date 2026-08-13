# Consolidated Lessons Learned & Resolutions

**Compiled:** August 13, 2026  
**Source:** Analysis of srab2001's dedicated lessons learned documents  
**Repositories Analyzed:**
- `meal_planner_app` (3 documents)
- `travel-deal-finder` 
- `raven_demo`

---

## Table of Contents

1. [Authentication & SSO](#authentication--sso)
2. [Deployment & Vercel](#deployment--vercel)
3. [Database & Migrations](#database--migrations)
4. [Testing & Code Quality](#testing--code-quality)
5. [Frontend Development](#frontend-development)
6. [API & Backend](#api--backend)
7. [Process & Workflow](#process--workflow)

---

## Authentication & SSO

### Issue: URL Parameter Persistence Through OAuth

**What Happened:** The `?returnTo=fitness` URL parameter persisted through OAuth, causing all logins to redirect to fitness instead of the intended destination.

**Root Cause:**
- OAuth redirect URL included `?returnTo=fitness` 
- URL parameter not cleared after OAuth callback
- Every login checked URL and redirected to fitness

**Resolution:**
```javascript
// BAD: Passing state in URL (gets lost during OAuth)
redirectUrl = `/callback?returnTo=${returnTo}`;

// GOOD: Store in localStorage, clear URL
localStorage.setItem('sso_return_to', returnTo);
window.history.replaceState(null, '', pathname);
redirectUrl = `/callback`;
```

**Best Practice Checklist:**
- [ ] Store transient state in localStorage BEFORE OAuth redirect
- [ ] Clear URL state immediately after storing
- [ ] Remove state from localStorage AFTER consuming it (including error paths)
- [ ] Document expected URL formats for each app
- [ ] Test both direct and SSO login flows

---

### Issue: URL Hash Format Mismatch Between Systems

**What Happened:** Fitness app expected `#auth=token=xxx&user=xxx` but backend was sending `#token=xxx`, causing silent failures.

**Root Cause:**
- Different code paths produced different hash formats
- No fallback handling for alternate formats
- Multiple app integrations without format agreement

**Resolution:**
```javascript
// Handle multiple formats
if (hash.startsWith('#auth=')) {
  // Preferred format with user data
  const parts = hash.slice(5).split('&');
  // Parse auth=value&user=value
} else if (hash.startsWith('#token=')) {
  // Fallback: verify with API to get user
  const token = hash.slice(7);
  const user = await api.verifyToken(token);
}
```

**Best Practice:**
Always handle multiple input formats when integrating independent systems. Document the preferred format and all fallbacks.

---

### Issue: Environment Variable Misconfiguration (FRONTEND_BASE)

**What Happened:** Backend `FRONTEND_BASE` was set to fitness app URL instead of meal planner, causing ALL OAuth logins to redirect to wrong app.

**Root Cause:**
- Copy/paste error during Render setup
- Similar-looking URLs (both from Render)
- No validation of environment variables at startup

**Resolution:**
```bash
# On Render backend, verify FRONTEND_BASE:
FRONTEND_BASE=https://meal-planner-gold-one.vercel.app  # Meal planner
# NOT the fitness app URL!

# Add validation at app startup
const API_BASE = import.meta.env.VITE_API_BASE_URL;
if (!API_BASE || !API_BASE.startsWith('https://')) {
  console.error('Invalid API_BASE:', API_BASE?.substring(0, 20));
  throw new Error('API configuration invalid');
}
```

**Best Practice:**
- Log environment variables (safely, truncated) at startup
- Validate URL format and domain expectations
- Use `.env.example` template files
- Document which database/environment each variable connects to

---

### Issue: State Not Cleared After Use (Stale localStorage)

**What Happened:** `sso_return_to` localStorage value persisted from previous SSO visits, causing repeated unwanted redirects.

**Root Cause:**
- State was set but not consumed reliably
- Multiple code paths could set the value
- No cleanup on error/fallback paths

**Resolution:**
```javascript
const returnTo = localStorage.getItem('sso_return_to');
localStorage.removeItem('sso_return_to'); // Clear FIRST, before any logic

if (returnTo === 'fitness') {
  // Handle redirect
}
// State is cleared regardless of outcome
```

**Pattern:**
Always clear transient state immediately after reading it. This prevents bugs where stale state causes repeated side effects.

---

### Issue: Admin Role in Wrong Database

**What Happened:** User had admin role in Neon database but production backend connected to Render PostgreSQL, so admin privileges never worked.

**Root Cause:**
- Two separate databases (Render + Neon) not clearly separated
- Admin role updates made in wrong database
- No clear documentation of which database served which purpose

**Resolution:**
```sql
-- Connect to PRODUCTION Render PostgreSQL (NOT Neon!)
-- Host: dpg-d4nj6demcj7s73dfvie0-a.oregon-postgres.render.com

-- Add role column if missing
ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'user';

-- Grant admin
UPDATE users SET role = 'admin' WHERE email = 'your-email@example.com';

-- Verify
SELECT email, role FROM users WHERE email = 'your-email@example.com';
```

**Best Practice:**
- Document which database is used for what (auth, core features, meals, etc.)
- Add comments in environment variable configs
- Create separate database client instances with clear names
- Always check `DATABASE_URL` first when debugging auth issues

---

## Deployment & Vercel

### Issue: ESM-Only Dependency Crashes in Vercel Serverless

**What Happened:** After shipping Google OAuth, production returned `FUNCTION_INVOCATION_FAILED` on auth routes. Error logs: `Cannot use import statement outside a module`. Build status: "Ready". Function: crashed at request time.

**Root Cause (Multiple Layers):**
1. `lib/db.ts` threw at module-import time when `DATABASE_URL` missing
2. `/api/auth/google/start` had no try/catch wrapper
3. **Real cause:** `jose` (JWT library) is ESM-only; Vercel's Node-function bundler wasn't reliably propagating `"type": "module"` signal from `package.json` into runtime context

**Misleading Fix That Seemed To Work (Then Failed):**
Added `"type": "module"` to package.json. Deployed cleanly. On next fresh redeploy with no build cache, identical crash came back. **This signal—a "fix" that works once then reappears—means the config change isn't the actual lever.**

**Actual Resolution:**
Removed ESM-only dependency entirely. Rewrote `lib/jwt.ts` using Web Crypto API only:

```javascript
// BEFORE: ESM-only jose library
import { SignJWT } from 'jose';

// AFTER: Web Crypto API (works in CommonJS, ESM, AND Edge Runtime)
import { crypto } from 'node:crypto';
const { subtle } = crypto;

// Now works everywhere regardless of module format
const signature = await subtle.sign('HMAC', key, data);
```

**Why This Works:**
- Web Crypto behaves identically whether surrounding code is CommonJS or ESM
- Works in Vercel serverless functions AND Edge Middleware (`edge_runtime` has no `node:crypto` import)
- Zero dependency on bundler magic or module-format config

**Best Practice Checklist:**
- [ ] "Ready" build status ≠ "deployed function works" — check runtime behavior separately
- [ ] If ESM-only dependency causes bundler issues, don't tune configs — replace the dependency
- [ ] Prefer Web APIs available in both Node.js and Edge Runtime (`crypto.subtle`, `fetch`, `TextEncoder`)
- [ ] Avoid `node:*` imports in functions that must work in Edge Runtime
- [ ] **Verification:** Compile with `tsc --outDir <tmp>` and inspect actual emitted JS

---

### Issue: Vercel Root Directory Misconfiguration

**What Happened:** Vercel couldn't find `fitness/frontend` directory, builds failed repeatedly.

**Root Cause:**
- Root Directory setting conflicts with custom build commands
- Cached configuration from previous deployments
- Project settings vs Production Overrides mismatch

**Resolution:**

For monorepo deployments:
```
Root Directory: fitness/frontend
Framework: Vite
Build Command: (default)
Output Directory: build
```

**Best Practice:**
When Vercel configuration is corrupted, delete and recreate the project from scratch rather than trying to "fix" cached settings.

---

### Issue: CORS Configuration

**What Happened:** Fitness app couldn't call backend API due to CORS errors after deployment.

**Root Cause:**
- New fitness app URL not added to backend CORS whitelist
- Old URL was deleted when project was recreated

**Resolution:**
```javascript
const allowedOrigins = [
  process.env.FRONTEND_BASE,
  'https://meal-planner-gold-one.vercel.app',
  'https://meal-planner-app-8hnw.vercel.app', // New fitness app
];
```

**Best Practice:**
When deploying new frontends, immediately update backend CORS allowlist. Use environment variables instead of hardcoded URLs when possible.

---

### Issue: Build Cache Causing Stale Artifacts

**What Happened:** Verification kept failing against outdated `dist/` output because source file was edited after last build. Spent an hour debugging "bugs" that were actually in the old build artifact.

**Root Cause:**
- Source file modified after last `npm run build`
- Running verification against stale compiled output
- Changes never reflected because build wasn't re-run

**Resolution:**
Always rebuild before verifying changes:
```bash
npm run build
# THEN verify
playwright test
```

**Deep-Dive Example (Race Condition Masked by Stale Build):**

After fixing stale build issue, a second bug surfaced:
- Handler set success message: `#editor-result.textContent = 'Saved...'`
- Handler called `loadContentItems()` to refresh dropdown
- Dropdown selection change cleared the success message as side effect
- Message visible for ~100ms, then silently overwritten

This was invisible in manual testing (glance-and-move-on) but would fail any automated verification that waits for the message.

**Fix:**
Only clear status messages on *user-initiated* actions, never as side effect of data refresh:

```javascript
// BAD: Refresh side effect clears message
async function handleSave() {
  setStatus('Saved...');
  await api.save(data);
  loadContentItems();  // ← This clears status as side effect
}

// GOOD: Only user action clears it
async function handleSave() {
  setStatus('Saved...');
  await api.save(data);
  // Don't call loadContentItems() here
}

function handleDropdownChange() {
  setStatus('');  // Only cleared by user action
  loadContentItems();
}
```

**Best Practice:**
- Re-run build before every verification
- State changes in side effects are invisible in manual testing
- Automated checks that *wait* for output catch these bugs immediately

---

## Database & Migrations

### Issue: Empty Array Type Inference in PostgreSQL

**What Happened:** Migration failed: `ERROR: cannot determine type of empty array`

**Root Cause:**
PostgreSQL cannot infer the type of an empty array literal without explicit casting.

```sql
-- FAILS
INSERT INTO exercise_definitions (..., secondary_muscles, ...) 
VALUES (..., ARRAY[], ...);

-- ERROR: cannot determine type of empty array
```

**Resolution:**
Always explicitly cast empty arrays:

```sql
-- Works
INSERT INTO exercise_definitions (..., secondary_muscles, ...) 
VALUES (..., ARRAY[]::TEXT[], ...);
```

Batch fix with sed:
```bash
sed -i '' 's/ARRAY\[\]/ARRAY[]::TEXT[]/g' migration.sql
```

**Best Practice:**
- Always explicitly cast: `ARRAY[]::type[]`
- Consider using `NULL` instead of empty arrays for optional fields
- Add type-casting checks to migration linting
- Test migrations on copy of production data

---

### Issue: Database URL Environment Variable Confusion

**What Happened:** `npx prisma migrate deploy` failed with "Authentication failed against database server."

**Root Cause:**
Fitness module used `FITNESS_DATABASE_URL` but Prisma schema was hardcoded to look for `DATABASE_URL`.

**Resolution:**
Option 1 - Explicit environment setup:
```bash
export DATABASE_URL="postgresql://...fitness..."
npx prisma migrate deploy
```

Option 2 - Update schema:
```prisma
datasource db {
  provider = "postgresql"
  url      = env("FITNESS_DATABASE_URL")  // Use specific variable name
}
```

**Best Practice:**
- Create `.env` file in subdirectory with correct `DATABASE_URL`
- Use `prisma --schema` flag to specify schema location
- Document environment variable requirements clearly
- Test migrations locally before deploying

---

### Issue: Migration State Inconsistency

**What Happened:** `prisma migrate deploy` says "No pending migrations" but table doesn't exist.

**Root Cause:**
Prisma's `_prisma_migrations` tracking table out of sync with actual database state (manual SQL applied, or migration failed mid-execution).

**Resolution:**
```bash
# Execute SQL directly, bypassing Prisma tracking
npx prisma db execute --file prisma/migrations/003_add_exercise_library/migration.sql

# Or verify actual schema
npx prisma db pull
```

**Best Practice:**
- Use `prisma migrate dev` in development to test migrations
- Use `prisma db pull` to verify actual schema
- Use `prisma db push` only for rapid prototyping (never production)
- Document manual migration steps when tracking breaks

---

### Issue: No Unique Constraint on Subscription User_ID

**What Happened:** `ON CONFLICT (user_id)` failed — no unique constraint exists.

**Resolution:**
Use separate INSERT/UPDATE queries:
```sql
-- Check first
SELECT * FROM subscriptions WHERE user_id = X;
-- Then INSERT or UPDATE as needed
```

---

### Issue: Null Validation Failures

**What Happened:** Validation error "target_value must be a positive number" for null values.

**Root Cause:**
Validation only checked `!== undefined`, not `!== null`.

**Resolution:**
```javascript
// BAD
if (value !== undefined) { ... }

// GOOD
if (value !== null && value !== undefined) { ... }
```

---

## Testing & Code Quality

### Issue: Stale Build Causing False Debug Output

**Scenario:** Playwright test failing, manual fetch calls working, request logging showing success.

**Root Cause:**
Verifying against `dist/` which was older than source file. All debugging pointed at different issues (routing, mocking, element lookup) when real cause was testing stale code.

**Resolution:**
Re-run build before every verification step:
```bash
npm run build
npm test
```

**Best Practice:**
Whenever a check that should pass keeps failing for reasons that don't add up:
1. **First:** Verify the artifact under test is actually current
2. Then debug the failure itself

---

## Frontend Development

### Issue: React Import Warning (React 17+)

**What Happened:** Unused import warning: `'React' is declared but its value is never used`

**Root Cause:**
React 17+ new JSX transform no longer requires `import React`.

**Resolution:**
```javascript
// BEFORE
import React from 'react';
import { BrowserRouter } from 'react-router-dom';

// AFTER
import { BrowserRouter } from 'react-router-dom';
```

---

### Issue: Template Literal Not Evaluated in className

**What Happened:** `className="difficulty-{exercise.difficulty_level}"` rendered literally as "difficulty-{exercise.difficulty_level}".

**Root Cause:**
Template literals require `${}` syntax, not just `{}`.

**Resolution:**
```jsx
// BAD
<span className="difficulty-badge difficulty-{exercise.difficulty_level}">

// GOOD
<span className={`difficulty-badge difficulty-${exercise.difficulty_level}`}>
  {exercise.difficulty_level}
</span>
```

---

### Issue: API Payload Mismatch

**What Happened:** Frontend sending `{answers, user_id, metadata}` but backend expecting `{messages, interview_answers, userProfile}`.

**Root Cause:**
Frontend and backend developed independently without API contract validation.

**Resolution:**
1. Define clear API contracts with TypeScript interfaces
2. Use tools like Postman/Insomnia to validate payloads
3. Implement request validation middleware on backend
4. Add integration tests for full request/response cycle

```javascript
// Define contract
interface CoachRequest {
  messages: Array<{ role: string; content: string }>;
  interview_answers: Record<string, string>;
  userProfile: { age: number; fitness_level: string };
}

// Validate on backend
const validated = validateCoachRequest(req.body);
if (!validated.ok) return res.status(400).json({ error: validated.errors });
```

---

## API & Backend

### Issue: Missing Try/Catch on API Routes

**What Happened:** `lib/db.ts` threw at module-import time, but no error handler caught it.

**Root Cause:**
API route handler had no try/catch wrapper for initialization code.

**Resolution:**
```javascript
// BEFORE
export default async function handler(req, res) {
  const data = await getData();  // If throws, unhandled
  res.json(data);
}

// AFTER
export default async function handler(req, res) {
  try {
    const data = await getData();
    res.json(data);
  } catch (error) {
    console.error('API error:', error.message);
    res.status(500).json({ error: 'Internal server error' });
  }
}

// OR with helper
export default withErrorHandling(async (req, res) => {
  const data = await getData();
  res.json(data);
});
```

**Best Practice:**
Wrap all API handler bodies with error handling. Lazy-initialize database clients inside functions, not at module load time.

---

### Issue: Lazy Initialization of Database Clients

**What Happened:** `lib/db.ts` threw at import time when `DATABASE_URL` missing, preventing entire module from loading.

**Root Cause:**
Database client initialized at module load, not at first use.

**Resolution:**
```javascript
// BEFORE: Throws at import time
const db = new PrismaClient({
  datasources: { db: { url: process.env.DATABASE_URL } }
});

// AFTER: Throws at first use (inside try/catch)
let dbClient = null;

function getClient() {
  if (!dbClient) {
    dbClient = new PrismaClient({
      datasources: { db: { url: process.env.DATABASE_URL } } 
    });
  }
  return dbClient;
}

// Usage
export default async function handler(req, res) {
  try {
    const db = getClient();
    const data = await db.query();
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
```

---

### Issue: No Validation of Environment Variables at Startup

**What Happened:** Wrong API_BASE deployed, API calls failed silently.

**Root Cause:**
No startup validation of critical environment variables.

**Resolution:**
```javascript
// At app startup
function validateEnv() {
  const required = ['DATABASE_URL', 'API_BASE', 'GOOGLE_CLIENT_ID'];
  for (const varName of required) {
    if (!process.env[varName]) {
      throw new Error(`Missing required env var: ${varName}`);
    }
  }
  
  // Validate format
  if (!process.env.API_BASE.startsWith('https://')) {
    throw new Error(`Invalid API_BASE format: ${process.env.API_BASE.substring(0, 20)}`);
  }
  
  console.log('✓ Environment variables validated');
}

validateEnv();
```

---

## Process & Workflow

### Lesson: Ask Before Doing on Ambiguous Specs

**What Happened (travel-deal-finder project):**
- Original plan: one PR per prompt (12 total)
- Prompt 6 said "combine before merging"
- Spent 30 mins reconsidering strategy instead of 3 hours redoing work

**Pattern:**
When a spec has a fork in the road, ask. The 30 seconds to read a clarification question is cheaper than 30 minutes to redo work.

---

### Lesson: Don't Ask When Spec Is Unambiguous

**Pattern:**
Once the workflow is confirmed (commit → push → CI → squash-merge → repeat), execute it silently for 6+ iterations without re-confirming each time.

---

### Lesson: Phase-Level PRs Over Per-Spec PRs

**What Happened:**
Changed from one PR per spec line to one PR per coherent feature phase. Result: 6 PRs instead of 12.

**Benefits:**
- Reviewer sees "whole feature" in one PR
- Eliminates inter-prompt rebases
- PR description explains how pieces fit together

**Rule:**
Right PR size = "one coherent feature", not "one spec line". When prompts touch overlapping code, combine into phase.

---

### Lesson: Injectable I/O Pays For Itself Immediately

**Pattern:**
Every module doing I/O accepts options bag: `fetchImpl`, `sleep`, `now`, `rng`, `logger`, `cronImpl`, `fsImpl`.

**Payoff (travel-deal-finder):**
- 91 tests run in <100ms (no real timers, no network)
- Kiwi API fallback testable without API key
- Mock data deterministic and reproducible

**Upfront cost:** ~5 lines per module  
**Breakeven:** First time you write a test

---

### Lesson: Mock-First, Real-API-Second

**Pattern:**
Any external dependency ships a believable fallback.

**Example (flight search):**
- If `FLIGHT_API_KEY` unset or API 500s → generate deterministic mock data
- New contributors run pipeline in <5 minutes with no signups
- CI exercises full flow without secrets
- Bad API key never breaks production run

**Takeaway:**
"It worked locally" should never depend on credentials.

---

### Lesson: Lock Schema Once

**What Happened (travel-deal-finder):**
- Phase 2: `origins` used
- Phase 3: renamed to `departureAirports`
- Three modules + test file had to change

**Prevention:**
Lock `config.json` schema in single source (e.g., `lib/configManager.js`'s `DEFAULT_CONFIG`). Treat schema changes as breaking-change PRs.

---

### Lesson: Automated Testing Early Catches Drift

**What Happened (raven_demo):**
- End-to-end smoke test ran exactly once, at release time
- Worked first try
- But if it hadn't, debugging would span 7 PRs

**Best Practice:**
Run smoke test in every CI pipeline, not just at release.

---

## Summary: Top Issues & Quick Fixes

| Issue | Severity | Quick Fix | Prevention |
|-------|----------|-----------|-----------|
| URL params lost in OAuth | CRITICAL | Use localStorage for state | Store state before redirect, clear after use |
| ESM-only dependency crashes | CRITICAL | Replace with Web Crypto | Prefer Web APIs in serverless/Edge |
| Empty array type error | HIGH | Cast: `ARRAY[]::TEXT[]` | Always explicitly cast empty arrays |
| Environment variable misconfigured | HIGH | Add startup validation | Log and validate all env vars at boot |
| Wrong database for admin role | HIGH | Update correct database | Document which DB serves what |
| Stale build artifact | MEDIUM | Rebuild before testing | Run `npm run build` before every test |
| Template literal not evaluated | LOW | Use `${}` syntax | Enable JSX linting |
| Try/catch missing on API routes | MEDIUM | Wrap handler body | Use error-handling middleware/helper |
| Lazy init database client | MEDIUM | Init on first use | Never init DB at module load |

---

**Document Version:** 1.0  
**Last Consolidated:** August 13, 2026  
**Maintained By:** srab2001

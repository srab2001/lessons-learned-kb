---
title: "Best Practice: Postgres/Prisma Migration Hygiene Checklist"
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

# Best Practice: Postgres/Prisma Migration Hygiene Checklist

## Practice statement

Four small, independently verifiable Postgres/Prisma hygiene practices, each grounded in a specific documented failure in the source material. None of these carry a quantified outcome — they are qualitative fixes to concrete bugs, bundled here into one checklist rather than four separate thin pages.

## Evidence chain

1. **Explicitly cast empty array literals.** A migration failed with `ERROR: cannot determine type of empty array` on an `INSERT` into an `exercise_definitions` table with a `secondary_muscles` column, because PostgreSQL cannot infer the type of a bare `ARRAY[]` literal. The fix: cast explicitly, e.g. `ARRAY[]::TEXT[]`, and a batch fix via `sed` was used to correct existing migration files.[^1] Recorded prevention: always cast explicitly, consider `NULL` instead of an empty array for optional fields, add type-casting checks to migration linting, and test migrations against a copy of production data. **Attribution note:** the `exercise_definitions`/`secondary_muscles` naming matches `meal_planner_app`'s fitness/exercise domain (see `docs/retrospectives/meal-planner-app.md`), but the source does not explicitly name a repository for this issue — that project tie is inferred, not stated.

2. **Verify actual migration state before trusting the tracking table.** `prisma migrate deploy` reported "No pending migrations" while the target table did not actually exist, because Prisma's `_prisma_migrations` tracking table had drifted from the real schema (e.g., from a manual SQL change or a mid-execution failure).[^2] Recorded fix: apply SQL directly with `prisma db execute --file <migration.sql>` to bypass tracking when needed, or use `prisma db pull` to verify the real schema. No repository is named for this issue.

3. **Don't rely on `ON CONFLICT` without a matching unique constraint.** An `ON CONFLICT (user_id)` clause failed because no unique constraint existed on that column.[^3] Recorded fix: use a check-then-insert/update pattern instead until the constraint is added. No repository is named for this issue.

4. **Validate for both `null` and `undefined`.** A validation check used `value !== undefined` only, so a `null` value passed the check and then failed downstream with a misleading "must be a positive number" error.[^4] Recorded fix: check `value !== null && value !== undefined`. No repository is named for this issue.

## Where it applies

Any Postgres schema using array-typed columns (item 1); any Prisma-managed schema, especially where manual SQL is sometimes applied outside Prisma's migration flow (item 2); any table using `ON CONFLICT` upserts (item 3); and any input validation logic distinguishing "not provided" from "explicitly empty" (item 4).

## Confidence and evidence caveats

`confidence: low` for all four items — each is a single, qualitative bug/fix pair with no defect-rate or time-saved metric, and no project attribution beyond the inferred tie noted for item 1.

> **Gap:** Items 2–4 have no naming or domain clue in the source tying them to any of the three repositories; they are deliberately left unattributed here rather than guessed into a specific project's retrospective page.

---

[^1]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Database & Migrations > Issue: Empty Array Type Inference in PostgreSQL.
[^2]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Database & Migrations > Issue: Migration State Inconsistency.
[^3]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Database & Migrations > Issue: No Unique Constraint on Subscription User_ID.
[^4]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Database & Migrations > Issue: Null Validation Failures.

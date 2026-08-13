---
title: "Best Practice: Frontend/API Integration Hygiene Checklist"
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

# Best Practice: Frontend/API Integration Hygiene Checklist

## Practice statement

Three small, independently verifiable frontend and frontend/backend integration hygiene practices, bundled here into one checklist rather than three separate thin pages. None carry a quantified outcome.

## Evidence chain

1. **Drop the unused `import React` on React 17+.** React 17+'s new JSX transform no longer requires `import React from 'react'`, and leaving it in produces an unused-import warning.[^1] No repository is named for this issue.

2. **Use `${}` interpolation in template literals, not bare `{}`, inside JSX class-name strings.** A class name written as `className="difficulty-{exercise.difficulty_level}"` rendered the literal text `difficulty-{exercise.difficulty_level}` rather than the interpolated value, because template literals require `${}` syntax.[^2] **Attribution note:** `exercise.difficulty_level` matches `meal_planner_app`'s fitness/exercise domain (see `docs/retrospectives/meal-planner-app.md`), but the source does not explicitly name a repository for this issue — that project tie is inferred, not stated.

3. **Define and validate an explicit request/response contract between frontend and backend built independently.** A frontend sent `{answers, user_id, metadata}` while the backend expected `{messages, interview_answers, userProfile}`, because the two sides were developed independently without an agreed contract.[^3] Recorded fix: define the contract explicitly (e.g., a shared TypeScript interface), validate payloads during development (e.g., with Postman/Insomnia), add request-validation middleware on the backend, and add integration tests covering the full request/response cycle. No repository is named for this issue; the example payload's `fitness_level` field is a weak, inconclusive signal toward the fitness domain and is not used here as a basis for attribution.

## Where it applies

Item 1 applies to any React 17+ codebase. Item 2 applies to any JSX codebase using dynamic class names. Item 3 applies to any project where frontend and backend are built or iterated on independently, especially without a shared type/schema definition.

## Confidence and evidence caveats

`confidence: low` for all three items — each is a single, qualitative bug/fix pair with no defect-rate or time-saved metric, and no confirmed project attribution for any of the three.

> **Gap:** None of the three issues in this page have a confirmed repository attribution in the source; item 2's domain-based inference is noted explicitly above, and items 1 and 3 have no attribution basis at all.

---

[^1]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Frontend Development > Issue: React Import Warning (React 17+).
[^2]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Frontend Development > Issue: Template Literal Not Evaluated in className.
[^3]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Frontend Development > Issue: API Payload Mismatch.

---
title: "Best Practice: Lock Shared Config/Schema Contracts Early and Treat Renames as Breaking Changes"
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

# Best Practice: Lock Shared Config/Schema Contracts Early and Treat Renames as Breaking Changes

## Practice statement

Once a shared config or schema field name is used by more than one module, lock its name and shape in a single source of truth, and treat a later rename as a breaking-change pull request rather than a routine edit.

## Evidence chain

On `travel-deal-finder`, a config field was named `origins` in one project phase, then renamed to `departureAirports` in a later phase — requiring three modules plus a test file to change as a result.[^1] The prevention approach recorded in the source: lock the `config.json` schema in a single source of truth (e.g., a `DEFAULT_CONFIG` constant in a config manager module) and treat schema changes as breaking-change PRs going forward.

See `docs/retrospectives/travel-deal-finder.md` for the full project context.

## Where it applies

Any project where a config or data schema is consumed by more than one module or file — the risk and rework cost of an uncoordinated rename scales with the number of consumers.

## Confidence and evidence caveats

`confidence: low` — single project, single documented instance ("three modules plus a test file"), no independent corroboration and no time or effort metric attached to the rework beyond the count of affected files.

> **Gap:** No second project in this source corroborates this pattern, and no rework-time metric is available — only the count of files touched.

---

[^1]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Process & Workflow > Lesson: Lock Schema Once.

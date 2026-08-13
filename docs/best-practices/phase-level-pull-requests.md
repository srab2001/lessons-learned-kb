---
title: "Best Practice: Size Pull Requests Around One Coherent Feature Phase"
sources:
  - context/engagement-notes/consolidated-lessons-learned-2026-08-13.md
source_count: 1
as_of_date: "2026-08-13"
last_compiled: "2026-08-13"
lifecycle: draft
confidence: low
sensitivity: internal
lesson_type: [process]
lifecycle_history:
  - date: "2026-08-13"
    from: ""
    to: draft
    reason: "initial synthesis from consolidated-lessons-learned-2026-08-13.md"
---

# Best Practice: Size Pull Requests Around One Coherent Feature Phase

## Practice statement

Size pull requests around one coherent feature phase rather than one PR per individual spec line or prompt. Combine prompts that touch overlapping code into a single phase-level PR.

## Evidence chain

On `travel-deal-finder`, the PR strategy changed mid-project from one PR per spec line to one PR per coherent feature phase, reducing the total PR count from a planned 12 to 6.[^1] Reported benefits: a reviewer sees the "whole feature" in one PR, inter-prompt rebases are eliminated, and the PR description can explain how the pieces fit together. The rule of thumb recorded in the source: the right PR size is "one coherent feature," not "one spec line."

**Attribution note:** this specific lesson block does not repeat the `travel-deal-finder` name, but its "12 total" → "6 PRs" figures match the plan described in the explicitly-named "Ask Before Doing on Ambiguous Specs" lesson immediately preceding it in the same source section, which does name `travel-deal-finder`. The attribution here is inferred from that match, not stated outright in this specific block.

See `docs/retrospectives/travel-deal-finder.md` for the full project context.

## Where it applies

Projects executed as a sequence of scoped prompts or spec items where individual items frequently touch overlapping code — the PR-count reduction and rebase elimination benefit is specific to that overlap condition, not a general claim that fewer, larger PRs are always better.

## Confidence and evidence caveats

`confidence: low` — single project, self-reported PR-count change (12 → 6), no independent corroboration, and no measure of review-quality or defect-rate impact from the change (only qualitative benefits are reported: "reviewer sees whole feature," "eliminates rebases").

> **Gap:** No second project in this source corroborates the PR-count benefit, and no defect or review-cycle-time metric is available to strengthen the claim beyond the raw PR count and qualitative benefits reported.

---

[^1]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Process & Workflow > Lesson: Phase-Level PRs Over Per-Spec PRs.

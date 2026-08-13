---
title: "Raven Demo — Project Retrospective"
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

# Raven Demo — Project Retrospective

> **Framing note:** `raven_demo` is named explicitly once in the source document. Like the other two repos in this source, it reads as a personal/practice project, not an Ad Hoc client engagement — no client name, contract period, or delivery value appears in the source.[^1] This page uses neutral project-retrospective language rather than client/engagement framing.

## Summary

The source material attributes exactly one lesson to `raven_demo`, concerning end-to-end smoke testing cadence.[^2] Nothing else in the consolidated document names this repository, and this page is correspondingly thin — see the gap note below.

> **Gap:** No scope, client, delivery period, or approximate value is available. No functional bug root-causes, deployment issues, or database issues are attributed to `raven_demo` anywhere in the source, so this retrospective cannot cover those minimum-viable-page categories for this project.

## Key lesson and root cause

An end-to-end smoke test was run exactly once, at release time, rather than as part of every CI run. It passed on the first try. The source notes, as a retrospective/counterfactual judgment rather than a measured outcome, that if it had failed instead, debugging would have had to span 7 pull requests' worth of changes made since the smoke test was last run.[^2] The recorded best practice: run the smoke test in every CI pipeline, not only at release.

> **Gap:** The "7 PRs" figure describes what debugging *would have* required had the test failed — it is not a measured outcome from an actual failure, and there is no before/after comparison (e.g., an actual incident where a late smoke test caused a costly investigation). Confidence is capped at `low` and this claim is treated as qualitative for KB purposes.

## Root-cause themes

The single lesson available reflects a general pattern also seen (independently) in `meal_planner_app`'s stale-build issues: verification run late or infrequently allows drift to accumulate silently between checks.[^2] See `docs/anti-patterns/stale-build-artifact-false-negatives.md` for the related build-freshness pattern, which the source does not attribute to a named repository.

## Key personnel

> **Gap:** No individuals are named or citable in the source material for this project.

---

[^1]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — document header ("Repositories Analyzed") and Process & Workflow > Lesson: Automated Testing Early Catches Drift.
[^2]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Process & Workflow > Lesson: Automated Testing Early Catches Drift.

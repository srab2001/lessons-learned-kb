---
title: "Best Practice: Run the End-to-End Smoke Test on Every CI Run, Not Only at Release"
sources:
  - context/engagement-notes/consolidated-lessons-learned-2026-08-13.md
source_count: 1
as_of_date: "2026-08-13"
last_compiled: "2026-08-13"
lifecycle: draft
confidence: low
sensitivity: internal
lesson_type: [process, technical]
lifecycle_history:
  - date: "2026-08-13"
    from: ""
    to: draft
    reason: "initial synthesis from consolidated-lessons-learned-2026-08-13.md"
---

# Best Practice: Run the End-to-End Smoke Test on Every CI Run, Not Only at Release

## Practice statement

Run the end-to-end smoke test as part of every CI pipeline run, not only at release time, so drift accumulated across multiple changes is caught early rather than all at once.

## Evidence chain

On `raven_demo`, an end-to-end smoke test was run exactly once, at release time. It passed on the first try. The source notes, as a retrospective/counterfactual judgment rather than a measured outcome from an actual failure, that if the test had failed instead, debugging would have had to span 7 pull requests' worth of changes made since the test was last run.[^1]

See `docs/retrospectives/raven-demo.md` for the full project context.

## Related pattern

This practice is the direct countermeasure to the pattern documented in `docs/anti-patterns/stale-build-artifact-false-negatives.md` — both concern the same underlying risk (drift or a stale artifact going undetected between infrequent checks), though the source does not connect the two to the same project.

## Where it applies

Any project relying on an end-to-end or integration-level smoke test as its primary confidence check before release — the later and less frequent that check runs, the more accumulated change it has to account for if it fails.

## Confidence and evidence caveats

`confidence: low` — the "7 PRs" figure is the source's own estimate of what debugging *would have* required had the test failed; it is not a measured outcome from an actual failure, there is no before/after comparison, and the source documents a single project with no corroboration.

> **Gap:** No actual incident is documented where a late smoke test caused a costly investigation — the practice is supported here by a near-miss/counterfactual judgment only.

---

[^1]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Process & Workflow > Lesson: Automated Testing Early Catches Drift.

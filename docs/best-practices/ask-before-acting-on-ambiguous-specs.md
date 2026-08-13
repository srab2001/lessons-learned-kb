---
title: "Best Practice: Ask Before Acting on an Ambiguous Spec, Then Execute Silently Once Confirmed"
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

# Best Practice: Ask Before Acting on an Ambiguous Spec, Then Execute Silently Once Confirmed

## Practice statement

When a spec or prompt has a genuine fork in interpretation, pause and ask a clarifying question before proceeding. Once an interpretation or workflow has been explicitly confirmed, execute it repeatedly without re-confirming each similar step.

## Evidence chain

On `travel-deal-finder`, the original plan was one pull request per prompt (12 total). Partway through, a prompt said to "combine before merging" — a genuine fork relative to the original plan. Pausing to ask a clarifying question cost about 30 minutes of reconsidering the PR strategy; the source's own retrospective estimate is that guessing wrong and redoing the resulting work would have cost roughly 3 hours instead.[^1] This is the source's own estimate of an avoided cost, not an independently measured before/after, and is treated as illustrative rather than a validated benchmark — see the confidence note below.

The counterpart lesson, from the same project: once the PR workflow was explicitly confirmed (commit → push → CI → squash-merge → repeat), it was executed silently for 6+ iterations without re-confirming each time.[^2] The pairing of these two lessons is the point — asking is warranted at a genuine fork, not as a default habit for every step once the ambiguity is resolved.

See `docs/retrospectives/travel-deal-finder.md` for the full project context.

## Where it applies

Multi-step, prompt- or spec-driven development workflows (including AI-pair-programming task lists) where an early wrong assumption compounds across many subsequent, similar steps — the cost of guessing wrong scales with how many remaining steps depend on the guess.

## Confidence and evidence caveats

`confidence: low` — this is a single project's self-reported estimate of an avoided cost (30 minutes vs. an estimated 3 hours), not a measured, corroborated outcome, and it comes from a single, unreviewed source document. Per this session's scope, the "30 min vs. 3 hours" figure was considered as a possible basis for a `docs/recommendations/` entry (it is a genuine metric in the source), but was not promoted to one this session — see this session's PR description for the reasoning and the option to revisit in a follow-up session.

> **Gap:** No corroborating example from a second project is available in this source to raise confidence above `low`.

---

[^1]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Process & Workflow > Lesson: Ask Before Doing on Ambiguous Specs.
[^2]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Process & Workflow > Lesson: Don't Ask When Spec Is Unambiguous.

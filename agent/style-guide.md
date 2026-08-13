# Editorial style guide

Evolves through review cycles. Append new conventions as they emerge from PR feedback.

---

## Voice and tone

KB pages are written for delivery teams planning or steering an engagement, not for retrospective facilitators running the session. Write clearly and directly. Assume the reader has basic delivery/PM literacy but no context on the specific project.

## Recommendation format

Standard recommendation format:

> [Team/project] [action taken] [outcome] [metric], [time context if relevant].

Example:
> Running a 3-day technical spike before committing to the migration approach on Project X cut downstream rework by an estimated 20% compared to the prior engagement's mid-migration pivot.

Do not write:
- "We significantly improved..." (no metric, no specificity)
- "The team has extensive experience..." (not a recommendation)
- "Leveraging agile methodology..." (not an outcome)

## Retrospective scoping statements

Retrospective scope summaries should be 2–4 sentences, written to be lifted directly into a briefing for a new team. Active voice. Specific scope. Named client. Period.

Example:
> Delivery lead for the Example Project modernization, a 14-month engagement for Example Client from 2024–2025. Scope included platform migration, a phased cutover plan, and post-launch stabilization support.

## Metrics and approximations

- Always use the metric as stated in the source material
- If a range is given, use the range — do not pick a midpoint without flagging it
- If a metric is approximate per the source, note it: "approximately 20%"
- If a metric is inferred (not directly stated), mark `confidence: medium` and note the inference

## Gap notes

Write gap notes in blockquote format with the word **Gap:** in bold:

> **Gap:** No quantified outcome available for this workstream. Team reported "smoother rollout" but no before/after metric was captured.

## Contradiction notes

> **Contradiction:** `context/retrospectives/example-project-2026.md` states the migration completed in 14 months; `context/engagement-notes/example-project-status.md` states 16 months. Awaiting maintainer resolution before promoting to active.

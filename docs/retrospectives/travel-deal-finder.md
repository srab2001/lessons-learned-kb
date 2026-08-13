---
title: "Travel Deal Finder — Project Retrospective"
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

# Travel Deal Finder — Project Retrospective

> **Framing note:** `travel-deal-finder` is named explicitly in the source document's Process & Workflow section, but — like the other two repos in this source — reads as a personal/practice project, not an Ad Hoc client engagement. No client name, contract period, or delivery value appears anywhere in the source.[^1] This page uses neutral project-retrospective language rather than client/engagement framing.

## Summary

`travel-deal-finder` is a flight-deal search pipeline built against a third-party flight API (Kiwi), developed through a series of scoped prompts/specs executed as a sequence of pull requests.[^2] The lessons captured for this project are entirely process- and testability-oriented — how work was scoped into PRs, how ambiguity in the spec was handled, and how the project's I/O and config were structured to stay testable. No functional bug root-causes are attributed to this project in the source (compare `docs/retrospectives/meal-planner-app.md`, which is bug/incident-heavy).

> **Gap:** No scope, client, delivery period, or approximate value is available in the source material.

## Key lessons and root causes

### Spec ambiguity handled by asking, not guessing

The original plan was one PR per prompt (12 total). Partway through, a prompt said to "combine before merging" — a genuine fork in interpretation relative to the original plan. Pausing to ask a clarifying question cost about 30 minutes of reconsidering the PR strategy; the source estimates that guessing wrong and redoing the resulting work would have cost about 3 hours.[^3] This is presented in the source as the team's own retrospective estimate of an avoided cost, not a measured before/after — see the corresponding best-practice page for how this is treated for confidence purposes.

Once the PR workflow was confirmed (commit → push → CI → squash-merge → repeat), it was executed silently for 6+ iterations without re-confirming each time — the counterpart lesson to the one above: ask when a spec forks, don't ask once it's unambiguous.[^4] This lesson does not explicitly name `travel-deal-finder`, but immediately follows and shares the same workflow narrative as the explicitly-named lesson above; the attribution here is contextual, not stated outright.

### PR sizing changed mid-project

The PR strategy changed from one PR per spec line to one PR per coherent feature phase, reducing the total from a planned 12 PRs to 6.[^5] Reported benefits: a reviewer sees the "whole feature" in one PR, inter-prompt rebases are eliminated, and the PR description can explain how the pieces fit together. The rule of thumb recorded: the right PR size is "one coherent feature," not "one spec line" — combine prompts into a phase when they touch overlapping code. This lesson also does not repeat the repo name explicitly, but its "12 total" → "6 PRs" figures match the plan described in the explicitly-named ask-before-doing lesson directly above it in the source, which is the basis for attributing it here.

### I/O designed to be testable from the start

Every module doing I/O accepted an injectable options bag (`fetchImpl`, `sleep`, `now`, `rng`, `logger`, `cronImpl`, `fsImpl`). Reported payoff: 91 tests ran in under 100ms with no real timers or network calls, and the Kiwi flight API's fallback path was testable without an API key. The estimated upfront cost was about 5 lines per module, with the cost paid back "the first time you write a test."[^6]

Related: any external dependency shipped a believable mock/fallback. If `FLIGHT_API_KEY` was unset or the live API returned a 500, the pipeline generated deterministic mock data instead. Reported effect: new contributors could run the full pipeline in under 5 minutes with no signups, CI exercised the full flow without secrets, and a bad API key never broke a production run.[^7] This lesson does not name a repository explicitly, but its flight-search / `FLIGHT_API_KEY` domain matches `travel-deal-finder`; the attribution is contextual.

### Schema renamed mid-project without a lock

A config field was named `origins` in one phase, then renamed to `departureAirports` in a later phase, requiring three modules plus a test file to change.[^8] The prevention approach recorded: lock the `config.json` schema in one source of truth (e.g., a `DEFAULT_CONFIG` constant in a config manager module) and treat schema changes as breaking-change PRs going forward.

## Root-cause themes

The recurring theme across these lessons is that process and design decisions made early (PR granularity, I/O injectability, schema ownership) compounded in cost or savings as the project scaled to more prompts/phases — the source frames all four workflow lessons as things that either paid off repeatedly once fixed, or cost repeated rework because they weren't fixed early.[^3][^5][^6][^8]

> **Gap:** No independent metric verifies the "91 tests," "6 PRs," "<5 minutes," or "30 min vs. 3 hours" figures beyond the source's own account — this is a single, self-reported project retrospective, not a corroborated benchmark. Confidence is capped at `low`.

## Key personnel

> **Gap:** No individuals are named or citable in the source material for this project.

---

[^1]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — document header ("Repositories Analyzed") and Process & Workflow section generally.
[^2]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Process & Workflow > Lesson: Injectable I/O Pays For Itself Immediately (Kiwi API reference).
[^3]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Process & Workflow > Lesson: Ask Before Doing on Ambiguous Specs.
[^4]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Process & Workflow > Lesson: Don't Ask When Spec Is Unambiguous.
[^5]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Process & Workflow > Lesson: Phase-Level PRs Over Per-Spec PRs.
[^6]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Process & Workflow > Lesson: Injectable I/O Pays For Itself Immediately.
[^7]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Process & Workflow > Lesson: Mock-First, Real-API-Second.
[^8]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Process & Workflow > Lesson: Lock Schema Once.

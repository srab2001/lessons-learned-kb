---
title: "Best Practice: Design External I/O for Testability and Ship a Mock-First Fallback"
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

# Best Practice: Design External I/O for Testability and Ship a Mock-First Fallback

## Practice statement

Give every module that performs I/O an injectable options bag (e.g., a fetch implementation, sleep/clock, RNG, logger, cron, filesystem), and ship a believable, deterministic mock/fallback for any external dependency — so a local or CI run never depends on live network access or a valid credential by default.

## Evidence chain

On `travel-deal-finder`, every I/O-performing module accepted an injectable options bag: `fetchImpl`, `sleep`, `now`, `rng`, `logger`, `cronImpl`, `fsImpl`. The reported upfront cost was about 5 lines per module, with the cost paid back "the first time you write a test." Reported payoff: 91 tests ran in under 100ms with no real timers or network calls, and the Kiwi flight API's fallback path was testable without an API key.[^1]

Related, in the same project's domain (flight search / `FLIGHT_API_KEY`): if the flight API key was unset, or the live API returned a 500, the pipeline generated deterministic mock data instead of failing. Reported effect: new contributors could run the full pipeline in under 5 minutes with no signups, CI exercised the full flow without secrets, and a bad API key never broke a production run. The source's own framing: *"It worked locally" should never depend on credentials.*[^2] This second lesson block does not repeat the repository name, but its flight-search domain and `FLIGHT_API_KEY` reference match `travel-deal-finder`'s domain; the attribution is inferred from that match.

See `docs/retrospectives/travel-deal-finder.md` for the full project context.

## Where it applies

Pipelines and integrations that depend on an external, rate-limited, or credentialed API — the injectable-I/O and mock-first patterns specifically address making local development, CI, and test suites independent of that external dependency's availability or credentials.

## Confidence and evidence caveats

`confidence: low` — single project, self-reported test-count and timing figures (91 tests, <100ms, <5 minutes), no independent corroboration. Per this session's scope, the 91-tests/<100ms and <5-minute figures were considered as possible bases for a `docs/recommendations/` entry (they are genuine metrics in the source), but were not promoted to one this session — see this session's PR description for the reasoning and the option to revisit in a follow-up session.

> **Gap:** No second project in this source corroborates either the injectable-I/O or mock-first pattern's reported payoff.

---

[^1]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Process & Workflow > Lesson: Injectable I/O Pays For Itself Immediately.
[^2]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Process & Workflow > Lesson: Mock-First, Real-API-Second.

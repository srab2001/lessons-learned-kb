---
title: "Raven Demo — Project Retrospective"
sources:
  - context/engagement-notes/consolidated-lessons-learned-2026-08-13.md
  - context/anti-patterns-raw/raven-demo-lessons-learned.md
source_count: 2
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
  - date: "2026-08-13"
    from: draft
    to: draft
    reason: "substantially expanded from a single thin lesson to three attributed root-cause incidents, via raven_demo's own lessons-learned doc (context/anti-patterns-raw/raven-demo-lessons-learned.md)"
---

# Raven Demo — Project Retrospective

> **Framing note:** `raven_demo` reads as a personal/practice project, not an Ad Hoc client engagement — no client name, contract period, or delivery value appears in either source.[^1] This page uses neutral project-retrospective language rather than client/engagement framing.

## Summary

Initially synthesized from a single lesson (smoke-test cadence) in the consolidated source, which named `raven_demo` only once.[^1] Locating and ingesting the project's own, more detailed lessons-learned document resolved two attribution gaps left open elsewhere in this KB and substantially expanded what can be said about this project: three distinct root-cause incidents are now attributable here, all arising while building a Google OAuth + admin-approval feature gating three demo apps.[^3]

> **Gap:** Still no scope, client, delivery period, or approximate value available for this project in either source.

## Key lessons and root causes

**1. ESM-only dependency crashed a Vercel serverless function after a clean build.** After shipping Google OAuth + admin-approval, production returned `FUNCTION_INVOCATION_FAILED` on `/api/auth/google/start` and related routes; a `"type": "module"` fix appeared to work once, then the identical crash reappeared on the next cache-clean deploy — the signal that the module-config change wasn't the real lever. Root cause: the `jose` JWT library is ESM-only and Vercel's bundler wasn't reliably propagating the module-format signal into the runtime. Fixed by replacing `jose` with a Web Crypto–only implementation, which is inert to bundler format and also runs in Edge Runtime (used by this project's middleware).[^3] Full writeup: `docs/anti-patterns/esm-only-dependency-crash-in-serverless.md`.

**2. A stale build artifact hid a real race-condition bug for an hour.** Playwright verification against a `/how-its-built` page's save/reset flow kept failing for reasons that didn't add up (manual `fetch` calls worked, logging showed success) — the actual cause was that the source file had been edited after the last build, so verification was testing old compiled output. Once rebuilt, a real bug surfaced underneath: a save handler's success message was being cleared as a side effect of an unrelated dropdown refresh.[^3] Full writeup: `docs/anti-patterns/stale-build-artifact-false-negatives.md`.

**3. Two Vercel projects tracked the same repo with separate environment variables and production bindings.** Recorded as a general takeaway from the same feature effort, not tied to a specific dated incident in the source: before concluding an env var is missing or a fix didn't ship, confirm which project's domain is actually being tested.[^3] See `docs/anti-patterns/environment-variable-misconfiguration.md`.

**4. (Previously synthesized) End-to-end smoke test run only at release, not every CI run.** It passed on the first try; the source notes as a counterfactual judgment, not a measured outcome, that a failure would have required debugging across roughly 7 pull requests' worth of accumulated changes.[^2] The recorded best practice: run the smoke test in every CI pipeline, not only at release.

> **Gap:** The "7 PRs" figure describes what debugging *would have* required had the test failed — not a measured outcome from an actual failure. Confidence on this specific claim is capped at `low` and it's treated as qualitative for KB purposes; this caps the whole page's confidence, since it's the only claim here framed as a quantified-sounding figure without being an actual measurement.

## Root-cause themes

Two related but distinct verification-timing failure modes appear across these incidents: a build succeeding says nothing about whether the deployed artifact actually works at request time (incident 1), and a build existing says nothing about whether it's the *current* build (incident 2) — "the build looks fine" isn't the same claim as "what I'm testing reflects my latest change."[^3] This is the same theme independently present in `meal_planner_app`'s stale-build issues (see `docs/anti-patterns/stale-build-artifact-false-negatives.md`, which now attributes both projects' instances of this pattern).

## Key personnel

> **Gap:** No individuals are named or citable in either source for this project.

---

[^1]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — document header ("Repositories Analyzed") and Process & Workflow > Lesson: Automated Testing Early Catches Drift.
[^2]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Process & Workflow > Lesson: Automated Testing Early Catches Drift.
[^3]: context/anti-patterns-raw/raven-demo-lessons-learned.md — full document (both incidents) and "Source" section (repo attribution, feature context).

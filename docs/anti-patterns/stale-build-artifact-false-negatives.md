---
title: "Anti-Pattern: Verifying Against a Stale Build Artifact"
sources:
  - context/engagement-notes/consolidated-lessons-learned-2026-08-13.md
  - context/anti-patterns-raw/raven-demo-lessons-learned.md
source_count: 2
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
  - date: "2026-08-13"
    from: draft
    to: draft
    reason: "attribution resolved via raven_demo's own lessons-learned doc -- confirms the topical link this page already flagged with docs/retrospectives/raven-demo.md was in fact the same project, not just a similar pattern"
---

# Anti-Pattern: Verifying Against a Stale Build Artifact

**Attribution:** [`raven_demo`](https://github.com/srab2001/raven_demo) — encountered while building the `/how-its-built` walkthrough page (a static HTML page with inline JS, no bundler), including a live editor that saves and resets content via the same admin API the `/admin` panel uses.[^3] Previously listed as an attribution gap; this page had already flagged a *topical* connection to `raven_demo`'s smoke-test-cadence lesson without evidence they were the same project — they turn out to be, confirmed now by this project's own lessons-learned document.

## What the pattern looks like

A source file is edited, but the compiled/bundled output (e.g., a `dist/` directory) is not rebuilt before running verification (tests, manual checks, or automated checks). Verification then runs against stale code, and any failure investigation chases the wrong cause.

## Failure mode / symptom

Verification kept failing against an outdated `dist/` output because a source file had been edited after the last `npm run build`. The source reports that about an hour was spent debugging "bugs" that were actually artifacts of the stale build, before the real cause (an out-of-date compiled file) was identified.[^1] The same underlying pattern is described a second time under Testing & Code Quality: a Playwright test was failing, manual `fetch` calls were working, and request logging showed success — all pointing at different candidate causes (routing, mocking, element lookup) — when the actual cause was that the test was exercising stale compiled code.[^2] The `raven_demo` source names the specific file and mechanism: Playwright verification against the built `dist/` output kept failing on a save/reset flow because `how-its-built/index.html` had been edited after the last build, so every run tested the old, unbuilt copy; `diff`-ing source against the built copy showed the divergence immediately.[^3]

**A deeper example, once the stale-build issue itself was fixed:** a second, subtler bug surfaced. A save handler set a success message (`'Saved...'`), then called a `loadContentItems()` refresh function; the dropdown-refresh, as a side effect, cleared the success message. The message was visible for about 100ms before being silently overwritten. This was invisible to manual testing (a glance-and-move-on check) but would reliably fail any automated check that waits for the message to persist.[^1][^3] Specifically: the handler set the message on `#editor-result`, then called `loadContentItems()` to refresh a dropdown, which re-selected the current item and cleared that same message as a side effect.[^3]

## Warning signs

- A check that "should" pass keeps failing for reasons that don't add up across multiple candidate explanations.
- Manual, glance-based verification looks fine, but a more deliberate automated check (one that waits for an expected state) fails.
- Debugging effort is being spent on the failing check's surrounding logic (routing, mocking, data) without first confirming the artifact under test reflects the current source.

## What to do instead

1. Rebuild before every verification step, as a fixed sequence rather than an occasional afterthought: `npm run build` then run tests/checks.[^1][^2][^3]
2. When a check that should pass keeps failing for reasons that don't add up, first verify the artifact under test is actually current — only then debug the failure itself.[^2][^3]
3. Only clear status/feedback messages on a genuinely user-initiated action; never clear them as a side effect of an unrelated data refresh, since state changes hidden inside side effects are invisible to manual testing but will reliably break automated checks that wait for that state.[^1][^3]
4. Treat automated checks that wait for output as a feature, not a nuisance — they catch exactly the class of race-condition/side-effect bug described above immediately, where manual testing would miss it.[^1][^3]

> **Gap:** No metric is available beyond the self-reported "about an hour" spent debugging the first instance of this pattern — there is no measure of how often this recurred, or of impact before the "always rebuild first" practice was adopted.

---

[^1]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Deployment & Vercel > Issue: Build Cache Causing Stale Artifacts (including the "Deep-Dive Example" subsection).
[^2]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Testing & Code Quality > Issue: Stale Build Causing False Debug Output.
[^3]: context/anti-patterns-raw/raven-demo-lessons-learned.md — "'Verified' against a stale build, and a race condition hidden by it" (full incident) and "Source" section (repo attribution).

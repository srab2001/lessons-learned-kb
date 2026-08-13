# KB structure — Lessons Learned KB

This document defines the editorial scope and intent of each section in the Lessons Learned KB. The agent must read this file before creating or substantially revising any KB page. If a proposed page does not fit a defined section, flag it in the PR for maintainer direction before creating it.

---

## Design constraints

The KB is small by design. Prefer fewer, richer pages over broad shallow coverage. A page that a delivery lead would actually cite is worth more than ten pages that are too thin to use. Pages should be reuse-ready — someone pulling from this KB should be able to act on the content directly, not synthesize it further.

Every page covers a bounded entity (one project, one client, one practice area) or a bounded synthesis topic (recommendations for a given capability). Do not create summary-of-summaries pages or meta-commentary pages.

---

## Sections

### `docs/retrospectives/`

**One page per project or engagement.**

Covers the substantive retrospective records the org can draw on when planning future work. Each page is a structured profile of one engagement: scope, period, client, outcomes, root causes of what went well or poorly, and available metrics. The goal is a page a delivery lead can pull from when scoping a similar engagement or briefing a new team.

**What goes here:** Projects the org has delivered that are worth learning from — successes and failures alike. Engagements too old to be relevant (ended 8+ years ago for most purposes) should be marked `archived` rather than deleted.

**What does not go here:** Teaming-partner-only retrospectives with no direct involvement, engagements still in active delivery with no available retrospective material, hypothetical or anticipated work.

**Minimum viable page:**
- Project name, client, period, engagement type, approximate scope/value
- Summary (2–3 sentences)
- Key outcomes with metrics where available
- Root-cause notes for anything that went notably well or poorly
- Key personnel if citable
- `lesson_type: []` populated with whichever of `process | technical | people-org | client-relationship | tooling` the page substantively covers

---

### `docs/recommendations/`

**One page per capability area.** Each page is a curated list of recommendations for that capability.

Recommendations are the most reusable KB artifacts. A recommendation is a single claim — grounded in a measurable outcome — that tells a future team what to do differently (or keep doing) in a specific domain.

**Capability areas (define pages for each that has sufficient source material):**
- `agile-delivery.md`
- `customer-experience.md`
- `platform-engineering.md`
- `data-and-analytics.md`
- `cloud-infrastructure.md`
- `accessibility.md`
- `program-management.md`

**What goes here:** Quantified, actionable claims derived from retrospectives and incident reviews. Each recommendation must meet the full recommendation standard defined in `CLAUDE.md`.

**What does not go here:** Qualitative claims without metrics (put those in the relevant retrospective page with `confidence: low`), generic advice, unverified assertions.

---

### `docs/incident-reviews/`

**One page per reviewed incident or postmortem.**

Incident reviews capture what actually happened, the root cause, decision drivers, and what would have been done differently. This is the most sensitive section — raw postmortem notes and stakeholder feedback are `restricted` by default. Synthesized lessons that do not expose source-level detail may be promoted to `internal`.

**What goes here:** Postmortems (written or oral), root-cause analyses, decision-driver synthesis, lessons captured in retrospectives.

**What does not go here:** Speculative analysis without a source, unattributed rumors.

**Sensitivity default:** `restricted`. Specific lessons that are abstracted from raw feedback (e.g., "the on-call rotation lacked a clear escalation path" without naming individuals) may be promoted to `internal` by maintainer direction.

---

### `docs/capability-areas/`

**One page per service line.** Synthesis pages that pull across multiple projects and recommendations to tell a coherent story about how the org works in that area.

These are the pages most directly useful when scoping new work — a delivery lead planning an agile-delivery-heavy engagement should be able to read `agile-delivery.md` and have enough context to plan discriminating practices.

**What goes here:** Cross-project synthesis of the org's approach, methodology, tooling, and outcomes in each service line. Links to supporting retrospectives and recommendations.

**What does not go here:** Project-specific detail (that lives in retrospectives), individual recommendations (those live in recommendations), or client-specific context.

**Sensitivity default:** `public`.

---

### `docs/best-practices/`

**One page per canonical practice.** A best practice is a specific, verifiable approach the org has proven works — not a vague strength ("we're good at agile") but a specific practice with an evidence chain ("running a 3-day spike before committing to a data migration approach cut rework by X on two of the last three legacy-migration engagements").

**What goes here:** The canonical practice statement (1–2 sentences, precision-written), the evidence chain that supports it (links to retrospectives, recommendations), and where it applies.

**What does not go here:** Practices that cannot be supported by evidence in the KB, generic industry advice.

**Sensitivity default:** `public` for the practice statement and evidence chain.

---

### `docs/client-context/`

**One page per client or agency the org has a working relationship with.**

Client context pages capture institutional knowledge about how a client works, what they value, who the key stakeholders are, and what the org's engagement history has been.

**What goes here:** Client-specific working patterns, stakeholder history, communication preferences, known constraints, engagement history.

**What does not go here:** Information that cannot be sourced from engagement notes or explicit team communication.

**Sensitivity default:** `internal`. Sections discussing specific individuals' working style based on direct feedback → `restricted`.

---

### `docs/anti-patterns/`

**One page per documented failure pattern.** Pages synthesize what is known about a specific way an engagement has gone wrong, so future teams can recognize the pattern early.

**What goes here:** Documented mistakes, near-misses, and failure patterns with evidence from retrospectives or incident reviews; what the warning signs looked like; what should be done instead.

**What does not go here:** Speculation without a source, blame directed at individuals.

**Sensitivity default:** `internal`. Promote to `public` only for patterns generic enough to share broadly with no client- or person-identifying detail.

> **Note:** this section did not exist in the template this repo was bootstrapped from (`proposal-intelligence-kb` had a `competitive-intelligence/` section here instead, which is proposal-capture-specific and has no lessons-learned analog). `anti-patterns/` was added as a best-effort replacement — reconsider the name and scope if it doesn't fit how the team actually wants to use this KB.

---

## Pages that do not belong in this KB

The following content types should not be created as KB pages, regardless of available source material:

- **Status reporting** — sprint status, burndown, RAG reports belong in project tracking tools, not here
- **Staffing plans or org charts** — too project-specific and volatile to maintain here
- **Generic methodology descriptions** — if it applies to all teams equally, it is not KB content

---

## Index file

`docs/_kb-index.yaml` is the page catalog. The agent maintains it as pages are created and updated. Format:

```yaml
pages:
  - path: docs/retrospectives/example-project.md
    title: "Example Project"
    section: retrospectives
    lifecycle: active
    confidence: high
    sensitivity: internal
    as_of_date: "2026-01-15"
    summary: "..."
    related:
      - docs/recommendations/agile-delivery.md
```

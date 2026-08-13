---
name: kb-retrospective
description: Synthesizes a raw retrospective source file (context/retrospectives/*.md) into a structured Lessons Learned KB page (docs/retrospectives/*.md) following the KB verifiability, traceability, and temporal clarity principles
version: 1.0.0
triggers:
  - "synthesize retrospective"
  - "create kb page"
  - "kb retrospective"
  - "ingest retrospective"
mode: prototype
output: markdown
---

# KB Retrospective Synthesis Skill

This skill replaces the ad-hoc synthesis prompt used in the offline ingestion workflow. Follow every rule below without exception. These rules are load-bearing — skipping any one of them produces a page that fails KB review.

---

## 1. Input

You are given a path to a context file under `context/retrospectives/`. That file is your **only** authoritative source for this synthesis. Read it completely before writing a single word of the KB page.

If the file references other documents (status reports, exit interviews, incident tickets), note the reference as a gap unless those documents are also present as context files.

---

## 2. KB Rules — Internalize Before Writing

These rules are non-negotiable. Review them before drafting.

### Verifiability
- **Never invent metrics not in the source material.** If a number does not appear in the context file, it does not appear in the KB page. "Significantly improved performance" is not a recommendation.
- Every quantified claim must be traceable to a specific sentence or table in the source file.
- If the source is qualitative only, the page confidence cannot exceed `low`.

### Traceability
- Every factual claim gets a `[^N]` footnote referencing the context file by path and, when possible, the specific section or quote.
- Do not write a claim that lacks a footnote. If you cannot cite it, write a gap note instead.

### Temporal Clarity
- `as_of_date` must come from the source material (engagement end date, document date, or stated period), never from today's date.
- Claims that are time-sensitive (user counts, cost savings, team size) must be date-stamped inline: "as of Q3 2025" or "during the stabilization phase (Jan–Mar 2026)".
- If the engagement ended more than 5 years before `last_compiled`, add a staleness notice at the top of the page body: `> **Staleness Notice:** This engagement ended more than 5 years ago. Details should be verified before reuse.`

### Lifecycle and Sensitivity
- Always set `lifecycle: draft` for new pages. Never mark a page `active` without explicit reviewer approval in a PR comment.
- Set `sensitivity: internal` for material from `context/retrospectives/` unless the file itself is marked otherwise.
- If the source file contains incident feedback, personnel-specific critique, or sensitive client detail, set `sensitivity: restricted` and note the reason.

### Frontmatter — Required Fields (no omissions)

```yaml
---
title: ""
sources:
  - context/retrospectives/<filename>.md
source_count: 1
as_of_date: "YYYY-MM-DD"         # from source material, not today
last_compiled: "YYYY-MM-DD"      # today's date when you write the page
lifecycle: draft
confidence: low                  # see confidence rules below
sensitivity: internal
lesson_type: []                  # see lesson-type guidance below
lifecycle_history:
  - date: "YYYY-MM-DD"
    from: ""
    to: draft
    reason: "initial synthesis from context/retrospectives/<filename>.md"
---
```

### Gap Notes
When source material is absent for a required section, write an explicit gap note — never leave the section empty or write vague filler:

```
> **Gap:** [What is missing and why it matters for reuse.]
```

---

## 3. Output Structure

Every retrospective KB page must have exactly these 8 sections in this order.

### Section 1 — Engagement Overview

A markdown table with these fields (use "Not in source" for any field absent from the source material):

| Field | Value |
|---|---|
| Client | |
| Engagement Type | |
| Period | |
| Approximate Scope/Value | |
| Team Size | |
| Role (lead / partner / sub-team) | |

### Section 2 — Program Summary

2–4 paragraphs covering:
- What the engagement delivered (scope, system, or service)
- The user population or beneficiary (size and type if available)
- Why this work mattered

Cite the source for every factual claim.

### Section 3 — Key Personnel Roles

A list of named roles and responsibilities drawn from the source. If specific names are available, include them only if they appear in the source (never infer). If no personnel information is in the source, write a gap note.

### Section 4 — What Happened

Bullets covering:
- Key decisions made and why (only what is in the source)
- What went well
- What went poorly

Do not editorialize. Stick to what the source states.

### Section 5 — Quantified Outcomes

**The most important section.** Only include metrics that appear in the source material.

Format each outcome as:

> **[Outcome label]:** [Metric] [^N]

If the source contains no quantified outcomes, this section must contain:

> **Gap:** No quantified outcomes found in source material. Confidence cannot exceed `low` until metrics are provided.

### Section 6 — Reusable Highlights

2–5 highlights suitable for briefing a new team starting similar work. Each should be a single sentence with a metric and a source footnote.

If confidence is `low`, add this notice:

> **Note:** Page is `lifecycle: draft` and `confidence: low`. These highlights should be verified against primary source before reuse.

### Section 7 — Related KB Pages

Links to related pages in the KB. Use relative markdown links. Include:
- Relevant `recommendations/` pages
- Relevant `best-practices/` or `anti-patterns/` pages
- Other `retrospectives/` pages for the same client

If no related pages exist yet, write:

> **Gap:** No related KB pages linked. Update this section as recommendations and best-practice pages are developed.

### Section 8 — Footnotes

List every footnote used in the page. Format:

```
[^1]: context/retrospectives/<filename>.md — [brief description of cited content, e.g., "Engagement Overview table, Period field"]
```

Every footnote must be traceable to a specific location in the source file. Vague footnotes ("source document") are not acceptable.

---

## 4. Confidence Rules

Apply these rules mechanically — do not upgrade confidence based on judgment alone.

| Level | Criteria |
|---|---|
| `high` | 2 or more independent sources, OR 1 primary source with 3 or more specific quantified metrics |
| `medium` | 1 source with at least 1 specific quantified metric (percentage, dollar amount, user count, timeline) |
| `low` | Qualitative only, no quantified metrics, or source is ambiguous about scope/outcomes |

When in doubt, assign the lower confidence level. It is always easier to promote than to correct a page that was over-confident.

---

## 5. Lesson-Type Mapping Guidance

Use these definitions to populate `lesson_type`. A page may have multiple lesson types.

| Lesson Type | What Belongs Here |
|---|---|
| `technical` | Architecture decisions, DevOps pipeline design, platform engineering, accessibility, API design, cloud migration approach |
| `process` | Delivery methodology, cadence, ceremonies, planning approach |
| `people-org` | Staffing approach, team structure, onboarding, subcontractor management |
| `client-relationship` | Stakeholder management, communication patterns, escalation handling |
| `tooling` | Tooling choices, automation, internal platform decisions |

If a section of the page is relevant to a lesson type, include it. If no information in the source supports a type, do not include it.

---

## 6. After Writing the Page

Before closing the session, you must do two things:

**Update the manifest.** Open `context/retrospectives/manifest.yaml` and add or update the entry for the source file you processed:

```yaml
- path: <filename>.md
  as_of_date: "YYYY-MM-DD"       # from the source file
  content_hash: "sha256:..."     # run: shasum -a 256 context/retrospectives/<filename>.md
  temporal_status: current       # current | aging | aged-out
  sensitivity: internal
  kb_impact:
    - docs/retrospectives/<slug>.md
```

To get the SHA256 hash:
```bash
shasum -a 256 context/retrospectives/<filename>.md
```

**Verify the output file.** Re-read the page you wrote and confirm:
- [ ] Every section is present (or has an explicit gap note)
- [ ] Every factual claim has a `[^N]` footnote
- [ ] No metric appears that is not in the source
- [ ] `lifecycle: draft` is set
- [ ] `as_of_date` is from the source, not today
- [ ] `last_compiled` is today's date
- [ ] `lesson_type` reflects actual content in the page
- [ ] Manifest is updated

Do not open a PR until this checklist is complete.

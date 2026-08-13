# Lessons Learned KB

An AI-curated, human-governed knowledge base that synthesizes project retrospectives, incident reviews, and delivery data into verified, traceable lessons for future engagements.

**Humans curate context. The agent writes. Reviewers approve.**

---

## What this is

This KB is a lessons-learned layer between raw delivery source material (retrospectives, postmortems, engagement notes) and the teams planning the next engagement. It maintains a small number of high-confidence, deeply traceable KB pages — project retrospectives, recommendations, best practices, anti-patterns, and client context — that teams can pull from when starting or steering an engagement.

This is not a project management tool. It is a knowledge curation tool.

---

## How it works

1. **Source material** lands in `context/` — retrospective notes, incident/postmortem writeups, engagement notes, raw metrics
2. **A maintainer runs a session** — opens a conversation with an LLM, points it at new context files, and steers synthesis in real time
3. **The agent synthesizes** — drafts or updates KB pages, traces every claim to source files, notes gaps explicitly, assigns sensitivity and confidence
4. **The agent opens a PR** — writes a description documenting every editorial decision; never merges its own PRs
5. **A human reviewer approves** — confirms sensitivity classifications, resolves contradictions, promotes lifecycle state
6. **Merged pages ship to the wiki** — a GitHub Action rebuilds the static site on merge to `main`

> **Note: Importing a source file does not automatically update wiki pages.** Source files require a synthesis session before KB content is updated:
> 1. The imported file lands in `context/<folder>/` in the KB repo.
> 2. Open a new Claude session, load it as a KB agent, and synthesize the new source into the relevant `docs/` page.
> 3. The agent opens a PR; a maintainer reviews and merges.
> 4. The GitHub Action rebuilds `wiki/site/` automatically on merge to `main`.

---

## Directory structure

```
lessons-learned-kb/
├── CLAUDE.md                    # Agent identity, rules, safety rails
├── structure.md                 # KB section scope and editorial intent
├── README.md
│
├── agent/
│   ├── agents.md                # Session workflow, branching, PR conventions
│   ├── journal.md               # Append-only editorial decision log
│   ├── style-guide.md           # Evolving conventions from review cycles
│   └── log.md                   # Machine-parseable session audit trail
│
├── context/                     # Human-curated raw source material
│   ├── manifest.yaml            # Root manifest
│   ├── retrospectives/          # Project completion notes, sprint retros, exit interviews
│   ├── incident-reviews-raw/    # Postmortem notes, evaluator/stakeholder feedback (RESTRICTED)
│   ├── engagement-notes/        # Internal status notes, working docs (INTERNAL)
│   ├── anti-patterns-raw/       # Documented failure patterns, near-misses (RESTRICTED)
│   ├── recommendations-raw/     # Raw metrics, survey results (INTERNAL)
│   ├── capability-areas/        # Cross-project practice-area notes (public)
│   └── best-practices-raw/      # Draft practice statements (INTERNAL)
│
└── docs/                        # Agent-written, human-approved KB pages
    ├── _kb-index.yaml           # Page catalog
    ├── retrospectives/          # One page per project/engagement
    ├── recommendations/         # One page per capability area
    ├── incident-reviews/        # One page per incident or reviewed engagement
    ├── capability-areas/        # Cross-project service-line synthesis
    ├── best-practices/          # Canonical practice statements
    ├── client-context/          # Client/agency working patterns and history
    └── anti-patterns/           # Documented failure patterns to avoid
```

---

## Sensitivity levels

| Level | Meaning | Wiki-published? |
|---|---|---|
| `public` | Ready to share broadly inside the org | Yes |
| `internal` | Internal analysis; not for external sharing | Yes, to logged-in KB users |
| `restricted` | Postmortem/incident feedback, sensitive client detail | Yes, to logged-in KB users |

The wiki itself is never publicly reachable — every page requires Google sign-in and membership on the `ALLOWED_KB_EMAILS` allow-list (see `middleware.js`/`api/auth/`). That allow-list *is* the KB maintainer group referenced in `CLAUDE.md`'s sensitivity definitions, so once a user is allowed to log in at all, they see every sensitivity level, not just `public`. There is no further per-page or per-user filtering beyond that single login gate.

---

## Starting a session

Open a conversation with your LLM. Tell it:
- Which context files to process
- What type of session (synthesis, maintenance, lint)
- Any direction from prior PR feedback

The agent reads `agent/journal.md` and `structure.md` before doing anything else.

---

## First steps

1. Add your first retrospective source files to `context/retrospectives/`
2. Update `context/retrospectives/manifest.yaml` with an entry for each file
3. Run a synthesis session to create the first `docs/retrospectives/` pages
4. Open the first PR

---

## Notes on this initial scaffold

This repo was bootstrapped from [`proposal-intelligence-kb`](https://github.com/srab2001/proposal-intelligence-kb), an existing Ad Hoc knowledge-base template built for proposal capture. The architecture, tooling, and workflow are preserved; the KB taxonomy and identity have been retargeted for lessons-learned content. See the PR description for the full list of what was ported, renamed, or intentionally left out because it only made sense for proposal work.

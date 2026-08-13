---
title: "Lessons Learned KB — Design"
sources: []
source_count: 0
as_of_date: "2026-08-13"
last_compiled: "2026-08-13"
lifecycle: active
confidence: high
sensitivity: internal
lesson_type: []
lifecycle_history:
  - date: "2026-08-13"
    from: ""
    to: active
    reason: "initial design doc for the standalone KB"
---

# Lessons Learned KB — Design

## What this is

A standalone GitHub repo + Vercel static site: markdown KB pages in `docs/`, built by MkDocs into `wiki/site/`, gated by a small Google-OAuth layer (`middleware.js`, `api/auth/`). There is no database and no downstream sync target — this is simpler than the template it was bootstrapped from.

## Components

| Component | Role |
|---|---|
| `context/` | Human-curated raw source material, organized by folder with sensitivity defaults |
| `docs/` | Agent-written, human-approved KB pages (source of truth) |
| `docs/_kb-index.yaml` | Page catalog |
| `wiki/docs/` | MkDocs source tree — wiki-only nav pages live here directly; individual KB pages get symlinked in from `docs/<section>/` as they're created (see `.github/workflows/kb-synthesis.yml` step 4) |
| `wiki/site/` | Built static site, committed by the `Build Wiki` action, served by Vercel |
| `middleware.js` + `api/auth/` | Google OAuth gate — session cookie or a shared-secret header (`KB_ACCESS_TOKEN`) |
| `.claude/agents/kb-synthesis.md`, `.claude/skills/kb-retrospective/` | Claude Code synthesis agent and skill |
| `.github/workflows/kb-synthesis.yml` | Optional CI path: `workflow_dispatch` to synthesize a specific new context file directly to `main` (no PR) |
| `.github/workflows/build-wiki.yml` | Rebuilds and deploys the wiki on any push to `main` touching `docs/**` or `wiki/**` |

## What was intentionally left out

This KB was bootstrapped from `proposal-intelligence-kb`, whose design describes a second Vercel app (`solution-architecture`) with a Neon Postgres database that ingests this KB's public pages via a `sync-kb` route into `IngestChunk`/`PastPerformanceSummary`/`Proof`/`Discriminator` tables for a RAG pipeline. That integration is entirely specific to the proposal-capture tool and has no lessons-learned equivalent, so:

- No database, no `DATABASE_URL`/`POSTGRES_URL`, no ORM — this repo has never had one; the Postgres dependency belonged to the *other* app.
- No admin-UI import path — the original's Admin → Resources UI lives in `solution-architecture`, not in this repo.
- `docs/technical-blueprint.md`, `docs/data-model.md`, `docs/test-plan.md`, and `docs/AGENT-RUNBOOK.md` from the source template were not ported — they described that cross-platform Neon integration and/or contained the original maintainer's local machine paths and personal email. See the PR description for the full list.

If a downstream consumer is built for this KB later, document its sync contract here.

## See also

`docs/technical-blueprint.md` — the request-by-request and pipeline-by-pipeline detail behind the components listed above (auth flow, the context/ → docs/ → wiki/site/ content pipeline, and the current access model: login gate only, no per-page sensitivity filtering).

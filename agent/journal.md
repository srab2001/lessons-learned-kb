# Agent journal

Append-only decision log. Read this at the start of every session. Most recent entries at the bottom.

---

## Setup session — 2026-08-13

Repo bootstrapped from `proposal-intelligence-kb` (rebranded for lessons-learned content; see PR description for the full list of what was ported, renamed, or intentionally left out). KB initialized with sensitivity defaults (`context/retrospectives/` → internal; `context/incident-reviews-raw/` → restricted) and recommendation standards (quantified metric required; qualitative-only → `confidence: low`). Staleness trigger set at 5+ years post-engagement. No context files processed yet — awaiting first source material.

## Post-bootstrap verification — 2026-08-13

Ran a local `mkdocs build --strict` against the bootstrap to test it before merge. It aborted: three of the seven wiki section index pages (`wiki/docs/anti-patterns/index.md`, `client-context/index.md`, `incident-reviews/index.md`) were left at `sensitivity: internal` from the bootstrap, while the other four were `public`. The `sensitivity_filter.py` build hook blanks any non-public page regardless of content, so those three section landing pages — generic "what goes here" text with nothing client- or incident-specific in them — were rendering as "Access Restricted" instead of their actual description. Fixed by setting all three to `sensitivity: public`, matching the other four. **Lesson for future sessions:** the `internal`/`restricted` sensitivity defaults in `structure.md` apply to individual KB content pages (a specific client's page, a specific incident's page) — not to the section index page itself, which is static nav-tree text with no per-entity detail. Don't apply the section's content-sensitivity default to its own index page.

Non-strict `mkdocs build` (matching what `build-wiki.yml` actually runs) succeeded both before and after the fix — the strict-mode failure would not have blocked the real CI build, but it was still worth fixing since it broke the live rendering of those three pages.

Wrote `docs/technical-blueprint.md` (the repo's own architecture doc — request/pipeline-level detail on auth, the content pipeline, and the sensitivity-filter build hook) since the source template's `technical-blueprint.md` was intentionally not ported (it described a different app's Neon/RAG integration). Cross-linked it from `docs/design.md` and `wiki/docs/about/user-guide.md`.

Could not verify the live Vercel preview directly — `lessons-learned-kb.vercel.app` is outside this session's network egress allowlist (`WebFetch` returned `EGRESS_BLOCKED`). Verification here is limited to the local `mkdocs build` test; someone with browser access should confirm the deployed preview renders and the OAuth gate behaves as expected before merge.

Declined to hardcode a real admin email (`asrab2001@gmail.com`, requested mid-session) into `.env.example` — that file holds placeholders only, matching how the OAuth/DB-adjacent secrets are handled. Directed it to be set as a Vercel environment variable (`ALLOWED_KB_EMAILS`) instead, same as `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET`/`AUTH_SECRET`.

## Context ingest — 2026-08-13

Landed `context/engagement-notes/consolidated-lessons-learned-2026-08-13.md` — a maintainer-supplied document synthesizing debugging lessons from three of the maintainer's own repos (`meal_planner_app`, `travel-deal-finder`, `raven_demo`). This was a **context ingest only**, not a synthesis session: the file is raw source material, not yet converted into `docs/` pages.

**Scope notes for whoever runs the synthesis session on this file:**
- The document is organized by technical topic (Auth/SSO, Deployment, DB, Testing, Frontend, API, Process) rather than by project, and mixes content that maps to at least four different KB sections: per-project root causes (→ `docs/retrospectives/`, one page each for the three repos), reusable fixes (→ `docs/recommendations/` under something like `platform-engineering` or a new capability), documented failure patterns (→ `docs/anti-patterns/`), and process lessons (→ `docs/best-practices/` and/or `docs/capability-areas/`). It will need to be split, not converted 1:1 into a single page.
- None of the "Best Practice" or "Resolution" claims in the source carry a quantified outcome (time saved, defect rate, etc.) — per `CLAUDE.md`'s recommendation standard, these can inform `docs/best-practices/` or `docs/anti-patterns/` entries (which don't require a metric) but do not qualify as `docs/recommendations/` entries, which do.
- The three source repos (`meal_planner_app`, `travel-deal-finder`, `raven_demo`) read as the maintainer's personal/practice projects, not Ad Hoc client engagements. `structure.md` and the wiki copy ("Maintained by the Ad Hoc delivery team") are written assuming client delivery engagements — flagged here rather than silently reinterpreted, since it affects how "client," "engagement," and "delivery lead" language in the resulting pages should read.
- Filed under `context/engagement-notes/` (internal by default) rather than `best-practices-raw` or `anti-patterns-raw` specifically, since the single document spans both and isn't yet split — the synthesis session should route each extracted lesson to the raw folder matching its eventual section, or split this file directly.
- `kb_impact` left empty in the manifest pending that synthesis session.

## Tooling — repo-to-context ingest script — 2026-08-13

Built `scripts/repo_to_context.py`, a standalone CLI requested by the maintainer to "point at a GitHub repo" and stage lessons-learned-shaped material into `context/`. Scoped deliberately narrow after a clarifying round-trip with the maintainer: it **stages raw material into `context/` only** — it never writes `docs/` pages, never invents a metric, and never sets `lifecycle: active` or `confidence: high`. A synthesis session still has to do the actual KB-page work, same as any other context ingest. This preserves `CLAUDE.md`'s traceability/no-invented-metric rules; an end-to-end auto-synthesizer was explicitly not what was wanted once the tradeoff was made concrete.

Behavior: for a target repo, it first looks for existing lessons-learned-shaped markdown (filename/content heuristics for retrospective/postmortem/incident/anti-pattern/best-practice/recommendation language) and classifies each match into the right `context/<folder>/` via keyword rules. If nothing matches, it falls back to a repo-activity digest (README + recent closed PRs + closed issues), explicitly labeled inside the file itself as *inferred, not authored* and staged under `context/engagement-notes/` (the catch-all — there's no dedicated raw folder for `client-context`; per `structure.md` those KB pages are sourced from `engagement-notes/` anyway, so unclassified and client-context-shaped material land in the same place).

Covers all 7 KB sections' backing folders (maintainer confirmed anti-patterns should be included, since the original ask listed only 6).

**Testing constraints:** this session's network egress blocks arbitrary calls to `api.github.com`/`raw.githubusercontent.com` (same restriction hit earlier trying to reach the Vercel preview), so the tool could not be exercised against a real repo from here. What *was* tested locally, without network: the classification regex against a table of realistic filenames (caught and fixed a real bug — `anti-?pattern` didn't match `ANTI_PATTERNS.md`'s underscore, only a hyphen), and the staging/manifest read-write-idempotency logic end-to-end in a scratch directory (new file, identical re-run is a no-op, changed content replaces rather than duplicates the manifest entry, `--dry-run` never touches disk). Running it against a real target repo (e.g. `meal_planner_app`, `travel-deal-finder`, `raven_demo`) still needs to happen outside this constrained session, or after those repos are attached to a session that has the network access to reach GitHub's REST/raw API directly.

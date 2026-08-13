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

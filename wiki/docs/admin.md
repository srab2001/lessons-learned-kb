---
title: "Admin — Upload New Materials"
lifecycle: active
confidence: high
sensitivity: public
---

# Admin — Upload New Materials

!!! info "Who this is for"
    KB maintainers only. There is currently no dedicated admin UI for this KB — content is added directly to the repo.

---

## Context folders

Select the folder that matches your content type:

| Folder | Use for | Sensitivity | Wiki destination |
|---|---|---|---|
| **Retrospectives** | Project completion notes, sprint retros, exit interviews | Internal | `retrospectives/` |
| **Recommendations (raw)** | Unverified metrics, capture notes | Internal | `recommendations/` |
| **Incident Reviews (raw)** | Postmortems, evaluator/stakeholder feedback | Restricted | Not published |
| **Anti-Patterns (raw)** | Documented failure patterns, near-misses | Restricted | Not published |
| **Engagement Notes** | Internal status notes, working docs | Internal | Not published |
| **Capability Areas** | Cross-project practice-area write-ups | Public | `capability-areas/` |
| **Best Practices (raw)** | Draft practice statements | Internal | `best-practices/` |

---

## How to add new material

1. Add the source `.md` file to the appropriate `context/<folder>/` directory in the repo.
2. Add an entry to that folder's `manifest.yaml` (path, `as_of_date`, content hash, sensitivity).
3. Open a Claude Code session in the repo and run a KB synthesis session (see `agent/agents.md` and `.claude/agents/kb-synthesis.md`), or dispatch the `KB Synthesis` GitHub Action manually from the Actions tab (or `gh workflow run kb-synthesis.yml -f folder=<folder> -f filename=<file>`) if you want CI to do it.
4. Review the resulting PR (or, for the CI path, the direct commit) before treating any page as `active`.
5. Merging to `main` triggers the `Build Wiki` action, which rebuilds `wiki/site/` and redeploys.

---

## Convert non-markdown files first

The KB only accepts `.md` files. For PDFs, Word documents, or PowerPoints:

```bash
pip install markitdown
markitdown your-file.pdf > output.md
```

Review the output for formatting artifacts before adding it to `context/`.

---

## Sensitivity rules

- **Restricted** material (incident feedback, sensitive personnel/client detail) must go into `context/incident-reviews-raw/` or `context/anti-patterns-raw/` — never into retrospectives or recommendations folders.
- The synthesis agent enforces sensitivity downstream, but correct folder assignment is the first line of defense.
- When in doubt, use a more restrictive folder.

# Documentation Skill: User Guide

This document explains how to use the `SKILL.md` file in this folder with your
AI coding agent. The skill file is written *for the agent*; this guide is
written *for you*.

---

## What It Does

`SKILL.md` gives an AI agent a repeatable process for:

- Writing and updating READMEs, architecture docs, runbooks, and guides
- Creating and maintaining schema documentation (ERDs, OpenAPI specs, data dictionaries)
- Writing changelog entries, release notes, and migration guides
- Auditing existing docs for gaps, outdated content, and duplication
- Cross-referencing and linking docs across repos without duplicating content
- Generating Mermaid diagrams (C4, sequence, ERD, network)

The agent follows a five-stage pipeline: **Ingest → Audit → Draft → Validate →
Present**. The audit step checks what already exists before writing anything new,
so you get a clear picture of what's net-new, what's an update, and what's just
linking.

---

## How to Use It

### 1. Add the file to your project

Copy this entire `documentation/` folder into your project under one of these paths:

| Location | When to use |
|----------|-------------|
| `.github/skills/documentation/` | GitHub Copilot (VS Code) auto-discovered |
| `.agents/skills/documentation/` | Alternate agent discovery path |
| `.claude/skills/documentation/` | Claude-compatible projects |

The `SKILL.md` filename and the `name` field in its frontmatter must match the
folder name (`documentation`). VS Code discovers it automatically from these paths.

### 2. Invoke it

Give the agent a documentation task. Examples:

- *"Document the Example API auth flow and create sequence diagrams and update
  the README."*
- *"Audit tickets #113–#130 and tell me what documentation already exists vs.
  what's missing."*
- *"Add a changelog entry for the pagination feature in PR #342."*
- *"Create a C4 container diagram for the Example Project backend."*
- *"Cross-link the current IG into the existing docs."*
- *"Generate an ERD for the session database."*

The agent will:
1. Parse your request and present a **task summary** for your approval.
2. **Audit** what documentation already exists and classify it (exists, outdated,
   missing, duplicated).
3. Wait for you to confirm scope before writing anything.
4. Draft the content, then self-validate against a quality checklist.
5. Present the output with a **status map** so you can see exactly what was created, updated, or linked.

### 3. Review the output

The agent marks every point where your review is needed with **HUMAN GATE**.
You'll see these at:

1. **After the task summary**: confirm the agent understood what you need.
2. **After the audit**: confirm which items are in scope before it drafts.
3. **After the final output**: review the docs before committing.

The agent will never commit, push, or publish on its own.

---

## What You Get in the Output

Every output from the agent includes:

| Section | What it contains |
|---------|-----------------|
| **Summary** | What was done, mapped to your task list |
| **Files changed/created** | List with paths and descriptions |
| **Audit status map** | Each item marked as: created (net-new), updated, linked, or skipped |
| **Sources used** | Files read, existing docs referenced, code inspected |
| **Open items** | Sections needing SME review, unverifiable claims, follow-up tasks |

---

## Key Capabilities

### Documentation auditing

Ask the agent to audit before writing. It will produce a table like:

```
┌─────────────────────────┬──────────────┬────────────────────────┐
│ Item                    │ Status       │ Action                 │
├─────────────────────────┼──────────────┼────────────────────────┤
│ Network diagram         │ Missing      │ Create net-new         │
│ API ERD                 │ Exists       │ Link from existing docs│
│ Auth flow diagram       │ Outdated     │ Update with new flow   │
│ OpenAPI spec            │ Exists       │ Enrich with examples   │
└─────────────────────────┴──────────────┴────────────────────────┘
```

This prevents the agent from rewriting docs that already exist.

### Schema documentation

The agent handles three schema formats:

| Format | What it produces |
|--------|-----------------|
| **Database (ERD)** | Mermaid `erDiagram` + table-by-table column details |
| **API (OpenAPI)** | Enriched specs with descriptions, examples, error responses |
| **Data dictionary** | Field-level mapping tables across source/target systems |

### Changelog and release notes

The agent follows [Keep a Changelog](https://keepachangelog.com/) conventions
by default, or matches your project's existing format. It categorizes entries
as Added/Changed/Deprecated/Removed/Fixed/Security and writes them in
imperative mood with ticket references.

### Diagrams

The agent generates Mermaid source for:
- **C4** (context, container, component): system architecture
- **Sequence**: auth flows, failover procedures, API call chains
- **ERD**: database relationships
- **Network**: VPCs, subnets, load balancers, security zones

You handle PNG/SVG export (or configure a tool to do it).

---

## Customizing for Your Team

The skill file reads a team documentation config if one exists. Create one of:

- `.github/docs-config.md`
- `docs-config.md`
- `.docs-config.md`

In it, specify your team's conventions:

```markdown
# Documentation Configuration: [Your Team]

## Documentation Toolchain
- **Markdown flavor:** GitHub Flavored Markdown
- **Diagram tool:** Mermaid
- **Export formats required:** PNG + Mermaid source

## Conventions
- **File naming:** kebab-case.md
- **README required sections:** Overview, Setup, Usage, Related Docs
- **Changelog format:** Keep a Changelog

## Locations
- **Technical docs repo:** team-repo-name
- **Architecture docs:** team-repo-name/team-folder/Architecture Diagrams
- **API specs:** team-repo-name/team-folder/Open Api Doc
```

If no config file is found, the agent infers conventions from your existing docs
and asks about anything it can't infer.

A full template is in §7 of the skill file, or use the copy-ready
`docs-config.template.md` included in this folder.

---

## Included Prompts

Pre-built prompts in `prompts/` that you can invoke directly:

| Prompt | File | Use when |
|--------|------|----------|
| Audit docs | `prompts/audit-docs.prompt.md` | Finding documentation gaps |
| Write changelog | `prompts/write-changelog.prompt.md` | Writing changelog entries or release notes |
| Create diagram | `prompts/create-diagram.prompt.md` | Creating Mermaid diagrams |
| Document schema | `prompts/document-schema.prompt.md` | Documenting DB/API schemas |

In VS Code, these appear as selectable prompts. In other agents, reference
them by path.

---

## Folder Contents

```
.github/skills/documentation/
├── SKILL.md                       ← skill file (agent reads this)
├── README.md                      ← you are here
├── AGENTS.md                      ← agent mode definition (docs agent)
├── quality-checklist.md           ← pre-output checklist (agent + human)
├── docs-config.template.md        ← team config template (copy to your project)
└── prompts/
    ├── audit-docs.prompt.md       ← find documentation gaps
    ├── write-changelog.prompt.md  ← changelog entries + release notes
    ├── create-diagram.prompt.md   ← Mermaid diagrams (C4, sequence, ERD, network)
    └── document-schema.prompt.md  ← DB/API schema documentation
```

The root-level `.github/copilot-instructions.md` tells agents when to activate
this skill automatically.

---

## What It Won't Do

- **Write application code.** Use the `ai-workflow` skill for code and tests.
- **Generate tests.** Use the `ai-workflow` skill for test generation.
- **Commit or publish docs.** Every output is a draft for your review.
- **Reorganize your doc structure.** It works within your existing layout unless
  you explicitly ask for reorganization.
- **Duplicate content.** If docs exist elsewhere, it links to them instead of
  copying.

---

## Quick Reference

| You want to... | Tell the agent... |
|----------------|-------------------|
| Write or update a README | Point to the directory and describe what's needed |
| Audit doc coverage | Give it a ticket list or feature set and ask "what's documented vs. missing?" |
| Create architecture diagrams | Describe the system or point to code and ask for C4/sequence/network diagrams |
| Document a database schema | Point to migration files or ORM models and ask for an ERD |
| Enrich an OpenAPI spec | Point to the spec and ask for descriptions, examples, and error responses |
| Write a changelog entry | Describe the change, category, and ticket/PR number |
| Cross-link existing docs | Describe what should link where it will verify targets exist before linking |
| Write a migration guide | Describe the breaking change and the before/after behavior |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Agent doesn't follow the workflow | Make sure the `documentation/` folder is under `.github/skills/`. Refer to it explicitly if needed. |
| Agent rewrites existing docs unnecessarily | Remind it: "Audit first. Don't duplicate." The skill already instructs this, but you can reinforce it. |
| Agent invents file paths or endpoints | Ask it to verify paths exist before documenting. The skill instructs this, but you can reinforce it. |
| Agent skips the audit step | Say "show me what already exists before writing anything new." |
| Diagrams don't match team style | Create or update the docs config file (see above). |
| Output doesn't match existing doc formatting | The agent reads existing docs first, but if it drifts, point it to a specific file as a style reference. |

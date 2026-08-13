# Copilot Instructions

These instructions tell GitHub Copilot (or any compatible AI agent) which skills
are available in this project and when to activate them. Place this file at your
project root or in `.github/copilot-instructions.md`.

---

## Available Skills

### documentation
- **Skill file:** `.github/skills/documentation/SKILL.md`
- **Activate when:** The user asks to write, update, or audit documentation;
  create diagrams; write changelog entries; document schemas; or cross-link
  existing docs.
- **What it does:** Creates or updates technical documentation using a five-stage
  pipeline (Ingest → Audit → Draft → Validate → Present) with human review
  gates.

---

## Reusable Prompts

| Prompt | File | Use when |
|--------|------|----------|
| Audit docs | `.github/skills/documentation/prompts/audit-docs.prompt.md` | Finding documentation gaps |
| Write changelog | `.github/skills/documentation/prompts/write-changelog.prompt.md` | Writing changelog entries or release notes |
| Create diagram | `.github/skills/documentation/prompts/create-diagram.prompt.md` | Creating Mermaid diagrams |
| Document schema | `.github/skills/documentation/prompts/document-schema.prompt.md` | Documenting DB/API schemas |

---

## Team Configuration

The documentation skill reads a team-specific config file to adapt to your conventions.
Copy the template from the skill folder and fill it in:

- **documentation:** Copy `.github/skills/documentation/docs-config.template.md` →
  `.github/docs-config.md` (or `docs-config.md` at project root)

If no config file exists, the agent infers conventions from the codebase and
asks about what it can't infer.

---

## General Rules

1. **Always present a task summary and wait for approval** before generating
   output. The skill enforces this as a human review gate.
2. **Never commit, push, or publish** without explicit user approval.
3. **Read existing docs before writing** to match project conventions.
4. **No hallucinated references** — verify file paths, endpoints, and names exist.
5. **No sensitive data** in output — no PII, credentials, or internal URLs
   unless the user explicitly provides them.
6. **Scope to the request** — do not add unrequested features or changes.

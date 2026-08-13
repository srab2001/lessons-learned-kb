# Copilot Instructions

These instructions tell GitHub Copilot (or any compatible AI agent) which skills
are available in this project and when to activate them. Place this file at your
project root or in `.github/copilot-instructions.md`.

---

## Available Skills

### ai-workflow
- **Skill file:** `.github/skills/ai-workflow/SKILL.md`
- **Activate when:** The user provides a ticket, issue, acceptance criteria, or
  asks to generate code, write tests, or review code/tests.
- **What it does:** Converts ticket requirements into code and tests using a
  five-stage pipeline (Ingest → Decompose → Generate → Validate → Present)
  with human review gates.

---

## Reusable Prompts

| Prompt | File | Use when |
|--------|------|----------|
| Ticket to code | `.github/prompts/ticket-to-code.prompt.md` | Converting a ticket into code + tests |
| Generate tests | `.github/prompts/generate-tests.prompt.md` | Writing tests from acceptance criteria |
| Review code | `.github/prompts/review-code.prompt.md` | Reviewing code for quality + security |

---

## Team Configuration

The ai-workflow skill reads a team-specific config file to adapt to your conventions.
Copy the template from the skill folder and fill it in:

- **ai-workflow:** Copy `.github/skills/ai-workflow/ai-workflow-config.template.md` →
  `ai-workflow-config.md` (or `.ai-config.md` at project root)

If no config file exists, the agent infers conventions from the codebase and
asks about what it can't infer.

---

## General Rules

1. **Always present a task summary and wait for approval** before generating
   output. Both skills enforce this as a human review gate.
2. **Never commit, push, or publish** without explicit user approval.
3. **Read existing code/docs before writing** to match project conventions.
4. **No hallucinated references**. Verify file paths, endpoints, and names exist.
5. **No sensitive data** in output; no PII, PHI, credentials, or internal URLs
   unless the user explicitly provides them.
6. **Scope to the request**. Do not add unrequested features, refactoring, or
   changes.

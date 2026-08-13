# AI Workflow Skill: User Guide

This document explains how to use the `SKILL.md` file in this folder with your
AI coding agent. The skill file is written *for the agent*; this guide is
written *for you*.

---

## What It Does

`SKILL.md` gives an AI agent a repeatable, auditable process for:

- Converting tickets/issues into working code and tests
- Generating tests from plain-English acceptance criteria
- Reviewing AI-generated code against quality and security standards
- Enforcing human review gates before anything gets committed

The agent follows a five-stage pipeline: **Ingest → Decompose → Generate →
Validate → Present**. At key stages, the agent pauses and waits for your
approval before continuing.

---

## How to Use It

### 1. Add the file to your project

Copy this entire `ai-workflow/` folder into your project under one of these paths:

| Location | When to use |
|----------|-------------|
| `.github/skills/ai-workflow/` | GitHub Copilot (VS Code), auto-discovered |
| `.agents/skills/ai-workflow/` | Alternate agent discovery path |
| `.claude/skills/ai-workflow/` | Claude-compatible projects |

The `SKILL.md` filename and the `name` field in its frontmatter must match the
folder name (`ai-workflow`). VS Code discovers it automatically from these paths.

### 2. Invoke it

Give the agent a ticket, issue, or set of requirements. Examples:

- *"Here's ticket #342: implement pagination for the /items endpoint."*
- *"Write tests for this acceptance criteria: users can search products by
  name and results are sorted alphabetically."*
- *"Review this PR for security and test coverage."*

The agent will:
1. Parse your input and present a **task summary** for your approval.
2. Wait for you to confirm before generating anything.
3. Produce code and/or tests, then self-validate against a quality checklist.
4. Present the output with an **AC-to-test coverage map** so you can verify
   every requirement is addressed.

### 3. Review the output

The agent marks every point where your review is needed with **HUMAN GATE**.
You'll see these at two points:

1. **After the task summary**: confirm the agent understood the ticket correctly.
2. **After the final output**: review the generated code/tests before committing.

The agent will never commit, push, or publish on its own.

---

## What You Get in the Output

Every output from the agent includes:

| Section | What it contains |
|---------|-----------------|
| **Summary** | What was done, mapped to ticket/ACs |
| **Files changed/created** | List with descriptions |
| **Test coverage map** | AC → test case mapping (happy path, error path, edge cases) |
| **Open items** | Assumptions, risks, anything the agent couldn't address |

---

## Customizing for Your Team

The skill file reads a team configuration file if one exists. Create one of these:

- `.github/ai-workflow-config.md`
- `ai-workflow-config.md`
- `.ai-config.md`

In it, specify your team's conventions:

```markdown
# AI Workflow Configuration: [Your Team]

## Project Context
- **Language/framework:** Java 17 / Spring Boot 3.x
- **Test framework:** JUnit 5 + Mockito
- **Test location:** src/test/java, matching package structure
- **Build tool:** Gradle

## Conventions
- **Test naming:** methodName_condition_expectedResult
- **Code style:** Google Java Style
- **PR requirements:** all tests pass, 80% coverage minimum
```

If no config file is found, the agent infers conventions from your codebase and
asks about anything it can't infer.

A full template is in §6 of the skill file, or use the copy-ready
`ai-workflow-config.template.md` included in this folder.

---

## Included Prompts

Pre-built prompts in `src/ad-hoc/prompts/` for this repository. When the
package is installed into a target project, these prompts may be placed under
`ai-workflow/prompts/`.

| Prompt | File | Use when |
|--------|------|----------|
| Ticket to code | `src/ad-hoc/prompts/ticket-to-code.prompt.md` | Converting a ticket into code + tests |
| Generate tests | `src/ad-hoc/prompts/generate-tests.prompt.md` | Writing tests from acceptance criteria |
| Review code | `src/ad-hoc/prompts/review-code.prompt.md` | Reviewing code for quality + security |

In VS Code, these appear as selectable prompts. In other agents, reference
them by path.

---

## Folder Contents

```
ai-workflow/
├── SKILL.md                           ← skill file (agent reads this)
├── README.md                          ← you are here
├── quality-checklist.md               ← pre-output checklist (agent + human)
├── ai-workflow-config.template.md     ← team config template (copy to your project)
└── copilot-instructions.md            ← Copilot activation instructions
```

In this repository:
- The agent mode file is at `src/ad-hoc/agents/ai-workflow.agent.md`.
- The shared prompts are in `src/ad-hoc/prompts/`.

---

## What It Won't Do

- **Choose your AI platform.** The skill works with any agent (i.e., Copilot, Claude,
  ChatGPT, or others).
- **Commit or publish code.** Every output is a draft for your review.
- **Add unrequested features.** The agent scopes strictly to the ticket.

---

## Quick Reference

| You want to... | Tell the agent... |
|----------------|-------------------|
| Turn a ticket into code + tests | Paste the ticket description |
| Generate tests only | Paste acceptance criteria and say "write tests" |
| Review existing code | Point to a file or PR and say "review this" |
| Check test coverage against ACs | Paste ACs and point to the test file |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Agent doesn't follow the workflow | Make sure the `ai-workflow/` folder is under `.github/skills/`. Refer to it explicitly if needed. |
| Agent adds unrequested features | Remind it: "Scope to the ticket only." The skill already instructs this, but agents occasionally drift. |
| Agent hallucinates file paths | Ask it to verify paths exist before writing code. The skill instructs this, but you can reinforce it. |
| Agent skips the review gate | Say "stop and show me the task summary first." |
| Output doesn't match team conventions | Create or update the team config file (see above). |

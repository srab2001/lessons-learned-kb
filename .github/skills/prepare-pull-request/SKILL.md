---
name: prepare-pull-request
description: "Analyze code changes and draft a review-ready pull request with validation, risks, and traceability." 
inputs:
  - name: change_context
    description: Code changes, git diff, commit history, and/or related ticket or specification describing the work. (Automatically gathered from the current branch unless overridden.)
    required: true
outputs:
  - name: pr_draft
    description: A complete pull request title and body formatted for clarity, traceability, and reviewer efficiency.
  - name: readiness_feedback
    description: Gaps, risks, and suggested improvements before marking the pull request ready for review.
---

# Prepare Pull Request

## Purpose

Enable GitHub Copilot to assist developers in preparing high-quality pull requests. The skill automatically gathers change context from the current branch, analyzes the type of change (frontend/backend), and interactively guides the developer through drafting a clear, structured PR that explains what changed, why it changed, how it was validated, and what reviewers should focus on.

This skill produces a draft pull request for human review. Final approval, validation, and submission remain the developer’s responsibility.

## Your Role

You are an experienced software engineer helping prepare high-quality pull requests using GitHub Copilot.

You:

- Write concise, reviewer-friendly pull requests
- Prioritize clarity and readability over completeness
- Focus on what reviewers need to understand quickly
- Explicitly call out missing information instead of guessing
- Highlight validation, risks, and traceability

## When to Use

Use this skill when:

- Preparing a new pull request (recommended and most effective)
- Converting a draft PR into a review-ready PR
- Improving or refining an existing PR description (some steps may be adapted or skipped)
- Validating whether a change is ready for review (some steps may be adapted or skipped)

> Note: This skill is optimized for new PRs and converting drafts, but can also help improve or validate existing PRs. For existing PRs, some steps (such as gathering the latest diff or running a preliminary code review) may be adapted or skipped depending on the current PR state.

Example prompts:

- "Help me draft a PR for this change"
- "Summarize this diff into a PR description"
- "Is this PR ready for review?"
- "What am I missing before submitting this PR?"

## Constraints

- Do not invent missing information — explicitly call it out. (This applies throughout the skill; see Output Guidance.)
- Do not include unrelated implementation details
- Do not rewrite or restructure content outside the scope of the pull request
- Prefer repository conventions over generic formats when available

## Preconditions

- Code changes are available (diff, commits, or branch)
- Some level of intent is available (ticket, spec, commit messages, or developer notes). If not, the agent will prompt the user for a ticket link, summary, or relevant notes before proceeding.

## Required Tools

This skill relies on the following tool access to function fully. Check availability at the start of the workflow:

| Tool | Used For | If Unavailable |
|------|----------|----------------|
| File system read | Reading PR templates, config files | Skip template detection; use standard format |
| Terminal / shell | Running linters, git commands | Ask user to run commands manually and paste output |
| Git | Reading commit history, branch diff | Ask user to paste `git log --oneline -10` and `git diff main` output |

**If required tools are missing:** Do not fail silently. Instead:

1. State which tools are unavailable
2. Continue with the steps that don't require those tools
3. For any step that needs a missing tool, provide the equivalent manual command and ask the user to paste the output

Example: "I don't have terminal access to run the linter. Please run `npm run lint` and paste the output so I can review it."

## Steps

1. Automatically gather the relevant change context from the current branch (e.g., latest commits, unmerged changes, or open PR diff).
2. If intent (ticket, summary, or notes) is not available, prompt the user for it up front.
3. Identify traceability by linking the change to a ticket, requirement, or acceptance criteria when available. (Intent and traceability are closely related and should be established before further analysis.)
4. Analyze the code changes and intent to determine the type of change (frontend/UI, backend/API, docs, config, etc.), intent, scope, and impact.
5. Check linting/formatting
   - Detect whether the repository runs a linter/formatter (pre-commit hooks, CI lint jobs, or project config files). Report the detected tools and configuration files
   - Prefer non-destructive checks: run linters/formatters in their "check" or dry-run mode to surface issues without modifying files (e.g., commands or flags that only list problems or produce a diff)
   - If a pre-commit hook or CI pipeline enforces lint/format rules, note that enforcement and which tools/configs were found
   - If no automated tooling or check mode is available, prompt the developer for the repository's canonical lint/format commands and ask whether to run autofix/format operations. Do not apply fixes without explicit developer approval
   - Surface any failures or autofixable issues and recommend the preferred remediation (run autofix/format locally and commit the changes, or grant explicit permission for the agent to create a follow-up commit)
6. Infer the primary purpose and user/system outcome
7. Run a preliminary Copilot code review to suggest improvements or flag issues, using both the code and the intent. Allow the user to address issues or proceed as desired.
8. Detect PR type and prompt for validation evidence as appropriate (screenshots for FE, tests for BE, preview steps for docs/config/infra, etc.).
9. Extract and organize key implementation details for reviewers. **Do not generate a line-by-line or exhaustive recap of every change. Focus on intent, reviewer context, and key points.**
10. Detect if the repository uses Commitizen or enforces Conventional Commits (by checking for configuration files or dependencies). If so, generate a PR title that follows the Conventional Commits style (e.g., feat:, fix:, docs:, chore:, ci:, etc.) and prompt the user to review or edit the title for compliance.
11. Generate a structured pull request body using the repository's PR template if detected (e.g., .github/pull_request_template.md), or a concise standard format:
    - Summary (what changed and why; keep it high-level and focused on reviewer context, not a detailed diff)
    - Key Implementation Notes (important technical/contextual details)
    - How To Test (steps for validation, test commands, or manual checks)
        - For frontend/UI changes, include screenshots or videos if prompted
        - For backend/API changes, describe API test steps, logs, or other relevant evidence if prompted
        - For docs/config/infra/other, describe how to preview, validate, or what to look for in review
    - References (add a link to the related ticket, issue, or requirement if provided; omit this section if not available, or call out if missing)
12. Present the draft PR to the user for review and feedback. Accept edits or additional information as needed.
13. Only open the pull request after explicit user approval.
14. Provide readiness feedback to guide whether the PR should be revised, remain draft, or be marked ready for review.

## Output Guidance

When generating the pull request:

- Prefer concise, scannable sections
- Avoid unnecessary low-level implementation details
- **Do not generate a detailed, line-by-line recap of every change. The PR summary should provide just enough context for a reviewer to understand the purpose, scope, and key points of the PR, not replace code review.**
- If information is missing, call it out as described in Constraints.
- Highlight reviewer-relevant details first
- Keep titles short, clear, and descriptive
- If Commitizen or Conventional Commits are detected, ensure the PR title follows the required style and prompt the user to review or edit as needed. Use types like `docs:`, `chore:`, or `ci:` for non-code PRs as appropriate.
- Tailor the "How To Test" section to the type of change: only prompt for screenshots/videos for significant frontend changes, for unit tests for new/significant backend logic if coverage is missing, and for preview/validation steps for docs/config/infra/other changes.
- Always include a "References" section in the PR body if a related ticket, issue, or requirement link is provided. If not, omit the section or call out that no reference was supplied.
- **Linting and Formatting:**
  - If a pre-commit hook is present and runs the linter and/or formatter, note that these are enforced automatically.
  - If not, ensure the linter and formatter are run manually and issues are addressed before preparing the PR.
- Interactively guide the user through the process: run a preliminary Copilot code review, detect PR type, prompt for missing validation only when warranted, present the draft for review, and only open the PR after user approval.

## Completion Criteria

- A clear, reviewer-friendly PR title and description are generated
- The PR includes traceability, validation, and risks
- Missing information and improvement opportunities are explicitly called out, per the Constraints section

## Graceful Degradation

If this skill cannot complete its full workflow, do not fail silently:

- **Partial completion:** Present whatever has been completed so far with a clear explanation of where the workflow stopped and why (e.g., "I was able to analyze the diff and draft the summary, but I couldn't run the linter because terminal access is unavailable.")
- **Missing tools:** Provide manual fallback steps for each blocked action rather than skipping it (e.g., "To run the code review manually, use: `gh pr review --comment`")
- **Inapplicable context:** If the skill is invoked in a context where it doesn't apply (no uncommitted changes, no open branch), explain why and suggest what the user could do instead (e.g., "There are no staged changes on this branch. Try `git diff HEAD` to see what's committed, or start by making changes to your codebase.")

## References

- Repository pull request template (if available)
- Related ticket, specification, or acceptance criteria
- Git commit history and diff

# Quality Checklist: AI Workflow (Code & Tests)

Run this checklist before presenting any output to the user.
If any item fails, fix it before presenting. If you cannot fix it, flag it
explicitly.

This checklist is usable by both agents and humans (e.g., in PR reviews).

---

## Correctness

- [ ] Code compiles / has no syntax errors
- [ ] Tests reference real functions, classes, and modules (not hallucinated)
- [ ] Imports exist in the project's dependency tree
- [ ] File paths used in the code are real and verified
- [ ] Code implements the requirement accurately

## Security (OWASP Top 10)

- [ ] No hardcoded secrets, tokens, or credentials
- [ ] User inputs are validated/sanitized before use in queries or commands
- [ ] No sensitive data logged or exposed in error messages
- [ ] Authentication and authorization checks are present where required
- [ ] No insecure defaults (debug mode, permissive CORS, wildcard permissions)

## Test Quality

- [ ] Every acceptance criterion has at least one corresponding test
- [ ] Happy path is covered
- [ ] Error / failure paths are covered
- [ ] Edge cases and boundary conditions are covered
- [ ] Tests use the project's existing framework and conventions
- [ ] Test data is synthetic: no real PII/PHI
- [ ] Tests are independent and repeatable (no shared mutable state)
- [ ] Test names describe the expected behavior (read like sentences)
- [ ] Assertions are specific (not just `assertNotNull`)

## Scope

- [ ] Output addresses the ticket, nothing more, nothing less
- [ ] No unrequested refactoring, feature additions, or style changes
- [ ] No new dependencies added without explicit ticket requirement
- [ ] No unrequested files created

## Presentation

- [ ] Summary maps output to ticket / acceptance criteria
- [ ] Files changed/created are listed with descriptions
- [ ] AC-to-test coverage map is included
- [ ] Open items and assumptions are flagged
- [ ] Any items the reviewer should validate are called out

---

## Using This Checklist

**Agents:** Run this internally before every PRESENT step (§2.5 of ai-workflow.md).

**Humans:** Use this during PR review or when evaluating AI-generated output.
Copy into a PR template or review comment as needed.

**CI/CD:** Checklist items marked "Security" map to static analysis rules.
Consider enforcing them via linting (e.g., `detect-secrets`, `semgrep`).

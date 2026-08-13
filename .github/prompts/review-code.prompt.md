---
description: 'Review code or tests for quality, security, and coverage using the ai-workflow skill'
agent: 'agent'
tools:
  - 'codebase'
---

Use the **ai-workflow** skill to review this code.

Apply the review framework from §4:

**Code review criteria:**
- Correctness: does it implement the requirement?
- Security: OWASP Top 10 (injection, auth, data exposure, misconfig, access control)
- Scope: within ticket scope, no unrequested changes?
- Completeness: no TODOs, placeholders, or hallucinated references?

**Test review criteria:**
- Every acceptance criterion has a test
- Tests are independent (no shared mutable state)
- Test names describe behavior
- Assertions are specific
- Error paths are tested
- No real sensitive data in fixtures

**Output format:**
- Blocking issues (with suggested fixes)
- Non-blocking issues (with suggestions)
- Coverage assessment (ACs covered vs. missing)
- Verdict: Ready for human review / Needs changes

**Code to review:**

${selection}

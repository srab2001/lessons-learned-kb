---
description: 'Generate tests from plain-English acceptance criteria using the ai-workflow skill'
agent: 'agent'
tools:
  - 'codebase'
---

Use the **ai-workflow** skill to generate tests from the acceptance criteria below.

Follow §3 (Writing Tests from Plain English) of the skill:
1. Parse the requirements into structured test specifications.
2. Generate test cases per behavior (happy path, error path, edge cases).
3. Ask clarifying questions only if ambiguity would meaningfully affect the tests.
4. Match the project's existing test framework, naming conventions, and file structure.
5. Present a coverage map showing which AC each test addresses.

**Acceptance criteria:**

${selection}

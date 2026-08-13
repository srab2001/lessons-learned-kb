---
description: 'Convert a ticket or issue into code and tests using the ai-workflow skill'
agent: 'agent'
tools:
  - 'codebase'
---

Use the **ai-workflow** skill to convert this ticket into working code and tests.

Follow the full Ingest → Decompose → Generate → Validate → Present pipeline.

**Instructions:**
1. Parse the ticket and present a task summary. Wait for my approval.
2. Decompose acceptance criteria into specific code and test tasks.
3. Read existing code and tests before generating anything.
4. Generate code and tests that follow the project's existing patterns.
5. Self-validate against the quality checklist.
6. Present the output with an AC-to-test coverage map.

**Ticket:**

${selection}

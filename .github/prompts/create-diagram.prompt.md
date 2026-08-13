---
description: 'Create a Mermaid diagram (C4, sequence, ERD, or network) from a system description'
agent: 'agent'
tools:
  - 'codebase'
---

Use the **documentation** skill to create a diagram for the system or process described below.

Follow §6 (Diagram Standards) of the skill:
- One diagram, one concern — split complex systems into multiple diagrams.
- Title every diagram with a Markdown heading.
- Label every node and edge — no unlabeled arrows.
- Use appropriate diagram type:
  - **C4** (context/container/component) for architecture
  - **Sequence** for flows and interactions
  - **erDiagram** for database relationships
  - **Network** for infrastructure topology
- Output Mermaid source. Note if PNG/SVG export is needed.

**What to diagram:**

${selection}
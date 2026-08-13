---
description: 'Document a database or API schema (ERD, OpenAPI enrichment, or data dictionary)'
agent: 'agent'
tools:
  - 'codebase'
---

Use the **documentation** skill to document the schema described below.

Follow §3 (Schema Documentation Procedures) of the skill:

**For database schemas:**
- Read migration files or ORM models
- Document every table: name, purpose, columns (name, type, nullable, default, constraints)
- Generate a Mermaid erDiagram with proper cardinality
- Note schema quirks (soft deletes, audit columns, partitioning)

**For API schemas (OpenAPI):**
- Read existing spec and endpoint implementations
- Add descriptions, examples, and error responses for every endpoint
- Document authentication requirements and rate limits

**For data dictionaries:**
- Create field-level mapping tables (source field → transform → target field)
- Document transformation logic
- Link to the relevant adapter/mapper code

**Schema to document:**

${selection}

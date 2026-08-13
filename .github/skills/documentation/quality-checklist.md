# Quality Checklist: Documentation

Run this checklist before presenting any documentation output to the user.
If any item fails, fix it before presenting. If you cannot fix it, flag it
explicitly.

This checklist is usable by both agents and humans (e.g., in doc reviews).

---

## Accuracy

- [ ] All file paths, endpoint URLs, and module names referenced are real
      (verified by reading the codebase or confirmed by the user)
- [ ] Version numbers, dependency names, and tool names are correct
- [ ] Diagram elements (nodes, edges, labels) match the actual system
- [ ] Schema documentation matches the actual schema (column names, types,
      constraints)

## Completeness

- [ ] Every item in the task summary is addressed
- [ ] No placeholder text (`[TODO]`, `TBD`, `...`) left in the output
      (unless flagged explicitly for the user to fill in)
- [ ] Cross-references point to real documents/sections
- [ ] Changelog entries include ticket/PR references where available

## Consistency

- [ ] Formatting matches the existing documentation in the project
- [ ] Terminology is consistent with the codebase and existing docs
- [ ] Heading hierarchy does not skip levels
- [ ] Diagram style (shapes, edge labels, layout direction) matches other
      diagrams in the project
- [ ] Link text is consistent across all documents referencing the same target

## Security / Sensitivity

- [ ] No hardcoded secrets, credentials, or tokens in examples
- [ ] No real PII or PHI in sample data or diagrams
- [ ] Internal URLs are only included if the user explicitly provided them
- [ ] Sensitive architecture details (security zones, key management) are
      appropriate for the document's audience and distribution

## Duplication

- [ ] No content duplicated from existing docs (link instead)
- [ ] If content exists elsewhere, cross-reference is used
- [ ] "Single source of truth" principle is maintained

## Scope

- [ ] Output addresses the request; nothing more, nothing less
- [ ] No unrequested restructuring, reorganization, or style changes
- [ ] No new files created that were not part of the task

## Diagrams (if applicable)

- [ ] Every diagram has a title (Markdown heading above the code block)
- [ ] Every node is labeled
- [ ] Every edge/arrow has a description
- [ ] One diagram covers one concern (not overloaded)
- [ ] Legend or key included if non-obvious conventions are used

## Schema Docs (if applicable)

- [ ] Every table/entity is documented with purpose
- [ ] Columns include: name, type, nullable, default, constraints
- [ ] Relationships show correct cardinality
- [ ] API endpoints include: method, path, parameters, responses, auth

## Changelog (if applicable)

- [ ] Entries use the project's existing format
- [ ] Entries are in imperative mood ("Add X", not "Added X")
- [ ] Breaking changes are listed first
- [ ] Migration guide included for breaking changes

## Presentation

- [ ] Summary maps output to the task list
- [ ] Files changed/created are listed with paths and descriptions
- [ ] Audit status map is included (if audit was performed)
- [ ] Sources used are listed (files read, docs referenced)
- [ ] Open items and SME review needs are flagged

---

## Using This Checklist

**Agents:** Run this internally before every PRESENT step (§2.5 of SKILL.md).

**Humans:** Use this during doc review or when evaluating AI-generated documentation.
Copy into a PR template or review comment as needed.

**Conditional sections:** Skip "Diagrams," "Schema Docs," or "Changelog" sections
if the task didn't involve those deliverables.

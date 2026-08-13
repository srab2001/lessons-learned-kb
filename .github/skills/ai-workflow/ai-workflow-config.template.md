# AI Workflow Configuration: [Team Name]

<!-- ─────────────────────────────────────────────────────────────────────
  Copy this file into your project as one of:
    .github/ai-workflow-config.md
    ai-workflow-config.md
    .ai-config.md

  The ai-workflow skill reads this file to adapt to your team's conventions.
  Fill in the sections that apply. Delete sections that don't.
───────────────────────────────────────────────────────────────────────── -->

## Project Context
- **Language/framework:** <!-- e.g., Java 17 / Spring Boot 3.x, Python 3.12 / FastAPI -->
- **Test framework:** <!-- e.g., JUnit 5 + Mockito, pytest, Jest -->
- **Test location:** <!-- e.g., src/test/java (matching package structure), tests/ -->
- **Build tool:** <!-- e.g., Gradle, Maven, npm, poetry -->
- **CI/CD:** <!-- e.g., GitHub Actions, Jenkins, GitLab CI -->

## Conventions
- **Test naming:** <!-- e.g., methodName_condition_expectedResult, test_descriptive_name -->
- **Test data:** <!-- e.g., TestDataBuilder pattern in src/test/helpers/, factories in tests/factories/ -->
- **Code style:** <!-- e.g., Google Java Style, Black + isort, team .editorconfig -->
- **PR requirements:** <!-- e.g., all tests pass, 80% coverage minimum, 1 approval -->

## Compliance
- **Framework:** <!-- e.g., FedRAMP Moderate, NIST 800-53 Rev 5, HIPAA, none -->
- **Data classification of this project:** <!-- e.g., CUI, Internal, Public -->
- **Security review required for:** <!-- e.g., auth flows, data handling, IaC, all changes -->

## Approved AI Tools
<!-- List the tools your team is authorized to use and any data classification limits. -->

| Tool | Approved Use | Data Classification Limit |
|------|-------------|--------------------------|
| <!-- e.g., GitHub Copilot --> | <!-- Code generation, completion --> | <!-- Internal --> |
| <!-- e.g., Claude --> | <!-- Documentation, analysis, test generation --> | <!-- Internal --> |

## Points of Contact

| Role | Name | When to Escalate |
|------|------|-----------------|
| Tech lead | <!-- name --> | Architectural decisions, scope questions |
| Security reviewer | <!-- name --> | High/critical risk AI outputs |
| Compliance POC | <!-- name --> | Data classification questions |

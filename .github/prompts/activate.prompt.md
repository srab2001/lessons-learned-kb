---
description: 'Install, update, or reinstall Activate Copilot using the activate-installer skill.'
agent: 'agent'
tools:
  - 'codebase'
  - 'run_in_terminal'
  - 'editFiles'
  - 'github'
---

# Activate

Use the `activate-installer` skill to install, update, or reinstall Activate Copilot in this repository.

## What to Do

1. Read the `activate-installer` skill file at `.github/skills/activate-installer/SKILL.md`
2. Follow the workflow defined in the skill end-to-end

## Accepted Commands

- `/activate install` — Run a fresh install (analyze repo, select tier, install files)
- `/activate install minimal` — Install the minimal tier only
- `/activate install standard` — Install the standard tier
- `/activate install advanced` — Install the advanced tier
- `/activate update` — Check for updates and apply them

If the user provides a tier, pass it to the skill. Otherwise, let the skill recommend one based on repository analysis.

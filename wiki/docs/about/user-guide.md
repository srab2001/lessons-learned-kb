---
title: "User Guide"
lifecycle: active
sensitivity: public
---

# User Guide

## What this KB is for

A small, high-confidence collection of pages that a delivery team can pull from when planning or steering an engagement: what happened on past projects, what recommendations follow from that, canonical best practices, failure patterns to watch for, and client-specific context.

## Adding new source material

1. Drop a markdown source file into the matching `context/<folder>/` directory (see [Admin](../admin.md) for the folder list).
2. Add a manifest entry.
3. Run (or dispatch) a KB synthesis session. See `agent/agents.md` for the full session workflow and `CLAUDE.md` for the editorial rules the agent follows.
4. Review the PR (or direct commit, for CI-triggered synthesis) before treating a page as reviewer-approved.

## Reading confidence and lifecycle

See the badge legend on the [Home](../index.md) page.

## Contributing improvements to this guide

This KB was bootstrapped from a proposal-capture KB template (`proposal-intelligence-kb`). As real usage patterns emerge, update this guide, `agent/style-guide.md`, and `structure.md` to reflect what's actually working.

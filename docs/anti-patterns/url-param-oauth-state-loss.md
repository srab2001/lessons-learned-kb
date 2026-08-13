---
title: "Anti-Pattern: Passing Transient State as a URL Parameter Through OAuth"
sources:
  - context/engagement-notes/consolidated-lessons-learned-2026-08-13.md
source_count: 1
as_of_date: "2026-08-13"
last_compiled: "2026-08-13"
lifecycle: draft
confidence: low
sensitivity: internal
lesson_type: [technical]
lifecycle_history:
  - date: "2026-08-13"
    from: ""
    to: draft
    reason: "initial synthesis from consolidated-lessons-learned-2026-08-13.md"
---

# Anti-Pattern: Passing Transient State as a URL Parameter Through OAuth

## What the pattern looks like

A redirect-to-destination or other transient piece of state (e.g., "where should the user land after login?") is passed as a URL query or hash parameter through an OAuth authorization/callback round trip, instead of being stored client-side and cleared before the redirect.

## Failure mode / symptom

In `meal_planner_app`, a `?returnTo=fitness` URL parameter was included in the OAuth redirect URL. It was not cleared after the OAuth callback completed, so the parameter effectively became sticky: every subsequent login — regardless of what the user actually intended — redirected to the fitness app.[^1]

**Related pitfall:** moving the state out of the URL and into `localStorage` does not fully fix this pattern on its own. In the same project, a `sso_return_to` value written to `localStorage` was not reliably cleared after being consumed — multiple code paths could set it, and there was no cleanup on error/fallback paths — which reproduced the same symptom (unwanted repeated redirects) through a different mechanism.[^2]

**Related pitfall:** integrating two systems that don't agree on the auth callback format is a distinct but adjacent failure mode. In the same project, a fitness app expected an auth callback hash of `#auth=token=xxx&user=xxx`, but the backend sent `#token=xxx` only, with no fallback handling — causing silent auth failures rather than a wrong redirect.[^3]

## Warning signs

- Logins unexpectedly and consistently redirect all users to the same unintended destination.
- Behavior differs between a direct login flow and an SSO/OAuth login flow for what should be equivalent logic.
- A "fix" that clears state at one point in the code doesn't fully resolve the symptom, because another code path (e.g., an error path) can still set or fail to clear the same state.

## What to do instead

1. Store transient state (e.g., the intended return-to destination) in `localStorage` **before** the OAuth redirect, not in the URL.
2. Clear the URL of any transient state immediately (e.g., `window.history.replaceState`) so it cannot leak into a later, unrelated navigation.
3. Remove the `localStorage` entry immediately after consuming it — including on error/fallback paths, not just the success path.
4. Document the expected callback format(s) for each integrated app, and add explicit fallback handling for any known alternate formats.
5. Test both the direct login flow and the SSO login flow explicitly, since they can silently diverge.[^1][^2][^3]

> **Gap:** The source does not report how many users or logins were affected, how long the misconfiguration was live, or how it was ultimately detected — only the root cause and code-level resolution. No frequency or impact metric is available, so this page cannot support a `docs/recommendations/` entry despite being clearly actionable.

---

[^1]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Authentication & SSO > URL Parameter Persistence Through OAuth.
[^2]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Authentication & SSO > State Not Cleared After Use (Stale localStorage).
[^3]: context/engagement-notes/consolidated-lessons-learned-2026-08-13.md — Authentication & SSO > URL Hash Format Mismatch Between Systems.

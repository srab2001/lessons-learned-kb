"""MkDocs hook: previously blanked restricted/internal pages at build time.

As of 2026-08-13, access control for this KB happens entirely at the login
gate (middleware.js + the ALLOWED_KB_EMAILS allow-list) -- the wiki is never
publicly reachable, and every allow-listed user is treated as a KB
maintainer per CLAUDE.md's sensitivity definitions (restricted content is
"never referenced outside KB maintainers" -- since ALLOWED_KB_EMAILS *is*
the maintainer group, anyone who can log in at all is meant to see
internal/restricted pages too, not just public ones).

This hook is intentionally a no-op now. It's kept in place (rather than
removed from wiki/mkdocs.yml's hooks list) so the per-page blanking
mechanism is easy to reintroduce if this KB ever needs tiered access
*within* the allow-listed group -- see agent/journal.md for the reasoning
behind dropping it.
"""

import logging

log = logging.getLogger("mkdocs.hooks.sensitivity_filter")


def on_page_markdown(markdown: str, page, config, files, **kwargs) -> str:
    return markdown

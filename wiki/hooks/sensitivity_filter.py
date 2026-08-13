"""MkDocs hook: block restricted/internal pages from the build output.

Pages with sensitivity: restricted or internal are excluded entirely.
This is a defense-in-depth measure — the nav in mkdocs.yml should only
reference public pages, but this hook prevents accidental exposure.
"""

import logging

log = logging.getLogger("mkdocs.hooks.sensitivity_filter")

ALLOWED = {"public", ""}


def on_page_markdown(markdown: str, page, config, files, **kwargs) -> str:
    sensitivity = str(page.meta.get("sensitivity", "public")).lower()
    if sensitivity not in ALLOWED:
        log.warning(
            "Page %s has sensitivity '%s' — replacing content with access notice.",
            page.file.src_path,
            sensitivity,
        )
        return (
            "# Access Restricted\n\n"
            "This page is not available in the public KB.\n"
        )
    return markdown

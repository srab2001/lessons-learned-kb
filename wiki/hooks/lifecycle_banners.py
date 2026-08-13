"""MkDocs hook: inject lifecycle status banners and "As of" source box into page content."""

import logging
import os

log = logging.getLogger("mkdocs.hooks.lifecycle_banners")

BANNERS = {
    "draft": (
        "info",
        "Draft",
        "This page is a draft and has not been reviewed. Content may be incomplete or unverified.",
    ),
    "stale": (
        "warning",
        "Stale Content",
        "One or more sources for this page have been updated since it was last compiled. "
        "The information below may not reflect the current state.",
    ),
    "contradicted": (
        "danger",
        "Contradicted",
        "New information contradicts some claims on this page. "
        "See flagged sections below for details.",
    ),
    "archived": (
        "abstract",
        "Archived",
        "This page has been archived and is retained for historical reference only.",
    ),
}


def _build_source_box(page) -> str:
    """Inject an 'As of' source box showing data currency and source files."""
    as_of = page.meta.get("as_of_date", "")
    sources = page.meta.get("sources", [])
    if not as_of and not sources:
        return ""
    lines = ['!!! abstract "Source & currency"']
    if as_of:
        lines.append(f"    **Data as of:** {as_of}")
    if sources:
        names = [os.path.basename(s) for s in sources]
        if len(names) == 1:
            lines.append(f"    **Source file:** `{names[0]}`")
        else:
            file_list = ", ".join(f"`{n}`" for n in names)
            lines.append(f"    **Source files ({len(names)}):** {file_list}")
        lines.append("    *(Full paths available in the [repo](https://github.com/srab2001/lessons-learned-kb/tree/main).)*")
    return "\n".join(lines) + "\n\n"


def on_page_markdown(markdown: str, page, config, files, **kwargs) -> str:
    lifecycle = page.meta.get("lifecycle", "").lower()

    # Build "As of" source box for content pages that have frontmatter dates
    as_of_box = ""
    if page.meta.get("as_of_date") or page.meta.get("sources"):
        as_of_box = _build_source_box(page)

    if not lifecycle or lifecycle == "active":
        return as_of_box + markdown

    banner_config = BANNERS.get(lifecycle)
    if not banner_config:
        log.warning("Unknown lifecycle state '%s' on page %s", lifecycle, page.file.src_path)
        return as_of_box + markdown
    admonition_type, title, message = banner_config
    banner = f'!!! {admonition_type} "{title}"\n    {message}\n\n'
    return banner + as_of_box + markdown

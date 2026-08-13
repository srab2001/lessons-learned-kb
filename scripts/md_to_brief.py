#!/usr/bin/env python3
"""
md_to_brief.py — Convert a Lessons Learned KB retrospective markdown page to a
printable standalone HTML brief. Outputs complete HTML to stdout.

Usage:
    python3 scripts/md_to_brief.py docs/retrospectives/example-project.md
"""

import sys
import re
import datetime

# ---------------------------------------------------------------------------
# Markdown conversion — use the `markdown` library if available, otherwise
# fall back to a minimal regex-based converter sufficient for KB page content.
# ---------------------------------------------------------------------------

try:
    import markdown as md_lib

    def convert_markdown(text):
        return md_lib.markdown(
            text,
            extensions=["tables", "footnotes", "fenced_code", "attr_list", "def_list"],
        )

except ImportError:
    def convert_markdown(text):
        """Minimal regex-based markdown converter (fallback)."""
        # Headings
        text = re.sub(r"^#{6}\s+(.+)$", r"<h6>\1</h6>", text, flags=re.MULTILINE)
        text = re.sub(r"^#{5}\s+(.+)$", r"<h5>\1</h5>", text, flags=re.MULTILINE)
        text = re.sub(r"^#{4}\s+(.+)$", r"<h4>\1</h4>", text, flags=re.MULTILINE)
        text = re.sub(r"^#{3}\s+(.+)$", r"<h3>\1</h3>", text, flags=re.MULTILINE)
        text = re.sub(r"^#{2}\s+(.+)$", r"<h2>\1</h2>", text, flags=re.MULTILINE)
        text = re.sub(r"^#{1}\s+(.+)$", r"<h1>\1</h1>", text, flags=re.MULTILINE)

        # Bold and italic
        text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)

        # Inline code
        text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)

        # Blockquotes
        text = re.sub(r"^>\s+(.+)$", r"<blockquote>\1</blockquote>", text, flags=re.MULTILINE)

        # Unordered lists (basic)
        text = re.sub(r"^[-*]\s+(.+)$", r"<li>\1</li>", text, flags=re.MULTILINE)
        text = re.sub(r"(<li>.*</li>)", r"<ul>\1</ul>", text, flags=re.DOTALL)

        # Horizontal rules
        text = re.sub(r"^---$", r"<hr>", text, flags=re.MULTILINE)

        # Links
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)

        # Paragraphs — wrap lines not already wrapped in tags
        lines = text.split("\n")
        result = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("<"):
                result.append(f"<p>{stripped}</p>")
            else:
                result.append(line)
        text = "\n".join(result)

        return text


# ---------------------------------------------------------------------------
# Frontmatter extraction
# ---------------------------------------------------------------------------

def parse_frontmatter(content):
    """Extract YAML frontmatter from a markdown file. Returns (meta_dict, body)."""
    meta = {}
    body = content

    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            fm_block = content[3:end].strip()
            body = content[end + 4:].strip()
            for line in fm_block.splitlines():
                m = re.match(r"^(\w[\w_-]*):\s*(.*)$", line)
                if m:
                    key = m.group(1)
                    val = m.group(2).strip().strip('"')
                    meta[key] = val
                # Handle list items for lesson_type
                m_list = re.match(r"^\s+-\s+(.+)$", line)
                if m_list:
                    # Append to last list key
                    last_key = list(meta.keys())[-1] if meta else None
                    if last_key:
                        existing = meta[last_key]
                        if isinstance(existing, list):
                            existing.append(m_list.group(1).strip())
                        else:
                            # Convert to list if the value was empty or []
                            meta[last_key] = [m_list.group(1).strip()]

    return meta, body


# ---------------------------------------------------------------------------
# Badge helpers
# ---------------------------------------------------------------------------

CONFIDENCE_COLORS = {
    "high": "#1a7f37",
    "medium": "#9a6700",
    "low": "#cf222e",
}

LIFECYCLE_COLORS = {
    "draft": "#6e40c9",
    "active": "#1a7f37",
    "stale": "#9a6700",
    "contradicted": "#cf222e",
    "archived": "#57606a",
}


def badge(label, value, bg_color):
    return (
        f'<span class="badge" style="background:{bg_color};color:#fff;">'
        f"{label}: {value}</span>"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: md_to_brief.py <path-to-kb-page.md>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        raw = f.read()

    meta, body = parse_frontmatter(raw)

    title = meta.get("title", "Retrospective Brief")
    as_of_date = meta.get("as_of_date", "")
    lifecycle = meta.get("lifecycle", "draft").lower()
    confidence = meta.get("confidence", "low").lower()
    sensitivity = meta.get("sensitivity", "internal")

    # Lesson types — may be a string like "[]" or a list
    lesson_type_raw = meta.get("lesson_type", "")
    if isinstance(lesson_type_raw, list):
        lesson_types = lesson_type_raw
    else:
        # Parse "[process, technical]" or "[]"
        lesson_types = [
            x.strip().strip("[]")
            for x in re.split(r"[,\[\]]", lesson_type_raw)
            if x.strip().strip("[]")
        ]

    generated_date = datetime.date.today().isoformat()

    is_draft = lifecycle != "active"
    watermark_html = ""
    if is_draft:
        watermark_html = '<div class="watermark">DRAFT — For Internal Use Only</div>'

    conf_color = CONFIDENCE_COLORS.get(confidence, "#57606a")
    life_color = LIFECYCLE_COLORS.get(lifecycle, "#57606a")

    lesson_type_badges = " ".join(
        f'<span class="mfactor-badge">{lt}</span>' for lt in lesson_types
    ) if lesson_types else '<span class="mfactor-badge">none specified</span>'

    body_html = convert_markdown(body)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Lessons Learned KB Brief</title>
  <style>
    /* ---- Reset & base ---- */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: Georgia, 'Times New Roman', serif;
      font-size: 11pt;
      line-height: 1.6;
      color: #1c1c1c;
      background: #ffffff;
      max-width: 800px;
      margin: 0 auto;
      padding: 0 1.5rem 2rem;
    }}

    /* ---- Top banner ---- */
    .banner {{
      background: #0c2340;
      color: #ffffff;
      padding: 0.6rem 1.2rem;
      margin: 0 -1.5rem 1.5rem;
      display: flex;
      flex-direction: column;
    }}
    .banner .kb-label {{
      font-size: 8pt;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      opacity: 0.75;
      font-family: Arial, sans-serif;
      margin-bottom: 0.25rem;
    }}
    .banner h1 {{
      font-size: 18pt;
      font-weight: bold;
      font-family: Georgia, serif;
      line-height: 1.2;
    }}

    /* ---- Metadata bar ---- */
    .meta-bar {{
      background: #f6f8fa;
      border: 1px solid #d0d7de;
      border-radius: 4px;
      padding: 0.6rem 1rem;
      margin-bottom: 1.5rem;
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      align-items: center;
      font-family: Arial, sans-serif;
      font-size: 9pt;
    }}
    .meta-bar .meta-item {{
      color: #57606a;
    }}
    .meta-bar .meta-item strong {{
      color: #1c1c1c;
    }}
    .badge {{
      display: inline-block;
      padding: 0.2em 0.55em;
      border-radius: 2px;
      font-size: 8pt;
      font-weight: bold;
      font-family: Arial, sans-serif;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    .mfactor-badge {{
      display: inline-block;
      padding: 0.15em 0.5em;
      border-radius: 2px;
      font-size: 8pt;
      font-family: Arial, sans-serif;
      background: #ddf4ff;
      color: #0550ae;
      border: 1px solid #0550ae;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}

    /* ---- Watermark ---- */
    .watermark {{
      position: fixed;
      top: 45%;
      left: 50%;
      transform: translate(-50%, -50%) rotate(-35deg);
      font-size: 52pt;
      font-family: Arial, sans-serif;
      font-weight: 900;
      color: rgba(207, 34, 46, 0.08);
      pointer-events: none;
      white-space: nowrap;
      z-index: 0;
      user-select: none;
    }}

    /* ---- Body content ---- */
    .content {{ position: relative; z-index: 1; }}

    h2 {{
      font-size: 13pt;
      font-weight: bold;
      border-bottom: 1px solid #d0d7de;
      padding-bottom: 0.2rem;
      margin: 1.4rem 0 0.6rem;
      color: #0c2340;
    }}
    h3 {{
      font-size: 11pt;
      font-weight: bold;
      margin: 1rem 0 0.4rem;
      color: #1c1c1c;
    }}
    h4, h5, h6 {{
      font-size: 10pt;
      font-weight: bold;
      margin: 0.8rem 0 0.3rem;
    }}
    p {{ margin-bottom: 0.7rem; }}
    ul, ol {{ margin: 0.4rem 0 0.7rem 1.5rem; }}
    li {{ margin-bottom: 0.25rem; }}

    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 0.8rem 0 1rem;
      font-size: 10pt;
    }}
    th {{
      background: #0c2340;
      color: #ffffff;
      text-align: left;
      padding: 0.4rem 0.6rem;
      font-family: Arial, sans-serif;
      font-size: 9pt;
    }}
    td {{
      padding: 0.35rem 0.6rem;
      border-bottom: 1px solid #e8ecef;
      vertical-align: top;
    }}
    tr:nth-child(even) td {{ background: #f6f8fa; }}

    blockquote {{
      border-left: 3px solid #d0d7de;
      margin: 0.5rem 0;
      padding: 0.4rem 0.8rem;
      color: #57606a;
      font-size: 10pt;
    }}
    blockquote strong {{ color: #cf222e; }}

    code {{
      font-family: 'Courier New', monospace;
      font-size: 9pt;
      background: #f6f8fa;
      padding: 0.1em 0.3em;
      border-radius: 2px;
    }}
    pre {{
      background: #f6f8fa;
      border: 1px solid #d0d7de;
      padding: 0.6rem;
      border-radius: 3px;
      overflow-x: auto;
      font-size: 9pt;
    }}

    /* ---- Footnotes ---- */
    .footnotes {{
      margin-top: 2rem;
      padding-top: 0.8rem;
      border-top: 1px solid #d0d7de;
      font-size: 9pt;
      color: #57606a;
    }}
    sup {{ font-size: 8pt; color: #0550ae; }}

    /* ---- Footer ---- */
    .brief-footer {{
      margin-top: 2.5rem;
      padding-top: 0.6rem;
      border-top: 1px solid #d0d7de;
      font-size: 8pt;
      color: #57606a;
      font-family: Arial, sans-serif;
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 0.3rem;
    }}

    /* ---- Print styles ---- */
    @media print {{
      body {{ max-width: 100%; padding: 0; font-size: 10pt; }}
      .banner {{
        background: #ffffff !important;
        color: #000000 !important;
        border-bottom: 2pt solid #000000;
        margin: 0 0 1rem;
        padding: 0.5rem 0;
      }}
      .banner .kb-label {{ color: #000000; opacity: 1; }}
      .banner h1 {{ color: #000000; font-size: 16pt; }}
      .watermark {{ display: none; }}
      .meta-bar {{ border: 1pt solid #999; }}
      h2 {{ color: #000000; }}
      table {{ page-break-inside: avoid; }}
      @page {{
        size: Letter;
        margin: 0.75in 0.75in 0.75in 0.75in;
      }}
    }}
  </style>
</head>
<body>

  <div class="banner">
    <span class="kb-label">Lessons Learned KB</span>
    <h1>{title}</h1>
  </div>

  <div class="meta-bar">
    {f'<span class="meta-item"><strong>As of:</strong> {as_of_date}</span>' if as_of_date else ''}
    {badge("Confidence", confidence, conf_color)}
    {badge("Lifecycle", lifecycle, life_color)}
    <span class="meta-item"><strong>Lesson Types:</strong> {lesson_type_badges}</span>
    <span class="meta-item" style="margin-left:auto;"><strong>Sensitivity:</strong> {sensitivity.upper()}</span>
  </div>

  {watermark_html}

  <div class="content">
    {body_html}
  </div>

  <div class="brief-footer">
    <span>Generated from Lessons Learned KB</span>
    <span>Generated: {generated_date}</span>
  </div>

</body>
</html>
"""

    print(html)


if __name__ == "__main__":
    main()

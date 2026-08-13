#!/usr/bin/env python3
"""
repo_to_context.py — Stage candidate Lessons Learned KB source material from
an external GitHub repository into context/, for a later synthesis session.

This tool does ONE thing: find raw material in a target repo and copy it into
the right context/<folder>/ with a manifest.yaml entry. It never writes
docs/ pages, never invents a metric, and never assigns lifecycle: active or
confidence: high — per CLAUDE.md, that requires an actual synthesis session
and human reviewer approval. Treat everything this tool stages as unreviewed.

How it decides what to fetch, per repo:
  1. Look for existing lessons-learned-shaped markdown files already committed
     in the repo (filenames/content matching retrospective, postmortem,
     incident, anti-pattern, best-practice, recommendation, or lessons-learned
     patterns) and classify each into the matching context/ subfolder.
  2. If none are found, fall back to a repo-activity digest: README + recent
     closed PRs + recent closed issues, assembled into one clearly-labeled
     "inferred, not authored" markdown file staged under context/engagement-notes/
     (the catch-all folder for material that hasn't been classified yet).

KB section -> context/ folder mapping (client-context has no dedicated raw
folder; per structure.md, client-context KB pages are sourced from
context/engagement-notes/):
  retrospectives   -> context/retrospectives/
  recommendations  -> context/recommendations-raw/
  incident reviews -> context/incident-reviews-raw/
  capability areas -> context/capability-areas/
  best practices   -> context/best-practices-raw/
  client context   -> context/engagement-notes/
  anti-patterns    -> context/anti-patterns-raw/

Usage:
    export GITHUB_TOKEN=ghp_...        # optional but recommended (rate limits)
    python3 scripts/repo_to_context.py owner/repo
    python3 scripts/repo_to_context.py owner/repo --branch main --dry-run
    python3 scripts/repo_to_context.py owner/repo --context-root context

Requires: pyyaml (see scripts/requirements.txt)
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request

try:
    import yaml
except ImportError:
    print(
        "error: pyyaml is required. Install with: pip install -r scripts/requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)

GITHUB_API = "https://api.github.com"
USER_AGENT = "lessons-learned-kb-repo-to-context/1.0"

# Every context/ folder this tool can stage into, and its sensitivity default.
# Kept in sync by hand with context/manifest.yaml -- if that file's defaults
# change, update this dict to match.
FOLDER_SENSITIVITY = {
    "retrospectives": "internal",
    "recommendations-raw": "internal",
    "incident-reviews-raw": "restricted",
    "anti-patterns-raw": "restricted",
    "engagement-notes": "internal",
    "capability-areas": "public",
    "best-practices-raw": "internal",
}

# Filename/content patterns that mark a markdown file as a *candidate* --
# worth inspecting further to classify -- versus ordinary repo documentation.
CANDIDATE_RE = re.compile(
    r"(?i)(lesson|retrospective|retro\b|postmortem|post-mortem|incident|"
    r"runbook|\brca\b|root[-_ ]?cause|anti[-_ ]?pattern|best[-_ ]?practice)"
)

# Classification rules, most specific first. Each is (regex, target_folder).
# Checked against "filename + first 2000 chars of content", lowercased.
CLASSIFY_RULES = [
    (re.compile(r"(?i)(incident|postmortem|post-mortem|outage|\brca\b|root[-_ ]?cause)"), "incident-reviews-raw"),
    (re.compile(r"(?i)(anti[-_ ]?pattern|\bmistake\b|what went wrong|don't repeat|do not repeat)"), "anti-patterns-raw"),
    (re.compile(r"(?i)best[-_ ]?practice"), "best-practices-raw"),
    (re.compile(r"(?i)recommendation"), "recommendations-raw"),
    (re.compile(r"(?i)(capability|architecture overview|platform overview)"), "capability-areas"),
    (re.compile(r"(?i)(retrospective|retro\b|lessons?[-_ ]?learned)"), "retrospectives"),
]
DEFAULT_FOLDER = "engagement-notes"  # unclassified candidates and the activity digest


def gh_request(url, token, accept="application/vnd.github+json"):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise SystemExit(f"error: GitHub API request failed ({e.code}) for {url}\n{body}")


def gh_json(url, token):
    return json.loads(gh_request(url, token).decode("utf-8"))


def get_default_branch(owner, repo, token):
    data = gh_json(f"{GITHUB_API}/repos/{owner}/{repo}", token)
    return data["default_branch"]


def get_tree(owner, repo, branch, token):
    data = gh_json(f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1", token)
    if data.get("truncated"):
        print("warning: repo tree was truncated by the GitHub API; some files may be missed", file=sys.stderr)
    return [item for item in data.get("tree", []) if item.get("type") == "blob" and item["path"].endswith(".md")]


def fetch_raw(owner, repo, branch, path, token):
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def classify(path, content):
    haystack = (path + "\n" + content[:2000]).lower()
    for pattern, folder in CLASSIFY_RULES:
        if pattern.search(haystack):
            return folder
    return DEFAULT_FOLDER


def get_readme(owner, repo, token):
    try:
        return gh_request(
            f"{GITHUB_API}/repos/{owner}/{repo}/readme", token, accept="application/vnd.github.raw"
        ).decode("utf-8", "replace")
    except SystemExit:
        return ""


def get_closed_prs(owner, repo, token, limit):
    data = gh_json(
        f"{GITHUB_API}/repos/{owner}/{repo}/pulls?state=closed&sort=updated&direction=desc&per_page={limit}",
        token,
    )
    return data


def get_closed_issues(owner, repo, token, limit):
    data = gh_json(
        f"{GITHUB_API}/repos/{owner}/{repo}/issues?state=closed&sort=updated&direction=desc&per_page={limit}",
        token,
    )
    return [item for item in data if "pull_request" not in item]  # issues endpoint also returns PRs


def build_activity_digest(owner, repo, branch, token, max_items):
    readme = get_readme(owner, repo, token)
    prs = get_closed_prs(owner, repo, token, max_items)
    issues = get_closed_issues(owner, repo, token, max_items)

    lines = [
        f"# {owner}/{repo} — Repo Activity Digest",
        "",
        f"**Generated:** {datetime.date.today().isoformat()} by `scripts/repo_to_context.py`",
        f"**Branch:** {branch}",
        "",
        "> **Gap:** No existing lessons-learned-shaped document was found in this repo. "
        "Everything below is *inferred* from README, closed PR, and closed issue text — "
        "it is not an authored retrospective or postmortem. Treat as low-confidence raw "
        "material; a synthesis session must read the actual PRs/issues linked below before "
        "any claim from this digest is written into a docs/ page, and no metric here should "
        "be trusted without checking the source PR/issue directly.",
        "",
        "---",
        "",
        "## README (excerpt)",
        "",
        (readme[:3000] + ("\n\n...(truncated)" if len(readme) > 3000 else "")) if readme else "_No README found._",
        "",
        "---",
        "",
        f"## Recently closed pull requests (up to {max_items})",
        "",
    ]
    if prs:
        for pr in prs:
            lines.append(f"### #{pr['number']}: {pr['title']}")
            lines.append(f"- URL: {pr['html_url']}")
            lines.append(f"- Merged: {pr.get('merged_at') or 'not merged'}")
            body = (pr.get("body") or "").strip()
            if body:
                lines.append("")
                lines.append(body[:1500] + ("\n\n...(truncated)" if len(body) > 1500 else ""))
            lines.append("")
    else:
        lines.append("_No closed pull requests found._")
        lines.append("")

    lines += ["---", "", f"## Recently closed issues (up to {max_items})", ""]
    if issues:
        for issue in issues:
            lines.append(f"### #{issue['number']}: {issue['title']}")
            lines.append(f"- URL: {issue['html_url']}")
            body = (issue.get("body") or "").strip()
            if body:
                lines.append("")
                lines.append(body[:1500] + ("\n\n...(truncated)" if len(body) > 1500 else ""))
            lines.append("")
    else:
        lines.append("_No closed issues found._")
        lines.append("")

    return "\n".join(lines)


def load_manifest(folder_dir):
    manifest_path = os.path.join(folder_dir, "manifest.yaml")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r") as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}
    data.setdefault("folder", os.path.relpath(folder_dir))
    data.setdefault("files", [])
    return data, manifest_path


def save_manifest(data, manifest_path):
    data["last_updated"] = datetime.date.today().isoformat()
    with open(manifest_path, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False, default_flow_style=False)


def already_staged(manifest_data, filename, content_hash):
    for entry in manifest_data.get("files", []):
        if entry.get("path") == filename and entry.get("content_hash") == f"sha256:{content_hash}":
            return True
    return False


def stage_file(context_root, folder, filename, content, source_note, dry_run):
    folder_dir = os.path.join(context_root, folder)
    os.makedirs(folder_dir, exist_ok=True)
    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    manifest_data, manifest_path = load_manifest(folder_dir)

    if already_staged(manifest_data, filename, content_hash):
        print(f"  = unchanged, skipping: context/{folder}/{filename}")
        return

    file_path = os.path.join(folder_dir, filename)
    print(f"  + staging: context/{folder}/{filename}  ({source_note})")
    if dry_run:
        return

    with open(file_path, "w") as f:
        f.write(content)

    manifest_data["files"] = [e for e in manifest_data.get("files", []) if e.get("path") != filename]
    manifest_data["files"].append(
        {
            "path": filename,
            "as_of_date": datetime.date.today().isoformat(),
            "content_hash": f"sha256:{content_hash}",
            "temporal_status": "current",
            "sensitivity": FOLDER_SENSITIVITY[folder],
            "kb_impact": [],
        }
    )
    save_manifest(manifest_data, manifest_path)


def slugify(text):
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "file"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo", help="Target repo as owner/repo, e.g. srab2001/travel-deal-finder")
    parser.add_argument("--branch", default=None, help="Branch to read (default: repo's default branch)")
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"), help="GitHub token (default: $GITHUB_TOKEN)")
    parser.add_argument("--context-root", default="context", help="Path to this KB's context/ directory")
    parser.add_argument("--max-activity-items", type=int, default=15, help="Max PRs/issues in the activity-digest fallback")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be staged without writing files")
    args = parser.parse_args()

    if "/" not in args.repo:
        parser.error("repo must be in owner/repo form")
    owner, repo = args.repo.split("/", 1)

    branch = args.branch or get_default_branch(owner, repo, args.token)
    print(f"Scanning {owner}/{repo}@{branch} for existing lessons-learned-shaped documents...")

    md_files = get_tree(owner, repo, branch, args.token)
    candidates = [f for f in md_files if CANDIDATE_RE.search(f["path"])]

    if not candidates:
        print("No candidate documents found by filename. Falling back to a repo-activity digest.")
        digest = build_activity_digest(owner, repo, branch, args.token, args.max_activity_items)
        filename = f"{slugify(repo)}-activity-digest-{datetime.date.today().isoformat()}.md"
        stage_file(
            args.context_root, DEFAULT_FOLDER, filename, digest,
            source_note="inferred from README/PRs/issues, not an authored doc",
            dry_run=args.dry_run,
        )
    else:
        print(f"Found {len(candidates)} candidate document(s); fetching and classifying each.")
        for item in candidates:
            content = fetch_raw(owner, repo, branch, item["path"], args.token)
            folder = classify(item["path"], content)
            filename = f"{slugify(repo)}-{slugify(os.path.basename(item['path']))}.md"
            header = (
                f"<!-- Staged from {owner}/{repo}@{branch}:{item['path']} "
                f"by scripts/repo_to_context.py on {datetime.date.today().isoformat()}. "
                f"Unreviewed -- classification into '{folder}' is a heuristic guess, not "
                f"a synthesis decision. Verify section fit and every claim before promoting "
                f"to a docs/ page. -->\n\n"
            )
            stage_file(
                args.context_root, folder, filename, header + content,
                source_note=f"classified as {folder} from {item['path']}",
                dry_run=args.dry_run,
            )

    print()
    print("Done. Nothing was written to docs/ -- this only staged raw material into context/.")
    print("Next step: run a KB synthesis session (see agent/agents.md) to turn staged files into")
    print("reviewed docs/ pages. Do not mark any resulting page active or confidence: high without")
    print("explicit reviewer approval, per CLAUDE.md.")


if __name__ == "__main__":
    main()

"""Restore current upstream protected Markdown units in translated files.

This helper deliberately changes only code fences, HTML comments, anchors, and
Listing attributes. It never changes prose or inline code automatically; a
token-count mismatch is reported for manual review instead of guessed.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


FENCE_RE = re.compile(
    r"(?ms)^(?:> ?)*```[^\n]*\n.*?^(?:> ?)*```[ \t]*(?:\r?\n|$)"
)
COMMENT_RE = re.compile(r"(?s)<!--.*?-->")
LISTING_RE = re.compile(r'<\/?Listing\b(?:"[^"]*"|[^>])*?>')
ANCHOR_RE = re.compile(r'<a\s+(?:id|name)="[^"]+"\s*>')


def upstream_text(root: Path, ref: str, relative: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"{ref}:{relative}"],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    return result.stdout if result.returncode == 0 else None


def replace_units(
    translated: str,
    upstream: str,
    pattern: re.Pattern[str],
    kind: str,
) -> tuple[str, list[str]]:
    expected = list(pattern.finditer(upstream))
    actual = list(pattern.finditer(translated))
    if len(expected) != len(actual):
        return translated, [f"{kind}: upstream {len(expected)}, translation {len(actual)}"]

    chunks: list[str] = []
    cursor = 0
    for source_match, translated_match in zip(expected, actual):
        chunks.append(translated[cursor : translated_match.start()])
        chunks.append(source_match.group(0))
        cursor = translated_match.end()
    chunks.append(translated[cursor:])
    return "".join(chunks), []


def restore_listing_tags(translated: str, upstream: str) -> tuple[str, list[str]]:
    expected = list(LISTING_RE.finditer(upstream))
    actual = list(LISTING_RE.finditer(translated))
    if len(expected) != len(actual):
        return translated, [f"Listing tag: upstream {len(expected)}, translation {len(actual)}"]

    chunks: list[str] = []
    cursor = 0
    caption_re = re.compile(r'(\bcaption\s*=\s*")[^"]*(")')
    for source_match, translated_match in zip(expected, actual):
        source_tag = source_match.group(0)
        translated_tag = translated_match.group(0)
        translated_caption = caption_re.search(translated_tag)
        if translated_caption:
            visible_caption = translated_caption.group(0)
            source_tag = caption_re.sub(visible_caption, source_tag, count=1)
        chunks.append(translated[cursor : translated_match.start()])
        chunks.append(source_tag)
        cursor = translated_match.end()
    chunks.append(translated[cursor:])
    return "".join(chunks), []


def restore_file(root: Path, path: Path, ref: str) -> list[str]:
    relative = path.relative_to(root).as_posix()
    source = upstream_text(root, ref, relative)
    if source is None:
        return [f"{relative}: cannot read {ref}:{relative}"]
    translated = path.read_text(encoding="utf-8")
    issues: list[str] = []
    for pattern, kind in (
        (FENCE_RE, "code block"),
        (COMMENT_RE, "HTML comment"),
        (ANCHOR_RE, "anchor"),
    ):
        translated, current_issues = replace_units(translated, source, pattern, kind)
        issues.extend(current_issues)
    translated, current_issues = restore_listing_tags(translated, source)
    issues.extend(current_issues)
    if translated != path.read_text(encoding="utf-8"):
        path.write_text(translated, encoding="utf-8")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--upstream-ref", default="upstream/main")
    args = parser.parse_args()
    root = args.root.resolve()
    all_issues: list[str] = []
    for path in sorted((root / "src").glob("*.md")):
        issues = restore_file(root, path, args.upstream_ref)
        all_issues.extend(issues)
    if all_issues:
        print("\n".join(all_issues))
        return 1
    print("restored current upstream protected Markdown units")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

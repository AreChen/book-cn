"""Normalize repeated blank lines in visible Markdown prose.

Translation snapshots often contain several empty lines around headings and
listings. Collapsing those runs improves readability and lets structural tools
align paragraphs, while fenced code and HTML comments are copied unchanged.
"""

from __future__ import annotations

import re
from pathlib import Path


FENCE_PATTERN = r"^(?:> ?)*```[^\n]*\n.*?^(?:> ?)*```[ \t]*(?:\r?\n|$)"
FENCE_RE = re.compile(FENCE_PATTERN, re.MULTILINE | re.DOTALL)
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
PROTECTED_RE = re.compile(
    rf"(?P<fence>{FENCE_PATTERN})|(?P<comment><!--.*?-->)",
    re.MULTILINE | re.DOTALL,
)
BLANK_RUN_RE = re.compile(r"(?:\r?\n[ \t]*){3,}")


def normalize(text: str) -> str:
    chunks: list[str] = []
    cursor = 0
    for match in PROTECTED_RE.finditer(text):
        visible = text[cursor : match.start()]
        chunks.append(BLANK_RUN_RE.sub("\n\n", visible))
        chunks.append(match.group(0))
        cursor = match.end()
    chunks.append(BLANK_RUN_RE.sub("\n\n", text[cursor:]))
    return "".join(chunks)


def main() -> int:
    root = Path.cwd()
    changed = 0
    for path in sorted((root / "src").glob("*.md")):
        before = path.read_text(encoding="utf-8")
        after = normalize(before)
        if after != before:
            path.write_text(after, encoding="utf-8")
            changed += 1
    print(f"normalized {changed} Markdown files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

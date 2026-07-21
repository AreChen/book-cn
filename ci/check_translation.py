"""Static checks for the Chinese Book source.

The checker deliberately compares only structure and content that a translation
must not change. Natural-language prose and visible link labels are allowed to
differ from the English upstream source.
"""

from __future__ import annotations

import argparse
from collections import Counter
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


# mdBook also permits fenced blocks inside Markdown blockquotes.  The `>`
# prefix is part of the Markdown container, not part of the protected code
# content, so mask and compare those blocks as complete units as well.
FENCE_RE = re.compile(
    r"(?ms)^(?:> ?)*```[^\n]*\n.*?^(?:> ?)*```[ \t]*(?:\r?\n|$)"
)
INLINE_CODE_RE = re.compile(
    r"(?<!`)(?P<ticks>`+)(?!`)(?P<content>.*?)(?<!`)(?P=ticks)(?!`)",
    re.DOTALL,
)
URL_RE = re.compile(r"(?<![\w])(?:https?://|mailto:)[^\s<>)\]\"`']+")
LINK_TARGET_RE = re.compile(r"\]\(\s*(?:<([^>]+)>|([^\s)]+))")
REFERENCE_TARGET_RE = re.compile(r"(?m)^\[[^\]\n]+\]:\s*(?:<([^>]+)>|(\S+))")
HTML_COMMENT_RE = re.compile(r"(?s)<!--.*?-->")
LISTING_TAG_RE = re.compile(r'<\/?Listing\b(?:"[^"]*"|[^>])*?>')
FILENAME_RE = re.compile(r'<span class="filename">(.*?)</span>')
ANCHOR_RE = re.compile(r'<a\s+(?:id|name)="([^"]+)"\s*>')
HEADING_RE = re.compile(r"(?m)^#{1,6}\s+.+?\s*$")
SUMMARY_LINK_RE = re.compile(r"(?<!\!)\[[^\]\n]+\]\(([^)\n]+)\)")
HAN_RE = re.compile(r"[\u3400-\u9fff]")

# Links maintained only by this translation project and intentionally absent
# from the official English source.
TRANSLATION_ONLY_URLS = frozenset({"https://arechen.github.io/book-cn/"})
TRANSLATION_ANCHOR_RE = re.compile(r"[a-z0-9][a-z0-9-]*")


def _normalize_listing_tag(tag: str) -> str:
    """Ignore only the human-readable Listing caption."""

    return re.sub(r'(\bcaption\s*=\s*")[^"]*(")', r'\1<translated>\2', tag)


def _mask_fenced_blocks(text: str) -> str:
    """Hide fenced code while checking prose-level protected tokens."""

    return FENCE_RE.sub(
        lambda match: "\n" * match.group(0).count("\n"),
        text,
    )


def _mask_html_comments(text: str) -> str:
    """Hide HTML comments while checking visible Markdown prose."""

    return HTML_COMMENT_RE.sub(
        lambda match: "\n" * match.group(0).count("\n"),
        text,
    )


def _filename_path(value: str) -> str:
    """Return the path part while permitting a translated visible label."""

    value = value.strip()
    if ":" in value:
        return value.rsplit(":", 1)[1].strip()
    if "：" in value:
        return value.rsplit("：", 1)[1].strip()
    return value


def _urls(text: str) -> list[str]:
    punctuation = ".,;:!?，。；：！？"
    return [value.rstrip(punctuation) for value in URL_RE.findall(text)]


def protected_tokens(text: str) -> dict[str, list[str]]:
    """Extract ordered tokens that translation must preserve."""

    without_fences = _mask_fenced_blocks(text)
    prose = _mask_html_comments(without_fences)
    link_targets = []
    for match in LINK_TARGET_RE.finditer(prose):
        link_targets.append(match.group(1) or match.group(2))
    for match in REFERENCE_TARGET_RE.finditer(prose):
        link_targets.append(match.group(1) or match.group(2))

    return {
        "code block": FENCE_RE.findall(text),
        "inline code": [
            match.group(0) for match in INLINE_CODE_RE.finditer(prose)
        ],
        "URL": _urls(prose),
        "link target": link_targets,
        "HTML comment": HTML_COMMENT_RE.findall(without_fences),
        "Listing tag": [_normalize_listing_tag(tag) for tag in LISTING_TAG_RE.findall(prose)],
        "filename path": [_filename_path(value) for value in FILENAME_RE.findall(prose)],
        "anchor": ANCHOR_RE.findall(prose),
    }


def _remove_allowed_translation_urls(
    expected: list[str], actual: list[str], allowed: Iterable[str]
) -> list[str]:
    """Remove only allowlisted URL occurrences added by the translation."""

    allowed = set(allowed)
    expected_counts = Counter(expected)
    seen_allowed = Counter()
    filtered: list[str] = []
    for value in actual:
        if value in allowed:
            if seen_allowed[value] >= expected_counts[value]:
                continue
            seen_allowed[value] += 1
        filtered.append(value)
    return filtered


def _remove_translation_anchor_aliases(
    expected: list[str], actual: list[str]
) -> list[str]:
    """Remove English slug aliases added for translated headings."""

    expected_counts = Counter(expected)
    seen_aliases = Counter()
    filtered: list[str] = []
    for value in actual:
        if TRANSLATION_ANCHOR_RE.fullmatch(value):
            if seen_aliases[value] >= expected_counts[value]:
                continue
            seen_aliases[value] += 1
        filtered.append(value)
    return filtered


def compare_protected_tokens(
    source: str,
    translated: str,
    path: str = "source",
    allowed_translation_urls: Iterable[str] = (),
) -> list[str]:
    """Return human-readable differences in protected token sequences."""

    issues: list[str] = []
    source_tokens = protected_tokens(source)
    translated_tokens = protected_tokens(translated)
    for kind, expected in source_tokens.items():
        actual = translated_tokens[kind]
        if kind == "URL":
            actual = _remove_allowed_translation_urls(
                expected, actual, allowed_translation_urls
            )
        elif kind == "anchor":
            actual = _remove_translation_anchor_aliases(expected, actual)
        if expected != actual:
            issues.append(
                f"{path}: {kind} differs (upstream {len(expected)}, translation {len(actual)})"
            )
    return issues


def markdown_structure_issues(text: str, path: str) -> list[str]:
    """Check the balanced structures needed by the Book preprocessor."""

    issues: list[str] = []
    opening_fences = len(re.findall(r"(?m)^(?:> ?)*```", text))
    if opening_fences % 2:
        issues.append(f"{path}: unbalanced fenced code block")
    if text.count("<Listing") != text.count("</Listing>"):
        issues.append(f"{path}: unbalanced Listing tags")
    if text.count("[") < text.count("]("):
        issues.append(f"{path}: unmatched Markdown link bracket")
    return issues


def validate_summary_links(root: Path) -> list[str]:
    """Ensure every relative file target in src/SUMMARY.md exists."""

    summary_path = root / "src" / "SUMMARY.md"
    if not summary_path.exists():
        return ["src/SUMMARY.md: file is missing"]

    issues: list[str] = []
    summary_dir = summary_path.parent
    for match in SUMMARY_LINK_RE.finditer(summary_path.read_text(encoding="utf-8")):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#", 1)[0].split("?", 1)[0]
        if not target:
            continue
        candidate = (summary_dir / target).resolve()
        if not candidate.exists():
            issues.append(f"src/SUMMARY.md: missing link target {target}")
    return issues


def _run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def _upstream_file(root: Path, ref: str, relative: str) -> str | None:
    result = _run_git(root, "show", f"{ref}:{relative}")
    if result.returncode != 0:
        return None
    return result.stdout


def _upstream_markdown_files(root: Path, ref: str) -> list[str] | None:
    result = _run_git(root, "ls-tree", "-r", "--name-only", ref, "src")
    if result.returncode != 0:
        return None
    return sorted(
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip().startswith("src/") and line.strip().endswith(".md")
    )


def validate_source(root: Path, upstream_ref: str, require_chinese: bool) -> list[str]:
    """Validate the working tree against the selected upstream ref."""

    issues: list[str] = []
    current_files = sorted(
        str(path.relative_to(root)).replace("\\", "/")
        for path in (root / "src").glob("*.md")
    )
    upstream_files = _upstream_markdown_files(root, upstream_ref)
    if upstream_files is None:
        issues.append(
            f"cannot read upstream ref {upstream_ref!r}; fetch it or pass --allow-missing-upstream"
        )
        upstream_files = current_files
    if current_files != upstream_files:
        issues.append(
            f"src file inventory differs (upstream {len(upstream_files)}, working tree {len(current_files)})"
        )

    for relative in current_files:
        path = root / relative
        text = path.read_text(encoding="utf-8")
        issues.extend(markdown_structure_issues(text, relative))
        if require_chinese and not HAN_RE.search(text):
            issues.append(f"{relative}: no Simplified Chinese text found")
        upstream = _upstream_file(root, upstream_ref, relative)
        if upstream is not None:
            issues.extend(
                compare_protected_tokens(
                    upstream,
                    text,
                    relative,
                    allowed_translation_urls=TRANSLATION_ONLY_URLS,
                )
            )

    issues.extend(validate_summary_links(root))
    return issues


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--upstream-ref", default="upstream/main")
    parser.add_argument("--require-chinese", action="store_true")
    parser.add_argument("--allow-missing-upstream", action="store_true")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = args.root.resolve()
    issues = validate_source(root, args.upstream_ref, args.require_chinese)
    if args.allow_missing_upstream:
        issues = [issue for issue in issues if "cannot read upstream ref" not in issue]
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        print(f"{len(issues)} translation check(s) failed")
        return 1
    print("translation structure checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

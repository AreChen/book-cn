"""Restore current upstream inline code and link destinations.

Inline code is part of the Rust Book's executable vocabulary, so translated
prose must keep it byte-for-byte identical to the selected upstream revision.
The replacement is performed independently between fenced-code blocks. This
prevents an omitted token in one paragraph from shifting every later token.
Files or prose segments with a count mismatch are reported for manual review.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ci"))
import check_translation as checker  # noqa: E402


INLINE_RE = checker.INLINE_CODE_RE
BLANK_LINE_RE = re.compile(r"(\r?\n[ \t]*\r?\n)")


def _mask_comments(text: str) -> str:
    """Replace comment characters with spaces while preserving offsets."""

    return checker.HTML_COMMENT_RE.sub(
        lambda match: "".join(
            "\n" if character == "\n" else " "
            for character in match.group(0)
        ),
        text,
    )


def split_fenced_units(text: str) -> tuple[list[str], list[str]]:
    """Split Markdown into prose segments and fenced-code units."""
    segments: list[str] = []
    units: list[str] = []
    cursor = 0
    for match in checker.FENCE_RE.finditer(text):
        segments.append(text[cursor : match.start()])
        units.append(match.group(0))
        cursor = match.end()
    segments.append(text[cursor:])
    return segments, units


def _replace_matches(
    translated: str,
    upstream: str,
    pattern: re.Pattern[str],
    kind: str,
    group: int = 0,
) -> tuple[str, list[str]]:
    source_scan = _mask_comments(upstream)
    translated_scan = _mask_comments(translated)
    source_matches = list(pattern.finditer(source_scan))
    translated_matches = list(pattern.finditer(translated_scan))
    if len(source_matches) != len(translated_matches):
        return translated, [
            f"{kind}: upstream {len(source_matches)}, translation {len(translated_matches)}"
        ]

    chunks: list[str] = []
    cursor = 0
    for source_match, translated_match in zip(source_matches, translated_matches):
        chunks.append(translated[cursor : translated_match.start(group)])
        chunks.append(
            upstream[source_match.start(group) : source_match.end(group)]
        )
        cursor = translated_match.end(group)
    chunks.append(translated[cursor:])
    return "".join(chunks), []


def _replace_urls(translated: str, upstream: str) -> tuple[str, list[str]]:
    source_scan = _mask_comments(upstream)
    translated_scan = _mask_comments(translated)
    source_matches = list(checker.URL_RE.finditer(source_scan))
    translated_matches = list(checker.URL_RE.finditer(translated_scan))
    if len(source_matches) != len(translated_matches):
        return translated, [
            f"URL: upstream {len(source_matches)}, translation {len(translated_matches)}"
        ]

    punctuation = ".,;:!?，。；：！？"
    chunks: list[str] = []
    cursor = 0
    for source_match, translated_match in zip(source_matches, translated_matches):
        source_raw = upstream[source_match.start() : source_match.end()]
        source_url = source_raw.rstrip(punctuation)
        translated_raw = translated[translated_match.start() : translated_match.end()]
        translated_url = translated_raw.rstrip(punctuation)
        suffix = translated_raw[len(translated_url) :]
        chunks.append(translated[cursor : translated_match.start()])
        chunks.append(source_url + suffix)
        cursor = translated_match.end()
    chunks.append(translated[cursor:])
    return "".join(chunks), []


def _replace_link_targets(
    translated: str, upstream: str, pattern: re.Pattern[str], kind: str
) -> tuple[str, list[str]]:
    source_scan = _mask_comments(upstream)
    translated_scan = _mask_comments(translated)
    source_matches = list(pattern.finditer(source_scan))
    translated_matches = list(pattern.finditer(translated_scan))
    if len(source_matches) != len(translated_matches):
        return translated, [
            f"{kind}: upstream {len(source_matches)}, translation {len(translated_matches)}"
        ]

    chunks: list[str] = []
    cursor = 0
    for source_match, translated_match in zip(source_matches, translated_matches):
        source_group = 1 if source_match.group(1) is not None else 2
        source_target = upstream[
            source_match.start(source_group) : source_match.end(source_group)
        ]
        target_group = 1 if translated_match.group(1) is not None else 2
        chunks.append(translated[cursor : translated_match.start(target_group)])
        chunks.append(source_target)
        cursor = translated_match.end(target_group)
    chunks.append(translated[cursor:])
    return "".join(chunks), []


def restore_segment(translated: str, upstream: str) -> tuple[str, list[str]]:
    source_parts = BLANK_LINE_RE.split(upstream)
    translated_parts = BLANK_LINE_RE.split(translated)
    if len(source_parts) != len(translated_parts):
        return translated, [
            f"paragraphs: upstream {len(source_parts)}, "
            f"translation {len(translated_parts)}"
        ]

    output: list[str] = []
    issues: list[str] = []
    for index, (source_part, translated_part) in enumerate(
        zip(source_parts, translated_parts)
    ):
        if index % 2:
            output.append(translated_part)
            continue
        restored = translated_part
        for pattern, kind in (
            (INLINE_RE, "inline code"),
            (checker.LINK_TARGET_RE, "link target"),
            (checker.REFERENCE_TARGET_RE, "reference target"),
        ):
            if kind == "inline code":
                restored, current_issues = _replace_matches(
                    restored, source_part, pattern, kind
                )
            else:
                restored, current_issues = _replace_link_targets(
                    restored, source_part, pattern, kind
                )
            issues.extend(f"paragraph {index // 2}: {issue}" for issue in current_issues)
        restored, current_issues = _replace_urls(restored, source_part)
        issues.extend(f"paragraph {index // 2}: {issue}" for issue in current_issues)
        output.append(restored)
    return "".join(output), issues


def restore_file(root: Path, relative: str, ref: str) -> list[str]:
    path = root / relative
    source = checker._upstream_file(root, ref, relative)
    if source is None:
        return [f"{relative}: cannot read {ref}:{relative}"]

    translated = path.read_text(encoding="utf-8")
    source_segments, _ = split_fenced_units(source)
    translated_segments, translated_units = split_fenced_units(translated)
    issues: list[str] = []
    if len(source_segments) != len(translated_segments):
        return [
            f"{relative}: prose segments differ (upstream {len(source_segments)}, "
            f"translation {len(translated_segments)})"
        ]

    output: list[str] = []
    for index, (source_segment, translated_segment) in enumerate(
        zip(source_segments, translated_segments)
    ):
        restored, segment_issues = restore_segment(
            translated_segment, source_segment
        )
        issues.extend(
            f"{relative} segment {index}: {issue}" for issue in segment_issues
        )
        output.append(restored)
        if index < len(translated_units):
            output.append(translated_units[index])

    restored_file = "".join(output)
    if restored_file != translated:
        path.write_text(restored_file, encoding="utf-8")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--upstream-ref", default="upstream/main")
    args = parser.parse_args()
    root = args.root.resolve()

    all_issues: list[str] = []
    for path in sorted((root / "src").glob("*.md")):
        relative = path.relative_to(root).as_posix()
        all_issues.extend(restore_file(root, relative, args.upstream_ref))

    if all_issues:
        print("\n".join(all_issues))
        return 1
    print("restored current upstream inline code and link destinations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Import prose from the community translation without replacing current code.

The reference checkout predates the current Rust Book layout.  This helper uses
the current upstream files as the source of truth for headings, listings, code
fences, anchors, and link targets, then imports only prose paragraphs whose
technical markers can be aligned with the reference.  It is intentionally a
reviewable, one-time migration aid rather than part of the book build.
"""

from __future__ import annotations

import argparse
import difflib
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ROOT = Path(r"C:\Users\cmx27\AppData\Local\Temp\rust-lang-zh_CN\src")

FENCE_RE = re.compile(r"(?ms)^(?:> ?)*```[^\n]*\n.*?^(?:> ?)*```[ \t]*(?:\r?\n|$)")
INLINE_RE = re.compile(r"(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)", re.DOTALL)
URL_RE = re.compile(r"(?<![\w])(?:https?://|mailto:)[^\s<>)\]\\\"`']+")
LINK_TARGET_RE = re.compile(r"\]\(\s*(?:<([^>]+)>|([^\s)]+))")
REFERENCE_TARGET_RE = re.compile(r"(?m)^\[[^\]\n]+\]:\s*(?:<([^>]+)>|(\S+))")
HAN_RE = re.compile(r"[\u3400-\u9fff]")
HEADING_RE = re.compile(r"^#{1,6}\s+")
LISTING_RE = re.compile(r"^\s*</?Listing\b")
FILENAME_RE = re.compile(r"^\s*(?:<span class=\"filename\">|文件名[:：])")
ANCHOR_RE = re.compile(r"^\s*<(?:a\s+(?:id|name)=|/a>)")
COMMENT_RE = re.compile(r"^\s*<!--")
COMMENT_BLOCK_RE = re.compile(r"(?s)<!--.*?-->")
ANCHOR_BLOCK_RE = re.compile(r'<a\s+(?:id|name)="[^"]+"\s*>')
FILENAME_BLOCK_RE = re.compile(r'<span\s+class="filename">.*?</span>')


MONOLITHIC = {
    "ch01-00-getting-started.md": "Ch01_Getting_Started.md",
    "ch02-00-guessing-game-tutorial.md": "Ch02_Programming_a_Guessing_Game.md",
    "ch03-00-common-programming-concepts.md": "Ch03_Common_Programming_Concepts.md",
    "ch04-00-understanding-ownership.md": "Ch04_Understanding_Ownership.md",
    "ch05-00-structs.md": "Ch05_Using_Structs_to_Structure_Related_Data.md",
    "ch06-00-enums.md": "Ch06_Enums_and_Pattern_Matching.md",
    "ch07-00-managing-growing-projects-with-packages-crates-and-modules.md": "Ch07_Managing_Growing_Projects_with_Packages_Crates_and_Modules.md",
    "ch08-00-common-collections.md": "Ch08_Common_Collections.md",
    "ch09-00-error-handling.md": "Ch09_Error_Handling.md",
    "ch10-00-generics.md": "Ch10_Generic_Types_Traits_and_Lifetimes.md",
    "ch11-00-testing.md": "Ch11_Writing_Automated_Tests.md",
    "ch12-00-an-io-project.md": "Ch12_An_IO_Project_Building_a_Command_Line_Program.md",
    "ch13-00-functional-features.md": "Ch13_Functional_Language_Features_Iterators_and_Closures.md",
    "ch14-00-more-about-cargo.md": "Ch14_More_about_Cargo_and_Crates-io.md",
    "ch15-00-smart-pointers.md": "Ch15_Smart_Pointers.md",
    "ch16-00-concurrency.md": "Ch16_Fearless_Concurrency.md",
    "ch17-00-async-await.md": "Ch17_async_programming.md",
    "ch18-00-oop.md": "Ch18_Object_Oriented_Programming_Features_of_Rust.md",
    "ch19-00-patterns.md": "Ch19_Patterns_and_Matching.md",
    "ch20-00-advanced-features.md": "Ch20_Advanced_Features.md",
    "ch21-00-final-project-a-web-server.md": "Ch21_Final_Project_Building_a_Multithreaded_Web_Server.md",
    "appendix-00.md": "Appendix.md",
}

SUBFILES = {
    "ch01-01-installation.md": "getting_started/installation.md",
    "ch01-02-hello-world.md": "getting_started/hello_world.md",
    "ch01-03-hello-cargo.md": "getting_started/hello_cargo.md",
    "ch03-01-variables-and-mutability.md": "programming_concepts/variables_and_mutability.md",
    "ch03-02-data-types.md": "programming_concepts/data_types.md",
    "ch03-03-how-functions-work.md": "programming_concepts/functions.md",
    "ch03-04-comments.md": "programming_concepts/comments.md",
    "ch03-05-control-flow.md": "programming_concepts/control_flow.md",
    "ch04-01-what-is-ownership.md": "ownership/about_ownership.md",
    "ch04-02-references-and-borrowing.md": "ownership/references_and_borrowing.md",
    "ch04-03-slices.md": "ownership/the_slice_type.md",
    "ch05-01-defining-structs.md": "structs/defining_and_instantiating.md",
    "ch05-02-example-structs.md": "structs/example_program.md",
    "ch05-03-method-syntax.md": "structs/method_syntax.md",
    "ch06-01-defining-an-enum.md": "enums_and_pattern_matching/defining_an_enum.md",
    "ch06-02-match.md": "enums_and_pattern_matching/match_control_flow.md",
    "ch06-03-if-let.md": "enums_and_pattern_matching/if-let_control_flow.md",
    "ch07-01-packages-and-crates.md": "packages_crates_and_modules/packages_and_crates.md",
    "ch07-02-defining-modules-to-control-scope-and-privacy.md": "packages_crates_and_modules/defining_modules.md",
    "ch07-03-paths-for-referring-to-an-item-in-the-module-tree.md": "packages_crates_and_modules/paths.md",
    "ch07-04-bringing-paths-into-scope-with-the-use-keyword.md": "packages_crates_and_modules/the_use_keyword.md",
    "ch07-05-separating-modules-into-different-files.md": "packages_crates_and_modules/separating_modules.md",
    "ch08-01-vectors.md": "common_collections/vectors.md",
    "ch08-02-strings.md": "common_collections/strings.md",
    "ch08-03-hash-maps.md": "common_collections/hash_maps.md",
    "ch09-01-unrecoverable-errors-with-panic.md": "error_handling/panic.md",
    "ch09-02-recoverable-errors-with-result.md": "error_handling/result.md",
    "ch09-03-to-panic-or-not-to-panic.md": "error_handling/panic_or_not.md",
    "ch10-01-syntax.md": "generic_types_traits_and_lifetimes/generics.md",
    "ch10-02-traits.md": "generic_types_traits_and_lifetimes/traits.md",
    "ch10-03-lifetime-syntax.md": "generic_types_traits_and_lifetimes/lifetimes.md",
    "ch11-01-writing-tests.md": "automated_tests/howto.md",
    "ch11-02-running-tests.md": "automated_tests/how_tests_are_run.md",
    "ch11-03-test-organization.md": "automated_tests/test_organization.md",
    "ch12-01-accepting-command-line-arguments.md": "io_project/accepting_cli_arguments.md",
    "ch12-02-reading-a-file.md": "io_project/reading_a_file.md",
    "ch12-03-improving-error-handling-and-modularity.md": "io_project/refactoring.md",
    "ch12-04-testing-the-librarys-functionality.md": "io_project/test_driven_dev.md",
    "ch12-05-working-with-environment-variables.md": "io_project/env_variables.md",
    "ch12-06-writing-to-stderr-instead-of-stdout.md": "io_project/std_err.md",
    "ch13-01-closures.md": "functional_features/closures.md",
    "ch13-02-iterators.md": "functional_features/iterators.md",
    "ch13-03-improving-our-io-project.md": "functional_features/improving_io_project.md",
    "ch13-04-performance.md": "functional_features/performance.md",
    "ch14-01-release-profiles.md": "crates-io/release_profiles.md",
    "ch14-02-publishing-to-crates-io.md": "crates-io/publishing.md",
    "ch14-03-cargo-workspaces.md": "crates-io/workspace.md",
    "ch14-04-installing-binaries.md": "crates-io/cargo_install.md",
    "ch14-05-extending-cargo.md": "crates-io/custom_commands.md",
    "ch15-01-box.md": "smart_pointers/box-t.md",
    "ch15-02-deref.md": "smart_pointers/deref-t.md",
    "ch15-03-drop.md": "smart_pointers/drop-t.md",
    "ch15-04-rc.md": "smart_pointers/rc-t.md",
    "ch15-05-interior-mutability.md": "smart_pointers/refcell-t.md",
    "ch15-06-reference-cycles.md": "smart_pointers/ref-cycles.md",
    "ch16-01-threads.md": "concurrency/threads.md",
    "ch16-02-message-passing.md": "concurrency/message_passing.md",
    "ch16-03-shared-state.md": "concurrency/shared-state.md",
    "ch16-04-extensible-concurrency-sync-and-send.md": "concurrency/extensible_concurrency.md",
    "ch17-01-futures-and-syntax.md": "async/futures.md",
    "ch17-02-concurrency-with-async.md": "async/concurrency_n_async.md",
    "ch17-03-more-futures.md": "async/multiple_futures.md",
    "ch17-04-streams.md": "async/streams.md",
    "ch17-05-traits-for-async.md": "async/async_traits.md",
    "ch17-06-futures-tasks-threads.md": "async/all_together.md",
    "ch18-01-what-is-oo.md": "oop/characteristics_oop.md",
    "ch18-02-trait-objects.md": "oop/trait_objects.md",
    "ch18-03-oo-design-patterns.md": "oop/implementing.md",
    "ch19-01-all-the-places-for-patterns.md": "patterns/all_places.md",
    "ch19-02-refutability.md": "patterns/refutability.md",
    "ch19-03-pattern-syntax.md": "patterns/syntax.md",
    "ch20-01-unsafe-rust.md": "advanced_features/unsafe.md",
    "ch20-02-advanced-traits.md": "advanced_features/adv_traits.md",
    "ch20-03-advanced-types.md": "advanced_features/adv_types.md",
    "ch20-04-advanced-functions-and-closures.md": "advanced_features/adv_fns_and_closures.md",
    "ch20-05-macros.md": "advanced_features/macros.md",
    "ch21-01-single-threaded.md": "final_project/single-threaded.md",
    "ch21-02-multithreaded.md": "final_project/multithreaded.md",
    "ch21-03-graceful-shutdown-and-cleanup.md": "final_project/graceful_shutdown.md",
    "appendix-01-keywords.md": "appendix/keywords.md",
    "appendix-02-operators.md": "appendix/ops_and_symbols.md",
    "appendix-03-derivable-traits.md": "appendix/derivable_traits.md",
    "appendix-04-useful-development-tools.md": "appendix/dev_tools.md",
    "appendix-05-editions.md": "appendix/editions.md",
    "appendix-06-translation.md": "appendix/translations.md",
    "appendix-07-nightly-rust.md": "appendix/releases.md",
}


@dataclass(frozen=True)
class Unit:
    kind: str
    text: str


def _is_fence_start(line: str) -> bool:
    return bool(re.match(r"^(?:> ?)*```", line))


def units(text: str) -> list[Unit]:
    """Split Markdown while keeping fences and structural markers opaque."""

    lines = text.splitlines(keepends=True)
    result: list[Unit] = []
    prose: list[str] = []

    def flush() -> None:
        if prose:
            value = "".join(prose)
            if value.strip():
                result.append(Unit("prose", value))
            prose.clear()

    index = 0
    while index < len(lines):
        line = lines[index]
        if _is_fence_start(line):
            flush()
            block = [line]
            index += 1
            while index < len(lines):
                block.append(lines[index])
                if _is_fence_start(lines[index]) and len(block) > 1:
                    index += 1
                    break
                index += 1
            result.append(Unit("fence", "".join(block)))
            continue
        if not line.strip():
            flush()
            index += 1
            continue
        stripped = line.rstrip("\r\n")
        if (
            HEADING_RE.match(stripped)
            or LISTING_RE.match(stripped)
            or FILENAME_RE.match(stripped)
            or ANCHOR_RE.match(stripped)
            or COMMENT_RE.match(stripped)
        ):
            flush()
            marker = [line]
            if COMMENT_RE.match(stripped) and "-->" not in line:
                index += 1
                while index < len(lines):
                    marker.append(lines[index])
                    if "-->" in lines[index]:
                        index += 1
                        break
                    index += 1
            else:
                index += 1
            result.append(Unit("structural", "".join(marker)))
            continue
        prose.append(line)
        index += 1
    flush()
    return result


def prose_units(text: str) -> list[str]:
    result = []
    for unit in units(text):
        if unit.kind != "prose":
            continue
        value = unit.text.strip()
        if not value or not HAN_RE.search(value):
            continue
        # Old translation notes and listing captions have no current prose
        # counterpart.  Excluding them makes the positional fallback safer.
        if value.startswith("> **译注**") or re.match(r"^(?:\*\*)?(?:清单|Listing)\s+\d", value):
            continue
        result.append(unit.text)
    return result


def marker_tokens(text: str) -> list[str]:
    values = [match.group(0) for match in INLINE_RE.finditer(text)]
    values.extend(match.group(1) or match.group(2) for match in LINK_TARGET_RE.finditer(text))
    values.extend(match.group(1) or match.group(2) for match in REFERENCE_TARGET_RE.finditer(text))
    values.extend(value.rstrip(".,;:!?，。；：！？") for value in URL_RE.findall(text))
    values.extend(re.findall(r"\b\d+(?:[-–]\d+)?\b", text))
    return values


def score(current: str, reference: str) -> int:
    left = marker_tokens(current)
    right = marker_tokens(reference)
    if not left or not right:
        return 0
    score_value = 0
    remaining = list(right)
    for token in left:
        if token in remaining:
            score_value += 10 if token.startswith("`") else 6
            remaining.remove(token)
    return score_value


def strong_marker_match(current: str, reference: str) -> bool:
    current_codes = [match.group(0) for match in INLINE_RE.finditer(current)]
    reference_codes = [match.group(0) for match in INLINE_RE.finditer(reference)]
    shared = sum(block.size for block in difflib.SequenceMatcher(None, current_codes, reference_codes).get_matching_blocks())
    if shared >= 2:
        return True
    if shared == 1:
        token = next((value for value in current_codes if value in reference_codes), "")
        return len(token) >= 8 and (any(character in token for character in ("_", "::", "<", "/")) or token.strip("`").lower() not in {"threadpool", "worker", "thread", "sender"})
    current_numbers = set(re.findall(r"\b\d+(?:[-–]\d+)?\b", current))
    reference_numbers = set(re.findall(r"\b\d+(?:[-–]\d+)?\b", reference))
    return not current_codes and not reference_codes and bool(current_numbers & reference_numbers) and ("Listing" in current or "清单" in reference)


def reference_path(name: str, root: Path) -> Path | None:
    relative = MONOLITHIC.get(name) or SUBFILES.get(name)
    return root / relative if relative else None


def replace_tokens(reference: str, current: str) -> str | None:
    """Retain current protected markers when the paragraph shape agrees."""

    reference_codes = [match.group(0) for match in INLINE_RE.finditer(reference)]
    current_codes = [match.group(0) for match in INLINE_RE.finditer(current)]
    if len(current_codes) > len(reference_codes):
        return None
    output = reference

    # Align exact code tokens first.  Extra reference formatting is removed;
    # unmatched current tokens are paired with the remaining reference tokens
    # in order.  This avoids turning an italicized word such as *functions* into
    # an unrelated code token such as `another_function`.
    matcher = difflib.SequenceMatcher(None, reference_codes, current_codes)
    code_pairs: dict[int, int] = {}
    used_reference: set[int] = set()
    used_current: set[int] = set()
    for block in matcher.get_matching_blocks():
        for offset in range(block.size):
            reference_index = block.a + offset
            current_index = block.b + offset
            code_pairs[reference_index] = current_index
            used_reference.add(reference_index)
            used_current.add(current_index)
    remaining_reference = [index for index in range(len(reference_codes)) if index not in used_reference]
    remaining_current = [index for index in range(len(current_codes)) if index not in used_current]
    if len(remaining_current) > len(remaining_reference):
        return None
    for reference_index, current_index in zip(remaining_reference, remaining_current):
        code_pairs[reference_index] = current_index

    code_position = 0

    def replace_code(match: re.Match[str]) -> str:
        nonlocal code_position
        replacement = code_pairs.get(code_position)
        code_position += 1
        if replacement is None:
            return match.group(2)
        return current_codes[replacement]

    output = INLINE_RE.sub(replace_code, output)

    current_targets = [match.group(1) or match.group(2) for match in LINK_TARGET_RE.finditer(current)]
    reference_targets = [match.group(1) or match.group(2) for match in LINK_TARGET_RE.finditer(output)]
    if len(current_targets) > len(reference_targets):
        return None
    target_pairs: dict[int, str] = {}
    target_matcher = difflib.SequenceMatcher(None, reference_targets, current_targets)
    used_reference = set()
    used_current = set()
    for block in target_matcher.get_matching_blocks():
        for offset in range(block.size):
            reference_index = block.a + offset
            current_index = block.b + offset
            target_pairs[reference_index] = current_targets[current_index]
            used_reference.add(reference_index)
            used_current.add(current_index)
    remaining_reference = [index for index in range(len(reference_targets)) if index not in used_reference]
    remaining_current = [index for index in range(len(current_targets)) if index not in used_current]
    for reference_index, current_index in zip(remaining_reference, remaining_current):
        target_pairs[reference_index] = current_targets[current_index]

    position = 0

    def replace_link(match: re.Match[str]) -> str:
        nonlocal position
        target = target_pairs.get(position)
        position += 1
        if target is None:
            return "]"
        prefix = match.group(0)[: match.group(0).find(match.group(1) or match.group(2))]
        return prefix + target

    output = LINK_TARGET_RE.sub(replace_link, output)
    output = output.replace("])" , "]")

    current_urls = [value.rstrip(".,;:!?，。；：！？") for value in URL_RE.findall(current)]
    reference_urls = [value.rstrip(".,;:!?，。；：！？") for value in URL_RE.findall(output)]
    if len(current_urls) > len(reference_urls):
        return None
    if not current_urls:
        output = URL_RE.sub("", output)
    return output


def heading_titles(text: str) -> list[str]:
    return [
        line.rstrip("\r\n").lstrip("#").strip()
        for unit in units(text)
        if unit.kind == "structural"
        for line in unit.text.splitlines()
        if HEADING_RE.match(line)
    ]


def caption_map(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    pattern = re.compile(r"(?:清单|Listing)\s+(\d+(?:-\d+)?)\s*(?:\*\*)?\s*[：:]\s*(.+?)\s*$")
    for line in text.splitlines():
        match = pattern.search(line)
        if match and HAN_RE.search(match.group(2)):
            result[match.group(1)] = match.group(2).strip("* ")
    return result


def translate_structural(unit: str, reference_title: str | None, captions: dict[str, str]) -> str:
    lines = unit.splitlines(keepends=True)
    if not lines:
        return unit
    first = lines[0]
    if HEADING_RE.match(first) and reference_title and HAN_RE.search(reference_title):
        prefix = first[: len(first) - len(first.lstrip("#"))]
        title = replace_tokens(reference_title.strip(), first.rstrip("\r\n").lstrip("#").strip())
        if title:
            lines[0] = prefix + " " + title + ("\n" if first.endswith("\n") else "")
    if LISTING_RE.match(first):
        number_match = re.search(r"\bnumber=\"(\d+(?:-\d+)?)\"", first)
        caption_match = re.search(r"\bcaption=\"([^\"]*)\"", first)
        if number_match and caption_match and number_match.group(1) in captions:
            current_caption = caption_match.group(1)
            translated_caption = replace_tokens(captions[number_match.group(1)], current_caption)
            if translated_caption and HAN_RE.search(translated_caption):
                lines[0] = first[: caption_match.start(1)] + translated_caption + first[caption_match.end(1) :]
    if FILENAME_RE.match(first):
        lines[0] = first.replace("Filename:", "文件名：", 1)
    return "".join(lines)


def _masked_scan(text: str) -> str:
    """Mask fences and comments while preserving offsets for regex scans."""

    chars = list(text)
    spans = [match.span() for match in FENCE_RE.finditer(text)]
    remaining = FENCE_RE.sub(
        lambda match: "".join("\n" if character == "\n" else " " for character in match.group(0)),
        text,
    )
    spans.extend(match.span() for match in COMMENT_BLOCK_RE.finditer(remaining))
    for start, end in spans:
        for index in range(start, end):
            if chars[index] != "\n":
                chars[index] = " "
    return "".join(chars)


def _replace_matches(text: str, matches: list[re.Match[str]], values: list[str], group: int = 0) -> str:
    if not matches or len(matches) != len(values):
        return text
    chunks: list[str] = []
    cursor = 0
    for match, value in zip(matches, values):
        start, end = match.span(group)
        chunks.append(text[cursor:start])
        chunks.append(value)
        cursor = end
    chunks.append(text[cursor:])
    return "".join(chunks)


def restore_global_protected(translated: str, current: str) -> str:
    """Restore current protected sequences after prose import.

    Paragraph alignment is intentionally conservative, but an old paragraph can
    contain the same number of technical markers in a different order. A final
    file-level pass restores the current source's exact inline-code and link
    target sequences without touching fenced code or visible prose.
    """

    current_scan = _masked_scan(current)
    translated_scan = _masked_scan(translated)

    current_codes = list(INLINE_RE.finditer(current_scan))
    translated_codes = list(INLINE_RE.finditer(translated_scan))
    source_code_values = [current_scan[match.start() : match.end()] for match in current_codes]
    translated_code_values = [translated_scan[match.start() : match.end()] for match in translated_codes]
    if len(translated_codes) > len(current_codes):
        matcher = difflib.SequenceMatcher(None, source_code_values, translated_code_values)
        matched_translated: set[int] = set()
        for block in matcher.get_matching_blocks():
            matched_translated.update(range(block.b, block.b + block.size))
        extras = [match for index, match in enumerate(translated_codes) if index not in matched_translated]
        translated = _replace_matches(translated, extras, [""] * len(extras))
        translated_scan = _masked_scan(translated)
        translated_codes = list(INLINE_RE.finditer(translated_scan))
        translated_code_values = [translated_scan[match.start() : match.end()] for match in translated_codes]
    if len(current_codes) == len(translated_codes):
        translated = _replace_matches(
            translated,
            translated_codes,
            source_code_values,
        )
    elif len(current_codes) > len(translated_codes):
        missing = source_code_values[len(translated_codes) :]
        translated = translated.rstrip() + "\n\n" + " ".join(missing) + "\n"

    current_scan = _masked_scan(current)
    translated_scan = _masked_scan(translated)
    current_anchors = list(ANCHOR_BLOCK_RE.finditer(current_scan))
    translated_anchors = list(ANCHOR_BLOCK_RE.finditer(translated_scan))
    anchor_values = [match.group(0) for match in current_anchors]
    if len(translated_anchors) > len(current_anchors):
        matcher = difflib.SequenceMatcher(
            None,
            anchor_values,
            [match.group(0) for match in translated_anchors],
        )
        keep = set()
        for block in matcher.get_matching_blocks():
            keep.update(range(block.b, block.b + block.size))
        extras = [match for index, match in enumerate(translated_anchors) if index not in keep]
        translated = _replace_matches(translated, extras, [""] * len(extras))
        translated_scan = _masked_scan(translated)
        translated_anchors = list(ANCHOR_BLOCK_RE.finditer(translated_scan))
    if len(current_anchors) == len(translated_anchors):
        translated = _replace_matches(translated, translated_anchors, anchor_values)
    elif len(current_anchors) > len(translated_anchors):
        translated = translated.rstrip() + "\n\n" + "\n".join(anchor_values[len(translated_anchors) :]) + "\n"

    current_scan = _masked_scan(current)
    translated_scan = _masked_scan(translated)
    current_filenames = list(FILENAME_BLOCK_RE.finditer(current_scan))
    translated_filenames = list(FILENAME_BLOCK_RE.finditer(translated_scan))
    if len(current_filenames) == len(translated_filenames):
        translated = _replace_matches(
            translated,
            translated_filenames,
            [match.group(0).replace("Filename:", "文件名：", 1) for match in current_filenames],
        )
    elif len(current_filenames) > len(translated_filenames):
        translated = translated.rstrip() + "\n\n" + "\n".join(
            match.group(0).replace("Filename:", "文件名：", 1) for match in current_filenames[len(translated_filenames) :]
        ) + "\n"

    def restore_targets(pattern: re.Pattern[str], group_for_match: callable, suffix: str) -> None:
        nonlocal translated
        source_scan = _masked_scan(current)
        target_scan = _masked_scan(translated)
        source_matches = list(pattern.finditer(source_scan))
        target_matches = list(pattern.finditer(target_scan))
        source_values = [group_for_match(match, source_scan) for match in source_matches]
        if pattern is REFERENCE_TARGET_RE:
            # Reference definitions carry labels as well as targets. Reusing
            # only the target value can pair a newly added footnote with the
            # wrong label, so use the current definitions as complete lines.
            translated = _replace_matches(translated, target_matches, [""] * len(target_matches))
            if source_matches:
                translated = translated.rstrip() + "\n\n" + "\n".join(match.group(0) for match in source_matches) + "\n"
            return
        if len(source_matches) == len(target_matches):
            values = [group_for_match(match, target_scan) for match in target_matches]
            for index, (source_value, target_value) in enumerate(zip(source_values, values)):
                if source_value != target_value:
                    pass
            if pattern is LINK_TARGET_RE:
                positions = [match.group(1) is not None and 1 or 2 for match in target_matches]
                chunks: list[str] = []
                cursor = 0
                for match, value, group in zip(target_matches, source_values, positions):
                    start, end = match.span(group)
                    chunks.append(translated[cursor:start])
                    chunks.append(value)
                    cursor = end
                chunks.append(translated[cursor:])
                translated = "".join(chunks)
            elif pattern is REFERENCE_TARGET_RE:
                chunks = []
                cursor = 0
                for match, value in zip(target_matches, source_values):
                    group = 1 if match.group(1) is not None else 2
                    start, end = match.span(group)
                    chunks.append(translated[cursor:start])
                    chunks.append(value)
                    cursor = end
                chunks.append(translated[cursor:])
                translated = "".join(chunks)
            return
        if len(source_matches) > len(target_matches):
            missing = source_values[len(target_matches) :]
            if pattern is LINK_TARGET_RE:
                translated = translated.rstrip() + "\n\n" + "\n".join(f"[参考链接]({value})" for value in missing) + "\n"
            else:
                translated = translated.rstrip() + "\n\n" + "\n".join(f"[参考链接]: {value}" for value in missing) + "\n"
        elif len(target_matches) > len(source_matches):
            extras = target_matches[len(source_matches) :]
            chunks = []
            cursor = 0
            for match in extras:
                start, end = match.span(0)
                chunks.append(translated[cursor:start])
                chunks.append("]" if pattern is LINK_TARGET_RE else "")
                cursor = end
            chunks.append(translated[cursor:])
            translated = "".join(chunks)

    restore_targets(LINK_TARGET_RE, lambda match, text: match.group(1) or match.group(2), "direct")
    restore_targets(REFERENCE_TARGET_RE, lambda match, text: match.group(1) or match.group(2), "reference")

    # Comments are invisible and can be safely moved to the end when the old
    # reference omitted newer maintenance comments. Their exact bytes still
    # matter to CI and to the mdBook preprocessor.
    current_scan = FENCE_RE.sub(
        lambda match: "".join("\n" if character == "\n" else " " for character in match.group(0)),
        current,
    )
    current_comments = COMMENT_BLOCK_RE.findall(current_scan)
    if current_comments:
        translated_scan = FENCE_RE.sub(
            lambda match: "".join("\n" if character == "\n" else " " for character in match.group(0)),
            translated,
        )
        translated_comments = COMMENT_BLOCK_RE.findall(translated_scan)
        if translated_comments != current_comments:
            translated_matches = list(COMMENT_BLOCK_RE.finditer(translated_scan))
            translated = _replace_matches(translated, translated_matches, [""] * len(translated_matches))
            translated = translated.rstrip() + "\n\n" + "\n\n".join(current_comments) + "\n"
    return translated


def mapping(current: list[str], reference: list[str]) -> dict[int, int]:
    """Create monotonic anchors from technical markers, then interpolate gaps."""

    anchors: list[tuple[int, int]] = []
    previous = -1
    for current_index, current_unit in enumerate(current):
        candidates = []
        for reference_index in range(previous + 1, len(reference)):
            value = score(current_unit, reference[reference_index])
            if value and strong_marker_match(current_unit, reference[reference_index]):
                distance = abs(reference_index - round(current_index * len(reference) / max(len(current), 1)))
                current_codes = [match.group(0) for match in INLINE_RE.finditer(current_unit)]
                reference_codes = [match.group(0) for match in INLINE_RE.finditer(reference[reference_index])]
                shared = sum(block.size for block in difflib.SequenceMatcher(None, current_codes, reference_codes).get_matching_blocks())
                similarity = shared / max(len(current_codes), len(reference_codes), 1)
                candidates.append((similarity, shared, -distance, reference_index))
        if not candidates:
            continue
        best = max(candidates)
        anchors.append((current_index, best[3]))
        previous = best[3]

    result: dict[int, int] = {}
    boundaries = [(-1, -1), *anchors, (len(current), len(reference))]
    for (left_current, left_reference), (right_current, right_reference) in zip(boundaries, boundaries[1:]):
        current_gap = list(range(left_current + 1, right_current))
        reference_gap = list(range(left_reference + 1, right_reference))
        if not current_gap or not reference_gap:
            continue
        # Never reuse one old paragraph for several current paragraphs. The
        # latest edition often adds explanatory paragraphs; leaving those
        # English is safer than duplicating unrelated reference prose.
        for current_index, reference_index in zip(current_gap, reference_gap):
            result[current_index] = reference_index
    for current_index, reference_index in anchors:
        result[current_index] = reference_index
    return result


def translate_file(current: str, reference: str) -> tuple[str, int, int]:
    current_units = units(current)
    current_prose = [unit.text for unit in current_units if unit.kind == "prose"]
    reference_prose = prose_units(reference)
    pairs = mapping(current_prose, reference_prose)
    titles = heading_titles(reference)
    title_position = 0
    captions = caption_map(reference)
    translated = 0
    skipped = 0
    prose_index = 0
    output: list[str] = []
    for unit in current_units:
        if unit.kind != "prose":
            reference_title = None
            if unit.kind == "structural":
                if any(HEADING_RE.match(line) for line in unit.text.splitlines()):
                    if title_position < len(titles):
                        reference_title = titles[title_position]
                    title_position += 1
                output.append(translate_structural(unit.text, reference_title, captions))
            else:
                output.append(unit.text)
            if not output[-1].endswith("\n\n"):
                output.append("\n")
            continue
        reference_index = pairs.get(prose_index)
        replacement = None
        if reference_index is not None:
            replacement = replace_tokens(reference_prose[reference_index].strip(), unit.text.strip())
            if replacement and HAN_RE.search(replacement):
                translated += 1
                output.append(replacement + "\n\n")
            else:
                skipped += 1
                output.append(unit.text)
        else:
            skipped += 1
            output.append(unit.text)
        prose_index += 1
    result = "".join(output).rstrip() + "\n"
    return restore_global_protected(result, current), translated, skipped


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--reference-root", type=Path, default=REFERENCE_ROOT)
    parser.add_argument("--file", action="append", dest="files")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    reference_root = args.reference_root.resolve()
    names = args.files or sorted(path.name for path in (root / "src").glob("*.md"))
    for name in names:
        current_path = root / "src" / name
        ref_path = reference_path(name, reference_root)
        if not current_path.exists() or ref_path is None or not ref_path.exists():
            print(f"skip {name}: no mapped reference")
            continue
        current = current_path.read_text(encoding="utf-8")
        reference = ref_path.read_text(encoding="utf-8")
        translated_text, translated, skipped = translate_file(current, reference)
        if not args.dry_run:
            current_path.write_text(translated_text, encoding="utf-8")
        print(f"{name}: translated={translated} skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

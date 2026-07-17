"""Adapt the community translation to the current official Book layout.

This is a one-time bulk editing aid, not a second mdBook build system. It uses
the current English files as the structure and code source, and imports only
natural-language sections from the gnu4cn reference repository. The generated
files are checked by ``ci/check_translation.py`` before they are kept.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ROOT = Path(r"C:\Users\cmx27\AppData\Local\Temp\rust-lang-zh_CN\src")


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

HEADING_OVERRIDES = {
    "ch01-01-installation.md": [0, 1, 3, 5, 6, 7, 8, 9],
    "ch01-03-hello-cargo.md": [0, 1, 2, 3, 4, 5],
    "ch03-05-control-flow.md": list(range(11)),
    "ch17-01-futures-and-syntax.md": [0, 1, 2, 3, 4],
    "ch17-03-more-futures.md": [1, 2],
    "appendix-04-useful-development-tools.md": [0, 1, 2, 3, 4],
}

COMMON_HEADING_FALLBACKS = {
    "The Anatomy of a Rust Program": "Rust 程序剖析",
    "Compilation and Execution": "编译和执行",
    "Summary": "本章小结",
    "Programming a Guessing Game": "编写猜数游戏",
    "Common Programming Concepts": "常见编程概念",
    "Understanding Ownership": "理解所有权",
    "Using Structs to Structure Related Data": "使用结构体组织相关数据",
    "Enums and Pattern Matching": "枚举与模式匹配",
    "Packages, Crates, and Modules": "包、crate 与模块",
    "Common Collections": "常见集合",
    "Error Handling": "错误处理",
    "Generic Types, Traits, and Lifetimes": "泛型、trait 与生命周期",
    "Writing Automated Tests": "编写自动化测试",
    "Smart Pointers": "智能指针",
    "Fearless Concurrency": "无畏并发",
    "Object Oriented Programming Features": "面向对象编程特性",
    "Patterns and Matching": "模式与匹配",
    "Advanced Features": "高级特性",
    "Final Project: Building a Multithreaded Web Server": "最终项目：构建多线程 Web 服务器",
}


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^```")
INLINE_RE = re.compile(r"`[^`\n]+`")
LINK_RE = re.compile(r"\]\(\s*(?:<([^>]+)>|([^\s)]+))")
REFERENCE_LINK_RE = re.compile(r"(?m)^\[[^\]\n]+\]:\s*(?:<([^>]+)>|(\S+))")
URL_RE = re.compile(r"(?<![\w])(?:https?://|mailto:)[^\s<>)\]\\\"`']+")
ANCHOR_RE = re.compile(r"(?s)<a\s+(?:id|name)\s*=\s*\"[^\"]+\"\s*>\s*</a>")
FILENAME_RE = re.compile(r'<span class="filename">.*?</span>')


def reference_path(name: str) -> Path | None:
    relative = MONOLITHIC.get(name) or SUBFILES.get(name)
    return REFERENCE_ROOT / relative if relative else None


def sectionize(text: str) -> tuple[str, list[tuple[str, str, str]]]:
    lines = text.splitlines(keepends=True)
    headings: list[tuple[int, str, str]] = []
    in_fence = False
    for index, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line.rstrip("\r\n"))
        if match:
            headings.append((index, match.group(1), match.group(2)))
    if not headings:
        return text, []
    prefix = "".join(lines[: headings[0][0]])
    sections = []
    for position, (start, level, title) in enumerate(headings):
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        body = "".join(lines[start + 1 : end])
        sections.append((level, title, body))
    return prefix, sections


def split_code_units(text: str) -> tuple[list[str], list[str]]:
    lines = text.splitlines(keepends=True)
    segments: list[str] = []
    units: list[str] = []
    current: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("<Listing"):
            segments.append("".join(current))
            current = []
            unit = [line]
            index += 1
            while index < len(lines):
                unit.append(lines[index])
                if lines[index].strip() == "</Listing>":
                    index += 1
                    break
                index += 1
            units.append("".join(unit))
            continue
        if FENCE_RE.match(line):
            segments.append("".join(current))
            current = []
            unit = [line]
            index += 1
            while index < len(lines):
                unit.append(lines[index])
                if FENCE_RE.match(lines[index]) and len(unit) > 1:
                    index += 1
                    break
                index += 1
            units.append("".join(unit))
            continue
        current.append(line)
        index += 1
    segments.append("".join(current))
    return segments, units


def clean_reference_text(text: str) -> str:
    text = re.sub(r'(?s)<!--.*?-->', "", text)
    text = re.sub(r'(?s)<a\s+(?:id|name)\s*=\s*"[^"]+"\s*>\s*</a>', "", text)
    text = re.sub(r'(?s)<span\s+class="filename">.*?</span>', "", text)
    text = text.replace("**Anatomy of a Rust Program**", "**Rust 程序剖析**")
    lines = []
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if re.match(r"^(?:文件名|Filename)[:：]", stripped):
            continue
        if re.match(r"^\*\*清单\s+\d+", stripped):
            continue
        if stripped in {"（End）", "(End)"}:
            continue
        lines.append(line)
    return "".join(lines)


def link_targets(text: str) -> list[str]:
    result = [m.group(1) or m.group(2) for m in LINK_RE.finditer(text)]
    result.extend(m.group(1) or m.group(2) for m in REFERENCE_LINK_RE.finditer(text))
    return result


def replace_inline_tokens(reference: str, current: str) -> str:
    current_tokens = INLINE_RE.findall(current)
    position = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal position
        if position >= len(current_tokens):
            return match.group(0)
        value = current_tokens[position]
        position += 1
        return value

    return INLINE_RE.sub(replace, reference)


def replace_link_targets(reference: str, current: str) -> str:
    current_targets = link_targets(current)
    position = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal position
        prefix = match.group(0)[: match.group(0).find(match.group(1) or match.group(2))]
        if position >= len(current_targets):
            return match.group(0)
        target = current_targets[position]
        position += 1
        return prefix + target

    reference = LINK_RE.sub(replace, reference)

    def replace_definition(match: re.Match[str]) -> str:
        nonlocal position
        if position >= len(current_targets):
            return match.group(0)
        prefix = match.group(0)[: match.group(0).find(match.group(1) or match.group(2))]
        target = current_targets[position]
        position += 1
        return prefix + target

    return REFERENCE_LINK_RE.sub(replace_definition, reference)


def replace_urls(reference: str, current: str) -> str:
    current_urls = [value.rstrip(".,;:!?，。；：！？") for value in URL_RE.findall(current)]
    position = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal position
        if position >= len(current_urls):
            return match.group(0)
        value = current_urls[position]
        position += 1
        return value

    return URL_RE.sub(replace, reference)


def preserve_current_markers(reference: str, current: str) -> str:
    markers: list[str] = []
    markers.extend(ANCHOR_RE.findall(current))
    markers.extend(FILENAME_RE.findall(current))
    markers.extend(re.findall(r"(?s)<!--.*?-->", current))
    for marker in markers:
        if marker and marker not in reference:
            reference = marker + "\n" + reference
    return reference


def translate_block(reference: str, current: str) -> str:
    reference = clean_reference_text(reference)
    if not reference.strip():
        return current
    return preserve_current_markers(reference, current)


def unit_number(unit: str) -> str | None:
    match = re.search(r'<Listing\s+[^>]*\bnumber="([^"]+)"', unit)
    return match.group(1) if match else None


def reference_unit_number(segment: str) -> str | None:
    match = re.search(r"(?:清单|Listing)\s+(\d+(?:-\d+)?)", segment[-1200:])
    return match.group(1) if match else None


def aligned_reference_segments(current: str, reference: str) -> list[str]:
    current_segments, current_units = split_code_units(current)
    reference_segments, reference_units = split_code_units(reference)
    if not reference_segments:
        return [current]

    # When both layouts have the same number of prose segments, pair them by
    # position. The old reference repository does not use the current
    # `<Listing>` wrappers, so trying to align units by listing numbers in this
    # case can concatenate unrelated reference segments and duplicate prose.
    if len(current_segments) == len(reference_segments):
        return reference_segments

    nonempty_reference_segments = [segment for segment in reference_segments if segment.strip()]

    # The reference checkout predates the current edition and therefore has a
    # different number of console/listing blocks in several chapters. Once
    # those blocks are removed, the remaining prose still follows the same
    # order. Pair prose segments by position so an extra upstream example does
    # not leave the following English prose untranslated.
    if len(current_segments) != len(reference_segments) or len(nonempty_reference_segments) != len(reference_segments):
        reference_segments = nonempty_reference_segments
        if not reference_segments:
            return [current]
        return [
            reference_segments[
                min(
                    round(index * (len(reference_segments) - 1) / max(len(current_segments) - 1, 1)),
                    len(reference_segments) - 1,
                )
            ]
            for index in range(len(current_segments))
        ]

    current_to_reference: dict[int, int] = {}
    numbered_reference = {
        number: index
        for index, number in enumerate(
            reference_unit_number(reference_segments[index]) for index in range(len(reference_units))
        )
        if number is not None
    }
    for index, unit in enumerate(current_units):
        number = unit_number(unit)
        if number in numbered_reference:
            current_to_reference[index] = numbered_reference[number]

    unused = [index for index in range(len(reference_units)) if index not in current_to_reference.values()]
    for index in range(len(current_units)):
        if index in current_to_reference:
            continue
        previous = max((value for key, value in current_to_reference.items() if key < index), default=-1)
        following = min((value for key, value in current_to_reference.items() if key > index), default=len(reference_units))
        candidates = [value for value in unused if previous < value < following]
        chosen = candidates[0] if candidates else (unused[0] if unused else None)
        if chosen is not None:
            current_to_reference[index] = chosen
            unused.remove(chosen)

    result: list[str] = []
    previous_reference_unit = -1
    for index in range(len(current_segments)):
        if index < len(current_units) and index in current_to_reference:
            boundary = current_to_reference[index]
            result.append("".join(reference_segments[previous_reference_unit + 1 : boundary + 1]))
            previous_reference_unit = boundary
        else:
            result.append("".join(reference_segments[previous_reference_unit + 1 :]))
            previous_reference_unit = len(reference_units) - 1
    if len(result) < len(current_segments):
        result.extend([""] * (len(current_segments) - len(result)))
    return result[: len(current_segments)]


def translate_body(current: str, reference: str) -> str:
    current_segments, current_units = split_code_units(current)
    reference_segments = aligned_reference_segments(current, reference)
    if not reference_segments:
        return current
    output: list[str] = []
    for index, current_segment in enumerate(current_segments):
        reference_segment = reference_segments[index] if index < len(reference_segments) else ""
        output.append(translate_block(reference_segment, current_segment))
        if index < len(current_units):
            output.append(current_units[index])
    return "".join(output)


def translated_heading(current_title: str, reference_title: str) -> str:
    reference_title = reference_title.strip()
    if not re.search(r"[\u3400-\u9fff]", reference_title):
        reference_title = COMMON_HEADING_FALLBACKS.get(current_title, current_title)
    return replace_inline_tokens(reference_title, current_title)


def heading_pairs(name: str, current: list[tuple[str, str, str]], reference: list[tuple[str, str, str]]) -> list[int]:
    override = HEADING_OVERRIDES.get(name)
    if override:
        return override[: len(current)]
    if len(current) == len(reference):
        return list(range(len(current)))
    if not reference:
        return [-1] * len(current)
    return [min(round(index * (len(reference) - 1) / max(len(current) - 1, 1)), len(reference) - 1) for index in range(len(current))]


def adapt_file(name: str, current: str, reference: str) -> str:
    if name == "title-page.md":
        return '''# 《Rust 程序设计语言》

_作者：Steve Klabnik、Carol Nichols 和 Chris Krycho，感谢 Rust 社区的贡献_

本书假定你使用 Rust 1.97.0（发布于 2026-07-09）或更高版本，并在所有项目的 *Cargo.toml* 文件中使用 `edition = "2024"`，以启用 Rust 2024 Edition 的惯用写法。请参阅[第 1 章的“安装”部分][install]<!-- ignore -->了解安装或更新 Rust 的方法，并参阅[附录 E][appendix-e]<!-- ignore -->了解 Edition。

HTML 版本可在线阅读：<https://doc.rust-lang.org/stable/book/>；通过 `rustup` 安装 Rust 后，也可以离线阅读，运行 `rustup doc --book` 即可打开。

本书还提供了若干社区[译本][translations]。

本书的[纸质书和电子书][nsprust]由 No Starch Press 出版。

[install]: ch01-01-installation.html
[appendix-e]: appendix-05-editions.html
[nsprust]: https://nostarch.com/rust-programming-language-3rd-edition
[translations]: appendix-06-translation.html

> **想要更具互动性的学习体验？可以试试另一版本的 Rust Book，它提供测验、高亮、可视化等功能：** <https://rust-book.cs.brown.edu>
'''

    if name == "foreword.md":
        start = reference.find("Rust 编程语言在短短几年间")
        if start < 0:
            start = 0
        end = reference.find("# 简介", start)
        selected = reference[start : end if end >= 0 else None].strip()
        return "# 前言\n\n" + selected + "\n"

    if name == "ch00-00-introduction.md":
        start = reference.find("# 简介")
        reference = reference[start:] if start >= 0 else reference

    current_prefix, current_sections = sectionize(current)
    reference_prefix, reference_sections = sectionize(reference)
    pairs = heading_pairs(name, current_sections, reference_sections)
    output = [translate_block(reference_prefix, current_prefix)]
    for index, (level, title, body) in enumerate(current_sections):
        reference_section = reference_sections[pairs[index]] if index < len(pairs) and pairs[index] >= 0 else ("", "", "")
        reference_title, reference_body = reference_section[1], reference_section[2]
        output.append(level + " " + translated_heading(title, reference_title) + "\n\n")
        output.append(translate_body(body, reference_body))
    return "".join(output).replace("\n\n\n\n", "\n\n")


def summary_translation(current: str, reference: str) -> str:
    reference_links = {}
    for match in re.finditer(r"\[([^\]\n]+)\]\(([^)\n]+)\)", reference):
        reference_links[match.group(2)] = match.group(1)

    def replace_line(match: re.Match[str]) -> str:
        label, target = match.group(1), match.group(2)
        ref_target = MONOLITHIC.get(target) or SUBFILES.get(target)
        ref_label = reference_links.get(ref_target)
        if ref_label:
            return match.group(0).replace(label, ref_label, 1)
        manual = {
            "The Rust Programming Language": "《Rust 程序设计语言》",
            "Foreword": "前言",
            "Introduction": "简介",
            "Getting Started": "入门",
            "Installation": "安装",
            "Hello, World!": "Hello, World!",
            "Hello, Cargo!": "Hello, Cargo!",
        }
        return match.group(0).replace(label, manual.get(label, COMMON_HEADING_FALLBACKS.get(label, label)), 1)

    lines = []
    for line in current.splitlines(keepends=True):
        lines.append(re.sub(r"\[([^\]\n]+)\]\(([^)\n]+)\)", replace_line, line))
    result = "".join(lines)
    result = result.replace("# Rust 程序设计语言", "# 《Rust 程序设计语言》", 1)
    result = result.replace("# Summary", "# 目录", 1)
    return result


def adapt_all(root: Path, reference_root: Path) -> list[str]:
    global REFERENCE_ROOT
    REFERENCE_ROOT = reference_root
    changed = []
    for path in sorted((root / "src").glob("*.md")):
        name = path.name
        current = path.read_text(encoding="utf-8")
        if name == "SUMMARY.md":
            reference = (reference_root / "SUMMARY.md").read_text(encoding="utf-8")
            translated = summary_translation(current, reference)
        else:
            ref_path = reference_path(name)
            if name in {"title-page.md", "foreword.md", "ch00-00-introduction.md"}:
                ref_path = reference_root / "Ch00_Forword_and_Introduction.md"
            if ref_path is None or not ref_path.exists():
                continue
            reference = ref_path.read_text(encoding="utf-8")
            translated = adapt_file(name, current, reference)
        if translated != current:
            path.write_text(translated.rstrip() + "\n", encoding="utf-8")
            changed.append(name)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--reference-root", type=Path, default=REFERENCE_ROOT)
    args = parser.parse_args()
    changed = adapt_all(args.root.resolve(), args.reference_root.resolve())
    print(f"adapted {len(changed)} files")
    print("\n".join(changed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

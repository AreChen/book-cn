import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "ci" / "check_translation.py"
SPEC = importlib.util.spec_from_file_location("check_translation", MODULE_PATH)
check_translation = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = check_translation
SPEC.loader.exec_module(check_translation)


class ProtectedContentTests(unittest.TestCase):
    def test_translation_may_change_prose_but_not_protected_content(self):
        source = '''# A heading

Use `cargo test` and see https://example.com/docs.

<a id="stable-anchor"></a>
<Listing number="1-1" file-name="src/main.rs" caption="A listing">
```rust,ignore
fn main() {}
```
</Listing>
'''
        translated = '''# 中文标题

使用 `cargo test`，详见 https://example.com/docs。

<a id="stable-anchor"></a>
<Listing number="1-1" file-name="src/main.rs" caption="中文说明">
```rust,ignore
fn main() {}
```
</Listing>
'''

        self.assertEqual(check_translation.compare_protected_tokens(source, translated), [])

    def test_changed_code_is_reported(self):
        source = "```rust\nfn main() {}\n```\n"
        translated = "```rust\nfn main() { println!(\"错误\"); }\n```\n"

        issues = check_translation.compare_protected_tokens(source, translated)

        self.assertTrue(any("code block" in issue for issue in issues))

    def test_changed_url_and_inline_code_are_reported(self):
        source = "See `cargo test` at https://example.com/docs.\n"
        translated = "参见 `cargo build`，网址为 https://example.com/other。\n"

        issues = check_translation.compare_protected_tokens(source, translated)

        self.assertTrue(any("inline code" in issue for issue in issues))
        self.assertTrue(any("URL" in issue for issue in issues))

    def test_allowlisted_translation_url_may_be_added(self):
        source = "See https://example.com/docs.\n"
        translated = (
            "参见 https://example.com/docs。\n"
            "本中文版本在线阅读：https://arechen.github.io/book-cn/\n"
        )

        self.assertEqual(
            check_translation.compare_protected_tokens(
                source,
                translated,
                allowed_translation_urls=check_translation.TRANSLATION_ONLY_URLS,
            ),
            [],
        )

    def test_fenced_code_is_not_counted_as_inline_code(self):
        source = "```text\nA `literal` in a code block\n```\nUse `cargo test`.\n"
        translated = "```text\nA `literal` in a code block\n```\n使用 `cargo test`。\n"

        self.assertEqual(
            check_translation.protected_tokens(source)["inline code"],
            ["`cargo test`"],
        )
        self.assertEqual(check_translation.compare_protected_tokens(source, translated), [])

    def test_blockquote_fenced_code_is_not_counted_as_inline_code(self):
        source = "> ```rust\n> let value = `literal`;\n> ```\nUse `cargo test`.\n"
        translated = "> ```rust\n> let value = `literal`;\n> ```\n使用 `cargo test`。\n"

        self.assertEqual(
            check_translation.protected_tokens(source)["inline code"],
            ["`cargo test`"],
        )
        self.assertEqual(check_translation.compare_protected_tokens(source, translated), [])

    def test_double_backtick_code_span_is_kept_as_one_token(self):
        source = "The error is `` cannot assign twice to immutable `x` ``.\n"
        translated = "错误是 `` cannot assign twice to immutable `x` ``。\n"

        self.assertEqual(
            check_translation.protected_tokens(source)["inline code"],
            ["`` cannot assign twice to immutable `x` ``"],
        )
        self.assertEqual(check_translation.compare_protected_tokens(source, translated), [])


class SummaryLinkTests(unittest.TestCase):
    def test_summary_links_must_resolve(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "src" / "chapter.md").write_text("# 中文\n", encoding="utf-8")
            summary = root / "src" / "SUMMARY.md"
            summary.write_text(
                "[存在](chapter.md)\n[缺失](missing.md#section)\n",
                encoding="utf-8",
            )

            issues = check_translation.validate_summary_links(root)

        self.assertEqual(len(issues), 1)
        self.assertIn("missing.md", issues[0])


if __name__ == "__main__":
    unittest.main()

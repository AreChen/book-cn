# 《Rust 程序设计语言》中文工作仓库

这是基于 [Rust 官方 Book 仓库](https://github.com/rust-lang/book) 的非官方中文翻译工作仓库。我们以官方 `main` 分支为内容上游，并参考社区已有译文来提高翻译效率和术语一致性。

本仓库当前处于增量翻译阶段：未完成翻译的章节仍保留官方英文原文，已翻译章节会在 [`TRANSLATION_STATUS.md`](TRANSLATION_STATUS.md) 中标记。这样每一次提交都能构建、审阅并跟随上游，而不会隐藏尚未翻译的内容。

## 在线阅读和本地构建

官方英文版：<https://doc.rust-lang.org/book/>

本地构建需要 mdBook 和仓库使用的预处理器。官方构建方式是：

```powershell
mdbook build
```

生成的站点位于 `book/` 目录。运行书中代码测试：

```powershell
cargo test --manifest-path packages/trpl/Cargo.toml --locked
mdbook test --library-path packages/trpl/target/debug/deps
```

## 翻译策略

- 官方 `rust-lang/book` 是内容和版本的唯一上游。
- [gnu4cn/rust-lang-zh_CN](https://github.com/gnu4cn/rust-lang-zh_CN) 用作参考译文、术语和章节组织的辅助材料，不直接覆盖本仓库内容。
- 保留 Rust 代码、代码标识符、命令、链接、锚点和示例行为。
- 翻译决定记录在 [`TRANSLATION.md`](TRANSLATION.md)，统一术语记录在 [`GLOSSARY.md`](GLOSSARY.md)。
- 每个已翻译文件记录对应的上游 commit，便于上游更新后重新审校。

## 参与贡献

请先阅读：

- [`TRANSLATION.md`](TRANSLATION.md)：翻译、同步和审校规则
- [`GLOSSARY.md`](GLOSSARY.md)：术语表
- [`TRANSLATION_STATUS.md`](TRANSLATION_STATUS.md)：文件级进度
- [`CONTRIBUTING.md`](CONTRIBUTING.md)：上游项目贡献说明

提交前至少运行：

```powershell
mdbook build
git diff --check
```

如果修改了代码清单或预处理器相关内容，再运行 `mdbook test`。

## 上游与许可证

- 中文 fork：<https://github.com/AreChen/book-cn>
- 官方上游：<https://github.com/rust-lang/book>
- 参考译文：<https://github.com/gnu4cn/rust-lang-zh_CN>
- 本仓库保留上游 MIT 和 Apache 2.0 许可证，详见 [`LICENSE-MIT`](LICENSE-MIT) 和 [`LICENSE-APACHE`](LICENSE-APACHE)。

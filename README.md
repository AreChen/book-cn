# 《Rust 程序设计语言》中文维护版 🦀

这是基于 [Rust 官方 Book 仓库](https://github.com/rust-lang/book) 的非官方中文翻译工作仓库。我们以官方 `main` 分支为内容上游，并参考社区已有译文来提高翻译效率和术语一致性。

> 中文版在线阅读：<https://arechen.github.io/book-cn/>

当前 `src/` 中的 112 个 Markdown 文件都已经完成第一轮中文翻译；接下来仍需要社区逐章审校、润色和跟随官方上游更新。翻译过程中的代码块、链接、锚点和 mdBook 标记会由自动检查器持续保护，具体进度见 [`TRANSLATION_STATUS.md`](TRANSLATION_STATUS.md)。

当前基线包含 956 个代码围栏和 424 个 `Listing` 标记。翻译检查器会将它们与官方 `upstream/main` 逐项比较，避免中文化过程中破坏示例代码或书籍构建结构。

## 在线阅读和本地构建

每次 `main` 分支有新的提交后，GitHub Actions 会自动构建并发布网站；也可以在仓库的 Actions 页面手动运行 Pages 工作流。

官方英文版：<https://doc.rust-lang.org/book/>

本地构建需要 mdBook 和仓库使用的预处理器：

```powershell
mdbook build
```

生成的站点位于 `book/` 目录。开发翻译时可以启动本地实时预览：

```powershell
mdbook serve --open
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

如果修改了代码清单或预处理器相关内容，再运行 `mdbook test`。Windows 上部分异步示例可能受本机 `link.exe` 查找 `windows.*.lib` 的方式影响；仓库 CI 在 Ubuntu 上执行完整的 mdBook 测试。

## 上游与许可证

- 中文 fork：<https://github.com/AreChen/book-cn>
- 官方上游：<https://github.com/rust-lang/book>
- 参考译文：<https://github.com/gnu4cn/rust-lang-zh_CN>
- 英文仓库说明：[`README.en.md`](README.en.md)
- 本仓库保留上游 MIT 和 Apache 2.0 许可证，详见 [`LICENSE-MIT`](LICENSE-MIT) 和 [`LICENSE-APACHE`](LICENSE-APACHE)。

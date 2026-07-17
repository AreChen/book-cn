# Rust Book 简体中文维护版设计

## 目标

把本地 `upstream/main` 所对应的 Rust 2024 版《Rust 程序设计语言》完整翻译为简体中文，并让仓库的默认 `mdbook build` 直接生成可阅读、可持续同步的中文版站点。

## 约束与事实来源

- `upstream/main` 是章节内容、代码、Rust Edition、链接和预处理器标记的唯一事实来源；本次基线为 `91754488`。
- `gnu4cn/rust-lang-zh_CN` 只作为表达、术语和旧章节译文的参考，必须以当前英文源码重新核对，不能整章覆盖。
- `src/` 保留官方文件名和目录结构，默认构建源是中文正文；代码块、输出、标识符、命令、路径、crate/API 名称、URL、锚点和 mdBook 标记保持可解析。
- 不引入仓库未声明的多语言 mdBook 功能，也不修改 `rustlings-cn`，不执行 commit 或 push。

## 架构

仓库继续使用官方 Book 的单一 `src/` 构建布局：翻译后的正文替换英文文本，`book.toml` 继续调用官方 `mdbook-trpl-note` 和 `mdbook-trpl-listing` 预处理器。英文同步通过已有 `upstream` remote、明确记录的上游 commit 和文件级状态完成，不把英文快照复制进构建目录。

章节处理采用“当前源码结构不变、文本层翻译”的规则。标题改为中文时，原源码已有的显式 `<a id>` 保持不变；缺少显式锚点但被正文引用的标题补充稳定的英文锚点，使原有链接不因中文标题而失效。代码围栏及其 info string、`Listing` 属性、`filename` 标记、`<!-- ignore -->` 注释和链接定义从当前英文版本保留，再只翻译自然语言标签/说明。

## 文档与维护

- `README.zh-CN.md` 说明中文入口、默认构建和验证命令。
- `TRANSLATION.md` 说明上游同步、参考译文使用、保留项和贡献流程。
- `TRANSLATION_STATUS.md` 为 112 个源 Markdown 文件记录当前基线、覆盖范围和复核状态；不能把未验证内容标成已审校。
- `GLOSSARY.md` 固化 ownership、borrowing、crate、trait、lifetime、async/await、Edition、Cargo 等术语。

## 验证

CI 和本地验证分层执行：先检查文件清单、SUMMARY 链接、Markdown 结构、代码块/预处理器标记与上游一致，再运行 `mdbook build`；随后运行 `cargo test --manifest-path packages/trpl/Cargo.toml --locked`，环境具备所需库时运行 `mdbook test`。任何平台工具链限制都在结果和文档中明确记录，不以单一构建成功代替代码测试。

## 失败处理

如果参考译文与当前英文源码不一致，保留当前源码的代码、链接和结构，重新翻译变化段落，并在状态表中标为需要复核。若 mdBook 预处理器或系统工具在 Windows/Ubuntu 上不可用，CI 保留可运行的静态检查和构建失败日志，不能静默跳过。

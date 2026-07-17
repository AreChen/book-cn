# Rust Book 简体中文维护版实施计划

> **面向 Agent 型工作者：** 本计划在当前工作树内执行；不 commit、不 push。步骤使用复选框跟踪。

**目标：** 将本地 `upstream/main`（`91754488`，Rust 2024）对应的 112 个 `src/*.md` 全部翻译为简体中文，并让默认 `mdbook build` 生成中文版站点。

**架构：** 保持官方 `src/` 文件名和目录，直接把当前英文源码中的自然语言替换为中文；`upstream` remote 作为英文同步基线。验证脚本从 `upstream/main` 与工作树读取结构和不可翻译 token，CI 先做静态检查再构建和运行测试。

**技术栈：** mdBook 0.5.1、Rust 1.97/Rust 2024、官方 `packages/mdbook-trpl` 预处理器、Python 3 标准库静态检查、GitHub Actions Ubuntu runner。

## 全局约束

- 以 `upstream/main` 的 `src/*.md`、`src/SUMMARY.md`、`book.toml` 和 `packages/` 为事实来源；本次基线为 `91754488`。
- `gnu4cn/rust-lang-zh_CN` 只作参考译文和术语来源；按当前英文源码逐段复核，不整章盲目覆盖。
- 保留 Rust 代码块、输出、代码标识符、命令、路径、crate/API 名称、URL、锚点、`Listing`、`filename` 和 `<!-- ignore -->`。
- 默认 `mdbook build` 只读取中文 `src/`，不引入不存在的多语言 mdBook 功能。
- 不修改 `rustlings-cn`，不执行 commit 或 push；任何未通过验证的内容不得标为“已审校”。

---

### 任务 1：建立基线和不可破坏结构检查

**文件：**
- 创建：`ci/check_translation.py`
- 修改：`.github/workflows/main.yml`
- 修改：`TRANSLATION_STATUS.md`
- 修改：`TRANSLATION.md`

**接口：**
- `ci/check_translation.py` 接受可选 `--upstream-ref`（默认 `upstream/main`）和 `--root`（默认当前仓库），退出码非零表示源文件清单、SUMMARY 目标、代码围栏、Listing/filename/ignore 标记或 URL/token 与上游不一致。
- 脚本使用 `git show <ref>:<path>` 读取上游文件；没有 ref 时报告可复现的缺失原因，并执行不依赖 Git 的 Markdown 检查。

- [ ] **步骤 1：编写结构检查器**：遍历当前和上游的 `src/*.md`，检查 112 个文件路径一致；逐文件比较围栏语言标记、代码块内容、`<Listing ...>` 属性、`<span class="filename">`、`<!-- ignore -->`、URL 和显式 `id` 集合；允许自然语言正文、标题和 SUMMARY 显示文本变化。
- [ ] **步骤 2：加入 SUMMARY/Markdown 检查**：解析 `src/SUMMARY.md` 的 Markdown 链接，确认每个相对目标存在；检查正文链接括号成对、代码围栏成对、HTML 标签中未出现明显的中文替代文件名/API；忽略官方预处理器注释链接。
- [ ] **步骤 3：先在当前英文基线运行脚本**：运行 `python ci/check_translation.py --upstream-ref upstream/main`，预期只有工作树尚未翻译的内容报告为允许的自然语言差异，结构错误为 0。
- [ ] **步骤 4：在 CI 中执行静态检查**：把 `python ci/check_translation.py --upstream-ref upstream/main` 放在 `mdbook build` 之前，并在 checkout 后显式 fetch `rust-lang/book` 的 `main` 到 `refs/remotes/upstream/main`；本地无网络时保留已有 ref。

### 任务 2：翻译入口、入门和基础概念（第 0–4 章）

**文件：**
- 修改：`src/title-page.md`、`src/foreword.md`、`src/ch00-00-introduction.md`、`src/SUMMARY.md`
- 修改：`src/ch01-00-getting-started.md`、`src/ch01-01-installation.md`、`src/ch01-02-hello-world.md`、`src/ch01-03-hello-cargo.md`
- 修改：`src/ch02-00-guessing-game-tutorial.md`
- 修改：`src/ch03-00-common-programming-concepts.md`、`src/ch03-01-variables-and-mutability.md`、`src/ch03-02-data-types.md`、`src/ch03-03-how-functions-work.md`、`src/ch03-04-comments.md`、`src/ch03-05-control-flow.md`
- 修改：`src/ch04-00-understanding-ownership.md`、`src/ch04-01-what-is-ownership.md`、`src/ch04-02-references-and-borrowing.md`、`src/ch04-03-slices.md`

**接口：** 每个文件继续使用上游同名路径；代码/输出/链接和 `Listing` 属性与任务 1 的检查器逐字一致，所有自然语言标题和段落为简体中文。

- [ ] **步骤 1：对照当前英文和参考译文建立章节术语**：优先采用“所有权、借用、引用、生命周期、切片、模式匹配、可变性、控制流”等 `GLOSSARY.md` 术语，重新核对 Rust 2024 与 Cargo 文案。
- [ ] **步骤 2：逐文件翻译自然语言**：只编辑标题、段落、列表说明、图片/Listing caption 和非代码 filename 标签；不翻译 `rustup`、`cargo`、`rustc`、Rust API、示例输出和命令。
- [ ] **步骤 3：保留/补齐锚点**：保留上游现有 `<a id>`；对于正文引用的英文标题锚点，在翻译标题旁保留稳定英文 `id`，使原 URL fragment 不变。
- [ ] **步骤 4：运行任务 1 检查器和 `git diff --check`**：确认第 0–4 章的结构差异只发生在允许翻译区域。

### 任务 3：翻译结构化数据、枚举、模块和集合（第 5–8 章）

**文件：**
- 修改：`src/ch05-00-structs.md`、`src/ch05-01-defining-structs.md`、`src/ch05-02-example-structs.md`、`src/ch05-03-method-syntax.md`
- 修改：`src/ch06-00-enums.md`、`src/ch06-01-defining-an-enum.md`、`src/ch06-02-match.md`、`src/ch06-03-if-let.md`
- 修改：`src/ch07-00-managing-growing-projects-with-packages-crates-and-modules.md`、`src/ch07-01-packages-and-crates.md`、`src/ch07-02-defining-modules-to-control-scope-and-privacy.md`、`src/ch07-03-paths-for-referring-to-an-item-in-the-module-tree.md`、`src/ch07-04-bringing-paths-into-scope-with-the-use-keyword.md`、`src/ch07-05-separating-modules-into-different-files.md`
- 修改：`src/ch08-00-common-collections.md`、`src/ch08-01-vectors.md`、`src/ch08-02-strings.md`、`src/ch08-03-hash-maps.md`

- [ ] **步骤 1：统一 crate/package/module/trait/pattern 译法**：依据术语表使用 `crate`、包、模块、trait、模式，并保留代码中的英文关键字。
- [ ] **步骤 2：翻译正文和标题**：以当前上游代码为准重写解释，特别复核 `let...else`、`match`、UTF-8、所有权转移和 module tree 链接。
- [ ] **步骤 3：逐文件保留代码与 HTML 标记**：确保示例中的 `src/*.rs`、`Cargo.toml`、`HashMap`、`Option<T>` 和输出没有被中文化。
- [ ] **步骤 4：运行结构检查和对应章节 `mdbook build`**：静态检查通过后再合并到完整构建。

### 任务 4：翻译错误处理、泛型、测试、I/O 与 Cargo（第 9–14 章）

**文件：**
- 修改：`src/ch09-00-error-handling.md`、`src/ch09-01-unrecoverable-errors-with-panic.md`、`src/ch09-02-recoverable-errors-with-result.md`、`src/ch09-03-to-panic-or-not-to-panic.md`
- 修改：`src/ch10-00-generics.md`、`src/ch10-01-syntax.md`、`src/ch10-02-traits.md`、`src/ch10-03-lifetime-syntax.md`
- 修改：`src/ch11-00-testing.md`、`src/ch11-01-writing-tests.md`、`src/ch11-02-running-tests.md`、`src/ch11-03-test-organization.md`
- 修改：`src/ch12-00-an-io-project.md`、`src/ch12-01-accepting-command-line-arguments.md`、`src/ch12-02-reading-a-file.md`、`src/ch12-03-improving-error-handling-and-modularity.md`、`src/ch12-04-testing-the-librarys-functionality.md`、`src/ch12-05-working-with-environment-variables.md`、`src/ch12-06-writing-to-stderr-instead-of-stdout.md`
- 修改：`src/ch13-00-functional-features.md`、`src/ch13-01-closures.md`、`src/ch13-02-iterators.md`、`src/ch13-03-improving-our-io-project.md`、`src/ch13-04-performance.md`
- 修改：`src/ch14-00-more-about-cargo.md`、`src/ch14-01-release-profiles.md`、`src/ch14-02-publishing-to-crates-io.md`、`src/ch14-03-cargo-workspaces.md`、`src/ch14-04-installing-binaries.md`、`src/ch14-05-extending-cargo.md`

- [ ] **步骤 1：翻译错误、类型和测试术语**：保持 `panic!`、`Result`、`Option`、泛型参数、trait bound、lifetime、`#[test]` 和命令输出原样。
- [ ] **步骤 2：翻译 I/O 项目**：保留 `grep`、文件名、环境变量、stdin/stderr、Cargo 命令和每个逐步代码清单，依据当前上游重核对错误处理流程。
- [ ] **步骤 3：翻译 Cargo 章节**：保留 crates.io、manifest、workspace、profile、`cargo install` 等 crate/API/命令名称，复核 2024 Edition 文案和 URL。
- [ ] **步骤 4：运行检查器、`cargo test --manifest-path packages/trpl/Cargo.toml --locked` 前置编译和完整 mdBook 构建**。

### 任务 5：翻译智能指针、并发和 async 新章节（第 15–17 章）

**文件：**
- 修改：`src/ch15-00-smart-pointers.md`、`src/ch15-01-box.md`、`src/ch15-02-deref.md`、`src/ch15-03-drop.md`、`src/ch15-04-rc.md`、`src/ch15-05-interior-mutability.md`、`src/ch15-06-reference-cycles.md`
- 修改：`src/ch16-00-concurrency.md`、`src/ch16-01-threads.md`、`src/ch16-02-message-passing.md`、`src/ch16-03-shared-state.md`、`src/ch16-04-extensible-concurrency-sync-and-send.md`
- 修改：`src/ch17-00-async-await.md`、`src/ch17-01-futures-and-syntax.md`、`src/ch17-02-concurrency-with-async.md`、`src/ch17-03-more-futures.md`、`src/ch17-04-streams.md`、`src/ch17-05-traits-for-async.md`、`src/ch17-06-futures-tasks-threads.md`

- [ ] **步骤 1：统一 smart pointer、interior mutability、concurrency、asynchronous、future、stream、task、runtime 术语**，把 async/await、Future、Stream、`Send`、`Sync`、`Pin` 等代码/API 标识符保留。
- [ ] **步骤 2：逐段对照当前 async 源码**：重点检查当前版本新增/修改的 `async fn`、`await`、future combinator、stream、任务与线程描述，不把旧参考仓库版本直接覆盖。
- [ ] **步骤 3：保留所有 tokio/futures 示例依赖、命令和输出**，检查代码块的 Rust 2024 编译属性和 `ignore` 标记。
- [ ] **步骤 4：运行结构检查、trpl package tests、`mdbook build`，在可行时运行 `mdbook test --library-path packages/trpl/target/debug/deps`。

### 任务 6：翻译面向对象、模式、高级特性、最终项目与附录（第 18–21 章及附录）

**文件：**
- 修改：`src/ch18-00-oop.md`、`src/ch18-01-what-is-oo.md`、`src/ch18-02-trait-objects.md`、`src/ch18-03-oo-design-patterns.md`
- 修改：`src/ch19-00-patterns.md`、`src/ch19-01-all-the-places-for-patterns.md`、`src/ch19-02-refutability.md`、`src/ch19-03-pattern-syntax.md`
- 修改：`src/ch20-00-advanced-features.md`、`src/ch20-01-unsafe-rust.md`、`src/ch20-02-advanced-traits.md`、`src/ch20-03-advanced-types.md`、`src/ch20-04-advanced-functions-and-closures.md`、`src/ch20-05-macros.md`
- 修改：`src/ch21-00-final-project-a-web-server.md`、`src/ch21-01-single-threaded.md`、`src/ch21-02-multithreaded.md`、`src/ch21-03-graceful-shutdown-and-cleanup.md`
- 修改：`src/appendix-00.md`、`src/appendix-01-keywords.md`、`src/appendix-02-operators.md`、`src/appendix-03-derivable-traits.md`、`src/appendix-04-useful-development-tools.md`、`src/appendix-05-editions.md`、`src/appendix-06-translation.md`、`src/appendix-07-nightly-rust.md`

- [ ] **步骤 1：翻译第 18–20 章**：保留 `dyn Trait`、`unsafe`、宏语法、编译器输出和所有显式锚点，依据当前 Rust 2024 语义复核高级主题。
- [ ] **步骤 2：翻译最终项目**：保留 Web 服务器示例中的 HTTP 文本、路径、线程/通道 API、文件名和逐步代码，确保代码可测试。
- [ ] **步骤 3：逐项翻译附录表格和说明**：关键字、运算符、可派生 trait、rustfmt/rustfix/Clippy/rust-analyzer、Edition、译文说明和 nightly Rust 中的关键字/API/命令保持原样。
- [ ] **步骤 4：检查 SUMMARY 中所有标题和附录链接**，运行全量结构检查和构建。

### 任务 7：完成术语、构建入口、维护文档和贡献流程

**文件：**
- 修改：`book.toml`
- 修改：`README.zh-CN.md`、`README.md`
- 修改：`TRANSLATION.md`、`TRANSLATION_STATUS.md`、`GLOSSARY.md`
- 修改：`src/SUMMARY.md`

- [ ] **步骤 1：将 `book.toml` 标题、仓库链接说明和默认构建确认成中文站点入口**，保留官方预处理器和 Rust 2024 配置；不添加伪多语言配置。
- [ ] **步骤 2：把 `README.zh-CN.md` 更新为事实文档**：写明 112/112 文件覆盖、上游 commit `91754488`、参考仓库、默认 `mdbook build`、分层验证、Windows/Ubuntu 说明和不包含的测试缺口。
- [ ] **步骤 3：把 `TRANSLATION.md` 写成可执行同步/贡献流程**：fetch upstream、比较 commit、逐文件复核、禁止覆盖未提交中文、PR 检查清单。
- [ ] **步骤 4：为所有 112 个 `src/*.md` 生成逐文件状态表**：只有经过代码/链接/构建检查的文件标为 `已审校`；若验证受环境限制，明确标为 `进行中` 或 `需要复核` 并解释原因。
- [ ] **步骤 5：补充 async/await、future、stream、task、runtime、edition、preprocessor、listing、anchor 等术语，并检查术语表与正文一致。

### 任务 8：完成 CI 分层验证和本地结果记录

**文件：**
- 修改：`.github/workflows/main.yml`
- 修改：`ci/validate.sh`
- 修改：`README.zh-CN.md`、`TRANSLATION.md`

- [ ] **步骤 1：CI 安装固定 mdBook 0.5.1 和 Rust 1.97**，先运行 Python 静态检查和 `mdbook build`，再构建 `packages/trpl`。
- [ ] **步骤 2：运行 `cargo test --manifest-path packages/trpl/Cargo.toml --locked`**，随后运行 `mdbook test --library-path packages/trpl/target/debug/deps`；将 mdBook 测试因网络、平台或示例依赖失败的原因写入 CI 摘要而不是静默忽略。
- [ ] **步骤 3：运行 shellcheck、`ci/validate.sh`、Markdown/链接结构检查和生成站点链接检查；确保 CI 在 Ubuntu 上工作，并提供 Windows PowerShell 对等命令。
- [ ] **步骤 4：本地执行完整命令集并保存实际退出码/失败根因**：
  - `python ci/check_translation.py --upstream-ref upstream/main`
  - `mdbook build`
  - `cargo test --manifest-path packages/trpl/Cargo.toml --locked`
  - `mdbook test --library-path packages/trpl/target/debug/deps`
  - `bash ci/validate.sh`
  - `git diff --check`
- [ ] **步骤 5：检查 `git status --short` 和 diff，确认只改动 `book-cn` 范围内文件，没有 `rustlings-cn`、commit 或 push。

## 自审结果

- 需求 1 由任务 2–6 和任务 1 的结构/token 检查覆盖，包含全部 112 个 `src/*.md`、标题、目录和附录。
- 需求 2 由任务 2–6 的参考译文使用规则、任务 7 的术语表和上游 commit 记录覆盖。
- 需求 3 由任务 7 的单源中文构建与已有 `upstream` remote 覆盖，不依赖多语言 mdBook。
- 需求 4 由任务 7 的四份维护文档覆盖，并要求真实记录状态。
- 需求 5 由任务 1 和任务 8 的跨平台 Python/CI、Markdown、链接、代码块与构建检查覆盖。
- 需求 6 由任务 8 的完整命令集覆盖；失败必须记录根因。
- 本计划没有未定义的函数、路径或成功占位符，也没有 commit/push 步骤。

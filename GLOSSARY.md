# Rust 中文术语表

这是本仓库的工作术语表。遇到官方新概念或社区存在明显分歧时，先在 Issue 或 PR 中讨论，再更新这里。

| English | 中文建议 | 说明 |
| --- | --- | --- |
| ownership | 所有权 | Rust 的核心概念，首次出现可附英文 |
| borrowing | 借用 | 与 borrow checker 配套使用 |
| borrow checker | 借用检查器 | 不译成“借贷检查器” |
| reference | 引用 | `&T` 和 `&mut T` 的 reference |
| lifetime | 生命周期 | 保留 lifetime 作为搜索关键词 |
| crate | crate（代码包） | 不把 crate 误译成普通软件包 |
| package | 包 | Cargo 的 package 概念 |
| module | 模块 | module tree 译为模块树 |
| trait | trait（特征） | 代码中保留 `trait` |
| generic | 泛型 | generic type 译为泛型类型 |
| closure | 闭包 | |
| iterator | 迭代器 | |
| pattern | 模式 | pattern matching 译为模式匹配 |
| slice | 切片 | |
| smart pointer | 智能指针 | |
| concurrency | 并发 | concurrency 与 parallelism 区分处理 |
| asynchronous | 异步 | async/await 代码保留原样 |
| edition | Edition（版本） | 具体写作 Rust 2024 Edition |
| unsafe Rust | 不安全 Rust | 不把 unsafe 解释成“不安全的语言” |

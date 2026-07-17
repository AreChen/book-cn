# 中文翻译进度

状态定义：

- `未开始`：当前保留官方英文内容。
- `进行中`：已有中文内容，但还没有完成社区审校。
- `已审校`：已按当前上游 commit 构建、检查链接和复核代码块。
- `需要复核`：上游文件发生变化，需要重新对照英文内容。

## 当前基线

- 上游：`rust-lang/book` 的 `main`
- 本地初始上游 commit：见 `git log -1` 和 `git merge-base main upstream/main`
- 参考译文：`gnu4cn/rust-lang-zh_CN`
- 当前范围：官方 `main` 分支中的 112 个 Markdown 文件

## 文件状态

| 文件范围 | 状态 | 说明 |
| --- | --- | --- |
| `src/SUMMARY.md` | 进行中 | 中文目录，链接目标与官方结构保持一致 |
| `src/title-page.md`、`src/foreword.md` | 进行中 | 已完成第一轮中文翻译，待社区审校 |
| `src/ch00-00-introduction.md` | 进行中 | 简介已完成第一轮中文翻译，待社区审校 |
| `src/ch01-*.md` – `src/ch21-*.md` | 进行中 | 第 1–21 章已完成第一轮中文翻译，待逐章审校 |
| `src/appendix-*.md` | 进行中 | 附录已完成第一轮中文翻译，专有名称和外部译本链接保留原样 |

## 自动检查快照

- 112 个源文件均包含中文内容。
- 956 个代码围栏、424 个 `Listing` 标记、链接目标、URL、HTML 注释和锚点已与 `upstream/main` 对齐。
- `ci/check_translation.py --upstream-ref upstream/main --require-chinese` 已通过。
- 仍需人工重点审校：术语一致性、中文自然度、与最新版 Rust API 的解释是否清晰，以及上游更新后的差异。

新增或修改章节时，请同时更新本表和对应的上游 commit 记录。上游文件发生变化后，相关条目应改为“需要复核”，完成审校并重新运行构建和检查后再改回“进行中”或“已审校”。

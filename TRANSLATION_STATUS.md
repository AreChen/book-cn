# 中文翻译进度

状态定义：

- `未开始`：当前保留官方英文内容。
- `进行中`：已有中文内容，但还没有完成审校。
- `已审校`：已按当前上游 commit 构建、检查链接和复核代码块。
- `需要复核`：上游文件发生变化，需要重新对照英文内容。

## 当前基线

- 上游：`rust-lang/book` 的 `main`
- 本地初始上游 commit：见 `git log -1` 和 `git merge-base main upstream/main`
- 参考译文：`gnu4cn/rust-lang-zh_CN`

## 文件状态

| 文件 | 状态 | 说明 |
| --- | --- | --- |
| `src/SUMMARY.md` | 进行中 | 第一章入口标题已中文化 |
| `src/ch01-00-getting-started.md` | 进行中 | 章节入口页已完成初译，待审校 |
| `src/ch01-01-installation.md` | 未开始 | 保留当前官方英文原文 |
| `src/ch01-02-hello-world.md` | 未开始 | 保留当前官方英文原文 |
| `src/ch01-03-hello-cargo.md` | 未开始 | 保留当前官方英文原文 |
| 其他 `src/` 文件 | 未开始 | 保留当前官方英文原文 |

新增或修改章节时，请同时更新本表和对应的上游 commit 记录。

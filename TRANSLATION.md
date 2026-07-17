# Book 中文翻译与同步指南

## 项目关系

- 中文仓库：<https://github.com/AreChen/book-cn>
- 官方上游：<https://github.com/rust-lang/book>
- 参考译文：<https://github.com/gnu4cn/rust-lang-zh_CN>
- `origin` 指向中文 fork，`upstream` 指向官方 Book 仓库。

## 翻译原则

1. 先阅读当前官方英文内容，再参考社区译文，最后用统一术语写出自然中文。
2. 代码块、Rust 关键字、类型名、函数名、crate 名、命令、文件名、链接 URL 和 HTML 锚点保持原样。
3. 不为了中文表达而改变示例代码、测试、命令输出或章节结构。
4. `Listing`、`<span class="filename">`、`<!-- ignore -->` 等 mdBook 预处理器标记必须保持可解析。
5. 章节标题和正文翻译保持一致；第一次出现的重要术语按 `GLOSSARY.md` 处理。
6. 官方英文源码有变化时，先更新上游基线，再对受影响的中文文件进行审校。

## 上游同步

翻译工作进行期间不要直接覆盖本地改动。建议先查看上游变化，再逐文件处理：

```powershell
git fetch upstream
git log --oneline main..upstream/main
git diff --stat main...upstream/main
```

不要在有未提交翻译时直接合并或覆盖 `src/`。每个翻译文件需要记录审校时对应的上游 commit；上游改动后，先在进度表中标为“需要复核”，再重新翻译相关段落。

## 参考译文的使用方式

`gnu4cn/rust-lang-zh_CN` 是有价值的社区参考，但它的文件命名、章节组织、Rust 版本基线和措辞可能与官方当前 Book 不完全一致。使用时遵循以下顺序：

1. 以本仓库 `upstream/main` 的英文文件为准。
2. 用参考仓库查找已有的术语和解释方式。
3. 根据当前章节的代码、Edition 和链接重新核对。
4. 在本仓库的术语表和提交说明中记录有争议的决定。

## 审校清单

- [ ] 代码块与原文逐字对应，能被 mdBook 正常解析。
- [ ] 命令、路径、crate 名和 API 名称没有被误译。
- [ ] Markdown 链接和页面内锚点有效。
- [ ] 术语符合 `GLOSSARY.md`。
- [ ] 没有遗漏英文段落，也没有把参考译文中的旧版本内容带入当前章节。
- [ ] `mdbook build` 和相关 `mdbook test` 通过。

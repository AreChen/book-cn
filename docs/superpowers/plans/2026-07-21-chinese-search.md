# 中文搜索增强实施计划

> **面向 Agent 型工作者：** 本计划在当前工作树内执行；每项任务按 TDD 顺序验证，并在最终验证通过后提交和推送。步骤使用复选框跟踪。

**目标：** 在不破坏 mdBook 原生英文搜索的前提下，让中文版 Rust Book 支持中文短语、中文单词以及中英文混合关键词搜索。

**架构：** 保留 mdBook 的搜索索引和英文搜索流程；构建完成后，从 mdBook 生成的 `searchindex*.js` 提取章节文档，生成按章节保存的轻量中文搜索数据。`search-cn.js` 仅在查询包含汉字时拦截输入，使用浏览器端规范化、短语包含匹配和标题/层级/正文加权排序；英文查询继续交给 mdBook 原生搜索。

**技术栈：** mdBook 0.5.1、原生浏览器 JavaScript、Node.js 内置 `vm`/`fs`/`node:test`、GitHub Actions Pages 构建。

## 全局约束

- 中文查询必须支持连续短语，例如“所有权”“生命周期”“错误处理”。
- 中英文混合查询必须支持，例如 `Rust 所有权`、`async 异步`。
- 中文结果显示中文结果计数、章节路径和正文上下文摘要，并保留 mdBook 的 `?highlight=` 页面高亮跳转。
- 英文查询、Rust/API 代码关键词、搜索快捷键和结果键盘导航继续使用 mdBook 原生行为。
- 中文搜索索引只能由当前构建生成的 `book/searchindex*.js` 产生，不能手工维护页面内容副本。
- `mdbook build` 后必须执行 `node tools/build_search_index.mjs`，Pages 和 CI 的构建流程都要明确执行该命令。
- 不新增运行时依赖；构建索引和测试只使用 Node.js 标准库。

---

### 任务 1：为中文查询行为建立失败测试

**文件：**

- 创建：`tools/test_search_cn.mjs`
- 待读取：`search-cn.js`

**接口：**

- 测试通过 Node `vm` 执行 `search-cn.js` 的无 DOM 分支，并读取 `globalThis.bookCnSearch`。
- `bookCnSearch.tokenizeQuery(query)` 返回按中文连续片段和英文/数字片段拆分、经过 NFKC 与小写规范化的关键词数组。
- `bookCnSearch.searchDocuments(docs, query, limit)` 返回按相关性排序的 `{ doc, score }` 结果数组。
- `bookCnSearch.makeTeaser(body, query, maxLength)` 返回已转义 HTML，并用 `<em>` 标出匹配词的摘要。

- [ ] **步骤 1：编写失败测试**：覆盖“所有权”短语匹配、`Rust 所有权` 混合匹配、标题命中高于正文命中、无结果返回空数组、摘要转义 HTML 和单元测试中的最小文档集合。
- [ ] **步骤 2：运行测试确认失败**：运行 `rtk node --test tools/test_search_cn.mjs`；预期测试因 `search-cn.js` 尚不存在或 `bookCnSearch` 未定义而失败，失败原因必须是功能缺失而不是测试语法错误。
- [ ] **步骤 3：暂不修改测试以迎合失败**：保留测试对公开函数名称和具体结果的约束，为后续实现提供红灯基线。

### 任务 2：实现可测试的中文搜索核心和浏览器适配器

**文件：**

- 创建：`search-cn.js`
- 修改：`book.toml:8-10`

**接口：**

- `bookCnSearch.hasHan(text)` 检测汉字字符。
- `bookCnSearch.normalizeText(text)` 执行 NFKC 规范化和大小写归一化。
- `bookCnSearch.tokenizeQuery(query)` 把 `Rust所有权` 拆成 `rust` 与 `所有权`，把 `错误处理` 保持为一个连续中文短语。
- `bookCnSearch.searchDocuments(docs, query, limit)` 对每个关键词执行字段内包含匹配；标题、章节层级、正文分别使用高、中、低权重排序；所有关键词都必须命中。
- `bookCnSearch.makeTeaser(body, query, maxLength)` 生成安全摘要并高亮关键词。
- 浏览器适配器在 `document` 存在时监听搜索框的 `input`、`keyup`、`compositionend` 和 `popstate`；含中文查询时停止 mdBook 原生事件传播，加载 `search-zh-index.js`，渲染中文计数、结果链接和摘要；不含中文时不拦截原生事件。

- [ ] **步骤 1：实现纯函数核心**：在 DOM 初始化之前定义并挂载 `bookCnSearch`；对空查询、NFKC 文本、连续中文片段、混合关键词、字段权重、结果上限、HTML 转义和摘要截断提供确定性行为。
- [ ] **步骤 2：实现浏览器适配器**：惰性加载 `path_to_root + "search-zh-index.js"`，通过 `window.bookCnSearchIndex.docs` 读取文档；使用 `textContent` 写入结果标题，使用转义后的摘要写入 `innerHTML`；结果链接携带 `highlight` 参数和原始章节锚点。
- [ ] **步骤 3：接入 mdBook**：将 `search-cn.js` 加入 `[output.html].additional-js`，保持 `ferris.js` 和 mdBook 原生搜索脚本同时存在。
- [ ] **步骤 4：运行红绿测试**：先运行 `rtk node --test tools/test_search_cn.mjs` 确认通过，再运行同一命令确认输出无警告。

### 任务 3：生成中文搜索索引并接入构建流程

**文件：**

- 创建：`tools/build_search_index.mjs`
- 修改：`.github/workflows/pages.yml:44-49`
- 修改：`.github/workflows/main.yml` 的 lint 构建步骤

**接口：**

- `tools/build_search_index.mjs` 默认读取当前目录的 `book/`，也接受一个可选输出目录参数。
- 脚本定位唯一的 `book/searchindex*.js`，在隔离 `vm` 中解析 `window.search`，按 `doc_urls` 和 `documentStore.docs` 输出 `book/search-zh-index.js`。
- 输出格式为 `window.bookCnSearchIndex = { docs: [{ url, title, breadcrumbs, body }] };`，文档顺序与 mdBook 原始引用一致。
- 找不到搜索索引、解析结果缺少 `doc_urls` 或文档存储时退出码非零并输出明确错误。

- [ ] **步骤 1：编写生成器测试夹具**：在 `tools/test_search_cn.mjs` 中为索引提取函数提供带有两个文档、两个 URL 和一个中文正文的最小 `searchindex` 配置，断言生成结果保留 URL、标题、章节路径和正文。
- [ ] **步骤 2：运行测试确认生成器失败**：运行 `rtk node --test tools/test_search_cn.mjs`；预期新增索引提取断言因 `tools/build_search_index.mjs` 不存在而失败。
- [ ] **步骤 3：实现索引生成器**：使用 Node 标准库解析生成的 mdBook 索引，稳定排序文档，使用 `JSON.stringify` 输出可直接执行的 JS，并处理 U+2028/U+2029 等脚本分隔符。
- [ ] **步骤 4：在 Pages 构建中执行生成器**：将 `node tools/build_search_index.mjs` 放在 `mdbook build` 之后、`actions/upload-pages-artifact` 之前。
- [ ] **步骤 5：在 CI lint 构建中执行生成器**：将同一命令放在 `mdbook build` 之后，确保本地和 CI 构建产物都包含中文索引。
- [ ] **步骤 6：运行测试和一次本地构建**：运行 `rtk node --test tools/test_search_cn.mjs` 与 `rtk mdbook build`，再运行 `rtk node tools/build_search_index.mjs`；预期生成 `book/search-zh-index.js` 且包含全部 mdBook 搜索章节。

### 任务 4：补充本地使用说明并完成全量验证

**文件：**

- 修改：`README.md`
- 修改：`README.zh-CN.md`

- [ ] **步骤 1：更新中文构建说明**：明确本地预览依次运行 `mdbook build`、`node tools/build_search_index.mjs` 和 `mdbook serve`；说明中文搜索首次输入中文时会惰性加载索引，英文搜索仍由 mdBook 提供。
- [ ] **步骤 2：复现原始失败用例**：在当前线上索引或构建前的 mdBook 原始索引上确认“所有权”无结果，记录为回归基线；不得把原始索引误当作修复后的中文索引。
- [ ] **步骤 3：验证生成索引**：使用 Node 加载 `book/search-zh-index.js` 和 `search-cn.js`，对“所有权”“借用”“生命周期”“Rust 所有权”“async 异步”分别断言结果数大于 0，并断言不存在的短语结果数为 0。
- [ ] **步骤 4：运行仓库已有检查**：运行 `rtk node --test tools/test_search_cn.mjs`、`rtk mdbook build`、`rtk node tools/build_search_index.mjs`、`rtk cargo test --manifest-path packages/mdbook-trpl/Cargo.toml --locked` 和 `rtk git diff --check`。
- [ ] **步骤 5：检查工作树和提交**：运行 `rtk git status --short --branch`，确认只包含搜索功能相关文件；提交消息使用 `feat: improve Chinese book search`。
- [ ] **步骤 6：推送并手动验证 Pages**：推送 `main` 后等待 CI 与 Pages 工作流；直接检查线上首页和至少一个章节的中文查询结果、结果链接中的 `highlight` 参数以及页面跳转后的 `<mark>` 高亮。

## 自审结果

- 中文短语和混合查询由任务 1–2 的纯函数测试与任务 4 的真实关键词检查覆盖。
- 原生英文搜索不被覆盖由任务 2 的“只在含汉字时拦截”约束和任务 4 的英文回归检查覆盖。
- 构建索引的来源、输出格式、缺失文件错误和 Pages/CI 接入由任务 3 覆盖。
- 结果安全性由任务 2 的 HTML 转义测试覆盖，链接高亮由任务 2 和任务 4 的跳转验证覆盖。
- 计划中的文件路径、函数名称和测试命令均已定义，没有未完成占位符。

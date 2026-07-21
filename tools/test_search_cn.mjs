import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import vm from "node:vm";

async function loadSearchApi() {
  const source = await readFile(new URL("../search-cn.js", import.meta.url), "utf8");
  const sandbox = { console };
  sandbox.globalThis = sandbox;
  vm.runInNewContext(source, sandbox, { filename: "search-cn.js" });
  return sandbox.bookCnSearch;
}

const documents = [
  {
    url: "ch04-01-what-is-ownership.html#what-is-ownership",
    title: "何为所有权？",
    breadcrumbs: "Rust 程序设计语言 » 掌握所有权 » 何为所有权？",
    body: "所有权是 Rust 管理内存的核心概念。每个值都有一个所有者。",
  },
  {
    url: "ch10-03-lifetime-syntax.html#lifetime-syntax",
    title: "以生命周期验证引用",
    breadcrumbs: "Rust 程序设计语言 » 泛型、特质与生命周期 » 生命周期",
    body: "生命周期确保引用始终有效，避免悬垂引用。",
  },
  {
    url: "ch17-00-async-await.html#async-await",
    title: "异步编程基础",
    breadcrumbs: "Rust 程序设计语言 » 异步编程基础",
    body: "async 与 await 让异步代码更容易编写。",
  },
];

test("中文查询按连续短语拆分，混合查询保留中英文关键词", async () => {
  const api = await loadSearchApi();

  assert.deepEqual([...api.tokenizeQuery("Rust所有权 async 异步")], [
    "rust",
    "所有权",
    "async",
    "异步",
  ]);
});

test("中文短语和中英文混合关键词可以命中章节", async () => {
  const api = await loadSearchApi();

  assert.equal(api.searchDocuments(documents, "所有权")[0].doc.url, documents[0].url);
  assert.equal(api.searchDocuments(documents, "Rust 所有权")[0].doc.url, documents[0].url);
  assert.equal(api.searchDocuments(documents, "async 异步")[0].doc.url, documents[2].url);
});

test("标题命中优先于仅正文命中，不存在的短语返回空数组", async () => {
  const api = await loadSearchApi();
  const ranked = api.searchDocuments([
    {
      url: "body.html",
      title: "其他章节",
      breadcrumbs: "Rust 程序设计语言",
      body: "这里讨论所有权相关的正文内容。",
    },
    documents[0],
  ], "所有权");

  assert.equal(ranked[0].doc.url, documents[0].url);
  assert.deepEqual([...api.searchDocuments(documents, "不存在的 Rust 概念")], []);
});

test("摘要会转义 HTML 并高亮匹配词", async () => {
  const api = await loadSearchApi();
  const teaser = api.makeTeaser("<script>alert(1)</script> 所有权负责管理内存。", "所有权");

  assert.equal(teaser.includes("<script>"), false);
  assert.equal(teaser.includes("&lt;script&gt;"), true);
  assert.equal(teaser.includes("<em>所有权</em>"), true);
});

test("生成器从 mdBook 索引提取文档并输出可执行的中文索引", async () => {
  const { createSearchIndexScript, extractSearchDocuments } = await import("./build_search_index.mjs");
  const config = {
    doc_urls: ["first.html#intro", "second.html"],
    index: {
      documentStore: {
        docs: {
          "0": {
            title: "简介",
            breadcrumbs: "书 » 简介",
            body: "Rust 入门。",
          },
          "1": {
            title: "所有权",
            breadcrumbs: "书 » 所有权",
            body: "所有权规则。",
          },
        },
      },
    },
  };

  const docs = extractSearchDocuments(config);
  assert.deepEqual(docs[1], {
    url: "second.html",
    title: "所有权",
    breadcrumbs: "书 » 所有权",
    body: "所有权规则。",
  });

  const sandbox = { window: {} };
  vm.runInNewContext(createSearchIndexScript(docs), sandbox);
  assert.deepEqual(JSON.parse(JSON.stringify(sandbox.window.bookCnSearchIndex.docs)), docs);
});

import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import vm from "node:vm";

const SEARCH_INDEX_PATTERN = /^searchindex(?:-[0-9a-f]+)?\.js$/i;

export function findSearchIndexName(fileNames) {
  const matches = fileNames.filter((fileName) => SEARCH_INDEX_PATTERN.test(fileName));
  if (matches.length === 0) {
    throw new Error("未找到 mdBook 生成的 searchindex*.js");
  }

  return matches.sort()[matches.length - 1];
}

export function parseSearchIndex(source, filename = "searchindex.js") {
  const sandbox = { window: { search: {} } };
  vm.runInNewContext(source, sandbox, { filename });
  const config = sandbox.window.search;
  if (!config || !Array.isArray(config.doc_urls)) {
    throw new Error("mdBook 搜索索引缺少 doc_urls");
  }
  if (!config.index?.documentStore?.docs) {
    throw new Error("mdBook 搜索索引缺少 documentStore.docs");
  }
  return config;
}

export function extractSearchDocuments(config) {
  const docs = config.index.documentStore.docs;
  return config.doc_urls.map((url, ref) => {
    const doc = docs[String(ref)] ?? docs[ref];
    if (!doc) {
      throw new Error(`mdBook 搜索索引缺少文档 ${ref}`);
    }

    return {
      url: String(url),
      title: String(doc.title ?? ""),
      breadcrumbs: String(doc.breadcrumbs ?? ""),
      body: String(doc.body ?? ""),
    };
  });
}

export function createSearchIndexScript(documents) {
  const json = JSON.stringify({ docs: documents })
    .replace(/\u2028/g, "\\u2028")
    .replace(/\u2029/g, "\\u2029");
  return `window.bookCnSearchIndex = ${json};\n`;
}

export async function buildSearchIndex(bookDirectory) {
  const fileNames = await readdir(bookDirectory);
  const searchIndexName = findSearchIndexName(fileNames);
  const searchIndexPath = path.join(bookDirectory, searchIndexName);
  const source = await readFile(searchIndexPath, "utf8");
  const config = parseSearchIndex(source, searchIndexPath);
  const documents = extractSearchDocuments(config);
  const outputPath = path.join(bookDirectory, "search-zh-index.js");
  await writeFile(outputPath, createSearchIndexScript(documents), "utf8");

  return {
    documents,
    outputPath,
    searchIndexPath,
  };
}

async function main() {
  const directoryArgument = process.argv[2] || "book";
  const bookDirectory = path.resolve(process.cwd(), directoryArgument);
  const result = await buildSearchIndex(bookDirectory);
  console.log(
    `已生成 ${result.outputPath}，来源为 ${path.basename(result.searchIndexPath)}，共 ${result.documents.length} 个搜索文档。`,
  );
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
}

(function (global) {
  "use strict";

  const HAN_CHAR_PATTERN = /[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/;
  const QUERY_TOKEN_PATTERN = /[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+|[a-z0-9_]+/gi;
  const DEFAULT_RESULT_LIMIT = 30;

  function normalizeText(value) {
    const text = String(value ?? "");
    const normalized = typeof text.normalize === "function" ? text.normalize("NFKC") : text;
    return normalized.toLocaleLowerCase();
  }

  function hasHan(value) {
    return HAN_CHAR_PATTERN.test(String(value ?? ""));
  }

  function tokenizeQuery(query) {
    return [...new Set(normalizeText(query).match(QUERY_TOKEN_PATTERN) || [])];
  }

  function countOccurrences(text, term) {
    if (!term) {
      return 0;
    }

    let count = 0;
    let offset = 0;
    while (offset < text.length) {
      const index = text.indexOf(term, offset);
      if (index === -1) {
        break;
      }
      count += 1;
      offset = index + term.length;
    }
    return count;
  }

  function searchDocuments(documents, query, limit = DEFAULT_RESULT_LIMIT) {
    const terms = tokenizeQuery(query);
    if (terms.length === 0 || !Array.isArray(documents)) {
      return [];
    }

    const results = [];
    for (const doc of documents) {
      const title = normalizeText(doc.title);
      const breadcrumbs = normalizeText(doc.breadcrumbs);
      const body = normalizeText(doc.body);
      let score = 0;
      let allTermsMatched = true;

      for (const term of terms) {
        const titleHits = countOccurrences(title, term);
        const breadcrumbHits = countOccurrences(breadcrumbs, term);
        const bodyHits = countOccurrences(body, term);
        const totalHits = titleHits + breadcrumbHits + bodyHits;

        if (totalHits === 0) {
          allTermsMatched = false;
          break;
        }

        score += Math.min(titleHits, 3) * 1000;
        score += Math.min(breadcrumbHits, 5) * 200;
        score += Math.min(bodyHits, 5) * 8;
        score += term.length;
      }

      if (allTermsMatched) {
        results.push({ doc, score });
      }
    }

    const resultLimit = Number.isFinite(limit) ? Math.max(0, Math.floor(limit)) : DEFAULT_RESULT_LIMIT;
    return results
      .sort((left, right) => {
        const scoreDifference = right.score - left.score;
        if (scoreDifference !== 0) {
          return scoreDifference;
        }
        return normalizeText(left.doc.title).localeCompare(normalizeText(right.doc.title));
      })
      .slice(0, resultLimit);
  }

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (character) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    })[character]);
  }

  function escapeRegExp(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function makeTeaser(body, query, maxLength = 220) {
    const rawBody = String(body ?? "");
    if (!rawBody) {
      return "";
    }

    const terms = tokenizeQuery(query).sort((left, right) => right.length - left.length);
    const normalizedBody = normalizeText(rawBody);
    const matchIndex = terms.reduce((bestIndex, term) => {
      const currentIndex = normalizedBody.indexOf(term);
      if (currentIndex === -1) {
        return bestIndex;
      }
      return bestIndex === -1 ? currentIndex : Math.min(bestIndex, currentIndex);
    }, -1);

    const length = Number.isFinite(maxLength) ? Math.max(40, Math.floor(maxLength)) : 220;
    const anchor = matchIndex === -1 ? 0 : matchIndex;
    const start = Math.max(0, anchor - Math.floor(length * 0.35));
    const end = Math.min(rawBody.length, start + length);
    let teaser = escapeHtml(rawBody.slice(start, end));

    if (terms.length > 0) {
      const pattern = terms.map(escapeRegExp).join("|");
      teaser = teaser.replace(new RegExp(`(${pattern})`, "giu"), "<em>$1</em>");
    }

    return `${start > 0 ? "…" : ""}${teaser}${end < rawBody.length ? "…" : ""}`;
  }

  const api = {
    hasHan,
    normalizeText,
    tokenizeQuery,
    searchDocuments,
    makeTeaser,
  };

  global.bookCnSearch = api;

  if (!global.document) {
    return;
  }

  let indexPromise = null;
  let lastQuery = "";

  function pathToRoot() {
    return typeof global.path_to_root === "string" ? global.path_to_root : "";
  }

  function getSearchBar() {
    return global.document.getElementById("mdbook-searchbar");
  }

  function getCurrentQuery() {
    return new URL(global.location.href).searchParams.get("search") || "";
  }

  function updateSearchUrl(query) {
    const url = new URL(global.location.href);
    if (url.searchParams.get("search") === query) {
      return;
    }

    if (query) {
      url.searchParams.set("search", query);
      url.searchParams.delete("highlight");
      url.hash = "";
    } else {
      url.searchParams.delete("search");
      url.searchParams.delete("highlight");
    }

    global.history.replaceState({}, global.document.title, url.href);
  }

  function loadIndex() {
    if (global.bookCnSearchIndex && Array.isArray(global.bookCnSearchIndex.docs)) {
      return Promise.resolve(global.bookCnSearchIndex);
    }
    if (indexPromise) {
      return indexPromise;
    }

    indexPromise = new Promise((resolve, reject) => {
      const script = global.document.createElement("script");
      script.src = `${pathToRoot()}search-zh-index.js`;
      script.async = true;
      script.onload = () => {
        if (global.bookCnSearchIndex && Array.isArray(global.bookCnSearchIndex.docs)) {
          resolve(global.bookCnSearchIndex);
        } else {
          reject(new Error("中文搜索索引格式无效"));
        }
      };
      script.onerror = () => reject(new Error("中文搜索索引加载失败"));
      global.document.head.appendChild(script);
    });
    return indexPromise;
  }

  function resultHref(doc, query) {
    const [file, anchor = ""] = String(doc.url || "").split("#", 2);
    const highlight = encodeURIComponent(query).replace(/'/g, "%27");
    return `${pathToRoot()}${file}?highlight=${highlight}${anchor ? `#${anchor}` : ""}`;
  }

  function clearResults(results) {
    while (results.firstChild) {
      results.removeChild(results.firstChild);
    }
  }

  function renderResults(query, results) {
    const header = global.document.getElementById("mdbook-searchresults-header");
    const list = global.document.getElementById("mdbook-searchresults");
    const listOuter = global.document.getElementById("mdbook-searchresults-outer");
    if (!header || !list || !listOuter) {
      return;
    }

    header.textContent = results.length > 0
      ? `找到 ${results.length} 个结果：`
      : `没有找到“${query}”的结果。`;
    clearResults(list);

    results.forEach(({ doc }, index) => {
      const item = global.document.createElement("li");
      const link = global.document.createElement("a");
      const teaser = global.document.createElement("span");
      link.href = resultHref(doc, query);
      link.textContent = doc.breadcrumbs || doc.title || doc.url;
      teaser.className = "teaser";
      teaser.id = `mdbook-cn-teaser_${index + 1}`;
      teaser.setAttribute("aria-label", "搜索结果摘要");
      teaser.innerHTML = makeTeaser(doc.body, query);
      item.append(link, teaser);
      list.appendChild(item);
    });

    listOuter.classList.remove("hidden");
  }

  function renderError(message) {
    const header = global.document.getElementById("mdbook-searchresults-header");
    const list = global.document.getElementById("mdbook-searchresults");
    const listOuter = global.document.getElementById("mdbook-searchresults-outer");
    if (!header || !list || !listOuter) {
      return;
    }

    header.textContent = message;
    clearResults(list);
    listOuter.classList.remove("hidden");
  }

  function runSearch(query) {
    const outer = global.document.getElementById("mdbook-searchbar-outer");
    if (outer) {
      outer.classList.add("searching");
    }

    return loadIndex()
      .then((index) => {
        if (getSearchBar()?.value.trim() !== query) {
          return;
        }
        const results = searchDocuments(index.docs, query);
        renderResults(query, results);
      })
      .catch((error) => {
        console.error(error);
        renderError("中文搜索索引加载失败，请刷新页面重试。");
      })
      .finally(() => {
        if (outer) {
          outer.classList.remove("searching");
        }
      });
  }

  function handleSearchEvent(event) {
    if (event.isComposing) {
      return;
    }

    const searchbar = getSearchBar();
    const query = searchbar?.value.trim() || "";
    if (!hasHan(query)) {
      return;
    }

    event.stopImmediatePropagation();
    if (event.type === "keyup") {
      event.preventDefault();
    }
    searchbar.classList.add("active");
    updateSearchUrl(query);
    if (query !== lastQuery) {
      lastQuery = query;
      runSearch(query);
    }
  }

  function handleHistoryNavigation() {
    const searchbar = getSearchBar();
    const query = getCurrentQuery();
    if (!searchbar || !hasHan(query)) {
      return;
    }

    searchbar.value = query;
    searchbar.classList.add("active");
    lastQuery = query;
    runSearch(query);
  }

  function setupBrowserSearch() {
    const searchbar = getSearchBar();
    if (!searchbar || searchbar.dataset.bookCnSearch === "true") {
      return;
    }

    searchbar.dataset.bookCnSearch = "true";
    searchbar.addEventListener("input", handleSearchEvent, true);
    searchbar.addEventListener("keyup", handleSearchEvent, true);
    searchbar.addEventListener("compositionend", handleSearchEvent, true);
    global.addEventListener("popstate", handleHistoryNavigation);

    const query = getCurrentQuery();
    if (hasHan(query)) {
      searchbar.value = query;
      searchbar.classList.add("active");
      const wrapper = global.document.getElementById("mdbook-search-wrapper");
      if (wrapper) {
        wrapper.classList.remove("hidden");
      }
      lastQuery = query;
      global.setTimeout(() => runSearch(query), 0);
    }
  }

  if (global.document.readyState === "loading") {
    global.document.addEventListener("DOMContentLoaded", setupBrowserSearch);
  } else {
    setupBrowserSearch();
  }
})(typeof globalThis === "undefined" ? window : globalThis);

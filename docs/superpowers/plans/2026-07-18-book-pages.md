# Implementation Plan: GitHub Pages for `book-cn`

## 1. Add the Pages workflow

- Create `.github/workflows/pages.yml`.
- Keep the existing `main.yml` CI workflow unchanged.
- Build with the repository's Rust 1.97 and mdBook 0.5.1 versions.
- Upload `./book` and deploy it through the GitHub Pages environment.

## 2. Update reader-facing documentation

- Add the Pages URL to `README.zh-CN.md`.
- Explain that pushes to `main` trigger deployment.
- Retain the local `mdbook build` and `mdbook serve` instructions.

## 3. Verify and publish

- Run `mdbook build`, translation checks, and `git diff --check`.
- Inspect the final diff and commit only the Pages change.
- Push the commit to `AreChen/book-cn`.
- Enable Pages with the workflow source and verify the deployment URL.

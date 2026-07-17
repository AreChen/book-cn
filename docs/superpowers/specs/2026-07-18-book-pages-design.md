# Design: Publish the Chinese Rust Book with GitHub Pages

**Date:** 2026-07-18  
**Status:** Approved

## Context

`book-cn` already builds a complete Chinese mdBook locally, but the repository has no public preview site. The existing CI workflow tests the book and translation without publishing the generated `book/` directory.

## Goals

- Publish the generated Chinese book at `https://arechen.github.io/book-cn/`.
- Rebuild automatically after changes to `main`.
- Keep generated HTML out of the source tree and retain the existing test workflow.
- Document the online site and local preview command.

## Decision

Add a dedicated `.github/workflows/pages.yml` workflow using the official GitHub Pages Actions flow:

1. Check out `main`.
2. Install Rust 1.97 and the pinned mdBook 0.5.1 tool.
3. Run `mdbook build`, including the repository's custom preprocessors.
4. Upload `book/` as a Pages artifact.
5. Deploy the artifact with `actions/deploy-pages`.

The workflow will run on pushes to `main` and manual dispatches. It will grant only `contents: read`, `pages: write`, and `id-token: write`, and use a single `pages` concurrency group so an older deployment cannot overwrite a newer one.

## Alternatives considered

- A committed `gh-pages` branch would work, but would add generated artifacts and a second branch to maintain.
- A documentation-only change would leave the user responsible for configuring and rebuilding Pages manually.

## Verification

- Run the existing mdBook build locally.
- Validate translation and whitespace checks.
- Check the workflow file for the expected Pages permissions, build artifact path, and deployment job.
- Enable the repository's Pages source as `workflow` and verify the published URL after the workflow completes.

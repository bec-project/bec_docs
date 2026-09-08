# Repository Guidelines — `bec_docs`

`bec_docs` is the unified BEC documentation repository. The site is built with **Zensical**,
configured in `zensical.toml`, and its content must remain compatible with **Diátaxis**.
Prefer focused documentation changes, follow nearby page conventions, and validate the smallest
relevant scope.

## Scope

These instructions apply to the whole `bec_docs` workspace.

## Project Overview

- This repository contains the BEC documentation site.
- It combines the documentation for three repositories:
  - `bec` (the main BEC codebase): https://github.com/bec-project/bec
  - `ophyd_devices` (ophyd device components for BEC): https://github.com/bec-project/ophyd_devices
  - `bec_widgets` (BEC-specific widgets for the UI): https://github.com/bec-project/bec_widgets
- Main documentation sources live under `docs/`.
- Navigation is configured in `zensical.toml`.
- Treat `pyproject.toml` as the source of truth for dependencies and Python tooling.

## Core Rules

- Use Zensical for site builds; do not introduce a parallel MkDocs or Sphinx configuration.
- Give each page a clear Diátaxis purpose: tutorial, how-to guide, explanation, or reference.
- Verify documented APIs, commands, and defaults against the relevant source repository. Do not
  invent behavior or present unreleased features as available in released versions.
- Keep diffs focused and preserve user changes outside the requested scope.
- Discuss larger structural changes before implementing them.
- Do not commit, push, or open PRs unless explicitly asked.

## First Read

- `zensical.toml` — navigation, theme, Markdown extensions, and API reference configuration
- `pyproject.toml` — dependencies, package configuration, and development tools
- neighboring pages in the relevant documentation section — tone, front matter, and markup patterns
- `src/bec_docs_pymdown_extensions/` — custom Markdown extensions and snippet handling
- `tests/extension_tests/` — unit tests for the documentation extensions
- `tests/snippet_tests/` — executable documentation examples and integration fixtures
- `.github/workflows/gh_pages_deploy.yml` — site build and publication workflow

## Local Overlay

If `AGENTS_PERSONAL.md` exists beside this file, treat it as an extension of this file.
Machine-specific environment and workflow instructions there take precedence over the generic
guidance here. Do not assume the overlay exists or copy its machine-specific details into shared
documentation. Keep it local and do not commit it.

## Repo Layout And Diátaxis

- `docs/getting-started/` — tutorials: guide a new user through a concrete learning experience.
  Provide enough explanation to follow the workflow, keeping advanced options and API detail out
  of the main path.
- `docs/how-to/` — how-to guides: solve a specific task for a reader who already knows the basics.
  State prerequisites, give concise actionable steps, and link to explanations for deeper context.
- `docs/learn/` — explanations: develop understanding of concepts, design choices, and tradeoffs.
- `docs/references/` — reference: provide precise, consistently structured API and technical details
  that readers can look up without following a narrative.
- `docs/assets/` and page-local asset directories — images and supporting files
- `docs/stylesheets/` — site styling
- `src/bec_docs_pymdown_extensions/` — Python package supporting documentation rendering
- `tests/` — extension and documentation-example validation

Choose the section by the reader's need, not simply the topic. A feature may have pages in multiple
sections; cross-link them instead of combining a tutorial, task guide, explanation, and complete API
listing into one page. Preserve the existing directory and navigation structure.

## Editing Guidelines

- Follow the Diátaxis section guidance above when adding or editing pages.
- Prefer small, focused documentation edits that preserve the existing structure and tone.
- Match the wording and formatting already used in nearby pages.
- When adding tables that need fixed column widths, prefer inline HTML tables over Markdown tables.
- Keep links relative and consistent with the surrounding docs.
- Do not remove or overwrite user changes outside the requested scope.
- If you need to make a larger structural change, please discuss it first before implementing.

## Admonitions

- Getting-started / tutorial pages must start with `!!! info "Goal"` stating the learning outcomes
  and end with `!!! success "What you have learned"` summarizing the key takeaways.
- How-to pages must start with `!!! info "Overview"` explaining the purpose of the page and end
  with `!!! success "Congratulations!"` celebrating completion of the task.
- Learning pages must provide a `!!! info "What to remember"` for end-of-page takeaways.

## Content Conventions

- Use sentence case in prose and keep headings consistent with neighboring pages.
- Prefer short examples that reflect real BEC usage.
- When appropriate, add related links to other documentation pages at the top of the page in a `related` section.
- Preserve relevant front matter and existing snippet identifiers when editing a page; check their
  consumers before renaming or removing them.
- Use Markdown extensions and tab syntax already configured in `zensical.toml` and used nearby.
  Do not assume that a MkDocs plugin or theme feature works with Zensical without validation.
- Edit source Markdown, assets, or extensions rather than generated output under `site/`.

## Common Task Routing

- New or moved pages: select the Diátaxis section, update navigation where appropriate, and check
  incoming links and related-page references.
- API reference changes: inspect the corresponding `bec`, `ophyd_devices`, or `bec_widgets` source
  and the mkdocstrings configuration in `zensical.toml`.
- Runnable examples: check the matching tests under `tests/snippet_tests/` and keep examples and
  expected outputs aligned.
- Markdown extension changes: add or update focused regression tests in `tests/extension_tests/`
  and check the rendered output.
- Product behavior changes belong in the relevant source repository; this repository documents
  that behavior.

## Local Development

Python 3.11+ is required. Install the documentation package and development dependencies from this
checkout:

```bash
python -m pip install -e '.[dev]'
zensical serve
```

Build the site using the same command as the deployment workflow:

```bash
zensical build
```

API rendering depends on the Python source paths configured under the mkdocstrings handler in
`zensical.toml`. Check those paths against the available sibling checkouts before diagnosing missing
imports; do not assume local checkout names match the configuration or commit machine-specific paths.

## Validation

- If you change navigation-relevant docs, check whether `zensical.toml` also needs an update.
- If you delete or merge pages, update internal links so no stale references remain.
- When practical, verify links and references with fast text searches before finishing.
- Build with `zensical build` for page, navigation, theme, or rendering changes when practical.
  Inspect affected pages visually when changing layout, tabs, admonitions, tables, or images.
- For custom extension changes, run the focused test first, then the extension suite as appropriate:

  ```bash
  python -m pytest tests/extension_tests
  ```

- Snippet integration tests require BEC and related dependencies and services. Consult
  `.github/actions/bec_e2e_snippet_tests/action.yml` and the existing fixtures for setup, then run
  the relevant test target. Do not start a broad service or GUI test run for prose-only changes.
- For agent-instruction-only changes, check paths, commands, and consistency; a site build is not
  required.
- Report what changed, what was validated, and any validation that could not be completed.

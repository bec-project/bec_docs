# Codex Instructions

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
- The site is built with Zensical and follows a diataxis structure.

## Editing Guidelines

- Follow the diataxis structure when adding or editing pages: 
  - Getting Started: high-level tutorials for new users, focused on teaching concepts and workflows without overwhelming details and lots of explanations. 
  - How-To: focused guides for specific tasks. Should be concise and practical, with just enough explanation to understand the steps. Reference learning pages for deeper dives into concepts. A user coming back to the how-to page should not be bombarded with information that is not directly relevant to the task at hand.
  - Learning: in-depth explanations of concepts and features
  - Reference: API documentation and technical details, treated as a lookup resource rather than a narrative
- Prefer small, focused documentation edits that preserve the existing structure and tone.
- Match the wording and formatting already used in nearby pages.
- When adding tables that need fixed column widths, prefer inline HTML tables over Markdown tables.
- Keep links relative and consistent with the surrounding docs.
- Do not remove or overwrite user changes outside the requested scope.
- If you need to make a larger structural change, please discuss it first before implementing.

## Admonitions
- Getting-started / tutorial pages must start with a info admonition "Goal" that clearly states the learning outcomes for the page and end with a success admonition "What you have learned" that summarizes the key takeaways.
- How-to pages must start with an info admonition "Overview" that explains the purpose of the page and end with a success admonition "Congratulations!" that celebrates the completion of the task.
- Learning pages must provide a `!!! info "What to remember"` for end-of-page takeaways.

## Content Conventions

- Use sentence case in prose and keep headings consistent with neighboring pages.
- Prefer short examples that reflect real BEC usage.
- When appropriate, add related links to other documentation pages at the top of the page in a `related` section.

## Validation

- If you change navigation-relevant docs, check whether `zensical.toml` also needs an update.
- If you delete or merge pages, update internal links so no stale references remain.
- When practical, verify links and references with fast text searches before finishing.

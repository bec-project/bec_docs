"""Build the docs search index that the BEC MCP server (bec_mcp_server) searches with BM25.

The Pages deploy runs this after ``zensical build`` and publishes the result next to the site, as
``bec_docs_index.json.gz``; the MCP server loads it from that URL (``--docs-index``). The index
stores the parsed pages of the site navigation only; the server computes its BM25 state when it
loads the file, so the format stays small and independent of the scoring code.

This file uses only the standard library and is kept in step with
``bec_mcp_server/docs/build.py``, which owns the format (``format``/``schema_version`` below).

    python tools/build_mcp_docs_index.py . --name bec_docs --output site/bec_docs_index.json.gz
"""

from __future__ import annotations

import argparse
import ast
import gzip
import json
import os
import re
import subprocess
import tomllib
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from textwrap import dedent
from typing import Any

#: identifies the file as a BEC docs index; bumped on incompatible format changes
INDEX_FORMAT = "bec-docs-index"
SCHEMA_VERSION = 1

# links/images may carry an attached pymdown attr list: [Title](url){ data-preview }
_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)(?:\{[^{}\n]*\})?")
_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]+\)(?:\{[^{}\n]*\})?")
_TAG_RE = re.compile(r"<[^>]+>")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
_INLINE_CODE_RE = re.compile(r"`([^`]+)`")
_ATTR_LIST_RE = re.compile(r"\s*\{[^{}\n]*\}\s*$")
_FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
# mkdocstrings autodoc directive (`::: package.module.Object`) and its indented options; the
# rendered API text is not in the markdown, so the directive is dropped rather than indexed
_AUTODOC_RE = re.compile(r"^(\s*):::\s+\S")

# bec_docs embeds tested, runnable code snippets via a custom pymdown preprocessor; the
# directive line references a test function in <repo>/tests/snippet_tests/ (see
# bec_docs/src/bec_docs_pymdown_extensions/snippet_preprocessor.py). We resolve it the same
# way so the actual commands each tutorial teaches end up in the index.
_SNIPPET_RE = re.compile(r"(\s*)--\[\]->\[\]--test_snippet--(.*)")
_SNIPPET_SUBDIR = Path("tests") / "snippet_tests"
_DOCS_DISPLAY_RE = re.compile(r"^(?P<indent>\s*)print\((?P<expr>.+)\)\s*#\s*docs-display\s*$")
_DOCS_HIDE_RE = re.compile(r"^\s*.*#\s*docs-hide\s*$")


def _strip_front_matter(text: str) -> str:
    if not text.startswith("---\n"):
        return text

    marker = "\n---\n"
    end = text.find(marker, 4)
    if end == -1:
        return text
    return text[end + len(marker) :]


def _strip_markdown_line(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("!!! ") or stripped.startswith("??? "):
        parts = stripped.split(maxsplit=2)
        if len(parts) == 3:
            # titles may contain markdown links/attr-lists, strip them like any other line
            return _strip_markdown_line(parts[2].strip('"'))
        # a bare admonition keyword ("??? tip") is markup, not content
        return ""

    if stripped.startswith("==="):
        # content-tab marker: keep the quoted title, drop the marker itself
        tab_title = re.match(r'^===\+?\s+"([^"]*)"\s*$', stripped)
        return tab_title.group(1) if tab_title else ""

    # pymdown "blocks" syntax: `/// tab | Title` opens a block, `///` closes it
    if stripped.startswith("///"):
        if "|" in stripped:
            return stripped.split("|", 1)[1].strip()
        return ""

    text = _IMAGE_RE.sub(r"\1", line)
    text = _LINK_RE.sub(r"\1", text)
    text = _INLINE_CODE_RE.sub(r"\1", text)
    text = _TAG_RE.sub(" ", text)
    text = _ATTR_LIST_RE.sub("", text)
    text = text.replace("|", " ")
    text = re.sub(r"^\s*[-*+]\s+", "", text)
    text = re.sub(r"^\s*\d+\.\s+", "", text)
    text = re.sub(r"^\s*>\s?", "", text)
    text = re.sub(r"\s+", " ", text)
    return unescape(text.strip())


def _clean_heading(text: str) -> str:
    # unlike body lines, headings keep their leading ordinals ("## 1. Check ...") so that
    # section lookups by the published heading text succeed
    cleaned = _IMAGE_RE.sub(r"\1", text)
    cleaned = _LINK_RE.sub(r"\1", cleaned)
    cleaned = _INLINE_CODE_RE.sub(r"\1", cleaned)
    cleaned = _TAG_RE.sub(" ", cleaned)
    cleaned = _ATTR_LIST_RE.sub("", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return unescape(cleaned).strip("# ").strip()


def _doc_url(site_url: str | None, relative_path: str) -> str | None:
    if not site_url:
        return None
    return f"{site_url.rstrip('/')}/{relative_path.removesuffix('.md')}.html"


def _nav_paths(nav: Any) -> set[str]:
    """Collect the page paths of a zensical/mkdocs nav tree."""
    if isinstance(nav, str):
        return {nav}
    if isinstance(nav, dict):
        nav = list(nav.values())
    if isinstance(nav, list):
        return set().union(*(_nav_paths(item) for item in nav))
    return set()


def _read_docs_project_config(repo_path: Path) -> tuple[Path, str | None, set[str] | None]:
    """Return the docs directory, the site URL and the nav page paths (None without a nav)."""
    zensical_path = repo_path / "zensical.toml"
    docs_dir = repo_path / "docs"
    site_url = None
    nav = None
    if zensical_path.exists():
        with zensical_path.open("rb") as stream:
            config = tomllib.load(stream)
        project = config.get("project", {})
        docs_dir = repo_path / project.get("docs_dir", "docs")
        site_url = project.get("site_url")
        if project.get("nav"):
            nav = _nav_paths(project["nav"])
    return docs_dir, site_url, nav


def _git_commit(repo_path: Path) -> str | None:
    """Short commit of the docs checkout, suffixed with -dirty for uncommitted changes."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    commit = result.stdout.strip()
    if result.returncode != 0 or not commit:
        return None
    try:
        status = subprocess.run(
            ["git", "-C", str(repo_path), "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return commit
    # a dirty tree means the indexed content may not match the recorded commit
    if status.returncode == 0 and status.stdout.strip():
        return f"{commit}-dirty"
    return commit


def _resolve_snippet(snippet_dir: Path, spec: str) -> list[str] | None:
    """Resolve a test_snippet directive to its caption + code lines, or None."""
    parts = spec.split(":")
    if len(parts) != 3:
        return None
    file_name, test_name, caption = parts
    snippet_path = snippet_dir / file_name
    if not snippet_path.is_file():
        return None
    try:
        file_text = snippet_path.read_text(encoding="utf-8")
        tree = ast.parse(file_text)
    except (OSError, SyntaxError, ValueError):
        return None

    function = next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == test_name
        ),
        None,
    )
    if function is None or function.end_lineno is None:
        return None

    code = dedent("\n".join(file_text.splitlines()[function.lineno : function.end_lineno]))
    code_lines: list[str] = []
    for line in code.splitlines():
        if _DOCS_HIDE_RE.match(line):
            continue
        display_match = _DOCS_DISPLAY_RE.match(line)
        if display_match:
            code_lines.append(f"{display_match.group('indent')}{display_match.group('expr')}")
        else:
            code_lines.append(line)
    return [caption.strip(), *code_lines]


def _closes_fence(stripped: str, open_fence: str) -> bool:
    # per CommonMark a code block only closes on the same fence char, at least as long
    fence_match = _FENCE_RE.match(stripped)
    return (
        fence_match is not None
        and stripped == fence_match.group(1)
        and fence_match.group(1)[0] == open_fence[0]
        and len(fence_match.group(1)) >= len(open_fence)
    )


def _split_sections(text: str, snippet_dir: Path | None) -> tuple[str | None, list[dict[str, Any]]]:
    """Split markdown into sections at its headings; returns the first H1 and the sections."""
    title: str | None = None
    sections: list[dict[str, Any]] = []
    heading: str | None = None
    level = 1
    # (line, keep_verbatim): verbatim lines are code and skip markdown stripping
    lines: list[tuple[str, bool]] = []
    # the fence string that opened the current code block (None outside code blocks)
    open_fence: str | None = None

    def flush_section() -> None:
        cleaned = [line if verbatim else _strip_markdown_line(line) for line, verbatim in lines]
        lines.clear()
        section_text = "\n".join(line for line in cleaned if line.strip()).strip()
        if section_text:
            sections.append({"heading": heading, "level": level, "text": section_text})

    # indentation of the autodoc directive being skipped (None outside one)
    autodoc_indent: int | None = None

    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if autodoc_indent is not None:
            indent = len(raw_line) - len(raw_line.lstrip())
            if stripped and indent > autodoc_indent:
                continue
            autodoc_indent = None
        autodoc_match = _AUTODOC_RE.match(raw_line) if open_fence is None else None
        if autodoc_match:
            autodoc_indent = len(autodoc_match.group(1))
            continue
        if open_fence is not None:
            if _closes_fence(stripped, open_fence):
                open_fence = None
            else:
                lines.append((raw_line, True))
            continue

        fence_match = _FENCE_RE.match(stripped)
        if fence_match:
            open_fence = fence_match.group(1)
            continue

        snippet_match = _SNIPPET_RE.match(raw_line)
        if snippet_match:
            # unresolvable directives are dropped, never indexed as junk
            resolved = (
                _resolve_snippet(snippet_dir, snippet_match.group(2)) if snippet_dir else None
            )
            lines.extend((line, True) for line in resolved or [])
            continue

        heading_match = _HEADING_RE.match(raw_line)
        if heading_match:
            flush_section()
            level = len(heading_match.group(1))
            heading = _clean_heading(heading_match.group(2))
            if level == 1 and heading and title is None:
                title = heading
            continue

        lines.append((raw_line, False))

    flush_section()
    return title, sections


def parse_markdown_page(
    path: Path, *, docs_dir: Path, site_url: str | None, snippet_dir: Path | None = None
) -> dict[str, Any]:
    """
    Parse one markdown page into its title and sections.

    Fenced code blocks are kept verbatim, because for developer docs the code is often the most
    valuable content; test_snippet directives are resolved to the referenced snippet code.

    Args:
        path (Path): The markdown file.
        docs_dir (Path): The docs root; page paths are relative to it.
        site_url (str | None): Base URL of the published site, used for page links.
        snippet_dir (Path | None): Directory holding the tested snippets.

    Returns:
        dict[str, Any]: The page with path, title, url and sections.
    """
    relative_path = path.relative_to(docs_dir).as_posix()
    text = _strip_front_matter(path.read_text(encoding="utf-8"))
    title, sections = _split_sections(text, snippet_dir)
    return {
        "path": relative_path,
        "title": title or path.stem.replace("-", " ").title(),
        "url": _doc_url(site_url, relative_path),
        "sections": sections,
    }


def parse_markdown_docs(repo_path: Path, *, site_url: str | None = None) -> list[dict[str, Any]]:
    """
    Parse the markdown pages of a documentation repository.

    When zensical.toml defines a nav, only the pages listed in it are parsed.

    Args:
        repo_path (Path): The repository root (holding zensical.toml and the docs directory).
        site_url (str | None): Override for the site URL from zensical.toml.

    Returns:
        list[dict[str, Any]]: The parsed pages, sorted by path.
    """
    docs_dir, config_site_url, nav = _read_docs_project_config(repo_path)
    if not docs_dir.exists():
        raise FileNotFoundError(f"Docs directory not found: {docs_dir}")

    pages: list[dict[str, Any]] = []
    for path in sorted(docs_dir.rglob("*.md")):
        if path.is_dir():
            continue
        relative = path.relative_to(docs_dir)
        if any(part.startswith(".") for part in relative.parts):
            continue
        # pages left out of the site navigation are drafts and placeholders; an agent must
        # not quote them as published documentation
        if nav is not None and relative.as_posix() not in nav:
            continue
        pages.append(
            parse_markdown_page(
                path,
                docs_dir=docs_dir,
                site_url=site_url or config_site_url,
                snippet_dir=repo_path / _SNIPPET_SUBDIR,
            )
        )
    return pages


def build_docs_index(
    repo_path: Path | str,
    output_path: Path | str,
    *,
    site_url: str | None = None,
    name: str | None = None,
) -> dict[str, Any]:
    """
    Build the docs index JSON from one documentation repository.

    An output path ending in .gz is written gzip-compressed. The file is replaced atomically,
    because running servers reload it when its mtime changes.

    Args:
        repo_path (Path | str): The documentation repository, e.g. a bec_docs checkout.
        output_path (Path | str): Where to write the index (.json or .json.gz).
        site_url (str | None): Override for the site URL from zensical.toml.
        name (str | None): Source name recorded in the index; defaults to the repo folder name.

    Returns:
        dict[str, Any]: The index payload that was written.
    """
    repo_path = Path(repo_path).expanduser().resolve()
    output_path = Path(output_path).expanduser()
    _, config_site_url, _ = _read_docs_project_config(repo_path)
    pages = parse_markdown_docs(repo_path, site_url=site_url)
    pages = [page for page in pages if page["sections"]]
    if not pages:
        raise RuntimeError(f"No searchable sections found in {repo_path}")

    payload = {
        "format": INDEX_FORMAT,
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": {
            "name": name or repo_path.name,
            "git_commit": _git_commit(repo_path),
            "site_url": site_url or config_site_url,
        },
        "page_count": len(pages),
        "pages": pages,
    }
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if output_path.suffix == ".gz":
        # mtime=0 keeps the compressed bytes reproducible for the same content
        data = gzip.compress(data, mtime=0)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = output_path.with_name(f".{output_path.name}.tmp")
    tmp_path.write_bytes(data)
    os.replace(tmp_path, output_path)
    return payload


def main(argv: list[str] | None = None) -> None:
    """Command-line entry point: build the index from a bec_docs checkout."""
    parser = argparse.ArgumentParser(description="Build the BEC documentation search index.")
    parser.add_argument("docs_repo", type=Path, help="Path to a bec_docs checkout.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("bec_docs_index.json.gz"),
        help="Output file; a .gz suffix writes it gzip-compressed (default: %(default)s).",
    )
    parser.add_argument("--site-url", default=None, help="Override the site URL for page links.")
    parser.add_argument(
        "--name", default=None, help="Source name recorded in the index (default: folder name)."
    )
    args = parser.parse_args(argv)
    payload = build_docs_index(args.docs_repo, args.output, site_url=args.site_url, name=args.name)
    source = payload["source"]
    print(
        f"Wrote {payload['page_count']} pages from {source['name']}@"
        f"{source['git_commit'] or 'unknown'} to {args.output}"
    )


if __name__ == "__main__":
    main()

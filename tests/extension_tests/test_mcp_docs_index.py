"""The docs search index for the BEC MCP server, built from this repository by the Pages deploy."""

import gzip
import importlib.util
import json
import tomllib
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location(
    "build_mcp_docs_index", REPO / "tools" / "build_mcp_docs_index.py"
)
builder = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(builder)


@pytest.fixture(scope="module")
def index(tmp_path_factory):
    output = tmp_path_factory.mktemp("index") / "bec_docs_index.json.gz"
    builder.build_docs_index(REPO, output, name="bec_docs")
    return json.loads(gzip.decompress(output.read_bytes()))


def _nav_pages():
    with (REPO / "zensical.toml").open("rb") as stream:
        return builder._nav_paths(tomllib.load(stream)["project"]["nav"])


def test_index_has_the_format_the_mcp_server_reads(index):
    assert index["format"] == "bec-docs-index"
    assert index["schema_version"] == 1
    assert index["source"]["name"] == "bec_docs"
    assert index["source"]["site_url"].startswith("https://")
    assert index["page_count"] == len(index["pages"]) > 0


def test_index_holds_only_pages_of_the_site_navigation(index):
    assert {page["path"] for page in index["pages"]} <= _nav_pages()


def test_index_text_carries_no_directives(index):
    text = json.dumps(index)
    assert "test_snippet" not in text
    assert ":::" not in text


def test_tested_snippets_are_resolved_into_the_index(index):
    assert "scans.line_scan(" in json.dumps(index)


def test_autodoc_directive_and_its_options_are_dropped(tmp_path):
    page = tmp_path / "page.md"
    page.write_text(
        "# API\n\nBefore the class.\n\n"
        "::: bec_server.scan_server.scans.scan_base.ScanBase\n"
        "    options:\n"
        "      show_root_heading: false\n\n"
        "After the class.\n"
    )

    parsed = builder.parse_markdown_page(page, docs_dir=tmp_path, site_url=None)

    assert parsed["sections"] == [
        {"heading": "API", "level": 1, "text": "Before the class.\nAfter the class."}
    ]

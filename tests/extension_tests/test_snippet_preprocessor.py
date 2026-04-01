from pathlib import Path
from unittest.mock import patch

import pytest

import bec_docs_pymdown_extensions.snippet_preprocessor as snippet_extension

from .preprocessor_test_data import INCLUDED_VALUE


@pytest.fixture()
def preprocessor_module():
    with (
        patch.object(snippet_extension, "TEST_SNIPPET_DIR", Path(__file__).parent),
        patch.object(
            snippet_extension,
            "_F_STRING_TOKENS",
            {
                "INCLUDED_VALUE": INCLUDED_VALUE,
                "PLACEHOLDER_TOKEN": snippet_extension.PLACEHOLDER_TOKEN,
            },
        ),
    ):
        yield snippet_extension


def test_transform_with_f_string(preprocessor_module):
    in_lines = [
        "a",
        "--[]->[]--test_snippet--preprocessor_test_data.py:transform_with_f_string:transform with f-string",
        "b",
    ]
    out_lines = preprocessor_module._transform_lines(in_lines)
    expected_lines = [
        "a",
        "/// tab | :material-import: transform with f-string",
        "```python",
        "code = 1",
        "```",
        "///",
        "/// tab | :material-export: output",
        "```",
        "interpolated f-string",
        "```",
        "///",
        "b",
    ]
    assert out_lines == expected_lines


def test_transform_with_constant_string(preprocessor_module):
    in_lines = [
        "a",
        "--[]->[]--test_snippet--preprocessor_test_data.py:transform_with_constant_string:transform with constant string",
        "b",
    ]
    out_lines = preprocessor_module._transform_lines(in_lines)
    expected_lines = [
        "a",
        "/// tab | :material-import: transform with constant string",
        "```python",
        "code = 2",
        "```",
        "///",
        "/// tab | :material-export: output",
        "```",
        "constant string",
        "```",
        "///",
        "b",
    ]
    assert out_lines == expected_lines


def test_snippet_with_no_output(preprocessor_module):
    in_lines = [
        "--[]->[]--test_snippet--preprocessor_test_data.py:snippet_with_no_output:snippet with no output"
    ]
    out_lines = preprocessor_module._transform_lines(in_lines)
    expected_lines = [
        '```python title="snippet with no output"',
        "code = 3",
        "run_function()",
        "```",
    ]
    assert out_lines == expected_lines


def test_snippet_rewrites_docs_display_and_hides_helper_lines(preprocessor_module):
    in_lines = [
        "--[]->[]--test_snippet--preprocessor_test_data.py:snippet_with_docs_display_and_hidden_lines:snippet with docs display"
    ]
    out_lines = preprocessor_module._transform_lines(in_lines)
    expected_lines = [
        "/// tab | :material-import: snippet with docs display",
        "```python",
        "render_me()",
        "```",
        "///",
        "/// tab | :material-export: output",
        "```",
        "constant string",
        "```",
        "///",
    ]
    assert out_lines == expected_lines


def test_snippet_replaces_placeholder_token_in_rendered_output(preprocessor_module):
    in_lines = [
        "--[]->[]--test_snippet--preprocessor_test_data.py:snippet_with_placeholder_output:snippet with placeholder output"
    ]
    out_lines = preprocessor_module._transform_lines(in_lines)
    expected_lines = [
        "/// tab | :material-import: snippet with placeholder output",
        "```python",
        "run_placeholder_demo()",
        "```",
        "///",
        "/// tab | :material-export: output",
        "```",
        "prefix ... suffix",
        "```",
        "///",
    ]
    assert out_lines == expected_lines

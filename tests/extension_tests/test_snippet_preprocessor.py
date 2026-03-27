from pathlib import Path
from unittest.mock import patch

import pytest

import bec_docs_pymdown_extensions.snippet_preprocessor as snippet_extension

from .preprocessor_test_data import INCLUDED_VALUE


@pytest.fixture()
def preprocessor_module():
    with (
        patch.object(snippet_extension, "TEST_SNIPPET_DIR", Path(__file__).parent),
        patch.object(snippet_extension, "_F_STRING_TOKENS", {"INCLUDED_VALUE": INCLUDED_VALUE}),
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
        "\n/// tab | transform with f-string\n```python \ncode = 1\n```\n///\n/// tab | expected output\n```\ninterpolated f-string\n```\n///\n",
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
        "\n/// tab | transform with constant string\n```python \ncode = 2\n```\n///\n/// tab | expected output\n```\nconstant string\n```\n///\n",
        "b",
    ]
    assert out_lines == expected_lines

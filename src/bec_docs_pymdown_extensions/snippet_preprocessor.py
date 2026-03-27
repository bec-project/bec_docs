import ast
from collections import defaultdict
from pathlib import Path
from textwrap import dedent

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

_CODE_SEQUENCE = "--[]->[]--test_snippet--"
TEST_SNIPPET_DIR = Path(__file__).parent / "../../tests/snippet_tests/"

PLACEHOLDER_TOKEN = "{{ placeholder }}"
_F_STRING_TOKENS = {"PLACEHOLDER_TOKEN": PLACEHOLDER_TOKEN}
_TOKEN_REPLACEMENTS = {PLACEHOLDER_TOKEN: "..."}


def _replace_placeholders(s: str) -> str:
    for k, v in _TOKEN_REPLACEMENTS.items():
        s = s.replace(k, v)
    return s


def _replacement(title: str, code: str, expected_output: str):
    return f"""
/// tab | {title}
```python 
{code}
```
///
/// tab | expected output
```
{_replace_placeholders(expected_output)}
```
///
"""


def _resolve_f_string_component(v: ast.expr) -> str:
    if isinstance(v, ast.Constant):
        return str(v.value)
    if isinstance(v, ast.FormattedValue):
        if not isinstance(v.value, ast.Name):
            return "[invalid placeholder in f-string]"
        return _F_STRING_TOKENS.get(v.value.id, f"[placeholder {v.value.id} not found]")
    return "[unsupported f-string component]"


def _process_str(node: ast.Assign):
    if isinstance(node.value, ast.JoinedStr):
        return "".join(_resolve_f_string_component(v) for v in node.value.values)
    if not isinstance(node.value, ast.Constant):
        return "[redirected constant - only use simply assigned constants as expected text]"
    return node.value.value


def _get_id_value(tree: ast.Module, id: str):
    for node in tree.body:
        if isinstance(node, ast.Assign):
            target = node.targets[0]
            if isinstance(target, ast.Name):
                if target.id == id:

                    value = _process_str(node)
                    return value


def _transform_lines(lines: list[str]):
    for i, line in enumerate(lines):
        if line.startswith(_CODE_SEQUENCE):
            line = line.removeprefix(_CODE_SEQUENCE).split(":")
            if len(line) != 3:
                lines[i] = "Incorrect syntax for tested code snippet!"
                continue
            file, test_name, title = line
            try:
                with open(TEST_SNIPPET_DIR / file) as f:
                    file_text = f.read()
                file_tree = ast.parse(file_text)
                function_defs = filter(lambda x: isinstance(x, ast.FunctionDef), file_tree.body)
                test_functions: list[ast.FunctionDef] = list(
                    filter(lambda x: x.name == test_name, function_defs)
                )
                if len(test_functions) == 0:
                    lines[i] = f"Failed to find test {test_name} in {file}"
                test_function = test_functions[0]
                code = "\n".join(
                    file_text.splitlines()[test_function.lineno : test_function.end_lineno]
                )
                expected_value = None
                for decorator in test_function.decorator_list:
                    if decorator.func.attr == "expected_output":
                        expected_value = _get_id_value(file_tree, decorator.args[0].args[0].id)
                lines[i] = _replacement(title, dedent(code), expected_value)
            except Exception as e:
                lines[i] = f"Failed to process code snippet file: {file} \n {e}"
    return lines


class TestSnippetsPreprocessor(Preprocessor):
    def run(self, lines):
        return _transform_lines(lines)


class TestSnippets(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(TestSnippetsPreprocessor(md), "snippets_preprocessor", 100000000)


def make_extension(**kwargs):
    return TestSnippets(**kwargs)

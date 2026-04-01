import pytest

from bec_docs_pymdown_extensions.matchers import ContainsExpectedOutputMatcher
from bec_docs_pymdown_extensions.snippet_preprocessor import PLACEHOLDER_TOKEN

CONSTANT_STRING = "constant string"
PLACEHOLDER_STRING = f"prefix {PLACEHOLDER_TOKEN} suffix"

INCLUDED_VALUE = "interpolated"
F_STRING = f"{INCLUDED_VALUE} f-string"


@pytest.mark.expected_output(ContainsExpectedOutputMatcher(F_STRING))
def transform_with_f_string():
    code = 1


@pytest.mark.expected_output(ContainsExpectedOutputMatcher(CONSTANT_STRING))
def transform_with_constant_string():
    code = 2


def snippet_with_no_output():
    code = 3
    run_function()


@pytest.mark.expected_output(ContainsExpectedOutputMatcher(CONSTANT_STRING))
def snippet_with_docs_display_and_hidden_lines():
    print(render_me())  # docs-display
    helper = render_me()  # docs-hide
    assert helper == "ok"  # docs-hide


@pytest.mark.expected_output(ContainsExpectedOutputMatcher(PLACEHOLDER_STRING))
def snippet_with_placeholder_output():
    run_placeholder_demo()


HTML = """\
<pre>
code = 1
</pre>
"""


@pytest.mark.expected_output(ContainsExpectedOutputMatcher(HTML, contains_html=True))
def transform_with_html_string():
    code = 1

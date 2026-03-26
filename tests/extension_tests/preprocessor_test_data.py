import pytest

from bec_docs_pymdown_extensions.matchers import ContainsExpectedOutputMatcher

CONSTANT_STRING = "constant string"

INCLUDED_VALUE = "interpolated"
F_STRING = f"{INCLUDED_VALUE} f-string"


@pytest.mark.expected_output(ContainsExpectedOutputMatcher(F_STRING))
def transform_with_f_string():
    code = 1


@pytest.mark.expected_output(ContainsExpectedOutputMatcher(CONSTANT_STRING))
def transform_with_constant_string():
    code = 2

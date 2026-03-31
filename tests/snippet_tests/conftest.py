from time import sleep

import pytest

from bec_docs_pymdown_extensions.matchers import ExpectedOutputMatcher


@pytest.fixture
def bec(bec_ipython_client_fixture):
    return bec_ipython_client_fixture


class TestSetupError(TypeError):
    """A failure to define the test correctly"""


@pytest.fixture(autouse=True)
def expected_output_check(capsys, request: pytest.FixtureRequest):
    mark = request.node.get_closest_marker("expected_output")
    if mark is None:
        yield
    else:
        if (len(mark.args) != 1) or not isinstance(matcher := mark.args[0], ExpectedOutputMatcher):
            raise TestSetupError("Mark your test with an expected output matcher!")
        yield
        captured = capsys.readouterr()
        if matcher.check(captured.out):
            pass
        else:
            # Retry after waiting to finish
            sleep(1)
            captured = capsys.readouterr()
            assert matcher.check(
                captured.out
            ), f"Expected output matcher {type(matcher)} failed for test: {request.node.name}. Diff:\n{matcher.diff(captured.out)}"

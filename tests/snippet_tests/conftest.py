from time import sleep

import pytest

from bec_docs_pymdown_extensions.matchers import ExpectedOutputMatcher


@pytest.fixture
def bec(bec_ipython_client_fixture):
    return bec_ipython_client_fixture


class TestSetupError(TypeError):
    """A failure to define the test correctly"""


def _get_expected_output_matcher(request: pytest.FixtureRequest) -> ExpectedOutputMatcher | None:
    """Return the matcher declared on the test, if any."""

    mark = request.node.get_closest_marker("expected_output")
    if mark is None:
        return None
    if (len(mark.args) != 1) or not isinstance(matcher := mark.args[0], ExpectedOutputMatcher):
        raise TestSetupError("Mark your test with an expected output matcher!")
    return matcher


@pytest.fixture
def expected_output_matcher(request: pytest.FixtureRequest) -> ExpectedOutputMatcher | None:
    """Expose the expected-output matcher to tests that validate output manually."""

    return _get_expected_output_matcher(request)


@pytest.fixture
def assert_expected_output(expected_output_matcher: ExpectedOutputMatcher | None, request):
    """Assert helper for tests that produce output outside normal pytest capture.

    Pair this with ``@pytest.mark.output_capture("manual")`` when the test itself must
    obtain the rendered output string, for example from IPython's pretty printer.
    """

    if expected_output_matcher is None:
        raise TestSetupError(f"No expected_output marker defined for test {request.node.name}")

    def _assert(output: str):
        assert expected_output_matcher.check(
            output
        ), f"Expected output matcher {type(expected_output_matcher)} failed for test: {request.node.name}. Diff:\n{expected_output_matcher.diff(output)}"

    return _assert


@pytest.fixture
def render_ipython_pretty():
    """Render an object through the same ``_repr_pretty_`` path used in BEC IPython.

    This is useful for snippet tests such as ``dev.samx`` where the documentation shows
    IPython pretty-printed output rather than plain stdout.
    """

    def _render(obj) -> str:
        class MockPrinter:
            def __init__(self):
                self.text_output = None
                self.indentation = 0

            def text(self, value):
                self.text_output = value

        printer = MockPrinter()
        obj._repr_pretty_(printer, cycle=False)
        return printer.text_output

    return _render


@pytest.fixture(autouse=True)
def expected_output_check(request: pytest.FixtureRequest):
    """Run the default expected-output assertion after each snippet test.

    Capture modes:
    - ``sys``: use ``capsys`` for normal Python stdout/stderr
    - ``fd``: use ``capfd`` for live progress / lower-level writes
    - ``manual``: skip automatic capture because the test validates the rendered output
      itself via ``assert_expected_output(...)``
    """

    matcher = _get_expected_output_matcher(request)
    if matcher is None:
        yield
    else:
        capture_mark = request.node.get_closest_marker("output_capture")
        capture_mode = capture_mark.args[0] if capture_mark else "sys"
        capture_fixture_name = {"sys": "capsys", "fd": "capfd", "manual": None}.get(capture_mode)
        if capture_fixture_name is None:
            if capture_mode != "manual":
                raise TestSetupError(f"Unsupported output capture mode: {capture_mode!r}")
            yield
            return
        capture = request.getfixturevalue(capture_fixture_name)
        yield
        captured = capture.readouterr()
        for _ in range(3):
            if matcher.check(captured.out):
                break
            else:
                # Retry after waiting to finish
                sleep(1)
                captured = capture.readouterr()
        assert matcher.check(
            captured.out
        ), f"Expected output matcher {type(matcher)} failed for test: {request.node.name}. Diff:\n{matcher.diff(captured.out)}"

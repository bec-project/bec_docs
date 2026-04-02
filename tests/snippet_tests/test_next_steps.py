from __future__ import annotations

import re
from time import sleep

import pytest

from bec_docs_pymdown_extensions.matchers import (
    ContainsExpectedOutputMatcher,
    SignalArrayOutputMatcher,
    SimilarExpectedOutputMatcher,
)
from bec_docs_pymdown_extensions.snippet_preprocessor import PLACEHOLDER_TOKEN


def _wait_for_scan_in_history(bec, scan_report, timeout_s: float = 7.0):
    """Wait until the specific scan appears in history and return it."""
    for _ in range(int(timeout_s / 0.1)):
        latest = bec.history.get_by_scan_id(scan_report.scan.scan_id)
        if latest is not None:
            return latest
        sleep(0.1)
    raise AssertionError("Timed out waiting for the scan to appear in bec.history")


def _normalize_scan_container_summary(output: str) -> str:
    """Strip runtime-specific values from ScanDataContainer summary output."""
    replacements = (
        (r"(\n \tStart time: ).*", r"\1"),
        (r"(\n\tStart time: ).*", r"\1"),
        (r"(\n\tEnd time: ).*", r"\1"),
        (r"(\n\tElapsed time: ).*( s)", r"\1\2"),
        (r"(\n\tScan ID: ).*", r"\1"),
        (r"(\n\tScan number: ).*", r"\1"),
        (r"(\n\tFile: ).*", r"\1"),
    )
    normalized = output
    for pattern, replacement in replacements:
        normalized = re.sub(pattern, replacement, normalized)
    return normalized


SCAN_HISTORY_SIGNAL_OUTPUT = """\
{'timestamp': array([1.77496343e+09, 1.77496343e+09, 1.77496343e+09, 1.77496344e+09,
        1.77496344e+09]),
 'value': array([-0.99140924, -0.49119309, -0.00282538,  0.49814051,  0.99329906])}
"""


SCAN_REPORT_OUTPUT = f"""\
ScanReport:
--------------------
	Status: COMPLETED
	Start time: {PLACEHOLDER_TOKEN}
	End time: {PLACEHOLDER_TOKEN}
	Elapsed time: {PLACEHOLDER_TOKEN} s
	Scan ID: {PLACEHOLDER_TOKEN}
	Scan number: {PLACEHOLDER_TOKEN}
	Number of points: 5
	File: {PLACEHOLDER_TOKEN}
"""


@pytest.mark.timeout(100)
@pytest.mark.output_capture("manual")
@pytest.mark.expected_output(ContainsExpectedOutputMatcher(SCAN_REPORT_OUTPUT))
def test_scan_report(bec, assert_expected_output):
    scan_report = scans.line_scan(  # docs-hide
        dev.samx, -1, 1, steps=5, exp_time=0.1, relative=False  # docs-hide
    )  # docs-hide
    scan_report.wait(num_points=True, file_written=True)  # docs-hide
    _wait_for_scan_in_history(bec, scan_report)  # docs-hide
    print(scan_report)  # docs-hide
    scan_report
    assert_expected_output(_normalize_scan_container_summary(str(scan_report)))  # docs-hide


SCAN_HISTORY_CONTAINER_OUTPUT = f"""\
ScanDataContainer:
 \tStart time: {PLACEHOLDER_TOKEN}
\tEnd time: {PLACEHOLDER_TOKEN}
\tElapsed time: {PLACEHOLDER_TOKEN} s
\tScan ID: {PLACEHOLDER_TOKEN}
\tScan number: {PLACEHOLDER_TOKEN}
\tScan name: line_scan
\tStatus: closed
\tNumber of points (monitored): 5
\tFile: {PLACEHOLDER_TOKEN}
"""


@pytest.mark.timeout(100)
@pytest.mark.output_capture("manual")
@pytest.mark.expected_output(ContainsExpectedOutputMatcher(SCAN_HISTORY_CONTAINER_OUTPUT))
def test_scan_history_container_summary(bec, assert_expected_output):
    scan_report = scans.line_scan(  # docs-hide
        dev.samx, -1, 1, steps=5, exp_time=0.1, relative=False  # docs-hide
    )  # docs-hide
    scan_report.wait(num_points=True, file_written=True)  # docs-hide
    _wait_for_scan_in_history(bec, scan_report)  # docs-hide
    latest = bec.history[-1]
    print(latest)  # docs-display
    assert_expected_output(_normalize_scan_container_summary(repr(latest)))  # docs-hide


@pytest.mark.timeout(100)
@pytest.mark.output_capture("fd")
@pytest.mark.expected_output(
    SignalArrayOutputMatcher(SCAN_HISTORY_SIGNAL_OUTPUT, value_atol=0.05, value_rtol=0.01)
)
def test_scan_history_signal_arrays(bec):
    scan_report = scans.line_scan(  # docs-hide
        dev.samx, -1, 1, steps=5, exp_time=0.1, relative=False  # docs-hide
    )  # docs-hide
    scan_report.wait(num_points=True, file_written=True)  # docs-hide
    latest = _wait_for_scan_in_history(bec, scan_report)  # docs-hide
    print(latest.devices.samx.samx.read())  # docs-display

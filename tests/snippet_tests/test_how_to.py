from __future__ import annotations

import re
from time import sleep

import h5py
import pytest

from bec_docs_pymdown_extensions.matchers import ContainsExpectedOutputMatcher
from bec_docs_pymdown_extensions.snippet_preprocessor import PLACEHOLDER_TOKEN


def _wait_for_scan_in_history(bec, scan_report, timeout_s: float = 7.0):
    for _ in range(int(timeout_s / 0.1)):
        latest = bec.history.get_by_scan_id(scan_report.scan.scan_id)
        if latest is not None:
            return latest
        sleep(0.1)
    raise AssertionError("Timed out waiting for the scan to appear in bec.history")


def _normalize_scan_container_summary(output: str) -> str:
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


def _prepare_completed_scan(bec):
    scan_report = scans.line_scan(  # docs-hide
        dev.samx, -1, 1, steps=5, exp_time=0.1, relative=False  # docs-hide
    )  # docs-hide
    scan_report.wait(num_points=True, file_written=True)  # docs-hide
    latest = _wait_for_scan_in_history(bec, scan_report)  # docs-hide
    return scan_report, latest  # docs-hide


def _master_file_path(scan_report):
    master_files = [file for file in scan_report.scan.public_files if "_master" in file]
    if not master_files:
        raise AssertionError("No master file was recorded for the scan")
    return master_files[0]


SCAN_HISTORY_CONTAINER_OUTPUT = f"""\
ScanDataContainer:
    Start time: {PLACEHOLDER_TOKEN}
    End time: {PLACEHOLDER_TOKEN}
    Elapsed time: {PLACEHOLDER_TOKEN} s
    Scan ID: {PLACEHOLDER_TOKEN}
    Scan number: {PLACEHOLDER_TOKEN}
    Scan name: line_scan
    Status: closed
    Number of points (monitored): 5
    File: {PLACEHOLDER_TOKEN}
"""


@pytest.mark.timeout(100)
def test_history_len(bec):
    _prepare_completed_scan(bec)  # docs-hide
    len(bec.history)
    assert len(bec.history) >= 1  # docs-hide


@pytest.mark.timeout(100)
def test_history_latest_scan(bec):
    _prepare_completed_scan(bec)  # docs-hide
    scan = bec.history[-1]
    assert scan is not None  # docs-hide


@pytest.mark.timeout(100)
def test_history_by_scan_number(bec):
    scan_number = 1234
    scan_report, _ = _prepare_completed_scan(bec)  # docs-hide
    scan_number = scan_report.scan.scan_number  # docs-hide
    scan = bec.history.get_by_scan_number(scan_number)
    assert scan is not None  # docs-hide


@pytest.mark.timeout(100)
def test_history_select_first_scan_number_match(bec):
    scan_number = 1234
    matches = bec.history.get_by_scan_number(scan_number)

    scan_report, latest = _prepare_completed_scan(bec)  # docs-hide
    scan_number = scan_report.scan.scan_number  # docs-hide
    matches = bec.history.get_by_scan_number(scan_report.scan.scan_number)  # docs-hide
    if isinstance(matches, list):  # docs-hide
        scan = matches[0]  # docs-hide
    else:  # docs-hide
        scan = matches  # docs-hide
    assert scan is not None  # docs-hide
    assert scan._msg.scan_id == latest._msg.scan_id  # docs-hide


@pytest.mark.timeout(100)
def test_history_by_scan_id(bec):
    scan_id = "your-scan-id"
    scan_report, _ = _prepare_completed_scan(bec)  # docs-hide
    scan_id = scan_report.scan.scan_id  # docs-hide
    scan = bec.history.get_by_scan_id(scan_id)
    assert scan is not None  # docs-hide


@pytest.mark.timeout(100)
def test_history_recent_scans(bec):
    _prepare_completed_scan(bec)  # docs-hide
    recent_scans = bec.history[-5:]
    assert len(recent_scans) >= 1  # docs-hide


@pytest.mark.timeout(100)
@pytest.mark.output_capture("manual")
@pytest.mark.expected_output(ContainsExpectedOutputMatcher(SCAN_HISTORY_CONTAINER_OUTPUT))
def test_history_print_scan_container(bec, assert_expected_output):
    _, scan = _prepare_completed_scan(bec)  # docs-hide
    print(scan)  # docs-display
    assert scan is not None  # docs-hide
    assert_expected_output(  # docs-hide
        _normalize_scan_container_summary(repr(scan)).replace("\t", "    ")  # docs-hide
    )  # docs-hide


@pytest.mark.timeout(100)
def test_history_metadata_access(bec):
    _, scan = _prepare_completed_scan(bec)  # docs-hide
    scan.metadata["bec"]
    scan.metadata["bec"]["scan_number"]
    assert scan.metadata["bec"]["scan_number"] is not None  # docs-hide


@pytest.mark.timeout(100)
def test_history_readout_groups_access(bec):
    _, scan = _prepare_completed_scan(bec)  # docs-hide
    scan.readout_groups.monitored_devices.read()
    scan.readout_groups.baseline_devices.read()
    assert scan.readout_groups.monitored_devices.read()  # docs-hide
    assert scan.readout_groups.baseline_devices.read()  # docs-hide


@pytest.mark.timeout(100)
def test_history_device_access(bec):
    _, scan = _prepare_completed_scan(bec)  # docs-hide
    scan.devices.samx.read()
    assert scan.devices.samx.read()  # docs-hide


@pytest.mark.timeout(100)
def test_history_signal_access(bec):
    _, scan = _prepare_completed_scan(bec)  # docs-hide
    scan.devices.samx.samx.get()
    scan.data.samx_setpoint.get()
    assert scan.devices.samx.samx.get() is not None  # docs-hide
    assert scan.data.samx_setpoint.get() is not None  # docs-hide


@pytest.mark.timeout(100)
def test_h5py_open_root(bec):
    import h5py

    path = "/path/to/S01234_master.h5"
    scan_report, _ = _prepare_completed_scan(bec)  # docs-hide
    path = _master_file_path(scan_report)  # docs-hide

    with h5py.File(path, "r") as f:
        print(list(f.keys()))
        assert "entry" in f  # docs-hide


@pytest.mark.timeout(100)
def test_h5py_collection_keys(bec):
    path = "/path/to/S01234_master.h5"
    scan_report, _ = _prepare_completed_scan(bec)  # docs-hide
    path = _master_file_path(scan_report)  # docs-hide

    with h5py.File(path, "r") as f:
        collection = f["entry"]["collection"]
        print(list(collection.keys()))
        assert "metadata" in collection  # docs-hide
        assert "readout_groups" in collection  # docs-hide


@pytest.mark.timeout(100)
def test_h5py_metadata_keys(bec):
    path = "/path/to/S01234_master.h5"
    scan_report, _ = _prepare_completed_scan(bec)  # docs-hide
    path = _master_file_path(scan_report)  # docs-hide

    with h5py.File(path, "r") as f:
        metadata = f["entry"]["collection"]["metadata"]
        print(list(metadata.keys()))
        assert len(metadata.keys()) > 0  # docs-hide


@pytest.mark.timeout(100)
def test_h5py_read_dataset(bec):
    path = "/path/to/S01234_master.h5"
    scan_report, _ = _prepare_completed_scan(bec)  # docs-hide
    path = _master_file_path(scan_report)  # docs-hide

    with h5py.File(path, "r") as f:
        data = f["entry"]["collection"]["readout_groups"]["monitored"]["samx"]["samx"]["value"][...]
        print(data)
        assert len(data) == 5  # docs-hide


@pytest.mark.timeout(100)
def test_h5py_visititems(bec):
    import h5py

    path = "/path/to/S01234_master.h5"
    scan_report, _ = _prepare_completed_scan(bec)  # docs-hide
    path = _master_file_path(scan_report)  # docs-hide

    seen = []  # docs-hide

    def show_tree(name, obj):
        print(name)
        seen.append(name)  # docs-hide

    with h5py.File(path, "r") as f:
        f.visititems(show_tree)

    assert any(name.startswith("entry/collection") for name in seen)  # docs-hide


@pytest.mark.timeout(100)
def test_h5py_file_references(bec):
    path = "/path/to/S01234_master.h5"
    scan_report, _ = _prepare_completed_scan(bec)  # docs-hide
    path = _master_file_path(scan_report)  # docs-hide

    with h5py.File(path, "r") as f:
        refs = f["entry"]["collection"]["file_references"]
        print(list(refs.keys()))
        assert refs is not None  # docs-hide

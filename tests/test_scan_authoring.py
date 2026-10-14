"""Run the tutorial class and displayed how-to tests with mocked server resources."""

from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

pytest.importorskip("bec_server")
from bec_lib.bec_errors import ScanInputValidationError
from bec_server.scan_server.tests.scan_fixtures import (
    ReadoutPriorityContainer,
    _make_scan_assembler,
)

from scan_authoring_example import HOW_TO, documented_tests, example_class

AlternatingScan = example_class()
# These are the actual test functions shown to scan developers in the how-to guide.
exec(compile(documented_tests(), str(HOW_TO), "exec"))


@pytest.fixture
def scan_assembler(tmp_path):
    with patch(
        "bec_server.scan_server.scan_manager.ScanManager.get_available_scans",
        return_value=[("AlternatingScan", AlternatingScan)],
    ):
        assemble = _make_scan_assembler(
            ReadoutPriorityContainer(), SimpleNamespace(_custom_devices={}), tmp_path
        )

    def create(*args, **kwargs):
        with (
            patch(
                "bec_server.scan_server.scans.scan_argument_modifier.get_scan_modifier",
                return_value=None,
            ),
            patch("bec_server.scan_server.scan_assembler.get_scan_modifier", return_value=None),
        ):
            return assemble(*args, **kwargs)

    return create


def test_invalid_repeat_count(scan_assembler):
    with pytest.raises(ScanInputValidationError):
        scan_assembler("alternating_scan", "samx", -0.5, 0.5, repeats=0, relative=False)


def test_baseline_status_checked_before_close(scan_assembler):
    scan = scan_assembler("alternating_scan", "samx", -0.5, 0.5, repeats=1, relative=False)
    operations = []
    scan._baseline_readout_status = Mock()
    scan._baseline_readout_status.wait.side_effect = lambda: operations.append("baseline")
    scan.actions.close_scan = Mock(side_effect=lambda: operations.append("close"))
    scan.close_scan()
    assert operations == ["baseline", "close"]


def test_constructor_does_not_emit_device_instructions(scan_assembler):
    with patch("bec_server.scan_server.scans.scan_actions.ScanActions._send") as send:
        scan_assembler("alternating_scan", "samx", -0.5, 0.5, repeats=1, relative=False)
    send.assert_not_called()

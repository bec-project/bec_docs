---
related:
  - title: Write an alternating-position scan
    url: getting-started/next-steps/write-a-scan.md
  - title: Scan lifecycle and authoring responsibilities
    url: learn/scans/scan-lifecycle.md
  - title: Scan development API
    url: references/bec-core/scan-base-and-stubs.md
---

# Test a scan

!!! info "Overview"
    Check a custom scan's measurement sequence, coordinates, and recovery with mocked
    devices, then verify that it runs and records data in a simulated BEC deployment.

## Before you start

Use a plugin installed in your development Python environment, with its scan exported
through the `bec.scans` entry point. Install pytest and the BEC development dependencies.
The examples test the
[alternating-position scan](../../getting-started/next-steps/write-a-scan.md), named
`alternating_scan`. Substitute your own scan name and its expected scientific results.

## 1. Load the scan fixtures

Create `tests/conftest.py` in your plugin, or add these entries to its existing
`pytest_plugins` list:

```python
pytest_plugins = [
    "bec_lib.tests.fixtures",
    "bec_server.scan_server.tests.scan_fixtures",
]
```

`scan_assembler` creates a scan with mocked server resources and motors. It discovers the
scan through your installed plugin. Its default mocked motor limits are -10 to 10, and
its initial position is zero. These tests do not start BEC services or move real devices.

## 2. Check the intended measurement

Create `tests/test_alternating_scan.py`:

```python
from unittest.mock import Mock

import numpy as np
import pytest

from bec_server.scan_server.errors import LimitError


def test_positions_and_counts(scan_assembler):
    scan = scan_assembler(
        "alternating_scan", "samx", -0.5, 0.5, repeats=3, relative=False
    )
    scan.prepare_scan()
    np.testing.assert_allclose(scan.positions[:, 0], [-0.5, 0.5, -0.5, 0.5, -0.5, 0.5])
    assert scan.positions.shape == (6, 1)
    assert scan.scan_info.num_points == 6
    assert scan.scan_info.num_monitored_readouts == 6


def test_relative_coordinates(scan_assembler):
    scan = scan_assembler(
        "alternating_scan", "samx", -0.5, 0.5, repeats=2, relative=True
    )
    scan.components.get_start_positions = Mock(return_value=[1.0])
    scan.prepare_scan()
    np.testing.assert_allclose(scan.positions[:, 0], [0.5, 1.5, 0.5, 1.5])


def test_limits_before_motion(scan_assembler):
    scan = scan_assembler(
        "alternating_scan", "samx", -20.0, 20.0, repeats=1, relative=False
    )
    scan.actions.set = Mock()
    with pytest.raises(LimitError):
        scan.prepare_scan()
    scan.actions.set.assert_not_called()


def test_one_acquisition_per_visit(scan_assembler):
    scan = scan_assembler(
        "alternating_scan", "samx", -0.5, 0.5, repeats=3, relative=False
    )
    scan.prepare_scan()
    scan.components.move_and_wait = Mock()
    scan.components.trigger_and_read = Mock()
    scan.scan_core()
    targets = [call.args[1][0] for call in scan.components.move_and_wait.call_args_list]
    np.testing.assert_allclose(targets, [-0.5, 0.5, -0.5, 0.5, -0.5, 0.5])
    assert scan.components.trigger_and_read.call_count == 6
```

Use a nonzero starting position to detect a missing relative offset. Count the acquisitions
the loop requests, as well as its declared metadata. An incorrect A/A/A/B/B/B sequence
should fail these tests even though it contains six positions.

## 3. Exercise partial work and recovery

Add these tests to the same file:

```python
@pytest.mark.parametrize("relative", [False, True])
def test_return_after_completion(scan_assembler, relative):
    scan = scan_assembler(
        "alternating_scan", "samx", -0.5, 0.5, repeats=1, relative=relative
    )
    scan.components.get_start_positions = Mock(return_value=[1.0])
    scan.prepare_scan()
    scan.components.move_and_wait = Mock()
    scan.components.trigger_and_read = Mock()
    scan.scan_core()
    scan.components.move_and_wait.reset_mock()
    scan.actions.complete_all_devices = Mock()
    scan.post_scan()
    if relative:
        scan.components.move_and_wait.assert_called_once_with(scan.motors, [1.0])
    else:
        scan.components.move_and_wait.assert_not_called()


def test_failure_before_start_position_is_known(scan_assembler):
    scan = scan_assembler(
        "alternating_scan", "samx", -0.5, 0.5, repeats=1, relative=True
    )
    scan.components.get_start_positions = Mock(side_effect=RuntimeError("read failed"))
    scan.components.move_and_wait = Mock()
    scan.actions.unstage_all_devices = Mock()
    with pytest.raises(RuntimeError, match="read failed") as failure:
        scan.prepare_scan()
    scan.on_exception(failure.value)
    scan.components.move_and_wait.assert_not_called()
    scan.actions.unstage_all_devices.assert_called_once()


def test_unstage_after_partial_staging(scan_assembler):
    scan = scan_assembler(
        "alternating_scan", "samx", -0.5, 0.5, repeats=1, relative=False
    )
    scan.actions.stage_all_devices = Mock(side_effect=RuntimeError("staging failed"))
    scan.actions.unstage_all_devices = Mock()
    with pytest.raises(RuntimeError, match="staging failed") as failure:
        scan.stage()
    scan.on_exception(failure.value)
    scan.actions.unstage_all_devices.assert_called_once()


def test_unstage_even_when_return_fails(scan_assembler):
    scan = scan_assembler(
        "alternating_scan", "samx", -0.5, 0.5, repeats=1, relative=True
    )
    scan.components.get_start_positions = Mock(return_value=[1.0])
    scan.prepare_scan()
    scan.actions.stage_all_devices = Mock()
    scan.actions.unstage_all_devices = Mock()
    scan.stage()
    scan.components.move_and_wait = Mock(side_effect=RuntimeError("move failed"))
    with pytest.raises(RuntimeError, match="move failed") as failure:
        scan.scan_core()
    with pytest.raises(RuntimeError, match="move failed"):
        scan.on_exception(failure.value)
    scan.actions.unstage_all_devices.assert_called_once()
```

A `Mock` records calls or supplies a controlled result/failure. These cases test recovery
when preparation cannot read a motor, staging fails partway through, or motion and its
recovery both fail. For your scan, also test restoration of every temporary device setting
and account for asynchronous statuses that must finish before closing.

Run the file from your plugin repository root:

```bash
python -m pytest -q tests/test_alternating_scan.py
```

## 4. Verify a simulated acquisition

Follow the tutorial's
[simulated run](../../getting-started/next-steps/write-a-scan.md#4-run-with-the-simulated-motor).
Confirm the six recorded positions, the detector readings, the master file, and the final
motor position. Repeat the relative case from a nonzero start. Exercise interruption in
that development deployment and inspect positions, queue state, and partial data before
continuing.

Mock tests prove the requested sequence and recovery decisions. A simulated run checks
plugin discovery, server execution, devices, data collection, and file writing together.
Keep both kinds of evidence before using a custom scan with beamline devices.

!!! success "Congratulations!"
    Your scan has checks for its intended measurements and partial-failure recovery, plus
    a simulated run that verifies the recorded result.

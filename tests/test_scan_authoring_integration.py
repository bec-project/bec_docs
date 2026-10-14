"""Run the tutorial as an installed plugin in an isolated simulated BEC deployment.

Run separately from the other integration tests, so the plugin is installed before
services start. Requires the pytest-bec-e2e plugin and --start-servers.
"""

import importlib
import os
import subprocess
import sys
import time
from pathlib import Path
from unittest.mock import Mock, patch

import h5py
import numpy as np
import pytest

from pytest_bec_e2e.plugin import bec_servers_scope
from typer.testing import CliRunner

from bec_lib.utils.plugin_manager.create.scan import _BUILTIN_ARGUMENTS
from bec_lib.utils.plugin_manager.main import _app

from scan_authoring_example import documented_tests, example_source


@pytest.fixture(scope="session")
def tutorial_plugin(tmp_path_factory):
    root = tmp_path_factory.mktemp("scan_authoring_plugin") / "my_beamline"
    root.mkdir()
    package = root / "my_beamline"
    scans_package = package / "scans"
    package.mkdir()
    (package / "__init__.py").write_text("")
    selections = ["SOFTWARE_TRIGGERED", "DeviceBase", "float", "float", "int"]
    builtins = [arg for arg in _BUILTIN_ARGUMENTS if arg.name in {"relative", "exp_time"}]
    # Resolve only the repository/components to this isolated fixture. Exercise the real
    # command, prompts, template, package export, and formatters before implementing it.
    with (
        patch("bec_lib.utils.plugin_manager.create.scan.plugin_repo_path", return_value=str(root)),
        patch(
            "bec_lib.utils.plugin_manager.create.scan._get_plugin_components_config",
            return_value=(None, None),
        ),
        patch(
            "bec_lib.utils.plugin_manager.create.scan.questionary.select",
            side_effect=[Mock(ask=Mock(return_value=value)) for value in selections],
        ),
        patch(
            "bec_lib.utils.plugin_manager.create.scan.questionary.checkbox",
            return_value=Mock(ask=Mock(return_value=builtins)),
        ),
    ):
        generated = CliRunner().invoke(
            _app,
            ["create", "scan", "alternating_scan"],
            input=(
                "Alternating-position scan\ny\ny\n"
                "motor\nMotor to move\ny\n"
                "position_a\nNone\nFirst position\ny\n"
                "position_b\nNone\nSecond position\ny\n"
                "repeats\nNone\nNumber of A/B pairs\nn\n"
            ),
        )
    assert generated.exit_code == 0, generated.output
    scan_file = scans_package / "alternating_scan.py"
    generated_source = scan_file.read_text()
    assert "class AlternatingScan(ScanBase):" in generated_source
    assert "relative: DefaultArgType.Relative" in generated_source
    assert "exp_time: DefaultArgType.ExposureTime = 0" in generated_source
    assert (scans_package / "__init__.py").read_text() == (
        "from .alternating_scan import AlternatingScan\n"
    )
    # Apply only the edits shown in the tutorial to the actual generated file.
    scan_file.write_text(example_source(generated_source))
    (root / "pyproject.toml").write_text(
        '[build-system]\nrequires = ["setuptools"]\n'
        'build-backend = "setuptools.build_meta"\n\n'
        '[project]\nname = "docs-scan-example"\nversion = "0.0.0"\n\n'
        '[project.entry-points."bec.scans"]\nplugin_scans = "my_beamline.scans"\n'
    )
    target = root / "installed"
    # Installation is confined to a temporary target, not the user's Python environment.
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--no-build-isolation",
            "--no-deps",
            "--target",
            str(target),
            str(root),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    previous = os.environ.get("PYTHONPATH")
    os.environ["PYTHONPATH"] = str(target) + (os.pathsep + previous if previous else "")
    sys.path.insert(0, str(target))
    importlib.invalidate_caches()
    try:
        yield target
    finally:
        sys.path.remove(str(target))
        if previous is None:
            os.environ.pop("PYTHONPATH", None)
        else:
            os.environ["PYTHONPATH"] = previous
        importlib.invalidate_caches()


@pytest.fixture(scope=bec_servers_scope)
def bec_servers(tutorial_plugin, bec_servers):
    # The prerequisite is installed before the parent fixture starts its services.
    yield bec_servers


def wait_for_history(client, report):
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        scan = client.history.get_by_scan_id(report.scan.scan_id)
        if scan is not None:
            return scan
        time.sleep(0.1)
    raise AssertionError("Tutorial scan did not appear in readable file-backed history")


@pytest.mark.timeout(100)
@pytest.mark.parametrize("relative", [False, True])
def test_tutorial_plugin_acquisition(bec_ipython_client_fixture, relative):
    client = bec_ipython_client_fixture
    devices = client.device_manager.devices
    for name in devices:
        if len(name) > 6:
            devices[name].enabled = False
    client._request_scan_reload()
    deadline = time.monotonic() + 10
    while not hasattr(client.scans, "alternating_scan"):
        assert time.monotonic() < deadline, "Reload did not publish the tutorial scan"
        time.sleep(0.1)
    client.scans.umv(devices.samx, 1, relative=False)
    report = client.scans.alternating_scan(
        devices.samx, -0.5, 0.5, repeats=3, relative=relative, exp_time=0.1
    )
    expected = np.tile([0.5, 1.5] if relative else [-0.5, 0.5], 3)
    assert report.status == "COMPLETED"
    assert report.scan.num_points == 6
    assert report.scan.num_monitored_readouts == 6
    np.testing.assert_allclose(report.scan.live_data["samx"]["samx"].val, expected, atol=0.05)
    final_position = devices.samx.read()["samx"]["value"]
    assert final_position == pytest.approx(1 if relative else 0.5, abs=0.05)
    scan = wait_for_history(client, report)
    np.testing.assert_allclose(scan.devices.samx.samx.read()["value"], expected, atol=0.05)
    files = report.scan.public_files
    master = next(path for path in files if "_master" in Path(path).name)
    assert files[master]["done_state"] and files[master]["successful"]
    with h5py.File(master, "r") as handle:
        monitored = handle["entry/collection/readout_groups/monitored"]
        assert "samx" in monitored
        assert len(monitored) > 1, "No detector data was recorded with the motor"


def test_documented_plugin_tests(tutorial_plugin):
    root = tutorial_plugin.parent
    tests = root / "tests"
    tests.mkdir()
    (tests / "conftest.py").write_text(
        'pytest_plugins = ["bec_lib.tests.fixtures", '
        '"bec_server.scan_server.tests.scan_fixtures"]\n'
    )
    (tests / "test_alternating_scan.py").write_text(documented_tests())
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(tests)],
        env={**os.environ, "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "9 passed" in result.stdout

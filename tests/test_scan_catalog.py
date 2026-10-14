"""Check catalog examples against server assembly without starting BEC services."""

import ast
import importlib
import re
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

pytest.importorskip("bec_server")
np = pytest.importorskip("numpy")
from bec_server.scan_server.tests.scan_fixtures import (
    ReadoutPriorityContainer,
    _make_scan_assembler,
)

CATALOG = Path(__file__).resolve().parents[1] / "docs/references/bec-core/scans.md"
# Independent counts for the published examples. Geometry-dependent cases are checked
# against their bounds rather than an implementation-derived expected point count.
EXPECTED_COUNTS = {
    "acquire": (1, 3),
    "time_scan": (5, 5),
    "line_scan": (5, 5),
    "grid_scan": (15, 15),
    "list_scan": (4, 4),
    "log_scan": (7, 7),
    "round_scan": (36, 36),
    "multi_region_line_scan": (7, 7),
    "multi_region_grid_scan": (15, 15),
    "cont_line_scan": (5, 5),
    "line_sweep_scan": (0, 0),
}


def catalog_examples():
    examples = {}
    for block in re.findall(r"```python\n(.*?)\n```", CATALOG.read_text(), re.DOTALL):
        call = ast.parse(block).body[0].value
        assert isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)
        assert call.func.value.id == "scans"
        args = [
            arg.attr if isinstance(arg, ast.Attribute) else ast.literal_eval(arg)
            for arg in call.args
        ]
        kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in call.keywords}
        examples[call.func.attr] = (args, kwargs)
    return examples


EXAMPLES = catalog_examples()


def builtin_scan_classes():
    # Inspect only built-in modules, independent of locally installed beamline plugins.
    directory = Path(importlib.import_module("bec_server.scan_server.scans").__file__).parent
    classes = {}
    for path in directory.glob("*.py"):
        module = importlib.import_module(f"bec_server.scan_server.scans.{path.stem}")
        for obj in vars(module).values():
            if (
                isinstance(obj, type)
                and obj.__module__ == module.__name__
                and getattr(obj, "is_scan", False)
                and getattr(obj, "scan_name", None) != "base_scan"
            ):
                classes[obj.scan_name] = obj
    return classes


def test_catalog_covers_builtin_acquisition_scans():
    assert set(EXAMPLES) == set(builtin_scan_classes())


@pytest.fixture(scope="module")
def plotted_positions():
    script = CATALOG.parents[3] / "tools/generate_scan_catalog_images.py"
    spec = importlib.util.spec_from_file_location("scan_catalog_images", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.example_positions()


@pytest.mark.parametrize("scan_name", EXAMPLES)
def test_catalog_example_preparation(scan_name, tmp_path, plotted_positions):
    classes = [(cls.__name__, cls) for cls in builtin_scan_classes().values()]
    with patch(
        "bec_server.scan_server.scan_manager.ScanManager.get_available_scans", return_value=classes
    ):
        assembler = _make_scan_assembler(
            ReadoutPriorityContainer(), SimpleNamespace(_custom_devices={}), tmp_path
        )
    args, kwargs = EXAMPLES[scan_name]
    with (
        patch(
            "bec_server.scan_server.scans.scan_argument_modifier.get_scan_modifier",
            return_value=None,
        ),
        patch("bec_server.scan_server.scan_assembler.get_scan_modifier", return_value=None),
    ):
        scan = assembler(scan_name, *args, **kwargs)
    if scan_name == "cont_line_scan":
        # The mocked motor has no velocity/acceleration signals. Supply compatible
        # values for preparation; no motion or detector acquisition is performed.
        def motor_attributes():
            scan.motor_velocity = 0.1
            scan.motor_acceleration = 1.0

        scan._get_motor_attributes = motor_attributes
    scan.prepare_scan()
    if scan_name in plotted_positions:
        np.testing.assert_allclose(plotted_positions[scan_name], scan.positions)
        image = CATALOG.parents[2] / "assets/scan-catalog" / f"{scan_name}.svg"
        assert image.resolve().is_file()
    if scan_name in EXPECTED_COUNTS:
        assert (
            scan.scan_info.num_points,
            scan.scan_info.num_monitored_readouts,
        ) == EXPECTED_COUNTS[scan_name]
    if scan.positions.size:
        assert np.isfinite(scan.positions).all()
        assert (scan.positions >= -1).all()
        assert (scan.positions <= 1).all()
    if scan_name == "line_scan":
        np.testing.assert_allclose(scan.positions[:, 0], [-1, -0.5, 0, 0.5, 1])
        np.testing.assert_allclose(scan.positions[:, 1], [-1, -0.5, 0, 0.5, 1])
    if scan_name == "multi_region_line_scan":
        np.testing.assert_allclose(scan.positions[:, 0], [-1, -0.5, 0, 0.25, 0.5, 0.75, 1])
    if scan_name == "grid_scan":
        np.testing.assert_allclose(scan.positions[:5, 0], [-1, -0.5, 0, 0.5, 1])
        np.testing.assert_allclose(scan.positions[5:10, 0], [1, 0.5, 0, -0.5, -1])
    if scan_name == "round_scan":
        np.testing.assert_allclose(
            np.linalg.norm(scan.positions, axis=1), [1 / 3] * 6 + [2 / 3] * 12 + [1] * 18
        )
    if scan_name == "round_roi_scan":
        assert np.abs(scan.positions[:, 1]).max() <= 0.5

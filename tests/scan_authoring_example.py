"""Apply the tutorial's edits to a generated scan and load the displayed tests."""

import ast
import re
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
TUTORIAL = ROOT / "docs/getting-started/next-steps/write-a-scan.md"
HOW_TO = ROOT / "docs/how-to/scans/test-a-scan.md"


def generated_example_source():
    from bec_lib.utils.plugin_manager.create.scan import (
        CustomArgumentSpec,
        ScanConfig,
        _BUILTIN_ARGUMENTS,
        _render_scan,
    )
    from bec_lib.utils.plugin_manager.create import scan

    arguments = [
        CustomArgumentSpec(name="motor", type="DeviceBase", doc="Motor to move"),
        CustomArgumentSpec(name="position_a", type="float", doc="First position"),
        CustomArgumentSpec(name="position_b", type="float", doc="Second position"),
        CustomArgumentSpec(name="repeats", type="int", doc="Number of A/B pairs"),
    ]
    builtins = [arg for arg in _BUILTIN_ARGUMENTS if arg.name in {"relative", "exp_time"}]
    builtins.sort(key=lambda arg: arg.default is not None)
    config = ScanConfig(
        name="alternating_scan",
        description="Alternating-position scan",
        scan_type="SOFTWARE_TRIGGERED",
        template_arguments=arguments + builtins,
    )
    return _render_scan(Path(scan.__file__).with_name("templates"), config)


def example_source(generated_source=None):
    tree = ast.parse(
        generated_source if generated_source is not None else generated_example_source()
    )
    scan_class = next(node for node in tree.body if isinstance(node, ast.ClassDef))
    constructor = next(
        node for node in scan_class.body if getattr(node, "name", None) == "__init__"
    )
    blocks = re.findall(r"```python\n(.*?)\n```", TUTORIAL.read_text(), re.DOTALL)
    for block in blocks:
        # Later blocks are client commands or the generated package export.
        if not (
            block.startswith("position_a:")
            or block.startswith("self.update_scan_info")
            or block.startswith("@scan_hook")
            or block.startswith("def _return_to_start")
        ):
            continue
        if block.startswith("position_a:"):
            edits = ast.parse("def inputs(\n" + block + "\n): pass").body[0].args.args
            for edit in edits:
                argument = next(arg for arg in constructor.args.args if arg.arg == edit.arg)
                argument.annotation = edit.annotation
            continue
        edits = ast.parse(block).body
        if block.startswith("self.update_scan_info"):
            constructor.body.extend(edits)
        else:
            for edit in edits:
                previous = next(
                    (node for node in scan_class.body if getattr(node, "name", None) == edit.name),
                    None,
                )
                if previous is None:
                    scan_class.body.append(edit)
                else:
                    scan_class.body[scan_class.body.index(previous)] = edit
    return ast.unparse(ast.fix_missing_locations(tree)) + "\n"


def example_class():
    module = ModuleType("documentation_alternating_scan")
    exec(compile(example_source(), str(TUTORIAL), "exec"), module.__dict__)
    return module.AlternatingScan


def documented_tests():
    blocks = re.findall(r"```python\n(.*?)\n```", HOW_TO.read_text(), re.DOTALL)
    return "\n\n".join(block for block in blocks if "def test_" in block)

---
related:
  - title: GUI tasks from the BEC IPython client
    url: how-to/gui/ipython-client-gui.md
  - title: Create Dock Area profiles from the BEC IPython client
    url: getting-started/next-steps/create-dock-area-profiles-from-ipython.md
  - title: BEC IPython GUI Commands
    url: getting-started/next-steps/gui-cli-interface.md
  - title: Control a Waveform from the IPython client
    url: how-to/gui/control-waveform-from-ipython.md
---

# Script GUI Setup and Run a Line Scan

!!! info "Goal"

    Put GUI setup and a line scan into a reusable Python function that you can import in the BEC IPython client.

Use this pattern when you want one command to prepare a dock area, configure widgets, and start a scan. This page shows
the script structure only; fill in the implementation for your beamline or plugin before using it.

## Prerequisites

- BEC is running with `Terminal + Dock`.
- The devices `samx`, `samy`, and `bpm4i` are available in `dev`.
- You have a script folder in a beamline or plugin repository.

## 1. Create the script

Create a Python file in your script folder, for example:

```text
scripts/alignment_gui.py
```

Add a function with the steps your workflow needs:

```python
def setup_gui_and_run_line_scan(gui, dev, scans):
    """Prepare a GUI layout and run a line scan."""
    # Clear or prepare the dock area for this workflow.
    # Example decision: remove existing widgets, or reuse widgets from the current layout.

    # Create or reuse the GUI widgets needed for the workflow.
    # Example widgets: ScanControl, Waveform, PositionerBox, Heatmap.

    # Configure devices and plots.
    # Example decisions:
    # - which motor should be scanned
    # - which signal should be plotted
    # - whether a DAP model should be attached

    # Run the line scan with the parameters for this workflow.
    # Example decision: start/stop range, number of steps, exposure time, relative mode.

    # Return useful references for interactive follow-up in the BEC IPython client.
    return {
        # "scan": scan,
        # "waveform": waveform,
        # "positioner": positioner,
    }
```

## 2. Import the script

If the script is inside an importable plugin package, use the package import path:

```python
from importlib import reload
from <plugin_package>.scripts import alignment_gui

reload(alignment_gui)
```

If the script folder is not part of a Python package, add it to `sys.path` first:

```python
import sys
from importlib import reload

sys.path.append("/path/to/plugin_repo/scripts")
import alignment_gui

reload(alignment_gui)
```

Use `reload(alignment_gui)` after editing the script so the IPython client sees the updated function.

## 3. Run the scripted setup

After filling in the function body for your workflow, call it from the BEC IPython client:

```python
widgets = alignment_gui.setup_gui_and_run_line_scan(gui, dev, scans)
```

The function should prepare the dock area, configure the widgets, run the line scan, and return references that are
useful for follow-up commands.

## 4. Continue interactively

Return widget references from your script when you want to adjust the GUI after the function runs:

```python
# Example after your script returns a Waveform reference:
# widgets["waveform"].clear_all()
# widgets["waveform"].plot(device_x=dev.samx, device_y=dev.bpm4i, dap="GaussianModel")
```

!!! success "Result"

    You have a script structure for one imported function that builds a GUI workflow and starts a line scan.

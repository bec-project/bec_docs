---
related:
  - title: Plotting and Data Analysis
    url: how-to/gui/ipython-client-gui.md
  - title: Access History with a Waveform
    url: how-to/gui/access-history-with-waveform.md
  - title: Access BEC History
    url: how-to/scans/access-bec-history.md
  - title: Create Dock Area profiles from the BEC IPython client
    url: getting-started/next-steps/create-dock-area-profiles-from-ipython.md
  - title: RPC GUI Control
    url: learn/gui/rpc-gui-control.md
  - title: Control a Waveform from the IPython client
    url: how-to/gui/control-waveform-from-ipython.md
---

# Script GUI Interactions

!!! info "Goal"

    Try a small BEC history analysis in the IPython client, smooth the data locally, fit it with a Waveform DAP curve,
    and then save the workflow as a script if you want to reuse it.

Start directly in the BEC IPython client. When the commands do what you want, move them into a small Python function in
your beamline or plugin repository.

## Prerequisites

- BEC is running with `Terminal + Dock`.
- At least one completed scan is available through `bec.history`.
- The `bpm4i` signal was recorded in the recent scans.
- You know the motor used for the scan, for example `samx`.
- The Python environment provides `numpy` and `scipy`.

## 1. Try the commands in IPython

Fetch the most recent scan, read the motor and signal data, and smooth the signal:

```python
import numpy as np
from scipy.ndimage import gaussian_filter1d

scan = bec.history[-1]
motor_name = "samx"
device_name = "bpm4i"
signal_name = "bpm4i"

x = np.asarray(scan.devices[motor_name][motor_name].read()["value"])
y = np.asarray(scan.devices[device_name][signal_name].read()["value"])

smoothed = gaussian_filter1d(y, sigma=2.0)
gradient = np.gradient(smoothed)
```

## 2. Plot the measurement and fit it with DAP

Create a Waveform and fill it with the measured signal, smoothed signal, and gradient. Attach a `GaussianModel` DAP
curve to the smoothed data:

```python
gui.bec.delete_all()
wf = gui.bec.new(gui.available_widgets.Waveform)

wf.title = f"{device_name} smoothed history fit"
wf.x_label = motor_name
wf.y_label = f"{device_name}-{signal_name}"

wf.plot(x=x, y=y, label="measured")
wf.plot(x=x, y=smoothed, label="smoothed", dap="GaussianModel")
wf.plot(x=x, y=gradient, label="gradient")
```

After the DAP curve has updated, inspect the fit output:

```python
wf.get_dap_summary()
wf.get_dap_params()
```

You can also read plotted data back from the Waveform and add another processed curve:

```python
data = wf.get_all_data()
smoothed_data = data["smoothed"]

x_from_waveform = np.asarray(smoothed_data["x"])
y_from_waveform = np.asarray(smoothed_data["y"])
y_shifted = y_from_waveform - np.min(y_from_waveform)

wf.plot(x=x_from_waveform, y=y_shifted, label="smoothed shifted")
```

!!! tip "Start in IPython, save later"

    Build the commands interactively first. After the plot and fit look useful, copy the working commands into a Python
    file so you can reuse them in later BEC IPython sessions.

## 3. Save the working commands as a script

Create a Python file in your script folder, for example:

```text
<beamline_plugin_repository>/scripts/history_gui_analysis.py
```

Put the working commands into a function. Keep `motor_name` explicit so the script is easy to read and does not need to
guess scan metadata:

```python
import numpy as np
from scipy.ndimage import gaussian_filter1d


def plot_smoothed_history_with_dap(
    gui,
    bec,
    *,
    motor_name,
    device_name="bpm4i",
    signal_name=None,
    count=3,
    smoothing_sigma=2.0,
    waveform=None,
):
    """Plot recent history scans, smoothed curves, gradients, and Gaussian DAP fits."""
    signal_name = signal_name or device_name
    scans = bec.history[-count:]
    if not scans:
        raise ValueError("No scans are available in bec.history.")

    if waveform is None:
        gui.bec.delete_all()
        wf = gui.bec.new(gui.available_widgets.Waveform)
    else:
        wf = waveform
        wf.clear_all()

    wf.title = f"{device_name} smoothed history fit"
    wf.x_label = motor_name
    wf.y_label = f"{device_name}-{signal_name}"

    plotted = []

    for index, scan in enumerate(scans, start=1):
        metadata = scan.metadata.get("bec", {})
        scan_number = metadata.get("scan_number", index)
        label_prefix = f"scan {scan_number}"

        x = np.asarray(scan.devices[motor_name][motor_name].read()["value"])
        y = np.asarray(scan.devices[device_name][signal_name].read()["value"])
        smoothed = gaussian_filter1d(y, sigma=smoothing_sigma)
        gradient = np.gradient(smoothed)

        wf.plot(x=x, y=y, label=f"{label_prefix}: measured")
        wf.plot(x=x, y=smoothed, label=f"{label_prefix}: smoothed", dap="GaussianModel")
        wf.plot(x=x, y=gradient, label=f"{label_prefix}: gradient")

        plotted.append(
            {
                "scan": scan,
                "scan_number": scan_number,
                "x": x,
                "measured": y,
                "smoothed": smoothed,
                "gradient": gradient,
            }
        )

    return {
        "waveform": wf,
        "plotted": plotted,
    }
```

## 4. Import the script

Beamline and plugin repositories are usually installed in the BEC environment in editable mode. If your script is inside
the plugin package, import it with the normal package path:

```python
from <plugin_package>.scripts import history_gui_analysis
```

For example, if your plugin package is called `my_beamline`:

```python
from my_beamline.scripts import history_gui_analysis
```

!!! tip "After editing the script"

    If the BEC IPython client is already running while you edit the file, restart the client or reload the module before
    calling the function again:

    ```python
    from importlib import reload

    reload(history_gui_analysis)
    ```

## 5. Run the scripted interaction

Call the function from the BEC IPython client:

```python
analysis = history_gui_analysis.plot_smoothed_history_with_dap(
    gui,
    bec,
    motor_name="samx",
    count=3,
)
```

The function creates a Waveform, plots the last three measured curves, plots smoothed and gradient curves, and attaches
Gaussian DAP fits to the smoothed curves.

## 6. Continue interactively

Use the returned objects when you want to inspect fit results or adjust the plot:

```python
wf = analysis["waveform"]
data = wf.get_all_data()

wf.get_dap_summary()
wf.title = "Updated smoothed history comparison"
```

!!! tip "Combine scripts with Dock Area profiles"

    A script does not have to create the full GUI from scratch. You can load a profile first, then fill the widgets that
    already exist in that profile:

    ```python
    gui.bec.load_profile("alignment_scan")
    wf = gui.bec.Waveform
    analysis = history_gui_analysis.plot_smoothed_history_with_dap(
        gui,
        bec,
        motor_name="samx",
        count=3,
        waveform=wf,
    )
    ```

    To start from the saved baseline version of a profile, use:

    ```python
    gui.bec.load_profile("alignment_scan", restore_baseline=True)
    ```

    This is the short form for loading the profile after restoring its runtime copy from the baseline. You can also call
    the restore step explicitly:

    ```python
    gui.bec.restore_baseline_profile("alignment_scan", show_dialog=False)
    ```

!!! success "Result"

    You have a reusable script pattern that combines BEC history access, Python analysis, and GUI plotting.

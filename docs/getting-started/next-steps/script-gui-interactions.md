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
    and continue adjusting the plot interactively.

Start directly in the BEC IPython client. This page shows how normal Python analysis can be combined with Waveform
plotting without turning the workflow into an automated control script.

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

## 3. Continue interactively

Use the Waveform reference when you want to inspect fit results or adjust the plot:

```python
data = wf.get_all_data()

wf.get_dap_summary()
wf.title = "Updated smoothed history comparison"
```

You can keep adding derived curves while you inspect the data:

```python
gradient_abs = np.abs(gradient)
wf.plot(x=x, y=gradient_abs, label="absolute gradient")
```

!!! tip "Use a profile when the layout already exists"

    You do not have to create the Waveform from scratch. You can load a Dock Area profile first, then fill the widgets
    that already exist in that profile:

    ```python
    gui.bec.load_profile("alignment_scan")
    wf = gui.bec.Waveform
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

    You combined BEC history access, Python analysis, Waveform plotting, and DAP fitting from the BEC IPython client.

<!--
TODO: Revisit as a dedicated, safety-reviewed scripting tutorial.

The script-saving workflow was intentionally removed from the published page for now.
When this topic returns, write it as a dedicated tutorial with clear boundaries for
which GUI interactions are appropriate to automate and which should remain manual.
-->

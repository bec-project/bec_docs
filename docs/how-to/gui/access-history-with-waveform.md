---
related:
  - title: Plotting and Data Analysis
    url: how-to/gui/ipython-client-gui.md
  - title: Access BEC History
    url: how-to/scans/access-bec-history.md
  - title: Control a Waveform from the IPython Client
    url: how-to/gui/control-waveform-from-ipython.md
  - title: Script GUI Interactions
    url: getting-started/next-steps/script-gui-interactions.md
---

# Access History with a Waveform

!!! info "Goal"

    Plot data from a completed scan in a Waveform and know when to use `bec.history` directly.

Use `bec.history` when you want scan data as Python objects. Use a Waveform history curve when you want to inspect a
previous scan in the GUI or attach a DAP curve to it.

!!! info "Live curves and history curves"

    A Waveform curve is a live device curve unless you pass `scan_number` or `scan_id` to `wf.plot(...)`.
    For example, `wf.plot(device_x="samx", device_y="bpm4i")` follows live BEC scan updates. If the Waveform does
    not yet have a scan attached, it initializes from the current scan when one exists, or from the latest history
    entry otherwise. This is useful for live plotting because the curve can show the most recently measured data and
    then update with later scans. Use `scan_number` or `scan_id` when you want a fixed history curve that is not
    replaced by live-scan updates.

## Prerequisites

- BEC is running with `Terminal + Dock`.
- At least one completed scan is available through `bec.history`.
- The history scan contains `samx` and `bpm4i` data.

## 1. Inspect the latest scan directly

Fetch the latest completed scan from BEC history:

```python
scan = bec.history[-1]
```

Read the motor and signal arrays directly:

```python
x = scan.devices.samx.samx.read()["value"]
y = scan.devices.bpm4i.bpm4i.read()["value"]
```

Use this path when you want to do Python analysis yourself, pass the data to another package, or inspect metadata:

```python
scan.metadata["bec"]
```

For a fuller guide to direct history access, see
[Access BEC History](../scans/access-bec-history.md){ data-preview }.

## 2. Plot the latest scan in a Waveform

Create a Waveform:

```python
wf = gui.bec.new(gui.available_widgets.Waveform)
```

Add a history curve for the latest scan:

```python
wf.plot(
    device_x="samx",
    device_y="bpm4i",
    scan_number=-1,
    label="latest bpm4i history",
)
```

For `scan_number`, negative values behave like history list indices. `-1` means the latest scan, `-2` means the scan
before that. Positive values are resolved as BEC scan numbers.

## 3. Plot a specific scan ID

Use a scan ID when you want to refer to one exact scan:

```python
scan = bec.history[-1]
scan_id = scan.metadata["bec"]["scan_id"]

wf.plot(
    device_x="samx",
    device_y="bpm4i",
    scan_id=scan_id,
    label=f"bpm4i {scan_id}",
)
```

## 4. Add a DAP curve to history data

History curves can be fitted by DAP in the same way as live or custom curves:

```python
wf.plot(
    device_x="samx",
    device_y="bpm4i",
    scan_number=-1,
    label="latest bpm4i fit",
    dap="GaussianModel",
)
```

Inspect the fit output:

```python
wf.get_dap_summary()
wf.get_dap_params()
```

## 5. Use the GUI history browser

You can also add history curves from the Waveform GUI:

1. Open the Waveform scan history browser from the plot toolbar :material-manage-search:.
2. Select the scan, device, and signal you want to inspect.
3. Add the selected history signal to the Waveform.

## 6. Read data back from the Waveform

After plotting, retrieve the curve data from the Waveform:

```python
data = wf.get_all_data()
```

The result is a dictionary keyed by curve label:

```python
data["latest bpm4i history"]["x"]
data["latest bpm4i history"]["y"]
```

## Large datasets

History curves can be big — an async detector can easily store hundreds of millions of points in one scan. The
Waveform protects the GUI in three ways, without hiding any data:

- **Confirmation before loading.** When the stored dataset exceeds the size limit (10 MB by default), a
  *Large dataset detected* dialog reports the affected signal and its size before anything is read. You can load it
  anyway, adjust the limit, or suppress the dialog for the session. The same knobs are scriptable:

    ```python
    wf.max_dataset_size_mb = 100          # raise the limit
    wf.skip_large_dataset_warning = True  # no dialog for this session
    ```

- **Loading progress.** While a confirmed large dataset is read from the file, a progress bar below the plot shows
  how far the load has come — the GUI stays responsive during the read.

- **Detail-preserving display.** Curves beyond a million points are drawn as a min/max envelope, so spikes and
  outliers remain visible at full zoom-out. The raw data is kept: zooming in re-renders the visible window at
  progressively finer detail, down to the individual samples.

!!! success "Result"

    You can inspect scan history directly through `bec.history`, plot it in a Waveform, fit history curves with DAP,
    and retrieve plotted curve data with `wf.get_all_data()`.

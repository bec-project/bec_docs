---
related:
  - title: Control the GUI from the IPython client
    url: getting-started/next-steps/gui-cli-interface.md
  - title: Use simulated models from the IPython client
    url: how-to/gui/use-simulated-models-from-ipython.md
  - title: GUI RPC interface reference
    url: references/bec-widgets/gui-rpc-interface.md
---

# Control a Waveform from the IPython Client

!!! info "Goal"

    Create or reuse a Waveform widget from the BEC IPython client, plot device data, and add a
    DAP model curve.

## Prerequisites

- BEC is running with a dock area.
- The `samx` and `bpm4i` devices are available in `dev`.

!!! note "Device names"

    In these examples, `samx` is a simulated positioner motor and `bpm4i` is a
    Beam Position Monitor.

## 1. Create a Waveform

Create a new Waveform in the default dock area:

```python
wf = gui.bec.new(gui.available_widgets.Waveform)
```

If the profile already contains a Waveform, use the widget from the dock area namespace instead:

```python
wf = gui.bec.Waveform
```

## 2. Plot device data

Plot `bpm4i` against the `samx` motor position:

```python
wf.plot(device_x=dev.samx, device_y=dev.bpm4i)
```

Run a scan to produce live data:

```python
scans.line_scan(dev.samx, -5, 5, steps=25, exp_time=0.1, relative=False)
```

## 3. Add a DAP model curve

Attach a Gaussian DAP model to the existing `bpm4i` curve:

```python
wf.add_dap_curve(device_label="bpm4i-bpm4i", dap_name="GaussianModel")
```

`device_label` is the existing source curve to fit. For this example, the default source
curve label is `bpm4i-bpm4i`, built from the y-axis device and signal. `dap_name` is the
DAP model to attach to that source curve.

Inspect the DAP result summary:

```python
wf.get_dap_summary()
```

Use the same model names as the LMFit built-in model classes, such as `GaussianModel`.

!!! tip "Add DAP when creating the curve"

    If you know that the curve should have a DAP model from the start, add it in the
    initial `plot` call:

    ```python
    wf.plot(device_x=dev.samx, device_y=dev.bpm4i, dap="GaussianModel")
    ```

    Do not call `plot` again with the same device pair after the source curve already
    exists. That creates a duplicate source curve and raises an error. Use
    `wf.add_dap_curve(device_label="bpm4i-bpm4i", dap_name="GaussianModel")` to add a DAP
    model to an existing curve.

## GUI equivalent

You can configure the same plot from the Waveform curve settings dialog:

1. Open the Waveform curve settings dialog from the plot toolbar :material-chart-timeline-variant:.
2. Set the x-axis mode to `device`.
3. Set the x-axis device to `samx`.
4. Add a y-axis curve for `bpm4i`.
5. Add the `GaussianModel` DAP model to the curve.
6. Confirm the dialog and run the scan.

!!! success "Result"

    The Waveform shows the device curve and the fitted DAP model curve.

## Related tasks

- Use [Use Simulated Models from the IPython Client](use-simulated-models-from-ipython.md){ data-preview }
  to make `bpm4i` produce Gaussian-shaped simulated data.
- Use [Script GUI Behaviour](script-gui-behaviour.md){ data-preview } to apply the same setup
  from a reusable script.

---
related:
  - title: Plotting and Data Analysis
    url: how-to/gui/ipython-client-gui.md
  - title: Fit Waveform Data with DAP
    url: how-to/gui/fit-waveform-data-with-dap.md
  - title: Access History with a Waveform
    url: how-to/gui/access-history-with-waveform.md
  - title: Script GUI interactions
    url: getting-started/next-steps/script-gui-interactions.md
  - title: Use simulated models from the IPython client
    url: how-to/devices/use-simulated-models-from-ipython.md
  - title: GUI RPC interface reference
    url: references/bec-widgets/gui-rpc-interface.md
---

# Plot Data using the IPython Client

!!! info "Goal"

    Create or reuse a Waveform widget from the BEC IPython client, plot device data, adjust plot and curve properties,
    and retrieve plotted data.

## Prerequisites

- BEC is running with a Dock Area.
- The `samx` and `bpm4i` devices are available in `dev`.

!!! info "Device names"

    In these examples, `samx` is a simulated positioner motor and `bpm4i` is a
    Beam Position Monitor.

## 1. Create a Waveform

Create a new Waveform in the default Dock Area:

```python
wf = gui.bec.new(gui.available_widgets.Waveform)
```

If the profile already contains a Waveform, use the widget from the Dock Area namespace instead:

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

## 3. Adjust the Waveform from IPython

The Waveform exposes plot properties through the same command interface:

```python
wf.title = "bpm4i intensity during samx scan"
wf.x_label = "samx position"
wf.y_label = "bpm4i signal"
wf.x_grid = True
wf.y_grid = True
```

Curve items are also exposed below the Waveform when they are RPC-visible. Use `get_curve(...)` when you want an
explicit reference to a curve:

```python
curve = wf.get_curve("bpm4i-bpm4i")
curve.set_color("#1f77b4")
curve.set_symbol("o")
curve.set_symbol_size(7)
curve.set_pen_width(2)
```

The same curve can usually also be reached through the Waveform namespace:

```python
wf.bpm4i_bpm4i.set_color("red")
```

!!! tip "Discover available methods"

    Use tab completion on `wf.` or `curve.` to see exposed methods and properties. Use `?` to inspect the docstring for
    a method, for example `wf.plot?` or `curve.set_color?`.

## 4. Read plotted data back from the Waveform

The Waveform can also return the data that is currently plotted:

```python
data = wf.get_all_data()
```

The result is a dictionary keyed by curve label:

```python
data["bpm4i-bpm4i"]["x"]
data["bpm4i-bpm4i"]["y"]
```

Use this when you want to inspect a plotted curve, pass it to another Python package, or compare it with processed data.

## GUI equivalent

You can configure the same device plot from the Waveform curve settings dialog:

1. Open the Waveform curve settings dialog from the plot toolbar :material-chart-timeline-variant:.
2. Set the x-axis mode to `device`.
3. Set the x-axis device to `samx`.
4. Add a y-axis curve for `bpm4i`.
5. Confirm the dialog and run the scan.

!!! success "Result"

    The Waveform shows the device curve, and you can adjust the plot and curve properties from the BEC IPython client.

## Related tasks

- Use [Fit Waveform Data with DAP](fit-waveform-data-with-dap.md){ data-preview }
  when you want to attach one or more DAP model curves to Waveform data.
- Use [Use Simulated Models from the IPython Client](../devices/use-simulated-models-from-ipython.md){ data-preview }
  to make `bpm4i` produce predictable simulated data.
- Use [Access History with a Waveform](access-history-with-waveform.md){ data-preview }
  to plot completed scans from history.
- Use [Script GUI Interactions](../../getting-started/next-steps/script-gui-interactions.md){ data-preview }
  to combine BEC history access, Python analysis, and GUI plotting from a reusable function.

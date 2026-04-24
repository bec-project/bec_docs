---
related:
  - title: Plot your first waveform
    url: getting-started/quick-start/05-plot-your-first-waveform.md
  - title: Save and switch GUI profiles
    url: getting-started/next-steps/save-and-switch-gui-profiles.md
  - title: Learn about RPC GUI control
    url: learn/gui/rpc-gui-control.md
---

# Control the GUI from the IPython Client

!!! info "Goal"

    Use the BEC IPython client to create a GUI widget, configure it, run a scan, and save the
    resulting dock area as a reusable profile.

## Before you start

Open BEC with `Terminal + Dock`, as shown in
[01 Open BEC](../quick-start/01-open-bec.md){ data-preview }.

This tutorial assumes that your session contains the simulated devices `samx` and `bpm4i`.

## 1. Inspect the GUI object

The IPython client provides a `gui` object. The default dock area is available as `gui.bec`.

```python
gui
gui.bec
```

List the widgets that can be created from the client:

```python
gui.available_widgets
```

## 2. Create a Waveform

Create a `Waveform` in the default dock area:

```python
wf = gui.bec.new(gui.available_widgets.Waveform)
```

The widget is also available from the dock area namespace:

```python
gui.bec.Waveform
```

!!! tip "Discover available methods"

    Exposed widget methods are available through IPython tab completion. Type `wf.` and
    press ++tab++ to inspect the methods available on the widget RPC object. To see the
    parameters and documentation for a method, use `?`, for example `wf.plot?`.

## 3. Plot device data

Configure the waveform to plot `bpm4i` against `samx`:

```python
wf.plot(device_x=dev.samx, device_y=dev.bpm4i)
```

## 4. Run a scan

Run a line scan and watch the waveform update:

```python
scans.line_scan(dev.samx, -5, 5, steps=10, exp_time=0.1, relative=False)
```

## 5. Save the layout as a profile

Save the current dock area as the `alignment_cli` profile:

```python
gui.bec.save_profile("alignment_cli")
```

Load the profile again when you want to return to this layout:

```python
gui.bec.load_profile("alignment_cli")
```

!!! success "What you have learned"

    You used the RPC GUI interface to create and configure a widget from the IPython client,
    then saved the GUI layout as a profile.

## Next step

Use [Script GUI Behaviour](../../how-to/gui/script-gui-behaviour.md){ data-preview } when you
want to turn this workflow into a reusable script.

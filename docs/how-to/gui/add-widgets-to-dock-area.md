---
related:
  - title: Plotting and Data Analysis
    url: how-to/gui/ipython-client-gui.md
  - title: Create Dock Area profiles from the BEC IPython client
    url: getting-started/next-steps/create-dock-area-profiles-from-ipython.md
  - title: GUI RPC interface reference
    url: references/bec-widgets/gui-rpc-interface.md
  - title: RPC GUI Control
    url: learn/gui/rpc-gui-control.md
---

# Add Widgets to a Dock Area

!!! info "Goal"

    Add BEC Widgets to an existing Dock Area from the BEC IPython client and control where they appear.

Use this guide when you already have BEC running with a Dock Area and want to add widgets with commands instead of the
toolbar. The examples use `gui.bec`, which is the default Dock Area in the `Terminal + Dock` layout.

## Prerequisites

- BEC is running with a Dock Area.
- You are using the BEC IPython client.

## 1. Choose a widget

Available widget classes are exposed through `gui.available_widgets`. Use tab completion to inspect the available
widgets. In the BEC IPython client, type `gui.available_widgets.` and press the tab key.

```python
gui.available_widgets
```

For example, `Waveform`, `PositionerBox`, and `ScanControl` can be created from the Dock Area:

```python
gui.available_widgets.Waveform
gui.available_widgets.PositionerBox
gui.available_widgets.ScanControl
```

## 2. Add a widget

Use `gui.bec.new(...)` to add a widget to the Dock Area:

```python
wf = gui.bec.new(gui.available_widgets.Waveform)
```

The returned object is the widget reference. Keep it in a variable when you want to configure it immediately:

```python
wf.title = "bpm4i during samx scan"
wf.x_label = "samx"
wf.y_label = "bpm4i"
```

## 3. Place a widget relative to another widget

Use `where` and `relative_to` when the new widget should be placed next to an existing widget. In the BEC IPython
client, use the dock tab name as the reference:

```python
pos = gui.bec.new(
    gui.available_widgets.PositionerBox,
    where="bottom",
    relative_to="Waveform",
)
pos.set_positioner("samx")
```

`where` can be `"left"`, `"right"`, `"top"`, or `"bottom"`.

Add another widget to the right of the same Waveform:

```python
wf2 = gui.bec.new(
    gui.available_widgets.Waveform,
    where="right",
    relative_to="Waveform",
)
```

!!! tip "Use existing widget names"

    From the BEC IPython client, `relative_to` uses the name shown on the dock tab, for example `"Waveform"`,
    `"ScanControl"`, or `"PositionerBox"`.

    If the same widget type appears multiple times, Dock Area indexes the repeated names. The first widget keeps the base
    name, and later widgets use names such as `"Waveform_0"` and `"Waveform_1"`.

## 4. Add a widget as a tab

Use `tab_with` when the new widget should share the same dock area as another widget:

```python
wf_history = gui.bec.new(
    gui.available_widgets.Waveform,
    tab_with="Waveform",
)
wf_history.title = "History comparison"
```

You can tab more widgets with the same named dock:

```python
scan = gui.bec.new(
    gui.available_widgets.ScanControl,
    tab_with="Waveform",
)
```

## 5. Inspect the Dock Area

List the BEC Widgets currently contained in the Dock Area:

```python
gui.bec.widget_map()
gui.bec.widget_list()
```

Inspect the splitter layout when you need to understand how widgets are arranged:

```python
gui.bec.describe_layout()
```

## 6. Remove widgets when needed

Remove one widget by dock name:

```python
gui.bec.delete("Waveform_0")
```

Clear the full Dock Area:

```python
gui.bec.delete_all()
```

!!! warning "Deleting widgets changes the current layout"

    If the current Dock Area profile is saved later, the saved profile will contain the updated layout. Save under a new
    profile name when you want to keep the original layout.

!!! success "Result"

    You added widgets to a Dock Area, placed them relative to existing widgets, created tabbed widgets, and inspected the
    resulting layout from the BEC IPython client.

## Related tasks

- Use [Plot Data using the IPython Client](control-waveform-from-ipython.md){ data-preview } when the widget you added
  is a Waveform and you want to plot device data.
- Use
  [Create Dock Area Profiles from the BEC IPython Client](../../getting-started/next-steps/create-dock-area-profiles-from-ipython.md){ data-preview }
  when the layout should be saved as a reusable Dock Area profile.

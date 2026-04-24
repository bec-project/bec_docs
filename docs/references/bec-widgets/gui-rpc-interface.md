---
related:
  - title: RPC GUI control
    url: learn/gui/rpc-gui-control.md
  - title: Control a Waveform from the IPython client
    url: how-to/gui/control-waveform-from-ipython.md
  - title: Script GUI behaviour
    url: how-to/gui/script-gui-behaviour.md
---

# GUI RPC Interface

This page lists common GUI RPC objects and methods used from the BEC IPython client.

## Common objects

| Object | Purpose |
| --- | --- |
| `gui` | GUI client entry point. |
| `gui.bec` | Default `BECDockArea` RPC reference. |
| `gui.available_widgets` | Widget classes available for remote creation. |
| `gui.bec.Waveform` | Dynamic reference to a Waveform in the dock area. |

## GUI client

| API | Use |
| --- | --- |
| `gui.show()` | Show the GUI. |
| `gui.hide()` | Hide the GUI. |
| `gui.raise_window()` | Bring the GUI window to the front. |
| `gui.new(...)` | Create a top-level GUI widget or window. |
| `gui.windows` | Access known GUI windows. |
| `gui.window_list` | List available windows. |
| `gui.available_widgets` | Inspect creatable widget classes. |

## Dock area

| API | Use |
| --- | --- |
| `gui.bec.new(gui.available_widgets.Waveform)` | Add a widget to the dock area. |
| `gui.bec.widget_map` | Inspect named widgets in the dock area. |
| `gui.bec.widget_list` | List widgets in the dock area. |
| `gui.bec.load_profile("alignment_cli")` | Load a profile. |
| `gui.bec.save_profile("alignment_cli")` | Save the current layout. |
| `gui.bec.restore_user_profile_from_default("alignment_cli", show_dialog=False)` | Restore a profile from its default copy without a confirmation dialog. |
| `gui.bec.delete_profile("name")` | Delete a local profile. |

## Waveform

| API | Use |
| --- | --- |
| `wf.plot(device_x=dev.samx, device_y=dev.bpm4i)` | Plot device data. |
| `wf.plot(..., dap="GaussianModel")` | Plot data and attach a DAP model. |
| `wf.add_dap_curve(device_label="bpm4i-bpm4i", dap_name="GaussianModel")` | Add a DAP curve to an existing source curve. |
| `wf.get_dap_params()` | Read DAP model parameters. |
| `wf.get_dap_summary()` | Read DAP output summaries. |
| `wf.get_curve(0)` | Access a curve by index or label. |
| `wf.get_all_data()` | Read all plotted curve data. |
| `wf.clear_all()` | Remove all curves. |
| `wf.x_mode` | Get or set the x-axis mode. |
| `wf.signal_x` | Get or set the x-axis signal name. |

## Common patterns

Create a Waveform and plot a device:

```python
wf = gui.bec.new(gui.available_widgets.Waveform)
wf.plot(device_x=dev.samx, device_y=dev.bpm4i)
```

Load a prepared profile and update the Waveform:

```python
gui.bec.load_profile("alignment_cli")
wf = gui.bec.Waveform
wf.clear_all()
wf.plot(device_x=dev.samx, device_y=dev.bpm4i, dap="GaussianModel")
```

Restore a shipped default profile from a script:

```python
gui.bec.restore_user_profile_from_default("alignment_cli", show_dialog=False)
```

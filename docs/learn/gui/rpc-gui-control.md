---
related:
  - title: BEC IPython GUI Commands
    url: getting-started/next-steps/gui-cli-interface.md
  - title: Create Dock Area profiles from the BEC IPython client
    url: getting-started/next-steps/create-dock-area-profiles-from-ipython.md
  - title: GUI RPC interface reference
    url: references/bec-widgets/gui-rpc-interface.md
---

# RPC GUI Control

The BEC IPython client can control GUI widgets through RPC. This lets users create widgets,
configure plots, load profiles, and script GUI behaviour from the command line.

## Main objects

`gui` is the client-side GUI entry point. It exposes windows, available widget classes, and
helpers to create or show GUI elements.

`gui.bec` is the default dock area opened by the `Terminal + Dock` launcher mode. It is a
client-side reference to a `BECDockArea` running in the GUI process.

`gui.available_widgets` lists widget classes that can be created remotely:

```python
gui.bec.new(gui.available_widgets.Waveform)
```

## RPC references

Objects returned by the GUI client are RPC references. A variable such as `wf` does not contain
the Qt widget itself. It contains a reference that sends allowed method calls and property access
to the GUI process.

```python
wf = gui.bec.new(gui.available_widgets.Waveform)
wf.plot(device_x=dev.samx, device_y=dev.bpm4i)
```

The dock area also exposes created widgets through a dynamic namespace. The first Waveform in
`gui.bec` can usually be reached as:

```python
gui.bec.Waveform
```

If a widget is deleted, an existing RPC reference to that widget is no longer useful. Get a new
reference from the dock area namespace, create the widget again, or reload the profile that
contains it.

## Exposed API surface

Only methods and properties listed in a widget's `USER_ACCESS` are exposed through RPC. This is
intentional: it keeps command-line control focused on stable user-facing operations instead of
internal Qt implementation details.

Examples of exposed operations include:

- `gui.bec.new(...)` to add a widget to a dock area.
- `gui.bec.load_profile(...)` to load a dock area profile.
- `gui.bec.restore_runtime_profile_from_baseline(..., show_dialog=False)` for scripted profile restore.
- `wf.plot(...)` and `wf.get_dap_summary()` for Waveform control.

## Timeouts and long operations

RPC calls wait for the GUI process to complete the requested operation. Most calls return
quickly, but profile loading, history access, or data-heavy plotting may take longer. If a call
times out, check whether the GUI process is responsive and whether the operation requested a very
large data set.

For repeatable workflows, prefer loading a saved profile first and then changing only the widget
settings that depend on the current experiment.

## Reacting to BEC callbacks

The IPython client can also run user callbacks when BEC publishes events. A common event for GUI
scripting is `scan_status`. It reports when a scan opens, pauses, closes, aborts, or halts.

Scan-status callbacks receive two arguments:

| Argument | Meaning |
| --- | --- |
| `content` | Message content as a dictionary. |
| `metadata` | Message metadata as a dictionary. |

Convert the content into a `ScanStatusMessage` when you want typed access to scan fields:

```python
from bec_lib.messages import ScanStatusMessage


def on_scan_status(content, metadata):
    msg = ScanStatusMessage(**content, metadata=metadata)
```

Useful fields include:

| Field | Use |
| --- | --- |
| `status` | Scan lifecycle state, for example `open` or `closed`. |
| `scan_name` | Scan type, for example `line_scan` or `grid_scan`. |
| `scan_number` | Human-readable scan number. |
| `scan_report_devices` | Devices used as scan axes. |
| `readout_priority` | Devices grouped by readout priority, including monitored devices. |

Callbacks are registered on `bec.callbacks`:

```python
callback_id = bec.callbacks.register(
    event_type="scan_status", callback=on_scan_status, sync=True
)
```

Use `sync=True` when the callback performs GUI RPC calls. Synchronous callbacks are queued and
polled by the IPython client during scan reporting. This avoids running GUI RPC calls from the
background callback thread and makes failures easier to diagnose.

Remove callbacks when the scripted behaviour should stop:

```python
bec.callbacks.remove(callback_id)
```

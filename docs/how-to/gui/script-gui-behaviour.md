---
related:
  - title: Control the GUI from the IPython client
    url: getting-started/next-steps/gui-cli-interface.md
  - title: Switch GUI profiles
    url: how-to/gui/switch-gui-profile.md
  - title: Add changes to your plugin repository
    url: how-to/git/add-changes-to-plugin-repository.md
---

# Script GUI Behaviour

!!! info "Goal"

    Use an IPython script to load a prepared GUI profile and adapt widgets to the current
    beamline workflow.

## Recommended approach

Use profile-first scripting:

1. Build and save the GUI layout interactively, for example as `alignment_cli`.
2. Load or restore that profile from the IPython client or from a script.
3. Access the widgets from `gui.bec`.
4. Apply script logic based on active devices, scan state, or the user workflow.

This keeps widget placement and docking layout in the profile, while scripts handle runtime
choices such as devices, DAP models, scan setup, or display settings.

## Simple scripts

Use a simple script when the GUI setup should happen once, before you run the scan.

### Without a profile

This version builds the needed widget from the script:

```python
wf = gui.bec.new(gui.available_widgets.Waveform)
wf.plot(device_x=dev.samx, device_y=dev.bpm4i, dap="GaussianModel")
```

This is useful for quick testing, but it mixes GUI construction and experiment logic in the
same script.

??? example "Full simple script without a profile"

    ```python
    def get_or_create_waveform(gui):
        try:
            return gui.bec.Waveform
        except AttributeError:
            return gui.bec.new(gui.available_widgets.Waveform)


    wf = get_or_create_waveform(gui)
    wf.clear_all()
    wf.plot(device_x=dev.samx, device_y=dev.bpm4i, dap="GaussianModel")
    ```

### With a profile

Profile-first scripting is preferred for reusable GUI workflows. Build the layout once with
normal GUI interactions, save it as `alignment_cli`, then let the script load the profile and
only change runtime settings:

```python
gui.bec.load_profile("alignment_cli")
wf = gui.bec.Waveform
wf.clear_all()
wf.plot(device_x=dev.samx, device_y=dev.bpm4i, dap="GaussianModel")
```

If the beamline ships `alignment_cli` as a default profile and you want to discard local
changes before running the script, restore it without the GUI confirmation dialog:

```python
gui.bec.restore_user_profile_from_default("alignment_cli", show_dialog=False)
```

??? example "Full profile-first script"

    ```python
    def get_or_create_waveform(gui):
        try:
            return gui.bec.Waveform
        except AttributeError:
            return gui.bec.new(gui.available_widgets.Waveform)


    try:
        gui.bec.load_profile("alignment_cli")
    except Exception as exc:
        print(f"Could not load profile 'alignment_cli': {exc}")
        print("Continuing with the current dock area.")

    wf = get_or_create_waveform(gui)
    wf.clear_all()
    wf.plot(device_x=dev.samx, device_y=dev.bpm4i, dap="GaussianModel")
    ```

Run a scan after the script has configured the GUI:

```python
scans.line_scan(dev.samx, -5, 5, steps=25, exp_time=0.1, relative=False)
```

## React to BEC scan information

Use a reactive script when the GUI should adapt to the scan that is currently running.

The example below listens for `scan_status` updates. When a `line_scan` opens, it shows a
Waveform with one monitored device. When a `grid_scan` opens, it shows a Heatmap with the two
scan motors as x/y axes and the selected monitored device as z.

```python
callback_id = bec.callbacks.register(
    event_type="scan_status", callback=on_scan_status, sync=True
)
```

Use `sync=True` for GUI RPC calls from scan callbacks. BEC polls synchronous callbacks while
the scan report is running, so the GUI call is executed from the IPython callback polling path
instead of a background callback thread.

??? example "Full reactive script"

    ```python
    import traceback

    from bec_lib.messages import ScanStatusMessage


    def pick_y_device(msg, selected_device="bpm4i"):
        if selected_device:
            return selected_device
        readout_priority = msg.readout_priority or {}
        monitored = readout_priority.get("monitored") or []
        return monitored[0] if monitored else None


    def configure_waveform_for_line_scan(gui, msg, selected_device="bpm4i"):
        if msg.status != "open" or not msg.scan_report_devices:
            return None

        device_x = msg.scan_report_devices[0]
        device_y = pick_y_device(msg, selected_device=selected_device)
        if not device_y:
            return None

        gui.bec.delete_all()
        wf = gui.bec.new(gui.available_widgets.Waveform)
        wf.plot(
            device_x=device_x,
            device_y=device_y,
            label=f"Scan {msg.scan_number} - {device_y}",
        )
        return wf


    def configure_heatmap_for_grid_scan(gui, msg, selected_device="bpm4i"):
        if msg.status != "open":
            return None
        if not msg.scan_report_devices or len(msg.scan_report_devices) < 2:
            return None

        device_x, device_y = msg.scan_report_devices[:2]
        device_z = pick_y_device(msg, selected_device=selected_device)
        if not device_z:
            return None

        gui.bec.delete_all()
        heatmap = gui.bec.new(gui.available_widgets.Heatmap)
        heatmap.plot(device_x=device_x, device_y=device_y, device_z=device_z)
        return heatmap


    def on_scan_status(content, metadata):
        try:
            msg = ScanStatusMessage(**content, metadata=metadata)
            scan_report_devices = msg.scan_report_devices or []
            if msg.status != "open":
                return

            if msg.scan_name == "line_scan" or len(scan_report_devices) == 1:
                configure_waveform_for_line_scan(gui, msg)
            elif msg.scan_name == "grid_scan" or len(scan_report_devices) >= 2:
                configure_heatmap_for_grid_scan(gui, msg)
        except Exception:
            print("Failed to update GUI from scan_status callback:")
            print(traceback.format_exc())


    callback_id = bec.callbacks.register(
        event_type="scan_status", callback=on_scan_status, sync=True
    )
    ```

Run scans to test the reactive behaviour:

```python
scans.line_scan(dev.samx, -5, 5, steps=25, exp_time=0.1, relative=False)
scans.grid_scan(
    dev.samx, -5, 5, 10,
    dev.samy, -5, 5, 10,
    exp_time=0.1,
    relative=False,
)
```

Remove the callback when the scripted behaviour should stop:

```python
bec.callbacks.remove(callback_id)
```

## Store reusable scripts

Store reusable GUI scripts in the beamline or plugin repository script folder if your
beamline uses one. Store reusable functions or macros in the repository `scripts/` or `macros/` folder
where applicable.

After changing repository scripts or macros, follow the Git workflow:

- [Add Changes to Your Plugin Repository](../git/add-changes-to-plugin-repository.md){ data-preview }
- [Merge Changes to main](../git/merge-changes-to-main.md){ data-preview }

!!! success "Result"

    The profile provides a stable GUI layout, and the script applies the runtime behaviour
    needed for the current experiment.

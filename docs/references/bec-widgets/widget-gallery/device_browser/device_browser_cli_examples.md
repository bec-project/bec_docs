<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/services/device_browser/device_browser.py
- Public example surface: DeviceBrowser is PLUGIN=True with ICON_NAME="lists" and no widget-specific USER_ACCESS list; only base BECWidget operations should be shown from CLI.
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.DeviceBrowser).
-->

Create a DeviceBrowser widget:

```python
devices = gui.bec.new(gui.available_widgets.DeviceBrowser)
```

Place it beside the current Waveform:

```python
devices = gui.bec.new(
    gui.available_widgets.DeviceBrowser,
    where="right",
    relative_to="Waveform",
)
```

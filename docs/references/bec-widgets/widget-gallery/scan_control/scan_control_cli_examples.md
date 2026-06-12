<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/control/scan_control/scan_control.py
- Public example surface: USER_ACCESS is attach, detach, screenshot. Constructor accepts allowed_scans and default_scan, but scan submission is GUI-driven rather than exposed as a CLI method.
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.ScanControl).
-->

Create a ScanControl widget:

```python
scan_control = gui.bec.new(gui.available_widgets.ScanControl)
```

Place it next to an existing Waveform by dock name:

```python
scan_control = gui.bec.new(
    gui.available_widgets.ScanControl,
    where="left",
    relative_to="Waveform",
)
```

Detach or attach the widget window:

```python
scan_control.detach()
scan_control.attach()
```

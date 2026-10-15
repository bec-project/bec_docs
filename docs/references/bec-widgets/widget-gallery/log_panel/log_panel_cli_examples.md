<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/utility/logpanel/logpanel.py
- Public example surface: LogPanel is PLUGIN=True with ICON_NAME="browse_activity". The source does not expose a widget-specific USER_ACCESS list, so examples are limited to creation and dock placement.
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.LogPanel).
-->

Create a LogPanel:

```python
logs = gui.bec.new(gui.available_widgets.LogPanel)
```

Place it below an existing Waveform:

```python
logs = gui.bec.new(
    gui.available_widgets.LogPanel,
    where="bottom",
    relative_to="Waveform",
)
```

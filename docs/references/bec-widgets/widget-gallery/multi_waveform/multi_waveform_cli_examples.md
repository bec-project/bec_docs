<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/plots/multi_waveform/multi_waveform.py
- Public example surface: USER_ACCESS includes plot, monitor, monitor.setter, set_curve_limit, set_curve_highlight, clear_curves, color_palette, opacity, flush_buffer, max_trace; plot(monitor: str, color_palette: str | None = "plasma").
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.MultiWaveform).
-->

Create the widget and connect it to a monitor signal. Replace `waveform_monitor` with the monitor available at your beamline:

```python
mwf = gui.bec.new(gui.available_widgets.MultiWaveform)
mwf.plot("waveform_monitor", color_palette="plasma")
```

Limit the visible traces and adjust display properties:

```python
mwf.set_curve_limit(50, flush_buffer=True)
mwf.highlight_last_curve = True
mwf.opacity = 60
```

Clear the displayed traces:

```python
mwf.clear_curves()
```

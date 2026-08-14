<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/plots/scatter_waveform/scatter_waveform.py
- Public example surface: USER_ACCESS includes plot, update_with_scan_history, clear_all, color_map, and device/signal properties; plot(device_x, device_y, device_z, signal_x=None, signal_y=None, signal_z=None, color_map="plasma", label=None, validate_bec=True).
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.ScatterWaveform).
-->

Create a scatter plot from two motors and one detector signal:

```python
scatter = gui.bec.new(gui.available_widgets.ScatterWaveform)
scatter.plot(
    device_x="samx",
    device_y="samy",
    device_z="bpm4i",
    color_map="plasma",
)
```

Update the color map or clear the plot:

```python
scatter.color_map = "viridis"
scatter.clear_all()
```

Load the latest scan history into the widget:

```python
scatter.update_with_scan_history(-1)
```

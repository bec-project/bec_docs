<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/plots/heatmap/heatmap.py
- Public example surface: USER_ACCESS includes plot, color_map, v_min/v_max, interpolation_method, oversampling_factor, enforce_interpolation, fft, log, device/signal properties; plot(device_x, device_y, device_z, signal_x=None, signal_y=None, signal_z=None, color_map="plasma", validate_bec=True, interpolation=None, enforce_interpolation=None, oversampling_factor=None, lock_aspect_ratio=None, show_config_label=None, reload=False).
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.Heatmap).
-->

Create a Heatmap for `samx`, `samy`, and `bpm4i`:

```python
heatmap = gui.bec.new(gui.available_widgets.Heatmap)
heatmap.plot(
    device_x="samx",
    device_y="samy",
    device_z="bpm4i",
    color_map="plasma",
)
```

Adjust interpolation and display settings:

```python
heatmap.interpolation_method = "nearest"
heatmap.oversampling_factor = 2.0
heatmap.enable_full_colorbar = True
```

Reload with explicit plotting options:

```python
heatmap.plot(
    device_x="samx",
    device_y="samy",
    device_z="bpm4i",
    interpolation="linear",
    oversampling_factor=1.5,
    reload=True,
)
```

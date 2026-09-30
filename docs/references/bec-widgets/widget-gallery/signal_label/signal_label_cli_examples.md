<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/utility/signal_label/signal_label.py
- Public example surface: USER_ACCESS includes custom_label/custom_units setters, decimal_places setter, show_default_units setter, show_select_button setter, signal visibility setters, display_array_data setter, max_list_display_len setter. Constructor accepts device and signal.
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.SignalLabel).
-->

Create a SignalLabel for one signal:

```python
label = gui.bec.new(
    gui.available_widgets.SignalLabel,
    device="bpm4i",
    signal="bpm4i",
)
```

Customize the display:

```python
label.custom_label = "BPM"
label.decimal_places = 4
label.show_default_units = True
```

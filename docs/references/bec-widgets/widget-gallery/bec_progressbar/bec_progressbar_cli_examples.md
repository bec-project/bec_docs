<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/progress/bec_progressbar/bec_progressbar.py
- Public example surface: USER_ACCESS includes set_value, set_maximum, set_minimum, label_template setter, state setter, _get_label. set_value(value), set_maximum(maximum: float), set_minimum(minimum: float).
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.BECProgressBar).
-->

Create and update a progress bar:

```python
progress = gui.bec.new(gui.available_widgets.BECProgressBar)
progress.set_minimum(0)
progress.set_maximum(100)
progress.set_value(25)
```

Customize the displayed label:

```python
progress.label_template = "$value / $maximum ($percentage %)"
```

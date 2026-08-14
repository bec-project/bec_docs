<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/control/device_control/position_indicator/position_indicator.py
- Public example surface: USER_ACCESS includes set_value, set_range, vertical setter, indicator_width setter, rounded_corners setter. set_range(min_value: float, max_value: float); set_value(position: float).
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.PositionIndicator).
-->

Create an indicator and set a range/value:

```python
indicator = gui.bec.new(gui.available_widgets.PositionIndicator)
indicator.set_range(-5, 5)
indicator.set_value(1.2)
```

Change orientation and style:

```python
indicator.vertical = True
indicator.indicator_width = 4
indicator.rounded_corners = 6
```

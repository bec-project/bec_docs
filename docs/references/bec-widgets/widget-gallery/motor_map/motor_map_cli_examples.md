<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/plots/motor_map/motor_map.py
- Public example surface: USER_ACCESS includes map, reset_history, get_data, device_x/device_y setters, color, max_points, precision, num_dim_points, background_value, scatter_size. map(...) is exposed and get_data() returns a dict.
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.MotorMap).
-->

Create a MotorMap for two motors:

```python
mm = gui.bec.new(gui.available_widgets.MotorMap)
mm.map(device_x="samx", device_y="samy")
```

Adjust the displayed history:

```python
mm.max_points = 100
mm.scatter_size = 8
mm.precision = 3
```

Read and reset the map data:

```python
data = mm.get_data()
mm.reset_history()
```

<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/control/device_control/positioner_box/positioner_box_2d/positioner_box_2d.py
- Public example surface: USER_ACCESS includes set_positioner_hor, set_positioner_ver, enable_controls_hor/ver setters, attach, detach, screenshot. Constructor accepts device_hor and device_ver.
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.PositionerBox2D).
-->

Create a PositionerBox2D and assign two motors:

```python
pos2d = gui.bec.new(gui.available_widgets.PositionerBox2D)
pos2d.set_positioner_hor("samx")
pos2d.set_positioner_ver("samy")
```

Disable one axis control temporarily:

```python
pos2d.enable_controls_hor = False
pos2d.enable_controls_hor = True
```

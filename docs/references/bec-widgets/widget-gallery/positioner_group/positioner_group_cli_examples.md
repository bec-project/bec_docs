<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/control/device_control/positioner_group/positioner_group.py
- Public example surface: USER_ACCESS includes set_positioners, attach, detach, screenshot; set_positioners(device_names: str) expects a space-separated string.
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.PositionerGroup).
-->

Create a group and add several motors:

```python
group = gui.bec.new(gui.available_widgets.PositionerGroup)
group.set_positioners("samx samy")
```

Update the group later:

```python
group.set_positioners("samx samy samz")
```

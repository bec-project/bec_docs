<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/control/device_control/positioner_box/positioner_box/positioner_box.py
- Public example surface: USER_ACCESS includes set_positioner, attach, detach, screenshot; set_positioner(positioner: str | Positioner).
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.PositionerBox).
-->

Create a PositionerBox and assign `samx`:

```python
pos = gui.bec.new(gui.available_widgets.PositionerBox)
pos.set_positioner("samx")
```

Place it below a Waveform by dock name:

```python
pos = gui.bec.new(
    gui.available_widgets.PositionerBox,
    where="bottom",
    relative_to="Waveform",
)
pos.set_positioner("samx")
```

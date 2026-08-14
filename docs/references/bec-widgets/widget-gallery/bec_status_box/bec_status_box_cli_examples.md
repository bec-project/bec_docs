<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/services/bec_status_box/bec_status_box.py
- Public example surface: USER_ACCESS includes get_server_state, remove, attach, detach, screenshot. get_server_state(self) -> str.
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.BECStatusBox).
-->

Create a status box:

```python
status = gui.bec.new(gui.available_widgets.BECStatusBox)
```

Read the current top-level server state:

```python
state = status.get_server_state()
```

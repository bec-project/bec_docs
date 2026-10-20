<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/services/bec_queue/bec_queue.py
- Public example surface: BECQueue is PLUGIN=True. It does not define widget-specific USER_ACCESS; examples are limited to creation and base attach/detach behavior.
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.BECQueue).
-->

Create the queue widget:

```python
queue = gui.bec.new(gui.available_widgets.BECQueue)
```

Place it next to a ScanControl widget:

```python
queue = gui.bec.new(
    gui.available_widgets.BECQueue,
    where="right",
    relative_to="ScanControl",
)
```

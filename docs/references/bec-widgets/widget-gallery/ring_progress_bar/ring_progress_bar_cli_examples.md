<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/progress/ring_progress_bar/ring_progress_bar.py and bec_widgets/widgets/progress/ring_progress_bar/ring.py
- Public example surface: RingProgressBar USER_ACCESS includes rings, add_ring, remove_ring, set_gap, set_center_label. add_ring(config: dict | None = None) -> Ring. Ring USER_ACCESS includes set_value.
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.RingProgressBar).
-->

Create a ring progress bar and add rings:

```python
rings = gui.bec.new(gui.available_widgets.RingProgressBar)
ring = rings.add_ring()
ring.set_value(40)

rings.set_center_label("40 %")
rings.set_gap(8)
```

Remove the last ring:

```python
rings.remove_ring()
```

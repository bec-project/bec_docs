<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/editors/text_box/text_box.py
- Public example surface: USER_ACCESS is set_plain_text and set_html_text; both methods take text: str.
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.TextBox).
-->

Create a TextBox and set plain text:

```python
text = gui.bec.new(gui.available_widgets.TextBox)
text.set_plain_text("Ready for alignment.")
```

Display simple HTML:

```python
text.set_html_text("<b>Status:</b> ready")
```

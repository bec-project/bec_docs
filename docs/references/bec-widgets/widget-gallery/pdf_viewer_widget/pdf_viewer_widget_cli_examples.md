<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/utility/pdf_viewer/pdf_viewer.py
- Public example surface: USER_ACCESS includes load_pdf, zoom_in, zoom_out, fit_to_width, fit_to_page, reset_zoom, previous_page, next_page, toggle_continuous_scroll, go_to_first_page, go_to_last_page, jump_to_page, current_page, current_file_path setter. load_pdf(file_path: str); jump_to_page(page_number: int).
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.PdfViewerWidget).
-->

Create a PDF viewer and load a file:

```python
pdf = gui.bec.new(gui.available_widgets.PdfViewerWidget)
pdf.load_pdf("/path/to/document.pdf")
```

Navigate the document:

```python
pdf.fit_to_width()
pdf.next_page()
pdf.jump_to_page(3)
```

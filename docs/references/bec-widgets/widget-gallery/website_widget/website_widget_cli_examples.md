<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/editors/website/website.py
- Public example surface: USER_ACCESS includes set_url, get_url, reload, back, forward, attach, detach, screenshot. set_url(url: str) and url property setter call set_url.
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.WebsiteWidget).
-->

Create a WebsiteWidget and open a URL:

```python
web = gui.bec.new(gui.available_widgets.WebsiteWidget)
web.set_url("https://bec.readthedocs.io/")
```

Use browser-like actions:

```python
web.reload()
current_url = web.get_url()
```

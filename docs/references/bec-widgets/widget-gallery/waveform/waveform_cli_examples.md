<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/plots/waveform/waveform.py
- Public example surface: USER_ACCESS includes plot, add_dap_curve, get_dap_summary, get_dap_params, get_all_data, get_curve, clear_all; plot(...) accepts x/y custom data, device_x/device_y, dap, scan_id, and scan_number.
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.Waveform).
-->

Create a Waveform and plot `bpm4i` against `samx`:

```python
wf = gui.bec.new(gui.available_widgets.Waveform)
wf.plot(device_x="samx", device_y="bpm4i")

wf.title = "bpm4i during samx scan"
wf.x_label = "samx"
wf.y_label = "bpm4i"
```

Attach a DAP model when creating the source curve:

```python
wf.plot(device_x="samx", device_y="bpm4i", dap="GaussianModel")
wf.get_dap_summary()
wf.get_dap_params()
```

Add a DAP model to an existing source curve:

```python
wf.add_dap_curve(device_label="bpm4i-bpm4i", dap_name="GaussianModel")
```

Plot custom arrays and read them back:

```python
import numpy as np

x = np.linspace(-5, 5, 101)
y = np.exp(-(x**2))

wf.plot(x=x, y=y, label="custom gaussian", dap="GaussianModel")
data = wf.get_all_data()
```

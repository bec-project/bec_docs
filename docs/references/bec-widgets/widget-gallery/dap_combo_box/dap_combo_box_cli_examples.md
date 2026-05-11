<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/dap/dap_combo_box/dap_combo_box.py
- Public example surface: USER_ACCESS includes select_y_axis, select_x_axis, select_fit_model. select_fit_model validates against available DAP models and raises ValueError for invalid names.
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.DapComboBox).
-->

Create a DapComboBox and select axes/model:

```python
dap = gui.bec.new(gui.available_widgets.DapComboBox)
dap.select_x_axis("samx")
dap.select_y_axis("bpm4i")
dap.select_fit_model("GaussianModel")
```

The model name must be available in the current DAP service. Invalid model names raise an error.

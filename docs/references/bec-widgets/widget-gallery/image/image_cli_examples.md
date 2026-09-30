<!--
Source verification audit:
- Source checked: /Users/janwyzula/PSI/bec_widgets/bec_widgets/widgets/plots/image/image.py and bec_widgets/widgets/plots/image/image_base.py
- Public example surface: Image USER_ACCESS includes device/device.setter, signal/signal.setter, color_map, v_min/v_max, colorbar flags, fft, log, num_rotation_90, transpose, main_image, add_roi, remove_roi, rois. ImageBase exposes add_roi/remove_roi used by Image.
- Examples use V3 Dock Area creation through gui.bec.new(gui.available_widgets.Image).
-->

Create an Image widget and connect it to a detector signal. Replace `camera` and `image` with the device and signal names used at your beamline:

```python
img = gui.bec.new(gui.available_widgets.Image)
img.device = "camera"
img.signal = "image"
```

Adjust the display:

```python
img.color_map = "viridis"
img.enable_full_colorbar = True
img.log = True
```

Add and remove an ROI:

```python
img.add_roi(name="beam_roi")
img.remove_roi("beam_roi")
```

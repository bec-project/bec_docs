---
related:
  - title: BEC Signals for Custom Devices
    url: learn/devices/bec-signals.md
  - title: Introduction to ophyd
    url: learn/devices/introduction-to-ophyd.md
  - title: ReadoutPriority in BEC
    url: learn/devices/readout-priority.md
---

# Add a Preview Signal to a Custom Device

!!! Info "Overview"
    Add a `PreviewSignal` to a custom ophyd device when you want BEC to forward live 1D or 2D preview data such as images, spectra, or monitor streams.

## Prerequisites

- You already have a custom device class in Python.
- Your device receives preview-like data from a callback, background thread, stream, or external client.
- You know whether the preview data is 1D or 2D.

!!! learn "[Learn about BEC signal classes](../../learn/devices/bec-signals.md){ data-preview }"

## 1. Declare the signal on the device class

Add `PreviewSignal` as a component on your device class.

Use `ndim=2` for images:

```python
from ophyd import Component as Cpt
from ophyd_devices import PreviewSignal
from ophyd_devices.interfaces.base_classes.psi_device_base import PSIDeviceBase


class MyDetector(PSIDeviceBase):
    preview_image = Cpt(PreviewSignal, name="preview_image", ndim=2)
```

Use `ndim=1` instead for line-like previews such as spectra.

## 2. Connect it to your preview callback

When your device receives new preview data, extract the payload first and then publish it with `put(...)`.

`PreviewSignal` accepts preview data in multiple forms:

- a Python `list`
- a NumPy array
- a fully constructed `DevicePreviewMessage`


```python
def _preview_callback(self, message: dict) -> None:
    if message.get("type", "") != "image":
        return

    data = message.get("data", {}).get("default")
    if data is None:
        return

    self.preview_image.put(data)
```

You first receive or assemble the preview payload in your callback or stream handler, and only then set it on the signal with `put(...)`.

If you pass a list or NumPy array, `PreviewSignal` wraps it into the BEC preview message type for you. If you already have a `DevicePreviewMessage`, you can pass that directly.

!!! warning "Stay aware of the data rate"
    When connecting a `PreviewSignal`, make sure that the incoming preview data rate is not too high. The purpose of a preview is to provide a lightweight stream that can be forwarded to GUIs and clients without overwhelming the network or BEC. If your preview data arrives at a very high rate, consider adding throttling or decimation logic in your callback before sending it to the signal.

## 3. Adjust orientation if needed

If your upstream image arrives in a different orientation than you want to show in BEC, configure the signal declaration with `transpose` or `num_rotation_90`.

Example:

```python
preview_image = Cpt(
    PreviewSignal,
    name="preview_image",
    ndim=2,
    transpose=True,
    num_rotation_90=1,
)
```

## 4. Verify the preview in BEC

Start the device, trigger the upstream preview source, and confirm that the preview appears in the relevant BEC client or GUI.

If nothing appears:

- verify that your callback is being called
- verify that `data` is not `None`
- verify that `ndim` matches the actual payload shape
- verify that the device is configured with a suitable `readoutPriority`

!!! success "Congratulations!"
    You have successfully added a `PreviewSignal` to a custom device. BEC can now forward your live preview stream independently of the final stored data.

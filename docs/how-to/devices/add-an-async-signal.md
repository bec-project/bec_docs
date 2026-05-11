---
related:
  - title: BEC Signals for Custom Devices
    url: learn/devices/bec-signals.md
  - title: ReadoutPriority in BEC
    url: learn/devices/readout-priority.md
  - title: Introduction to ophyd
    url: learn/devices/introduction-to-ophyd.md
---

# Add an Async Signal to a Custom Device

!!! Info "Overview"
    Add an `AsyncSignal` to a custom ophyd device when the device produces one asynchronous data stream and you want BEC to forward it during a scan.

## Prerequisites

- You already have a custom device class in Python.
- Your device produces asynchronous data outside the normal `read()` path.
- You know the dimensionality of the async payload.
- You know how new async updates should be written into the dataset.

!!! learn "[Learn about BEC signal classes](../../learn/devices/bec-signals.md){ data-preview }"

## 1. Declare the signal on the device class

Declare one `AsyncSignal` component on the device.

```python
from ophyd import Component as Cpt, Device
from ophyd_devices import AsyncSignal


class MyDetector(Device):
    waveform = Cpt(
        AsyncSignal,
        name="waveform",
        ndim=1,
        async_update={"type": "add", "max_shape": [None, 1024]},
        max_size=1000,
    )
```

This defines one asynchronous signal named `waveform`.

- `ndim` describes the payload dimensionality
- `async_update` tells BEC how incoming updates should be stored
- `max_size` controls how much async data BEC keeps in memory for that signal

## 2. Define `async_update` on the signal

In normal usage, define `async_update` once on the signal declaration.

Example for a stream of fixed-length waveforms:

```python
async_update={"type": "add", "max_shape": [None, 1024]}
```

This means each new update adds one more waveform of length `1024`.

!!! note "When to override it"
    For `add_slice`, the slice `index` may need to change between updates. In that case, pass updated `async_update` metadata with the individual `put(...)` call.

!!! note "Learn about update modes"
    See [BEC Signals for Custom Devices](../../learn/devices/bec-signals.md#async-update-metadata) for details on `add`, `add_slice`, and `replace`.

## 3. Receive the async data first

`AsyncSignal` is meant for data that arrives asynchronously from a callback, subscription, socket, thread, or other background source.

Typical pattern:

```python
def _get_waveform(self):
    return [1.0, 2.0, 3.0, 4.0]


values = self._get_waveform()
self.waveform.put(values)
```

The important sequence is:

1. receive one async sample from the hardware or upstream source
2. convert it into the payload you want to send
3. call `put(...)` on the `AsyncSignal`

## 4. Handle `add_slice` if needed

If the signal uses `add_slice` and the slice `index` changes during runtime, send the updated metadata with the individual update.

Example:

```python
self.waveform.put(
    first_chunk,
    async_update={"type": "add_slice", "index": 0, "max_shape": [None, 1024]},
)

self.waveform.put(
    second_chunk,
    async_update={"type": "add_slice", "index": 1, "max_shape": [None, 1024]},
)
```

If your device naturally emits one complete new waveform, row, or image per update, `add` is usually simpler than `add_slice`.

## 5. Verify the data stream

Run a short acquisition and confirm that:

- your callback or background reader is receiving async data
- the payload shape matches the declared signal
- the signal receives updates with `put(...)`
- the chosen `async_update` mode matches the intended dataset layout

If no async data appears in BEC, first check whether the payload shape and `async_update` configuration match each other.

!!! success "Congratulations!"
    You have successfully added an `AsyncSignal` to a custom device. BEC can now forward one asynchronous data stream from your device during the scan.

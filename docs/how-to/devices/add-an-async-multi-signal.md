---
related:
  - title: BEC Signals for Custom Devices
    url: learn/devices/bec-signals.md
  - title: ReadoutPriority in BEC
    url: learn/devices/readout-priority.md
  - title: Introduction to ophyd
    url: learn/devices/introduction-to-ophyd.md
---

# Add an Async Multi Signal to a Custom Device

!!! Info "Overview"
    Add an `AsyncMultiSignal` to a custom ophyd device when the device produces asynchronous data for multiple named channels or fields and you want BEC to forward that stream as one grouped signal.

## Prerequisites

- You already have a custom device class in Python.
- Your device produces asynchronous data outside the normal `read()` path.
- You know the fixed set of sub-signal names you want to expose in BEC.
- You can transform each incoming sample into a dictionary keyed by those sub-signal names.

!!! learn "[Learn about BEC signal classes](../../learn/devices/bec-signals.md){ data-preview }"

## 1. Declare the signal on the device class

Declare one `AsyncMultiSignal` component and list all sub-signal names explicitly.

```python
from ophyd import Component as Cpt, Device
from ophyd_devices import AsyncMultiSignal


class MyFlyer(Device):
    data = Cpt(
        AsyncMultiSignal,
        name="data",
        signals=["target_x", "target_y"],
        ndim=1,
        async_update={"type": "add", "max_shape": [None]},
        max_size=1000,
    )
```

This defines one grouped async signal with two sub-signals:

- `target_x`
- `target_y`

The `async_update` metadata is part of the signal definition. In this example, each new update is appended to the async stream.

`max_size` controls how much async data BEC keeps in memory for that signal.

The resulting data output for a device named `my_flyer` will look like:

```json
{
    "my_flyer_data_target_x": {"value": ...},
    "my_flyer_data_target_y": {"value": ...}
}
```

## 2. Receive the async data first

`AsyncMultiSignal` is meant for data that arrives asynchronously from a callback, subscription, socket, thread, or other background source.

Typical pattern:

```python
def _get_async_data(self):
    return {
        "target_x": {"value": 10},
        "target_y": {"value": 20},
    }
signals = self._get_async_data()
self.data.put(signals)
```

The important sequence is:

1. receive one async sample from the hardware or upstream source
2. convert it into the required signal dictionary
3. call `put` with that dictionary on the `AsyncMultiSignal`

## 3. Choose the async update mode

`AsyncMultiSignal` requires async update metadata describing how new data should be handled.

Example:

```python
async_update={"type": "add", "max_shape": [None]}
```

Define this once on the signal declaration. After that, the device code should normally call `self.data.put(signals)` without repeating `async_update` on every update.

The main exception is `add_slice`: if the slice `index` changes between updates, pass updated `async_update` metadata with the individual `put(...)` call.

!!! note "Learn about async update modes"
    See [BEC Signals for Custom Devices](../../learn/devices/bec-signals.md#async-update-metadata) for details on available async update types and their behavior.

## 4. Verify the data stream

Run a short acquisition and confirm that:

- your async callback or background reader is receiving samples
- each sample is converted into a dictionary with valid signal names
- all keys match the declared `signals` list
- `self.data.put(signals)` is called after the sample has been assembled

If no async data appears in BEC, first check for signal-name mismatches and incomplete payload dictionaries.

!!! success "Congratulations!"
    You have successfully added an `AsyncMultiSignal` to a custom device. BEC can now forward a structured asynchronous stream with multiple named sub-signals from your device.

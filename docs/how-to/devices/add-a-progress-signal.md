---
related:
  - title: BEC Signals for Custom Devices
    url: learn/devices/bec-signals.md
  - title: ReadoutPriority in BEC
    url: learn/devices/readout-priority.md
  - title: Introduction to ophyd
    url: learn/devices/introduction-to-ophyd.md
---

# Add a Progress Signal to a Custom Device

!!! Info "Overview"
    Add a `ProgressSignal` to a custom ophyd device when you want BEC to track scan progress from that device, for example while data is being acquired or processed asynchronously.

## Prerequisites

- You already have a custom device class in Python.
- Your device has a natural progress measure such as completed triggers, completed frames, or processed points.
- You know the current value and the expected maximum value during the operation.

!!! learn "[Learn about BEC signal classes](../../learn/devices/bec-signals.md){ data-preview }"

## 1. Declare the signal on the device class

Add `ProgressSignal` as a component on your device class:

```python
from ophyd import Component as Cpt, Device
from ophyd_devices import ProgressSignal


class MyDetector(Device):
    progress = Cpt(ProgressSignal, name="progress")
```

This creates one signal that emits BEC progress messages.

## 2. Decide what progress means for the device

Choose one quantity that moves toward completion in a clear way.

Typical examples are:

- completed frames out of total frames
- completed scan points out of total points
- processed events out of total events

The most common pattern is to send:

- the current value
- the maximum value
- whether the operation is done

## 3. Update the signal during runtime

When the device makes progress, send a progress update with `put(...)`.

Example:

```python
self.progress.put(value=25, max_value=100, done=False)
```

When the operation is finished:

```python
self.progress.put(value=100, max_value=100, done=True)
```

## 4. Connect it to your callback or worker loop

`ProgressSignal` is usually updated from a callback, subscription, worker thread, or polling loop.

Typical pattern:

```python
def _update_progress(self, completed, total):
    self.progress.put(
        value=completed,
        max_value=total,
        done=completed >= total,
    )
```

This keeps the progress signal close to the logic that already knows how much work has been completed.

## 5. Verify the progress updates

Run a short acquisition and confirm that:

- the device sends progress updates while work is ongoing
- `value` increases in the expected direction
- `max_value` is stable and meaningful
- `done` becomes `true` when the operation finishes

If progress does not appear in BEC, first check whether the callback or worker loop that computes progress is actually running.

!!! success "Congratulations!"
    You have successfully added a `ProgressSignal` to a custom device. BEC can now track the device's runtime progress during the scan.

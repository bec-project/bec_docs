---
related:
  - title: BEC Signals for Custom Devices
    url: learn/devices/bec-signals.md
  - title: File writing
    url: learn/file-writer/introduction.md
  - title: ReadoutPriority in BEC
    url: learn/devices/readout-priority.md
---

# Add a File Event Signal to a Custom Device

!!! Info "Overview"
    Add a `FileEventSignal` to a custom ophyd device when the real measurement data is written to an external file and BEC must track the output path and completion state.

## Prerequisites

- You already have a custom device class in Python.
- Your device writes scan data to a file such as HDF5.
- Your device knows the final output path before or during acquisition.
- Your acquisition flow exposes a completion state or status callback.

!!! learn "[Learn about BEC signal classes](../../learn/devices/bec-signals.md){ data-preview }"

## 1. Declare the signal on the device class

Add `FileEventSignal` as a component on your device class:

```python
from ophyd import Component as Cpt
from ophyd_devices import FileEventSignal
from ophyd_devices.interfaces.base_classes.psi_device_base import PSIDeviceBase


class MyDetector(PSIDeviceBase):
    file_event = Cpt(FileEventSignal, name="file_event")
```

## 2. Emit the initial file event before acquisition starts

As soon as the final output path is known, publish an initial file event with `done=False`.

This is the same pattern used in `csaxs_bec/devices/jungfraujoch/eiger.py`:

```python
self.file_event.put(
    file_path=self._full_path,
    done=False,
    successful=False,
    hinted_h5_entries={"data": "entry/data/data"},
)
```

In many devices this is a good fit for `on_stage()`.

## 3. Emit the final file event when acquisition completes

When the asynchronous acquisition finishes, publish a second file event with the resolved completion status.

```python
def _file_event_callback(self, status: DeviceStatus) -> None:
    self.file_event.put(
        file_path=self._full_path,
        done=status.done,
        successful=status.success,
        hinted_h5_entries={"data": "entry/data/data"},
    )
```

Attach this callback to the status object returned by your asynchronous acquisition or completion logic.

## 4. Provide HDF5 dataset hints when applicable

For HDF5-based detectors, set `hinted_h5_entries` so downstream BEC components know where the primary data lives inside the file.

Example:

```python
hinted_h5_entries={"data": "entry/data/data"}
```

This is especially important for downstream file linking and data discovery.

## 5. Verify the file event flow

Run a short acquisition and confirm that:

- the initial file event is emitted with the expected `file_path`
- the final file event is emitted after completion
- `successful` reflects the actual acquisition outcome
- the path points to the final file, not a temporary staging location

If your file format or downstream consumer needs extra context, include fields such as `file_type` or `metadata`.

## 6. Use the file event in BEC
With the file event signal in place, BEC can now track the produced file and its completion state alongside the rest of the acquisition. For more information on how to use files in BEC and how to link them, see the [File Writer documentation](../../learn/file-writer/introduction.md).


!!! success "Congratulations!"
    You have successfully added a `FileEventSignal` to a custom device. BEC can now track the produced file and its completion state alongside the rest of the acquisition.

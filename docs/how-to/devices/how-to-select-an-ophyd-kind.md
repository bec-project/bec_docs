---
related:
  - title: Ophyd Kind in BEC
    url: ../../learn/devices/ophyd-kinds.md
  - title: ReadoutPriority in BEC
    url: ../../learn/devices/readout-priority.md
  - title: How to select a readout priority
    url: ../../how-to/devices/how-to-select-readout-priority.md

---
# Select a signal Kind

!!! Info "Overview"
    Choosing `Kind` for a signal in your custom ophyd device determines how BEC will handle the signal and its associated data.

## Prerequisites

- You are writing a custom ophyd device class for BEC.
- For background on how BEC uses `Kind`, see:

    !!! learn "[How BEC uses ophyd Kind](../../learn/devices/ophyd-kinds.md){ data-preview }"

## 1. Choose the signal purpose

For each signal, the `Kind` attribute decides how the signal is treated in runtime. Most of the time we can classify your device signals into three categories:

- Primary monitored readings, use `Kind.hinted` and `Kind.normal`
- Configuration metadata, use `Kind.config`
- Internal controls, use `Kind.omitted`

In the ophyd read interface, this maps to:

- `read()` includes `Kind.hinted` and `Kind.normal`.
- `read_configuration()` includes `Kind.config`.
- `Kind.omitted` is excluded from both.

!!! info "hinted"

    The `Kind.hinted` value is a special flag that indicates the most important `Kind.normal` signal from a device. It highlights that this signal should be the primary signal for plotting and display in GUIs.

## 2. Setup your device class

When defining your custom ophyd device, set the `kind` argument of each signal component to the appropriate `Kind` value based on its purpose. For example:

```python
from ophyd import Component as Cpt, Device, EpicsSignal, EpicsSignalRO, Kind


class MyDetector(Device):
    # Primary scan value
    counts = Cpt(EpicsSignalRO, ":Counts", kind=Kind.hinted)

    # Additional scan value
    elapsed_time = Cpt(EpicsSignalRO, ":ElapsedTime", kind=Kind.normal)

    # Configuration metadata
    acquisition_time = Cpt(EpicsSignal, ":AcqTime", kind=Kind.config)

    # Internal control signal
    acquire = Cpt(EpicsSignal, ":Acquire", kind=Kind.omitted)
```

## 3. Verify the result

After loading your device:

- Check `device.read()` and confirm only scan signals appear.
- Check `device.read_configuration()` and confirm setup signals appear.
- Confirm internal controls are absent from both outputs.

!!! success "Congratulations!"

    You have now learned how to decide about which `Kind` attribute to use for which signal.

!!! important "ReadoutPriority and Kind"

    BEC's readout priorities (e.g. `monitored`, `baseline`, `async`) determine when signals are read during a scan, while `Kind` determines how signals from a device are read. Both attributes work together to define the behavior of signals in BEC.




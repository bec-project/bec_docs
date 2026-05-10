---
related:
  - title: Add an EPICS signal
    url: how-to/devices/add-an-epics-signal.md
---

# EPICS Signal Variants

BEC exposes three common EPICS-backed signal classes through `ophyd_devices`:

- `ophyd_devices.EpicsSignal`
- `ophyd_devices.EpicsSignalRO`
- `ophyd_devices.EpicsSignalWithRBV`

Use these classes when you want to expose a single EPICS process variable in BEC instead of a full motor-style device.

## Which one should I use?

The right choice depends on whether the PV is writable and how EPICS exposes its readback:

- Choose `ophyd_devices.EpicsSignal` for a normal read/write signal.
- Choose `ophyd_devices.EpicsSignalRO` for a read-only signal that BEC should monitor but never write to.
- Choose `ophyd_devices.EpicsSignalWithRBV` when the EPICS record has a setpoint PV and a separate readback PV following the usual `prefix` and `prefix_RBV` pattern.

## What goes into `deviceConfig`?

Each class expects a slightly different `deviceConfig` section in the BEC config:

- `ophyd_devices.EpicsSignal`: `read_pv`, and optionally `write_pv` if the write PV differs from the read PV
- `ophyd_devices.EpicsSignalRO`: `read_pv`
- `ophyd_devices.EpicsSignalWithRBV`: `prefix`

!!! info "What to remember"
    - Use EPICS signal classes when you want to expose a single EPICS PV in BEC rather than a full motor device.
    - Choose `EpicsSignal` for read/write PVs, `EpicsSignalRO` for read-only PVs, and `EpicsSignalWithRBV` when setpoint and readback follow the usual RBV pattern.
    - The correct `deviceConfig` fields depend on the chosen class.
    - Picking the right EPICS signal variant keeps the BEC device model aligned with the underlying EPICS record behavior.

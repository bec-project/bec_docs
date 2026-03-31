---
related:
  - title: Select a signal Kind
    url: ../../how-to/devices/how-to-select-an-ophyd-kind.md
  - title: Relation between Ophyd Kind and data in BEC
    url: ophyd-kinds.md
---

# ReadoutPriority in BEC

`readoutPriority` is a key part of the device configuration that controls when BEC reads a device during a scan. It is independent of the ophyd `Kind` attribute, which controls which signals are included in those `device.read()` or `device.read_configuration()` operations. However, together they determine which data will be included in scan data, configuration metadata or excluded.

- `Kind` controls which signals are included in `read()` and `read_configuration()`.
- `readoutPriority` controls if a device's `read()` is requested during a scan.

## Available priorities

BEC supports a set of five readout priorities that can be assigned to devices in the configuration. The most common ones are `monitored` and `baseline`, which are used for devices that should be read at monitored scan read points and baseline points, respectively. The `async` priority is used for devices that produce asynchronous data streams, while `on_request` is for devices that should only be read when explicitly requested. Finally, `continuous` is for devices that continuously produce data and are handled separately from standard BEC-triggered reads.

## Readout priority modifications during scans

If the user requests to scan a motor that is not configured as `monitored`, BEC automatically promotes it to `monitored` for that scan request. This ensures that scan motors are always included in monitored data, even if their static configuration differs.

## Practical guidance

- Choose `monitored` for devices that should be monitored in scans.
- Choose `baseline` for mostly static setup-state devices and motors.
- Choose `on_request` for devices that should only be read when explicitly requested.
- Choose `async` for devices like large-area detectors that produce asynchronous data streams.
- Choose `continuous` for continuously emitted device data.

!!! information "Keep choices orthogonal to ophyd `Kind`"

    `Kind` controls the inclusion of signals in the `read()` and `read_configuration()` interface of a device, while `readoutPriority` controls when BEC includes that device in it scan readouts. The two attributes work together, but are configured independently. This also allows you to dynamically change the `readoutPriority` of a device to exclude it from scans, e.g. scan motors, while keeping the general device readout interface intact.

---
related:
  - title: Select a Signal Kind
    url: how-to/devices/how-to-select-an-ophyd-kind.md
  - title: ophyd Kind
    url: learn/devices/ophyd-kinds.md
---

# Readout Priority

`readoutPriority` is a key part of the device configuration that controls when BEC reads a device during a scan. It is independent of the ophyd `Kind` attribute, which controls which signals are included in those `device.read()` or `device.read_configuration()` operations. Together they determine which data will be included in scan data, configuration data or excluded.

!!! info "Readout Priority vs. ophyd Kind"
    - `Kind` controls which signals are included in `read()` and `read_configuration()`.
    - `readoutPriority` controls if a device's `read()` is requested during a scan.

## Readout Priority Options

BEC supports four readout priorities that can be assigned to devices in the configuration. The
most common ones are `monitored` and `baseline`, which are used for devices that should be read at
monitored scan read points and baseline points, respectively. The `async` priority is used for
devices that produce asynchronous data streams, while `on_request` is for devices that should only
be read when explicitly requested.

### Modifications during Scans

If the user requests to scan a motor that is not configured as `monitored`, the scan typically promotes it to `monitored` for that scan request. This ensures that scan motors are always included in monitored data, even if their static configuration differs.

### Practical guidance

- Choose `monitored` for devices that should be monitored in scans.
- Choose `baseline` for mostly static setup-state devices and motors.
- Choose `on_request` for devices that should only be read when explicitly requested.
- Choose `async` for devices like large-area detectors that produce asynchronous data streams.

!!! info "Keep `readoutPriority` separate from ophyd `Kind`"

    `Kind` controls which signals a device exposes through `read()` and
    `read_configuration()`. `readoutPriority` controls when BEC asks that device for
    those readings during a scan. In other words, `Kind` defines the contents of a
    device readout, while `readoutPriority` defines when that readout participates in
    acquisition. This separation lets you adjust scan behavior without changing the
    device's underlying read interface.

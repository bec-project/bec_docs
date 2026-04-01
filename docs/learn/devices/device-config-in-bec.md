---
related:
  - title: Add an EPICS motor
    url: ../../how-to/devices/add-an-epics-motor.md
  - title: Write a new ophyd class
    url: ../../how-to/devices/write-a-new-ophyd-class.html
  - title: Add a pseudo motor
    url: ../../how-to/devices/add-a-pseudo-motor.html
  - title: ReadoutPriority in BEC
    url: ../../learn/devices/readout-priority.md
  - title: Select a readout priority
    url: ../../how-to/devices/how-to-select-readout-priority.md
---

# Device Configuration in BEC

BEC creates representative devices and signals dynamically on the device server,
following the specifications given in the device configuration.

The device configuration can be loaded from and stored to YAML files and contains
the information needed to construct devices and manage their behavior in BEC.

## Ophyd device configuration

An example of an EPICS-backed signal device entry:

```yaml
curr:
  readoutPriority: baseline
  description: SLS ring current
  deviceClass: ophyd.EpicsSignalRO
  deviceConfig:
    auto_monitor: true
    read_pv: ARIDI-PCT:CURRENT
  deviceTags:
    - cSAXS
  onFailure: buffer
  enabled: true
  readOnly: true
  softwareTrigger: false
```

The `curr` key is the device name in BEC (for example accessible as `dev.curr`).

## Required fields

According to the current BEC device model, the required fields in each device
entry are:

- `enabled`
- `deviceClass`
- `readoutPriority`

### `deviceClass`

The device class specifies the type of the device. For example, `EpicsSignalRO`
is a read-only EPICS signal class, and `EpicsMotor` is a motor class.

### `readoutPriority`

The readout priority specifies with which priority the device is read out.
Supported values are:

- `on_request`
- `baseline`
- `monitored`
- `async`

For BEC-controlled readouts, `on_request`, `baseline`, and `monitored` are the
most common categories. `async` is used for asynchronous data streams.

!!! learn "[ReadoutPriority in BEC](../../learn/devices/readout-priority.md){ data-preview }"

### `enabled`

The enabled status specifies whether the device is enabled in the current
session.

## Optional fields

The following fields are optional in the device entry model:

- `deviceConfig` (defaults to `{}`)
- `connectionTimeout` (defaults to `5.0`)
- `description` (defaults to `''`)
- `deviceTags` (defaults to `[]`)
- `needs` (defaults to `[]`)
- `onFailure` (defaults to `retry`)
- `readOnly` (defaults to `false`)
- `softwareTrigger` (defaults to `false`)
- `userParameter` (defaults to `{}`)

### `deviceConfig` (dictionary)

The device config contains class-specific configuration parameters. In the
example above, it contains `read_pv` and `auto_monitor`.

Conceptually, BEC constructs the selected class by passing the `deviceConfig`
parameters to the constructor of the device class.

### `readOnly` (boolean)

The read-only field indicates whether writing to the device is disabled. Defaults to `false`.

### `softwareTrigger` (boolean)

The software-trigger field determines whether BEC should explicitly invoke the
device trigger method during scans. Defaults to `false`. Any device which implements a trigger method and should be triggered during scans should have this field set to `true`.

### `deviceTags` (list of strings)

Device tags are used to group and filter devices.

### `onFailure` (string with limited set of values)

`onFailure` specifies failure behavior:

- `buffer`: fallback to the last value in Redis
- `retry`: retry once, then raise if it fails again
- `raise`: raise immediately

### `description` (string)

The description provides additional human-readable information about the
device.

### `needs` (list of device names)

`needs` declares device dependencies.

If a device lists dependencies in `needs`, those referenced devices must be
present in the same effective configuration. BEC will ensure that these devices
are constructed before the device that declares the dependency. Field needed for
pseudo devices that combine multiple underlying devices.

### `connectionTimeout` (float)

`connectionTimeout` controls connection timeout behavior for device
initialization. Defaults to `5.0` seconds.

### `userParameter` (dictionary)

`userParameter` stores user-managed auxiliary metadata for a device.

## Combining config files

Device configurations are often split into multiple files for maintainability
and then combined using YAML include patterns.

Conceptually, this allows teams to keep base, endstation, or subsystem device
groups separate while still loading one effective session configuration.

This page focuses on understanding the model. A dedicated how-to can cover
authoring patterns for combined configuration files.

## Relation to signal-level structure

Device configuration defines device-level construction and BEC-level behavior.
Signal-level behavior is defined in the ophyd class, including `Kind` values on
signals.

!!! learn "[Ophyd Kind and scan data in BEC](../../learn/devices/ophyd-kinds.md){ data-preview }"

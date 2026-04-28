---
related:
  - title: Load and Save a Device Session
    url: how-to/devices/load-and-save-a-device-session-from-the-bec-ipython-client.md
  - title: Validate a Device Configuration
    url: how-to/devices/validate-a-device-configuration.md
  - title: Inspect the Current Device Session
    url: how-to/devices/inspect-the-current-device-session-from-the-bec-ipython-client.md
  - title: Add an EPICS motor
    url: how-to/devices/add-an-epics-motor.md
  - title: Add a pseudo motor
    url: how-to/devices/add-a-pseudo-motor.html
  - title: ReadoutPriority in BEC
    url: learn/devices/readout-priority.md
  - title: Select a readout priority
    url: how-to/devices/how-to-select-readout-priority.md
---

# Device Configuration in BEC

BEC creates representative devices and signals dynamically on the device server,
following the specifications given in the device configuration.

The device configuration can be loaded from and stored to YAML files and contains
the information needed to construct devices and manage their behavior in BEC.

## Device configuration and device session

In BEC, it is useful to separate two closely related ideas:

- The **device configuration** is the YAML description on disk.
- The **device session** is the currently active set of devices loaded into the running BEC system.

The device session usually starts from one or more YAML configuration files, but once loaded it becomes runtime state shared across the BEC services and clients.

This distinction matters because you can inspect and modify the current session from the BEC client, and you can also export that active session back to a YAML file.

!!! learn "[Learn how larger configurations can be composed from multiple files](managing-device-configs.md){ data-preview }"

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

## How BEC loads a device session

When a device session is loaded, the device server reads the effective device configuration and turns each device entry into a live ophyd-backed object. The process is easiest to understand as three main steps.

### 1. Create a valid ophyd object

For each device entry, BEC resolves the configured `deviceClass`, combines it with the corresponding `deviceConfig`, and constructs an ophyd object on the device server.

Dependencies declared through `needs` are resolved first so devices are initialized in an order that satisfies those relationships.

### 2. Try to connect to the device

After creating the object, BEC tries to establish a connection to the underlying device. This is where timeouts, unreachable IOCs, or other connection problems surface.

If the connection fails, BEC still tracks that outcome explicitly so the session state reflects that the device did not initialize successfully.

### 3. Read and publish the device interface

Once the object exists, BEC inspects its signal interface and serializes device information such as signals, methods, and metadata. The device server then publishes this interface and the device data endpoints through Redis.

Other BEC services and clients connect to these published endpoints rather than directly to the ophyd object itself.

## Why clients do not access ophyd objects directly

The live ophyd object exists on the device server. Other services do not hold that object directly. Instead, they consume the published interface from Redis and generate proxy devices from it.

This proxy layer is what lets users interact with devices through BEC's distributed architecture while the real ophyd object stays on the device server.

In practice, this is why commands such as `dev.show_all()`, `dev.samx.read()`, or `dev.samx.read_configuration()` work from the BEC client even though the actual ophyd object was created somewhere else.

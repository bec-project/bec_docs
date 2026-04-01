---
related:
  - title: Select an ophyd Kind for your device signals
    url: ../../how-to/devices/how-to-select-an-ophyd-kind.md
---

# Ophyd Kind and data in BEC

Every signal component in an ophyd device carries a `Kind` attribute that controls how that
signal is treated at runtime. It determines whether a signal is included in `read()`,
`read_configuration()`, or neither of the two methods. 
BEC will read devices during scans using the `read()` method, while it reads device configuration on demand using `read_configuration()`. Therefore, the `Kind` attribute of signals in a device determines whether they contribute to scan data, are stored as configuration data, or are excluded from both.

## The four Kind values

Ophyd defines `Kind` as a flag enumeration in `ophyd.Kind`. The four values used in BEC device
integrations are:

| Kind | Integer | Role in BEC |
|---|---|---|
| `hinted` | 5 | Signal should be monitored and carries a flag for highlighting in plots. It is returned by `read()` on the device. |
| `normal` | 1 | Signal should be monitored. It is returned by `read()` on the device. |
| `config` | 2 | Signal represents configuration data. It is returned by `read_configuration()` on the device. |
| `omitted` | 0 | Signal is excluded from both `read()` and `read_configuration()` on the device. |

??? note "Ophyd sub-device and `Kind` attributes"

    `Kind` is a flag enum, and its values are combined. Ophyd allows sub-devices to be added as components. Each devices may carry its own signals with `Kind` attributes. Now if the sub-device is implemented with `Kind=Kind.config`, the `Kind` of all signals from the sub-device are the combined `Kind` flag enums. 
    
    ``` py 
    from ophyd import Kind, Device, Component as Cpt, Signal

    class SubDevice(Device):
        sub_signal = Cpt(Signal, kind=Kind.normal)
        sub_config_signal = Cpt(Signal, kind=Kind.config)

    class RootDevice(Device):
        signal = Cpt(Signal, kind=Kind.normal)
        signal_config = Cpt(Signal, kind=Kind.config)
        sub_device = Cpt(SubDevice, kind=Kind.config)
    
    device = RootDevice(name="device")

    device.read()
    OrderedDict([('device_signal',
              {'value': 0.0, 'timestamp': 1775022455.4195719})])

    device.read_configuration()
    OrderedDict([('device_signal_config',
              {'value': 0.0, 'timestamp': 1775022455.419599}),
             ('device_sub_device_sub_config_signal',
              {'value': 0.0, 'timestamp': 1775022455.4196732})])
    ```
    In particular, this means `Kind.config & Kind.config = Kind.config` and `Kind.config & Kind.normal = Kind.omitted`. This means that `Kind.normal` signals of a sub-device are excluded from a `device.read()` on the root device if the sub-device is added with `Kind.config`.

## How BEC reads signals

There are two relevant factors to understand how BEC reads signals from devices:

- The device configuration and `readoutPriority` classifies devices into `baseline`, `monitored`, and `async` categories. During scans, this determines which devices are read and when.

    !!! learn "[ReadoutPriority in BEC](../../learn/devices/readout-priority.md){ data-preview }"

- For each device, the `Kind` attribute of its signals determines which signals are included in `read()` and `read_configuration()`. This determines whether a signal contributes to step-wise scan data, is stored as configuration data, or is excluded from both.

### 1. Scan data

During a scan, BEC calls `device.read()` on every device with `readoutPriority = 'monitored'` for every step to collect
measurement values. The `Kind` attribute therefore determines whether a signal contributes to
step-wise scan data.

### 2. Device configuration

The configuration of a device is read on demand via `device.read_configuration()`. Values for signals with `Kind.config` are
collected and stored in BEC as configuration data, which avoids reading them continuously during each scan
step. This is done for all devices with `readoutPriority` of `monitored` or `baseline`.


!!! info "Kind.omitted"
    Signals with `Kind.omitted` are excluded from both `read()` and `read_configuration()`. BEC does not read or publish them during normal operation. This is the right choice for internal control handles (triggers, reset commands) and low-level hardware state that is not needed in the data record.
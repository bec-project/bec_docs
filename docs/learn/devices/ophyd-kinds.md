---
related:
  - title: Select an ophyd Kind for your device signals
    url: ../../how-to/devices/how-to-select-an-ophyd-kind.md
---

# Ophyd Kind

Every signal component in an ophyd device carries a `Kind` attribute that controls how that
signal is treated at runtime. It determines whether a signal is included in `device.read()`,
`device.read_configuration()`.

!!! example "Example Ophyd Device"

    Example device with signals of different `Kind`:
    ```python
    from ophyd import Kind, Device, Component as Cpt, Signal

    class MainDevice(Device):
        signal = Cpt(Signal, kind=Kind.normal)
        signal_config = Cpt(Signal, kind=Kind.config)
        signal_omitted = Cpt(Signal, kind=Kind.omitted)
    
    device = MainDevice(name="device")

    device.read()
    OrderedDict([('device_signal',
              {'value': 0.0, 'timestamp': 1775022455.4195719})])

    device.read_configuration()
    OrderedDict([('device_signal_config',
              {'value': 0.0, 'timestamp': 1775022455.419599})])
    ```

Omitted signals are excluded from both `device.read()` and `device.read_configuration()`. This is the right choice for internal control handles (triggers, reset commands) and low-level hardware state that is not needed in the data record. They can be read directly from the device interface.
!!! example
    ```python
    device.signal_omitted.read()
    {'device_signal_omitted': {'value': 0.0, 'timestamp': 1775022455.4195719}}
    ```

## The four Kind values

Ophyd defines `Kind` as a flag enumeration in `ophyd.Kind`. The four values used in BEC device
integrations are:

| Kind | Integer | Role in BEC |
|---|---|---|
| `hinted` | 5 | Signal should be monitored and carries a flag for highlighting in plots. It is returned by `read()` on the device. |
| `normal` | 1 | Signal should be monitored. It is returned by `read()` on the device. |
| `config` | 2 | Signal represents configuration data. It is returned by `read_configuration()` on the device. |
| `omitted` | 0 | Signal is excluded from both `read()` and `read_configuration()` on the device. |


## Combining Kind values

`Kind` is a flag enum, which means that its values can be combined using bitwise AND (`&`) operations. This is relevant when you have sub-devices in your ophyd device class. If a sub-device is added with `Kind.config`, then all signals from that sub-device will be combined with `Kind.config`. This means that signals with `Kind.normal` in the sub-device will become `Kind.omitted` when accessed through the root device, and signals with `Kind.config` will remain `Kind.config`. 

??? example "Ophyd Device with Sub-device"
    
    ``` py 
    from ophyd import Kind, Device, Component as Cpt, Signal

    class SubDevice(Device):
        sub_signal = Cpt(Signal, kind=Kind.normal)
        sub_config_signal = Cpt(Signal, kind=Kind.config)

    class MainDevice(Device):
        signal = Cpt(Signal, kind=Kind.normal)
        signal_config = Cpt(Signal, kind=Kind.config)
        signal_omitted = Cpt(Signal, kind=Kind.omitted)
        sub_device = Cpt(SubDevice, kind=Kind.config)
    
    device = MainDevice(name="device")

    device.read()
    OrderedDict([('device_signal',
              {'value': 0.0, 'timestamp': 1775022455.4195719})])

    device.read_configuration()
    OrderedDict([('device_signal_config',
              {'value': 0.0, 'timestamp': 1775022455.419599}),
             ('device_sub_device_sub_config_signal',
              {'value': 0.0, 'timestamp': 1775022455.4196732})])
    ```

## Readings in BEC

As explained above, the `Kind` attribute determines which signals are included in `device.read()` and `device.read_configuration()`. If you would like to understand further how BEC uses these methods to acquire data during scans, please check the learning material about [*ReadoutPriority in BEC*](../../learn/devices/readout-priority.md){ data-preview } or consult the how-to guide on [*Select a Readout Priority*](../../how-to/devices/how-to-select-readout-priority.md){ data-preview }.
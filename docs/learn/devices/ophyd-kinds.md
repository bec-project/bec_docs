---
related:
  - title: Introduction to ophyd
    url: ../../learn/devices/introduction-to-ophyd.md
  - title: Select an ophyd Kind for your device signals
    url: ../../how-to/devices/how-to-select-an-ophyd-kind.md
---

# ophyd `Kind`

Every signal component in an ophyd device carries a `Kind` attribute that controls how that
signal is treated at runtime. It determines whether a signal is included in `device.read()`,
`device.read_configuration()`, or excluded from both.

!!! example "Example ophyd device"

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

Signals with `Kind.omitted` are excluded from both `device.read()` and
`device.read_configuration()`. This is the right choice for internal control handles
(triggers, reset commands) and low-level hardware state that is not needed in the data
record. These signals can still be accessed directly from the device interface.
!!! example
    ```python
    device.signal_omitted.read()
    {'device_signal_omitted': {'value': 0.0, 'timestamp': 1775022455.4195719}}
    ```

## The four `Kind` values

ophyd defines `Kind` as a flag enumeration in `ophyd.Kind`. The following values are available:

| Kind | Integer | Meaning |
|---|---|---|
| `hinted` | 5 | The signal is included in `read()` and marked as especially important for plotting or analysis. |
| `normal` | 1 | The signal is included in `read()` and intended for general monitoring. This is the default kind if not specified. |
| `config` | 2 | The signal represents configuration data and is included in `read_configuration()`. |
| `omitted` | 0 | The signal is excluded from both `read()` and `read_configuration()`. |


## Combining `Kind` values

`Kind` is a flag enum. In practice, this becomes relevant when you have sub-devices in an
ophyd device class, because the `Kind` of the parent component is combined with the `Kind`
of the signals inside that sub-device.

For example, if a sub-device is added with `Kind.config`, its signals are filtered through
that parent `Kind`. A signal that is `Kind.normal` inside the sub-device becomes
`Kind.omitted` when viewed from the root device, while a signal that is already
`Kind.config` remains `Kind.config`.

??? example "ophyd device with sub-device"
    
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

## `Kind` in BEC

The `Kind` attribute determines which signals are included in `device.read()` and
`device.read_configuration()`. To understand when BEC calls these methods during data
acquisition, see [*Readout Priority*](../../learn/devices/readout-priority.md){ data-preview }
or the how-to guide on [*Select a readout priority*](../../how-to/devices/how-to-select-readout-priority.md){ data-preview }.

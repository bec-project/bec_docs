---
related:
  - title: ophyd Kind values
    url: learn/devices/ophyd-kinds.md
  - title: Device config in BEC
    url: learn/devices/device-config-in-bec.md
  - title: Select a Signal Kind
    url: how-to/devices/how-to-select-an-ophyd-kind.md
---

# Introduction to `ophyd`

`ophyd` is a Python library for modeling hardware as Python objects. Instead of treating each
control-system value as a separate special case, ophyd gives you a shared vocabulary for building
hardware interfaces from signals and devices.

This works for both EPICS-backed and non-EPICS devices, which makes ophyd useful as a common
hardware abstraction independent of the underlying control layer.

In BEC, ophyd is the device abstraction layer used by the device server to construct and represent
hardware in a consistent way.

If you are new to ophyd, the most important idea is simple: represent one hardware value as a
signal, and represent one logical piece of hardware as a device.

## Signals and devices

- `Signal`, which represents one readable or writable quantity
- `Device`, which groups one or more signals into a logical hardware object

A single hardware value can often be represented as a signal. A motor, detector, shutter, or other
instrument is usually represented as a device composed of several signals.

Typical examples are:

- a readback value represented as one signal
- a motor represented as a device with setpoint, readback, limits, and status signals
- a detector represented as a device with acquisition, timing, and file-related signals

This device-and-signal model is what gives ophyd its structure. Signals hold the individual values,
and devices provide the hierarchy around them.

## Components

ophyd devices are usually defined as Python classes. The signals and sub-devices that belong to a
device are declared as `Component`s on that class.

That lets you describe the shape of a device once and then instantiate it for different hardware
instances later.

For example, a small motor-like device class might look like this:

```python
from ophyd import Component as Cpt, Device, EpicsSignal, EpicsSignalRO


class SimpleMotor(Device):
    setpoint = Cpt(EpicsSignal, "VAL")
    readback = Cpt(EpicsSignalRO, "RBV")
    motor_is_moving = Cpt(EpicsSignalRO, "MOVN")
```

This class defines the structure of the device, but not one specific instance of it.

## Prefixes and instances

Once the class exists, you can create concrete device instances by supplying a prefix and a name.
This is one of the main advantages of defining reusable ophyd device classes.

For example:

```python
samx = SimpleMotor("X01DA-ES1-MOT:", name="samx")
samy = SimpleMotor("X01DA-ES2-MOT:", name="samy")
```

These two Python objects share the same internal structure, but they refer to different hardware.

With the `SimpleMotor` definition above, these prefixes would map to PVs such as:

- `samx.setpoint` -> `X01DA-ES1-MOT:VAL`
- `samx.readback` -> `X01DA-ES1-MOT:RBV`
- `samx.motor_is_moving` -> `X01DA-ES1-MOT:MOVN`
- `samy.setpoint` -> `X01DA-ES2-MOT:VAL`
- `samy.readback` -> `X01DA-ES2-MOT:RBV`
- `samy.motor_is_moving` -> `X01DA-ES2-MOT:MOVN`

## Reading and configuration

Two ophyd methods are especially important:

- `read()`, which returns the main runtime data of a device
- `read_configuration()`, which returns configuration-style data

This distinction is useful because not every signal should be treated as live measured data. Some
values belong to the current measurement stream, while others are better treated as setup or
configuration metadata.

## `Kind` and what gets read

ophyd uses the `Kind` attribute on signals to control whether they appear in `read()`,
`read_configuration()`, or neither.

Common `Kind` values are:

- `normal`
- `hinted`
- `config`
- `omitted`

This is the main mechanism for telling ophyd whether a signal should behave like measured data,
configuration data, or an internal implementation detail.

!!! learn "[Learn more about ophyd Kind values](../../learn/devices/ophyd-kinds.md){ data-preview }"

## Why ophyd is useful

The device-and-signal model makes it possible to:

- build reusable device classes
- represent complex hardware hierarchically
- read groups of related values together
- expose a consistent interface to higher-level software layers

That makes ophyd a practical abstraction layer for scientific instrumentation software.

## What to read next

If you are learning ophyd specifically for BEC, the next useful pages are:

- [ophyd Kind values](../../learn/devices/ophyd-kinds.md)
- [Readout Priority](../../learn/devices/readout-priority.md)
- [Device config in BEC](../../learn/devices/device-config-in-bec.md)

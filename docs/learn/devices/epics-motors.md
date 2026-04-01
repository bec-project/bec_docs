---
related:
  - title: Add an EPICS motor
    url: how-to/devices/add-an-epics-motor.md
  - title: Write a new ophyd class
    url: how-to/devices/write-a-new-ophyd-class.html
  - title: Add a pseudo motor
    url: how-to/devices/add-a-pseudo-motor.html
---

# EPICS Motor Variants

BEC exposes three closely related EPICS motor classes through `ophyd_devices`:

- `ophyd_devices.EpicsMotor`
- `ophyd_devices.EpicsMotorEC`
- `ophyd_devices.EpicsUserMotorVME`

## Which one should I use?

The right choice depends on your EPICS motor implementation. 

- If you have an ECMC-based motor, choose `ophyd_devices.EpicsMotorEC` to get ECMC-specific signals and checks.
- If you have a VME user motor, choose `ophyd_devices.EpicsUserMotorVME` to get VME-specific signals and behavior.
- For everything else, start with `ophyd_devices.EpicsMotor` as the normal default.


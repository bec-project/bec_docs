---
related:
  - title: Add an EPICS motor
    url: how-to/devices/add-an-epics-motor.md
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

!!! info "What to remember"
    - BEC provides several EPICS motor classes because different motor backends expose different behavior and signals.
    - `ophyd_devices.EpicsMotor` is the normal default choice.
    - Use `ophyd_devices.EpicsMotorEC` for ECMC-based motors and `ophyd_devices.EpicsUserMotorVME` for VME user motors.
    - Choosing the closest matching motor class gives you the right backend-specific interface in BEC.

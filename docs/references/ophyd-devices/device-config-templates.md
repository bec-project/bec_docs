---
related:
  - title: EpicsMotor, EpicsMotorEC, EpicsUserMotorVME
    url: ../../learn/devices/epics-motors.html
  - title: EpicsSignal, EpicsSignalRO, EpicsSignalWithRBV
    url: ../../learn/devices/epics-signals.html
  - title: Add an EPICS motor
    url: ../../how-to/devices/add-an-epics-motor.html
  - title: Add an EPICS signal
    url: ../../how-to/devices/add-an-epics-signal.html
---

# Device config templates

This page lists the currently supported `deviceConfig` templates for common EPICS-backed device classes exposed through `ophyd_devices`.

## EPICS motor classes

### `ophyd_devices.EpicsMotor`

`deviceConfig` fields:

- `prefix`: `str`, required. EPICS IOC prefix, for example `X25DA-ES1-MOT:`
- `limits`: `tuple[float, float] | None`, optional. Soft limits of the motor

Full example:

```yaml
samx:
  readoutPriority: baseline
  description: Beamline sample stage X motor
  deviceClass: ophyd_devices.EpicsMotor
  deviceConfig:
    prefix: 'X25DA-ES1-MOT:'
  deviceTags:
    - motor
  onFailure: retry
  enabled: true
  readOnly: false
  softwareTrigger: false
```

### `ophyd_devices.EpicsMotorEC`

`deviceConfig` fields:

- `prefix`: `str`, required. EPICS IOC prefix, for example `X25DA-ES1-MOT:`
- `limits`: `tuple[float, float] | None`, optional. Soft limits of the motor

Full example:

```yaml
samx_ec:
  readoutPriority: baseline
  description: ECMC-based sample stage X motor
  deviceClass: ophyd_devices.EpicsMotorEC
  deviceConfig:
    prefix: 'X25DA-ES1-MOT:'
  deviceTags:
    - motor
  onFailure: retry
  enabled: true
  readOnly: false
  softwareTrigger: false
```

### `ophyd_devices.EpicsUserMotorVME`

`deviceConfig` fields:

- `prefix`: `str`, required. EPICS IOC prefix, for example `X25DA-ES1-MOT:`
- `limits`: `tuple[float, float] | None`, optional. Soft limits of the motor

Full example:

```yaml
samx_vme:
  readoutPriority: baseline
  description: VME user motor for sample stage X
  deviceClass: ophyd_devices.EpicsUserMotorVME
  deviceConfig:
    prefix: 'X25DA-ES1-MOT:'
  deviceTags:
    - motor
  onFailure: retry
  enabled: true
  readOnly: false
  softwareTrigger: false
```

## EPICS signal classes

### `ophyd_devices.EpicsSignal`

`deviceConfig` fields:

- `read_pv`: `str`, required. EPICS read PV, for example `X25DA-ES1-MOT:GET`
- `write_pv`: `str | None`, optional. EPICS write PV if it differs from `read_pv`

Full example:

```yaml
beamstop_open:
  readoutPriority: monitored
  description: Beamstop open state
  deviceClass: ophyd_devices.EpicsSignal
  deviceConfig:
    read_pv: 'X25DA-ES1-OP:OPEN'
    write_pv: 'X25DA-ES1-OP:OPEN'
  deviceTags:
    - signal
  onFailure: retry
  enabled: true
  readOnly: false
  softwareTrigger: false
```

### `ophyd_devices.EpicsSignalRO`

`deviceConfig` fields:

- `read_pv`: `str`, required. EPICS read PV, for example `X25DA-ES1-MOT:GET`

Full example:

```yaml
ring_current:
  readoutPriority: monitored
  description: Storage ring current
  deviceClass: ophyd_devices.EpicsSignalRO
  deviceConfig:
    read_pv: 'ARIDI-PCT:CURRENT'
  deviceTags:
    - signal
  onFailure: retry
  enabled: true
  readOnly: true
  softwareTrigger: false
```

### `ophyd_devices.EpicsSignalWithRBV`

`deviceConfig` fields:

- `prefix`: `str`, required. EPICS IOC prefix, for example `X25DA-ES1-DET:ACQUIRE`

Full example:

```yaml
detector_acquire:
  readoutPriority: monitored
  description: Detector acquire state
  deviceClass: ophyd_devices.EpicsSignalWithRBV
  deviceConfig:
    prefix: 'X25DA-ES1-DET:ACQUIRE'
  deviceTags:
    - signal
  onFailure: retry
  enabled: true
  readOnly: false
  softwareTrigger: false
```

## Notes

- The examples show complete device entries so you can see how `deviceConfig` fits into the wider BEC config structure.
- The only class-specific part documented here is `deviceConfig`. Top-level fields such as `readoutPriority`, `deviceTags`, `enabled`, and `readOnly` are shared BEC config fields.
- The field names and types here are based on the current local `ophyd_devices` config templates.

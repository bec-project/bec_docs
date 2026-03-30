---
related:
  - title: Config file
    url: how-to/devices/config-file.html
  - title: Write a new ophyd class
    url: how-to/devices/write-a-new-ophyd-class.html
  - title: EPICS signal classes
    url: learn/devices/epics-signals.html
---

# Add an EPICS signal to the device config

!!! Info "Overview"
    Add a simple EPICS-backed signal to your BEC device configuration using the YAML config file or the GUI.

## Pre-requisites

- You decided on a name for the signal in BEC, for example `beamstop_open`
- You already know the EPICS PV or prefix you want to connect
- You are working at the beamline and the IOC is accessible in the beamline network
- You already know which signal class you want to use. If you are not sure, see

    !!! learn "[Learn about EPICS signal classes](../../learn/devices/epics-signals.md){ data-preview }"

## Using the YAML config

Choose the example that matches the signal class you already selected, and add it to the YAML config file relevant to your experiment.

### Read/write signal with `EpicsSignal`

Use this for a writable PV. If the same PV is used for both reading and writing, you can omit `write_pv`.

```yaml
beamstop_open:
  readoutPriority: monitored
  description: Beamstop open state
  deviceClass: ophyd_devices.EpicsSignal
  deviceConfig:
    read_pv: 'X01DA-OP-STATE-01:OPEN'
    write_pv: 'X01DA-OP-STATE-01:OPEN'
  deviceTags:
    - signal
  onFailure: retry
  enabled: true
  readOnly: false
  softwareTrigger: false
```

### Read-only signal with `EpicsSignalRO`

Use this when BEC should only observe the PV and never write to it.

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

### Signal with separate readback using `EpicsSignalWithRBV`

Use this for a signal class that expects a `prefix`.

```yaml
detector_acquire:
  readoutPriority: monitored
  description: Detector acquire state
  deviceClass: ophyd_devices.EpicsSignalWithRBV
  deviceConfig:
    prefix: 'X01DA-DET-01:Acquire'
  deviceTags:
    - signal
  onFailure: retry
  enabled: true
  readOnly: false
  softwareTrigger: false
```

Save the file and reload the config in BEC. For example through the BEC command line interface:

```py
bec.config.update_session_with_file("<my-config.yaml>")
```

## Using the GUI

1. Open the Device Manager (DM) view in the BEC main application.
2. Load the config file you want to edit.
3. Click the "Add Device" button.
4. Select the EPICS signal class you want to add.
5. Fill in the device name, description, and the required PV field values.
6. Click "Add Device".
7. Save the updated config file or load it directly into BEC with "Update Config".

If the GUI version you are using does not offer the class you need, add the device through the YAML config instead.

!!! success "Congratulations!"
    You have successfully added an EPICS signal to your BEC config. The device should now be available in the GUIs and in the device container of the command line interface, for example as `dev.beamstop_open`.

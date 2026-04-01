---
related:
  - title: Ophyd Kind in BEC
    url: ../../learn/devices/ophyd-kinds.md
  - title: ReadoutPriority in BEC
    url: ../../learn/devices/readout-priority.md
  - title: Device Configuration in BEC
    url: ../../learn/devices/device-config-in-bec.md
  - title: How to select an Ophyd Kind
    url: ../../how-to/devices/how-to-select-an-ophyd-kind.md
---
# Select a readout priority

!!! Info "Overview"
    Selecting a `readoutPriority` for your device in the device config file determines when signals from that device are read during a scan. This is an important choice that affects readings from your device during scans.

## Prerequisites

- You have defined a device in your BEC device config file, either through the YAML config or through the GUI.
- The `read()` and `read_configuration()` methods of your device return the expected signals and values.

    !!! learn "[Consult the ophyd kinds documentation](../../learn/devices/ophyd-kinds.md){ data-preview }"

## 1. Pick a `readoutPriority`

Choose the priority based on when BEC should read this device:

- Use `monitored` for values that must be read at scan read points.
- Use `baseline` for setup-state values that are mostly static during a scan.
- Use `on_request` for devices you only want to read explicitly.
- Use `async` for devices producing asynchronous data streams.
- Use `continuous` for continuously emitted data handled outside normal monitored/baseline reads.

## 2. Set it in the device config

Set `readoutPriority` on the device definition in your BEC device configuration.

!!! learn "[Device Configuration in BEC](../../learn/devices/device-config-in-bec.md){ data-preview }"

Example:

```yaml
ring_current:
  readoutPriority: monitored
  description: Storage ring current
  deviceClass: ophyd_devices.EpicsSignalRO
  deviceConfig:
    read_pv: 'ARIDI-PCT:CURRENT'
  enabled: true
```

!!! tip "DeviceManager View in the BEC App"

    If you are configuring devices from the GUI, select the desired `readoutPriority` value in the device's configuration form.

## 3. Verify during a scan

Run a short scan 'line_scan' and confirm the device is read at the expected points:

- `monitored`: Reading is included at every step of the scan.
- `baseline`: A single reading is included.
- `on_request`: No readings are included.

!!! success "Congratulations!"
    
    You have successfully selected a `readoutPriority` for your device. This will control when BEC reads signals from this device during scans, which is crucial for ensuring the right data is collected at the right time.

If you are interested in more details on how `readoutPriority` works in BEC, please check the learning material on the topic:
    
!!! learn "[ReadoutPriority in BEC](../../learn/devices/readout-priority.md){ data-preview }"







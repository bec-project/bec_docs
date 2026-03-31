---
related:
  - title: Ophyd Kind in BEC
    url: ../../learn/devices/ophyd-kinds.md
  - title: ReadoutPriority in BEC
    url: ../../learn/devices/readout-priority.md
  - title: Device definition
    url: ../../learn/devices/device-definition.md
---
# Select a readout priority

!!! Info "Overview"
    Selecting a `readoutPriority` for your device in the device config file determines when signals from that device are read during a scan. This is an important choice that affects readings from your device during scans.

## Prerequisites

- You have defined a device in your BEC device config file, either through the YAML config or through the GUI.
- The `read()` and `read_configuration()` methods of your device return the expected signals and values.

    !!! learn "[Consult the ophyd kinds documentation](../../learn/devices/ophyd-kinds.md){ data-preview }"





---
related:
  - title: Device Configuration in BEC
    url: learn/devices/device-config-in-bec.md
  - title: Device Sessions in BEC
    url: learn/devices/device-sessions-in-bec.md
  - title: Load and Save a Device Session
    url: how-to/devices/load-and-save-a-device-session-from-the-bec-ipython-client.md
  - title: Validate a Device Configuration
    url: how-to/devices/validate-a-device-configuration.md
---

# Managing Device Configurations

A beamline can easily have hundreds of devices. Managing this in a single file is often not practical. BEC supports splitting the device configuration into multiple files and loading them together. 

Conceptually, this allows teams to keep base, endstation, or subsystem device groups separate while still loading one effective session configuration.

!!! Example "Compose a device configuration"

    ```yaml
    base_config:
      - !include ./path/to/base_config.yaml

    endstation:
      - !include ./path/to/endstation_config.yaml

    curr:
      readoutPriority: baseline
      description: SLS ring current
      deviceClass: ophyd.EpicsSignalRO
      deviceConfig:
        auto_monitor: true
        read_pv: ARIDI-PCT:CURRENT
      deviceTags:
        - cSAXS
      onFailure: buffer
      enabled: true
      readOnly: true
      softwareTrigger: false
    ```


In the example config above, we combine two separate device configuration files into one effective configuration. The `!include` syntax is a feature supported by BEC's YAML parser and allows including the contents of another YAML file at that location. The resulting device configuration is a combination of all included files and any additional entries defined directly in the main config. 

This effective configuration becomes the basis for the current device session in BEC once it is loaded.

!!! learn "[Learn more about device sessions and how BEC turns config entries into live devices](device-sessions-in-bec.md){ data-preview }"

If you need to work with this configuration in practice, use the task-focused guides:

- [Load and save a device session from the BEC IPython client](../../how-to/devices/load-and-save-a-device-session-from-the-bec-ipython-client.md)
- [Validate a device configuration](../../how-to/devices/validate-a-device-configuration.md)

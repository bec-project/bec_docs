---
related:
  - title: Device Configuration in BEC
    url: learn/devices/device-config-in-bec.md
---

# Managing Device Configurations

All devices from a beamline easily amounts to hundreds of devices. Managing this in a single file is often not practical. BEC supports splitting the device configuration into multiple files and loading them together. 

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


## How to validate a device configuration

To avoid errors during loading of the device config, the device config can be validated before loading it. We provided a command line tool for this called `ophyd_test` which is installed through `ophyd_devices` and available in the BEC Python environment. 

Once you activate the BEC Python environment, you can run the following command to validate a device config file:

```bash
ophyd_test --config ./path/to/my/config/file.yaml
```

This will perform a static validation of the device config and will print any errors that are found. For checking if the devices can be created and connect successfully, an additional flag can be passed:

```bash
ophyd_test --config ./path/to/my/config/file.yaml --connect
```

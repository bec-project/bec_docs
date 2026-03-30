---
related:
  - title: Add changes to your plugin repository
    url: how-to/git/add-changes-to-plugin-repository.html
  - title: Add an EPICS signal
    url: how-to/devices/add-an-epics-signal.html
  - title: Device config templates
    url: references/ophyd-devices/device-config-templates.html
---

# Add a custom EPICS device

!!! Info "Overview"
    Build a small custom ophyd device around several EPICS signals, add it to your beamline plugin repository, and load it through a demo config in BEC.

## Pre-requisites

- You have a beamline plugin repository, for example `/sls/<beamline>/config/bec/<beamline-name>_bec`
- You can edit the Python package that contains your custom devices
- You know the EPICS prefix or PV names you want to expose
- You want one logical device in BEC rather than several separate standalone signals

## 1. Decide what belongs into the custom device

Use a custom EPICS device when several signals belong together conceptually and should appear as one device in BEC.

Typical examples:

- a detector with `acquire`, `exposure`, and `state`
- a shutter with `open`, `close`, and `status`
- a temperature controller with `setpoint`, `readback`, and `enabled`

Before writing code, decide which signals are:

- primary readback values that users should normally see
- configuration values that are useful but not shown all the time
- internal or low-level fields that should usually stay out of the default readout

## 2. Create the device class

In your plugin repository, add a device module to the `devices` directory if you do not already have one. Something like:

```text
<plugin-repo>/devices/demo_temperature_controller.py
```

Then define your custom device with EPICS-backed components:

```python
from ophyd import Component as Cpt
from ophyd import EpicsSignal, EpicsSignalRO, Kind

from ophyd_devices import PSIDeviceBase


class DemoTemperatureController(PSIDeviceBase):
    temperature = Cpt(
        EpicsSignalRO, 
        ":TEMP", 
        kind=Kind.hinted, 
        auto_monitor=True, 
        doc="Current temperature"
    )
    setpoint = Cpt(
        EpicsSignal, 
        ":SET", 
        kind=Kind.normal, 
        auto_monitor=True, 
        doc="Temperature setpoint"
    )
    enabled = Cpt(
        EpicsSignal, 
        ":ENABLE", 
        kind=Kind.config, 
        auto_monitor=True, 
        doc="Temperature enable status"
    )
    status = Cpt(
        EpicsSignalRO, 
        ":STATE", 
        kind=Kind.normal, 
        auto_monitor=True, 
        doc="Temperature status"
    )
```

!!! info "[Learn about ophyd.kind](../../learn/devices/ophyd-kind.md)"

This assumes the configured `prefix` is the common base PV, for example `X01DA-TCTRL-01`.

With that setup, the full PVs would resolve to:

- `X01DA-TCTRL-01:TEMP`
- `X01DA-TCTRL-01:SET`
- `X01DA-TCTRL-01:ENABLE`
- `X01DA-TCTRL-01:STATE`

## 3. Add the device class to the `__init__.py` of your devices package

To simplify imports, add your new device class to the `__init__.py` of your devices package, i.e. in `<plugin-repo>/devices/__init__.py`:

```python
from .demo_temperature_controller import DemoTemperatureController
```

## 4. Add the Python changes to the plugin repository

Commit the new device class in your plugin repository using the same workflow you use for other beamline-specific code changes.

If you want a step-by-step Git walkthrough, see:

- [`Add changes to your plugin repository`](../git/add-changes-to-plugin-repository.md)


## 5. Prepare a device config entry

Add the device to a config file that you can safely load for testing.

Example:

```yaml
demo_temp_ctrl:
  readoutPriority: monitored
  description: Demo temperature controller
  deviceClass: my_beamline.devices.DemoTemperatureController
  deviceConfig:
    prefix: "X01DA-TCTRL-01"
  deviceTags:
    - detector
    - demo
  onFailure: retry
  enabled: true
  readOnly: false
  softwareTrigger: false
```

!!! info "[Learn about device config fields](../../learn/devices/device-config-fields.md)"


We recommend putting an example config like this next to the device code, for example in `<plugin-repo>/devices/demo_temperature_controller.yaml`, and then copying it into the main config file when you want to test it.

## 6. Load the demo config in BEC

For example:

```py
bec.config.update_session_with_file("<demo-config.yaml>")
```

Then verify that:

- the device appears in the device container
- the main signals can be read
- writes go to the intended EPICS PVs

!!! success "Congratulations!"
    You have added a custom EPICS device to your plugin repository and prepared a demo config to load it in BEC.

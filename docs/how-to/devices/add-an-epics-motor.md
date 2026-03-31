---
related:
  - title: Config file
    url: how-to/devices/config-file.html
  - title: Write a new ophyd class
    url: how-to/devices/write-a-new-ophyd-class.html
  - title: Add a pseudo motor
    url: how-to/devices/add-a-pseudo-motor.html
  - title: EPICS motor classes
    url: learn/devices/epics-motors.html
---

# Add an EPICS motor to the device config


!!! Info "Overview"
    Add an EPICS motor to your BEC device configuration using either the YAML config file or the GUI.



## Pre-requisites
- You decided for a name for the motor in BEC, for example `samx`
- You already know the IOC prefix for the motor you want to add, for example `X01DA-MO-USER-01:`
- You are working at the beamline and the IOC is accessible in the beamline network
- You already know which device class variant you want to use for the motor (e.g. `ophyd_devices.EpicsMotor`). If you are not sure, see 

    !!! learn "[Learn about EPICS motor classes](../../learn/devices/epics-motors.md){ data-preview }" 
  

## Using the YAML config
The most direct way to add the EPICS motor is to add it to the YAML config file relevant to your experiment. Simply add the following configuration to the file:

``` yaml
samx:
  readoutPriority: baseline
  description: Beamline sample stage X motor
  deviceClass: ophyd_devices.EpicsMotor
  deviceConfig:
    prefix: 'X01DA-MO-USER-01:'
  deviceTags:
    - motor
  onFailure: retry
  enabled: true
  readOnly: false
  softwareTrigger: false
```

!!! learn "[Learn about device definition](../../learn/devices/device-definition.md){ data-preview }" 

If you want to use a different EPICS motor class variant, simply change the `deviceClass` field to the relevant class.

Save the file and reload the config in BEC. For example through the BEC command line interface:

``` py
bec.config.update_session_with_file("<my-config.yaml>")
```

## Using the GUI
You can also add the EPICS motor through the BEC main application. Open the Device Manager (DM) view, load your config file, and click on the "Add Device" button. Fill in the form with the relevant information for your motor, and click "Add Device".
The device will be added to your config, and you can either first save the new config to a file before loading it into BEC, or directly load the updated config into BEC using the "Update Config" button. 

In the video below, we show you the full process of adding an EPICS motor to the config through the GUI, and then loading the updated config into BEC. 

<!-- Add video here -->

!!! success "Congratulations!"
    You have successfully added an EPICS motor to your BEC config. You can now use this motor in your scans and other operations in BEC. The device should now be available in the GUIs and in the device container of the command line interface `dev.samx`.

---
related:
  - title: Config file
    url: how-to/devices/config-file.html
  - title: Write a new ophyd class
    url: how-to/devices/write-a-new-ophyd-class.html
  - title: Add a pseudo motor
    url: how-to/devices/add-a-pseudo-motor.html
---

# Add an EpicsMotor
This is a how-to guide on adding an *EpicsMotor* to the device config in BEC. We will show you how to add the motor through both the YAML config file and the GUI.

!!! Info "Goal"
    You have an *EpicsMotor* at your beamline that you want to add to the device config in BEC. How would you do that?

## Steps

Placeholder.

## Related pages

Placeholder.



## Pre-requisites
- You decided for a name for the motor in BEC, for example `samx`
- You already know the IOC prefix for the motor you want to add, for example `X01DA-MO-USER-01:`
- You are working at the beamline and the IOC is accessible in the beamline network

## Using the YAML config
The most direct way to add the *EpicsMotor*  is to add it to the YAML config file relevant to your experiment. Simply add the following configuration to the file:

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

Save the file and reload the config in BEC. For example through the BEC command line interface:

``` py
bec.config.update_session_with_file("<my-config.yaml>")
```

## Using the GUI
You can also add the *EpicsMotor* through the BEC main application. Open the Device Manager (DM) view, load your config file, and click on the "Add Device" button. Fill in the form with the relevant information for your motor, and click "Add Device".
The device will be added to your config, and you can either first save the new config to a file before loading it into BEC, or directly load the updated config into BEC using the "Update Config" button. 

In the video below, we show you the full process of adding an *EpicsMotor* to the config through the GUI, and then loading the updated config into BEC. 

<!-- Add video here -->

??? success "Congratulations!"
    You have successfully added an *EpicsMotor* to your BEC config. You can now use this motor in your scans and other operations in BEC. The device should now be available in the GUIs and in the device container of the command line interface `dev.samx`.


---
related:
  - title: Config file
    url: how-to/devices/config-file.html
  - title: Write a new ophyd class
    url: how-to/devices/write-a-new-ophyd-class.html
  - title: Add a pseudo motor
    url: how-to/devices/add-a-pseudo-motor.html
---
# Add an EpicsMotor to the config
!!! Info "Goal"

    This How-to guide will show you how to add an *EpicsMotor* to your BEC config.

Below, we show two alternative ways to add an *EpicsMotor* to your BEC config: either by editing the YAML config file directly, or through the Device Manager view in the BEC main application.
To do this, you need to provide enough information for the *EpicsMotor* configuration.

At minimum, we will need to provide:
* deviceClass: The ophyd class for the device, in this case *ophyd_devices.EpicsMotor*.
* deviceConfig: The device configuration, which includes the motor prefix.
* description: A brief description of the motor.
* enabled: Whether the motor is enabled or not. Default is true.
* readoutPriority: The readout priority for the motor. For a motor, we typically recommend 'baseline'.

If you would like to read more about the configuration options in detail, please check out the [...missing link...].

## Steps

1. Choose a name for your motor, for example *samx*.

2. Determine the prefix for your motor, for example *X01DA-MO-USER:*.

3. Prepare the device definition and add it to your config, either through the YAML file or through the GUI.

=== "YAML config"

    You can add the *EpicsMotor* to your YAML config file by adding a new entry for the motor with the relevant information. 
    For example, you can add the following configuration to your YAML file:

    ``` yaml
    samx:
      deviceClass: ophyd_devices.EpicsMotor
      deviceConfig:
        prefix: 'X01DA-MO-USER-01:'
      description: Beamline sample stage X motor
      enabled: true
      readoutPriority: baseline
    ```

=== "Device Manager GUI"

    You can also add the *EpicsMotor* through the Device Manager view in the BEC main application.
    The video below shows you how to do that.

    <figure>
      <video autoplay muted loop playsinline controls width="100%" preload="metadata">
        <source src="add_an_epics_motor_assets/add_epics_motor_dmview_docs.mp4" type="video/mp4">
        Your browser does not support the video tag.
      </video>
      <figcaption>Device Manager workflow for adding an EpicsMotor.</figcaption>
    </figure>

!!! success "Congratulations!"
    You have successfully added an *EpicsMotor* to your BEC config. You can now use this motor in your scans and other operations in BEC. The device should now be available in the GUIs and in the device container of the command line interface `dev.samx`.

## Common Pitfalls

* You added the device to the config, but you forgot to save the YAML file.
* Incorrect indentation or formatting in the YAML file can prevent the device from loading in BEC.
* If the device is not connected, BEC will disable it (`enabled=false`) and raise a warning.

## Next Steps

You can now load the updated config into BEC, either through the command line or through the Device Manager view in the main application.

=== "Command line interface"

    1. Make sure you saved the YAML file.
    2. Go to the terminal with your current bec session. Run the following command to load the updated config into BEC:
    ``` py
    bec.config.update_session_with_file("<my-config.yaml>")
    ```

=== "Device Manager GUI"

    1. Review the prepared config in the table of the Device Manager view.
    2. Click the "Upload Config" button in the toolbar to load the updated config into BEC.
    3. Optional: Run a connectivity test prior to uploading the config, to make sure that all devices can be connected to.






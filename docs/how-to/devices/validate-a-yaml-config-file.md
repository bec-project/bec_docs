---
related:
  - title: Managing Device Configurations
    url: learn/devices/managing-device-configs.md
  - title: Device Configuration in BEC
    url: learn/devices/device-config-in-bec.md
  - title: Load and Save a Device Session
    url: how-to/devices/load-and-save-a-device-session-from-the-bec-ipython-client.md
---

# Validate a YAML configuration file for BEC

!!! Info "Overview"
    Validate a YAML file before loading it to BEC, so you can catch syntax and connection problems early.

## Prerequisites

- You have the BEC Python environment activated.
- You know the path to the YAML file you want to validate.
- If the connection should be tested, you can access the underlying devices from the machine where you run the validation.

## 1. Run a static validation

To validate the structure of a device configuration file, run:

```bash
ophyd_test --config ./path/to/my/config/file.yaml
```

This checks whether the configuration can be parsed and validated as a BEC device configuration.

## 2. Check whether devices can also connect

If you also want to test device creation and connection, add `--connect`:

```bash
ophyd_test --config ./path/to/my/config/file.yaml --connect
```

Use this when the target environment has access to the underlying devices, and you want to catch connection issues before loading the config into a running session.

![ophyd_test_is_valid.png](../../assets/ophyd_test_is_valid.png)

## 3. Load the file after validation

Once the file validates successfully, load it from the BEC IPython client:

```py
bec.config.update_session_with_file("./path/to/my/config/file.yaml")
```

!!! success "Congratulations!"

    You can now validate a device configuration with `ophyd_test` before loading it to BEC.


!!! warning "Validation was not successful"

    If you encounter validation errors, these details are printed in the terminal. In addition, running the test also writes a report to `./device_test_reports/<file_name>.txt` in the current working directory. This file includes an overview of the encountered errors during the test run, and is helpful to identify and fix problems in the configuration file.

    ![dev_show_all.png](../../assets/static_device_test_with_errors.png)

## Common Pitfalls

- A static validation does not prove that all devices are reachable. Use `--connect` when you also need a connection check.
- A successful validation does not replace reviewing the loaded device session. After loading the file, inspect the device session using `dev.show_all()` in the client.
- Connection checks depend on where they run. A file may validate on one machine but fail to connect on another machine if the network or device availability differs.

## Next Steps

- Continue with [Load and Save a Device Session](load-and-save-a-device-session-from-the-bec-ipython-client.md) to apply the file.

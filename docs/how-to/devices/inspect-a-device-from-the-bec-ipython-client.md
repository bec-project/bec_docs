---
related:
  - title: Load Your First Config
    url: getting-started/quick-start/02-load-your-first-config.md
  - title: ophyd Kind in BEC
    url: learn/devices/ophyd-kinds.md
  - title: Change Config Signals from the BEC IPython Client
    url: how-to/devices/change-config-signals-from-the-bec-ipython-client.md
---

# Inspect a Device from the BEC IPython Client

!!! Info "Overview"
    Inspect a device from the BEC IPython client so you can see its summary, live values, and configuration-style signals.

## Prerequisites

- You have a running BEC IPython client session.
- A device configuration is already loaded.
- You know the device name you want to inspect, for example `samx`.

## 1. List the available devices

Start by checking which devices are available in the current session:

```py
dev.show_all()
```

This prints the devices known to the client together with status information such as whether they are enabled and which class they use.

!!! tip "Use tab completion"

    Type `dev.` and press `TAB` to explore available device names directly in the shell.

## 2. Print the device overview

To inspect one device in more detail, evaluate the device object:

--[]->[]--test_snippet--test_quickstart.py:test_inspect_samx:Device overview

This prints a compact overview of the device, including:

- general metadata such as `enabled`, `readoutPriority`, and device class
- current values
- config signals


Use this first when you want a quick overview without manually calling several methods.

!!! learn "[Learn more about device configuration](../../learn/devices/device-config-in-bec.md){ data-preview }"

!!! learn "Whether a signal is included in `.read()` or `.read_configuration()` depends on its ophyd Kind. [Learn more about ophyd Kind](../../learn/devices/ophyd-kinds.md){ data-preview }"

## 3. Print the device summary

To get a more detailed summary of the device, including all its defined signals and their ophyd Kinds, call

```py
dev.samx.summary()
```

![device summary](device_summary.png)

## 3. Read the live values

To inspect the current read values directly, call `read()`:

--[]->[]--test_snippet--test_quickstart.py:test_samx_read:Read

This is the fastest way to see the device's current readings in dictionary form.

For positioners, you can also use `wm` for a compact readback and setpoint view:

```py
dev.samx.wm
```

## 4. Read the config signals

To inspect the configuration-style signals, call `read_configuration()`:

```py
dev.samx.read_configuration()
```

Use this when you specifically want values that belong to the device setup rather than the normal `read()` output.

!!! success "Congratulations!"

    You can now inspect a device from the BEC IPython client with `dev.show_all()`, `dev.<name>`, `dev.<name>.read()`, and `dev.<name>.read_configuration()`.

## Common Pitfalls

- `dev.samx` prints a summary, but it does not return the same structure as `dev.samx.read()`.
- If `dev.samx` does not exist, the device is either not loaded or has a different name in the current config.
- `read()` and `read_configuration()` serve different purposes. If a value is missing from `read()`, check whether it is a config signal instead.

## Next Steps

- If you want to change a signal-backed configuration value from the client, continue with [Change Config Signals from the BEC IPython Client](change-config-signals-from-the-bec-ipython-client.md).

---
related:
  - title: Load and export a config
    url: getting-started/load-and-export-a-config.html
---

# Load your first config

In this tutorial you will load the demo device configuration and use it to explore the first devices in your BEC
session. By the end, you will have a live `dev` namespace with simulated devices and know the two fastest ways to
inspect a device from the shell.

## Before you start

Continue in the same BEC session you opened in [01 Open BEC at PSI](open-bec-at-psi.md) or
[02 Open BEC outside of PSI](open-bec-outside-psi.md). For this tutorial, use a training, local, or test deployment
rather than a production beamline session.

## 1. Load the demo configuration

BEC ships with a simulated device framework for development, testing, and onboarding. The demo configuration mimics a
small beamline environment with multiple positioners, detectors, and cameras, so you can learn the workflow without
connecting to real hardware.

Load that demo configuration now:

--[]->[]--test_snippet--test_getting_started.py:test_load_demo_config:load the demo config

## 2. Check the available devices

Inspect the devices currently available in the session:

--[]->[]--test_snippet--test_getting_started.py:test_show_all_devices:show all the devices in the session

You should see a list of simulated devices, including motors such as `samx` and `samy`.

!!! tip

    BEC provides tab completion throughout the shell. Try `dev.` and press `TAB` to discover available devices and attributes, or `scans.` to explore the scan interface.

## 3. Inspect one device

Start with one of the simulated motors:

--[]->[]--test_snippet--test_getting_started.py:test_inspect_samx:inspect the samx motor

This prints a device overview with the most important metadata, current values, and config signals. Use this overview
when you want to understand what a device is, whether it is enabled, what limits it has, and which
signals are currently changing.

## 4. Inspect the live values directly

--[]->[]--test_snippet--test_getting_started.py:test_samx_read:read from the samx motor

`.read()` returns the current readback values for the device and is the quickest way to inspect its live state from the
shell.

## What you learned

You loaded the demo configuration, saw that BEC includes a simulated beamline for training and development, inspected
the available devices, and learned the two most useful shell entry points for a first inspection: `dev.samx` for the
device overview and `dev.samx.read()` for live values. In the next step you will start moving a device and learn the
difference between blocking and non-blocking motion commands.

## Next step

Continue with [04 Move a device](move-a-device.md), where you will use the newly loaded motors for your first controlled
move.

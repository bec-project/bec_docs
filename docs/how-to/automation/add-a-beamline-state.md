---
related:
  - title: Learn about BEC automation
    url: learn/automation/index.md
  - title: Add a signal to BEC
    url: learn/how-to/devices/add-an-epics-signal.md
---

# Add a beamline state

!!! Info "Goal"
    Register a beamline state in BEC through either the CLI or the GUI, and observe when it changes

## Prerequisites

- A device/signal which you wish to monitor. 

(This how-to uses a device from the [demo config]("getting-started/quick-start/02-load-your-first-config.md"){ data-preview }, which you can replace with your device of choice.)

## Instructions

/// tab | :material-console: BEC Shell

### 1. Import the config class for the type of state you wish to add

We will be using a beamline state which monitors whether a device is within specified limits.

```python
from bec_lib.bl_states import DeviceWithinLimitsStateConfig
```

### 2. Create the configuration

Replace `samx` in the following snippet with your signal of choice, and adjust the limit values for that device, or
leave it as is to test it out with the demo config:

```python
samx_config = DeviceWithinLimitsStateConfig(name="samx_in_limits", device="samx", high_limit=10, low_limit=-10)
```

### 3. Add the configuration to the beamline state manager

(if you renamed the config variable in the previous step, adjust it here too)

```python
bec.beamline_states.add(samx_config)
```

### 4. Inspect the result

--[]->[]--test_snippet--test_howto_automation.py:test_show_all_bl_states:Inspect the beamline states


///
/// tab | :material-television-guide: BEC Widgets GUI

Coming soon!
<!-- TODO: Add GUI beamline state guide with screenshots -->

///


!!! Success "Congratulations!"
    You have successfully added a simple beamline state to BEC.

## Next Steps

- Use your new state for the scan interlock!

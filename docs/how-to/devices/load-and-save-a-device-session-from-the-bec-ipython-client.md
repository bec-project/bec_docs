---
related:
  - title: Device Configuration in BEC
    url: learn/devices/device-config-in-bec.md
  - title: Managing Device Configurations
    url: learn/devices/managing-device-configs.md
  - title: Inspect the Current Device Session
    url: how-to/devices/inspect-the-current-device-session-from-the-bec-ipython-client.md
---

# Load and Save a Device Session

!!! Info "Overview"
    Load a device configuration file into the current BEC session and save the current session back to disk from the BEC IPython client.

## Prerequisites

- You have a running BEC IPython client session.
- You know the path to the YAML file you want to load.
- The YAML file is accessible from the machine where the BEC IPython client is running.

## 1. Load a config file into the current session

To update the current device session from a YAML file, call:

```py
bec.config.update_session_with_file("./path/to/my-config.yaml")
```

This loads the file from disk and sends the resulting configuration to the running BEC services.

If the file changes devices that already exist in the current session, BEC may prompt you to resolve conflicts before applying the update.

!!! learn "[Learn more about the device configuration in BEC](../../learn/devices/device-config-in-bec.md){ data-preview }"

## 2. Verify that the new session is active

After loading the file, inspect the current session from the client:

```py
dev.show_all()
```

Use this to confirm that the expected devices are present and that their status and class information match the file you loaded.

## 3. Save the current session to disk

To write the currently active device session to a YAML file, call:

```py
bec.config.save_current_session("./config_saved.yaml")
```

This exports the full current session as it exists in BEC at that moment.

Use this when you want to:

- keep a copy of the active session
- create a starting point for further edits
- persist runtime changes in a file before reusing them later

## 4. Reload a saved session later

A saved session file can be loaded again with the same command:

```py
bec.config.update_session_with_file("./config_saved.yaml")
```

This is a practical workflow when you want to export the current session, edit the YAML file, and then apply it again.

!!! success "Congratulations!"

    You can now load a device configuration file into the current BEC session with `bec.config.update_session_with_file(...)` and export the active session with `bec.config.save_current_session(...)`.

## Common Pitfalls

- Loading a file updates the current session in BEC. It does not keep the previous session unless you saved it separately.
- Runtime changes made in a session are not automatically written back to the original YAML file. Use `bec.config.save_current_session(...)` if you want a file on disk.
- If BEC reports conflicts during loading, review them carefully instead of forcing the update unless you are sure the new file should replace the current session values.

## Next Steps

- Use [Validate a Device Configuration](validate-a-device-configuration.md) before loading a new file when you want an extra check.
- Use [Inspect the Current Device Session](inspect-the-current-device-session-from-the-bec-ipython-client.md) to review what is currently active in the session.

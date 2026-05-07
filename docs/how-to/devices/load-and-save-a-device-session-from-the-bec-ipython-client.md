---
related:
  - title: Device Sessions in BEC
    url: learn/devices/device-sessions-in-bec.md
  - title: Error Handling During Session Updates
    url: learn/devices/error-handling-during-session-updates.md
  - title: Device Configuration in BEC
    url: learn/devices/device-config-in-bec.md
  - title: Managing YAML Configs
    url: learn/devices/managing-yaml-configs.md
  - title: Inspect the Current Device Session
    url: how-to/devices/inspect-the-current-device-session-from-the-bec-ipython-client.md
  - title: Validate a YAML configuration file for BEC
    url: how-to/devices/validate-a-yaml-config-file.md
---

# Load and Save a Device Session

!!! Info "Overview"
    Load a YAML configuration file as a new session to BEC, and save the current session to a YAML file on disk from the BEC IPython client.

## Prerequisites

- You have a running BEC IPython client session.
- You know the path to the YAML file you want to load.
- The YAML file is accessible from the machine where the BEC IPython client is running.

## 1. Load a YAML file into the current session

To update the current device session from a YAML file, call:

```py
bec.config.update_session_with_file("./path/to/my-config.yaml")
```

This loads the file from disk and sends the resulting configuration to the running BEC services.

!!! info

    Every time you load a new YAML file, BEC automatically saves the previous session to a backup file in a beamline-defined path together with a timestamp. The path is defined in the `client_data_base_path` field of the deployment config for your beamline, but it will also be printed in the terminal whenever you update your session.

In case you have a previous session with devices already active, the new file will update the current session with the new values. 
If there are conflicts between device configurations as defined in the new file and the current session, BEC will prompt you with options to resolve them. 
This allows you to review the differences and decide how to proceed instead of automatically overwriting the current session with the new file.

!!! learn "[Learn more about device sessions and device configurations in BEC](../../learn/devices/device-sessions-in-bec.md){ data-preview }"

## 2. Verify that the device session was loaded successfully

After loading the file, inspect the current session from the client:

```py
dev.show_all()
```

Use this to confirm that the expected devices are present and that their status and class information match the file you loaded. In case of failed connections to devices, they will appear as disabled in the session, and you can check the terminal output for details about which devices failed to connect and why.

!!! learn "[Learn more about error handling during session updates](../../learn/devices/error-handling-during-session-updates.md){ data-preview }"

## 3. Save the current device session to disk

From the BEC IPython client, you can also save the current session to a YAML file on disk. This is useful when you want to keep a copy of the active session, create a starting point for further edits, or persist runtime changes in a file before reusing them later.

```py
bec.config.save_current_session("./config_saved.yaml")
```

This exports the device session in BEC with all current values of its device configurations.

Use this when you want to:

- keep a copy of the active session
- create or update a YAML file based on the current session

## 4. Reload a recovery file

As mentioned in step 1, every time you load a new YAML file, BEC automatically saves the previous session to a backup file in a beamline-defined path together with a timestamp. This allows you to recover the previous session if needed.
Let's assume the path to the recovery directory is `<file_dir>` and the file name is `recovery_config_2026-05-04_08-39-23.yaml`. You can load this recovery file with the same command as before:

```py
bec.config.update_session_with_file("<file_dir>/recovery_config_2026-05-04_08-39-23.yaml")
```

!!! success "Congratulations!"

    You can now load a device configuration file into the current BEC session with `bec.config.update_session_with_file(...)` and export the active session with `bec.config.save_current_session(...)`.

## Common Pitfalls

- Updating the session with a new YAML file overwrites the current session values with the new file. There are currently no options to merely update a subset of devices or fields. All device configurations that should be loaded into the session must be included in the YAML file.
- Runtime changes made in a session are not automatically written back to the original YAML file. Use `bec.config.save_current_session(...)` if you want a file on disk.
- If BEC reports conflicts during loading, review them carefully instead of forcing the update unless you are sure the new file should replace the current session values.

## Next Steps

- Use [Validate a YAML configuration file for BEC](validate-a-yaml-config-file.md) before loading a new file when you want an extra check.
- Use [Inspect the Current Device Session](inspect-the-current-device-session-from-the-bec-ipython-client.md) to review what is currently active in the session.

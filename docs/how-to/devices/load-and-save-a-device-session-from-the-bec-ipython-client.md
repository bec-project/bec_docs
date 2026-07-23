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
    Load a YAML configuration file as a new session in BEC, add devices from another YAML file, and save the current session to YAML from the BEC IPython client.

## Prerequisites

- You have a running BEC IPython client session.
- You know the path to the YAML file you want to load.
- The YAML file is accessible from the machine where the BEC IPython client is running.

## 1. Replace the current session from a YAML file

To replace the current device session from a YAML file, call:

```py
bec.config.update_session_with_file("./path/to/my-config.yaml")
```

This loads the file from disk and sends the resulting configuration to the running BEC services.

!!! info

    Every time you load a new YAML file, BEC automatically saves the previous session to a recovery file in a beamline-defined path together with a timestamp. The path will also be printed in the terminal whenever you replace your session.

If a previous session is already active, `update_session_with_file(...)` replaces it with the configuration from the new file.
If there are conflicts between device configurations as defined in the new file and the current session, BEC will prompt you with options to resolve them.
This allows you to review the differences and decide how to proceed instead of automatically overwriting the current session with the new file.

!!! learn "[Learn more about device sessions and device configurations in BEC](../../learn/devices/device-sessions-in-bec.md){ data-preview }"

## 2. Add devices from another YAML file

If you want to keep the current session and only add new devices from another YAML file, call:

```py
bec.config.add_to_session("./path/to/additional-devices.yaml")
```

This keeps the current session active and adds the new device entries from the file.

Use this when you want to:

- extend the current session with new devices
- load another config fragment without replacing the full session

If a device in the file already exists in the current session, the request is rejected instead of overwriting the existing device definition. Use `update_session_with_file(...)` when you want to replace the session with a complete new configuration.

## 3. Verify that the device session was loaded successfully

After loading or extending the session, inspect the current session from the client:

```py
dev.show_all()
```

Use this to confirm that the expected devices are present and that their status and class information match the file you loaded. In case of failed connections to devices, they will appear as disabled in the session, and you can check the terminal output for details about which devices failed to connect and why.

!!! learn "[Learn more about error handling during session updates](../../learn/devices/error-handling-during-session-updates.md){ data-preview }"

## 4. Save the current device session to disk

From the BEC IPython client, you can save the current session to a YAML file on disk. This is useful when you want to keep a copy of the active session, create a starting point for further edits, or persist runtime changes in a file before reusing them later.

```py
bec.config.save_current_session("./config_saved.yaml")
```

This exports the device session in BEC with all current values of its device configurations.

Use this when you want to:

- keep a copy of the active session
- create or update a YAML file based on the current session

If you want to export the session as a split YAML bundle grouped by `deviceTags`, use:

```py
bec.config.save_current_session("./device_config_bundle", split_by_tag=True)
```

This creates a bundle directory containing a `main.yaml` manifest and one YAML file per tag. The manifest links the tag files with `!include`, which is useful for larger beamline setups that keep subsystems in separate files. Note that if you use multiple tags for a device, it will take the first tag in the list to determine which file to write the device configuration to.

## 5. Reload a recovery file

As mentioned in step 1, every time you replace the session from a YAML file, BEC automatically saves the previous session to a recovery file in a beamline-defined path together with a timestamp. This allows you to recover the previous session if needed.
Let's assume the path to the recovery directory is `<file_dir>` and the file name is `recovery_config_2026-05-04_08-39-23.yaml`. You can load this recovery file with the same command as before:

```py
bec.config.update_session_with_file("<file_dir>/recovery_config_2026-05-04_08-39-23.yaml")
```

!!! success "Congratulations!"

    You can now replace the current device session with `bec.config.update_session_with_file(...)`, add new devices with `bec.config.add_to_session(...)`, and export the active session with `bec.config.save_current_session(...)`.

## Common Pitfalls

- `bec.config.update_session_with_file(...)` replaces the current session with the content of the new file. Use it when you want one file to define the full session.
- `bec.config.add_to_session(...)` only adds new devices. It does not update the definition of devices that already exist in the session.
- Runtime changes made in a session are not automatically written back to the original YAML file. Use `bec.config.save_current_session(...)` if you want a file on disk.
- If BEC reports conflicts during loading, review them carefully instead of forcing the update unless you are sure the new file should replace the current session values.

## Next Steps

- Use [Validate a YAML configuration file for BEC](validate-a-yaml-config-file.md) before loading a new file when you want an extra check.
- Use [Inspect the Current Device Session](inspect-the-current-device-session-from-the-bec-ipython-client.md) to review what is currently active in the session.

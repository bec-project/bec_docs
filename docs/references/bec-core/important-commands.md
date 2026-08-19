---
related:
  - title: Restart the BEC server
    url: how-to/general/restart-the-bec-server.md
  - title: Access BEC History
    url: how-to/scans/access-bec-history.md
  - title: Inspect the Current Device Session
    url: how-to/devices/inspect-the-current-device-session-from-the-bec-ipython-client.md
  - title: GUI RPC Interface
    url: references/bec-widgets/gui-rpc-interface.md
---

# Important BEC commands

This page collects frequently used BEC shell commands and BEC IPython client commands.

Use it as a lookup page when you need the command name, a reminder of the syntax, or a quick hint about what the
command affects.

## Shell commands

### Start the BEC IPython client

The `bec` command is installed by the `bec_ipython_client` package.

| Command | Use |
| --- | --- |
| `bec` | Start the BEC IPython client. |
| `bec --nogui` | Start the client without opening the GUI. |
| `bec --gui-id <id>` | Connect the client to an existing GUI instead of creating a new one. |
| `bec --dont-wait-for-server` | Start the client without waiting for the server to become available. |
| `bec --post-startup-file <path>` | Run a Python file after the client startup sequence. |

Common shared options added by the BEC service argument parser:

| Option | Use |
| --- | --- |
| `--config <path>` | Use a specific BEC config file. |
| `--bec-server <host:port>` | Connect directly to a Redis server address instead of loading a config file. |
| `--log-level <level>` | Set the console log level. |
| `--file-log-level <level>` | Set the file log level. |
| `--redis-log-level <level>` | Set the Redis log level. |
| `--user <name>` | Use a specific user name for the client session. |

`--config` and `--bec-server` are mutually exclusive.

### Manage the BEC server stack

The `bec-server` command is installed by the `bec-server` package.

| Command | Use |
| --- | --- |
| `bec-server start` | Start the BEC service stack. |
| `bec-server stop` | Stop the BEC service stack. |
| `bec-server restart` | Restart the BEC service stack. |
| `bec-server attach` | Attach to the running BEC tmux session. |


### Start individual BEC services

The `bec-server` package also installs service-specific entry points.

| Command | Service |
| --- | --- |
| `bec-scihub` | Start the SciHub service. |
| `bec-device-server` | Start the device server. |
| `bec-scan-server` | Start the scan server. |
| `bec-scan-bundler` | Start the scan bundler. |
| `bec-file-writer` | Start the file writer service. |
| `bec-dap` | Start the data processing service. |
| `bec-procedure-worker` | Start the procedure worker. |

## BEC IPython client commands

### Built-in line magics

The BEC IPython client registers the following line magics:

| Magic | Use |
| --- | --- |
| `%abort` | Abort the active scan. |
| `%reset` | Reset the scan queue. |
| `%deferred_pause` | Request a queue pause after the current scan. This is only useful when scans are queued. |
| `%restart` | Restart the active scan. |
| `%halt` | Emergency stop. Halt the scan without cleanup. |
| `%stop` | Stop all devices. |
| `%server_restart` | Request a restart of the BEC server stack. |
| `%schema <scan_name>` | Print the metadata schema for a scan. |
<!-- Temporarily hidden until fully supported:
| `%pause` | Pause the active scan immediately. |
| `%resume` | Continue a paused scan. |
| `%su <user>` | Switch the current BEC user. |
-->

### Common client helper APIs

These helpers are available from the `bec` object or from standard session objects loaded into the client namespace.

| API | Use |
| --- | --- |
| `bec.show_last_alarm()` | Print the most recent alarm with rich formatting. |
| `dev.show_all()` | List devices in the current device session. |
| `bec.history[-1]` | Access the most recent scan in the local scan history. |
| `gui.available_widgets` | Inspect GUI widget classes that can be created remotely. |

## Notes

- Available scans, macros, device names, and beamline-specific helpers depend on the currently loaded deployment and session.
- For GUI-specific commands, continue with [GUI RPC Interface](../bec-widgets/gui-rpc-interface.md).

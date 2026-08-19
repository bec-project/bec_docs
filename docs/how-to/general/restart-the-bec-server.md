---
related:
  - title: Open BEC
    url: getting-started/quick-start/01-open-bec.md
  - title: Install BEC Locally
    url: how-to/general/install-bec-locally.md
  - title: Connect to the BEC VM
    url: how-to/general/connect-to-the-bec-vm-with-xfreerdp.md
---

# Restart the BEC server

!!! Info "Overview"
    Restart the BEC service stack either from a terminal on the BEC host or directly from an active BEC IPython client. 

## Prerequisites

- No scan or other critical acquisition is currently running.
- You know which machine runs the BEC services.
- If you restart from a terminal, you can log in to that machine and activate the correct Python environment.
- If you restart from the client, you already have a working BEC IPython client session.

!!! warning "Restart only when BEC is idle"

    Restarting the server interrupts the running services and briefly disconnects clients. Do not restart BEC while scans, device motions, or file writing are still active.

## 1. Choose the restart method

/// tab | BEC IPython client

Use this path when you already have an active BEC client session and do not want to open a second terminal on the BEC host.

From the BEC prompt, run:

```py
%server_restart
```

///

/// tab | Terminal on the BEC host

Use this path when you want to restart BEC directly on the machine that runs the services. It is the only option if the server is not responding or it is not running yet.

If BEC runs on a remote VM or server, open a shell on that machine first:

/// tab | Template
```bash
ssh <user>@<bec-vm-host>
```

`cd` to the directory where the BEC services are installed. The exact path depends on your setup:

```bash
cd /sls/<xname>/config/bec/<deployment_name>
```

Activate the Python environment that provides the BEC commands.

```bash
source ./bec_venv/bin/activate
```
///

/// tab | Example
```bash
ssh personal_u@x99sa-bec-001.psi.ch
```

`cd` to the directory where the BEC services are installed. The exact path depends on your setup:

```bash
cd /sls/x99sa/config/bec/production
```

Activate the Python environment that provides the BEC commands.

```bash
source ./bec_venv/bin/activate
```
///

Then restart the BEC services:

```bash
bec-server restart
```

This stops the running services and starts them again with the currently installed code and configuration.

If you want to inspect the stack after the restart, you can attach to the running services:

```bash
bec-server attach
```

///

## 2. Wait for the services to come back

After the restart command, give the services a moment to come back up.

If you restarted from the IPython client, the client may briefly lose its connection while the services restart. Wait for the connection to recover, or reopen the client if needed.

## 3. Verify that BEC is ready again

Once the restart is complete, confirm that the server and client are usable again with a small check from the BEC prompt:

```py
dev.show_all()
```

You can also verify that your intended change was picked up, for example by checking that a new scan, device configuration, or plugin behavior is now available.

!!! success "Congratulations!"

    You can now restart the BEC server either from the host terminal with `bec-server restart` or from the BEC IPython client with `%server_restart`.

## Common pitfalls

- Restarting while an acquisition is still running.
- Running `bec-server restart` on the wrong machine.
- Forgetting to activate the Python environment before calling `bec-server`.
- Expecting the IPython client to stay responsive during the short restart window.

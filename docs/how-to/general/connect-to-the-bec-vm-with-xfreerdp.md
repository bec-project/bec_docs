---
related:
  - title: Update BEC to a new version
    url: how-to/general/update-deployment.md
---

# Connect to the BEC VM with xfreerdp

!!! Info "Goal"
    Open a remote desktop session to the BEC virtual machine from a Linux workstation using `xfreerdp`.

    This is a PSI-specific guide. It assumes that your beamline provides a BEC VM that is reachable from your current network.

## Pre-requisites
- You are on a Linux machine with `xfreerdp` installed.
- You know the hostname of the BEC VM, for example `x99sa-bec-001.psi.ch`.
- You are a PSI beamline scientist or staff member with access to the BEC VM.
- You are connected to the PSI network or the relevant beamline network.

## 1. Check that `xfreerdp` is available

In a terminal, run:

```bash
xfreerdp /version
```

If the command is not found, install FreeRDP first using your Linux distribution's package manager.

## 2. Start the remote desktop session

Run `xfreerdp` with your VM hostname and the recommended options:

```bash
xfreerdp /v:<bec-vm-host>.psi.ch /dynamic-resolution +clipboard +fonts
```

The most important arguments are:

- `/v:` for the VM hostname
- `/dynamic-resolution` to resize the remote desktop together with your local window
- `+clipboard` to enable copy and paste between the local machine and the VM
- `+fonts` to improve font rendering in the remote session

## 3. Enter your password and log in

After the command starts:

1. enter your personal PSI username and password when prompted
2. wait for the desktop session to open
3. verify that you can see the VM desktop and interact with it normally


## 4. Disconnect from the session

When you are done:

- log out from the VM desktop to not leave your personal session open

!!! success "Congratulations!"
    You have successfully connected to the BEC VM using `xfreerdp`.

## Common pitfalls
- Using the wrong hostname for the VM.
- Trying to connect from outside the PSI or beamline network.

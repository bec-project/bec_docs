---
related:
  - title: Connect to the BEC VM with xfreerdp
    url: how-to/general/connect-to-the-bec-vm-with-xfreerdp.md
---

# Set the Active Account with `bec-set-account`

!!! Info "Goal"
    Set the active account for the BEC server using the local `bec-set-account` wrapper from the beamline config directory.

    This is a PSI-specific guide. It assumes that you already know the correct process-group account, for example `p12345`.

## Pre-requisites
- You are in the beamline config directory that contains the `bec-set-account` wrapper, for example `/sls/x99sa/config/bec/production`.
- You have write access to the config directory and permission to change the active account, typically a PSI beamline scientist or staff member.
- You know the process-group account you want to activate, for example `p12345`.
- You are connected to the PSI or relevant beamline network.

## 1. Check that `bec-set-account` is available

In a terminal, run:

```bash
./bec-set-account --help
```

You should see help output similar to:

```text
Usage: ./bec-set-account <pgroup>

Change the active pgroup in BEC to the specified pgroup.
```

## 2. Set the active account

On the beamline, the wrapper already knows how to update the BEC server account. You only need to specify the process-group account:

```bash
./bec-set-account p12345
```

The command sets the active account for the BEC server.

## 3. Verify the result

If the command succeeds, it prints a confirmation message similar to:

```text
Account p12345 has been set successfully.
```

!!! success "Congratulations!"
    You have successfully set the active account with `bec-set-account`.

## Common pitfalls
- Using a process-group value that does not match the required format `p` followed by exactly five digits.
- Running the command outside the config directory that contains the wrapper.
- Running the command on a machine that cannot reach the BEC server environment.

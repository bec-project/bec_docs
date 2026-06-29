---
related:
  - title: Add a beamline state
    url: how-to/automation/add-a-beamline-state.md
  - title: Learn about BEC automation
    url: learn/automation/index.md
---

# Configure the scan interlock

The scan interlock actor allows automatically placing a lock on the primary scan queue when a beamline state goes
outside of desired parameters.

!!! Info "Goal"
    Change the settings for the scan interlock.

## Prerequisites

- Have a beamline state registered, to which the interlock should react.

## 1. Enable or disable the scan interlock

/// tab | :material-console: BEC Shell

The interlock can be switched on or off through the `enabled` property of the high-level interface
under `bec.builtin_actors.scan_interlock`. Set it to `True` to enable it and `False` to disable it.

```python
bec.builtin_actors.scan_interlock.enabled = True
```

///
/// tab | :material-television-guide: BEC Widgets GUI

Coming soon!

<!-- TODO: Add GUI screenshot -->

///

## 2. Add a beamline state to the interlock

/// tab | :material-console: BEC Shell

A beamline state can be "added to the interlock" meaning that the interlock is triggered whenever that state goes
out of bounds.

```python
bec.builtin_actors.scan_interlock.add_state_to_interlock(<state name>, [<allowed status values>])
```

Where `state_name` is the `name` parameter the state configuration was defined with, and the allowed status values are
any subset of `valid`, `invalid`, `warning`, `unknown`. If the current status of the beamline state is not in the list
provided, the interlock will trigger. The default value is `["valid", "warning"]`, so the interlock will trigger whenever
the state is `invalid` or `unknown`. For example, the following line:

```python
bec.builtin_actors.scan_interlock.add_state_to_interlock("samx_in_limits")
```

will add the [test state created in the how-to]("how-to/automation/add-a-beamline-state.md"){ data-preview } with the
default set of allowed values.

///
/// tab | :material-television-guide: BEC Widgets GUI

Coming soon!

<!-- TODO: Add GUI screenshot -->

///

## 3. Choose the trigger setting

/// tab | :material-console: BEC Shell

The interlock trigger mode allows choice over the behaviour when the interlock triggers. It can be set through the
`trigger_setting` property of the high-level interface under `bec.builtin_actors.scan_interlock`. The interlock always
places a lock on the queue, so that the next scheduled item will not run until it is removed. This setting dictates what
happens to the currently running scan, according to the following table:

| Value            | Behaviour                                                   |
| ---------------- | ----------------------------------------------------------- |
| `"do_nothing"`   | :material-arrow-collapse-right: Let the current scan finish |
| `"restart_scan"` | :material-restart: Abort and reschedule the running scan    |
| `"pause_scan"`   | :material-pause: Pause the running scan (work in progress)  |

```python
bec.builtin_actors.scan_interlock.trigger_setting = "restart_scan"
```

///
/// tab | :material-television-guide: BEC Widgets GUI

Coming soon!

<!-- TODO: Add GUI screenshot -->

///

!!! Success "Congratulations!"
You can now make use of the scan interlock feature

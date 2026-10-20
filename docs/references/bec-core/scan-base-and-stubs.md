---
related:
  - title: Write an alternating-position scan
    url: getting-started/next-steps/write-a-scan.md
  - title: Scan lifecycle and authoring responsibilities
    url: learn/scans/scan-lifecycle.md
  - title: Test a scan
    url: how-to/scans/test-a-scan.md
---

# Scan development API

This reference describes the scan class, hooks, metadata, and runtime operations used to
implement a custom scan. For a complete example, see
[Write an alternating-position scan](../../getting-started/next-steps/write-a-scan.md).
For lifecycle design and recovery responsibilities, see
[The scan lifecycle](../../learn/scans/scan-lifecycle.md).

## Scan class and inputs

Import the base class and trigger type from `bec_server.scan_server.scans.scan_base`.
Subclass `ScanBase`, define experimental inputs in `__init__`, and forward server arguments
with `super().__init__(**kwargs)`.

| Attribute | Default | Contract |
| --- | --- | --- |
| `scan_name` | `"base_scan"` | Override with a unique, valid Python identifier; this becomes the client callable name |
| `scan_type` | `ScanType.SOFTWARE_TRIGGERED` | Software triggering issues triggers through scan operations; hardware triggering delegates acquisition timing to a device |
| `is_scan` | `True` | Whether the request creates an acquisition scan |
| `is_internal` | `False` | Internal scans are omitted from the public client scan namespace |
| `arg_input` | `{}` | Ordered types/annotations for repeated positional argument bundles; unnecessary for fixed signatures |
| `arg_bundle_size` | `{"bundle": 0, "min": None, "max": None}` | Bundle width and minimum/maximum bundle counts; set together with `arg_input` for bundled signatures |

`ScanType.HARDWARE_TRIGGERED` and `ScanType.SOFTWARE_TRIGGERED` describe who supplies the
acquisition trigger. They do not by themselves specify whether a motor moves continuously.

For individual inputs, use `Annotated[T, ScanArgument(...)]` from `bec_lib.scan_args`.
`ScanArgument` can supply descriptions, bounds such as `gt`/`ge`, units, and GUI labels.
`reference_units="motor"` refers to the device argument named `motor`.
`DefaultArgType.Relative` and `DefaultArgType.ExposureTime` provide common input annotations.
The server serializes the scan signature for client validation and help.

`gui_config`, when defined on the class, maps display groups to parameter names. Plugin
argument modifiers can change the published signature and defaults. Inspect the installed
scan's client help when using a deployment's customized interface.

## Server resources and scan state

The assembler supplies required `scan_id`, `redis_connector`, `device_manager`,
`instruction_handler`, `request_inputs`, and `system_config`. Optional base arguments include
readout selections (`monitored`, `on_request`), `scan_modifier`, user/request metadata,
`scan_queue`, `run_on_exception_hook`, and `additional_scan_parameters`.
Do not construct these resources in the client or issue runtime device RPC in `__init__`.

| Instance attribute | Purpose |
| --- | --- |
| `dev` | Server device container |
| `actions` | `ScanActions` instance for this scan |
| `components` | `ScanComponents` instance for this scan |
| `scan_info` | Validated `ScanInfo` model used in published scan state |
| `positions` | Author-managed trajectory; initialize and publish it during preparation |
| `start_positions` | Author-managed starting positions, initialized as an empty list |

`positions` on the scan and `scan_info.positions` are separate attributes: update the
published metadata explicitly. For `N` visits and `M` motors, use an array of shape `(N, M)`;
a per-point target passed to a component has shape `(M,)`.

### Metadata used by step scans

| `ScanInfo` field | Default | Meaning |
| --- | --- | --- |
| `positions` | `None` | Combined motor targets in visit order |
| `num_points` | `0` | Number of logical visits/points |
| `num_monitored_readouts` | `0` | Expected monitored readouts during preparation; updated to the actual requested count at normal close |
| `relative` | `False` | Coordinate convention recorded for this scan |
| `exp_time` | `0` | Nonnegative exposure time in seconds |
| `frames_per_trigger` | `1` | Positive detector frame count per trigger |
| `burst_at_each_point` | `1` | Positive number of trigger/read cycles per logical point |
| `scan_report_devices` | `[]` | Devices included in scan reporting; device objects are stored by name |
| `run_on_exception_hook` | `True` | Whether exception cleanup is requested. Halt skips the hook through a queue-item override; this field remains unchanged |

Set positions, counts, and acquisition settings before `open_scan`. For standard step
acquisition, expected monitored readouts are `num_points * burst_at_each_point`.
Model assignment is validated. `update_scan_info` writes known model fields and stores
unrecognized keyword names in `additional_scan_parameters`.

::: bec_server.scan_server.scans.scan_base.ScanBase
    options:
      show_root_heading: false
      show_source: false
      members: [update_scan_info]
      heading_level: 3

## Lifecycle hooks

Implement all abstract hooks, and decorate overrides with `@scan_hook` from
`bec_server.scan_server.scans.scan_modifier` so scan modifiers can attach to them.
The decorator does not schedule a hook or create a per-point loop.

| Hook | Caller and responsibility |
| --- | --- |
| `prepare_scan()` | Worker: resolve positions, check limits, initialize metadata and preparation statuses |
| `open_scan()` | Worker: call `actions.open_scan()` to publish the opening state |
| `stage()` | Worker: configure devices and track partial setup |
| `pre_scan()` | Worker: finish required preparation immediately before acquisition |
| `scan_core()` | Worker: execute the experimental sequence |
| `at_each_point(...)` | Scan/component: execute one visit; its signature must match the caller |
| `post_scan()` | Worker: complete acquisition and perform normal recovery |
| `unstage()` | Worker: release device setup |
| `close_scan()` | Worker: account for outstanding work and call `actions.close_scan()` |
| `on_exception(exception)` | Conditional exception path: recover from partial setup/execution; remaining normal hooks are not automatically run |

Normal worker order is prepare → open → stage → pre → core → post → unstage → close.
An exception breaks that sequence. Halt disables the exception hook; shutdown can bypass
cleanup. A custom scan must not assume that starting positions, device staging, or its
own settings are fully initialized when recovery begins.

## Actions

`ScanActions` belongs to one scan. Operations with `wait=True` wait before returning;
`wait=False` returns a `ScanStatus` for later checking. Lists of device names or `DeviceBase`
objects are accepted by the operations below where their signatures allow them.
Runtime actions check the worker's interruption state and operate with the scan's device
ownership. They are not ordinary client scan submissions.
Most actions require a running scan and belong in lifecycle hooks. Configuration methods
such as `set_device_readout_priority` can also be called in `__init__`.

The following methods cover opening/closing, device preparation, movement, readout selection,
and acquisition. `readout_time` is a scan argument published to devices. The standard
step-scan components do not apply it as an additional delay. The trigger/read component
applies exposure and settling delays.

::: bec_server.scan_server.scans.scan_actions.ScanActions
    options:
      show_root_heading: false
      show_source: false
      members:
        - open_scan
        - stage_all_devices
        - pre_scan_all_devices
        - set_device_readout_priority
        - set
        - read_baseline_devices
        - trigger_all_devices
        - read_monitored_devices
        - complete_all_devices
        - unstage_all_devices
        - add_scan_report_instruction_scan_progress
        - close_scan
      heading_level: 3

## Components

`ScanComponents` combines operations while leaving scan metadata, lifecycle ownership, and
recovery in the scan class. Component methods below wait for their necessary operations
and do not return a `ScanStatus` for callers to wait on.

- `move_and_wait` accepts one target per motor. With `last_positions`, it skips targets
  considered unchanged by `numpy.isclose`.
- `get_start_positions` returns current motor positions as a list.
- `check_limits` checks each motor column against inclusive limits. A device whose low
  limit is not below its high limit is treated as having no configured limits.
- `step_scan` iterates trajectory rows and bursts, invoking its per-point callback. The
  callback receives `(motors, position_row, last_positions=...)`; the initial
  `last_positions` is one combined position of shape `(M,)`, not a whole trajectory.
- The default per-point operation moves and waits, then calls `trigger_and_read`.
  When the scan owns software-triggered devices, triggering waits for exposure time
  multiplied by frames per trigger and for device completion before reading monitored
  devices. With no such devices, the trigger action returns immediately.

::: bec_server.scan_server.scans.scan_components.ScanComponents
    options:
      show_root_heading: false
      show_source: false
      members:
        - move_and_wait
        - get_start_positions
        - check_limits
        - step_scan_at_each_point
        - trigger_and_read
      heading_level: 3

### `step_scan(motors, positions, at_each_point=None, last_positions=None)`

Visit each row in `positions`, repeating the per-point operation according to
`scan_info.burst_at_each_point`. Returns `None` after the loop completes.

| Parameter | Shape/type and default |
| --- | --- |
| `motors` | List of device names or `DeviceBase` objects, one per trajectory column |
| `positions` | NumPy array of shape `(N, M)` |
| `at_each_point` | Callback `(motors, position_row, last_positions=...)`; defaults to `step_scan_at_each_point` |
| `last_positions` | Initial previous position of shape `(M,)`; default `None` |

The component copies the current row into `last_positions` after each visit. A callback
must perform the intended acquisition; the loop does not add a second acquisition itself.

## Status objects and errors

`ScanStatus` is a server operation status, distinct from the client's `ScanReport`.
The main lookup operations are:

| Member | Contract |
| --- | --- |
| `.wait(min_wait=None, timeout=inf, logger_wait=5, resolve_on_known_type=False)` | Wait for the operation and its sub-statuses; returns the status; raises on instruction failure or timeout |
| `.done` | Completion flag; checking it marks the status as checked but does not by itself verify success |
| `.result` | Result, or sub-results for a container; `None` until completed; a property, not a method |
| `.add_status(status)` | Attach a sub-status to a container status |

`resolve_on_known_type` is intended for internal RPC return-type handling. Custom scans
normally leave it at `False`. A wait timeout does not itself request a device stop.
Closing checks for unchecked or unfinished statuses and can issue warnings or wait for
remaining work; explicitly check dependencies before using their results or closing.

::: bec_server.scan_server.scans.scan_status.ScanStatus
    options:
      show_root_heading: false
      show_source: false
      members: [result, done, add_status]
      heading_level: 3

Relevant exceptions are imported from `bec_server.scan_server.errors`:

| Exception | Meaning |
| --- | --- |
| `LimitError` | A target is outside a motor's configured limits |
| `DeviceInstructionError` | A device instruction failed; its error information is available to the worker |
| `ScanAbortion` | Execution cannot continue or an interruption requests abortion |
| `UserScanInterruption` | A user interruption carrying exit-state information; derived from `ScanAbortion` |

These exceptions do not replace scan-specific recovery. Keep cleanup valid after partially
completed work, and inspect device and queue state before resuming an interrupted experiment.

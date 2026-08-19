# Scan Base and Stubs

`ScanBase` is the server-side base class shared by concrete BEC scans. Scan stubs and their status
objects are the lower-level building blocks used by scan actions to coordinate devices.

For most scan authors, the important practical rule is simple: inherit from `ScanBase`, implement
the lifecycle hooks you need, and prefer `self.actions` plus `self.components` over talking to
stubs directly.

## What `ScanBase` gives a scan

When a concrete scan inherits from `ScanBase`, it gets:

- `self.scan_info`: the shared runtime metadata model for the scan
- `self.actions`: high-level lifecycle and device-coordination helpers
- `self.components`: reusable motion and acquisition patterns
- `self.dev`: access to the current device container
- bookkeeping fields such as `positions`, `start_positions`, and baseline-readout status handles

Concrete scans then fill in the lifecycle by implementing hook methods such as:

- `prepare_scan`
- `open_scan`
- `stage`
- `pre_scan`
- `scan_core`
- `post_scan`
- `unstage`
- `close_scan`
- `on_exception`

These hooks are normal methods, typically decorated with `@scan_hook`.

## What scan stubs are for

Scan stubs represent lower-level device instructions and their completion state.

In everyday scan code, you usually meet them indirectly because methods on `self.actions` return a
`ScanStubStatus` object. Typical examples are:

- `self.actions.set(...)`
- `self.actions.stage_all_devices(...)`
- `self.actions.read_baseline_devices(...)`
- `self.actions.complete_all_devices(...)`

Those returned status objects let a scan decide whether to wait immediately or carry on and wait
later.

## `ScanStubStatus` in practice

`ScanStubStatus` is the handle used to track completion, errors, and returned values from an
instruction.

The most common operations are:

- `.wait()`: block until the instruction finishes or fails
- `.done`: inspect whether it has completed
- `.result`: access the returned result after completion
- `.add_status(...)`: combine several statuses into one container status

This is why many scans store handles such as `self._baseline_readout_status` or
`self._premove_motor_status` in `prepare_scan` and then wait on them later in `pre_scan` or
`close_scan`.

## Recommended authoring pattern

For most scan implementations, the cleanest pattern is:

1. store scan inputs in `__init__`
2. call `update_scan_info(...)` for metadata that depends on those inputs
3. use `prepare_scan` to build positions, check limits, and schedule progress reporting
4. use `self.actions` and `self.components` for device work instead of open-coding low-level
   instruction handling
5. keep status objects when work can proceed asynchronously, then wait at the right lifecycle step

## Related topics

- [Scans](scans.md){ data-preview }
- [Scan Actions Methods](scan-actions-methods.md){ data-preview }
- [Scan Info](scan-info.md){ data-preview }
- [Scan Components](../../learn/scans/scan-components.md){ data-preview }

---
related:
  - title: Write an alternating-position scan
    url: getting-started/next-steps/write-a-scan.md
  - title: Scan development API
    url: references/bec-core/scan-base-and-stubs.md
  - title: Test a scan
    url: how-to/scans/test-a-scan.md
---

# The scan lifecycle and authoring responsibilities

A scan class describes an experimental procedure. The client submits its inputs, while the
server constructs the class and calls its lifecycle methods to coordinate devices and
publish measurements. The framework supplies device operations; the scan author owns the
measurement sequence, its metadata, and recovery from partially completed work.

## From a client call to server execution

The server discovers scan classes from built-ins and installed plugin entry points. It
publishes their names, signatures, and input metadata. The client uses that information to
build the `scans` interface and validate calls; the server validates and assembles requests
again before execution.

The assembler injects resources such as the device manager, connector, instruction handler,
request inputs, and scan ID. These belong to the running server. A custom constructor
accepts its experimental inputs and forwards the injected arguments to `super().__init__`.
Submitting a scan therefore differs from constructing a class locally: the request is
scheduled, associated with a queue, and executed with server-managed resources.

## Constructor setup and runtime work

The constructor stores inputs, initializes recovery state, and configures metadata. Runtime
device RPC is prohibited during construction: the assembler raises an error if it occurs.
Moves, reads, detector preparation, and acquisition belong in lifecycle hooks.

The server can construct requests before they execute. Consequently, relative coordinates
must be resolved from motor positions during preparation, rather than when the client
submits the scan or when the constructor stores its offsets.

## The normal sequence

The direct worker calls these hooks in order:

```text
prepare_scan → open_scan → stage → pre_scan → scan_core
             → post_scan → unstage → close_scan
```

`prepare_scan` establishes the trajectory and scan metadata. `open_scan` publishes the
opening state so downstream services know what measurement to expect. `stage` configures
devices for the run; `pre_scan` performs preparation immediately before acquisition.

`scan_core` owns the experimental sequence. `post_scan` completes devices and performs
normal recovery, such as returning a relative scan to its starting positions. `unstage`
releases device setup. `close_scan` publishes the final scan state after outstanding work
has been accounted for.

The worker does not independently call `at_each_point`. A scan's own loop or a component
such as `step_scan` calls it. This allows different procedures to define what a point means:
a position in a trajectory, a timed acquisition, or a repeated visit to the same position.

## Positions, points, and readouts

For a step scan with `N` visits and `M` motors, the trajectory has shape `(N, M)`. A row is
one combined motor position. Repeated visits remain separate rows: the alternating-position
example has six points for three A/B pairs, not two points because only two locations differ.

The scan prepares absolute target positions, checks limits, and publishes `positions`,
`num_points`, and the expected `num_monitored_readouts` before opening. A burst can produce
multiple trigger/read cycles per visit, so the expected readout count can differ from the
position count. Detector frames are another separate quantity.

Downstream progress reporting, data bundling, and file writing depend on this metadata.
Declaring the correct count does not perform the acquisition; the loop must actually issue
the intended reads. On normal close, the actions layer updates the monitored-readout count
to the number it requested during execution.

## Actions, components, and status objects

Actions are individual runtime operations, such as setting a device or requesting a read.
Components combine actions into reusable sequences. For example, `step_scan_at_each_point`
moves motors, waits for them, and performs a trigger/read cycle. The scan class retains
ownership of the experiment's opening, closing, counts, and recovery.

Operations that support `wait=False` return a `ScanStatus`. The status represents the
outstanding operation; it is distinct from the client's `ScanReport`, which represents a
submitted request. A status can also contain sub-statuses for several devices.

This permits independent preparation to overlap. A scan can start a baseline read, perform
other setup, then wait for that status before closing. Dependencies must still be respected:
acquisition cannot assume a move or device preparation has finished just because it was
requested. Waiting checks for instruction failures as well as completion. Merely polling
`.done` is not a substitute for checking failure before using the operation's result.

The closing action checks for unchecked or unfinished statuses and can warn or wait for
remaining work. Explicit waits at the appropriate dependency boundary make the intended
sequence clear and prevent accidental dependence on closing-time cleanup.

## Failure and interruption

An exception interrupts the normal sequence. The remaining completion, unstaging, and
closing hooks are not automatically executed in that sequence. The worker normally invokes
`on_exception`, when exception cleanup is enabled, and reports the failed or interrupted
state. Halt disables that hook; worker shutdown can also bypass it.

Cleanup must therefore tolerate failure during preparation, staging, acquisition, or
completion. Starting positions may not have been captured, staging may have completed on
only some devices, and a temporary setting may have changed before a later operation failed.
A device error can also make the recovery operation fail.

The alternating-position example attempts a return when the scan is relative and its
starting position is known. It still attempts unstaging if that return fails. A more complex
experiment must additionally track and restore its own settings and complete or stop any acquisition it started. Copying the normal completion
sequence into every exception path is insufficient when setup is only partly complete.

Interruption is cooperative: the worker checks between lifecycle hooks, and the actions
layer checks when operations are issued. A long custom calculation or loop that does not
reach those checks can delay a response. Pausing a request does not guarantee that a physical
device stops immediately. Device stop and scan termination are different operations.

!!! info "What to remember"
    Keep constructors free of runtime device operations. Prepare positions and counts before
    opening the scan, make dependencies between status objects explicit, and own recovery
    from partial work. The worker runs the lifecycle; the scan defines its acquisition loop.

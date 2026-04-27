---
related:
  - title: Introduction to Scans
    url: learn/scans/introduction.md
  - title: Scan Lifecycle
    url: learn/scans/lifecycle.md
  - title: Scan Actions
    url: learn/scans/scan-actions.md
  - title: Scan Components
    url: learn/scans/scan-components.md
  - title: Scan Info
    url: learn/scans/scan-info.md
  - title: ScanArgument
    url: learn/scans/scanargument.md
  - title: Scan Definition Info
    url: learn/scans/scan-definition-info.md
---

# Learn by Example

This page walks through a small BEC scan implementation and points out where the shared scan
shape becomes scan-specific.

The example used here is `acquire`. It is much shorter than a motor-driven scan, which makes the
fixed lifecycle easier to see before moving on to more complex scan types.

## Why This Example

`acquire` is a good first example because it shows the full scan lifecycle without adding motor
trajectory logic on top.

It still demonstrates the main parts of a real scan:

- a compact `__init__` with `ScanArgument` metadata
- `gui_config` for graphical clients
- a small but meaningful `prepare_scan`
- a short `scan_core`
- explicit cleanup in `post_scan` and `close_scan`

## The Class Definition and Inputs

The first part of the class tells BEC what kind of scan this is, how GUIs should present it, and
what inputs it accepts.

```py
from __future__ import annotations

from typing import Annotated

from bec_lib.scan_args import ScanArgument, Units
from bec_server.scan_server.scans import ScanBase, ScanType
from bec_server.scan_server.scans.scan_modifier import scan_hook


class Acquire(ScanBase):
    scan_type = ScanType.SOFTWARE_TRIGGERED  # (1)!
    scan_name = "acquire"  # (2)!

    gui_config = {  # (3)!
        "Acquisition Parameters": [
            "exp_time",
            "frames_per_trigger",
            "settling_time",
            "readout_time",
        ],
    }

    def __init__(
        self,
        exp_time: Annotated[
            float, ScanArgument(display_name="Exposure Time", units=Units.s, ge=0)
        ] = 0,  # (4)!
        frames_per_trigger: Annotated[
            int, ScanArgument(display_name="Frames per Trigger", ge=1)
        ] = 1,
        settling_time: Annotated[
            float, ScanArgument(display_name="Settling Time", units=Units.s, ge=0)
        ] = 0,
        readout_time: Annotated[
            float, ScanArgument(display_name="Readout Time", units=Units.s, ge=0)
        ] = 0,
        **kwargs, # (5)!
    ):
        super().__init__(**kwargs) # (6)!
        self.exp_time = exp_time
        self.frames_per_trigger = frames_per_trigger
        self.settling_time = settling_time
        self.readout_time = readout_time

        self.update_scan_info(  # (7)!
            exp_time=exp_time,
            frames_per_trigger=frames_per_trigger,
            settling_time=settling_time,
            readout_time=readout_time,
        )
```

1. `scan_type` tells BEC that this scan's main logic is software-triggered.
2. `scan_name` is the name published by the scan server and exposed to the client. It must be unique across all scans and a valid Python identifier. Once loaded, the scan is available as `scans.<scan_name>(...)` on the client.
3. The `gui_config` dictionary groups and enables input fields in graphical clients. In this case, all inputs are grouped under "Acquisition Parameters". Keys that don't appear in `gui_config` are still valid inputs from the command-line but they won't be shown in GUIs.
4. `ScanArgument(...)` carries labels, units, and validation bounds. In this case, the `exp_time` argument must be a float and the `ScanArgument` further specifies that it should be displayed as "Exposure Time" with units of seconds and the value must be greater than or equal to (ge) 0. 
5. `**kwargs` is needed to be able to make the scan connect to BEC's scan lifecycle and forward additional metadata to `ScanBase`. 
6. The `super().__init__(**kwargs)` call is required to properly initialize the scan base class and give the scan access to devices, actions, components, and the scan info object. It usually doesn't need to receive any additional arguments, only `**kwargs`. 
7. Use `update_scan_info(...)` to update any standard scan metadata field that depends on the scan inputs. This is important as it is the scan info object that is used for broadcasting information about the scan to clients, devices, and the file writer. In this case, the acquisition parameters are added to the scan info for later reference.


## `prepare_scan`: Small But Still Important

Even a short scan usually uses `prepare_scan` to finalize metadata and publish progress reporting.

```py
@scan_hook
def prepare_scan(self):
    self.update_scan_info(  # (1)!
        num_points=1,
        num_monitored_readouts=self.frames_per_trigger,
    )

    self.actions.add_scan_report_instruction_scan_progress(  # (2)!
        points=self.scan_info.num_monitored_readouts,
        show_table=False,
    )

    self._baseline_readout_status = self.actions.read_baseline_devices(wait=False)  # (3)!
```

1. The scan declares its final runtime shape: one acquisition step with a known readout count.
2. The progress instruction lets clients render consistent progress even for a simple scan.
3. Baseline readout starts early and can finish in parallel with the rest of scan setup.

This is useful to compare with a motor scan: the hook is still important, but it is shorter because
there are no positions to generate, shift, or limit-check.

## The Shared Lifecycle Around The Acquisition

After `prepare_scan`, the scan looks much like any other BEC scan again.

```py
@scan_hook
def open_scan(self):
    self.actions.open_scan()

@scan_hook
def stage(self):
    self.actions.stage_all_devices()

@scan_hook
def pre_scan(self):
    self.actions.pre_scan_all_devices()  # (1)!

@scan_hook
def scan_core(self):
    for _ in range(self.frames_per_trigger):  # (2)!
        self.components.trigger_and_read()  # (3)!
```

1. `pre_scan_all_devices()` runs the usual last-moment device preparation.
2. `frames_per_trigger` still affects the acquisition loop, even though nothing is moving.
3. The scan reuses the shared trigger-and-read helper instead of implementing detector logic itself.

This is the key lesson of the `acquire` example: even the shortest useful scan still fits the same
hook order and still delegates repetitive device work to shared helpers.

## Cleanup

The final hooks show how the scan finishes cleanly.

```py
@scan_hook
def post_scan(self):
    self.actions.complete_all_devices()  # (1)!

@scan_hook
def unstage(self):
    self.actions.unstage_all_devices()

@scan_hook
def close_scan(self):
    if self._baseline_readout_status is not None:  # (2)!
        self._baseline_readout_status.wait()
    self.actions.close_scan()
    self.actions.check_for_unchecked_statuses()  # (3)!
```

1. `post_scan` lets devices finish their acquisition-side work before teardown.
2. `close_scan` waits for the asynchronous baseline readout to finish.
3. The final status check helps catch unfinished device operations.

This cleanup path is shorter than in a relative motor scan, because there are no motors to move
back and no point-pattern state to unwind.

## What This Example Shows

The `acquire` scan is a compact example of the shared scan shape:

- the hook order is unchanged
- `prepare_scan` is still where final scan metadata is prepared
- `scan_core` stays short because it composes shared helpers
- scan-definition metadata such as `gui_config` and `ScanArgument` lives alongside the code
- even a simple scan still needs explicit cleanup

## Next Step

After this example, the next useful topic is [scan info](scan-info.md).

That page explains the shared metadata object this scan keeps updating through
`update_scan_info(...)`.

After `scan info`, continue with [scan actions](scan-actions.md), and then move on to
[scan components](scan-components.md) for `components`.

## What to Remember

!!! info "What to remember"
    - This page uses `acquire` because it shows the shared scan shape with minimal extra logic.
    - The scan-specific parts are mostly in `__init__`, `prepare_scan`, and the short acquisition loop in `scan_core`.
    - The repetitive execution path is delegated to shared helpers in `actions` and `components`.
    - More complex scans keep the same lifecycle, but add motion planning and richer cleanup on top.

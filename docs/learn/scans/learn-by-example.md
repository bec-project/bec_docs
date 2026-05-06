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
  - title: GUI Config
    url: learn/scans/gui-config.md
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

- a compact `__init__` with shared default argument types
- `gui_config` for graphical clients
- a small but meaningful `prepare_scan`
- a short `scan_core`
- explicit cleanup in `post_scan` and `close_scan`

## The Class Definition and Inputs

The first part of the class tells BEC what kind of scan this is, how GUIs should present it, and
what inputs it accepts.

```py
from __future__ import annotations

import numpy as np

from bec_lib.scan_args import DefaultArgType
from bec_server.scan_server.scans.scan_base import ScanBase, ScanType
from bec_server.scan_server.scans.scan_modifier import scan_hook


class Acquire(ScanBase):
    scan_type = ScanType.SOFTWARE_TRIGGERED  # (1)!
    scan_name = "acquire"  # (2)!

    gui_config = {  # (3)!
        "Scan Parameters": [
            "exp_time",
            "frames_per_trigger",
            "settling_time",
            "settling_time_after_trigger",
            "readout_time",
            "burst_at_each_point",
        ]
    }

    def __init__(
        self,  # (4)!
        exp_time: DefaultArgType.ExposureTime = 0,
        frames_per_trigger: DefaultArgType.FramesPerTrigger = 1,
        settling_time: DefaultArgType.SettlingTime = 0,
        settling_time_after_trigger: DefaultArgType.SettlingTimeAfterTrigger = 0,
        readout_time: DefaultArgType.ReadoutTime = 0,
        burst_at_each_point: DefaultArgType.BurstAtEachPoint = 1,
        **kwargs, # (5)!
    ):
        super().__init__(**kwargs) # (6)!
        self.motors = []
        self.exp_time = exp_time
        self.frames_per_trigger = frames_per_trigger
        self.settling_time = settling_time
        self.settling_time_after_trigger = settling_time_after_trigger
        self.readout_time = readout_time
        self.burst_at_each_point = burst_at_each_point

        self.update_scan_info(  # (7)!
            exp_time=exp_time,
            frames_per_trigger=frames_per_trigger,
            settling_time=settling_time,
            settling_time_after_trigger=settling_time_after_trigger,
            readout_time=readout_time,
            burst_at_each_point=burst_at_each_point,
        )
```

1. `scan_type` tells BEC that this scan's main logic is software-triggered.
2. `scan_name` is the name published by the scan server and exposed to the client. It must be unique across all scans and a valid Python identifier. Once loaded, the scan is available as `scans.<scan_name>(...)` on the client.
3. The `gui_config` dictionary groups and enables input fields in graphical clients. In the current implementation, `acquire` groups its inputs under "Scan Parameters" and includes timing plus burst settings. Keys that don't appear in `gui_config` are still valid inputs from the command-line but they won't be shown in GUIs.
4. The current scan uses shared `DefaultArgType` aliases instead of spelling out `Annotated[..., ScanArgument(...)]` for each input. That keeps the signature compact while still reusing the standard scan argument definitions for exposure time, settling, readout, and burst settings.
5. `**kwargs` is needed to be able to make the scan connect to BEC's scan lifecycle and forward additional metadata to `ScanBase`. 
6. The `super().__init__(**kwargs)` call is required to properly initialize the scan base class and give the scan access to devices, actions, components, and the scan info object. In this scan, `self.motors = []` also makes it explicit that `acquire` does not move any motors.
7. Use `update_scan_info(...)` to update any standard scan metadata field that depends on the scan inputs. This is important as it is the scan info object that is used for broadcasting information about the scan to clients, devices, and the file writer. In this case, the acquisition parameters, including post-trigger settling and burst count, are added to the scan info for later reference.


## `prepare_scan`

For `acquire`, we only measure at the current position, so `prepare_scan` does not need to generate a list of positions or check motor limits. We update the scan info container with the acquisition parameters: no positions, one logical point and depending on the `burst_at_each_point` setting, one or more monitored readouts.

```py

@scan_hook
def prepare_scan(self):
    self.update_scan_info(  
        positions=np.array([]),
        num_points=1,
        num_monitored_readouts=self.burst_at_each_point,
    )

    self.actions.add_scan_report_instruction_scan_progress(  
        points=self.scan_info.num_monitored_readouts,
        show_table=False,
    )

    self._baseline_readout_status = self.actions.read_baseline_devices(wait=False)  
```

Once the scan info is updated with the correct parameters, we can send the information about the upcoming acquisitions to any clients that may want to report on the scan progress. In this case, we use `add_scan_report_instruction_scan_progress` to suggest that clients report progress based on the number of monitored readouts, which is the most relevant measure of progress for this scan. The `show_table=False` argument indicates that clients should not show a progress table with individual point statuses, just a progress bar.

Finally, `prepare_scan` triggers a readout of all devices of readout priority `baseline`. This is done asynchronously by passing `wait=False`, so the scan can proceed to `open_scan` while the baseline readout is still in progress. The resulting status object is stored in `self._baseline_readout_status` so that we can check on it later (in `close_scan`) and make sure the baseline readout has finished before closing the scan.

## `open_scan`

After `prepare_scan`, `acquire` opens the scan in the standard way.

```py
@scan_hook
def open_scan(self):
    self.actions.open_scan()
```

Opening the scan will emit a new scan status message with all the metadata we prepared in scan info, so it is important to make sure the scan info is up to date before this step. 

Any device that implements runtime logic based on the scan info metadata will now receive the updated scan info.

## `stage`

Stageing tells devices to get ready for the upcoming acquisition.

```py
@scan_hook
def stage(self):
    self.actions.stage_all_devices()
```

If a device implements custom `on_stage` logic, it will be triggered by `stage_all_devices()`. For example, a detector may configure itself for acquisition during staging, and then be ready to receive trigger signals once the scan starts.

## `pre_scan`

`pre_scan` gives devices one last chance to prepare before the acquisition starts.

```py
@scan_hook
def pre_scan(self):
    self.actions.pre_scan_all_devices()
```

In `acquire`, we don't have any time-critical motors to prepare, so we can just delegate to the shared `pre_scan_all_devices` helper. In a motor-driven scan, this is where we would typically wait for the motors to reach their starting positions before triggering any `pre_scan` logic.

In general, `pre_scan` is meant for any preparation that needs to happen after the scan is open but before the first acquisition starts. It is a good place for time-critical preparation, e.g. devices that have a very short window between being armed and needing to receive a first trigger.

## `scan_core`

`scan_core` contains the main acquisition loop.

```py
@scan_hook
def scan_core(self):
    for _ in range(self.burst_at_each_point): 
        self.at_each_point() 
```

As we are not moving between acquisitions in this scan, the core loop is merely a burst loop that calls `at_each_point` for each acquisition. The `at_each_point` hook is a common extension point for scans that have a repetitive acquisition step, such as line scans, grid scans, or in this case, a burst of acquisitions at each point. By putting the trigger-and-read logic in `at_each_point`, we can keep the main loop in `scan_core` clean and focused on the overall structure of the scan, while still allowing for complex per-point logic when needed.

## `at_each_point`

The actual trigger-and-read work happens in a separate per-point hook.

```py
@scan_hook
def at_each_point(self):
    self.components.trigger_and_read() 
```

The `trigger_and_read` component is a shared helper that triggers all devices that are set to `softwareTrigger=True` before starting a readout of all devices of readout priority `monitored`. 

## `post_scan`

Once acquisition is done, `post_scan` lets devices finish their scan-side work.

```py
@scan_hook
def post_scan(self):
    self.actions.complete_all_devices() 
```

The `complete_all_devices` helper calls the `complete` method on all devices that implement it. The `complete` method on a device is meant for any logic that needs to happen after the last acquisition has been triggered but before the scan is closed. For example, a detector may need to wait until all frames have been read out and processed before it can report that it is done with the scan.

## `unstage`

After that, the scan unstages devices in the standard way.

```py
@scan_hook
def unstage(self):
    self.actions.unstage_all_devices()
```

## `close_scan`

The closing hook waits for the baseline readout to finish before emitting the final scan status.

```py
@scan_hook
def close_scan(self):
    if self._baseline_readout_status is not None:
        self._baseline_readout_status.wait()
    self.actions.close_scan()
    self.actions.check_for_unchecked_statuses()
```

An additional check is performed to make sure that no status objects were left unchecked at the end of the scan. If any status was left unchecked, a warning will be logged.

## `on_exception`

If any exception is raised during the scan lifecycle, the `on_exception` hook gives the scan a chance to clean up.

```py
@scan_hook
def on_exception(self, exception: Exception):
    pass
```

In this case, there is no special cleanup needed.


## What This Example Shows

The `acquire` scan is a compact example of the shared scan shape:

- the same lifecycle from [Scan Lifecycle](lifecycle.md){data-preview} appears here unchanged
- each hook stays small and focused, even though the page now looks at them one by one
- `prepare_scan` and `scan_core` are the most informative hooks for understanding what this scan actually does
- `at_each_point` shows how per-acquisition work can be factored out of the main loop
- the rest of the hooks mostly delegate to shared helpers in `actions` and `components`
- scan-definition metadata such as `gui_config` and the shared default argument types lives alongside the executable scan code

## Next Step

After this example, the next useful topic is [scan info](scan-info.md){data-preview}, because `acquire`
updates `scan_info` in `__init__` and `prepare_scan` and then relies on that shared runtime
metadata for progress reporting and scan status messages.

After `scan info`, continue with [scan actions](scan-actions.md){data-preview} to see the building blocks used in scans for common operations. Afterwards, [scan components](scan-components.md){data-preview} show how to combine scan actions into reusable scan building blocks.

## What to Remember

!!! info "What to remember"
    - This page uses `acquire` because it shows the full lifecycle with almost no motion-planning noise.
    - In `acquire`, most of the scan-specific behavior lives in `__init__`, `prepare_scan`, `scan_core`, and `at_each_point`.
    - More complex scans keep the same lifecycle, but make hooks such as `prepare_scan`, `scan_core`, `post_scan`, and `on_exception` richer.

---
related:
  - title: Scan Actions
    url: learn/scans/scan-actions.md
  - title: Position Generators
    url: learn/scans/position-generators.md
  - title: ScanArgument
    url: learn/scans/scanargument.md
  - title: Scan Info
    url: learn/scans/scan-info.md
---

# Scan Components

`self.components` contains reusable scan logic for common scan patterns.

Where `actions` gives a scan high-level operations such as staging, reading, or publishing progress,
`components` builds on top of those operations to make frequently used scan patterns easier to
reuse.

## Why Scan Components Matter

Many scans need the same kinds of logic:

- loop over prepared positions
- move devices and wait for motion to finish
- trigger and read at each point
- capture starting positions for relative scans
- check limits before motion begins

Without shared components, each scan would need to reimplement that behavior for itself.

`components` exists so scans can reuse those patterns directly and stay focused on what is actually
scan-specific.

## `actions` Versus `components`

The difference is mostly one of level.

- `actions` provides scan-facing operations such as `stage_all_devices()`, `read_baseline_devices()`, or `set(...)`
- `components` combines those operations into reusable scan patterns such as step scans, trigger-and-read sequences, or move-and-wait flows

That is why components are best understood as reusable building blocks on top of `actions`.

A concrete scan will often use both:

- `actions` for lifecycle work and reporting
- `components` for the repeated motion and acquisition pattern inside `prepare_scan` or `scan_core`

## Common `ScanComponents` Helpers

Some of the most commonly used helpers are listed below.

<!-- The table is in html as the columns would otherwise wrap. There seems to be no internal way to control column width in markdown -->
<table>
  <colgroup>
    <col style="width: 30%;">
    <col style="width: 50%;">
    <col style="width: 20%;">
  </colgroup>
  <thead>
    <tr>
      <th>Helper</th>
      <th>Role</th>
      <th>Typical hook</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap;"><code>step_scan(...)</code></td>
      <td>Runs the standard repeated move/trigger/read pattern for prepared point lists.</td>
      <td><code>scan_core</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>step_scan_at_each_point(...)</code></td>
      <td>Handles the usual per-point logic used inside a step scan.</td>
      <td><code>at_each_point</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>trigger_and_read()</code></td>
      <td>Runs the common trigger/read sequence without rewriting the device coordination each time.</td>
      <td><code>scan_core</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>move_and_wait(...)</code></td>
      <td>Moves devices and waits for motion to complete before continuing.</td>
      <td><code>prepare_scan</code> or <code>post_scan</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>get_start_positions(...)</code></td>
      <td>Captures the starting device positions, for example for relative scans.</td>
      <td><code>prepare_scan</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>check_limits(...)</code></td>
      <td>Checks planned motion against device limits before the scan starts moving hardware.</td>
      <td><code>prepare_scan</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>optimize_trajectory(...)</code></td>
      <td>Reorders prepared positions to reduce unnecessary motion for scans that benefit from path optimization.</td>
      <td><code>prepare_scan</code></td>
    </tr>
  </tbody>
</table>

The important point is not to memorize every helper name. The important point is that common scan
behavior is reused instead of being rewritten in every scan class.

## A Typical Example

In a step scan, the scan-specific code often looks something like this:

1. prepare the positions
2. check limits
3. update `scan_info`
4. let `components.step_scan(...)` handle the repeated move/trigger/read sequence

That is a cleaner pattern than manually open-coding every move, wait, trigger, and read inside the
scan class.

This is also why components help readability: once you know the shared helpers, you can see more
quickly which parts of a scan are generic and which parts are genuinely specific to that scan.

## Two Common Execution Styles

The same framework supports both software-triggered and hardware-triggered scans.

### Software-triggered scans

Scans such as `acquire`, `time_scan`, `line_scan`, and `grid_scan` usually follow a simple pattern:

1. move to the next position if needed
2. wait for motion to finish
3. apply settling time
4. trigger devices
5. read monitored devices

In many cases this logic is handled through `components.step_scan(...)` and
`components.trigger_and_read()`.

### Hardware-triggered or continuous scans

Scans such as `cont_line_fly_scan` or `monitor_scan` use the same lifecycle, but their
`scan_core` hook looks different:

- the motor may move continuously between only a start and stop point
- per-point work may be driven by readback updates or by repeated trigger/read cycles while motion is still active
- progress is often reported through readback instructions rather than a fixed point table

So the framework stays the same, but the reused execution pattern changes to suit the scan style.

## Next Step

After `components`, continue with [position generators](position-generators.md).

That page covers the reusable helpers used to build point lists and trajectories before the scan
execution pattern begins.

## What To Remember

!!! info "What to remember"
    - `components` contains reusable scan patterns built on top of `actions`.
    - Components help scans reuse common motion and acquisition logic more elegantly.
    - Components are most useful when a scan needs a familiar execution pattern without reimplementing it from scratch.

---
related:
  - title: Introduction to Scans
    url: learn/scans/introduction.md
  - title: Learn by Example
    url: learn/scans/learn-by-example.md
  - title: Scan Info
    url: learn/scans/scan-info.md
---

# Scan Lifecycle

BEC uses one shared scan structure across the system. Concrete scans such as `line_scan`,
`grid_scan`, `time_scan`, or `monitor_scan` all follow that same structure, even if they move
different devices or collect data in different ways.

Scans implement these hooks as normal methods and the scan server calls those hooks in a fixed order, which gives every BEC scan its recognizable shape.


## The Fixed Hook Order

Scans are structured around the following hooks:

<!-- The table is in html as the columns would otherwise wrap. There seems to be no internal way to control column width in markdown -->
<table>
  <colgroup>
    <col style="width: 24%;">
    <col style="width: 76%;">
  </colgroup>
  <thead>
    <tr>
      <th>Hook</th>
      <th>Role</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap;"><code>prepare_scan</code></td>
      <td>Prepare the scan for the upcoming acquisition.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>open_scan</code></td>
      <td>Open the scan and emit a new scan status message with all relevant metadata.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>stage</code></td>
      <td>Stage the devices for the upcoming acquisition.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>pre_scan</code></td>
      <td>Run any pre-scan logic, such as preparing time-critical devices.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>scan_core</code></td>
      <td>Run the core logic of the scan; trigger readouts if needed and optionally call <code>at_each_point()</code> for per-point logic.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>post_scan</code></td>
      <td>Run any post-scan logic, such as moving devices back to their original position.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>unstage</code></td>
      <td>Unstage the devices.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>close_scan</code></td>
      <td>Close the scan and emit a final scan status message with all relevant metadata.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>on_exception</code></td>
      <td>If an exception is raised during any earlier step, run cleanup logic here.</td>
    </tr>
  </tbody>
</table>


???+ Example "Example hook order in `fermat_spiral`"
    As an example, the `fermat_spiral` scan implements the lifecycle hooks in the following way:

    - `prepare_scan`: Build the Fermat position list, optionally shift it by the current motor positions for relative scans, check motor limits, update `scan_info`, schedule scan-progress reporting, trigger a baseline readout, and start moving to the first point.
    - `open_scan`: Open a new scan by calling `self.actions.open_scan()` after the metadata is ready.
    - `stage`: Stage all participating devices through `self.actions.stage_all_devices()`.
    - `pre_scan`: Wait until the motors have reached the first point, then run `pre_scan` on all devices.
    - `scan_core`: Run a step scan over the prepared spiral positions and call `at_each_point` so each point performs the move/trigger/readout sequence.
    - `post_scan`: Ask all devices to complete their work and, for relative scans, move the motors back to their original positions.
    - `unstage`: Unstage all devices through `self.actions.unstage_all_devices()`.
    - `close_scan`: Wait for the asynchronous baseline readout to finish, publish the closing scan status, and check that no statuses were left unchecked.
    - `on_exception`: If the scan was relative, move the motors back to their recorded starting positions.


## What to Remember

!!! info "What to remember"
    - Every BEC scan follows the same lifecycle, even when the acquisition details differ.
    - The hook order is fixed.
    - The lifecycle stays recognizable even when the details of a scan change.

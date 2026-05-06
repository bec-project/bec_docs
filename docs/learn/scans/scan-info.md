---
related:
  - title: Learn by Example
    url: learn/scans/learn-by-example.md
  - title: Scan Actions
    url: learn/scans/scan-actions.md
  - title: Scan Components
    url: learn/scans/scan-components.md
  - title: Introduction to Scans
    url: learn/scans/introduction.md
---

# Scan Info

A scan must keep track of its runtime metadata and parameters in a structured way. In BEC, that is the role of the `ScanInfo` model. Every scan has an instance of `ScanInfo` that is created by `ScanBase` when the scan object is initialized and then updated by the concrete scan during its lifecycle. It is accessible as `self.scan_info` from any scan hook or method, although it is most commonly updated through a helper method called `update_scan_info(...)` that can update both known top-level fields and extra scan-specific parameters in one call. 

## What `scan_info` Is For

Without one shared runtime model, each part of BEC would need to reconstruct the scan from a mix of
request arguments, device instructions, and status messages.

`scan_info` solves that by keeping the scan description in one structured object, including:

- what scan is running
- how many points or monitored readouts it expects
- which timing parameters apply
- which devices should be reported
- which request inputs the user originally sent
- which extra scan-specific parameters should travel with the scan

The `ScanInfo` model is the single source of truth for the scan's runtime metadata and is the main content for published scan status messages. Any device or client that needs to know about the scan relies on it for the most accurate and up-to-date description.

## The `ScanInfo` Model

The current `ScanInfo` model contains the following fields.

<!-- The table is in html as the columns would otherwise wrap. There seems to be no internal way to control column width in markdown -->
<table>
  <colgroup>
    <col style="width: 24%;">
    <col style="width: 50%;">
    <col style="width: 26%;">
  </colgroup>
  <thead>
    <tr>
      <th>Field</th>
      <th>Role</th>
      <th>Typically set by</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap;"><code>scan_name</code></td>
      <td>Name of the scan class published to the client, for example <code>acquire</code>.</td>
      <td><code>ScanBase</code> from the class attribute</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>scan_id</code></td>
      <td>Unique runtime identifier for this scan instance.</td>
      <td>Queue and worker setup</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>scan_type</code></td>
      <td>Internal scan type, currently <code>software_triggered</code> or <code>hardware_triggered</code>.</td>
      <td><code>ScanBase</code> from the class attribute</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>scan_number</code></td>
      <td>Assigned scan number for the run, if available.</td>
      <td>Queue and runtime bookkeeping</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>dataset_number</code></td>
      <td>Assigned dataset number for the run, if available.</td>
      <td>Queue and runtime bookkeeping</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>num_points</code></td>
      <td>Number of logical scan points.</td>
      <td>Usually <code>prepare_scan</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>positions</code></td>
      <td>Prepared position array for scans that precompute positions.</td>
      <td>Usually <code>prepare_scan</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>exp_time</code></td>
      <td>Exposure time for the scan.</td>
      <td><code>__init__</code> or <code>update_scan_info(...)</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>frames_per_trigger</code></td>
      <td>Number of frames collected per trigger.</td>
      <td><code>__init__</code> or <code>update_scan_info(...)</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>settling_time</code></td>
      <td>Settling delay before a software trigger.</td>
      <td><code>__init__</code> or <code>update_scan_info(...)</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>settling_time_after_trigger</code></td>
      <td>Settling delay after a software trigger.</td>
      <td><code>__init__</code> or <code>update_scan_info(...)</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>readout_time</code></td>
      <td>Readout delay after triggering.</td>
      <td><code>__init__</code> or <code>update_scan_info(...)</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>burst_at_each_point</code></td>
      <td>How many bursts are collected at each point.</td>
      <td><code>__init__</code> or <code>update_scan_info(...)</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>relative</code></td>
      <td>Whether prepared positions are interpreted relative to the current device state.</td>
      <td><code>__init__</code> or <code>update_scan_info(...)</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>run_on_exception_hook</code></td>
      <td>Whether the scan should run its <code>on_exception</code> cleanup hook on interruption.</td>
      <td>Base initialization or later update</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>request_inputs</code></td>
      <td>Structured copy of the original request inputs sent by the client.</td>
      <td><code>ScanBase</code> initialization</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>readout_priority_modification</code></td>
      <td>Requested overrides to device readout priority during the scan.</td>
      <td>Usually helper calls in <code>actions</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>scan_report_instructions</code></td>
      <td>UI/report instructions such as progress widgets or readback displays.</td>
      <td>Usually helper calls in <code>actions</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>scan_report_devices</code></td>
      <td>Devices highlighted in scan reports. Device objects are stored by name.</td>
      <td>Usually <code>update_scan_info(...)</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>monitor_sync</code></td>
      <td>Monitor synchronization mode for fly scans. This field is marked for removal.</td>
      <td>Scan-specific logic when needed</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>additional_scan_parameters</code></td>
      <td>Extra scan-specific parameters that do not have dedicated top-level fields.</td>
      <td>Unknown keys passed to <code>update_scan_info(...)</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>user_metadata</code></td>
      <td>User-provided metadata attached to the request.</td>
      <td>Request setup</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>system_config</code></td>
      <td>System-side configuration relevant to the scan, such as file-writing settings.</td>
      <td>Request setup</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>scan_queue</code></td>
      <td>Name of the queue this scan belongs to.</td>
      <td>Request setup</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>metadata</code></td>
      <td>Additional runtime metadata associated with the scan request.</td>
      <td>Request setup and runtime bookkeeping</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>num_monitored_readouts</code></td>
      <td>Total number of monitored readouts expected for the run.</td>
      <td>Usually <code>prepare_scan</code></td>
    </tr>
  </tbody>
</table>


## Next Step

After `scan_info`, continue with [scan actions](scan-actions.md){data-preview}.

That page covers the high-level scan operations used to publish scan state and coordinate device
work. After that, move on to [scan components](scan-components.md){data-preview} for the reusable scan patterns
built on top of those operations.

## What To Remember

!!! info "What to remember"
    - `scan_info` is the shared runtime metadata model for a scan.
    - `ScanBase` creates it, and concrete scans usually finish populating it during `prepare_scan`.
    - Known updates go to named `ScanInfo` fields; unknown updates go to `additional_scan_parameters`.
    - Published scan status messages are derived from `scan_info`.

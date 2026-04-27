---
related:
  - title: Scan Info
    url: learn/scans/scan-info.md
  - title: Scan Components
    url: learn/scans/scan-components.md
  - title: Learn by Example
    url: learn/scans/learn-by-example.md
---

# Scan Actions

`self.actions` is the high-level interface a scan uses to interact with devices and publish
scan-related state.

In practice, `self.actions` is an instance of `ScanActions`. These methods
wrap common device-server instructions, track their statuses, and update scan-report state so that
concrete scans do not need to reimplement the same coordination logic again and again.

## What `actions` Is For

`actions` is typically used for three kinds of work:

- lifecycle orchestration such as opening, staging, and closing a scan
- device operations such as moving, triggering, reading, and completing
- reporting and metadata updates such as progress instructions and readout-priority changes

The important design point is that `actions` stays scan-facing and task-oriented. A scan usually
asks for a high-level operation like `stage_all_devices()` or `read_baseline_devices()` rather than
building instruction messages manually.

## Common `ScanActions` Methods

The current public `ScanActions` API includes the following methods most relevant to scan authors.

<!-- The table is in html as the columns would otherwise wrap. There seems to be no internal way to control column width in markdown -->
<table>
  <colgroup>
    <col style="width: 28%;">
    <col style="width: 48%;">
    <col style="width: 24%;">
  </colgroup>
  <thead>
    <tr>
      <th>Method</th>
      <th>Role</th>
      <th>Typical hook</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap;"><code>open_scan()</code></td>
      <td>Publishes the opening scan status message for the current scan.</td>
      <td><code>open_scan</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>stage_all_devices()</code></td>
      <td>Stages all enabled scan devices, with async devices handled separately for better throughput.</td>
      <td><code>stage</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>stage(...)</code></td>
      <td>Stages one device or a selected device list instead of the whole scan device set.</td>
      <td><code>stage</code> in custom cases</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>pre_scan_all_devices()</code></td>
      <td>Runs the pre-scan device step across all enabled devices.</td>
      <td><code>pre_scan</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>pre_scan(...)</code></td>
      <td>Runs the pre-scan device step only for selected devices.</td>
      <td><code>pre_scan</code> in custom cases</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>set(...)</code></td>
      <td>Sends coordinated set instructions to one or several devices.</td>
      <td><code>prepare_scan</code> or <code>scan_core</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>kickoff(...)</code></td>
      <td>Starts a kickoff-capable device with optional configuration parameters.</td>
      <td><code>scan_core</code> or flyer setup</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>complete(...)</code></td>
      <td>Completes one device explicitly.</td>
      <td><code>post_scan</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>complete_all_devices()</code></td>
      <td>Completes all enabled scan devices.</td>
      <td><code>post_scan</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>read_monitored_devices()</code></td>
      <td>Reads the current monitored-device group and advances the monitored readout counter.</td>
      <td><code>scan_core</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>read_manually(...)</code></td>
      <td>Performs an explicit read and returns the result to the scan, rather than relying on the usual monitored-read path.</td>
      <td>Special cases only</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>publish_manual_read(...)</code></td>
      <td>Publishes externally collected data as the next monitored readout.</td>
      <td>Special cases only</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>read_baseline_devices()</code></td>
      <td>Reads the baseline-device group, often around scan setup or teardown.</td>
      <td>Usually <code>prepare_scan</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>trigger_all_devices()</code></td>
      <td>Triggers all devices configured for software triggering in the scan.</td>
      <td><code>scan_core</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>unstage(...)</code></td>
      <td>Unstages one selected device.</td>
      <td><code>unstage</code> in custom cases</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>unstage_all_devices()</code></td>
      <td>Unstages all enabled scan devices.</td>
      <td><code>unstage</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>add_scan_report_instruction_scan_progress(...)</code></td>
      <td>Adds a scan-progress instruction so clients can render scan progress consistently.</td>
      <td>Usually <code>prepare_scan</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>add_scan_report_instruction_readback(...)</code></td>
      <td>Adds a live readback instruction for selected devices.</td>
      <td>Usually <code>prepare_scan</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>add_scan_report_instruction_device_progress(...)</code></td>
      <td>Adds a device-progress instruction for devices exposing progress signals.</td>
      <td>Usually <code>prepare_scan</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>set_device_readout_priority(...)</code></td>
      <td>Modifies which devices are treated as monitored, baseline, on-request, or async during the scan.</td>
      <td>Usually <code>__init__</code> or <code>prepare_scan</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>close_scan()</code></td>
      <td>Finalizes monitored-readout counts, checks cleanup state, and publishes the closing scan status.</td>
      <td><code>close_scan</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>check_for_unchecked_statuses()</code></td>
      <td>Warns about unfinished or unchecked status objects and waits on remaining work when needed.</td>
      <td><code>close_scan</code> or cleanup</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>add_device_with_required_response(...)</code></td>
      <td>Marks devices whose instructions must emit explicit response messages.</td>
      <td>Special cases only</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>rpc_call(...)</code></td>
      <td>Makes a low-level RPC call to a device-server method and returns the result.</td>
      <td>Advanced cases only</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>send_client_info(...)</code></td>
      <td>Sends an informational message to clients, for example for GUI status updates.</td>
      <td>Any hook when useful</td>
    </tr>
  </tbody>
</table>

## How `actions` Fits With `scan_info`

Many `actions` methods do more than send device instructions.

For example:

- `add_scan_report_instruction_*` updates `scan_info.scan_report_instructions`
- `set_device_readout_priority(...)` updates `scan_info.readout_priority_modification`
- `close_scan()` writes back the actual `num_monitored_readouts` before publishing the closing status

So `actions` is one of the main ways a concrete scan both performs work and keeps its shared runtime
description synchronized.

## When To Prefer `actions`

Prefer `actions` when you want to express an operation in scan terms:

- open or close the scan
- stage or unstage devices
- trigger or read the configured scan device groups
- publish scan progress or readback instructions
- adjust scan-local readout priorities

This keeps scan code short and consistent.

If you need reusable lower-level scan logic such as step-scan execution, motor limit checking, or
move-and-wait helpers, that belongs in `components`.

## Next Step

After `actions`, continue with [scan components](scan-components.md).

## What To Remember

!!! info "What to remember"
    - `actions` is the scan-facing helper for lifecycle operations, device instructions, and reporting updates.
    - Most concrete scans should prefer `actions` over building instruction messages manually.
    - Several `actions` methods also update `scan_info`, not just device state.

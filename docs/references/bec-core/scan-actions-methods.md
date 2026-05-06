---
related:
  - title: Scan Actions
    url: learn/scans/scan-actions.md
  - title: Scan Components
    url: learn/scans/scan-components.md
  - title: Scan Info
    url: learn/scans/scan-info.md
---

# ScanActions Methods

The following methods are most relevant to scan authors.

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

!!! tip
    This table is meant as a reference, not as something to memorize in one pass. For most readers,
    it is more useful to return here while reading or writing concrete scan implementations.

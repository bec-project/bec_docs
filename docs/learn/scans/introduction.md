---
related:
  - title: System architecture overview
    url: learn/system-architecture/overview/index.md
  - title: File writing
    url: learn/file-writer/introduction.md
  - title: Access BEC history
    url: how-to/scans/access-bec-history.md
---

# Scans in BEC

!!! Info "Overview"
    Scans are the core of BEC's functionality. They are the tools that move your devices, trigger readouts, and produce the data you analyze. In BEC, all scans follow a shared structure and report themselves in a consistent way, even when their motion logic differs.

BEC scans follow one shared model. Whether you run a simple acquisition, a line scan, a grid scan,
or a continuous scan, BEC handles them in the same overall way.


## The Main Idea

The most important idea in BEC scan execution is simple:

- all scans follow the same overall structure
- all scans are reported through the same backend model
- all scans are executed on the server
- all scans produce data that can be accessed in the same general way afterward
- the client learns the available scans from the scan server, including their current signatures and metadata

That is true even when the middle of the scan is very different.

For example, a line scan, a grid scan, and a continuous scan may move differently, but they still fit into one common scan framework.

## What Happens During A Scan

!!! Note "Dataflow during a scan"
    A general overview of the dataflow in BEC can be found in the [system architecture overview](../../learn/system-architecture/overview/data-flow.md){ data-preview }.

At a high level, a scan in BEC follows this path:

1. The scan server publishes the available scan classes together with their serialized signatures, grouped inputs, and GUI metadata.
2. The client exposes those scans dynamically, so commands such as `scans.line_scan(...)` use the current server-side definition.
3. When a scan is called, the client validates the user inputs, resolves device-name strings to device objects where needed, and bundles repeated positional inputs for scans such as `line_scan` or `umv` before sending the request to the server.
4. On the server, the request is queued and receives runtime identifiers.
5. Once it is the scan's turn to run, the scan server queue hands over the request to a scan worker.
6. The scan worker runs the scan class's lifecycle hooks and sends device instructions through Redis.
7. Devices publish readouts and status updates.
8. The scan bundler groups those readouts into logical scan points.
9. Clients, history, and the file writer consume the resulting scan data.

From the user side, the important part is consistency: every scan goes through the same backend
steps, reports its progress in the same general way, and produces scan data that can be accessed
through the same tools afterward.

## The Shared Scan Shape

As mentioned above, all BEC scans follow the same overall shape. They share the same lifecycle steps, and they use the same helpers to report themselves and produce data. This allows users to be always prompted with a familiar structure, even when the motion logic of the scan differs. The shared shape also makes it easier to learn new scans, since you can focus on the differences in motion logic rather than having to learn a new overall structure for each scan. The lifecycle steps are:

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

BEC runs these lifecycle steps in the same order every time.

This shared shape is why BEC scans feel related rather than like separate one-off tools.

## Where To Go Next

If you want the next layer of detail:

- read [Learn by example](../learn/scans/learn-by-example.md){ data-preview } to go through the `acquire` scan example in detail, and see how the shared scan shape applies to a specific scan type.

## What to Remember

!!! info "What to remember"
    - In BEC, all scans follow the same overall shape.
    - Different scan types use the same backend framework, even when their motion logic differs.
    - Every scan reports itself in a common structured way while it runs.
    - Every scan has to implement the same lifecycle steps, even when some of those steps are empty.
    - The lifecycle steps are called in the same order for every scan.

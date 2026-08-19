# Scans

This page summarizes the built-in scans that BEC commonly publishes to clients.

The exact scan list depends on the scan server and any installed plugins, so treat this page as a
reference for the standard built-ins rather than a hard guarantee of what every deployment exposes.
In a client session, `scans.<TAB>` and `scans.<name>?` always show the live scan surface you
actually have.

## Common built-in scans

### Point and time based acquisition

- `acquire`: take one or more acquisitions at the current position without moving motors.
- `time_scan`: trigger and read at a fixed interval for a requested number of points.
- `line_scan`: step one or more motors through evenly spaced start and stop positions.
- `grid_scan`: step two or more motors through a rectilinear grid, optionally snaked.
- `list_scan`: visit an explicit list of positions instead of generating them from start and stop
  values.
- `log_scan`: use logarithmically spaced positions between start and stop.

### Region and geometry scans

- `multi_region_line_scan`: join several separate 1D regions into one scan.
- `multi_region_grid_scan`: join several rectangular sub-grids into one scan.
- `round_scan`: sample concentric circular shells around a center.
- `round_roi_scan`: generate circular-shell points clipped to a rectangular region of interest.
- `hexagonal_scan`: sample a 2D hexagonal grid inside the requested bounds.
- `fermat_scan`: sample a Fermat spiral inside rectangular bounds.

### Continuous scans

- `cont_line_scan`: move one motor continuously between start and stop while triggering readout at
  predefined positions.
- `line_sweep_scan`: move one motor continuously and trigger readout from live readback updates
  instead of a precomputed point table.

### Motion commands exposed through the scan interface

- `mv`: move one or more motors and return control immediately after the request is sent.
- `umv`: move one or more motors and wait for the requested motion to finish before returning.

These commands are published through the same scan infrastructure, but they are motion commands,
not data-taking scans.

## How to read scan help in the client

The client learns scan signatures, docs, and GUI grouping dynamically from the scan server.

Use:

- `scans.<TAB>` to discover what is available right now
- `scans.line_scan?` to inspect one scan's signature, docstring, and examples
- GUI scan dialogs to inspect grouped inputs from `gui_config`

## What stays consistent across scans

Even when the motion logic changes, scans in BEC still share the same general model:

- they are submitted through the client as `scans.<name>(...)`
- they run on the scan server, not in the client process
- they publish progress and scan metadata in the same general way
- they return scan reports and appear in `bec.history` afterward

## Related topics

- [Introduction to Scans](../../learn/scans/introduction.md){ data-preview }
- [Scan Lifecycle](../../learn/scans/lifecycle.md){ data-preview }
- [Scan Components](../../learn/scans/scan-components.md){ data-preview }

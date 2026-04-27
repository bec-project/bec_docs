---
related:
  - title: Scan Components
    url: learn/scans/scan-components.md
  - title: Learn by Example
    url: learn/scans/learn-by-example.md
  - title: Fast Axis and Slow Axis
    url: learn/scans/fast-axis-slow-axis.md
---

# Position Generators

Many scans need a prepared list of points before the scan can start moving hardware.

BEC keeps that logic in `position_generators`: a collection of reusable helpers that generate
positions for common scan patterns. A scan typically uses these helpers in `prepare_scan`, then
records the resulting positions in `scan_info`, checks limits, and lets `components` handle the
repeated execution pattern.

## Why Position Generators Matter

Position generation is often one of the most scan-specific parts of a scan.

For example, a scan may need to produce:

- a straight line through one or more axes
- a rectangular grid, optionally with snaking
- a spiral or Fermat pattern
- a circular shell pattern
- several disconnected regions combined into one trajectory

Keeping those patterns in reusable helpers makes scan classes shorter and easier to read.

## Common Position Generators

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
      <th>Typical scan type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap;"><code>line_scan_positions(...)</code></td>
      <td>Builds linearly spaced points for one or more axes.</td>
      <td>line scans</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>log_scan_positions(...)</code></td>
      <td>Builds positions with logarithmically increasing spacing between start and stop.</td>
      <td>logarithmic line scans</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>nd_grid_positions(...)</code></td>
      <td>Builds an N-dimensional grid, with optional snaking to reduce unnecessary travel.</td>
      <td>grid scans</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>multi_region_line_positions(...)</code></td>
      <td>Builds one 1D trajectory across several separate line regions.</td>
      <td>multi-region line scans</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>multi_region_grid_positions(...)</code></td>
      <td>Builds several rectangular sub-grids and concatenates them into one scan path.</td>
      <td>multi-region grid scans</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>spiral_positions(...)</code></td>
      <td>Builds an Archimedean spiral clipped to a rectangular region.</td>
      <td>spiral scans</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>fermat_spiral_pos(...)</code></td>
      <td>Builds a Fermat spiral inside rectangular scan bounds.</td>
      <td>Fermat spiral scans</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>round_scan_positions(...)</code></td>
      <td>Builds concentric circular shells around a center point.</td>
      <td>round scans</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>get_round_roi_scan_positions(...)</code></td>
      <td>Builds circular shell points and clips them to a rectangular region of interest.</td>
      <td>round ROI scans</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>hex_grid_2d(...)</code></td>
      <td>Builds a 2D hexagonal grid inside the requested scan bounds.</td>
      <td>hexagonal scans</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>oscillating_positions(...)</code></td>
      <td>Yields values in a back-and-forth pattern instead of returning a finite point array.</td>
      <td>hysteresis or oscillating scans</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>rotate_points(...)</code></td>
      <td>Rotates a 2D point set around a chosen center.</td>
      <td>supporting helper</td>
    </tr>
  </tbody>
</table>

## Position Array Shape

For helpers that return a finite point list, the result is a NumPy array of shape
`(num_points, num_motors)`. Each row is one scan point, and each column corresponds to one motor or
scanned axis. For single-axis scans, that usually means shape `(num_points, 1)`.

For example, a two-motor grid scan might generate and consume positions like this:

```py
positions = position_generators.nd_grid_positions(
    [(-1.0, 1.0, 3), (-2.0, 2.0, 5)],
    snaked=True,
)

for point in positions:
    motor1_position = point[0]
    motor2_position = point[1]
```

## How Scans Use Them

The usual pattern is:

1. use a position generator in `prepare_scan`
2. optionally shift those points for relative motion
3. check limits against the final point list
4. store the positions and point count in `scan_info`
5. pass the prepared positions into `components.step_scan(...)` or another execution helper

This keeps the scan code split into clear responsibilities:

- position generators decide where the scan should go
- `actions` handles lifecycle and reporting
- `components` handles the repeated execution pattern

If the scan wants to improve the traversal order after generating the points, it can then call
`components.optimize_trajectory(...)` before execution begins. This is useful when the point
generator defines which points should be visited, but the scan still wants to reduce unnecessary
travel between those points.

## When Not To Use One

Not every scan needs a position generator.

For example:

- `acquire` does not move through a point list at all
- monitor-style scans may react to live updates instead of a precomputed trajectory
- some scans generate their next point on the fly rather than preparing the full array up front

So position generators are common, but they are most useful when the scan can describe its path in
advance.

## Next Step

After position generators, continue with [fast axis and slow axis](fast-axis-slow-axis.md).

That page explains the axis-order convention used when scans generate points for more than one
motor.

## What To Remember

!!! info "What to remember"
    - Position generators build reusable point lists for common scan geometries.
    - They are most often used in `prepare_scan` before limit checks and execution begin.
    - They keep scan classes shorter by separating path generation from execution logic.

---
related:
  - title: Position Generators
    url: learn/scans/position-generators.md
  - title: ScanArgument
    url: learn/scans/scanargument.md
  - title: Learn by Example
    url: learn/scans/learn-by-example.md
---

# Fast Axis and Slow Axis

When a scan moves more than one axis, the order of those axes matters.

BEC follows one consistent convention:

- the outermost axis is the slow axis
- the innermost axis is the fast axis

That means the fast axis changes most often, while the slow axis changes only after the inner sweep
has finished.

## What That Means In Practice

A useful way to read the convention is:

For every point in `samx` from `-5` to `5`, move `samy` from `-10` to `10`.

In that example:

- `samx` is the slow axis
- `samy` is the fast axis

So the scan stays on one `samx` value while it sweeps through the full `samy` range, then advances
to the next `samx` value and repeats.

!!! example
    A 2D grid scan like this:

    ```py
    scans.grid_scan(dev.samx, -5, 5, 3, dev.samy, -10, 10, 5, snaked=False, relative=False)
    ```

    would have `samx` as the slow axis and `samy` as the fast axis, so the scan would:

    1. keep `samx` fixed at `-5` while it sweeps `samy` from `-10` to `10`
    2. advance `samx` to the next value (in this case `0`) while it again sweeps `samy` from `-10` to `10`
    3. advance `samx` to the next value (in this case `5`) while it again sweeps `samy` from `-10` to `10`
    4. finish the scan after the last `samx` value has been reached and its inner sweep has completed

    If the requirement is to have `samy` as the slow axis and `samx` as the fast axis, one would just swap the order of the motor arguments:

    ```py
    scans.grid_scan(dev.samy, -10, 10, 5, dev.samx, -5, 5, 3, snaked=False, relative=False)
    ```

## Why This Matters

This convention affects how you read and define multi-axis scans:

- the order of axes in a grid or nested scan is meaningful
- the generated point order follows that nesting
- snaking typically changes the traversal direction of the fast axis while keeping the same slow-axis structure

Keeping that convention stable makes scan definitions easier to reason about and makes generated
point lists more predictable.

## A Simple Example

At the user level, a grid scan might look like this:

```py
scans.grid_scan(dev.samx, -5, 5, 3, dev.samy, -10, 10, 5, snaked=False)
```

The same ordering appears in the generated positions:

```py
positions = position_generators.nd_grid_positions(
    [(-5.0, 5.0, 3), (-10.0, 10.0, 5)],
    snaked=False,
)

for point in positions:
    samx_position = point[0]
    samy_position = point[1]
```

Here the first axis is the outer loop and the second axis is the inner loop:

- axis 1: slow axis
- axis 2: fast axis

So the point order follows this pattern:

1. keep the first axis fixed
2. sweep the second axis through all of its values
3. advance the first axis
4. repeat

## How To Read Existing Scan Code

When you see code such as:

```py
positions = position_generators.nd_grid_positions(
    [(start_motor1, stop_motor1, steps_motor1), (start_motor2, stop_motor2, steps_motor2)],
    snaked=True,
)
```

read it as:

- the first tuple defines the slow axis
- the second tuple defines the fast axis

That same idea also applies more generally to nested point generation: outer definitions correspond
to slower-changing axes, and inner definitions correspond to faster-changing axes.

## Next Step

After axis-order conventions, continue with [ScanArgument](scanargument.md).

That page covers the rich input metadata used in scan signatures.

## What To Remember

!!! info "What to remember"
    - In BEC, the outermost axis is the slow axis and the innermost axis is the fast axis.
    - The fast axis changes most often within the generated point list.
    - This convention makes multi-axis scan definitions and point ordering easier to read.

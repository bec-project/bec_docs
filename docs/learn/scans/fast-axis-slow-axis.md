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

- the first user-provided axis is the fast axis
- the last user-provided axis is the slow axis

That means the fast axis changes most often, while the slow axis changes only after the fast-axis
sweep has finished.

## What That Means In Practice

A useful way to read the convention is:

For every point in `samx` from `-5` to `5`, move `samy` from `-10` to `10`.

In that example:

- `samx` is the fast axis
- `samy` is the slow axis

So the scan sweeps through all `samx` values while `samy` stays fixed, then advances `samy` to its
next value and repeats.

!!! example
    A 2D grid scan like this:

    ```py
    scans.grid_scan(dev.samx, -5, 5, 3, dev.samy, -10, 10, 5, snaked=False, relative=False)
    ```

    would have `samx` as the fast axis and `samy` as the slow axis, so the scan would:

    1. keep `samy` fixed at `-10` while it sweeps `samx` from `-5` to `5`
    2. advance `samy` to the next value (in this case `-5`) while it again sweeps `samx` from `-5` to `5`
    3. continue until the last `samy` value has been reached and its `samx` sweep has completed
    4. finish the scan after the last row of fast-axis points has been acquired

    If the requirement is to have `samy` as the fast axis and `samx` as the slow axis, swap the
    order of the motor arguments:

    ```py
    scans.grid_scan(dev.samy, -10, 10, 5, dev.samx, -5, 5, 3, snaked=False, relative=False)
    ```

## Why This Matters

This convention affects how you read and define multi-axis scans:

- the order of axes in a grid or nested scan is meaningful
- the generated point order follows that nesting
- snaking typically changes the traversal direction of the fast axis while keeping the same
  slow-axis structure

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

- axis 1: fast axis
- axis 2: slow axis

So the point order follows this pattern:

1. keep the second axis fixed
2. sweep the first axis through all of its values
3. advance the second axis
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

- the first tuple defines the fast axis
- the second tuple defines the slow axis

That same idea also applies more generally to nested point generation in BEC's grid helpers: early
user-provided axis definitions correspond to faster-changing axes, and later ones correspond to
slower-changing axes.

## Next Step

After axis-order conventions, continue with [ScanArgument](scanargument.md).

That page covers the rich input metadata used in scan signatures.

## What To Remember

!!! info "What to remember"
    - In BEC grid-style scans, the first user-provided axis is the fast axis and later axes change more slowly.
    - The fast axis changes most often within the generated point list.
    - This convention makes multi-axis scan definitions and point ordering easier to read.

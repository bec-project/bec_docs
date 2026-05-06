---
related:
  - title: Position Generators
    url: learn/scans/position-generators.md
  - title: Argument Bundles
    url: learn/scans/argument-bundles.md
  - title: GUI Config
    url: learn/scans/gui-config.md
  - title: Learn by Example
    url: learn/scans/learn-by-example.md
---

# ScanArgument

`ScanArgument(...)` enables a scan to attach rich metadata to one of its inputs.

As a result, the signature can provide more information to users and clients, such as which units an input uses, which bounds apply, and how the input should be labeled in a GUI.

!!! Warning "It is highly recommended to use `ScanArgument` for any scan input."

## A Typical Example

```py
from typing import Annotated

from bec_lib.scan_args import ScanArgument, Units


exp_time: Annotated[
    float,
    ScanArgument(display_name="Exposure Time", units=Units.s, ge=0),
] = 0
```

This says several things at once:

- the input should be treated as a `float`
- GUIs should label it as `Exposure Time`
- the value is expressed in seconds
- the value must be greater than or equal to zero

## Reusing Common Annotations With `DefaultArgType`

Writing out full `Annotated[..., ScanArgument(...)]` definitions is useful when a scan needs a
custom input definition. However, BEC already provides shared aliases for the common internal scan
parameters that are represented in [scan info](scan-info.md){data-preview} and used in many scans.

To avoid repeating those annotations in every scan class, these common definitions are collected in
`DefaultArgType`.

For example, the typical example above is equivalent to:

```py
from bec_lib.scan_args import DefaultArgType


exp_time: DefaultArgType.ExposureTime = 0
```

The same pattern is used for other internal scan parameters such as `FramesPerTrigger`,
`SettlingTime`, `SettlingTimeAfterTrigger`, `ReadoutTime`, `BurstAtEachPoint`, and also for common
boolean scan options such as `Relative`.

This keeps scan signatures shorter while still preserving the same `ScanArgument` metadata for
validation, GUI generation, and scan discovery.

## Common `ScanArgument` Fields

Some of the most commonly used fields are listed below.

<!-- The table is in html as the columns would otherwise wrap. There seems to be no internal way to control column width in markdown -->
<table>
  <colgroup>
    <col style="width: 26%;">
    <col style="width: 50%;">
    <col style="width: 24%;">
  </colgroup>
  <thead>
    <tr>
      <th>Field</th>
      <th>Role</th>
      <th>Typical use</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap;"><code>display_name</code></td>
      <td>Provides a clearer user-facing label than the raw Python parameter name.</td>
      <td>GUI labels</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>description</code></td>
      <td>Provides a longer explanation of what the input means.</td>
      <td>help text or documentation</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>tooltip</code></td>
      <td>Adds short explanatory text for interactive UIs.</td>
      <td>GUI hover text</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>units</code></td>
      <td>Declares the explicit unit for the input, such as seconds or degrees.</td>
      <td>user-facing display</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>reference_units</code></td>
      <td>Tells BEC to interpret the value in the units of another input, such as a motor argument.</td>
      <td>user-facing display</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>gt</code>, <code>ge</code>, <code>lt</code>, <code>le</code></td>
      <td>Applies numeric bounds to the input.</td>
      <td>validation</td>
    </tr>
  </tbody>
</table>

## Units and Reference Units

Two patterns are especially common.

Explicit units:

- `Annotated[float, ScanArgument(units=Units.s)]`
- `Annotated[float, ScanArgument(units=Units.eV)]`
- `Annotated[float, ScanArgument(units=Units.deg)]`

Reference units:

- `Annotated[float, ScanArgument(reference_units="motor1")]`
- `Annotated[float, ScanArgument(reference_units="motor2")]`
- `Annotated[float, ScanArgument(reference_units="device")]`

Reference units are especially useful for scan inputs such as start, stop, or step size, where the
value should automatically use the same unit as a related device input.

## Next Step

After `ScanArgument`, continue with [argument bundles](argument-bundles.md){data-preview} for
repeated positional inputs and [GUI config](gui-config.md){data-preview} for graphical grouping.

## What To Remember

!!! info "What to remember"
    - `ScanArgument` attaches rich metadata to individual scan inputs.
    - It is usually used through `Annotated[..., ScanArgument(...)]`.
    - It helps BEC validate inputs and present them clearly in GUIs and clients.

---
related:
  - title: Position Generators
    url: learn/scans/position-generators.md
  - title: Scan Definition Info
    url: learn/scans/scan-definition-info.md
  - title: Learn by Example
    url: learn/scans/learn-by-example.md
---

# ScanArgument

`ScanArgument(...)` is the main way a scan attaches rich metadata to one of its inputs.

In practice, this metadata is usually carried through `Annotated[..., ScanArgument(...)]` in a
scan's `__init__` signature. That makes the input definition useful not only to Python, but also to
validation, GUIs, and client-side scan discovery.

## Why `ScanArgument` Matters

Without `ScanArgument`, a scan input would mostly just have a Python type.

With `ScanArgument`, the same input can also describe:

- how it should be labeled in a GUI
- which units it uses
- whether it should use the units of another input
- which bounds or limits apply
- which extra explanatory text should be shown to the user

That is what lets one scan signature serve as both an implementation interface and a user-facing
definition.

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
      <td>timing or physical values</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>reference_units</code></td>
      <td>Tells BEC to interpret the value in the units of another input, such as a motor argument.</td>
      <td>position-like inputs</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>gt</code>, <code>ge</code>, <code>lt</code>, <code>le</code></td>
      <td>Applies numeric bounds to the input.</td>
      <td>validation</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>reference_limits</code></td>
      <td>Uses the limits of another input as a validation reference.</td>
      <td>device-related bounds</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>alternative_group</code></td>
      <td>Associates inputs that represent alternative ways to express a similar choice.</td>
      <td>advanced GUI behavior</td>
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

## How It Fits Into Scan Definitions

`ScanArgument` does not replace the scan signature. It enriches it.

The usual pattern is:

1. define the Python parameter in `__init__`
2. wrap it in `Annotated[..., ScanArgument(...)]`
3. let BEC serialize that richer input definition for validation and GUI generation

This is why `ScanArgument` shows up so often in real scan definitions: it is the bridge between the
scan's code-level inputs and its user-facing definition.

## Next Step

After `ScanArgument`, continue with [scan definition info](scan-definition-info.md), which covers
the broader scan-definition model around the signature, grouped positional inputs, and `gui_config`.

## What To Remember

!!! info "What to remember"
    - `ScanArgument` attaches rich metadata to individual scan inputs.
    - It is usually used through `Annotated[..., ScanArgument(...)]`.
    - It helps BEC validate inputs and present them clearly in GUIs and clients.

---
related:
  - title: ScanArgument
    url: learn/scans/scanargument.md
  - title: Argument Bundles
    url: learn/scans/argument-bundles.md
  - title: Learn by Example
    url: learn/scans/learn-by-example.md
---

# GUI Config

This page explains how scans can group their inputs for graphical clients through `gui_config`.

## What `gui_config` Does

`gui_config` describes how scan inputs should be grouped in graphical interfaces.

For example, a scan can group inputs under headings such as:

- `Device`
- `Movement Parameters`
- `Acquisition Parameters`

This does not change how the scan runs. It helps GUIs present scan inputs in a clear structure
instead of showing one flat list of parameters.

## A Typical Example

```py
gui_config = {
    "Device 1": ["motor1", "start_motor1", "stop_motor1"],
    "Device 2": ["motor2", "start_motor2", "stop_motor2"],
    "Movement Parameters": ["step", "relative"],
    "Acquisition Parameters": [
        "exp_time",
        "frames_per_trigger",
        "settling_time",
        "readout_time",
    ],
}
```

In this example, the scan definition is still the same Python class and the same Python signature.
`gui_config` only changes how that information is grouped and presented in graphical clients.

## How It Fits With Scan Signatures

`gui_config` does not replace the scan signature or `ScanArgument` metadata.

Instead, these pieces work together:

- the signature defines which inputs exist
- `ScanArgument` enriches individual inputs with labels, units, bounds, and descriptions
- `gui_config` groups those inputs into a clearer layout for GUIs

This is why `gui_config` is best thought of as presentation metadata rather than execution logic.

## Reloading The Scan Server

If you add a new scan or change an existing scan class, the scan server must reload that Python code
before the changes become available.

In practice, that means you should restart or reload the scan server after editing scan
implementations. Otherwise the running server will continue using the old version of the scan.

## Next Step

If you want to see `gui_config` and related scan-definition details in a richer real scan, read the
[worked example: hexagonal scan](hexagonal-scan-example.md).

## What To Remember

!!! info "What to remember"
    - `gui_config` groups scan inputs for graphical clients.
    - It changes presentation, not scan execution.
    - `gui_config` works alongside the scan signature and `ScanArgument` metadata.
    - After changing scan code, the scan server must be reloaded or restarted.

# Scan Definition Info

This page explains the extra information a scan class can define so that the rest of BEC can present
and understand the scan correctly.

## The Scan Signature

In the current scan implementation, a scan definition is described largely by its `__init__`
signature plus a few class attributes.

The scan server serializes that signature and publishes it to clients. The client then uses it to:

- expose the scan under `scans.<name>`
- attach a live Python signature in IPython
- validate kwargs and bundled positional inputs
- resolve device-name strings to device objects when the annotations require that

This means the signature is no longer only local Python documentation. It is part of the runtime API
contract between the scan server, the client, and GUIs.

## `arg_input` and `arg_bundle_size`

!!! tip
    `arg_input` and `arg_bundle_size` are special cases for scans with an undefined number of
    input arguments. Most scans developed in plugins do not need them.

If the number of input arguments is not fixed, the usual Python-style fixed signature is not enough.

For example, a line scan can work with any number of motors in parallel, so the scan cannot rely on
one fixed positional argument layout in the way an ordinary Python function usually would.

In those cases, scans with repeated positional bundles declare those bundles explicitly.

For a line scan, that can look like this:

```py
arg_input = {
    "device": DeviceBase,
    "start": float,
    "stop": float,
}
arg_bundle_size = {"bundle": 3, "min": 1, "max": None}
```

`arg_bundle_size` then tells BEC how many positional values belong to one bundle and how many
bundles are allowed.

This is what lets BEC validate a call such as:

```py
scans.line_scan(dev.samx, -1, 1, dev.samy, -2, 2, steps=5, relative=False)
```

without treating those positional arguments as an unstructured `*args` blob.

Rich input metadata for individual parameters is covered separately on
[ScanArgument](scanargument.md). This page focuses on the broader scan-definition structure around
the signature, grouped positional bundles, and GUI grouping.

## `gui_config`

`gui_config` describes how scan inputs should be grouped in graphical interfaces.

For example, a scan can group inputs under headings such as:

- `Device`
- `Movement Parameters`
- `Acquisition Parameters`

This does not change how the scan runs. It helps GUIs present scan inputs in a clear structure
instead of showing one flat list of parameters.

## Unit Annotations

Many scans annotate numerical inputs through `Annotated[..., ScanArgument(...)]`.

Typical examples are:

- `Annotated[float, ScanArgument(units=Units.s)]` for seconds
- `Annotated[float, ScanArgument(units=Units.eV)]` for electron volts
- `Annotated[float, ScanArgument(units=Units.deg)]` for degrees

These annotations make the intended unit explicit in the scan definition.

Scans can also reference the unit of another input directly. For example:

- `Annotated[float, ScanArgument(reference_units="motor1")]`
- `Annotated[float, ScanArgument(reference_units="motor2")]`
- `Annotated[float, ScanArgument(reference_units="device")]`

This means the value should use the same unit as that referenced input. So
`Annotated[float, ScanArgument(reference_units="motor1")]` means “interpret this value in the
units of `motor1`.”

This is especially useful for position-like parameters such as starts, stops, and step sizes.

## `scan_def` and `scan_group`

Two pieces of scan-definition-related metadata are now handled on the client side and propagated in
the request `system_config`:

- `scans.scan_def`, which creates a temporary scan-definition ID and wraps several scan requests into one logical definition
- `scans.scan_group`, which assigns several scan requests to one queue group

These are context managers and decorators. They do not replace the scan class definition itself, but
they are part of how modern BEC associates related scan requests at runtime.

## Reloading The Scan Server

If you add a new scan or change an existing scan class, the scan server must reload that Python code
before the changes become available.

In practice, that means you should restart or reload the scan server after editing scan
implementations. Otherwise the running server will continue using the old version of the scan.

## Next Step

If you want to see these ideas in a richer real scan, read the
[worked example: hexagonal scan](hexagonal-scan-example.md).

## What To Remember

!!! info "What to remember"
    - The serialized scan signature is part of the runtime API between the scan server, clients, and GUIs.
    - `arg_input` and `arg_bundle_size` define repeated positional bundles such as move targets or line-scan ranges.
    - `ScanArgument` carries units, bounds, labels, and other GUI-facing metadata for individual inputs.
    - `gui_config` helps GUIs present scan parameters clearly.
    - Unit annotations make scan inputs more explicit and can also refer to the units of another input.
    - After changing scan code, the scan server must be reloaded or restarted.

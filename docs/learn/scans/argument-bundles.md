---
related:
  - title: ScanArgument
    url: learn/scans/scanargument.md
  - title: GUI Config
    url: learn/scans/gui-config.md
  - title: Learn by Example
    url: learn/scans/learn-by-example.md
---

# Argument Bundles

This page explains how scans can describe repeated positional input bundles when a normal fixed
Python signature is not enough.

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
[ScanArgument](scanargument.md).

## Reloading The Scan Server

If you add a new scan or change an existing scan class, the scan server must reload that Python code
before the changes become available.

In practice, that means you should restart or reload the scan server after editing scan
implementations. Otherwise the running server will continue using the old version of the scan.

## Next Step

After argument bundles, continue with [GUI Config](gui-config.md) to see how scans group inputs for
graphical clients.

## What To Remember

!!! info "What to remember"
    - The serialized scan signature is part of the runtime API between the scan server, clients, and GUIs.
    - `arg_input` and `arg_bundle_size` define repeated positional bundles such as move targets or line-scan ranges.
    - `ScanArgument` covers rich metadata for individual inputs, while argument bundles describe repeated positional structure.
    - After changing scan code, the scan server must be reloaded or restarted.

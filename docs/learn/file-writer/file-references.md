---
related:
  - title: File writing
    url: learn/file-writer/introduction.md
  - title: DefaultFormat and the default HDF5 layout
    url: learn/file-writer/default-format.md
  - title: Add a custom NeXuS structure for the file writer
    url: how-to/customize-bec/add-a-custom-nexus-structure.md
---

# File References from Devices

Some devices create their own files instead of sending their data to BEC. These are most often large area detectors with their own backend for writing HDF5 files.

BEC supports this by letting devices report file information through ophyd-side helper signals such as `FileEventSignal` in `ophyd_devices.utils.bec_signals`. Devices can also indicate hinted entries in their files that the master file should link to. This allows the master file to link to specific datasets in the external file instead of linking to the file root.

!!! learn "[Learn about BEC signal classes](../devices/bec-signals.md){ data-preview }"

## How `DefaultFormat` uses file references

`DefaultFormat.write_bec_entries()` creates `/entry/collection/file_references`.

File references from all devices are collected in that group as external links.
For each hinted entry, `DefaultFormat` creates an external link with the hinted name. If there are no hints, it creates a fallback link named `data` that points to the root of the external file.

That means custom file-writer plugins can reuse the collected references through `self.file_references` and place additional external links wherever their NeXuS layout needs them.

## When this matters for custom formats

This mechanism is useful when:

- a detector writes its own HDF5 file
- the master file should link to detector data instead of duplicating it
- a beamline-specific layout wants links under `entry/instrument/...` or `entry/data`

In those cases, the custom writer can use `self.file_references` together with `create_ext_link(...)` to place links in the desired structure.

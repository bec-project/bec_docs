---
related:
  - title: File writing
    url: index.md
  - title: Add a custom NeXuS structure for the file writer
    url: ../../how-to/customize-bec/add-a-custom-nexus-structure.md
---

# DefaultFormat and the Default HDF5 Layout

The built-in NeXuS writer format lives in `bec_server.file_writer.default_writer.DefaultFormat`.

When BEC writes the master HDF5 file, it instantiates `DefaultFormat` or one of its subclasses with:

- `storage`: an `HDF5Storage` instance used to build the HDF5 tree
- `data`: scan data grouped by device
- `info_storage`: scan metadata, including BEC metadata and converted start and end timestamps
- `configuration`: device configuration data
- `file_references`: external file references collected during the scan
- `beamline_states`: recorded beamline state messages
- `device_manager`: the current device manager

## How the layout is built

The writer calls `get_storage_format()`.

That method performs two steps in order:

1. `write_bec_entries()` creates the base structure that BEC expects.
2. `format()` adds the format-specific groups, datasets, and links.

For custom writers, the important consequence is simple: your `format()` method extends the existing storage tree. It does not return a new dictionary.

## What `write_bec_entries()` creates

Before custom formatting runs, BEC already creates the main structural content under `/entry`.

This includes:

- `/entry` with `NXentry`
- `/entry/collection/devices`
- `/entry/collection/metadata`
- `/entry/collection/readout_groups`
- `/entry/collection/configuration`
- `/entry/collection/file_references`
- `/entry/collection/states`

The `readout_groups` entries are derived from BEC readout priorities such as `baseline`, `monitored`, and `async`.

The `file_references` group is where BEC stores external links to files announced by devices.

The `states` group stores beamline state messages in structured datasets.

!!! note

    The default structure in `entry/collection` is used by BEC functionality beyond file writing. Custom formats should extend it, not overwrite it.

## What `format()` is expected to do

`DefaultFormat.format()` and any subclass implementation operate on `self.storage`.

In practice, a custom writer should:

- create or reuse groups with `self.storage.create_group(...)`
- add datasets with `create_dataset(...)`
- add NeXuS-style links with `create_soft_link(...)` or `create_ext_link(...)`
- use helper methods such as `self.get_entry(...)` to access device values from scan data

If you want to preserve the standard default layout and only add beamline-specific entries, call `super().format()` first and then append your additions.

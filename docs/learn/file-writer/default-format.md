---
related:
  - title: File writing
    url: learn/file-writer/introduction.md
  - title: Customizing the file writer
    url: learn/file-writer/plugin-repository-integration.md
  - title: Add a custom NeXuS structure for the file writer
    url: how-to/customize-bec/add-a-custom-nexus-structure.md
---

# Default HDF5 Layout

The built-in NeXuS writer writes data in a format defined by`bec_server.file_writer.default_writer.DefaultFormat`.
BEC relies on this format to provide automated access to scan data and metadata, so it is important to understand the structure it creates and how custom formats can extend it.

Listed below is an overview of important components of the DefaultFormat, which can become relevant when customizing the file writer to use a beamline-specific NeXuS structure.

- `storage`: A storage object that is used to build the HDF5 tree
- `data`: Scan data grouped by device
- `info_storage`: Scan metadata, including BEC metadata and converted start and end timestamps
- `configuration`: Device configuration data
- `file_references`: External file references collected during the scan
- `beamline_states`: Beamline state configurations recorded during the scan
- `device_manager`: The current device manager

## Basic structure

The basic structure of the HDF5 file is created under the `/entry/collection` group. This includes groups for devices, metadata, readout groups, configuration, file references, and states. The writer creates this structure through the `write_bec_entries()` method, which is called before the `format()` method that custom formats can override.

For custom writers, the important consequence is simple: your `format()` method extends the existing storage tree. You should avoid overwriting any existing structure under `/entry/collection`, as BEC relies on it for functionality such as history access. Instead, add your beamline-specific entries in new groups or as links to existing groups.

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

The `file_references` group is where BEC stores external links to data from devices with their own file writing, such as for example and AreaDetector with HDF5 plugin.

The `states` group stores beamline state messages in structured datasets.

## What `format()` is expected to do

`DefaultFormat.format()` and any subclass implementation operate on `self.storage`. There are a set of methods available to create groups, datasets, and links. Custom formats should use these to extend the existing structure with beamline-specific entries. 

Some common operations include:

- create or reuse groups with `self.storage.create_group(...)`
- add datasets with `create_dataset(...)`
- add data through links, either soft links to existing groups or datasets with `create_soft_link(...)` or external links to datasets in external files with `create_ext_link(...)`.
- use helper methods such as `self.get_entry(...)` to access device values from scan data

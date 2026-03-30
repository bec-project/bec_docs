---
related:
  - title: File writing
    url: ../../learn/file-writer/index.md
---

# Add a custom NeXuS structure for the file writer

!!! Info "Overview"

    Define a custom NeXuS layout for files written by BEC. This is done by subclassing `DefaultFormat` and writing your custom layout in the `format()` method.

## Pre-requisites
- A beamline plugin repository is available and installed.
- Write access (beamline manager) to the beamline plugin package.

!!! learn "[Learn about file writing in BEC](../../learn/file-writer/index.md){ data-preview }"

## Create a custom writer format class

- Create a new module in your plugin under `<bec_plugin>.file_writer.<module>`.

``` py
# <bec_plugin>/file_writer/custom_nexus.py
from bec_server.file_writer.default_writer import DefaultFormat


class BeamlineNeXusFormat(DefaultFormat):
    """Beamline-specific NeXuS structure for BEC output files."""

    def format(self) -> None:
        """
        Prepare the NeXus file format.
        Override this method in file writer plugins to customize the HDF5 file format.

        The class provides access to the following attributes:
        - self.storage: The HDF5Storage object.
        - self.data: The data dictionary.
        - self.file_references: The file references dictionary.
        - self.device_manager: The DeviceManagerBase object.

        See also: :class:`bec_server.file_writer.file_writer.HDF5Storage`.

        """
        pass
```

- Implement the `format()` method to extend the NeXuS structure. You can use `self.storage` to create groups, datasets, and links. Use helper accessors such as `self.get_entry(...)` when you want values from device data.


``` py
# <bec_plugin>/file_writer/custom_nexus.py
from bec_server.file_writer.default_writer import DefaultFormat


class BeamlineNeXusFormat(DefaultFormat):
    """Beamline-specific NeXuS structure for BEC output files."""

    def format(self) -> None:
        # Add entry group
        entry = self.storage.create_group("entry")

        # Add control group with monitor data
        control = entry.create_group("control")
        control.attrs["NX_class"] = "NXmonitor"
        control.create_dataset(name="mode", data="monitor")
        control.create_dataset(name="integral", data=self.get_entry("bpm4i"))
```

- Create a soft link to an existing dataset or an external link through a file reference.

    !!! learn "[Learn about file_references from devices](../../learn/file-writer/file-references.md){ data-preview }"

``` py
# <bec_plugin>/file_writer/custom_nexus.py
from bec_server.file_writer.default_writer import DefaultFormat


class BeamlineNeXusFormat(DefaultFormat):
    """Beamline-specific NeXuS structure for BEC output files."""

    def format(self) -> None:
        # Add entry group
        entry = self.storage.create_group("entry")

        # Add control group with monitor data
        control = entry.create_group("control")
        control.attrs["NX_class"] = "NXmonitor"
        control.create_dataset(name="mode", data="monitor")
        control.create_dataset(name="integral", data=self.get_entry("bpm4i"))

        # Add an external link to a file reference
        if "eiger" in self.device_manager.devices:
            instrument = entry.create_group("instrument")
            instrument.attrs["NX_class"] = "NXinstrument"
            eiger = instrument.create_group("eiger")
            eiger.attrs["NX_class"] = "NXdetector"

            file_ref = self.file_references.get("eiger")
            if file_ref is not None:
                # file_ref is a FileMessage with file_path and hinted_h5_entries
                eiger.create_ext_link("data", file_ref.file_path, "/entry/data/data")

            # Add a soft link to the external link above
            main_data = entry.create_group("data")
            main_data.attrs["NX_class"] = "NXdata"
            main_data.create_soft_link(name="data", target="/entry/instrument/eiger/data")
```

!!! warning "Important"

    BEC relies on a consistent data structure under `entry/collection` for functionality such as history access. This structure is written automatically by the FileWriter. Custom formats should not overwrite it, as doing so may break this functionality.

## Expose the custom format in the plugin module
BEC automatically discovers file-writer plugins from the module. You can simply add your class to the `__init__.py` of the file writer module.

``` py
# <bec_plugin>/file_writer/__init__.py
from .custom_nexus import BeamlineNeXusFormat
```

!!! success "Congratulations!"
    You have successfully added a custom NeXuS structure to the BEC file writer. BEC can now write files using your beamline-specific layout.

## Common Pitfalls
- Not exposing the custom format class in the file writer module `<bec_plugin>.file_writer.__init__.py`.
- Returning a dictionary from `format()`. The method should mutate `self.storage` and return `None`.
- Treating `self.file_references["eiger"]` as a plain dictionary. Entries are `FileMessage` objects.
- The BEC server needs to be restarted after plugin changes are made.

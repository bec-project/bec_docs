---
related:
  - title: File writing
    url: learn/file-writer/introduction.md
  - title: File references from devices
    url: learn/file-writer/file-references.md
---

# Add a Custom NeXuS Structure for the File Writer

!!! Info "Overview"

    Define a custom NeXuS layout for files written by BEC. This is done by subclassing `DefaultFormat` and writing your custom layout in the `format()` method.

## Pre-requisites
- A beamline plugin repository is available and installed.
- Write access (beamline manager) to the beamline plugin package.

!!! learn "[Learn about file writing in BEC](../../learn/file-writer/introduction.md){ data-preview }"

## 1. Create a custom writer format class

Create a new module in your plugin under `<bec_plugin>.file_writer.<module>`.

``` py
from bec_server.file_writer.default_writer import DefaultFormat


class BeamlineNeXusFormat(DefaultFormat):
    """Beamline-specific NeXuS structure for BEC output files."""

    def format(self) -> None:
        pass
```

## 2. Implement the custom layout

Extend the `format()` method with the groups, datasets, and links you want to add.

``` py
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

Use helper accessors such as `self.get_entry(...)` when you want values from device data.

## 3. Add file references or links if needed

If a detector writes its own file, you can add an external link through a file reference.

!!! learn "[Learn about file references from devices](../../learn/file-writer/file-references.md){ data-preview }"

``` py
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

        # Add an external link from a file reference
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

    BEC relies on a consistent data structure under `entry/collection` for functionality such as history access. This structure is written automatically by the file writer. Custom formats should not overwrite it, as doing so may break this functionality.

## 4. Expose the custom format in the plugin module

Add the class to the `__init__.py` of the file writer module so BEC can discover it.

``` py
from .custom_nexus import BeamlineNeXusFormat
```

## 5. Restart BEC and verify the result

Restart the file writer service or the entire BEC server so the updated plugin code is loaded, then run a small test scan and inspect the produced file.

Check that:

- the custom groups are present in the output file
- links point to the expected datasets or external files

!!! success "Congratulations!"
    You have successfully added a custom NeXuS structure to the BEC file writer. BEC can now write files using your beamline-specific layout.

## Common pitfalls
- Not exposing the custom format class in the file writer module `<bec_plugin>.file_writer.__init__.py`.
- Restarting the BEC server after plugin changes are made. The server needs to be restarted to load the new plugin code.
- Treating `self.file_references["eiger"]` as plain dictionaries. Entries are individual `bec_lib.messages.FileMessage` objects.

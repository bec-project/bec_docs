---
related:
  - title: File writing
    url: learn/file-writer/index.md
  - title: Add a custom NeXuS structure for the file writer
    url: how-to/customize-bec/add-a-custom-nexus-structure.md
---

# Customizing the File Writer

BEC discovers custom file-writer formats from the plugin repository entry point group `bec.file_writer`.

The file-writer loader imports the registered module and inspects the classes exposed from it. Those classes become the available writer formats.

In practice, that usually means:

1. your custom writer class is imported from that module, often via `__init__.py`
2. BEC loads the available classes and selects one of them for the master file writer

## How BEC chooses the writer class

The selection logic is:

- if no file-writer plugin is installed, BEC uses the built-in default format
- if exactly one custom writer class is available, BEC uses it automatically
- if multiple custom writer classes are available, BEC uses the class name configured in `file_writer.plugin`

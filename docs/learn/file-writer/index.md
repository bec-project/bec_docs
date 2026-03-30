---
related:
  - title: Add a custom NeXuS structure for the file writer
    url: ../../how-to/customize-bec/add-a-custom-nexus-structure.md
---

# File writing

This section explains how BEC writes HDF5 and NeXuS data, describes the default file format, and covers how the format can be customized.

## What to read first

- [DefaultFormat and the default HDF5 layout](default-format.md)
- [Customizing the file writer from a plugin repository](plugin-repository-integration.md)
- [Async and sync file writing](async-and-sync-writers.md)
- [File references from devices](file-references.md)

## Overview

BEC file writing is organized around a few distinct pieces:

- the master file writer, which assembles the main scan file
- the built-in `DefaultFormat`, which defines the base HDF5 and NeXuS structure
- plugin-provided writer classes, which can extend that structure
- file references, which let devices announce externally created files so they can be linked into the master file
- async writing, which continuously writes data while the scan is still running

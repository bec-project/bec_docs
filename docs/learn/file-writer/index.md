---
related:
  - title: Add a custom NeXuS structure for the file writer
    url: how-to/customize-bec/add-a-custom-nexus-structure.md
---

# File Writing

BEC writes scan data to HDF5 files. It does not strictly enforce a NeXuS convention by default, but beamlines can define their own HDF5 or NeXuS-style structure through a plugin-based file-writer format.

This section explains how BEC writes HDF5 data, describes the default file format, and covers how beamline-specific structures can be customized.

## What to read first

- [Where files are written](where-files-are-written.md)
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

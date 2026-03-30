---
related:
  - title: File writing
    url: index.md
  - title: DefaultFormat and the default HDF5 layout
    url: default-format.md
---

# Async and Sync File Writing

BEC uses two complementary file-writing paths.

## Sync writing

The main master file is written by the normal file-writer path after the scan storage is ready.

Conceptually, this path:

- collects scan segments and baseline data in scan storage
- collects announced external file references
- assembles the final device and metadata structures
- writes the master `.h5` file through `HDF5FileWriter`

This is the path that uses `DefaultFormat` or a custom subclass of it.

## Async writing

Async device data is handled separately by `AsyncWriter`.

This writer listens to async device streams during the scan and writes their content incrementally into a temporary HDF5 file under `/entry/collection/devices`.

It supports multiple async update modes:

- `add`
- `add_slice`
- `replace`

The final master-file write can then append to the already opened file handle if async data was written first.

## Why there are two paths

The split exists because some device data is only available once the scan is complete, while other device data arrives continuously and needs to be written during the scan.

Using both paths allows BEC to:

- preserve a coherent master-file layout
- stream large or incremental async data efficiently
- publish file status updates while writing is still in progress

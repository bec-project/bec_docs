---
related:
  - title: Access Scan Data
    url: getting-started/next-steps/access-scan-data.md
  - title: Access BEC History
    url: how-to/scans/access-bec-history.md
  - title: Default HDF5 Layout
    url: learn/file-writer/default-format.md
---

# Open BEC HDF5 Files with h5py

!!! info "Overview"
    Open a BEC scan file with `h5py`, inspect its metadata and recorded datasets, and locate linked external files when present.

## Pre-requisites

- `h5py` is installed in the Python environment you are using.
- You know the path to the BEC HDF5 file you want to inspect.
- The file is readable from your current machine.

Start with the BEC master file, usually named like `S01234_master.h5`. That file contains the standard BEC structure and can reference additional detector files.

## 1. Find the scan file

If you just ran the scan, copy the file path from the `File:` line in the scan report.

If you want to inspect an older scan, retrieve it from history first:

```py
scan = bec.history[-1]
scan
```

Printing the scan container shows a summary that includes the file path.

## 2. Open the file with h5py

In Python, open the HDF5 file in read-only mode:

--[]->[]--test_snippet--test_how_to.py:test_h5py_open_root:Open the HDF5 file in read-only mode

For a standard BEC file, this usually starts with the top-level `entry` group.

## 3. Inspect the main BEC groups

The BEC-specific content is typically under `/entry/collection`.

--[]->[]--test_snippet--test_how_to.py:test_h5py_collection_keys:Inspect the main BEC groups

The groups that are usually most useful are:

- `metadata` for scan metadata
- `readout_groups` for recorded scan data grouped by readout priority
- `devices` for device-oriented access
- `file_references` for external file links

## 4. Read metadata and one dataset

To inspect metadata:

--[]->[]--test_snippet--test_how_to.py:test_h5py_metadata_keys:Inspect metadata keys

To read one dataset into memory:

--[]->[]--test_snippet--test_how_to.py:test_h5py_read_dataset:Read one dataset into memory

The exact path below `readout_groups` depends on the devices and signals recorded in your scan. In the HDF5 file, the standard group names are `monitored`, `baseline`, and `async`.

## 5. Explore the tree when you do not know the exact path

If you want to inspect the structure first, walk the file:

--[]->[]--test_snippet--test_how_to.py:test_h5py_visititems:Walk the HDF5 tree

This is useful when you know the file contains the data you need but do not yet know the exact dataset path.

## 6. Check external file references

If the scan includes detectors that write their own files, inspect `file_references`:

--[]->[]--test_snippet--test_how_to.py:test_h5py_file_references:Inspect file references

The master file is still the main entry point, but detector data can live in separate files linked from there.

!!! success "Congratulations!"
    You have successfully opened a BEC scan file with `h5py` and inspected the main metadata and data groups.

## Common pitfalls

- Opening a detector sidecar file and expecting the full BEC structure there.
- Hard-coding one dataset path and assuming every scan writes the same device and signal names.
- Forgetting to use `[...]` to read the dataset into memory, which can lead to unexpected behavior if you try to access it later after closing the file.
- Using `[...]` on a very large dataset without checking its shape first.
- Modifying the file accidentally by opening it in a writable mode instead of `"r"`.

## Next steps

- [Open BEC HDF5 Files with silx](open-bec-hdf5-files-with-silx.md){ data-preview }
- [Access BEC History](access-bec-history.md){ data-preview }
- [Default HDF5 Layout](../../learn/file-writer/default-format.md){ data-preview }

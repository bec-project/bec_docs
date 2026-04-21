---
related:
  - title: File writing
    url: learn/file-writer/where-files-are-written.md
  - title: Open BEC HDF5 files with h5py
    url: how-to/scans/open-bec-hdf5-files-with-h5py.md
  - title: Open BEC HDF5 files with silx
    url: how-to/scans/open-bec-hdf5-files-with-silx.md
---

# Access Scan Data

A guide to accessing scan data after acquisition. This guide assumes you are comfortable with [running a simple scan](../quick-start/04-run-your-first-scan.md){ data-preview } and observing the live data.

## Goal

Learn how to access the data from your scans after they have finished.

## Steps

## 0. Run a scan

For an intro to running scans, see the example linked above. We will use the scan from that example, but assign it to a variable in our console:
```python
    scan_report = scans.line_scan(dev.samx, -1, 1, steps=5, exp_time=0.1, relative=False)
```

## 1. Inspect the output from a scan you have just run

Having run the scan above, we can see inspect its status:

--[]->[]--test_snippet--test_next_steps.py:test_scan_report:Inspect the scan report


## 2. Inspect the latest scan from history

Fetch the most recent scan history entry:

--[]->[]--test_snippet--test_next_steps.py:test_scan_history_container_summary:Inspect the latest scan container

This gives you a handle to the scan data after execution.

!!! tip "Scan history is a list of all past scans"
    `bec.history` behaves like a normal Python list. Index `0` accesses the first stored scan, while negative indices such as `-1`
    access entries from the end, so `bec.history[-1]` gives you the most recent scan.

## 3. Read one signal from the stored result

For example, inspect the recorded motor values for `samx`:

This returns arrays of timestamps and values collected during the scan, which you can use for further analysis:

--[]->[]--test_snippet--test_next_steps.py:test_scan_history_signal_arrays:Read one signal from scan history

Each entry represents one sampled point from the scan, so history is not just a final snapshot. It preserves the full
recorded series for later plotting, fitting, or custom analysis workflows.

## 4. Access the stored data

For each scan, an HDF5 file is written containing all the recorded signals and additional metadata about the scan which
was run. It can be found in the `File: ` entry in the scan report, both for an active scan and one obtained from the
history. You can open this file with your preferred HDF5 viewer, or with `h5py` in Python. For an introduction to working with the BEC HDF5 file structure, see [Open BEC HDF5 files with h5py](../../how-to/scans/open-bec-hdf5-files-with-h5py.md){ data-preview } and [Open BEC HDF5 files with silx](../../how-to/scans/open-bec-hdf5-files-with-silx.md){ data-preview } for a GUI-based approach.


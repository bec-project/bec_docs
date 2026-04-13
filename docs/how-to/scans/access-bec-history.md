---
related:
  - title: File writing
    url: learn/file-writer/introduction.md
---

# Access BEC History

!!! Info "Overview"
    Retrieve previous scans from `bec.history` and inspect their metadata and data in a BEC client session.

## Pre-requisites
- You are connected to a running BEC client session.
- The scans you want to inspect are still available in the BEC history and their files are readable from your current machine.

`bec.history` keeps a local history of recent scans. In current BEC, this history is limited to the last 10 000 readable scans. Each lookup returns a `ScanDataContainer`, the same data container type you also get from scan reports.

The structure of this container is similar to the layout BEC writes under `entry/collection` in the HDF5 file. For example, `metadata` corresponds to `entry/collection/metadata`, and the device and readout access paths are built from `entry/collection/readout_groups`.

## 1. Check how many scans are available in history

In a BEC IPython session, run:

--[]->[]--test_snippet--test_how_to.py:test_history_len:Check the history length

This returns the number of scans currently available in the local history cache.

## 2. Find the scan data container

Depending on what information you already have, there are several ways to retrieve a `ScanDataContainer`.

/// tab | Most recent scan

To get the most recent scan:

--[]->[]--test_snippet--test_how_to.py:test_history_latest_scan:Get the most recent scan

Here the index is the offset in the history: `-1` is the last scan, `-2` is the second-to-last scan, and so on.

///
/// tab | Scan number

To get a scan by scan number:

--[]->[]--test_snippet--test_how_to.py:test_history_by_scan_number:Get a scan by scan number

If the scan number exists only once in the history, you get a single `ScanDataContainer`. If it appears multiple times, BEC returns a list of `ScanDataContainer` objects.

If you get a list, select one element first before accessing attributes such as `metadata`, `devices`, or `readout_groups`:

--[]->[]--test_snippet--test_how_to.py:test_history_select_first_scan_number_match:Select one result from several scan-number matches

///
/// tab | Scan ID

To get a scan by scan ID:

--[]->[]--test_snippet--test_how_to.py:test_history_by_scan_id:Get a scan by scan ID

This is useful when you already copied the scan ID from a report, log, or notebook.

///
/// tab | Several recent scans

To get several recent scans at once:

--[]->[]--test_snippet--test_how_to.py:test_history_recent_scans:Get several recent scans at once

This returns a list of `ScanDataContainer` objects.

As above, access `metadata` or device data on one scan container, for example `recent_scans[0]`, not on the list itself.
///

## 3. Inspect the scan container

Printing the container is often a good first check:

--[]->[]--test_snippet--test_how_to.py:test_history_print_scan_container:Print a scan container

This shows a compact summary such as scan ID, scan number, scan name, status, number of points, and the file path.

## 4. Access metadata and scan data

Once you have a scan object, you can inspect metadata:

--[]->[]--test_snippet--test_how_to.py:test_history_metadata_access:Inspect scan metadata

To read full monitored or baseline groups:

--[]->[]--test_snippet--test_how_to.py:test_history_readout_groups_access:Read monitored and baseline groups

To work with one device and all of its signals:

--[]->[]--test_snippet--test_how_to.py:test_history_device_access:Read one device from the scan container

To work with a single signal:

--[]->[]--test_snippet--test_how_to.py:test_history_signal_access:Read one signal from the scan container

`scan.devices` is convenient when you want to explore a device-oriented view. `scan.data` is useful when you already know the signal name and want to access it directly.

These access paths resemble the HDF5 structure written by the file writer: metadata is stored under `entry/collection/metadata`, while monitored and baseline device data are exposed from `entry/collection/readout_groups`.

!!! success "Congratulations!"
    You have successfully accessed previous scans through `bec.history`.

## Common pitfalls
- Requesting a scan number or scan ID that is not present in the current history cache.
- Expecting one result from `get_by_scan_number(...)` when multiple scans share the same scan number.
- Assuming the history contains every past scan. It only keeps a bounded set of recent readable scans.
- Trying to access file-backed data when the underlying HDF5 file is no longer readable on the current machine.

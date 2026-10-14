---
related:
  - title: Run your first scan
    url: getting-started/quick-start/04-run-your-first-scan.md
  - title: Access BEC history
    url: how-to/scans/access-bec-history.md
  - title: Open BEC HDF5 files with h5py
    url: how-to/scans/open-bec-hdf5-files-with-h5py.md
  - title: Open BEC HDF5 files with silx
    url: how-to/scans/open-bec-hdf5-files-with-silx.md
---

# Access scan data

!!! info "Goal"
    Retrieve the latest scan, read a recorded signal and its timestamps,
    and locate the saved HDF5 file.

## Before you start

Complete [Run your first scan](../quick-start/04-run-your-first-scan.md){ data-preview }.
Continue in the same BEC IPython session with the demo configuration loaded. The scan's
files must be readable from the machine running your client.

Use the `scan_report` from that tutorial. If you started a new session, run the same
five-point scan again:

```python
scan_report = scans.line_scan(
    dev.samx, -1, 1, steps=5, exp_time=0.1, relative=False
)
```

## 1. Get the last scan from history

Retrieve the most recent scan:

--[]->[]--test_snippet--test_next_steps.py:test_scan_history_container_summary:Inspect the last scan

`bec.history[-1]` selects the last entry in the client's history. It returns a
`ScanDataContainer`, whose summary shows the scan ID, five points, five monitored readouts,
and the master-file path for this example.

History contains recent scans whose files are accessible to your client. A newly completed
scan can take a moment to appear; if the history is empty or still shows the previous scan,
wait briefly and repeat the lookup.

!!! tip "Find a particular scan"
    Other clients can also submit scans, so the last entry may belong to another measurement.
    When you want the scan associated with your report, use its scan ID:

    ```python
    scan_id = scan_report.scan.scan_id
    scan = bec.history.get_by_scan_id(scan_id)
    ```

    If that scan has not appeared in history yet, the lookup returns `None`; wait briefly
    and repeat it.

## 2. Read the recorded motor signal

Read the `samx` signal from the `samx` device:

--[]->[]--test_snippet--test_next_steps.py:test_scan_history_signal_arrays:Read your recorded motor signal

The result contains `value` and `timestamp` arrays. For this scan, expect five values
close to `[-1, -0.5, 0, 0.5, 1]`, in measurement order, with a timestamp for each reading.
These are the recorded positions at each point, rather than only the motor's final position.
The first `samx` selects the device; the second selects its signal.

This container reads the saved data from the scan file. You can use the arrays for
plotting or further analysis.

## 3. Inspect the report and locate the saved file

You can also inspect the report retained from the scan call:

--[]->[]--test_snippet--test_next_steps.py:test_scan_report:Inspect the scan report

`Status: COMPLETED` describes the request, while `Status: closed` in the history container
describes the recorded scan.

Find the `File:` line in the report or container summary. It identifies the BEC master
HDF5 file for this scan. You have already read a signal through the container; to inspect
that file directly, follow
[Open BEC HDF5 files with h5py](../../how-to/scans/open-bec-hdf5-files-with-h5py.md){ data-preview }
or [Open BEC HDF5 files with silx](../../how-to/scans/open-bec-hdf5-files-with-silx.md){ data-preview }.

For other ways to retrieve earlier measurements, see
[Access BEC history](../../how-to/scans/access-bec-history.md){ data-preview }.

!!! success "What you have learned"
    You retrieved the last scan from history, learned how to select a scan by its ID,
    read recorded values and timestamps, and located its master HDF5 file.

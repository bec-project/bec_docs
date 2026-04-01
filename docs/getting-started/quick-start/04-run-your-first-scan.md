# Run your first scan

!!! Info "Goal"

    In this tutorial you will submit a simple line scan and inspect the result from history. By the end, you will have seen the
    core scan loop that underpins most everyday BEC operation.

## Before you start

Continue in the same session with the demo configuration loaded and the tutorial motor `samx` available.

!!! tip "TAB completion for scans"
    BEC provides tab completion for the full scan interface. Type `scans.` and press `TAB` to discover available scan
    commands and their names.

If you are not sure which parameters a scan expects, ask the IPython client directly with `?`:

```python
scans.line_scan?
```

That opens the scan docstring together with its signature and an **example** of use:

```python
• default@bec [4/19] ❯❯ scans.line_scan?
Signature:
scans.line_scan(
    *args,
    exp_time: float = 0,
    steps: int = None,
    relative: bool = False,
    burst_at_each_point: int = 1,
    **kwargs,
)
Docstring:
A line scan for one or more motors.

Args:
    *args (Device, float, float): pairs of device / start position / end position
    exp_time (float): exposure time in s. Default: 0
    steps (int): number of steps. Default: 10
    relative (bool): if True, the start and end positions are relative to the current position. Default: False
    burst_at_each_point (int): number of acquisition per point. Default: 1

Returns:
    ScanReport

Examples:
    >>> scans.line_scan(dev.motor1, -5, 5, dev.motor2, -5, 5, steps=10, exp_time=0.1, relative=True)
File:      ~/PSI/bec/bec_lib/bec_lib/scans.py
Type:      function
```

## 1. Submit a simple line scan

Run a short absolute line scan over `samx`:

```python
scans.line_scan(dev.samx, -1, 1, steps=5, exp_time=0.1, relative=False)
```

BEC shows a progress bar while the scan runs, together with a table of the monitored devices used during the scan.

## 2. Let the scan finish in the client

For this short tutorial scan, you can simply let the CLI report complete before moving on to the history view.

## 3. Inspect the latest scan from history

Fetch the most recent scan history entry:

--[]->[]--test_snippet--test_getting_started.py:test_scan_history_container_summary:Inspect the latest scan container

This gives you a handle to the scan data after execution.

!!! tip "Scan history is a list of all past scans"
    `bec.history` behaves like a normal Python list. Index `0` accesses the first stored scan, while negative indices such as `-1`
    access entries from the end, so `bec.history[-1]` gives you the most recent scan.

## 4. Read one signal from the stored result

For example, inspect the recorded motor values for `samx`:

This returns arrays of timestamps and values collected during the scan, which you can use for further analysis:

--[]->[]--test_snippet--test_getting_started.py:test_scan_history_signal_arrays:Read one signal from scan history

Each entry represents one sampled point from the scan, so history is not just a final snapshot. It preserves the full
recorded series for later plotting, fitting, or custom analysis workflows.

!!! success "What you have learned"

    You submitted a line scan, watched the live scan report in the client, and retrieved the latest result from `bec.history`.
    You also saw that scan history stores arrays of recorded values and timestamps, which makes it the starting point for later analysis or GUI workflows.

## Next step

Continue with [05 Create your first GUI](05-create-your-first-gui.md), where you will start using the companion Dock Area and
connect a few widgets to the same live BEC session from the GUI.

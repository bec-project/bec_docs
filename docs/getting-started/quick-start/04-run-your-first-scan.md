# Run Your First Scan

!!! Info "Goal"

    In this tutorial you will submit a simple line scan and observe the result.

## Before you start

Continue in the same session with the demo configuration loaded and the tutorial motor `samx` available.

!!! tip "Tab completion for scans"
    BEC provides tab completion for the full scan interface. Type `scans.` and press `TAB` to discover available scan
    commands and their names.

If you are not sure which parameters a scan expects, ask the IPython client directly with `?`:

```python
scans.line_scan?
```

This will display the scan documentation, including its signature and an **example** of use:

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

Run a short line scan over the simulated `samx` motor:

--[]->[]--test_snippet--test_quickstart.py:test_samx_line_scan:Run a line scan with the `samx` motor

<!-- TODO: link to learn about signals -->
This runs a scan where the `samx` motor is moved from the position `-1` to `1`, and all the 
"[monitored](../../learn/devices/readout-priority.md){ data-preview }" devices and signals in BEC are recorded at each of five points,
evenly spaced along this trajectory. For devices which expect an exposure time, `exp_time=0.1` indicates that they should
expose for `0.1` seconds. The keyword `relative` determines whether the start and end positions are relative to the
current motor position or absolute positions.

BEC shows a progress bar while the scan runs, together with a table of the monitored devices used during the scan.

## 2. Let the scan finish in the client

For this short tutorial scan, you can simply let the scan complete and observe the output in the console.

!!! success "What you have learned"

    You submitted a line scan, and observed the output in the BEC console.

## Next step

Continue with [05 Create your first GUI plot](05-create-your-first-gui.md){ data-preview }, where you will start using the Dock Area and draw a plot from a scan.

Alternatively, you can check out the more in-depth tutorial on [accessing your scan data](../next-steps/access-scan-data.md){ data-preview }.

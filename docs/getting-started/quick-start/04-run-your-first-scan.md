# Run your first scan

!!! info "Goal"
    Discover a scan, run it with a simulated motor, and keep the report that identifies
    your measurement.

## Before you start

Continue in the BEC IPython session from [Move a device](03-move-a-device.md), with the
demo configuration loaded and `dev.samx` available.

## 1. Discover the line scan

Type `scans.` and press ++tab++ to see the scans available from your running server.
For this exercise, inspect the line scan:

```python
scans.line_scan?
```

This displays the scan documentation, including its signature and **examples** of use.
For the built-in line scan, an abbreviated help display looks like this:

```text
Signature:
scans.line_scan(
    *args,
    steps: int,
    relative: bool,
    exp_time: float = 0,
    frames_per_trigger: int = 1,
    settling_time: float = 0,
    settling_time_after_trigger: float = 0,
    readout_time: float = 0,
    burst_at_each_point: int = 1,
)
Docstring:
A line scan for one or more motors.

Args:
    *args (device: DeviceBase, start: float, stop: float): repeated scan argument bundles.
    steps (int): steps.
    relative (bool): Whether the positions are relative to the current position.
    exp_time (float [s]): Exposure time in seconds. Default: 0 s
    ...

Returns:
    ScanReport

Examples:
    Minimum:
        >>> scans.line_scan(dev.device1, -1.0, 1.0, steps=10, relative=False)
    ...
```

Find `steps`, `exp_time`, and `relative`: we will set all three explicitly below.
Available scans and their defaults can differ between deployments, so use the help from
your own session.

## 2. Run a scan and keep its report

Run a short scan over the simulated `samx` motor, assigning the returned report to
`scan_report`:

--[]->[]--test_snippet--test_quickstart.py:test_samx_line_scan:Run a line scan with the `samx` motor

The motor visits five equally spaced positions: `-1`, `-0.5`, `0`, `0.5`, and `1`.
`relative=False` makes these absolute positions, independent of the motor's starting
position. `exp_time=0.1` requests a 0.1-second exposure from devices that use this setting.

At each position, BEC records the
[monitored devices](../../learn/devices/readout-priority.md){ data-preview }.
The client shows progress and a table of their readings. Simulated readbacks can differ
slightly from the requested positions, and detector values will vary between runs.

## 3. Identify your scan

The report belongs to this particular request. Inspect its scan ID:

```python
scan_report.scan.scan_id
```

Keep `scan_report` in your session. You will use it to find this measurement again in
[Access scan data](../next-steps/access-scan-data.md){ data-preview }.

## Next step

Continue with [05 Plot your first waveform](05-plot-your-first-waveform.md){ data-preview }
to plot scan data, or follow [Access scan data](../next-steps/access-scan-data.md){ data-preview }
to inspect the recorded values and find the saved file.

!!! success "What you have learned"
    You discovered a scan with IPython help, ran an absolute five-point measurement,
    and kept its report and scan ID for accessing the result.

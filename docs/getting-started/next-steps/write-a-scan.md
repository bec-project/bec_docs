---
related:
  - title: Scan lifecycle and authoring responsibilities
    url: learn/scans/scan-lifecycle.md
  - title: Scan development API
    url: references/bec-core/scan-base-and-stubs.md
  - title: Test a scan
    url: how-to/scans/test-a-scan.md
---

# Write an alternating-position scan

!!! info "Goal"
    Write a scan that measures alternately at two positions, make it available through
    your plugin using the scan generator, and verify its recorded values with a simulated
    motor.

## Before you start

Complete [Run your first scan](../quick-start/04-run-your-first-scan.md). Use a development
BEC installation with the demo configuration and a beamline plugin you can edit, installed
in editable mode in the scan server's Python environment. The generator requires exactly
one installed BEC plugin repository and the `black` and `isort` packages. You need basic
Python familiarity, including classes and methods.

The example package is `my_beamline`; substitute your plugin's package name in paths and
imports. The motor is the simulated `samx`. Read
[the scan lifecycle](../../learn/scans/scan-lifecycle.md) for background on the methods below.

## 1. Define the measurement

We want to measure at position A, then position B, and repeat this pair three times:

```text
A, B, A, B, A, B
```

That is six measured visits, even though there are only two distinct positions. Each visit
records its own data; the scan does not subtract or average the measurements.

## 2. Generate and implement the scan

Activate the Python environment containing your editable plugin, then run:

```bash
bec-plugin-manager create scan alternating_scan
```

The generator finds the installed plugin repository. Enter a description, select
`SOFTWARE_TRIGGERED`, and include the built-in arguments `relative` and `exp_time`.
Use the arrow keys to move through selections, space to toggle built-in arguments,
and enter to confirm. Choose to set up custom arguments, then add these in order:

| Argument name | Type | Units | Description |
| --- | --- | --- | --- |
| `motor` | `DeviceBase` | No units prompt | Motor to move |
| `position_a` | `float` | `None` | First position |
| `position_b` | `float` | `None` | Second position |
| `repeats` | `int` | `None` | Number of A/B pairs |

Answer yes to **Add another argument?** until you have entered `repeats`, then answer no.
The generator writes `my_beamline/scans/alternating_scan.py`, exports `AlternatingScan`
from the scans package, and formats both files. Its template includes the lifecycle hooks
and input metadata; you still need to implement the measurement.

Open the generated file. Keep its imports, class declaration, `gui_config`, input
assignments, and any plugin-specific components the generator selected. The next steps
fill in the measurement and recovery logic in that class.

### Configure inputs and readouts

The generator knows the input types and descriptions, but it does not know that A and B
are motor positions or that a scan needs at least one pair. Add `reference_units="motor"`
to associate both position inputs with the selected motor's units, and `gt=0` so input
validation rejects zero or negative repeat counts. These annotations describe the inputs;
they do not move the motor or convert relative offsets into absolute targets.

In the generated `__init__` signature, update those three annotations as follows,
preserving their labels and descriptions. Keep the other parameters as generated:

```python
position_a: Annotated[
    float,
    ScanArgument(
        display_name="Position A",
        description="First position",
        reference_units="motor",
    ),
],
position_b: Annotated[
    float,
    ScanArgument(
        display_name="Position B",
        description="Second position",
        reference_units="motor",
    ),
],
repeats: Annotated[
    int,
    ScanArgument(display_name="Repeats", description="Number of A/B pairs", gt=0),
],
```

The generated constructor already stores the inputs and passes `relative` and `exp_time`
into `update_scan_info`. We also want the progress display to identify the scanned motor
and every measurement to include its position. `scan_report_devices` selects it for scan
reporting; monitored readout priority includes it in each acquisition's readings.

Add these readout settings at the end of the constructor:

```python
self.update_scan_info(scan_report_devices=self.motors)
self.actions.set_device_readout_priority(self.motors, priority="monitored")
```

This completes the template's TODOs for scan-report devices and monitored motor readouts.
These operations configure scan metadata. Actual device operations belong in
the hooks because the constructor can run before the queued scan starts.

### Prepare the trajectory

The template leaves trajectory generation as a TODO. Our scan needs a row for every visit:
`np.tile` repeats A/B in acquisition order, and `reshape(-1, 1)` makes one motor column.
For three pairs that is six rows, including the repeated positions.

Resolve relative offsets during preparation using the motor's position when the queued
scan begins. Save that position for the return move, then check the resulting absolute
targets against motor limits before any scan motion. Publish the trajectory and counts
before opening so progress reporting and data collection know what to expect. We read once
per visit, so both counts equal the number of rows.

Replace the generated `prepare_scan` method with:

```python
@scan_hook
def prepare_scan(self):
    self.positions = np.tile([self.position_a, self.position_b], self.repeats)
    self.positions = self.positions.astype(float).reshape(-1, 1)
    if self.relative:
        self.start_positions = self.components.get_start_positions(self.motors)
        self.positions += self.start_positions
    self.components.check_limits(self.motors, self.positions)
    count = len(self.positions)
    self.update_scan_info(
        positions=self.positions,
        num_points=count,
        num_monitored_readouts=count,
    )
    self.actions.add_scan_report_instruction_scan_progress(points=count, show_table=True)
    self._baseline_readout_status = self.actions.read_baseline_devices(wait=False)
```

Indent this method and the following methods inside `AlternatingScan`, as in the generated
file. `show_table=True` lets you see the alternating motor readings during the run.
Keep the asynchronous baseline read: it collects the baseline devices separately from
our six monitored readings, and the generated `close_scan` waits for it to finish.

### Implement acquisition

Preparing positions only describes the scan; the generated `scan_core` still has no
acquisition loop. Use `step_scan` to visit the rows in order. It calls `at_each_point` for
each visit, so that hook needs arguments for the motors, target row, and previous position.
The standard per-point component moves and waits before triggering and reading, ensuring
the measurement belongs to the requested position.

Keep the `@scan_hook` decorators so scan modifiers can extend these hooks. Fill in the
generated `scan_core` and `at_each_point` methods:

```python
@scan_hook
def scan_core(self):
    self.components.step_scan(self.motors, self.positions, at_each_point=self.at_each_point)

@scan_hook
def at_each_point(self, motors, positions, last_positions=None):
    self.components.step_scan_at_each_point(motors, positions, last_positions=last_positions)
```

The loop requests one acquisition at each row. Its six reads must match the six monitored
readouts declared during preparation; setting the count alone would not collect data.

### Complete the recovery hooks

For this example, a relative scan should return to the position from which its offsets
were measured; an absolute scan should finish at B. Both normal completion and exception
recovery need the same return operation. The helper checks that the scan is relative and
a starting position was captured. These checks avoid a return move for an absolute scan
or when preparation failed before reading the initial position.

Add this helper in the generated helper-method section:

```python
def _return_to_start(self):
    if self.relative and self.start_positions:
        self.components.move_and_wait(self.motors, self.start_positions)
```

The generated `post_scan` completes devices. Add the return after that completion so the
motor moves back after acquisition has finished. Fill in `on_exception` too: a failed scan
skips the remaining normal hooks, so recovery must attempt both the return and unstaging.
Use `finally` to attempt unstaging even if the return move also fails.

Update `post_scan` and fill in `on_exception`:

```python
@scan_hook
def post_scan(self):
    self.actions.complete_all_devices()
    self._return_to_start()

@scan_hook
def on_exception(self, exception):
    try:
        self._return_to_start()
    finally:
        self.unstage()
```

Keep the generated `open_scan`, `stage`, `pre_scan`, `unstage`, and `close_scan` methods.
They handle opening, device setup and release, baseline completion, and closing status
checks.

An interruption that skips the exception hook does not perform this cleanup.
Device-specific settings or hardware-triggered acquisition would need additional recovery
logic; see [the lifecycle explanation](../../learn/scans/scan-lifecycle.md#failure-and-interruption)
for those responsibilities.

## 3. Reload and inspect the scan

From the BEC IPython client, request a scan reload:

```python
bec._request_scan_reload()
```

This is currently an internal client helper. The reload request is asynchronous: when
`alternating_scan` appears in `scans.` completion, inspect its published interface:

```python
scans.alternating_scan?
```

You should see `motor`, `position_a`, `position_b`, required `repeats` and `relative`,
and `exp_time` with the generated default `0`. If the name is absent, check the server's
plugin installation, package export, and logs for import errors or duplicate scan names.

## 4. Run with the simulated motor

In the demo session, submit three pairs at absolute positions -0.5 and 0.5:

```python
scan_report = scans.alternating_scan(
    dev.samx, -0.5, 0.5, repeats=3, relative=False, exp_time=0.1,
)
```

Let the blocking progress display finish. It should show six readings, alternating
between values near -0.5 and 0.5. Inspect the readings that reached the client:

```python
scan_report.scan.live_data["samx"]["samx"].val
```

Expect values close to:

```text
[-0.5, 0.5, -0.5, 0.5, -0.5, 0.5]
```

The motor finishes near 0.5 because this run is absolute. Inspect it with `dev.samx.read()`.
Use [Access scan data](access-scan-data.md) to inspect the saved result and master file.

## 5. Check relative coordinates

Move the simulated motor to 1, then repeat using offsets:

```python
scans.umv(dev.samx, 1, relative=False)
relative_report = scans.alternating_scan(
    dev.samx, -0.5, 0.5, repeats=3, relative=True, exp_time=0.1,
)
relative_report.scan.live_data["samx"]["samx"].val
```

The readings should now alternate near 0.5 and 1.5. After the scan completes, the motor
should be back near 1. This verifies both the coordinate offset and the return behavior.

## Next step

Follow [Test a scan](../../how-to/scans/test-a-scan.md) to keep these measurement and cleanup
checks in your plugin's tests. Keep the
[scan development API](../../references/bec-core/scan-base-and-stubs.md) nearby when changing
individual operations.

!!! success "What you have learned"
    You generated and implemented a scan, inspected its client interface, and
    verified six alternating measurements in absolute and relative coordinates with a
    simulated motor.

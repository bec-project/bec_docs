---
related:
  - title: set() vs put() in ophyd
    url: learn/devices/set-vs-put.md
  - title: EPICS Signal Variants
    url: learn/devices/epics-signals.md
---

# EPICS put completion

`EpicsSignal` supports EPICS put completion, which means EPICS reports back when the write request itself has completed.

This is an EPICS-specific detail that matters because it changes how `set()` decides that a write is finished.

## Configuring `put_complete`

The relevant option is `put_complete`, which is configured on the signal definition. The default value is `False`.

```python
from ophyd import Component as Cpt, Device, EpicsSignal


class MyDevice(Device):
    my_signal = Cpt(EpicsSignal, "PV:NAME", put_complete=True)
```

## How it changes `set()`

For `EpicsSignal.set()`, `put_complete` changes the completion condition:

<table>
  <colgroup>
    <col style="width: 22%;">
    <col style="width: 48%;">
    <col style="width: 30%;">
  </colgroup>
  <thead>
    <tr>
      <th>Configuration</th>
      <th>Completion behavior</th>
      <th>What the caller gets</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>put_complete=False</code></td>
      <td><code>set()</code> writes the value, then waits until the readback reaches the target.</td>
      <td>A <code>Status</code> that completes when the readback matches.</td>
    </tr>
    <tr>
      <td><code>put_complete=True</code></td>
      <td><code>set()</code> calls <code>put(..., use_complete=True)</code> internally and finishes when EPICS reports put completion.</td>
      <td>A <code>Status</code> that completes on EPICS put completion.</td>
    </tr>
  </tbody>
</table>

!!! info "How `put_complete` changes `set()`"
    - `put_complete=False`: "wait until the signal value reaches the requested target"
    - `put_complete=True`: "wait until EPICS says the write request has completed"

This can be useful for EPICS signals where the EPICS put-completion callback is the right completion signal for the write.

## What it does not change

`put_complete` changes how `set()` finishes, but it does not change the role of `put()`.

Even when `put_complete=True` is enabled on the signal:

- `put()` still performs a direct write
- `put()` still returns immediately
- `put()` still does not return a `Status`

That is why `set()` remains the normal ophyd API when the caller needs structured completion tracking.

!!! info "What to remember"
    - `put_complete` is an `EpicsSignal` option that changes how `set()` decides the write is finished.
    - With `put_complete=False`, `set()` waits for the readback to reach the target.
    - With `put_complete=True`, `set()` finishes when EPICS reports put completion.
    - `put_complete` does not turn `put()` into a completion-tracked API: `put()` still writes directly and returns immediately.

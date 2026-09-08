---
related:
  - title: Introduction to ophyd
    url: learn/devices/introduction-to-ophyd.md
  - title: Change Config Signals from the BEC IPython Client
    url: how-to/devices/change-config-signals-from-the-bec-ipython-client.md
  - title: EPICS put completion
    url: learn/devices/epics-put-completion.md
---

# `set()` vs `put()` in `ophyd`

In ophyd, both `set()` and `put()` can write a new value to a writable signal, but they serve different purposes.

The short version is:

- use `put()` for a direct low-level write
- use `set()` when you want a write operation with completion tracking

That distinction matters in BEC because user-facing device operations often need clear completion semantics, while device-internal helper signals often just need to publish a new value immediately.

## What `put()` does

`put()` is the low-level write method on a signal.

It sends a value to the signal and returns immediately. It does not return a `Status` object and is therefore not the right abstraction when the caller needs to wait for completion in a structured way.

`put()` is a direct wrapper around the underlying control layer, i.e. in the case of pyepics (default for ophyd_devices), it is calling `epics.PV.put()`. 

Typical uses of `put()` include:

- updating a soft signal inside device implementation code
- writing trigger-like signals that should be pushed directly
- direct signal writes where completion tracking is not needed or not meaningful

Example:

```python
my_signal.put(5)
```

## What `set()` does

`set()` is the higher-level write method.

It starts a write operation and returns a `Status` object that tells the caller when the operation is considered complete or has failed. This makes `set()` a better fit for coordinated device actions, plans, and user-facing control flows.

Example:

```python
status = my_signal.set(5)
status.wait()
```

In other words, `set()` is not just about sending a value. It is about sending a value and giving the caller a standard way to observe completion.
Under the hood, `set()` uses `put()` to perform the actual write, but it adds the completion tracking layer on top. 

## The practical difference

The key difference is the API contract:

<table>
  <colgroup>
    <col style="width: 20%;">
    <col style="width: 80%;">
  </colgroup>
  <thead>
    <tr>
      <th>Method</th>
      <th>Behavior</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap;"><code>put()</code></td>
      <td>Perform a direct write. No <code>Status</code> object is returned.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>set()</code></td>
      <td>Perform a write operation with completion tracking and return a <code>Status</code>.</td>
    </tr>
  </tbody>
</table>

That means the choice is usually driven by what the caller needs:

- If you only need to publish or write a value, `put()` is often enough.
- If the caller needs to wait until the operation is done, use `set()`.

## How `set()` decides it is done

For a basic ophyd `Signal`, `set()` uses the lower-level write path and then waits until the signal readback reaches the target value within the configured tolerances.

This is why `set()` is often described as a write-and-wait operation rather than just a write.

For `EpicsSignal`, there is one extra detail worth knowing: `put_complete` changes how `set()` decides that the write has finished. That EPICS-specific behavior is covered separately in [EPICS put completion](../../learn/devices/epics-put-completion.md).


## Choosing between them

In practice, the choice is simple:

- use `put()` when you only need to write a value
- use `set()` when the caller needs a `Status` and clear completion semantics

!!! info "What to remember"
    - `put()` is the low-level write method for directly updating a signal value.
    - `set()` is the higher-level write method that returns a `Status` so callers can wait for completion.
    - For a basic ophyd `Signal`, `set()` writes the value and waits until the readback reaches the target.
    - If you are working with `EpicsSignal`, `put_complete` adds EPICS-specific completion behavior for `set()`.

---
related:
  - title: The Data API
    url: learn/data-api/index.md
  - title: Subscriptions and Updates
    url: learn/data-api/subscriptions-and-updates.md
  - title: Read Scan History with the Data API
    url: how-to/scans/read-scan-history-with-the-data-api.md
---

# Subscribe to Live Data with the Data API

!!! Info "Overview"
    Receive aligned, columnar scan data from a running BEC as it is produced — from a script, a
    service, or any non-GUI consumer.

## Prerequisites

- A running BEC deployment and a started `BECClient` (in the BEC IPython client, `bec` is that
  client).
- The device and signal names you want to follow.

!!! learn "[Learn how subscriptions and updates work](../../learn/data-api/subscriptions-and-updates.md){ data-preview }"

## 1. Define a callback

The callback receives one immutable snapshot per delivery. It may be called from a background
thread, so keep it self-contained and fast.

```python
def on_update(update):
    if update.reason == "rebind":
        print(f"now following scan {update.scan_id}")
    cols = update.aligned()
    x = cols[("samx", "samx")]
    y = cols[("bpm4i", "bpm4i")]
    print(f"{update.scan_id}: {len(x)} aligned points, complete={update.complete}")
```

## 2. Subscribe with `scan="live"`

```python
subscription = bec.data_api.subscribe(
    sources=[("samx", "samx"), ("bpm4i", "bpm4i")],
    scan="live",
    callback=on_update,
    min_emit_interval=0.1,
)
```

If a scan is already running, the first delivery is a `"backfill"` snapshot with everything
recorded so far; afterwards coalesced `"live"` updates follow. When the next scan starts, the
subscription re-binds automatically and emits `"rebind"`.

## 3. Include async detector data

Async signals are declared the same way; the Data API joins them with the monitored signals by
ordinal when the device declares the `"monitored"` acquisition group:

```python
subscription = bec.data_api.subscribe(
    sources=[("samx", "samx"), ("waveform", "waveform_waveform")],
    scan="live",
    callback=on_update,
)
```

## 4. Subscribe to device streams without a scan

Pass `scan=None` for scan-independent streams — readbacks, `"monitor_1d"` monitors, and preview
signals. Cap the retention for these endless streams:

```python
subscription = bec.data_api.subscribe(
    sources=[("waveform", "monitor_1d")],
    scan=None,
    callback=on_update,
    max_points=1000,
)
```

## 5. Close the subscription

```python
subscription.close()
```

Subscriptions also work as context managers for scoped use:

```python
with bec.data_api.subscribe(sources=[("samx", "samx")], scan="live", callback=on_update):
    bec.scans.line_scan(dev.samx, -5, 5, steps=100, exp_time=0.1, relative=False)
```

!!! note "Sources that are not available yet"
    `subscription.unbound_sources` lists declared sources that no plugin currently delivers, for
    example a device whose signal info has not settled. They are retried automatically on the next
    scan status update.

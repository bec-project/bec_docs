---
related:
  - title: Access BEC History
    url: how-to/scans/access-bec-history.md
  - title: Subscribe to Live Data with the Data API
    url: how-to/scans/subscribe-to-live-data-with-the-data-api.md
  - title: Data Source Plugins and Scan Lifecycle
    url: learn/data-api/plugins-and-lifecycle.md
---

# Read Scan History with the Data API

!!! Info "Overview"
    Load a finished scan's data in the same aligned, columnar form the live path delivers — with
    an up-front size estimate for large datasets.

## Prerequisites

- A running BEC deployment and a started `BECClient`.
- The scan id of a finished scan (for example from `bec.history`).

!!! learn "[Learn how history serving fits the scan lifecycle](../../learn/data-api/plugins-and-lifecycle.md){ data-preview }"

## 1. Subscribe with a concrete scan id

```python
scan_id = bec.history[-1].metadata.bec.scan_id

updates = []
subscription = bec.data_api.subscribe(
    sources=[("samx", "samx"), ("bpm4i", "bpm4i")],
    scan=scan_id,
    callback=updates.append,
)
```

The read runs on a worker thread; the callback receives one `"history"` snapshot when it
completes. An *open* scan id is served live instead and re-routes to history when it finishes —
the code path is the same.

## 2. Guard against very large datasets

Pass `size_limit_bytes` to arm the size gate. When the estimated payload exceeds the limit,
nothing is read until you confirm:

```python
subscription = bec.data_api.subscribe(
    sources=[("waveform", "waveform_waveform")],
    scan=scan_id,
    callback=updates.append,
    size_limit_bytes=10 * 1024**2,  # 10 MB
)

if subscription.size_gated:
    print(f"estimated {subscription.estimated_bytes / 1024**2:.1f} MB")
    subscription.confirm_size()  # explicitly load anyway
```

You can also ask for the estimate without subscribing:

```python
estimate = bec.data_api.estimate_bytes([("waveform", "waveform_waveform")], scan_id)
```

## 3. Follow the progress of a large read

A big scan is read from the file in slabs on a worker thread. Pass `progress_callback` to see how
far it has come — the fraction runs from 0 to 1 and reaches 1.0 once, just before the update is
delivered:

```python
subscription = bec.data_api.subscribe(
    sources=[("waveform", "waveform_waveform")],
    scan=scan_id,
    callback=updates.append,
    progress_callback=lambda fraction: print(f"\rloading {fraction:.0%}", end=""),
)
```

The callback runs on the reading thread, so keep it cheap and never touch GUI objects from it —
widgets use the bridge's `progress` signal for that.

## 4. Use the columns

```python
update = updates[-1]
cols = update.aligned()
x = cols[("samx", "samx")]
y = cols[("bpm4i", "bpm4i")]
```

The columns are identical to what a live subscription would have accumulated over the scan — the
history snapshot is the authoritative end state of the same contract.

!!! note "When history is enough"
    For interactive exploration of finished scans, [`bec.history`](access-bec-history.md) or the
    [HDF5 file](open-bec-hdf5-files-with-h5py.md) may be simpler. Use the Data API when the same
    code must serve live and historic data, or when you want the aligned columnar form.

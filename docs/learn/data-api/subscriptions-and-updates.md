---
related:
  - title: The Data API
    url: learn/data-api/index.md
  - title: Ordinal Alignment
    url: learn/data-api/ordinal-alignment.md
  - title: Data Source Plugins and Scan Lifecycle
    url: learn/data-api/plugins-and-lifecycle.md
  - title: Data API Reference
    url: references/bec-core/data-api.md
---

# Subscriptions and Updates

A *subscription* is the unit of data access in the Data API: one declared set of sources, bound to
one scan scope, delivering a stream of immutable snapshots to one callback.

## Creating a subscription

```python
subscription = client.data_api.subscribe(
    sources=[("samx", "samx"), ("bpm4i", "bpm4i")],
    scan="live",
    callback=on_update,
    min_emit_interval=0.1,
)
```

- `sources` is a list of `(device, entry)` pairs. The entry is the signal name as it appears in
  the device's data — the same names used in scan segments and async signals.
- `scan` selects the scope:
    - `"live"` follows the currently active scan and every scan that starts afterwards,
    - a concrete scan id serves exactly that scan — an open scan is served live, a finished scan
      from the scan history,
    - `None` subscribes to scan-independent device streams (readbacks, `"monitor_1d"` monitors,
      preview signals).
- `callback` receives each update. It may be invoked from background threads — see the
  [threading notes](plugins-and-lifecycle.md#threading-model).

The subscription stays active until `close()` is called (or the object is garbage collected); it
also supports the context-manager protocol.

## The update: a full-state columnar snapshot

Every delivery is a `SubscriptionUpdate` carrying the *complete current state* of the
subscription's sources — not a delta. Consumers therefore never need to accumulate data
themselves; rendering the newest update always produces the correct picture, and skipping an
intermediate update loses nothing.

```python
def on_update(update):
    cols = update.aligned()           # equal-length columns, one per source
    x = cols[("samx", "samx")]
    y = cols[("bpm4i", "bpm4i")]
```

The important fields:

| Field / method       | Meaning                                                                     |
|----------------------|-----------------------------------------------------------------------------|
| `update.scan_id`     | The scan this snapshot belongs to.                                          |
| `update.reason`      | Why it was emitted: `"live"`, `"backfill"`, `"history"`, or `"rebind"`.     |
| `update.sources`     | Mapping of `(device, entry)` to a per-source `SourceData` snapshot.         |
| `update.aligned()`   | Equal-length value columns restricted to ordinals present in every source.  |
| `update.axis(mode)`  | An x-axis column parallel to `aligned()`: `"index"`, `"timestamp"`, or `"device"`. |
| `update.complete`    | `True` when no source has known gaps and all sources reached the same frontier. |

`aligned()` and `axis()` are memoized on the immutable snapshot, so calling them repeatedly is
free.

### Column types

A column is a *sequence*, not necessarily a tuple. Live data accumulates point by point and is
delivered as tuples, while a file-backed history read hands the file's arrays through untouched —
`values`, `timestamps` and the columns from `aligned()` are then `numpy.ndarray`. Keeping the
arrays intact is what makes a multi-million-point history load cheap: converting such a column to
Python objects and back costs seconds, on the thread that is trying to draw it.

Consumers must therefore accept either type, which mainly means never testing a column for
truthiness:

```python
if values is None or len(values) == 0:   # correct for tuples and arrays alike
    return
if not values:                           # WRONG: ValueError on a multi-element array
    return
```

`np.asarray(column)` is a no-op when the column already is an array, so rendering code can call it
unconditionally.

### Update reasons

- `"backfill"` — the initial delivery after subscribing, containing everything already recorded
  for the bound scan.
- `"live"` — new points arrived while the scan is running.
- `"rebind"` — the subscription switched scans (a new scan started under `scan="live"`) or its
  source set changed; consumers should reset any per-scan display state.
- `"history"` — the bound scan finished and the snapshot now comes from the authoritative scan
  history.

## Emission coalescing

Live messages can arrive far faster than a consumer can usefully process them. The subscription
coalesces emissions: at most one update per `min_emit_interval` seconds is delivered, and a
trailing emission flushes the final state after a burst. Because updates are full snapshots,
coalescing is lossless — the last update of a burst contains everything.

The interval can be changed at runtime with `subscription.set_min_emit_interval(seconds)`; BEC
Widgets exposes this per widget through the
[`update_rate` property](../../how-to/gui/build-a-widget-on-the-data-api.md).

Non-live emissions (backfill, history, rebind) bypass the rate limit — they are one-shot
deliveries, not streams.

## Bounding memory and load

- `max_points` caps the per-source retention; the oldest points are dropped beyond it. This is
  recommended for endless device streams (`scan=None`), which have no natural end.
- `size_limit_bytes` arms the [size gate](plugins-and-lifecycle.md#the-size-gate): when the
  serving plugin can estimate the payload up front (history scans), a subscription whose estimate
  exceeds the limit withholds the load until `confirm_size()` is called. Nothing is read in the
  meantime.
- `progress_callback` reports how far a history read has come, as a fraction from 0 to 1. Large
  datasets are read from the file in slabs rather than in one call, so the fraction advances
  during the read and reaches 1.0 exactly once, when the update is about to be delivered. The
  callback runs on the reading worker thread; Qt consumers use the
  [bridge's `progress` signal](../../how-to/gui/build-a-widget-on-the-data-api.md) instead, which
  marshals it onto the GUI thread.

!!! info "What to remember"
    - One subscription = one source set, one scan scope, one callback.
    - Every update is an immutable **full-state** snapshot; dropping intermediate updates is safe
      by design.
    - `aligned()` gives equal-length columns; `axis()` resolves the x-axis — consumers do not
      trim, pair, or buffer data themselves.
    - Columns are tuples for live data and numpy arrays for history reads: length-check them,
      never test them for truthiness.
    - `reason` tells the consumer whether to append (`"live"`) or rebuild (`"backfill"`,
      `"history"`, `"rebind"`).
    - Coalescing bounds the update rate without losing data; `max_points` and the size gate bound
      memory, and `progress_callback` reports how a large read is advancing.

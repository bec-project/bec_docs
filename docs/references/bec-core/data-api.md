---
related:
  - title: The Data API
    url: learn/data-api/index.md
  - title: Subscriptions and Updates
    url: learn/data-api/subscriptions-and-updates.md
  - title: Subscribe to Live Data with the Data API
    url: how-to/scans/subscribe-to-live-data-with-the-data-api.md
---

# Data API Reference

This page lists the public Data API surface in `bec_lib.data_api`. The entry point is the lazily
created `client.data_api` facade.

## `DataAPI`

| API                                     | Use                                                                 |
|-----------------------------------------|---------------------------------------------------------------------|
| `client.data_api`                       | Per-client facade; created on first access.                         |
| `data_api.subscribe(...)`               | Create a subscription (see parameters below).                       |
| `data_api.estimate_bytes(sources, scan)`| Estimate a scan's payload size without reading it; `None` if unknown. |

### `subscribe` parameters

| Parameter           | Meaning                                                                                    |
|---------------------|--------------------------------------------------------------------------------------------|
| `sources`           | List of `(device, entry)` pairs.                                                           |
| `scan`              | `"live"` to follow the active scan, a concrete scan id, or `None` for device streams.      |
| `callback`          | Called with each `SubscriptionUpdate`; may run on background threads.                      |
| `min_emit_interval` | Live-emission coalescing interval in seconds (default `0.1`; `0` disables coalescing).     |
| `max_points`        | Per-source retention cap; oldest points dropped beyond it.                                 |
| `size_limit_bytes`  | Arm the size gate: withhold loads whose up-front estimate exceeds the limit.               |

Raises `ValueError` when a concrete scan id cannot be served and `CorrelationGroupError` when the
source list is empty.

## `Subscription`

| API                                  | Use                                                                    |
|--------------------------------------|------------------------------------------------------------------------|
| `subscription.scan_id`               | Currently bound scan id.                                               |
| `subscription.sources`               | Declared source set.                                                   |
| `subscription.unbound_sources`       | Declared sources not currently delivering (retried automatically).     |
| `subscription.set_sources(sources)`  | Atomically replace the source set.                                     |
| `subscription.min_emit_interval`     | Current coalescing interval in seconds.                                |
| `subscription.set_min_emit_interval(s)` | Change the coalescing interval at runtime.                          |
| `subscription.size_gated`            | Whether delivery is withheld pending `confirm_size()`.                 |
| `subscription.estimated_bytes`       | Up-front payload estimate of the bound scan, if known.                 |
| `subscription.confirm_size()`        | Load a size-gated subscription.                                        |
| `subscription.close()`               | Release all resources (also available as a context manager).           |

## `SubscriptionUpdate`

| API                          | Use                                                                            |
|------------------------------|--------------------------------------------------------------------------------|
| `update.scan_id`             | Scan the snapshot belongs to.                                                  |
| `update.reason`              | `"live"`, `"backfill"`, `"history"`, or `"rebind"`.                            |
| `update.sources`             | Mapping `(device, entry)` → `SourceData` snapshot.                             |
| `update.aligned()`           | Equal-length value columns at the ordinals present in every source (memoized). |
| `update.aligned_ordinals`    | The ordinals of the aligned columns.                                           |
| `update.axis(mode, source)`  | X-axis column: `"index"`, `"timestamp"`, or `"device"`.                        |
| `update.get(device, entry)`  | One source's snapshot, or `None`.                                              |
| `update.complete`            | `True` when no source has gaps and all share one frontier.                     |
| `update.aligned_contiguous`  | `True` when the aligned ordinals are the contiguous range `0..n-1`.            |
| `update.metadata`            | Group label, lagging sources, and plugin-specific extras.                      |

## `SourceData`

| Field               | Meaning                                                        |
|---------------------|----------------------------------------------------------------|
| `device`, `entry`   | Source identity.                                               |
| `kind`              | `"monitored"`, `"async"`, or `"unindexed"`.                    |
| `ordinals`          | Correlation keys of the stored points (sorted).                |
| `values`, `timestamps` | Columns parallel to `ordinals`; tuples for live data, `numpy.ndarray` for file-backed history reads. |
| `complete`          | Whether ordinals 0..frontier are all present.                  |
| `metadata`          | Async update type, acquisition group, max shape, and similar.  |

## `QtDataSubscription` (BEC Widgets)

| API                                   | Use                                                                 |
|---------------------------------------|---------------------------------------------------------------------|
| `QtDataSubscription(client, sources, scan, parent, ...)` | Subscribe and deliver updates on the Qt thread. |
| `bridge.updated`                      | Qt signal emitting each `SubscriptionUpdate`.                       |
| `bridge.scan_id`, `bridge.sources`    | Pass-throughs to the underlying subscription.                       |
| `bridge.healthy`                      | `False` while any declared source is not delivering.                |
| `bridge.size_gated`, `bridge.estimated_bytes`, `bridge.confirm_size()` | Size-gate pass-throughs.           |
| `bridge.set_min_emit_interval(s)`     | Change the coalescing interval at runtime.                          |
| `bridge.close()`                      | Close; also triggered by the Qt parent's destruction.               |

Widgets deriving from `PlotBase` additionally expose the `update_rate` property (Hz, 1–100),
which applies to every bridge of the widget.

---
related:
  - title: Subscriptions and Updates
    url: learn/data-api/subscriptions-and-updates.md
  - title: The Data API
    url: learn/data-api/index.md
  - title: Data Flow
    url: learn/system-architecture/overview/data-flow.md
  - title: Access BEC History
    url: how-to/scans/access-bec-history.md
---

# Data Source Plugins and Scan Lifecycle

Underneath the uniform subscription contract, the Data API routes each subscription to one of
several **data source plugins**. This page explains that routing, the life of a live-follow
subscription, and the rules that keep the whole machinery thread-safe.

## The plugin architecture

A plugin owns one way of producing data. Three ship with BEC:

| Plugin               | Priority | Serves                                                                 |
|----------------------|---------:|------------------------------------------------------------------------|
| Live plugin          |       10 | The currently running (or otherwise open) scan: scan segments for `monitored` sources, async signal streams, legacy async readbacks. |
| History plugin       |       50 | Finished scans, read from the scan history and the scan's HDF5 file on a worker thread. |
| Device-stream plugin |       90 | Scan-independent streams (`scan=None`): device readbacks, `"monitor_1d"` monitors, preview signals. |

When a subscription binds to a scan, the plugins are consulted in ascending priority order; the
first plugin that *claims* the scan serves all of its sources. Individual sources may still
resolve as unavailable (for example a device whose info has not settled yet) — these are reported
through `subscription.unbound_sources` and retried on the next scan status update rather than
failing the subscription.

## Life of a live-follow subscription

A subscription created with `scan="live"` moves through a well-defined lifecycle:

1. **Bind and backfill.** If a scan is already running, the live plugin claims it and immediately
   delivers a `"backfill"` snapshot containing every point recorded so far. Subscribing mid-scan
   therefore never misses data.
2. **Live delivery.** New scan segments and async messages extend the columns; coalesced
   `"live"` updates flow to the callback.
3. **Scan change.** When a new scan opens, the subscription re-binds to it and emits a
   `"rebind"` snapshot — the consumer's cue to reset per-scan state.
4. **Terminal flush.** When the scan reaches a terminal state, the live state is flushed one last
   time.
5. **Re-route to history.** Once the finished scan appears in the scan history, the subscription
   re-binds to the history plugin and delivers an authoritative `"history"` snapshot. The data a
   consumer ends up holding is identical to what a later history read would return.

Subscriptions bound to a concrete scan id follow the same path from whichever stage the scan is
in: an open scan is served live (including the re-route at the end), a finished one directly from
history.

## The size gate

History reads have a knowable cost: the history plugin can estimate the payload size of a scan
before reading anything. A subscription created with `size_limit_bytes` compares that estimate
against the limit; when it exceeds the limit, the subscription reports `size_gated=True` together
with `estimated_bytes`, and **no data is read** until the consumer calls `confirm_size()`. BEC
Widgets uses this to ask the user before loading very large datasets into a plot. Live scans have
no up-front estimate and are never gated.

## Threading model

The Data API is a multithreaded component, and its rules matter to anyone extending it:

- **Callbacks may run off the GUI thread.** Live updates are delivered from dispatcher threads,
  history reads from a worker thread. Qt consumers must marshal updates onto the Qt main thread —
  BEC Widgets' `QtDataSubscription` does exactly this and is the recommended integration point
  for widgets.
- **History reads never block the caller.** Opening a history-served subscription starts a worker
  thread; `close()` joins it.
- **Lock ordering is part of the design.** Internally one lock guards the Data API's state.
  Scan-storage accessors take the scan-manager lock, which dispatcher callbacks hold while
  delivering data — so Data API code must never acquire the scan-manager lock while holding its
  own lock on a non-dispatcher thread. Entry points that need scan items on such threads
  prefetch them *before* taking the Data API lock. Follow this rule when adding new entry points
  or plugins; violating it re-creates a deadlock between `subscribe()` and the scan-segment
  callback.

!!! info "What to remember"
    - Plugins claim whole scans in priority order: live (10), history (50), device streams (90).
    - A `"live"` subscription backfills on entry, follows scan changes with `"rebind"`, and ends
      every scan re-routed to the authoritative history snapshot.
    - The size gate withholds large *history* loads until `confirm_size()`; live data is never
      gated.
    - Callbacks can arrive on background threads — widgets go through `QtDataSubscription`.
    - Never take the scan-manager lock while holding the Data API lock on a non-dispatcher
      thread; prefetch scan items first.

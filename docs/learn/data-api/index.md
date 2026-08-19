---
related:
  - title: Subscriptions and Updates
    url: learn/data-api/subscriptions-and-updates.md
  - title: Ordinal Alignment
    url: learn/data-api/ordinal-alignment.md
  - title: Subscribe to Live Data
    url: how-to/scans/subscribe-to-live-data-with-the-data-api.md
  - title: Data Flow
    url: learn/system-architecture/overview/data-flow.md
---

# The Data API

The Data API is the client-side data access layer of BEC. It gives consumers — plotting widgets,
scripts, and analysis tools — one uniform way to receive scan data, regardless of whether that data
is currently being produced by a running scan, already sits in the scan history, or streams from a
device outside any scan.

Before the Data API, every consumer solved these problems on its own: widgets subscribed to raw
Redis endpoints, re-implemented buffering and pairing of device readings, trimmed arrays to equal
lengths, and handled scan changes with ad-hoc logic. The Data API moves all of that shared logic
into `bec_lib`, so a consumer only declares *which* data it wants and receives ready-to-use,
aligned columns.

## What it provides

- **One subscription contract.** A consumer calls `client.data_api.subscribe(...)` with a list of
  `(device, entry)` pairs and receives immutable, columnar snapshots
  ([`SubscriptionUpdate`](subscriptions-and-updates.md)) — the same shape for live updates,
  backfills of already-recorded points, and history reads.
- **Correct pairing of readings.** Points are joined by *ordinal* (the scan point id, the async
  message index, or an arrival counter) instead of by arrival order, so out-of-order or dropped
  messages can never silently shift one curve against another
  ([ordinal alignment](ordinal-alignment.md)).
- **Live-follow across scans.** A subscription with `scan="live"` automatically re-binds to each
  new scan, backfills points that were recorded before the subscription existed, and re-routes to
  the scan history once the scan is finished and written.
- **Bounded resource usage.** Emission coalescing limits the update rate, retention caps bound
  endless device streams, and a size gate lets consumers confirm large history loads before
  anything is read.

## Who should use it

The Data API is a **developer-facing** interface. End users interact with it indirectly through
the BEC Widgets plotting tools, which are all built on it. Use the Data API directly when you

- build a custom widget that displays live or historic scan data,
- write a script or service that consumes scan data as it is produced,
- need past scan data in the same aligned, columnar form the widgets use.

For occasional interactive access to finished scans, the
[scan history](../../how-to/scans/access-bec-history.md) and the
[HDF5 files](../../how-to/scans/open-bec-hdf5-files-with-h5py.md) remain the simplest tools; the
Data API becomes valuable when live and historic data must be handled through one code path.

!!! info "What to remember"
    - The Data API is the single data-access contract for live scans, scan history, and
      scan-independent device streams.
    - Consumers receive immutable columnar snapshots with pre-aligned columns — no manual
      buffering, trimming, or pairing.
    - It lives in `bec_lib` (`client.data_api`); BEC Widgets adds a thin Qt bridge on top.
    - All BEC plotting widgets are built on it, so its behavior defines what the GUI shows.

---
related:
  - title: Subscriptions and Updates
    url: learn/data-api/subscriptions-and-updates.md
  - title: Readout Priority
    url: learn/devices/readout-priority.md
  - title: BEC Signals for Custom Devices
    url: learn/devices/bec-signals.md
---

# Ordinal Alignment and Correlation Groups

The central promise of the Data API is that a point plotted for one source is paired with the
*matching* point of every other source — never merely with whatever arrived at the same time.
This page explains the mechanism behind that promise.

## Why arrival order is not enough

Redis delivers messages reliably, but consumers can subscribe mid-scan, messages from different
endpoints interleave freely, and async detectors emit at their own pace. A consumer that pairs
readings by position — "the 5th x value belongs to the 5th y value" — silently corrupts its data
the moment one source skips or repeats a message. Earlier plotting code carried exactly this
fragility.

## Ordinals

The Data API keys every stored point by an **ordinal** — an integer that identifies *which*
acquisition the point belongs to:

| Source kind  | Ordinal                                                                       |
|--------------|-------------------------------------------------------------------------------|
| `monitored`  | The scan `point_id` of the scan segment that carried the reading.             |
| `async`      | The per-scan async message index (for `add` updates) or the slice row (for `add_slice`); `replace` sources expose a single point. |
| `unindexed`  | An arrival counter — used for legacy async devices that publish no indices.   |

A point arriving late fills its hole; a point arriving twice overwrites in place. Ordering on the
wire becomes irrelevant.

## Correlation groups

Not all sources of a subscription can be meaningfully paired. The Data API partitions the declared
sources into **correlation groups** and aligns each group independently:

- **`scan`** — all `monitored` signals, plus async signals whose device declares the
  `"monitored"` acquisition group (one emission per scan point). These share the scan point id as
  their ordinal and align against each other.
- **`async:<tag>`** — async signals sharing a free-form acquisition group tag; they promise a
  common cadence with each other, but not with the scan.
- **`standalone:<device>/<entry>`** — sources that cannot promise any cadence (unindexed legacy
  devices, ungrouped async signals, scan-independent device streams). Each is its own group.

Each group emits its own updates (`update.metadata["group"]` names it), so one widget can
subscribe to a mixed source set and still receive correctly-scoped snapshots.

## Aligned columns and completeness

Within a group, `update.aligned()` returns the values at the ordinals present in **every** source
of the group. A source that has not yet delivered ordinal 7 simply holds back ordinal 7 from the
aligned view — it does not shift later points. The full per-source state remains available in
`update.sources` for consumers that want leading, unaligned data.

Two related signals help consumers judge the state:

- `update.complete` is `True` when every source holds an uninterrupted range from ordinal 0 to a
  common frontier — nothing is missing anywhere.
- `update.metadata["lagging_sources"]` lists sources trailing the group frontier by more than a
  small threshold. A silent detector does not block delivery — updates keep flowing — but it
  stalls the aligned view, and this field makes the responsible source visible instead of leaving
  a mysteriously frozen curve.

!!! info "What to remember"
    - Every point is keyed by an ordinal — scan point id, async index, or arrival counter — so
      pairing survives out-of-order, dropped, and repeated messages.
    - Sources are partitioned into correlation groups (`scan`, `async:<tag>`, standalone); only
      sources in the same group are aligned with each other.
    - `aligned()` is the intersection over ordinals: a lagging source holds back the aligned view
      but never corrupts it.
    - `complete` and `lagging_sources` turn "why is my curve stuck?" into a visible answer.

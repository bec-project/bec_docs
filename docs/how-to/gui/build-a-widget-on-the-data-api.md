---
related:
  - title: The Data API
    url: learn/data-api/index.md
  - title: Subscriptions and Updates
    url: learn/data-api/subscriptions-and-updates.md
  - title: Data Source Plugins and Scan Lifecycle
    url: learn/data-api/plugins-and-lifecycle.md
---

# Build a Widget on the Data API

!!! Info "Overview"
    Display live or historic scan data in a custom Qt widget through `QtDataSubscription` — the
    thread-safe bridge all BEC plotting widgets use.

## Prerequisites

- A custom widget following the [BEC widget pattern](../../learn/gui/introduction.md).
- The device and signal names the widget should display.

!!! learn "[Learn how subscriptions and updates work](../../learn/data-api/subscriptions-and-updates.md){ data-preview }"

## 1. Create the bridge instead of subscribing directly

Data API callbacks can arrive on background threads. `QtDataSubscription` wraps the subscription
in a `QObject` and re-emits every update as a Qt signal on the GUI thread — never call
`data_api.subscribe` directly from widget code.

```python
from bec_widgets.utils.qt_data_subscription import QtDataSubscription


class MyWidget(BECWidget, QWidget):
    def _setup_subscription(self):
        self._bridge = QtDataSubscription(
            self.client,
            sources=[("samx", "samx"), ("bpm4i", "bpm4i")],
            scan="live",
            parent=self,
            min_emit_interval=self.update_interval_s,
        )
        self._bridge.updated.connect(self._on_data_update)
```

Parenting the bridge to the widget ties the subscription's lifetime to the widget; it closes
automatically when the widget is destroyed. Close and recreate the bridge when the source set
changes.

## 2. Render full snapshots

Every update carries the complete current state, so the render slot is a pure function of the
newest update — no accumulation in the widget:

```python
@SafeSlot(object)
def _on_data_update(self, update):
    if update.reason in ("backfill", "history", "rebind"):
        self._reset_per_scan_state(update.scan_id)
    cols = update.aligned()
    self.curve.setData(
        cols[("samx", "samx")],
        cols[("bpm4i", "bpm4i")],
    )
```

Use `update.reason` to distinguish appends (`"live"`) from situations that require rebuilding
cached display state.

!!! warning "Never test a column for truthiness"
    Columns arrive as tuples from the live path but as `numpy.ndarray` from history reads, and
    `if not values:` raises `ValueError` on an array with more than one element. Inside a
    `SafeSlot` that surfaces as a widget that simply shows nothing. Length-check instead:

    ```python
    if values is None or len(values) == 0:
        return
    ```

## 3. Respect the widget update rate

Widgets deriving from `PlotBase` expose an `update_rate` property (Hz, clamped to 1–100,
settable at runtime from the Designer, RPC, or code). Pass `self.update_interval_s` when creating
bridges — the property setter then re-applies a changed rate to every active bridge in place.

Widget classes declare their default via a class attribute; pick it to match the widget's render
cost:

```python
class MyWidget(PlotBase):
    DEFAULT_UPDATE_RATE = 15.0
```

## 4. Handle device streams and large loads

- For scan-independent streams pass `scan=None` and a `max_points` cap, exactly as in the
  [script how-to](../scans/subscribe-to-live-data-with-the-data-api.md).
- For history-bound widgets pass `size_limit_bytes`; a gated bridge reports `size_gated` and
  `estimated_bytes`, letting the widget ask the user before calling `confirm_size()`.
- A confirmed large load still takes seconds to read from disk. Connect `bridge.progress` to show
  it, instead of leaving the user in front of a window that looks frozen:

```python
self._bridge.progress.connect(self._on_load_progress)

@SafeSlot(float)
def _on_load_progress(self, fraction: float):
    self._progress_row.setVisible(fraction < 1.0)
    self._progress_bar.setValue(int(fraction * 100))
```

  The signal is emitted on the Qt thread (the backend reports from its worker thread and the
  bridge marshals it), so the slot may touch widgets directly. `Waveform` does this with a
  labelled bar below the plot.

!!! note "Health checks"
    `bridge.healthy` is `False` while any declared source is not delivering — use it to show a
    connection state instead of a silently empty plot.

---
related:
  - title: File writing
    url: learn/file-writer/introduction.md
---

# BEC Signals for Custom Devices

`ophyd_devices.utils.bec_signals` provides convenience signal classes that wrap ophyd signals with BEC-native message types. They are designed to forward preview data, file events, progress updates, and asynchronous signal streams into BEC.

## Exported signal classes

The module exports the following classes:

- `ProgressSignal`
- `FileEventSignal`
- `PreviewSignal`
- `DynamicSignal`
- `AsyncSignal`
- `AsyncMultiSignal`

## Core behavior

All BEC signal classes build on `BECMessageSignal`, which adds:

- BEC message validation (`BECMessage` subclasses)
- standardized `signal_info` metadata via `describe()`
- conversion support from dictionaries to typed BEC messages
- immediate completion semantics for `set(...)`

`SignalInfo` metadata includes fields such as `data_type`, `saved`, `ndim`, `scope`, `role`, `signals`, `signal_metadata`, and `acquisition_group`.

## Signal classes in practice

### `PreviewSignal`

Use this to stream 1D or 2D preview data (for example beam monitor cameras). It emits `DevicePreviewMessage` and supports optional orientation correction:

- `num_rotation_90`: rotate 2D data before publishing
- `transpose`: transpose 2D data before publishing

You can publish arrays directly with `preview.put(array_data)`.

### `ProgressSignal`

Use this for scan-linked progress updates. It emits `ProgressMessage` and can be updated by either:

- `progress.put(msg=...)`
- `progress.put(value=..., max_value=..., done=..., metadata=...)`

### `FileEventSignal`

Use this when a device writes external files. It emits `FileMessage` and supports:

- `file_path`
- `done`
- `successful`
- `file_type`
- `hinted_h5_entries`
- `metadata`

`hinted_h5_entries` is important for downstream file linking in BEC file writing.

### `DynamicSignal`

General signal group for `DeviceMessage` payloads with named sub-signals and metadata. It validates signal names and async update metadata.

### `AsyncSignal`

Specialized dynamic signal for one asynchronous channel. Requires async-update metadata describing how data is appended or replaced.

### `AsyncMultiSignal`

Specialized dynamic signal for multiple asynchronous sub-signals, with strict signal-name validation.

## How device-server callbacks route these signals

In `bec_server.device_server.bec_message_handler.BECMessageHandler.emit`, callback dispatch is based on signal type:

- `FileEventSignal` -> `_handle_file_event_signal`
- `ProgressSignal` -> `_handle_progress_signal`
- `PreviewSignal` -> `_handle_preview_signal`
- `DynamicSignal` (therefore also `AsyncSignal` and `AsyncMultiSignal`) -> `_handle_async_signal`

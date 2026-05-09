---
related:
  - title: File writing
    url: learn/file-writer/introduction.md
  - title: Add a Preview Signal
    url: how-to/devices/add-a-preview-signal.md
  - title: Add a File Event Signal
    url: how-to/devices/add-a-file-event-signal.md
  - title: Add an Async Multi Signal
    url: how-to/devices/add-an-async-multi-signal.md
---

# BEC Signals for Custom Devices

Ophyd devices typically use `Signal` and `Component` objects to communicate with hardware. `BECSignal`s are building their counterparts designed to communicate with BEC instead of hardware. This allows devices to send structured messages and inform BEC about e.g. progress updates, file events, and asynchronous data streams.

!!! info "BEC Signals are internal components"
    BEC signals are not meant to be read out directly through the command-line interface. They are internal components that allow devices to send structured messages to BEC. 

## Signal classes

BEC provides several signal classes for different use cases. Some of them are designed for broadcasting runtime information such as progress updates and file events, while others are designed for streaming asynchronous data into the scan dataset and are therefore saved to HDF5.

<table>
  <colgroup>
    <col style="width: 22%;">
    <col style="width: 56%;">
    <col style="width: 22%;">
  </colgroup>
  <thead>
    <tr>
      <th>Signal class</th>
      <th>Description</th>
      <th>Saved to HDF5?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap;"><code>ProgressSignal</code></td>
      <td>Used to emit a device-related progress using a <code>ProgressMessage</code>.</td>
      <td>No</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>FileEventSignal</code></td>
      <td>Used to report external file-writing events using a <code>FileMessage</code>.</td>
      <td>Yes, as file references</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>PreviewSignal</code></td>
      <td>Used to stream 1D or 2D preview data using a <code>DevicePreviewMessage</code>.</td>
      <td>No</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>AsyncSignal</code></td>
      <td>Used to represent a single asynchronous data channel with async-update metadata. Every update must provide the specified signal.</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>AsyncMultiSignal</code></td>
      <td>Used to represent multiple asynchronous sub-signals with strict signal-name validation. Every update must provide all specified signals.</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>DynamicSignal</code></td>
      <td>Similar to <code>AsyncMultiSignal</code> but an update does not require all specified signals.</td>
      <td>Yes</td>
    </tr>
  </tbody>
</table>

`FileEventSignal` does not store the detector payload itself in the scan dataset. Instead, BEC records file references in the master HDF5 file so externally written data can be linked there.

## Usage and metadata

BEC signals are defined as normal ophyd components:

```python
class MyDevice(Device):
    progress = Cpt(ProgressSignal, name="progress")
    file_event = Cpt(FileEventSignal, name="file_event")
    preview = Cpt(PreviewSignal, name="preview", ndim=2, max_shape=[1024, 1024])
    async_signal = Cpt(
        AsyncSignal,
        name="async_signal",
        ndim=1,
        max_size=1000,
        async_update={"type": "add", "max_shape": [None, 1000]},
    )
    async_multi_signal = Cpt(
        AsyncMultiSignal,
        name="async_multi_signal",
        signals=["temperature", "pressure"],
        async_update={"type": "add", "max_shape": [None, None]},
    )
```

and then used from within the device methods:

```python
self.progress.put(value=50, max_value=100, done=False)
```

The exact signature depends on the signal class but in general, the `put(...)` can be used to pass in either the data values directly or a structured message object.

For more details on how to use each signal class, see the following how-to guides:

- [Add a Progress Signal](../../how-to/devices/add-a-progress-signal.md)
- [Add a File Event Signal](../../how-to/devices/add-a-file-event-signal.md)
- [Add a Preview Signal](../../how-to/devices/add-a-preview-signal.md)
- [Add an Async Signal](../../how-to/devices/add-an-async-signal.md)
- [Add an Async Multi Signal](../../how-to/devices/add-an-async-multi-signal.md)

## Async update metadata

`AsyncSignal`, `AsyncMultiSignal`, and `DynamicSignal` need `async_update` metadata so BEC knows how each async update should be aggregated into the scan dataset. 

The async update metadata supports three modes:

<table>
  <colgroup>
    <col style="width: 18%;">
    <col style="width: 54%;">
    <col style="width: 28%;">
  </colgroup>
  <thead>
    <tr>
      <th>Mode</th>
      <th>Description</th>
      <th>Required metadata</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap;"><code>add</code></td>
      <td>Append each new update along the first axis of the dataset.</td>
      <td><code>type</code>, <code>max_shape</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>add_slice</code></td>
      <td>Write each new update into a specific slice of a larger dataset.</td>
      <td><code>type</code>, <code>index</code>, <code>max_shape</code></td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>replace</code></td>
      <td>Replace the current dataset with each new async update instead of extending it.</td>
      <td><code>type</code></td>
    </tr>
  </tbody>
</table>



In normal usage, define `async_update` once on the signal declaration and then send only data values at runtime.

```python
waveform = Cpt(
    AsyncSignal,
    name="waveform",
    ndim=1,
    max_size=1000,
    async_update={"type": "add", "max_shape": [None, 1024]},
)

self.waveform.put(values)
```


### `add`

Use `add` when every new update should be appended along the first axis.

Typical uses:

- one growing 1D stream
- a sequence of fixed-length waveforms
- a sequence of variable-length 1D datasets
- a sequence of images

Example definitions:

```python
# growing 1D stream
async_update={"type": "add", "max_shape": [None]}

# stream of fixed-length waveforms
async_update={"type": "add", "max_shape": [None, 1024]}

# stream of variable-length 1D datasets
async_update={"type": "add", "max_shape": [None, None]}

# stream of fixed-size images
async_update={"type": "add", "max_shape": [None, 512, 512]}
```

What is required:

- `type="add"`
- `max_shape`

How to read the `max_shape` argument:

- `[None]` means one unlimited 1D stream
- `[None, 1024]` means an unlimited number of rows, each of length `1024`
- `[None, None]` means an unlimited number of 1D datasets with varying length
- `[None, 512, 512]` means an unlimited number of images, each `512 x 512`

When to use it:

- when each update is one new value block, row, waveform, or image
- when you do not need to target a specific slice index

!!! warning "Prefer fixed inner sizes when possible"
    `[None, None]` is supported for a dataset that is an array of 1D datasets with varying length. However, whenever possible, prefer a fixed inner size such as `[None, 1024]`. Variable-length inner data is the most inefficient way of writing the dataset.

### `add_slice`

Use `add_slice` when async updates should be written into a specific slice of a larger dataset: Rather than appending an entire new row, each update fills a slice of the specified `index` along the first axis.

Example definition:

```python
waveform = Cpt(
    AsyncSignal,
    name="waveform",
    ndim=1,
    max_size=1000,
    async_update={"type": "add_slice", "index": 0, "max_shape": [None, 20]},
)
```

Example runtime updates for building up a 2D dataset, one slice at a time:

```python
# fill the first slice (index 0) 
self.waveform.put(
  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
  async_update={"type": "add_slice", "index": 0, "max_shape": [None, 20]}
)

# append to the first slice (index 0)
self.waveform.put(
  [11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 
  async_update={"type": "add_slice", "index": 0, "max_shape": [None, 20]}
)

# fill in the second slice (index 1)
self.waveform.put(
  [21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 
  async_update={"type": "add_slice", "index": 1, "max_shape": [None, 20]}
)
```


What is required:

- `type="add_slice"`
- `max_shape`
- `index`

When to use it:

- when updates belong to a specific slice index
- when one logical row or slice is filled over multiple updates

!!! warning "Specify the slice index on each update"
    In contrast to `add` and `replace`, `add_slice` updates require the `async_update` metadata to be passed on each `put(...)` call, because the slice `index` may change between updates.


### `replace`

Use `replace` when each new async update should replace the current dataset instead of extending it.

Example definition:

```python
result = Cpt(
    AsyncSignal,
    name="result",
    ndim=1,
    max_size=10,
    async_update={"type": "replace"},
)
```

At runtime:

```python
self.result.put(latest_result)
```

What is required:

- `type="replace"`

When to use it:

- when the device publishes a refreshed full result
- when old async data should be superseded instead of extended

!!! info "What to remember"
    - `BECSignal` classes are ophyd-style components for sending structured messages from devices into BEC instead of talking directly to hardware.
    - Choose the signal class based on the kind of information your device publishes: progress updates, file events, preview data, or asynchronous data streams.
    - Declare BEC signals on the device class like normal ophyd components, then publish updates with `put(...)` from the device code.
    - `AsyncSignal`, `AsyncMultiSignal`, and `DynamicSignal` need `async_update` metadata so BEC knows how incoming async data should be written into the scan dataset.
    - For async streams, use `add` by default, use `add_slice` for indexed slice updates, and use `replace` when each update should overwrite the previous result.

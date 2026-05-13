---
related:
  - title: Write a custom ophyd device
    url: ../../how-to/devices/development/write-a-custom-device.md
  - title: Use status objects in a custom ophyd device
    url: ../../how-to/devices/development/use-status-objects-in-a-custom-device.md
  - title: Introduction to ophyd
    url: introduction-to-ophyd.md
  - title: BEC signals for custom devices
    url: bec-signals.md
  - title: Device config in BEC
    url: device-config-in-bec.md
---

# Custom Ophyd Devices

If you are familiar with ophyd and want to integrate a new device, we recommend that you use the `PSIDeviceBase` class from `ophyd_devices`. It essentially serves as a template for how to structure your custom device class and allows you to focus on local device logic.

Ophyd itself provides a nice abstraction with lifecycle methods such as `stage()`, `unstage()`, `trigger()`, and so on. BEC leverages these methods in its scan execution. The idea is that if your device always needs to follow a certain pattern for a scan, then we will place this logic on the device level. A good example of this is a detector with its own backend that writes files. In that case, the device requires the relevant information about where to write files, how many frames to acquire, and so on.

## The role of `PSIDeviceBase`

At its core, `PSIDeviceBase` is still an ophyd `Device`, so you define signals and sub-devices in the usual way with `Component` declarations. The difference is that it wraps a few important ophyd lifecycle methods and forwards them into explicit hook methods that are easier to override during integration work:

<table>
  <thead>
    <tr>
      <th style="width: 24%; white-space: nowrap;">Hook</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap;"><code>on_init()</code></td>
      <td>Runs at the end of device initialization. Use it for setup logic that does not depend on connected signals.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>on_connected()</code></td>
      <td>Runs after the device and its signals are connected. Use it for setting default signal values, subscriptions, and logic that depends on connected signals.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>on_stage()</code></td>
      <td>Runs during <code>stage()</code>. Use it to prepare the device for an upcoming scan.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>on_unstage()</code></td>
      <td>Runs during <code>unstage()</code>. Use it to reset the state of the device after a scan, must be idempotent.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>on_pre_scan()</code></td>
      <td>Runs right before scan execution starts. Use it for actions that must happen immediately before acquisition.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>on_trigger()</code></td>
      <td>Runs when the device is triggered. This is typically called during the <code>at_each_point</code> hook from the scan interface in BEC.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>on_complete()</code></td>
      <td>Runs when BEC checks whether the device has finished. Use it to report if the acquisition finished successfully.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>on_kickoff()</code></td>
      <td>Runs when a fly-scan style acquisition is started explicitly. Use it for devices that begin a longer-running acquisition.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>on_stop()</code></td>
      <td>Runs when the device is stopped. Use it to stop the device. It should be fast and non-blocking.</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;"><code>on_destroy()</code></td>
      <td>Runs when the device is destroyed. Use it for final cleanup of threads, sockets, or other resources.</td>
    </tr>
  </tbody>
</table>

## When the hooks run

The most useful way to understand the hooks is to think about what kind of device logic belongs into each phase of the lifecycle.

### Initialization

`on_init()` runs at the end of `__init__()`.

At this point the Python object exists, but you should assume that signals are not connected yet. This hook is therefore best for local setup such as:

- creating helper attributes
- initializing caches or configuration state
- preparing task or file-handling helpers

### Connection

`on_connected()` is not called from the constructor. Instead, it is called later by the device manager after the device and its signals are connected.

This is the right place for:

- setting default signal values
- assigning `kind`
- installing callbacks or subscriptions
- any setup that needs live signal access

### Stage and unstage

- `on_stage()` is the place to prepare the device for the upcoming scan.
- `on_unstage()` is the place to undo temporary scan setup and return the device to a known state.

Typical tasks in this phase are applying scan-dependent settings, allocating temporary resources, and resetting transient state once the scan is over.

### Pre-scan

BEC adds one extra phase that is not part of the standard ophyd `Device` API.

This hook is useful for setup that must happen immediately before scan execution starts on all participating devices. Typical examples are:

- arming a detector backend
- opening a shutter
- checking readiness of an external controller

Because this phase sits close to actual acquisition, it is often where devices change from a configured state into an armed or ready state.

### Trigger and complete

`on_trigger()` is usually the place for step-scan acquisition logic, while `on_complete()` is where a device reports whether its acquisition or backend work has actually finished.

This split is important for detectors and other asynchronous devices. Triggering an action and observing its completion are often not the same thing.

### Kickoff

Use `on_kickoff()` when the device starts a longer-running acquisition explicitly instead of performing one trigger per point.

This is the typical entry point for fly-scan style devices, streamers, and other devices that need to start a run once and then stay active while the scan progresses.

### Stop and destroy

`on_stop()` should usually be fast and non-blocking. Its job is to tell the device to stop what it is doing and let the rest of the BEC stop logic proceed.

`on_destroy()` is the final cleanup hook. Use it for resources that should disappear when the device object is torn down, such as threads, sockets, or file handles.

## Status objects and asynchronous work

The most important design choice when implementing a hook is whether the action is synchronous or asynchronous.

A synchronous action finishes before the hook returns. In that case, the hook can simply perform the work and return `None`.

An asynchronous action starts now but finishes later. This is common for detectors, shutters, motion controllers, and file-writing backends. In that case, the hook should return a `StatusBase` or `DeviceStatus` object.

You can think of these status objects as future-like objects. They represent work that is still in progress and will later resolve either:

- successfully, when the action is done
- with an exception, when the action fails or times out

BEC waits on the returned status before moving on to the next scan step or lifecycle phase.

This is the key rule:

- return `None` only when the hook has finished synchronously
- return a status object when completion happens later

In practice, a status object answers questions such as:

- has the detector really become ready yet?
- has the move really completed yet?
- has the acquisition backend returned to idle?

`PSIDeviceBase` also helps with interruption handling through `cancel_on_stop(status)`. If a scan is stopped, the base class marks registered status objects as failed with `DeviceStoppedError`. That keeps long-running acquisitions from hanging forever after an abort.

## Waiting for hardware conditions

`PSIDeviceBase.wait_for_condition(...)` is a convenience wrapper for simple polling loops. It repeatedly checks a callable until it becomes true or a timeout is reached.

It is especially useful when:

- a device has no native status object
- a hardware controller exposes only state PVs
- the loop must react to an external BEC stop

With `check_stopped=True`, the helper raises `DeviceStoppedError` as soon as the device has been stopped, which is usually better than waiting for the full timeout.

## CompareStatus and TransitionStatus

For many devices, asynchronous completion can be expressed directly in terms of signal values. `ophyd_devices` provides two helper status classes for this: `CompareStatus` and `TransitionStatus`.

Both classes are specialized subscription-based status objects. They listen to a signal and resolve automatically when a certain condition becomes true. This makes them a natural fit for hooks such as `on_pre_scan()`, `on_trigger()`, `on_complete()`, or `on_kickoff()`.

!!! learn "[Review the general status-object model first](#status-objects-and-asynchronous-work)"

### `CompareStatus`

`CompareStatus` waits until one signal value matches a comparison against a target value.

Use it when success can be expressed as a single condition such as:

- `acquire == 1`
- `ready == 1`
- `state == "armed"`
- `temperature < threshold`

It supports comparison operators such as `==`, `!=`, `<`, `<=`, `>`, and `>=`. It can also be configured with failure values that immediately raise an exception if the signal enters an invalid state.

This makes it a good fit for actions such as:

- waiting for a detector to report that acquisition has started
- waiting for a shutter to report open or closed
- checking that a controller reached a ready state without entering an error state

### `TransitionStatus`

`TransitionStatus` waits for a signal to move through a sequence of values in order.

Use it when success is not one static value, but a state transition pattern such as:

- `0 -> 1`
- `1 -> 0`
- `0 -> 1 -> 0`
- `"idle" -> "arming" -> "armed"`

This is especially useful for signals that encode progress through a small state machine. A common example is an acquire PV that changes to `1` when acquisition starts and back to `0` when acquisition is finished.

`TransitionStatus` supports two modes:

- `strict=True`: each expected transition must be seen from the previous expected value to the next one
- `strict=False`: intermediate unrelated values are tolerated as long as the expected values are eventually observed in order

You can also define `failure_states` that should immediately fail the status if encountered.

### When to choose which helper

- Use `CompareStatus` when one value tells you that the action has succeeded.
- Use `TransitionStatus` when success means that the signal must move through a sequence of states.

For example:

- `on_pre_scan()` often uses `CompareStatus` to wait until a detector has become armed.
- `on_complete()` often uses `TransitionStatus` to wait until an acquire signal transitions back to idle.

!!! learn "[See a practical how-to with both helpers](../../how-to/devices/development/use-status-objects-in-a-custom-device.md){ data-preview }"

## How scan metadata reaches the device

Custom devices often need information about the active scan: exposure time, number of frames, scan type, or user metadata. `PSIDeviceBase` stores that context on `self.scan_info`.

When the device is used outside a real scan, the base class falls back to a mocked scan-info object from `ophyd_devices.tests.utils.get_mock_scan_info(...)`. That makes local development and testing easier because the device can still access scan-related fields without a running BEC scan server.

In current BEC scan implementations, the scan object builds a `ScanInfo` model and updates it with values such as:

- `scan_name`
- `scan_id`
- `num_points`
- `exp_time`
- `frames_per_trigger`
- `settling_time`
- `request_inputs`
- `user_metadata`

That is why custom devices can make decisions in hooks such as `on_stage()` or `on_pre_scan()` based on the active scan configuration.

## The role of the device manager

The constructor of `PSIDeviceBase` accepts `device_manager`. BEC passes this through during device creation so custom devices can resolve other devices or beamline services when needed.

Many simple devices never need it. It becomes more important for devices that:

- depend on other devices
- need cross-device coordination
- create pseudo or composite abstractions

If your device depends on other devices, prefer making that relationship explicit in the config and in the constructor rather than hard-coding session-specific names deep inside the class.

## BEC-specific signal types

A custom device can use ordinary ophyd signals, but BEC also provides specialized signal classes for data that should flow through BEC services in a richer way.

Examples include:

- `ProgressSignal` for scan progress updates
- `FileEventSignal` for produced files
- `PreviewSignal` for 1D or 2D preview data
- `AsyncSignal` and `AsyncMultiSignal` for asynchronous streams

These signals carry BEC-native message structures and are especially useful for detectors, streamers, and devices that publish more than simple scalar readbacks.

!!! learn "[Learn about BEC-specific signal classes](bec-signals.md){ data-preview }"

## A useful mental model

When you write a custom device for BEC, think in layers:

1. ophyd defines the device structure and the signal hierarchy
2. `PSIDeviceBase` defines how that device joins the BEC lifecycle
3. the device config tells BEC how to instantiate the class in one session

That separation is what makes custom devices reusable. The Python class captures behavior, while the BEC config supplies beamline-specific names, prefixes, and parameters.

## What to read next

- [Write a custom ophyd device](../../how-to/devices/development/write-a-custom-device.md)
- [Use status objects in a custom ophyd device](../../how-to/devices/development/use-status-objects-in-a-custom-device.md)
- [BEC signals for custom devices](bec-signals.md)
- [Device config in BEC](device-config-in-bec.md)

!!! info "What to remember"
    - `PSIDeviceBase` is the main integration point for custom ophyd devices in BEC.
    - Hook implementations should distinguish clearly between synchronous and asynchronous work.
    - Status objects are future-like objects that let BEC wait for device work to complete.
    - `CompareStatus` is useful for one target condition, while `TransitionStatus` is useful for ordered state changes.
    - `cancel_on_stop(...)` and `wait_for_condition(..., check_stopped=True)` help custom devices stop cleanly.
    - `self.scan_info` gives the device access to the active scan context.

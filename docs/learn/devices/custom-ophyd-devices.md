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
- any setup that needs signal access
- installing callbacks or subscriptions

### Stage and unstage

`on_stage()` is the main entry point for scan preparation logic. It is called during `stage()`, which BEC calls before a scan starts.

- use relevant scan metadata from the `ScanStatusMessage` accessible through `self.scan_info.msg` to set up the device for the specific scan configuration.
- if stage is called twice, it will raise an exception. Therefore you can assume that staging is a deliberate action that only happens once per scan, and is undone by `unstage()`.

`on_unstage()` is the place to undo temporary scan setup and return the device to a known state.

- it should be idempotent because BEC calls it during cleanup after a scan, even if staging failed or was interrupted.
- the right place to reset scan-dependent state such as counters, temporary files, or backend resources that should not persist after the scan is over.

Typical tasks in this phase are applying scan-dependent settings, allocating temporary resources, and resetting transient state once the scan is over.

### Pre-scan

`on_pre_scan()` is a hook that BEC adds, which is not part of the standard ophyd `Device` API. It is useful for setup that must happen immediately before scan execution starts on all participating devices. Typical examples are:

- arming a detector backend
- opening a shutter
- checking readiness of an external controller

Because this phase sits close to actual acquisition, it is often where devices change from a configured state into an armed or ready state. It is most often also implemented as an asynchronous hook that returns a status object, so BEC can wait for the device to become ready before starting the scan.

### Trigger and complete

If a scan is software triggered, `on_trigger()` is the main entry point for acquisition logic. It is called from the `at_each_point` hook in the scan interface, so it runs once per scan point, and should be implemented as an asynchronous hook that returns a status object.

- trigger the acquisition on the device or its backend
- return a status object that resolves when the acquisition is done

At the end of a scan, BEC checks whether the device has finished by calling `on_complete()`. This is where the device should report whether acquisition or backend work has actually completed successfully. It is an asynchronous hook that returns a status object.

- check that the acquisition is done, all files are successfully written and BEC can move on to for example linking files
- Raise an exception if the acquisition failed
- It is typically helpful to implement a timeout logic in this hook, so that if the device or backend hangs, the scan will fail at some point with a meaningful error instead of hanging indefinitely.

### Kickoff

`on_kickoff()` is a separate hook fairly similar to `on_pre_scan()`. It is part of the fly-scan interface from ophyd, and is an asynchronous hook that returns a status object. The status should resolved once the kickoff action is done and the device is actively acquiring.

- use it for a fly-scan acquisition, for example to start a trajectory motion on a controller
- resolve immediately after the controller starts moving, NOT after the move finished. That way, the kickoff status only represents the time it takes to start the acquisition, and the rest of the scan can proceed while the acquisition is still running. Dependening on the logic of your scan, BEC will check for acquisition completion either in `on_complete()` or in a custom method.

### Stop and destroy

`on_stop()` should usually be fast and non-blocking. Any cleanup logic needed to stop the device should go here.

`on_destroy()` is the final cleanup hook. Use it for resources that should disappear when the device object is torn down, such as threads, sockets, or file handles. It should be safe to call and not raise an exception.

## Status objects and asynchronous work

The most important design choice when implementing a hook is whether the action is synchronous or asynchronous.

A synchronous action finishes before the hook returns. In that case, the hook can simply perform the work and return `None`.

An asynchronous action starts now but finishes later. This is common for the integration of detectors or other more complex devices. In that case, the hook should return a `StatusBase` or `DeviceStatus` object.

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

!!! info 

    If you interested in more details about status objects, how to create them, and how to use them in custom devices, check out the [Use status objects in a custom ophyd device](../../how-to/devices/development/use-status-objects-in-a-custom-device.md) guide.

## How scan metadata reaches the device

Custom devices often need information about the active scan: exposure time, number of frames, scan type, or user metadata. `PSIDeviceBase` stores that context on `self.scan_info`.

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

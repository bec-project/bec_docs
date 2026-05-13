---
related:
  - title: Custom ophyd devices
    url: ../../../learn/devices/custom-ophyd-devices.md
  - title: Write a custom ophyd device
    url: write-a-custom-device.md
  - title: BEC signals for custom devices
    url: ../../../learn/devices/bec-signals.md
---

# Use status objects in a custom ophyd device

!!! Info "Overview"
    Use `CompareStatus` and `TransitionStatus` in custom ophyd device hooks when the device action starts immediately but completes only after a signal reaches the expected state.

## Prerequisites

- You already have a custom device class based on `PSIDeviceBase`.
- Your device exposes signal values that indicate readiness, acquisition, or completion.
- You know whether success is best described as one target value or as a sequence of transitions.

!!! learn "[Learn when custom devices should return status objects](../../../learn/devices/custom-ophyd-devices.md#status-objects-and-asynchronous-work){ data-preview }"

## Use `CompareStatus` in `on_pre_scan()`

`CompareStatus` is a good fit when pre-scan preparation should complete as soon as one signal reaches one target value.

For example, assume a detector has:

- an `arm` signal that starts preparation
- a `ready` signal that becomes `1` once arming is complete
- a `state` signal that may go to `"error"` if arming fails

In that case, `on_pre_scan()` can start arming and return a `CompareStatus`:

```py
from ophyd_devices.utils.psi_device_base_utils import CompareStatus


def on_pre_scan(self):
    self.arm.put(1)
    status = CompareStatus(
        signal=self.ready,
        value=1,
        operation_success="==",
        timeout=5,
    )
    self.cancel_on_stop(status)
    return status
```

If the device has an explicit error state, include that as a failure value:

```py
def on_pre_scan(self):
    self.arm.put(1)
    status = CompareStatus(
        signal=self.state,
        value="armed",
        operation_success="==",
        failure_value=["error", "fault"],
        timeout=5,
    )
    self.cancel_on_stop(status)
    return status
```

Use this pattern when one value is enough to decide whether the device is ready.

## Use `TransitionStatus` in `on_complete()`

`TransitionStatus` is a better fit when completion is expressed as a sequence of states.

A common detector pattern is:

- `acquire = 1` while acquisition is running
- `acquire = 0` again once acquisition is complete

If the signal should explicitly transition back to idle, `on_complete()` can return:

```py
from ophyd_devices.utils.psi_device_base_utils import TransitionStatus


def on_complete(self):
    status = TransitionStatus(
        signal=self.acquire,
        transitions=[1, 0],
        strict=True,
        timeout=10,
    )
    self.cancel_on_stop(status)
    return status
```

This tells BEC to wait until acquisition is first observed as active and then observed as idle again.

If the controller may pass through an error code, fail early with `failure_states`:

```py
def on_complete(self):
    status = TransitionStatus(
        signal=self.acquire,
        transitions=[1, 0],
        strict=True,
        failure_states=[-1],
        timeout=10,
    )
    self.cancel_on_stop(status)
    return status
```

Use this pattern when completion depends on a state transition rather than one static value.

## Choose the right helper

- Use `CompareStatus` when success means “the signal reached this value”.
- Use `TransitionStatus` when success means “the signal moved through these values in order”.

## Common pitfalls

- Returning `None` even though the device is still changing state asynchronously.
- Forgetting `cancel_on_stop(status)`, which can leave BEC waiting on a status after an abort.
- Using `CompareStatus` when the real requirement is to observe a full transition sequence.
- Using `TransitionStatus` with an incomplete transition list, for example waiting only for `0` when the real completion pattern is `1 -> 0`.

!!! success "Congratulations!"
    You have used status objects to describe asynchronous device behavior in a way that BEC can wait for reliably during scans.

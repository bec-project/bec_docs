---
related:
  - title: Custom ophyd devices in BEC
    url: ../../../learn/devices/custom-ophyd-devices.md
  - title: Introduction to ophyd
    url: ../../../learn/devices/introduction-to-ophyd.md
  - title: BEC signals for custom devices
    url: ../../../learn/devices/bec-signals.md
  - title: Device config in BEC
    url: ../../../learn/devices/device-config-in-bec.md
---

# Write a custom ophyd device

!!! Info "Overview"
    Create a reusable ophyd device for BEC by subclassing `PSIDeviceBase`, declaring the device signals as ophyd components, implementing the scan hooks you need, and exposing the class in your device config.

## Prerequisites

- You have a beamline plugin repository or a local checkout of `ophyd_devices`.
- You are comfortable editing Python classes and reloading the BEC device config.
- You already know the control-system endpoints you need, for example EPICS PV suffixes.

!!! learn "[Learn how custom ophyd devices fit into BEC](../../../learn/devices/custom-ophyd-devices.md){ data-preview }"

## 1. Create the device class

In BEC, custom devices should usually inherit from `ophyd_devices.PSIDeviceBase`. It wraps the normal ophyd `Device` lifecycle with BEC-specific hooks such as `on_connected()`, `on_stage()`, `on_pre_scan()`, `on_trigger()`, and `on_stop()`.

Create a new module in your plugin, for example `<bec_plugin>/devices/beam_stop_shutter.py`:

```py
from ophyd import Component as Cpt
from ophyd import EpicsSignal, EpicsSignalRO, StatusBase

from ophyd_devices import PSIDeviceBase


class BeamStopShutter(PSIDeviceBase):
    """Simple shutter device that can be prepared automatically for scans."""

    open_cmd = Cpt(EpicsSignal, "OPEN")
    close_cmd = Cpt(EpicsSignal, "CLOSE")
    state = Cpt(EpicsSignalRO, "STATE")
    ready = Cpt(EpicsSignalRO, "READY")

    def __init__(self, prefix: str, name: str, ready_timeout: float = 5.0, **kwargs) -> None:
        super().__init__(prefix=prefix, name=name, **kwargs)
        self._ready_timeout = ready_timeout
```

This keeps the device reusable: the class defines the structure once, and each BEC config entry supplies the concrete `prefix` and optional configuration values.

## 2. Set defaults in `on_connected()`

`on_connected()` is called by the BEC device manager after the device and its signals are connected. Use it for default setup that depends on live signals.

```py
class BeamStopShutter(PSIDeviceBase):
    ...

    def on_connected(self) -> None:
        self.open_cmd.kind = "omitted"
        self.close_cmd.kind = "omitted"
        self.state.kind = "hinted"
        self.ready.kind = "config"
```

This is a good place to:

- assign ophyd `kind` values
- register callbacks
- apply beamline-specific default values

## 3. Implement the scan hooks you need

You do not need to override every hook. Only implement the ones that match the device behavior you want in BEC.

For a shutter that must be opened automatically before the first trigger, `on_pre_scan()` is often enough:

```py
class BeamStopShutter(PSIDeviceBase):
    ...

    def on_pre_scan(self) -> StatusBase:
        def _wait_until_ready() -> None:
            self.open_cmd.put(1)
            ready = self.wait_for_condition(
                condition=lambda: bool(self.ready.get()),
                timeout=self._ready_timeout,
                check_stopped=True,
            )
            if not ready:
                raise RuntimeError(f"{self.name} did not become ready")

        status = self.task_handler.submit_task(_wait_until_ready)
        self.cancel_on_stop(status)
        return status

    def on_stop(self) -> None:
        self.close_cmd.put(1)
```

Important details:

- Return a `StatusBase` or `DeviceStatus` when the action is asynchronous.
- Use `wait_for_condition(..., check_stopped=True)` for polling loops that must react to an external stop.
- Register long-running statuses with `cancel_on_stop(...)` so BEC can fail them cleanly when a scan is interrupted.

If your device must prepare itself during `stage()`, stream data during `trigger()`, or start a fly-scan acquisition during `kickoff()`, implement `on_stage()`, `on_trigger()`, or `on_kickoff()` instead.

## 4. Use `scan_info` when scan context matters

`PSIDeviceBase` keeps the current scan metadata on `self.scan_info`. That lets your device adjust its behavior to the active scan.

For example:

```py
def on_stage(self):
    exp_time = self.scan_info.msg.scan_parameters["exp_time"]
    self.exposure_time.put(exp_time)
```

This is useful when the device needs information such as exposure time, number of frames, scan name, or other request parameters before acquisition starts.

## 5. Export the class

Expose the new class from your package so BEC can import it from `deviceClass`:

```py
from .beam_stop_shutter import BeamStopShutter
```

If the class lives in a beamline plugin, add the import there. If it belongs upstream in `ophyd_devices`, add it to `ophyd_devices.__init__.py`.

## 6. Add the device to the BEC config

Reference the class in your device config and pass constructor arguments through `deviceConfig`:

```yaml
beamstop:
  readoutPriority: baseline
  description: Beam stop shutter
  deviceClass: <bec_plugin>.devices.BeamStopShutter
  deviceConfig:
    prefix: "X01DA-FE-OPEN:"
    ready_timeout: 5.0
  deviceTags:
    - shutter
  enabled: true
  readOnly: false
  softwareTrigger: false
```

The keys inside `deviceConfig` must match the constructor signature of your device class.

!!! learn "[Learn more about device config in BEC](../../../learn/devices/device-config-in-bec.md){ data-preview }"

## 7. Reload and verify the device

Reload the config and reconnect the device server. Then verify that:

- the device appears in the client as `dev.beamstop`
- `dev.beamstop.read()` returns the signals you expect
- a scan that uses the device reaches `on_pre_scan()` and opens the shutter
- stopping the scan closes the shutter and cancels any outstanding status objects

## Common pitfalls

- Initializing live signal defaults in `__init__()` instead of `on_connected()`.
- Returning `None` from an asynchronous hook even though the device still has work to finish.
- Forgetting `cancel_on_stop(status)` for long-running `pre_scan`, `trigger`, or `kickoff` logic.
- Polling without `check_stopped=True`, which can leave the device hanging after a scan stop.
- Forgetting to export the class from the package used by `deviceClass`.

## Next steps

- Add tests with `patched_device(...)` from `ophyd_devices.tests.utils` so you can exercise the device without a real IOC.
- If the device streams files, previews, or async data, use the BEC-specific signal classes documented in [BEC signals for custom devices](../../../learn/devices/bec-signals.md).

!!! success "Congratulations!"
    You have written a custom ophyd device for BEC, connected it to the BEC lifecycle, and exposed it through the device config so it can participate in scans like any other device.

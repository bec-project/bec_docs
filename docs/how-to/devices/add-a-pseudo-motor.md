---
related:
  - title: Add an EPICS motor
    url: ../../how-to/devices/add-an-epics-motor.md
  - title: Pseudo positioners
    url: ../../learn/devices/pseudo-positioners.md
  - title: EPICS motor classes
    url: ../../learn/devices/epics-motors.md
  - title: Device config templates
    url: ../../references/ophyd-devices/device-config-templates.md
---

# Add a Pseudo Positioner

!!! Info "Goal"
    Create a pseudo positioner for BEC by subclassing `ophyd_devices.interfaces.base_classes.PSIPseudoMotorBase`, wiring it to existing motors, and exposing it in your beamline plugin or `ophyd_devices` package.

!!! tip
    If you want to expose slit center or slit width as pseudo motors, you usually do not need to write a new implementation. `ophyd_devices` already provides `VirtualSlitCenter` and `VirtualSlitWidth`. They are merely meant as examples in this how-to guide.

## Pre-requisites
- A beamline plugin repository or local `ophyd_devices` development checkout is available.
- The real motors used by the pseudo positioner already exist in the BEC device config.
- You know which real devices your pseudo positioner depends on, for example two slit blades or two sample stage motors.

!!! learn "[Learn about pseudo positioners](../../learn/devices/pseudo-positioners.md)"

## 1. Create a new pseudo positioner class

In `ophyd_devices`, pseudo positioners for BEC are typically implemented by subclassing `PSIPseudoMotorBase`. This base class provides the pseudo `readback`, `setpoint`, `motor_is_moving`, and a combined `move()` implementation.

Create a new module for your device, for example `<bec_plugin>.devices.virtual_slit.py`:

``` py
from typing import TYPE_CHECKING

from ophyd_devices.interfaces.base_classes.psi_pseudo_motor_base import PSIPseudoMotorBase

if TYPE_CHECKING:
    from bec_lib.devicemanager import DeviceManagerBase


class VirtualSlitCenter(PSIPseudoMotorBase):
    """Pseudo motor that exposes the center of two slit blades."""

    def __init__(
        self,
        name: str,
        left_slit: str,
        right_slit: str,
        device_manager: DeviceManagerBase,
        egu: str | None = None,
        **kwargs,
    ) -> None:
        positioners = self.get_positioner_objects(
            name=name,
            positioners={"left": left_slit, "right": right_slit},
            device_manager=device_manager,
        )
        if egu is None:
            egu = positioners["left"].egu
        super().__init__(
            name=name,
            device_manager=device_manager,
            positioners=positioners,
            egu=egu,
            **kwargs,
        )
```

The keys in `positioners={"left": ..., "right": ...}` are important. They must match the argument names used in the calculation methods you implement next.

## 2. Implement the coordinate transforms

Implement the three required methods:

- `forward_calculation(...)` for mapping the current real motor coordinates to one pseudo coordinate
- `inverse_calculation(position, ...)` for mapping a requested pseudo coordinate back to real motor targets
- `motors_are_moving(...)`

!!! warning
    The pseudo positioner expects that the underlying real devices provide `readback` or `user_readback`, `setpoint` or `user_setpoint`, and `motor_is_moving` signals.

``` py
from ophyd import Signal


class VirtualSlitCenter(PSIPseudoMotorBase):
    ...

    def forward_calculation(self, left: Signal, right: Signal) -> float:
        left_pos = left.get()
        right_pos = right.get()
        return float((left_pos + right_pos) / 2)

    def inverse_calculation(
        self, position: float, left: Signal, right: Signal
    ) -> dict[str, float]:
        left_pos = left.get()
        right_pos = right.get()
        width = right_pos - left_pos
        return {
            "left": position - width / 2,
            "right": position + width / 2,
        }

    def motors_are_moving(self, left: Signal, right: Signal) -> int:
        return int(left.get() or right.get())
```

`PSIPseudoMotorBase.wait_for_connection()` validates these method signatures against the `positioners` keys. If your positioner mapping uses `left` and `right`, then all three methods must accept `left` and `right`.

## 3. Expose the class for discovery

Export the class from your package so it can be referenced from the BEC config.

``` py
from .virtual_slit import VirtualSlitCenter
```

If you keep custom devices in a beamline plugin, add the import to that plugin package. If you contribute upstream, add it to `ophyd_devices.__init__.py`.

## 4. Add the pseudo positioner to the BEC config

The pseudo positioner must list its dependent motors in `needs`, and the names in `deviceConfig` must match the constructor arguments of your class.

``` yaml
slit_center:
  readoutPriority: monitored
  description: Virtual slit center position
  deviceClass: <bec_plugin>.devices.VirtualSlitCenter
  deviceConfig:
    left_slit: samx
    right_slit: samy
  deviceTags:
    - motor
  needs:
    - samx
    - samy
  enabled: true
  readOnly: false
  softwareTrigger: false
```

The `needs` field is required because `get_positioner_objects()` verifies that each dependency is declared in the session config before it resolves the real devices from the device manager.

## 5. Reload BEC and verify the pseudo positioner

Reload the config and reconnect the device server so the new class is imported. Then verify that:

- the pseudo device appears in BEC as `dev.slit_center`
- `dev.slit_center.readback.get()` returns the calculated pseudo coordinate
- moving `dev.slit_center` updates the underlying motors as expected

For example, if the left and right motors are at `1` and `3`, the pseudo center should read back `2`.

!!! success "Congratulations!"
    You have successfully added a pseudo positioner to BEC. You can now expose derived coordinates such as slit center, slit width, or other beamline-specific virtual axes as normal motors in scans.

## Common pitfalls
- Forgetting to declare the dependent motors in `needs`. In that case `get_positioner_objects()` will raise a connection error.
- Using calculation method arguments that do not match the `positioners` keys.
- Referencing devices that do not provide `move()`, `readback` or `user_readback`, `setpoint` or `user_setpoint`, and `motor_is_moving`.
- Forgetting to export the class from your package, which prevents BEC from importing it from `deviceClass`.

## Next steps
- Add tests similar to `ophyd_devices/tests/test_virtual_slits.py` for your forward calculation, inverse calculation, and move behavior.
- If your pseudo positioner needs extra config values such as an offset, add them as normal constructor arguments and optional config signals.

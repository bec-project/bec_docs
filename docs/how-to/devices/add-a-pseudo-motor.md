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
    Before writing a new pseudo positioner, check whether `ophyd_devices` already provides one that matches your use case. For example, it already includes pseudo positioners such as `VirtualSlitCenter` and `VirtualSlitWidth`.

## Pre-requisites
- A beamline plugin repository or local `ophyd_devices` development checkout is available.
- The real motors used by the pseudo positioner already exist in the BEC device config.
- You know which real devices your pseudo positioner depends on, for example a monochromator angle motor.

!!! learn "[Learn about pseudo positioners](../../learn/devices/pseudo-positioners.md)"

## 1. Create a new pseudo positioner class

In `ophyd_devices`, pseudo positioners for BEC are typically implemented by subclassing `PSIPseudoMotorBase`. This base class provides the pseudo `readback`, `setpoint`, `motor_is_moving`, and a combined `move()` implementation.

Create a new module for your device, for example `<bec_plugin>.devices.mono_energy.py`:

``` py
from typing import TYPE_CHECKING

import numpy as np
from ophyd_devices.interfaces.base_classes.psi_pseudo_motor_base import PSIPseudoMotorBase

if TYPE_CHECKING:
    from bec_lib.devicemanager import DeviceManagerBase


class MonoEnergy(PSIPseudoMotorBase):
    """Pseudo positioner that exposes monochromator energy in keV."""

    def __init__(
        self,
        name: str,
        theta_motor: str,
        theta_offset_deg: float = 0.0,
        device_manager: DeviceManagerBase,
        **kwargs,
    ) -> None:
        positioners = self.get_positioner_objects(
            name=name,
            positioners={"theta": theta_motor},
            device_manager=device_manager,
        )
        super().__init__(
            name=name,
            device_manager=device_manager,
            positioners=positioners,
            egu="keV",
            **kwargs,
        )

        # Si(111) lattice-plane spacing in angstrom, used in Bragg's law.
        self._d_spacing_angstrom = 3.1356
        self._theta_offset_deg = theta_offset_deg
```

The keys in `positioners={"theta": ...}` are important. They must match the argument names used in the calculation methods you implement next.

## 2. Implement the coordinate transforms

Implement the three required methods:

- `forward_calculation(...)` for mapping the current real motor coordinates to one pseudo coordinate
- `inverse_calculation(position, ...)` for mapping a requested pseudo coordinate back to real motor targets
- `motors_are_moving(...)`

!!! warning
    The pseudo positioner expects that the underlying real devices provide `readback` or `user_readback`, `setpoint` or `user_setpoint`, and `motor_is_moving` signals.

For a Si(111) monochromator, the conversion is based on Bragg's law:

```text
n lambda = 2 d sin(theta)
```

With first-order reflection (`n = 1`) and the photon-energy relation `E [keV] = 12.39841984 / lambda [A]`, you can convert between monochromator angle and energy.

In practice, the motor angle is often not exactly equal to the physical Bragg angle. A calibrated offset is therefore often included in the conversion.

``` py
from ophyd import Signal


class MonoEnergy(PSIPseudoMotorBase):
    ...

    def forward_calculation(self, theta: Signal) -> float:
        theta_deg = theta.get() - self._theta_offset_deg
        theta_rad = np.deg2rad(theta_deg)
        wavelength_angstrom = 2 * self._d_spacing_angstrom * np.sin(theta_rad)
        return float(12.39841984 / wavelength_angstrom)

    def inverse_calculation(self, position: float, theta: Signal) -> dict[str, float]:
        wavelength_angstrom = 12.39841984 / position
        theta_rad = np.arcsin(wavelength_angstrom / (2 * self._d_spacing_angstrom))
        return {"theta": float(np.rad2deg(theta_rad) + self._theta_offset_deg)}

    def motors_are_moving(self, theta: Signal) -> int:
        return int(theta.get())
```

This example assumes first-order Bragg reflection for a Si(111) monochromator and expresses the pseudo position in keV. The value `3.1356` is the Si(111) lattice-plane spacing in angstrom, which is the `d` term in Bragg's law. `theta_offset_deg` is an optional calibration offset between the motor angle and the physical Bragg angle. `PSIPseudoMotorBase.wait_for_connection()` validates these method signatures against the `positioners` keys. If your positioner mapping uses `theta`, then all three methods must accept `theta`.

## 3. Expose the class for discovery

Export the class from your package so it can be referenced from the BEC config.

``` py
from .mono_energy import MonoEnergy
```

If you keep custom devices in a beamline plugin, add the import to that plugin package. If you contribute upstream, add it to `ophyd_devices.__init__.py`.

## 4. Add the pseudo positioner to the BEC config

The pseudo positioner must list its dependent motors in `needs`, and the names in `deviceConfig` must match the constructor arguments of your class.

``` yaml
mono_energy:
  readoutPriority: monitored
  description: Virtual Si(111) monochromator energy
  deviceClass: <bec_plugin>.devices.MonoEnergy
  deviceConfig:
    theta_motor: mono_theta
    theta_offset_deg: 0.15
  deviceTags:
    - motor
  needs:
    - mono_theta
  enabled: true
  readOnly: false
  softwareTrigger: false
```

The `needs` field is required because `get_positioner_objects()` verifies that each dependency is declared in the session config before it resolves the real devices from the device manager.

In this example, `theta_offset_deg` is a beamline-specific calibration parameter. It lets you keep the pseudo energy aligned with the physical Bragg angle even when the motor readback has a small offset.

## 5. Reload BEC and verify the pseudo positioner

Reload the config and reconnect the device server so the new class is imported. Then verify that:

- the pseudo device appears in BEC as `dev.mono_energy`
- `dev.mono_energy.readback.get()` returns the calculated energy
- moving `dev.mono_energy` updates the underlying monochromator angle motor as expected

For example, with a silicon `d` spacing of `3.1356 A`, a monochromator angle near `11.4` degrees corresponds to roughly `10 keV`.

!!! success "Congratulations!"
    You have successfully added a pseudo positioner to BEC. You can now expose derived coordinates such as monochromator energy or other beamline-specific virtual axes as normal motors in scans.

## Common pitfalls
- Forgetting to declare the dependent motors in `needs`. In that case `get_positioner_objects()` will raise a connection error.
- Using calculation method arguments that do not match the `positioners` keys.
- Referencing devices that do not provide `move()`, `readback` or `user_readback`, `setpoint` or `user_setpoint`, and `motor_is_moving`.
- Forgetting to include a calibration offset when the motor angle differs slightly from the physical Bragg angle.
- Forgetting to validate the physical range of your conversion, for example when the requested energy would make the `asin(...)` term invalid.
- Forgetting to export the class from your package, which prevents BEC from importing it from `deviceClass`.

## Next steps
- Add tests similar to `ophyd_devices/tests/test_virtual_slits.py` for your forward calculation, inverse calculation, and move behavior.
- If your pseudo positioner needs extra calibration values such as offsets, add them as normal constructor arguments and config entries.

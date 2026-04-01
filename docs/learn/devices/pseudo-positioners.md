---
related:
  - title: Add a Pseudo Positioner
    url: how-to/devices/add-a-pseudo-motor.md
  - title: EPICS motor classes
    url: learn/devices/epics-motors.md
---

# Pseudo Positioners

Pseudo positioners in `ophyd_devices` expose a derived coordinate while delegating motion to one or more real positioners. In BEC, they are typically implemented by subclassing `ophyd_devices.interfaces.base_classes.PSIPseudoMotorBase`.

`PSIPseudoMotorBase` provides the pseudo `readback`, `setpoint`, `motor_is_moving`, and a combined `move()` implementation. Subclasses supply the coordinate transform logic.

!!! example
    In a slit system, the slit center or slit width is the pseudo coordinate that users want to work with, while the left and right slit blades are the real motors that actually move.

## Required methods

`PSIPseudoMotorBase` expects you to implement three methods. Together, they define how the pseudo coordinate is derived from the current real motor positions, and how a requested pseudo move is translated back into real motor targets.

The important detail is that these methods work with ophyd signal objects, not plain numbers. In practice, that means you normally read each input with `.get()`.

## Forward calculation

/// tab | Info

This is the real-to-pseudo mapping. Start from the current positions of the real motors and calculate the one pseudo value that BEC should show to the user. 

For example, if the real motors are the left and right slit blades, `forward_calculation(...)` can compute the slit center or slit width from their current positions.

BEC uses this method for the pseudo `readback` and pseudo `setpoint`.

```py
def forward_calculation(self, ...) -> float
```
///

/// tab | Example

A simple slit-center implementation averages the left and right blade positions:

```py
def forward_calculation(self, left: Signal, right: Signal) -> float:
    left_pos = left.get()
    right_pos = right.get()
    return float((left_pos + right_pos) / 2)
```
///

## Inverse calculation

/// tab | Info

This is the pseudo-to-real mapping. Start from the pseudo target requested by the user and calculate where each real motor must move so that the pseudo device reaches that target. 

For example, if a user requests a slit center of `4`, `inverse_calculation(...)` must calculate the corresponding target positions for the left and right slit blades.

BEC calls this method during `move()`. The first argument is the requested pseudo target as a `float`. The remaining arguments are the current readback-side signals for the child motors.

The method must return a `dict[str, float]` containing the real motor targets. The dictionary keys must match the names from your `positioners` mapping. If you configured `{"left": ..., "right": ...}`, then you must return `{"left": ..., "right": ...}`.

```py
def inverse_calculation(self, position: float, ...) -> dict[str, float]
```
///

/// tab | Example

This example keeps the current slit width constant while moving the slit center to the requested pseudo target:

```py
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
```
///

## Movement state

/// tab | Info

BEC uses this method to determine whether the pseudo motor should be considered moving. It receives the child motors' `motor_is_moving` signals and should return an `int`.

```py
def motors_are_moving(self, ...) -> int
```
///

/// tab | Example

This example reports the pseudo motor as moving whenever either real motor is moving:

```py
def motors_are_moving(self, left: Signal, right: Signal) -> int:
    return int(left.get() or right.get())
```
///

## Connection and move behavior

`PSIPseudoMotorBase.wait_for_connection()` validates the method signatures against the `positioners` keys. If your positioner mapping uses `left` and `right`, then all three methods must accept `left` and `right`.

During connection and motion, BEC uses the methods in this order:

1. During `wait_for_connection()`, the pseudo motor resolves the child signals from the configured positioners.
2. It connects `forward_calculation()` to the pseudo `readback`.
3. It connects `forward_calculation()` again to the pseudo `setpoint`.
4. It connects `motors_are_moving()` to the pseudo `motor_is_moving`.
5. Later, when you call `move()`, BEC calls `inverse_calculation()` and then moves each child motor to the returned target.

## Device requirements

The underlying real devices must provide:

- `readback` or `user_readback`
- `setpoint` or `user_setpoint`
- `motor_is_moving`
- `move()`

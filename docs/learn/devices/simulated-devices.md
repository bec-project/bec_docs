---
related:
  - title: Use Simulated Models from the IPython Client
    url: how-to/devices/use-simulated-models-from-ipython.md
  - title: Device Config in BEC
    url: learn/devices/device-config-in-bec.md
  - title: Control a Waveform from the IPython client
    url: how-to/gui/control-waveform-from-ipython.md
  - title: Fit Waveform Data with DAP
    url: how-to/gui/fit-waveform-data-with-dap.md
---

# Simulated Devices

Simulated devices are BEC devices whose readback values are produced by a simulation object instead of physical
hardware. They are useful for onboarding, GUI exploration, DAP testing, and safe workflow development.

Not every device is simulated. A device exposes simulation controls only when its device class provides a `sim` object
and exposes it to the client. In the BEC IPython client, that appears as:

```python
dev.<device>.sim
```

For example:

```python
dev.bpm4i.sim
```

## Simulation Interface

The common simulation interface exposes these user-facing controls:

| API | Purpose |
| --- | --- |
| `dev.<device>.sim.get_models()` | List simulation models available for the device. |
| `dev.<device>.sim.select_model("ModelName")` | Select the active simulation model. |
| `dev.<device>.sim.params` | Read or update parameters for the active model. |
| `dev.<device>.sim.show_all()` | Print the active model, parameters, methods, and model list. |

This is runtime state. It is quick to change from the IPython client and is the preferred way to explore a simulated
setup interactively.

## Model Types

The available model names depend on the simulated device type.

1D monitor and waveform simulations use LMFit model classes. A monitor such as `bpm4i` can use names such as
`GaussianModel`, `ConstantModel`, or other available LMFit built-in model class names. BEC DAP uses the same LMFit
model naming style, which is why `GaussianModel` can be used both for simulated `bpm4i` data and for a Waveform DAP
curve.

1D monitor simulations also add BEC-specific parameters:

| Parameter | Purpose |
| --- | --- |
| `ref_motor` | Motor whose current position is used as the model input. |
| `noise` | Noise mode, for example `uniform`, `poisson`, or `none`. |
| `noise_multiplier` | Scale used by the noise model. |

By default, `ref_motor` is `samx`. If your scan uses another motor, update `ref_motor` so the simulated signal follows
the motor you are scanning.

Simulated positioners are different. They simulate positioner behavior, but they do not expose LMFit model selection
for their readback.

2D simulated cameras are also different. They use camera-specific model names such as `constant` and `gaussian`, not
LMFit class names such as `GaussianModel`.

## Runtime Setup and Persistent Defaults

Runtime setup changes the current device object:

```python
dev.bpm4i.sim.select_model("GaussianModel")
dev.bpm4i.sim.params = {"amplitude": 100, "center": 0, "sigma": 1, "ref_motor": "samx"}
```

This is the right approach for exploration, onboarding, demos, and temporary test sessions.

For long-term defaults, put the same setup in the device configuration through `sim_init`. During device
initialization, BEC selects the configured model and applies the configured parameters:

```yaml
bpm4i:
  deviceConfig:
    sim_init:
      model: GaussianModel
      params:
        amplitude: 100
        center: 0
        sigma: 1
        ref_motor: samx
```

Use `sim_init` when a simulated device should always start with the same model in a beamline, plugin, or test
configuration.

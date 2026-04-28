---
related:
  - title: GUI tasks from the BEC IPython client
    url: how-to/gui/ipython-client-gui.md
  - title: Control a Waveform from the IPython client
    url: how-to/gui/control-waveform-from-ipython.md
  - title: Script GUI setup and run a line scan
    url: how-to/gui/script-gui-setup-and-run-line-scan.md
  - title: LMFit built-in models
    url: https://lmfit.github.io/lmfit-py/builtin_models.html
---

# Use Simulated Models from the IPython Client

!!! info "Goal"

    Configure a simulated device model at runtime so you can explore GUI and DAP workflows in a
    safe environment.

## Prerequisites

- BEC is running with the simulated `bpm4i` device.
- The device exposes the simulation interface as `dev.bpm4i.sim`.

## 1. Select the simulation model

Set `bpm4i` to report values from a Gaussian simulation model:

```python
dev.bpm4i.sim.select_model("GaussianModel")
```

The model names follow the LMFit built-in model class names. The same names are also shipped
as the default BEC DAP model names.

See the [LMFit built-in models](https://lmfit.github.io/lmfit-py/builtin_models.html) for
available model classes and parameters.

## 2. Set the model parameters

Set the Gaussian parameters:

```python
dev.bpm4i.sim.params = {"amplitude": 100, "center": 0, "sigma": 1}
```

## 3. Use the simulated device in a Waveform

Plot the simulated device and attach the matching DAP model:

```python
wf = gui.bec.new(gui.available_widgets.Waveform)
wf.plot(device_x=dev.samx, device_y=dev.bpm4i, dap="GaussianModel")
scans.line_scan(dev.samx, -5, 5, steps=25, exp_time=0.1, relative=False)
```

Inspect the DAP output:

```python
wf.get_dap_summary()
```

!!! success "Result"

    The simulated `bpm4i` signal produces Gaussian-shaped data, and the Waveform can display
    both the measured curve and the DAP fit.

## Make the simulation persistent

Prefer runtime setup from the IPython client while developing or onboarding users. Use device
configuration only when the simulation should be the long-term default for a beamline or test
configuration.

In that case, define `sim_init` inside the full device configuration:

```yaml
bpm4i:
  deviceConfig:
    sim_init:
      model: GaussianModel
      params:
        amplitude: 100
        center: 0
        sigma: 1
```

---
related:
  - title: Create Dock Area profiles from the BEC IPython client
    url: getting-started/next-steps/create-dock-area-profiles-from-ipython.md
  - title: RPC GUI Control
    url: learn/gui/rpc-gui-control.md
  - title: GUI RPC Interface
    url: references/bec-widgets/gui-rpc-interface.md
---

# Plotting and Data Analysis from the BEC IPython Client

Use these guides when you want to plot live data, inspect scan history, fit curves with DAP, or combine BEC Widgets
with ordinary Python analysis from the BEC IPython client.

If you are new to the `gui` object, read [RPC GUI Control](../../learn/gui/rpc-gui-control.md){ data-preview } for the
underlying command model. To create and switch Dock Area profiles from commands, use
[Create Dock Area Profiles from the BEC IPython Client](../../getting-started/next-steps/create-dock-area-profiles-from-ipython.md){ data-preview }.

## Choose the right task

| Situation | Use this guide | What it gives you |
| --- | --- | --- |
| You want to plot live device data or style Waveform curves. | [Control a Waveform from the IPython Client](control-waveform-from-ipython.md) | Creates and configures Waveform plots from BEC IPython commands. |
| You want to attach DAP models to plotted data. | [Fit Waveform Data with DAP](fit-waveform-data-with-dap.md) | Adds one or more DAP model curves and reads fit parameters. |
| You want to inspect data from an already completed scan. | [Access History with a Waveform](access-history-with-waveform.md) | Plots history data in Waveform or reads raw values from `bec.history`. |
| You tried useful commands interactively and want to reuse them. | [Script GUI Interactions](../../getting-started/next-steps/script-gui-interactions.md) | Turns plotting and light analysis steps into a small Python function. |
| You need predictable data for plotting or DAP examples. | [Use Simulated Models from the IPython Client](../devices/use-simulated-models-from-ipython.md) | Configures simulated device output before plotting it. |

## Common plotting workflow

Most command-line plotting work follows this order:

1. Configure a real or
   [simulated device signal](../devices/use-simulated-models-from-ipython.md){ data-preview }.
2. [Plot live data in a Waveform](control-waveform-from-ipython.md){ data-preview }.
3. [Add a DAP curve](fit-waveform-data-with-dap.md){ data-preview } when you need a fitted model.
4. [Inspect scan history](access-history-with-waveform.md){ data-preview } when you need to compare with previous scans.
5. Read plotted data back from the Waveform with `wf.get_all_data()` for quick checks or small transformations.
6. Move repeated commands into a
   [small script](../../getting-started/next-steps/script-gui-interactions.md){ data-preview } only after the
   interactive workflow is useful.

## Learning material

- [RPC GUI Control](../../learn/gui/rpc-gui-control.md){ data-preview } explains how GUI command objects work.
- [GUI RPC Interface](../../references/bec-widgets/gui-rpc-interface.md){ data-preview } lists common exposed methods.

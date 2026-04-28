---
related:
  - title: Dock Area Profiles
    url: getting-started/next-steps/dock-area-profiles-tutorial.md
  - title: BEC IPython GUI Commands
    url: getting-started/next-steps/gui-cli-interface.md
  - title: Learn how Dock Area profiles work
    url: learn/gui/dock-area-profiles/index.md
---

# Create Dock Area Profiles from the BEC IPython Client

!!! info "Goal"

    Save, modify, and switch Dock Area profiles from the BEC IPython client.

This tutorial creates the same `alignment_scan` and `motor_check` profiles as
[Dock Area Profiles](dock-area-profiles-tutorial.md){ data-preview }, but uses BEC IPython commands instead of toolbar
actions.

## Before you start

Open BEC with `Terminal + Dock`, as shown in
[01 Open BEC](../quick-start/01-open-bec.md){ data-preview }.

Start with a dock area containing a **ScanControl** and a **Waveform** widgets. This is the layout created in
[06 Create Your First GUI](../quick-start/06-create-your-first-gui.md){ data-preview }.

## 1. Save the current layout

Save the current dock area as `alignment_scan`:

```python
gui.bec.save_profile("alignment_scan", quick_select=True)
```

The profile is saved and included in the toolbar quick selector.

## 2. Add widgets for the second layout

Add a second Waveform to the right of the first one:

```python
wf2 = gui.bec.new(
    gui.available_widgets.Waveform,
    where="right",
    relative_to="Waveform",
)
wf2.plot(device_x="samx", device_y="bpm4i")
```

Add a PositionerBox below the first Waveform and set it to `samx`:

```python
pos_samx = gui.bec.new(
    gui.available_widgets.PositionerBox,
    where="bottom",
    relative_to="Waveform",
)
pos_samx.set_positioner("samx")
```

Add another PositionerBox below the second Waveform and set it to `samy`:

```python
pos_samy = gui.bec.new(
    gui.available_widgets.PositionerBox,
    where="bottom",
    relative_to="Waveform_0",
)
pos_samy.set_positioner("samy")
```

!!! tip "Place widgets relative to existing widgets"

    The `relative_to` argument accepts an existing widget reference or a widget name. Use the name shown on the dock tab,
    for example `"Waveform"`, `"ScanControl"`, or `"PositionerBox"`.

    If the same widget type appears multiple times in the same layout, Dock Area starts indexing those names. The first
    widget keeps the base name without an index, and the next ones use indexed names such as `"Waveform_0"` and
    `"Waveform_1"`.

## 3. Save the second profile

Save the modified dock area as `motor_check`:

```python
gui.bec.save_profile("motor_check", quick_select=True)
```

## 4. Switch between profiles

Load the first profile:

```python
gui.bec.load_profile("alignment_scan")
```

Load the second profile:

```python
gui.bec.load_profile("motor_check")
```

!!! success "What you have learned"

    You used BEC IPython commands to save, modify, and switch Dock Area profiles.

## Next step

Use [Script GUI Setup and Run a Line Scan](../../how-to/gui/script-gui-setup-and-run-line-scan.md){ data-preview } when
you need a reusable script that creates a GUI layout and starts a scan.

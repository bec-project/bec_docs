---
related:
  - title: Plot your first waveform
    url: getting-started/quick-start/05-plot-your-first-waveform.md
  - title: Dock Area Profiles
    url: getting-started/next-steps/dock-area-profiles-tutorial.md
  - title: Create Dock Area profiles from the BEC IPython client
    url: getting-started/next-steps/create-dock-area-profiles-from-ipython.md
  - title: Learn about RPC GUI control
    url: learn/gui/rpc-gui-control.md
---

# BEC IPython GUI Commands

!!! info "Goal"

    Learn the BEC IPython objects used to inspect, create, and control GUI widgets.

This page is a short orientation before the longer GUI command tutorials. It explains which objects are available in
the BEC IPython client and how to discover the commands they expose.

## Before you start

Open BEC with `Terminal + Dock`, as shown in
[01 Open BEC](../quick-start/01-open-bec.md){ data-preview }.

You should have a BEC IPython session and a dock area window.

## The `gui` object

The BEC IPython client provides a `gui` object:

```python
gui
```

Use it as the entry point for GUI windows, available widget classes, and the default dock area.

## The default dock area

The dock area opened by `Terminal + Dock` is available as:

```python
gui.bec
```

This object lets you add widgets, inspect widgets, load profiles, save profiles, and clear the dock area.

## Available widgets

List the widget classes that can be created from BEC IPython:

```python
gui.available_widgets
```

Create a widget by passing one of those classes to `gui.bec.new(...)`:

```python
wf = gui.bec.new(gui.available_widgets.Waveform)
```

## Widget references

The variable returned by `gui.bec.new(...)` is a reference to the widget in the GUI process. Use it to call exposed
widget methods:

```python
wf.plot(device_x=dev.samx, device_y=dev.bpm4i)
```

Created widgets are also available from the dock area namespace:

```python
gui.bec.Waveform
```

## Discover commands

Use IPython tab completion to inspect available commands:

```python
wf.
```

Then press ++tab++.

Use `?` to inspect parameters and documentation:

```python
wf.plot?
gui.bec.new?
gui.bec.save_profile?
```

!!! note "What is exposed"

    BEC IPython only exposes stable user-facing widget methods. Internal Qt implementation details are not exposed.

## Where to go next

- Use [Dock Area Profiles](dock-area-profiles-tutorial.md){ data-preview } to learn the profile workflow by clicking in
  the GUI.
- Use [Create Dock Area Profiles from the BEC IPython Client](create-dock-area-profiles-from-ipython.md){ data-preview }
  to learn the same profile workflow from commands.
- Use [Control a Waveform from the IPython Client](../../how-to/gui/control-waveform-from-ipython.md){ data-preview }
  for a focused Waveform task.
- Use [RPC GUI Control](../../learn/gui/rpc-gui-control.md){ data-preview } when you want the underlying concept.

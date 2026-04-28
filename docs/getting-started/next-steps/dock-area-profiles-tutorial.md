---
related:
  - title: Switch Dock Area profiles
    url: how-to/gui/switch-dock-area-profile.md
  - title: Toggle Dock Area profile quick selection
    url: how-to/gui/toggle-dock-area-profile-quick-selection.md
  - title: Restore a Dock Area profile to its baseline
    url: how-to/gui/restore-dock-area-profile-baseline.md
  - title: Delete a Dock Area profile
    url: how-to/gui/delete-dock-area-profile.md
  - title: Share a Dock Area profile with other accounts
    url: how-to/gui/share-dock-area-profile-with-other-accounts.md
  - title: Learn how Dock Area profiles work
    url: learn/gui/dock-area-profiles/index.md
  - title: Create Dock Area profiles from the BEC IPython client
    url: getting-started/next-steps/create-dock-area-profiles-from-ipython.md
---

# Dock Area Profiles

!!! info "Goal"

    In this tutorial you will save two dock area reusable configurations as Dock Area profiles and switch between them.

!!! tip "What is a Dock Area profile?"

    A Dock Area profile is a saved configuration of the dock area, including the widgets it contains and their configuration.
    Profiles allow you to quickly switch between different GUI setups for different tasks.
    Learn more about how profiles work in [Dock Area Profiles](../../learn/gui/dock-area-profiles/index.md){ data-preview }.

This tutorial continues from [06 Create Your First GUI](../quick-start/06-create-your-first-gui.md){ data-preview }.
Start with BEC open in the `Terminal + Dock` interface and a dock area containing a **ScanControl** and a **Waveform** widgets.

## 1. Save the current layout

In the dock area toolbar, click the save button :material-content-save-outline:.

Enter the profile name:

```
alignment_scan
```

Keep `Include in quick selection` enabled, then click `Save`.

![save_profile.gif](../assets/save_profile.gif)

The profile name appears in the profile selector in the dock area toolbar.

## 2. Change the layout and add more widgets

Create a second layout that is easy to recognize when you switch profiles:

1. Open `Add Device Control` and add twice `PositionerBox`.
2. Open `Add Plot` and add another `Waveform`.
3. Move the new widgets to the right side of the dock area.

You should now have the original scan control and waveform plot, plus two positioner boxes and
a second waveform plot.

![profile_new_layout.gif](../assets/profile_new_layout.gif)

## 3. Save a second profile

Click the save button again :material-content-save-outline:.

Enter the profile name:

```
motor_check
```

Keep `Include in quick selection` enabled, then click `Save`.

![save_second_profile.gif](../assets/save_second_profile.gif)

## 4. Switch between profiles

Use the profile selector in the dock area toolbar to switch back to `alignment_scan`.

The dock area reloads the layout saved in the first profile. Use the selector again to switch to `motor_check`.

![profile_switch.gif](../assets/profile_switch.gif)

!!! success "What you have learned"

    You have saved two Dock Area profiles and used the dock area toolbar to switch between different layouts.

## Next step

To create the same profiles from commands, use
[Create Dock Area Profiles from the BEC IPython Client](create-dock-area-profiles-from-ipython.md){ data-preview }.

To remove a local profile, use [Delete a Dock Area Profile](../../how-to/gui/delete-dock-area-profile.md){ data-preview }.
For a background on profile inspection, storage, and sharing, see
[Dock Area Profiles](../../learn/gui/dock-area-profiles/index.md){ data-preview }.

---
related:
  - title: Manage GUI profiles
    url: how-to/gui/manage-gui-profiles.md
  - title: Share a GUI profile with other accounts
    url: how-to/gui/share-gui-profile-with-other-accounts.md
  - title: Learn how GUI profiles are stored
    url: learn/gui/gui-profiles.md
---

# Save and Switch GUI Profiles

!!! info "Goal"

    In this tutorial you will save two dock area reusable configurations as GUI profiles and switch between them.

This tutorial continues from [06 Create Your First GUI](../quick-start/06-create-your-first-gui.md){ data-preview }.
Start with BEC open in the `Terminal + Dock` interface and a dock area containing a scan control and a waveform plot.

## 1. Save the current layout

In the dock area toolbar, click the save button.

Enter the profile name:

```
alignment_scan
```

Keep `Include in quick selection` enabled, then click `Save`.

![save_profile.gif](../assets/save_profile.gif)

The profile name appears in the profile selector in the dock area toolbar.

## 2. Change the layout and add more widgets

Add another widget to make a visibly different workspace. For example, open `Add Device Control` and add a
`PositionerBox` and also add another `Waveform` plot from the `Add Plot` menu.

Arrange and configure the widgets so this layout and settings are different from the first one.

![profile_new_layout.gif](../assets/profile_new_layout.gif)

## 3. Save a second profile

Click the save button again.

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

    You have saved two GUI profiles and used the dock area toolbar to switch between different layouts.

## Next step

To manage, delete, or inspect saved profiles, see [Manage GUI Profiles](../../how-to/gui/manage-gui-profiles.md). For
a background on where profiles are stored and how shared profiles are deployed,
see [GUI Profiles](../../learn/gui/gui-profiles.md).

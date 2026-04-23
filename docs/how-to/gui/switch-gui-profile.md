---
related:
  - title: Toggle GUI profile quick selection
    url: how-to/gui/toggle-gui-profile-quick-selection.md
  - title: Delete a GUI profile
    url: how-to/gui/delete-gui-profile.md
  - title: Learn about the profile manager
    url: learn/gui/profile-manager.md
---

# Switch GUI Profiles

!!! Info "Goal"

    Load a saved GUI profile into the dock area.

## Prerequisites

- You have BEC open with a dock area.
- The profile you want to load is already available.

If you do not have profiles yet, first create one with
[Save and Switch GUI Profiles](../../getting-started/next-steps/save-and-switch-gui-profiles.md){ data-preview }.

## Option 1: Switch from the quick selector

Use the quick selector when the profile is listed in the dock area toolbar. This is the shortest way to switch profiles.

Open the profile selector in the dock area toolbar and select the profile you want to load.

![profile_switch.gif](../../getting-started/assets/profile_switch.gif)

The dock area loads the selected profile and replaces the current layout.

!!! note "Quick selection"

    Not every profile is shown in the quick selector. A profile only appears there when quick selection is enabled for that
    profile. Learn how to control this with [Toggle GUI Profile Quick Selection](toggle-gui-profile-quick-selection.md){ data-preview }.

## Option 2: Switch from the profile manager

Use the profile manager when the profile is not listed in the quick selector, or when you want to check the profile
preview and metadata before loading it.

!!! learn "[Learn more about the profile manager](../../learn/gui/profile-manager.md){ data-preview }"

### 1. Open the profile manager

Click the **manage button** :material-account-cog: in the dock area toolbar.

![dock_area_toolbar_profile_manager.png](assets/dock_area_toolbar_profile_manager.png)

### 2. Select the profile

Click the profile you want to load.

Use the preview and metadata panel to confirm that you selected the correct profile.

![dock_area_manager.png](assets/dock_area_manager.png)

### 3. Switch to the profile

Click the **switch profile button** :material-play-circle-outline:.

The selected profile is loaded into the dock area and replaces the current layout. The active profile is shown with the
filled green **switch profile button** icon <span style="color: green;">:material-play-circle:</span>.

## Option 3: Switch from the BEC IPython client

Use the BEC IPython client when you want to load a profile from a command or script.

You can load the same profile from the `BECDockArea` object in the BEC IPython client:

```python
gui.bec.load_profile("profile_name")
```

Replace `profile_name` with the name shown in the profile manager.

!!! success "Result"

    The dock area now uses the layout saved in the selected profile.

## Common Pitfalls

- Switching profiles replaces the current dock area layout with the saved layout from the selected profile.
- If the profile does not appear in the quick selector, open the profile manager and switch from there.
- To make a profile appear in the quick selector, enable quick selection for that profile. Learn how to do that with
  [Toggle GUI Profile Quick Selection](toggle-gui-profile-quick-selection.md){ data-preview }.

## Next Steps

- Use [Toggle GUI Profile Quick Selection](toggle-gui-profile-quick-selection.md){ data-preview } to control whether a profile appears
  in the toolbar selector.
- Use [Restore a GUI Profile to Its Default](restore-gui-profile-default.md){ data-preview } when you want to discard local layout
  changes for the active profile.

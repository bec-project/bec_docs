---
related:
  - title: Dock Area Profiles
    url: learn/gui/dock-area-profiles/index.md
  - title: Runtime and baseline profile copies
    url: learn/gui/dock-area-profiles/runtime-and-baseline-copies.md
  - title: Switch Dock Area profiles
    url: how-to/gui/switch-dock-area-profile.md
  - title: Toggle Dock Area profile quick selection
    url: how-to/gui/toggle-dock-area-profile-quick-selection.md
  - title: Delete a Dock Area profile
    url: how-to/gui/delete-dock-area-profile.md
  - title: Share a Dock Area profile with other accounts
    url: how-to/gui/share-dock-area-profile-with-other-accounts.md
---

# The Dock Area Profile Manager

Use the profile manager when you want to inspect available profiles, check profile metadata, or act on a profile from
the GUI.

## Open the profile manager

Open the profile manager with the **manage button** :material-account-cog: in the dock area toolbar.

![dock_area_toolbar_profile_manager.png](../../../how-to/gui/assets/dock_area_toolbar_profile_manager.png)

The profile manager shows the available profiles, profile actions, profile metadata, and a screenshot preview.

![dock_area_manager.png](../../../how-to/gui/assets/dock_area_manager.png)

## Main areas of the profile manager

The profile manager has four main parts:

- the **Actions** column with the buttons for switching, toggling quick selection, and deleting
- the profile list, including the profile name and author
- the metadata panel for the selected profile
- the screenshot preview for the selected profile

## Actions in the profile manager

| Button | Meaning |
| --- | --- |
| **switch profile button** :material-play-circle-outline: | Load the selected profile into the dock area. |
| **toggle quick selection button** :material-star-outline: | Show or hide the profile in the toolbar quick selector. |
| **delete button** :material-trash-can-outline: | Delete a writable local profile. This button is disabled for bundled read-only profiles. |

Use the task pages when you want the step-by-step workflow:

- [Switch Dock Area Profiles](../../../how-to/gui/switch-dock-area-profile.md)
- [Toggle Dock Area Profile Quick Selection](../../../how-to/gui/toggle-dock-area-profile-quick-selection.md)
- [Delete a Dock Area Profile](../../../how-to/gui/delete-dock-area-profile.md)

## Metadata shown for the selected profile

| Field | Meaning |
| --- | --- |
| `Name` | The saved profile name. |
| `Author` | The saved author metadata when available. |
| `Created` | When the profile was first saved. |
| `Modified` | When the selected profile copy was last updated. |
| `Quick select` | Whether the profile appears in the toolbar quick selector. |
| `Widgets` | The number of widgets stored in the profile. |
| `Size (KB)` | The file size of the selected profile data. |
| `Runtime path` | The path to the editable runtime profile. Use this when you need the current `.ini` file for sharing or inspection. |
| `Baseline path` | The path to the baseline profile used when restoring runtime changes. |

The screenshot preview is stored in the profile file when a screenshot is available during save.

For the workflow that uses the `Runtime path` field, see
[Share a Dock Area Profile with Other Accounts](../../../how-to/gui/share-dock-area-profile-with-other-accounts.md).

## Inspect available profiles from the BEC IPython client

To inspect which profiles are available in the current dock area namespace from the BEC IPython client, call:

```python
gui.bec.list_profiles()
```

This returns the available profile names for the current namespace.

Use the Dock Area profile manager when you need more than the names, such as metadata, the screenshot preview, or the
`Runtime path` and `Baseline path` fields.

## Related topics

- To learn what profiles are, see [Dock Area Profiles](index.md).
- To learn how runtime and baseline profile copies behave, see
  [Runtime and Baseline Copies](runtime-and-baseline-copies.md).

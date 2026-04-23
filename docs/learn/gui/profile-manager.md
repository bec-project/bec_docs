---
related:
  - title: Learn what a GUI profile contains
    url: learn/gui/gui-profiles.md
  - title: Learn about user and default profile copies
    url: learn/gui/gui-profile-copies-and-namespaces.md
  - title: Switch GUI profiles
    url: how-to/gui/switch-gui-profile.md
  - title: Toggle GUI profile quick selection
    url: how-to/gui/toggle-gui-profile-quick-selection.md
  - title: Delete a GUI profile
    url: how-to/gui/delete-gui-profile.md
  - title: Share a GUI profile with other accounts
    url: how-to/gui/share-gui-profile-with-other-accounts.md
---

# The GUI Profile Manager

Use the profile manager when you want to inspect available profiles, check profile metadata, or act on a profile from
the GUI.

## Open the profile manager

Open the profile manager with the **manage button** :material-account-cog: in the dock area toolbar.

![dock_area_toolbar_profile_manager.png](../../how-to/gui/assets/dock_area_toolbar_profile_manager.png)

The profile manager shows the available profiles, profile actions, profile metadata, and a screenshot preview.

![dock_area_manager.png](../../how-to/gui/assets/dock_area_manager.png)

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

- [Switch GUI Profiles](../../how-to/gui/switch-gui-profile.md)
- [Toggle GUI Profile Quick Selection](../../how-to/gui/toggle-gui-profile-quick-selection.md)
- [Delete a GUI Profile](../../how-to/gui/delete-gui-profile.md)

## Metadata shown for the selected profile

| Field | Meaning |
| --- | --- |
| `Name` | The saved profile name. |
| `Author` | The saved author metadata when available. |
| `Created` | When the profile was first saved. |
| `Modified` | When the selected copy was last updated. |
| `Quick select` | Whether the profile appears in the toolbar quick selector. |
| `Widgets` | The number of widgets stored in the profile. |
| `Size (KB)` | The file size of the selected profile data. |
| `User path` | The path to the writable user copy. Use this when you need the original `.ini` file for sharing or inspection. |
| `Default path` | The path to the default baseline copy used for restore. |

The screenshot preview is stored in the profile file when a screenshot is available during save.

For the workflow that uses the `User path` field, see
[Share a GUI Profile with Other Accounts](../../how-to/gui/share-gui-profile-with-other-accounts.md).

## Inspect available profiles from the BEC IPython client

To inspect which profiles are available in the current dock area namespace from the BEC IPython client, call:

```python
gui.bec.list_profiles()
```

This returns the available profile names for the current namespace.

Use the GUI profile manager when you need more than the names, such as metadata, the screenshot preview, or the
`User path` and `Default path` fields.

## Related topics

- To learn what the profile file contains and how it is restored, see [GUI Profiles](gui-profiles.md).
- To learn how user and default copies behave, see [GUI Profile Copies and Namespaces](gui-profile-copies-and-namespaces.md).

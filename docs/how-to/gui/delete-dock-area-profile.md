---
related:
  - title: Switch Dock Area profiles
    url: how-to/gui/switch-dock-area-profile.md
  - title: Restore a Dock Area profile to its baseline
    url: how-to/gui/restore-dock-area-profile-baseline.md
  - title: Share a Dock Area profile with other accounts
    url: how-to/gui/share-dock-area-profile-with-other-accounts.md
  - title: Learn about profile origins and metadata
    url: learn/gui/dock-area-profiles/runtime-and-baseline-copies.md#profile-origins
---

# Delete a Dock Area Profile

!!! Info "Goal"

    Delete a locally created Dock Area profile from the dock area profile manager.

## Prerequisites

- You have BEC open with a dock area.
- The profile you want to delete was created locally.

If you do not have profiles yet, first create one with
[Save and Switch Dock Area Profiles](../../getting-started/next-steps/dock-area-profiles-tutorial.md){ data-preview }.

Read-only profiles from BEC Widgets or the beamline plugin repository cannot be deleted from the GUI.

## 1. Open the profile manager

Click the manage button :material-account-cog: in the dock area toolbar.

![dock_area_toolbar_profile_manager.png](assets/dock_area_toolbar_profile_manager.png)

## 2. Select the profile

Click the profile you want to delete.

Check the metadata panel before deleting. Profiles from the local settings area can be deleted; bundled read-only
profiles cannot.

![dock_area_manager.png](assets/dock_area_manager.png)

!!! learn "[Learn more about the profile manager fields](../../learn/gui/dock-area-profiles/profile-manager.md){ data-preview }"

!!! learn "[Learn about Dock Area profile origins](../../learn/gui/dock-area-profiles/runtime-and-baseline-copies.md#profile-origins){ data-preview }"

    The profile origin controls whether the profile can be deleted from the profile manager.

## 3. Delete the profile

Click the delete button <span style="color: red;">:material-trash-can-outline:</span>.

Confirm the deletion when prompted.

Deleting a profile removes the writable copy from the local settings area.

## 4. Delete from the BEC IPython client

You can delete a local profile from the `BECDockArea` object in the BEC IPython client:

```python
gui.bec.delete_profile("profile_name")
```

Replace `profile_name` with the name shown in the profile manager.

!!! success "Result"

    The local profile is removed from the profile manager and no longer appears in the toolbar selector.

## Common Pitfalls

- The delete button is disabled for read-only profiles.
- Deleting a local profile cannot be undone from the profile manager.
- To make a useful profile available to other accounts, share it through the plugin repository before deleting your
  local copy.

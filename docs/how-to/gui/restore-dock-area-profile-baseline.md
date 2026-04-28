---
related:
  - title: Switch Dock Area profiles
    url: how-to/gui/switch-dock-area-profile.md
  - title: Toggle Dock Area profile quick selection
    url: how-to/gui/toggle-dock-area-profile-quick-selection.md
  - title: Runtime and baseline profile copies
    url: learn/gui/dock-area-profiles/runtime-and-baseline-copies.md
---

# Restore a Dock Area Profile to Its Baseline

!!! Info "Goal"

    Replace the current runtime profile with its saved baseline profile.

## Prerequisites

- You have BEC open with a dock area.
- The profile you want to restore is the active profile.

If you do not have profiles yet, first create one with
[Dock Area Profiles](../../getting-started/next-steps/dock-area-profiles-tutorial.md){ data-preview }.

## 1. Activate the profile

Load the profile you want to restore.

Use [Switch Dock Area Profiles](switch-dock-area-profile.md) if you need to activate a different profile first.

## 2. Start the restore action

Click the reset button :material-arrow-u-left-top: in the dock area toolbar.

![restore_profile_toolbar.png](assets/restore_profile_toolbar.png)

The dock area shows a confirmation dialog with previews of the current layout and the saved baseline layout.

![restore_profile_dialog.png](assets/restore_profile_dialog.png)

## 3. Confirm the restore

Check the previews in the confirmation dialog.

Confirm the restore only if you want to replace the current runtime profile with the saved baseline profile.

When you confirm, BEC restores the runtime profile from the baseline profile and reloads the dock area.

!!! learn "[Learn about runtime and baseline profiles](../../learn/gui/dock-area-profiles/runtime-and-baseline-copies.md){ data-preview }"

    The Learn page explains how BEC stores runtime and baseline profiles, and why bundled profiles behave differently
    from locally created profiles.

!!! success "Result"

    The dock area uses the saved baseline layout for the restored profile.

## Restore from the BEC IPython client

Use the IPython client when a script should restore a known baseline profile without opening the confirmation dialog:

```python
gui.bec.restore_baseline_profile("alignment_cli", show_dialog=False)
```

Use [BEC IPython GUI Commands](../../getting-started/next-steps/gui-cli-interface.md){ data-preview }
for the introductory BEC IPython command workflow.

## Common Pitfalls

- Restoring a profile discards the current runtime profile for that profile.
- For locally created profiles, saving again with the same name and confirming the overwrite updates the saved baseline
  profile.
- Profiles from the beamline plugin repository and profiles bundled with BEC Widgets are read-only; their bundled
  baselines cannot be overwritten from the GUI.

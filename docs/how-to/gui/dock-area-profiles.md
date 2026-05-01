---
related:
  - title: Add Widgets to a Dock Area
    url: how-to/gui/add-widgets-to-dock-area.md
  - title: Dock Area Profiles
    url: getting-started/next-steps/dock-area-profiles-tutorial.md
  - title: Create Dock Area profiles from the BEC IPython client
    url: getting-started/next-steps/create-dock-area-profiles-from-ipython.md
  - title: Learn how Dock Area profiles work
    url: learn/gui/dock-area-profiles/index.md
---

# Dock Area Tasks

Use these guides when you need to add widgets to a Dock Area or manage Dock Area profiles.

If you are new to the Dock Area itself, start with
[06 Create Your First GUI](../../getting-started/quick-start/06-create-your-first-gui.md){ data-preview }. If you are
new to working with profiles, continue with
[Dock Area Profiles](../../getting-started/next-steps/dock-area-profiles-tutorial.md){ data-preview }.

## Choose the right task

| Situation                                                        | Use this guide                                                                                  | What it changes                                                       |
|------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| You want to add another tool to the current Dock Area.           | [Add Widgets to a Dock Area](add-widgets-to-dock-area.md)                                       | Creates a widget and places it in the current Dock Area.              |
| You want to use a different saved layout now.                    | [Switch Dock Area Profiles](switch-dock-area-profile.md)                                        | Loads another profile into the current Dock Area.                     |
| The profile exists, but it is missing from the toolbar selector. | [Toggle Dock Area Profile Quick Selection](toggle-dock-area-profile-quick-selection.md)         | Shows or hides the profile in the quick selector without deleting it. |
| The active profile has local layout changes you want to discard. | [Restore a Dock Area Profile to Its Baseline](restore-dock-area-profile-baseline.md)            | Replaces the runtime profile with its saved baseline.                 |
| A local profile is no longer useful.                             | [Delete a Dock Area Profile](delete-dock-area-profile.md)                                       | Removes the writable local profile from the profile manager.          |
| Another e-account or beamline deployment needs the same profile. | [Share a Dock Area Profile with Other Accounts](share-dock-area-profile-with-other-accounts.md) | Copies the profile directly or adds it to the plugin repository.      |

## Common Dock Area workflow

Most Dock Area work follows this order:

1. Create an initial Dock Area in
   [06 Create Your First GUI](../../getting-started/quick-start/06-create-your-first-gui.md){ data-preview }.
2. Add widgets manually or with
   [BEC IPython commands](add-widgets-to-dock-area.md){ data-preview }.
3. Save useful layouts as profiles with the
   [Dock Area Profiles](../../getting-started/next-steps/dock-area-profiles-tutorial.md){ data-preview }
   tutorial.
4. [Switch between profiles](switch-dock-area-profile.md){ data-preview } during normal work.
5. [Adjust quick selection](toggle-dock-area-profile-quick-selection.md){ data-preview } so the toolbar only shows the
   profiles you use often.
6. [Restore a profile](restore-dock-area-profile-baseline.md){ data-preview } when runtime changes should be discarded.
7. [Share useful profiles](share-dock-area-profile-with-other-accounts.md){ data-preview } before deleting local copies.

The [profile manager](../../learn/gui/dock-area-profiles/profile-manager.md){ data-preview } is the safest place to
inspect profile metadata before changing or deleting a profile.

## Learning material

- [Dock Area Profiles](../../learn/gui/dock-area-profiles/index.md){ data-preview } explains what profiles are.
- [Runtime and Baseline Copies](../../learn/gui/dock-area-profiles/runtime-and-baseline-copies.md){ data-preview }
  explains profile storage, origins, and restore behavior.

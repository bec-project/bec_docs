---
related:
  - title: Learn what a GUI profile contains
    url: learn/gui/gui-profiles.md
  - title: Learn about the GUI profile manager
    url: learn/gui/profile-manager.md
  - title: Restore a GUI profile to its default
    url: how-to/gui/restore-gui-profile-default.md
  - title: Share a GUI profile with other accounts
    url: how-to/gui/share-gui-profile-with-other-accounts.md
---

# GUI Profile Copies and Namespaces

This page explains how BEC manages writable and default profile copies, where bundled profiles come from, and how dock
area namespaces keep different profile sets separate.

## User and default copies

When a new profile is saved, BEC writes two copies:

- a `default` copy
- a `user` copy

The `user` copy is the editable working copy. The `default` copy is the baseline used when the profile is restored to
its default layout.

When switching profiles, BEC saves the current layout to the selected profile's `user` copy before loading the next
profile.

For locally created profiles, saving again with the same name and confirming the overwrite updates both the `user` copy
and the `default` copy. This means the restore point for that local profile becomes the latest saved layout.

## How loading chooses a profile copy

When BEC loads a profile, it prefers the `user` copy. If no `user` copy exists, it falls back to the `default` copy.

This is why local changes to a profile are loaded again on the next switch, even when the profile originally came from a
bundled default.

## Profile origins

GUI profiles have three origins:

| Origin          | Source                                   | Delete?          | Overwrite default? |
|-----------------|------------------------------------------|------------------|--------------------|
| Local settings  | Active BEC widgets settings profile root | :material-check: | :material-check:   |
| Beamline plugin | `<beamline_repo>/bec_widgets/profiles/`  | :material-close: | :material-close:   |
| BEC Widgets     | Built-in BEC Widgets profiles            | :material-close: | :material-close:   |

The profile manager uses the origin to decide whether the delete action is enabled and whether the profile is treated as
read-only.

## Bundled profiles

BEC also discovers read-only bundled profiles from:

- BEC Widgets built-in profiles
- the active plugin repository profile directory

The preferred beamline plugin repository profile directory is:

```text
<beamline_repo>/bec_widgets/profiles/
```

For plugin repositories that keep widget resources inside the Python package, BEC also checks:

```text
<beamline_repo>/<plugin_package>/bec_widgets/profiles/
```

Use the top-level `bec_widgets/profiles/` directory for new shared profiles unless your
plugin already stores widget-specific resources inside the package directory.

When BEC discovers one of these bundled profiles, it ensures that namespace-specific copies exist in the writable
settings area. It creates both a namespace-specific `default` copy and a namespace-specific `user` copy so the GUI can
load the profile and track local changes in the writable area.

The bundled default itself still remains read-only in origin.

## Namespace-specific profile directories

Within the writable profile root, BEC stores profiles in separate namespace directories below `user/` and `default/`.

The purpose of the namespace is to distinguish different subsets of profiles for different dock areas. This lets BEC
keep one set of profiles for one type of dock area and a different set for another type of dock area, instead of mixing
all profiles into one shared list.

In practice, a namespaced profile layout looks like this:

```text
widget_settings/profiles/
  default/<namespace>/<profile>.ini
  user/<namespace>/<profile>.ini
```

BEC slugifies the namespace before it is used as a directory name. If a namespace-specific file does not exist, BEC can
still fall back to the legacy non-namespaced path when checking for an existing profile.

## How BEC resolves the dock area namespace

Each dock area uses a `profile_namespace` to scope its profile set.

In practice, `dock_area.py` uses this namespace so different dock area contexts can keep different profile subsets. For
example, one dock area type can have its own saved profiles, while another dock area type uses a separate set.

If a namespace is not passed explicitly, BEC derives one in this order:

1. the explicit `profile_namespace`
2. the dock area's `objectName()`
3. the dock area's `windowTitle()`
4. the current dock area mode, as `<mode>_workspace`
5. the dock area class name
6. the fallback namespace `general`

This keeps different dock area types and contexts from accidentally sharing the same profile list.

## Last-used profile state

BEC also stores the last-used profile separately from the profile INI files.

This metadata is written to:

```text
widget_settings/profiles/_meta.ini
```

The last-used profile key is scoped by namespace and can also be scoped by dock area instance ID. When an instance ID is
present, BEC first checks the instance-specific entry and can then fall back to the namespace-wide entry.

## Restore behavior

When you restore a profile to its default, BEC copies the `default` profile file over the `user` profile file and then
reloads the profile.

The quick-select flag is preserved during this restore.

## Related topics

- For the GUI view of these fields, use [The GUI Profile Manager](profile-manager.md).
- For the user workflow, use [Restore a GUI Profile to Its Default](../../how-to/gui/restore-gui-profile-default.md).

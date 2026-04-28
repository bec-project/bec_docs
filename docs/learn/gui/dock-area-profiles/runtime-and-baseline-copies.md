---
related:
  - title: Dock Area Profiles
    url: learn/gui/dock-area-profiles/index.md
  - title: Dock Area profile manager
    url: learn/gui/dock-area-profiles/profile-manager.md
  - title: Restore a Dock Area profile to its baseline
    url: how-to/gui/restore-dock-area-profile-baseline.md
  - title: Share a Dock Area profile with other accounts
    url: how-to/gui/share-dock-area-profile-with-other-accounts.md
---

# Runtime and Baseline Copies

Dock Area profiles use two profile copies:

- the `runtime` profile, which is the editable working copy
- the `baseline` profile, which is the restore point

When BEC loads a profile, it prefers the runtime profile. If a runtime profile is not available, it falls back to the
baseline profile. When a profile is restored, BEC replaces the runtime profile with the baseline profile and reloads the
dock area.

For locally created profiles, saving again with the same name updates both the runtime profile and the baseline profile.
For bundled profiles from BEC Widgets or a beamline plugin repository, the bundled source remains read-only.

## Profile origins

Dock Area profiles have three origins:

| Origin | Source | Delete? | Update baseline? |
| --- | --- | --- | --- |
| eAccount settings | Active BEC widgets settings profile root | :material-check: | :material-check: |
| Beamline plugin | `<beamline_repo>/bec_widgets/profiles/` | :material-close: | :material-close: |
| BEC Widgets | Built-in BEC Widgets profiles | :material-close: | :material-close: |

The profile manager uses the origin to decide whether the delete action is enabled and whether a profile is treated as
read-only.

## Profile hierarchy

An eAccount is the experiment account assigned to an experiment. It has limited storage access and owns the writable
profile settings for that experiment.

```text
Dock Area profile sources

  BEC Widgets core library
    bec_widgets/widgets/containers/dock_area/profiles/
      <profile>.ini
        -> read-only baseline source

  Beamline plugin repository
    <beamline_repo>/bec_widgets/profiles/
      <profile>.ini
        -> shared read-only baseline source

  eAccount A writable settings
    widget_settings/profiles/
      baseline/<namespace>/<profile>.ini
      runtime/<namespace>/<profile>.ini

  eAccount B writable settings
    widget_settings/profiles/
      baseline/<namespace>/<profile>.ini
      runtime/<namespace>/<profile>.ini

Transfer paths

  Plugin repository profile
    -> deployed for all eAccounts that use that plugin revision

  eAccount A profile file
    -> copied manually to eAccount B
    -> useful for ad hoc sharing between two eAccounts
```

## Beamline plugin profiles

BEC discovers read-only bundled profiles from:

- BEC Widgets built-in profiles
- the active beamline plugin repository profile directory

The preferred beamline plugin repository profile directory is:

```text
<beamline_repo>/bec_widgets/profiles/
```

For plugin repositories that keep widget resources inside the Python package, BEC also checks:

```text
<beamline_repo>/<plugin_package>/bec_widgets/profiles/
```

Use the top-level `bec_widgets/profiles/` directory for new shared profiles unless your plugin already stores
widget-specific resources inside the package directory.

## Namespace-specific profile directories

Within the writable profile root, BEC stores profiles in separate namespace directories below `runtime/` and
`baseline/`.

The namespace distinguishes different subsets of profiles for different dock areas. This lets BEC keep one set of
profiles for one type of dock area and a different set for another type of dock area, instead of mixing all profiles
into one shared list.

In practice, a namespaced profile layout looks like this:

```text
widget_settings/profiles/
  baseline/<namespace>/<profile>.ini
  runtime/<namespace>/<profile>.ini
```

BEC slugifies the namespace before it is used as a directory name.

## How BEC resolves the dock area namespace

Each dock area uses a `profile_namespace` to scope its profile set.

If a namespace is not passed explicitly, BEC derives one in this order:

1. the explicit `profile_namespace`
2. the dock area's `objectName()`
3. the dock area's `windowTitle()`
4. the current dock area mode, as `<mode>_workspace`
5. the dock area class name
6. the fallback namespace `general`

This keeps different dock area types and contexts from accidentally sharing the same profile list.

## Last-used profile state

BEC stores the last-used profile separately from the profile INI files:

```text
widget_settings/profiles/_meta.ini
```

The last-used profile key is scoped by namespace and can also be scoped by dock area instance ID. When an instance ID is
present, BEC first checks the instance-specific entry and can then fall back to the namespace-wide entry.

## Related topics

- For the GUI view of these fields, use [The Dock Area Profile Manager](profile-manager.md).
- For the task workflow, use
  [Restore a Dock Area Profile to Its Baseline](../../../how-to/gui/restore-dock-area-profile-baseline.md).

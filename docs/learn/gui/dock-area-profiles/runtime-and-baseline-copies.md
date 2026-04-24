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
| Beamline plugin | `<beamline_repo>/<beamline_package>/bec_widgets/profiles/` | :material-close: | :material-close: |
| BEC Widgets | Built-in BEC Widgets profiles | :material-close: | :material-close: |

The profile manager uses the origin to decide whether the delete action is enabled and whether a profile is treated as
read-only.

## Profile hierarchy

An eAccount is the experiment account assigned to an experiment. It has limited storage access and owns the writable
profile settings for that experiment.

Profiles can come from read-only bundled sources or from writable eAccount settings:

| Layer | Path | Role |
| --- | --- | --- |
| BEC Widgets core library | `bec_widgets/widgets/containers/dock_area/profiles/<profile>.ini` | Built-in read-only baseline source. |
| Beamline plugin repository | `<beamline_repo>/<beamline_package>/bec_widgets/profiles/<profile>.ini` | Shared read-only baseline source deployed with the plugin revision. |
| eAccount writable baseline | `widget_settings/profiles/baseline/<namespace>/<profile>.ini` | Local restore point for one eAccount and namespace. |
| eAccount writable runtime | `widget_settings/profiles/runtime/<namespace>/<profile>.ini` | Editable working copy loaded by the Dock Area. |

When a bundled profile is used, BEC creates writable eAccount copies so the running session can edit the profile without
modifying the bundled source. For durable sharing, commit the profile to the beamline plugin repository. For short-term
sharing between two eAccounts, copy the eAccount profile file directly.

## Beamline plugin profiles

BEC discovers read-only bundled profiles from:

- BEC Widgets built-in profiles
- the active beamline plugin repository profile directory

Beamline plugin profiles must be stored in:

```text
<beamline_repo>/<beamline_package>/bec_widgets/profiles/
```

Here, `<beamline_repo>` is the Git repository directory and `<beamline_package>` is the Python package directory inside
that repository. For example, a repository named `debye_bec` can contain a Python package directory also named
`debye_bec`, so the profile directory is `debye_bec/debye_bec/bec_widgets/profiles/`.

Profiles committed there are shared with all eAccounts that use that beamline plugin revision. BEC treats those files as
read-only bundled baseline sources; local runtime and baseline copies are created in the eAccount settings area when the
profile is used.

Use this plugin directory when a Dock Area profile should be distributed as part of the beamline GUI setup. For ad hoc
sharing between two eAccounts, copy the profile file between the eAccount settings directories instead.

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

If `profile_namespace` is passed explicitly, BEC uses that value. If it is not passed and automatic namespace resolution
is enabled, BEC derives the namespace in this order:

1. the dock area's `objectName()`
2. the dock area's `windowTitle()`
3. the current dock area mode, as `<mode>_workspace`

If automatic namespace resolution is disabled and no explicit namespace is passed, BEC uses `general`.

The profile utilities then use the resolved namespace for profile lookup and storage. New namespace-scoped profiles are
written to the namespace-specific directory. Profile lookup can also see unscoped profile files for compatibility, but
new Dock Area profile sets should use a clear namespace.

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

---
related:
  - title: Switch Dock Area profiles
    url: how-to/gui/switch-dock-area-profile.md
  - title: Delete a Dock Area profile
    url: how-to/gui/delete-dock-area-profile.md
  - title: Add changes to your plugin repository
    url: how-to/git/add-changes-to-plugin-repository.md
  - title: Learn about the profile manager fields
    url: learn/gui/dock-area-profiles/profile-manager.md
  - title: Learn about runtime and baseline copies
    url: learn/gui/dock-area-profiles/runtime-and-baseline-copies.md
---

# Share a Dock Area Profile with Other Accounts

!!! Info "Goal"

    Find the `.ini` file for a locally saved Dock Area profile so you can share it with another eAccount or add it to
    the beamline plugin repository.

## Prerequisites

- You have saved and tested the profile locally.
- You can access the eAccount or beamline plugin repository where the profile should be copied.
- You can open a Gitea pull request if the profile should become part of the plugin repository.

An eAccount is the experiment account assigned to an experiment. It has limited storage access and owns the writable
Dock Area profile settings for that experiment.

!!! learn "[Learn how runtime and baseline profile copies are stored](../../learn/gui/dock-area-profiles/runtime-and-baseline-copies.md){ data-preview }"

## 1. Find the saved profile

Open the profile manager from the dock area toolbar and select the profile.

Read the `Runtime path` field in the metadata panel. This is the editable `.ini` file for the saved profile.

Use this path as the source file when you copy the profile to another eAccount or add the profile to the plugin
repository.

!!! learn "[Learn more about the profile manager fields](../../learn/gui/dock-area-profiles/profile-manager.md){ data-preview }"

## 2. Choose where to share the profile

/// tab | :material-source-branch: Plugin repository

Use this option for durable beamline reuse. The profile becomes available to every eAccount that uses the deployed
plugin revision.

### Copy the profile into the plugin repository

Copy the profile INI file into the preferred plugin repository profile directory:

/// tab | :material-file-tree: Template path

```text
/sls/<xname>/config/bec/<deployment_name>/<beamline_repo>/<beamline_package>/bec_widgets/profiles/
```

///
/// tab | :material-map-marker-path: Example path

```text
/sls/x01da/config/bec/production/debye_bec/debye_bec/bec_widgets/profiles/
```

///

Here, `<beamline_repo>` is the Git repository directory and `<beamline_package>` is the Python package directory inside
that repository. In many beamline plugins they have the same name, for example `debye_bec/debye_bec`.

!!! note

    If the `bec_widgets/profiles/` directory does not exist yet, create it before
    copying the profile file.

Keep the file name readable and specific. For example:

```
alignment_scan.ini
```

The plugin repository path follows the same beamline repository layout described in
[Add Changes to Your Plugin Repository](../git/add-changes-to-plugin-repository.md){ data-preview }.

### Add the file to the plugin repository

Continue with [Add Changes to Your Plugin Repository](../git/add-changes-to-plugin-repository.md) to stage, commit, and
push the profile file.

### Open a Gitea pull request

Open a pull request against the plugin repository's `main` branch.

After the pull request is approved and merged, the profile is available as a bundled profile when the next deployment
uses that commit.

///
/// tab | :material-account-switch: Another eAccount

Use this option for ad hoc sharing between two eAccounts. Copy the profile directly only when the profile does not need
to be reviewed, versioned, or distributed through the plugin repository.

### Copy the profile to another eAccount

Copy the profile INI file into the target eAccount's writable profile directory:

/// tab | :material-file-tree: Template path

```text
/sls/<xname>/data/<target_eAccount>/raw/widget_settings/profiles/runtime/<namespace>/
```

///
/// tab | :material-map-marker-path: Example path

```text
/sls/x01da/data/e12345/raw/widget_settings/profiles/runtime/bec/
```

///

If the profile should also be the restore point in the target eAccount, copy it to the matching baseline directory:

/// tab | :material-file-tree: Template path

```text
/sls/<xname>/data/<target_eAccount>/raw/widget_settings/profiles/baseline/<namespace>/
```

///
/// tab | :material-map-marker-path: Example path

```text
/sls/x01da/data/e12345/raw/widget_settings/profiles/baseline/bec/
```

///

Use the same file name in both locations.

///

## 3. Check the shared profile

After deployment or after copying the profile to another eAccount, open BEC with a dock area.

Open the profile manager and verify that the profile is listed. Bundled profiles appear as read-only profiles and cannot
be overwritten or deleted from the GUI.

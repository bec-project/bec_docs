---
related:
  - title: Switch GUI profiles
    url: how-to/gui/switch-gui-profile.md
  - title: Delete a GUI profile
    url: how-to/gui/delete-gui-profile.md
  - title: Add changes to your plugin repository
    url: how-to/git/add-changes-to-plugin-repository.md
  - title: Learn about the profile manager fields
    url: learn/gui/profile-manager.md
---

# Share a GUI Profile with Other Accounts

!!! Info "Goal"

    Find the original `.ini` file for a locally saved GUI profile so you can add it to the beamline plugin repository
    and share it with other accounts.

## Prerequisites

- You have saved and tested the profile locally.
- You can access the beamline plugin repository.
- You can open a Gitea pull request for the plugin repository.

## 1. Find the saved profile

Open the profile manager from the dock area toolbar and select the profile.

Read the `User path` field in the metadata panel. This is the original `.ini` file for the saved profile.

Use this path as the source file when you add the profile to the plugin repository.

!!! learn "[Learn more about the profile manager fields](../../learn/gui/profile-manager.md){ data-preview }"

## 2. Copy the profile into the plugin repository

Copy the profile INI file into the preferred plugin repository profile directory:

```
/sls/<xname>/config/bec/<deployment_name>/<plugin_repo>/bec_widgets/profiles/
```

!!! note

    If the `bec_widgets/profiles/` directory does not exist yet, create it before
    copying the profile file.

Keep the file name readable and specific. For example:

```
alignment_scan.ini
```

If your plugin already keeps widget resources inside its Python package, the package-local
profile directory is also supported:

```text
/sls/<xname>/config/bec/<deployment_name>/<plugin_repo>/<plugin_package>/bec_widgets/profiles/
```

## 3. Add the file to the plugin repository

Once you know the original `.ini` file location and the target profile directory, continue with
[Add Changes to Your Plugin Repository](../git/add-changes-to-plugin-repository.md) to stage, commit, and push the
profile file.

## 4. Open a Gitea pull request

Open a pull request against the plugin repository's `main` branch.

After the pull request is approved and merged, the profile is available as a bundled
profile when the next deployment uses that commit.

## 5. Check the deployed profile

After deployment, open BEC with a dock area.

Open the profile manager and verify that the profile is listed. Bundled profiles appear as read-only profiles and cannot
be overwritten or deleted from the GUI.

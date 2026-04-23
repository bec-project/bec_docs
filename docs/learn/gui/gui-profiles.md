---
related:
  - title: Learn about the GUI profile manager
    url: learn/gui/profile-manager.md
  - title: Learn about user and default profile copies
    url: learn/gui/gui-profile-copies-and-namespaces.md
  - title: Save and switch GUI profiles
    url: getting-started/next-steps/save-and-switch-gui-profiles.md
  - title: Share a GUI profile with other accounts
    url: how-to/gui/share-gui-profile-with-other-accounts.md
---

# GUI Profiles

GUI profiles store the dock area layout so that you can return to a useful workspace later. A profile records which
widgets are present, how they are docked, selected widget settings, the quick-select flag, profile timestamps, and a
screenshot preview when available.

This page explains what a GUI profile is and how the profile file works. For inspection and browsing, use
[The GUI Profile Manager](profile-manager.md). For the advanced rules around user and default copies and dock area
namespaces, continue with [GUI Profile Copies and Namespaces](gui-profile-copies-and-namespaces.md).

## Where profiles are stored

Profiles are stored as INI files. The dock area reads and writes them through
[QSettings](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QSettings.html).

User-created and user-modified profiles are written under the BEC widgets settings profile root:

```text
<widgets_settings.base_path>/profiles/
```

This root can be overridden with:

```text
BECWIDGETS_PROFILE_DIR
```

On PSI deployments, this widgets settings root is typically created under the account's `raw` area. In practice, GUI
profiles are usually stored below:

```text
/sls/<xname>/data/<account>/raw/widget_settings/profiles/
```

This matches the same `raw` base area used for other BEC-written files. For the surrounding directory layout, see
[Where Files Are Written](../file-writer/where-files-are-written.md).

## What the profile file contains

The profile file stores more than the dock arrangement. It combines several kinds of state in the same INI file:

- dock geometry and docking state
- a widget manifest that lists which widgets must be recreated
- widget state saved from Qt properties
- profile metadata such as timestamps and quick-select state
- an optional screenshot preview

The dock layout itself is written through
[QSettings](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QSettings.html), together
with [Qt Advanced Docking System](https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System)
state and the widget manifest.

The per-widget state is restored through
the [Qt property system](https://doc.qt.io/qtforpython-6/PySide6/QtCore/Property.html). BEC inspects readable, writable,
and stored properties
from each widget's
[meta-object](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QMetaObject.html), which is provided by
[QObject](https://doc.qt.io/qtforpython-6.5/PySide6/QtCore/QObject.html).

In practice, this means a profile can restore both the dock arrangement and widget settings, as long as those widget
settings are exposed as Qt properties and are not explicitly skipped by the widget state manager.

## How BEC reconstructs a profile

When a profile is loaded, BEC does the work in stages:

1. It chooses the profile file to load.
2. It reads the widget manifest from the INI file.
3. It recreates the listed widgets.
4. It restores the dock layout.
5. It restores widget-specific settings from the stored Qt properties.

This is why a profile can bring back both the widget set and the state of those widgets, rather than only their
positions on screen.

## Sharing profiles across experiments

A profile saved from the GUI belongs to the current settings area. To reuse it across accounts or experiments, move the
profile INI file into the plugin repository profile directory and commit it.

For the task-focused workflow, use
[Share a GUI Profile with Other Accounts](../../how-to/gui/share-gui-profile-with-other-accounts.md).

## Related topics

- To inspect available profiles, fields, and actions, see [The GUI Profile Manager](profile-manager.md).
- To understand user and default copies, profile origins, and namespaces, see
  [GUI Profile Copies and Namespaces](gui-profile-copies-and-namespaces.md).

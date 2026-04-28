---
related:
  - title: Dock Area Profiles
    url: learn/gui/dock-area-profiles/index.md
  - title: Runtime and baseline profile copies
    url: learn/gui/dock-area-profiles/runtime-and-baseline-copies.md
  - title: Dock Area profile manager
    url: learn/gui/dock-area-profiles/profile-manager.md
---

# Qt Storage and Reconstruction

Dock Area profile files are INI files. BEC reads and writes them through
[QSettings](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QSettings.html).

## What the profile file contains

The profile file stores more than the dock arrangement. It combines several kinds of state in the same INI file:

- dock geometry and docking state
- a widget manifest that lists which widgets must be recreated
- widget state saved from Qt properties
- profile metadata such as timestamps and quick-selection state
- an optional screenshot preview

The dock layout itself is written through QSettings, together with
[Qt Advanced Docking System](https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System) state and the widget
manifest.

The per-widget state is restored through
the [Qt property system](https://doc.qt.io/qtforpython-6/PySide6/QtCore/Property.html). BEC inspects readable, writable,
and stored properties from each widget's
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

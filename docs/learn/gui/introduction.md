---
related:
  - title: RPC GUI Control
    url: learn/gui/rpc-gui-control.md
  - title: Dock Area Profiles
    url: learn/gui/dock-area-profiles/index.md
  - title: Create Your First GUI
    url: getting-started/quick-start/06-create-your-first-gui.md
  - title: GUI how-to guides
    url: how-to/index.md
---

# Introduction to BEC Widgets

BEC Widgets is a modular [Qt6](https://doc.qt.io/qt-6/qt-intro.html) GUI framework for beamline experiment control. Rather than providing
one monolithic application, it is organized as a collection of independent, reusable widgets that
can be assembled into task-specific interfaces, largely without any glue code.

## Independent by design

GUI applications in BEC always run in a separate OS process, even when started from the IPython client. They connect
to the same Redis instance as the scan server and device server, but they never share memory or
threads with the acquisition pipeline. This means heavy plotting, large datasets, or a momentary
UI freeze cannot slow down a running scan or affect data acquisition. The worst case is a dropped
frame in the GUI; the backend continues uninterrupted.

## How widgets receive live data

Widgets generally do not poll for updates. Instead, live data reaches the GUI through the BEC Dispatcher,
which bridges BEC's event-driven Redis messages into Qt's signal/slot model. A widget developer
declares which Redis endpoint should update which Qt slot; the Dispatcher handles subscription,
message decoding, and thread-safe delivery to the GUI thread. This keeps widget implementations
free of transport boilerplate while ensuring that data always arrives on the correct thread.

## Remote control and scripting

BEC Widgets are designed to be fully controllable from scripts and the IPython client through Remote Procedure Calls (RPC). Every widget exposes a public API of methods and properties that can be accessed remotely. This allows users to automate GUI interactions, build custom workflows that combine data analysis with live plot updates, or switch GUI profiles in response to scan state changes. The BEC IPython client provides a convenient interface for connecting to running GUI instances and accessing their widgets. Users do not have to choose between a graphical interface and command-line control; they can have both at the same time, with seamless integration between them.

## Developing with BEC Widgets

BEC Widgets supports four complementary development paths, all built on the same widget set and
event-driven backend.

### Assemble graphically in BEC Designer

BEC Designer is a thin wrapper around Qt Designer that makes every BEC widget available as a
designer plugin. Plugins are auto-generated from widget classes, so new widgets appear
automatically without extra effort. Because BEC widgets expose Qt properties and signals/slots,
properties are editable in Designer's property panel and inter-widget connections can be wired
visually. BEC Widgets can be freely combined with standard Qt widgets to build larger and 
bespoke interfaces, tailored to specific experiment needs. The resulting `.ui` files can be 
launched directly with the BEC Widgets launcher, giving teams a running Redis-connected 
application without writing any Python.

### Assemble graphically in the Dock Area and save profiles

From the BEC Launcher, you can work with a Dock Area either in `Terminal + Dock` mode or in the
BEC App's Dock Area. In `Terminal + Dock`, the Dock Area is immediately available as `gui.bec`
next to the IPython client. Users add widgets from the
toolbar menus, adjust their settings, rearrange and tear out panels, and save the result as a
reusable profile. This mode keeps the terminal as the primary control interface while graphical
widgets provide richer views of plots, queues, and device state. It is the mode used throughout
the quick-start tutorials.

### Script appearance and behavior through RPC

The BEC IPython client exposes [RPC control](./rpc-gui-control.md){data-preview} over any running GUI. Each GUI application is
identified by a `gui_id`, and the IPython client can connect to any running instance by that ID.
The object access pattern follows the Qt parent/child hierarchy, making it easy to reach any
widget from the command line. Scripting RPC calls is the natural mode for automating GUI
interactions, switching profiles in response to scan state, or building experiment workflows that
combine data analysis with live plot updates. This is also the mode to script how a GUI should
look at runtime: create docks and widgets, set titles and labels, configure curves, and load
profiles programmatically.

### Write custom widgets by inheriting from `BECWidget`

When built-in widgets are not enough, you can create your own widget by subclassing `BECWidget`.
This gives you the standard BEC integration points out of the box, including dispatcher-based live
data updates, Qt property support, and RPC exposure for user-facing methods. In practice, this path
is used to build beamline-specific views that can then be reused in BEC Designer, the Dock Area,
and scripted RPC workflows.

## What to read next

- [RPC GUI Control](rpc-gui-control.md) explains how the BEC IPython client communicates with
  running widgets and how the CLI namespace is constructed from the Qt widget hierarchy.
- [Dock Area Profiles](dock-area-profiles/index.md) explains how GUI workspace configurations are
  saved, restored, and shared across e-accounts.
- [Create Your First GUI](../../getting-started/quick-start/06-create-your-first-gui.md) is a
  hands-on tutorial that walks through opening a dock area, adding widgets, and running a scan.
- [Introduction to Qt](https://doc.qt.io/qt-6/qt-intro.html) can help if you want to understand the 
  underlying GUI framework that BEC Widgets is built on.

---
related:
  - title: Overview
    url: learn/system-architecture/overview.md
  - title: Core Services
    url: learn/system-architecture/core-services.md
  - title: Data Flow
    url: learn/system-architecture/data-flow.md
---

# Clients

Clients are first-class participants in the BEC architecture. They are treated like any other
service on the shared messaging layer, but they are not the source of truth for scan execution. The
backend services remain responsible for orchestration, device access, synchronization, and file
writing.

This means that user-facing tools can stay comparatively lightweight, because they do not need to
re-implement the core acquisition logic locally. It also makes new clients comparatively easy to
build: a CLI, GUI, notebook integration, web frontend, or custom application in another language
can connect to the same event streams and request paths without rewriting the backend behavior.

Because the backend owns the orchestration state, BEC can also support any number of clients in
parallel. Multiple users, tools, or services can observe and interact with the same running system
at the same time.

## Main Client Entry Points

The most common entry points into BEC are:

- the BEC IPython client for interactive beamline control and scripting
- the Python library and client APIs for programmatic access
- the BEC GUI and widget-based applications for graphical workflows

All of them connect to the same backend architecture. In practice, a client sends requests, observes
queue and scan status, displays progress and data, and may expose higher-level helper APIs such as
`bec.history`.

Because clients and services use the same shared system model, the distinction between them is often
one of role rather than capability. A user-facing client may mainly display state and submit scan
requests, while another service may consume the same events for analysis or automation.

## Event-Driven Interaction

This event-based architecture fits graphical user interfaces naturally. GUIs are themselves
event-driven systems: they subscribe to state changes, react to user actions, and update views
asynchronously. In BEC, a GUI can listen to queue events, progress updates, device readouts, and
file notifications directly from the shared event streams, without needing its own orchestration
backend.


## Analysis as a Client

The data analysis pipeline is a good example of how flexible this model is. Analysis does not need
to be treated as a special case outside the architecture. It can behave like any other client or
service in the system: subscribe to live events, process incoming data, publish results back into
BEC, and, if necessary, submit new scans in response to what it observes.

That makes feedback-driven workflows possible without bypassing the central orchestration layer.

!!! info "What to remember"
    - Clients participate in the same event-driven architecture as backend services.
    - The backend remains the source of truth for orchestration and hardware access.
    - GUIs fit naturally into this model because they are event-driven themselves.
    - Analysis pipelines can also behave like clients, including submitting new scans when needed.

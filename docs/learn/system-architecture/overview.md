---
related:
  - title: Device configuration in BEC
    url: learn/devices/device-config-in-bec.md
  - title: File writing
    url: learn/file-writer/index.md
  - title: Access BEC history
    url: how-to/scans/access-bec-history.md
---

# Overview

BEC uses a service-oriented, event-driven architecture built around a shared Redis message bus.
This page explains how the system is organized, how the core services interact, and why this model
makes it easy to build new clients, services, and graphical interfaces without duplicating the
backend logic.

![BEC architecture overview](../../assets/BEC_architecture.png)

## Architecture model

BEC is organized as a set of smaller services that communicate through Redis instead of as one large
application that owns orchestration, device access, data synchronization, file writing, and user
interfaces all in the same process.

### Why a service-based model

Acquisition requirements evolve quickly, and it is often difficult to know in advance which scan
patterns, detector workflows, or analysis-driven feedback loops will be needed a year from now. A
beamline control system therefore has to adapt quickly to changing scientific and operational
requirements without becoming the bottleneck for data acquisition.

The service-based approach in BEC is meant to provide exactly that flexibility. EPICS and device
controllers provide the low-level control interface, but they do not by themselves provide the
higher-level orchestration needed to execute scans, validate requests, coordinate devices, observe
progress and results, write structured files, and connect online analysis or external systems. BEC
therefore separates these responsibilities into independent services rather than concentrating them
in one large application. This keeps user interfaces lightweight, allows orchestration to evolve
independently from clients, and lets downstream consumers such as file writing or analysis subscribe
to the same live streams without interfering with scan control.

### Why device access is centralized

The primary job of experiment-control software is to provide an orchestration
layer above the underlying control system. A unified entry point is therefore what allows BEC to
coordinate motion and acquisition across the system. If clients were to talk to EPICS directly or
drive hardware independently, BEC could not reliably enforce ordering, synchronization, queueing,
or conflict-free device access.

There is also a practical device-integration reason for centralizing control. Some hardware and
device interfaces support only a single active connection or are otherwise not designed for several
independent clients to interact with them safely at the same time. In those cases, a central device
connection service is the logical design choice.

### Redis as the shared system bus

In BEC, Redis is more than a cache. It acts as the central transport and coordination layer for the
system.

Conceptually, services publish requests, status updates, readouts, metadata, and results to Redis,
and other services subscribe to the parts they need.

This keeps services loosely coupled, allows multiple clients to observe the same scan state, and
makes it possible to add new consumers such as analysis jobs or custom dashboards without changing
the scan logic itself. It also provides a low-latency way to share transient state across the
system.

### Language independence

BEC also does not enforce one particular implementation language for its services. Today, many core
services and clients are written in Python, but that is a practical choice rather than an
architectural requirement. Because the system is organized around a shared messaging model, new
clients or auxiliary services can be built in other languages or frameworks without rewriting the
core scan, device, or file-writing logic. In practice, the wider BEC ecosystem already includes
tools written in Go, Rust, and TypeScript alongside the Python-based services.

!!! info "What to remember"
    - BEC uses a service-oriented architecture so the system can adapt quickly to changing
      acquisition requirements.
    - Device access is centralized so hardware connections and coordinated motion can be managed
      safely.
    - Redis acts as the shared system bus between services.
    - The architecture is language-independent, even though many current services are written in
      Python.

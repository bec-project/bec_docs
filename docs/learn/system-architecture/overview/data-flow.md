---
related:
  - title: Overview
    url: learn/system-architecture/overview.md
  - title: Core Services
    url: learn/system-architecture/core-services.md
  - title: Clients
    url: learn/system-architecture/clients-and-data-flow.md
  - title: Access BEC History
    url: how-to/scans/access-bec-history.md
---

# Data Flow

BEC is built around shared event streams and coordinated service interactions. Requests, state
updates, readouts, metadata, and file-writing signals move through the system in a way that lets
multiple clients and services observe the same acquisition without duplicating the orchestration
logic.

## How Data Flows Through the System

The exact message details depend on the scan type and deployment, but the overall lifecycle is:

1. A client submits a scan request.
2. The scan server validates the request and assembles scan instructions.
3. The scan is inserted into a queue and picked up by a scan worker.
4. The scan worker issues device operations through Redis.
5. The device server performs the corresponding actions on ophyd devices.
6. Devices and services publish status, progress, metadata, and readouts back to Redis.
7. The scan bundler synchronizes asynchronous readouts into logical scan points.
8. Clients, file writers, and analysis services consume those streams.
9. The file writer persists the scan to disk, while clients can still inspect recent results live or
   through history helpers.

!!! tip "Shared streams keep behavior consistent"
    Because orchestration lives on the server side, a CLI, GUI, notebook helper, analysis service,
    or automation layer can all build on the same backend behavior instead of re-implementing scan
    control.

!!! learn "[Access BEC history](../../how-to/scans/access-bec-history.md){ data-preview }"

## What to Remember

- Data in BEC flows through shared event streams rather than direct client-to-client control paths.
- The scan server, device server, scan bundler, file writer, and analysis services all participate
  in the same coordinated system model.
- Multiple consumers can observe the same acquisition state and data stream at the same time.
- Clients can remain lightweight because the backend owns orchestration and synchronization.

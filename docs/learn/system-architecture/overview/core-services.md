

# Core Services

The service-oriented architecture of BEC is built around a few central backend components. Each has
its own responsibility, but they work together through the shared Redis message bus.

## Scan Server

The scan server is the main orchestration service. It is the place where scan requests enter the
backend.

Its responsibilities are:

- validate incoming scan requests
- assemble executable scan instructions
- place scans into a queue for execution
- run scan workers that execute the queued scan logic
- publish device instructions and scan state updates

This decomposition matters because BEC is not just "run a plan now". It treats scan execution as a
managed workflow with validation, queuing, and state reporting.

## Device Server

The device server is the hardware-facing service layer. It wraps ophyd objects and exposes them to
the rest of BEC through Redis-mediated operations.

Its responsibilities are:

- construct devices from the active BEC device configuration
- expose device methods and signals to the rest of the system
- execute hardware operations requested by the scan server or clients
- provide a common interface over EPICS-backed and non-EPICS-backed devices

This is one of the most important architectural decisions in BEC. Instead of requiring every client
or workflow to import and own devices locally, the device server centralizes live device access in
one service.

!!! learn "[Introduction to ophyd](../../learn/devices/introduction-to-ophyd.md){ data-preview }"

## Scan Bundler

Control-system readouts are naturally asynchronous. Different devices may produce their values at
slightly different times, even when they belong to the same logical scan point.

The scan bundler turns these asynchronous readouts into synchronized scan data by grouping them
using metadata such as point identifiers or timestamps.

This matters because:

- clients usually want one logical "point" of data
- online analysis often expects synchronized records
- file writing becomes simpler when the data stream is already bundled into scan points

## File Writer

The file writer is responsible for persisting scan data to structured HDF5 output.

The file writer is intentionally a separate service. This keeps writing concerns out of the core
orchestration path and allows file format logic to evolve independently.

At a high level, the file writer:

- writes the final master file after the scan completes
- writes asynchronous device data continuously during the scan when needed
- adds the default BEC HDF5 and NeXuS-style structure through `DefaultFormat`
- links in externally produced files when needed
- supports customization through writer plugins

This separation is important because beamlines may need both a stable default file structure and
beamline-specific extensions, while some async data streams are too large or too frequent to delay
until the end of the scan.

!!! learn "[File writing](../../learn/file-writer/index.md){ data-preview }"

## SciHub Connector

The SciHub connector links BEC to external systems such as a logbook, a data catalog, or a BEC
database.

Architecturally, this shows an important BEC pattern: external integrations are kept at the edge of
the system instead of being mixed into scan execution itself.

## Data Analysis Pipeline

BEC treats online analysis as another consumer and producer on the shared Redis bus.

That means an analysis pipeline can:

- subscribe to live scan events
- process data during acquisition
- publish results or metadata back into BEC
- feed back information that may influence later actions
- behave like any other client in the system and submit new scans if necessary

Simple processing may run close to the core services, while heavier workflows can be delegated to
external compute resources such as batch jobs.

!!! info "What to remember"
    - The scan server is the orchestration entry point for scan execution.
    - The device server centralizes live hardware access through ophyd.
    - The scan bundler turns asynchronous readouts into synchronized scan data.
    - The file writer persists scan output while supporting both default structure and custom
      beamline-specific extensions.
    - External integrations and analysis pipelines can subscribe to the same event streams without
      being tightly coupled to the core orchestration path.

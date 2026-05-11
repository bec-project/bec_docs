---
related:
  - title: System architecture overview
    url: learn/system-architecture/overview/index.md
  - title: File writing
    url: learn/file-writer/introduction.md
  - title: Access BEC history
    url: how-to/scans/access-bec-history.md
---

# Scans in BEC

!!! Info "Overview"
    Scans are the core of BEC's functionality. They are the tools that move your devices, trigger readouts, and produce the data you analyze. 
    
    In BEC, all scans follow the same structure and report themselves in a consistent way, even when their motion logic differs.

BEC scans follow one shared model. Whether you run a simple acquisition, a line scan, a grid scan,
or a continuous scan, BEC handles them in the same overall way.


## The Main Idea

The most important idea in BEC scan execution is simple:

- all scans follow the same overall structure
- all scans are reported through the same backend model
- all scans are executed on the server
- all scans produce data that can be accessed in the same general way afterward
- the client learns the available scans from the scan server, including their current signatures and metadata

That is true even when the middle of the scan is very different.

For example, a line scan, a grid scan, and a continuous scan may move differently, but they still fit into one common scan framework.

## Client and server responsibilities

One of the most important design choices in BEC is that the client and the scan server do different
jobs.

The client is the user-facing side. It learns which scans are currently available from the scan
server and exposes them dynamically as `scans.<name>(...)`. That means the client does not hardcode
the live scan definitions. Instead, it uses the signatures, documentation, and GUI metadata
published by the server at runtime.

When you call a scan from the client, the client does not run the scan logic locally. It validates
and packages your inputs, adds request metadata, and sends a scan request to the scan server.

The scan server is the execution side. It owns the registered scan classes, validates incoming scan
requests against those server-side definitions, puts accepted requests into the scan queue, and
hands them to a scan worker. The worker then instantiates the scan class and runs its lifecycle.

This separation brings several practical benefits:

- scans can be improved or extended on the server while clients pick up the updated scan definitions and signatures dynamically
- queueing, execution, progress reporting, and scan data production can be coordinated in one place instead of being split across independently executing clients
- users can run scans from lightweight client scripts without moving hardware logic into each script
- different clients, languages, and machines can submit scan requests without needing to execute the full scan logic locally
- different clients and interfaces can share the same server-side scan implementation and runtime model

In other words, `scans.line_scan(...)` in the client is a request interface, while the scan class
implementation lives and runs on the scan server.

!!! tip "Most custom workflows do not need a new scan"
    If your goal is to combine several existing scan calls, react to results, or add beamline-specific decision logic, it is usually simpler to write a normal Python script around the built-in scans first.

    Create a new scan class only when you need new server-side scan behavior, lifecycle integration, or a reusable scan that should appear as its own `scans.<name>(...)` entry.

## What Happens During A Scan

!!! Note "Dataflow during a scan"
    A general overview of the dataflow in BEC can be found in the [system architecture overview](../../learn/system-architecture/overview/data-flow.md){ data-preview }.

At a high level, a scan in BEC follows this path:

1. The scan server publishes the available scan classes together with their serialized signatures, grouped inputs, and GUI metadata.
1. The client exposes those scans dynamically, so commands such as `scans.line_scan(...)` use the current server-side definition.
1. When a scan is called, the client validates and bundles the arguments, adds request metadata, and sends a request to the server with the scan class's name.
1. On the server, the request is checked against the server-side scan definitions and, if accepted, put into the scan server queue.
1. Once it is the scan's turn to run, the scan server queue hands over the request to a scan worker.
1. The scan worker instantiates the scan class on the server and runs its lifecycle hooks.
1. During the scan, the scan class may use scan actions or components to trigger readouts, move devices, or run custom logic at each scan point.
1. Devices publish readouts and status updates.
1. The scan bundler groups those readouts into logical scan points.
1. Clients, history, and the file writer consume the resulting scan data.

From the user side, the important part is consistency: every scan goes through the same lifecycle
steps. **If you have seen one scan, you have seen them all.** You can focus on the differences in motion logic without having to learn a new overall structure for each scan type.

## The Shared Scan Shape

As mentioned above, all BEC scans follow the same overall shape. They use the same lifecycle and
the same helpers to report themselves and produce data. That shared structure is why BEC scans feel
related rather than like separate one-off tools.

The details of a scan may change a lot from one scan type to another, but the lifecycle around
those details stays recognizable. That makes it easier to learn new scans because you can focus on
the motion logic instead of relearning the full structure each time.

The next page, [Scan Lifecycle](lifecycle.md), breaks down those shared lifecycle steps and what
each hook is responsible for.

## Where To Go Next

If you want the next layer of detail:

- read [Scan Lifecycle](lifecycle.md){ data-preview } to see the shared hook order used by every
  BEC scan.
- read [Learn by example](../learn/scans/learn-by-example.md){ data-preview } to go through the `acquire` scan example in detail, and see how the shared scan shape applies to a specific scan type.

## What to Remember

!!! info "What to remember"
    - In BEC, all scans follow the same overall shape.
    - Different scan types use the same backend framework, even when their motion logic differs.
    - Every scan reports itself in a common structured way while it runs.
    - Every scan follows the same lifecycle, even when some hooks do very little.
    - The lifecycle order is fixed, which makes new scan types easier to understand.

---
related:
  - title: Scan Info
    url: learn/scans/scan-info.md
  - title: Scan Components
    url: learn/scans/scan-components.md
  - title: Learn by Example
    url: learn/scans/learn-by-example.md
---

# Scan Actions

Scan Actions are the building blocks for scan work. They are the main way a concrete scan performs operations such as opening, staging, triggering, reading, and closing a scan. They are also the main way a concrete scan updates its runtime metadata and published status. Every scan has access to these operations through `self.actions` from any scan hook or method, and they are designed to be the preferred way for concrete scans to perform common work and updates.

!!! Info "Scan Actions vs. Scan Components"
    Scan Actions are the lower-level building blocks, while Scan Components are larger, more bespoke patterns built on top of Scan Actions.

## What Scan Actions Are For

Scan Actions are typically used for three kinds of work:

- lifecycle orchestration such as opening, staging, and closing a scan
- device operations such as moving, triggering, reading, and completing
- reporting and metadata updates such as progress instructions and readout-priority changes

## ScanActions Methods

For a full list of available methods, see the reference page for
[ScanActions Methods](../../references/bec-core/scan-actions-methods.md){ data-preview }.

!!! Tip 
    We recommend browsing the reference page to get a sense of the available methods and their purposes but do not recommend trying to memorize them. When writing a concrete scan, you can always use auto-complete to find the right method for your needs. More importantly, we recommend going through actual scan implementations to see how these methods are used in practice. 

## Next Step

After `actions`, continue with [scan components](scan-components.md).

## What To Remember

!!! info "What to remember"
    - `actions` is the scan-facing helper for lifecycle operations, device instructions, and reporting updates.
    - Most concrete scans should prefer `actions` over building instruction messages manually.
    - Several `actions` methods also update `scan_info`, not just device state.

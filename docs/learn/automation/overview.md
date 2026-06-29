---
related:
  - title: Run a procedure
    url: how-to/automation/run-procedure.md
  - title: Create a beamline state
    url: how-to/automation/add-a-beamline-state.md
  - title: Configure the scan interlock
    url: how-to/automation/configure-scan-interlock.md
---

# Overview

BEC provides tools to enable automation of beamline tasks. The three key features are _Beamline States_, which monitor
changes in device signals or other conditions, _BEC Procedures_, which enable the scheduling of parallel, long-running
background tasks on the BEC server in separated processes, and _BEC Actors_, which build on these to provide an
ergonomic interface for reacting to certain conditions, such as changes in beamline states.

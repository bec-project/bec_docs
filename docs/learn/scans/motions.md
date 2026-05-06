---
related:
  - title: Scan Lifecycle
    url: learn/scans/lifecycle.md
  - title: Scan Components
    url: learn/scans/scan-components.md
  - title: Argument Bundles
    url: learn/scans/argument-bundles.md
---

# Motions

In BEC, a scan does not have to acquire detector data.

A coordinated motion can also be treated as a scan if it uses the same lifecycle, reporting model,
and request interface as other scans. That is why commands such as `mv` and `umv` are implemented
with the same scan framework even though their main job is to reposition motors.

This allows motion-only commands to benefit from the scan infrastructure:

- it can reuse the same argument handling and validation
- it can publish status in the same general format
- it can use the same actions and components helpers
- it can fit naturally into the same client and server model as other scan-like operations

## Marking A Motion-Only Command

There are two flags that a scan can set to indicate that it is not a data-taking scan:
- `is_scan=False` indicates that the operation is not a scan, so it should be kept separate from ordinary scan entries in user interfaces.
- `scan_type=None` indicates that the operation is neither hardware-triggered nor software-triggered, so it should not be confused with acquisition scans.

## `move` and `updated_move`

Both `move` and `updated_move` are motion commands implemented through the scan interface.

They accept repeated motor/target bundles, support relative motion, and run through the same hook
structure as other scans.

They are exposed as `scans.mv` and `scans.umv` or through the high-level-interface as 

- `umv` for `scans.umv(..., relative=False)`
- `umvr` for `scans.umv(..., relative=True)`
- `mv` for `scans.mv(..., relative=False)`
- `mvr` for `scans.mv(..., relative=True)`

## The Shared Lifecycle

Even though this command is motion-only, it still defines the same lifecycle hooks:

- `prepare_scan`
- `open_scan`
- `stage`
- `pre_scan`
- `scan_core`
- `post_scan`
- `unstage`
- `close_scan`
- `on_exception`

In motion-only scans, most lifecycle hooks are kept empty or very simple. In particular, `scan_core` is the main place where the motion logic lives.

## What To Remember

!!! info "What to remember"
    - In BEC, a scan does not have to acquire data to use the scan framework.
    - Coordinated motions such as `move` and `updated_move` can use the same lifecycle and reporting model as scans.
    - Motion-only commands can still reuse argument bundles, actions, components, and scan status reporting.
    - To mark a motion-only command, set `is_scan=False` and `scan_type=None` in the scan class.
    - Lifecycle hooks must be defined, but they can be kept simple or empty if they are not needed.

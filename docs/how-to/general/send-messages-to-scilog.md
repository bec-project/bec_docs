---
related:
  - title: Core Services
    url: learn/system-architecture/overview/core-services.md
---

# Send messages to SciLog

!!! Info "Overview"
    Send text, tags, and attachments from the BEC IPython client to a configured [SciLog](https://scilog.psi.ch) messaging service.

## Prerequisites

- You have a running BEC IPython client session.
- SciLog messaging is enabled for your deployment or session.

!!! tip "Logbook selection"

    BEC automatically configures SciLog to use the logbook associated with the currently active pgroup.

## 1. Create and send a simple message

Create a new SciLog message object from the BEC client and send it:

```py
msg = bec.messaging.scilog.new()
msg.add_text("Beamline is ready for alignment.")
msg.send()
```

You can also create and send a short message in one line:

```py
bec.messaging.scilog.new("Beamline checks completed.").send()
```

## 2. Add formatting and tags

SciLog messages support formatted text and tags:

```py
msg = bec.messaging.scilog.new()
msg.add_text("Alignment warning", bold=True, color="yellow")
msg.add_text(" Check the slit positions before continuing.")
msg.add_tags(["alignment", "warning"])
msg.send()
```

`add_text()` supports:

- `bold=True`
- `italic=True`
- `color="red"`, `"green"`, `"yellow"`, `"pink"`, `"blue"` or `"black"`

!!! tip "Pen Colors vs Markers"

    In SciLog, `black`, `red`, and `green` are pen colors. `yellow`, `pink`, and `blue` are markers.

BEC adds the default `bec` tag automatically if you do not provide tags yourself.

If you want to change the default tags for the current client session, set them explicitly:

```py
bec.messaging.scilog.set_default_tags(["bec", "beamline-x", "commissioning"])
```

## 3. Attach a file

Add attachments from a local path before sending the message:

```py
msg = bec.messaging.scilog.new("Attached: latest detector snapshot.")
msg.add_attachment("/path/to/snapshot.png")
msg.send()
```

For image attachments, you can also provide display dimensions:

```py
msg = bec.messaging.scilog.new("Overview image")
msg.add_attachment("/path/to/overview.png", width=800, height=450)
msg.send()
```

Attachments must exist on disk and must be smaller than 5 MB.

## 4. Combine text, tags, and attachments

SciLog messages are built from ordered elements. BEC keeps the order in which you add content, so you can structure a message as text, image, text or in any other sequence that fits your note.

In practice, you will often send all parts together:

```py
msg = bec.messaging.scilog.new()
msg.add_text("Beam position before correction:")
msg.add_attachment("/path/to/before.png", width=700)
msg.add_text("Beam position after correction:")
msg.add_attachment("/path/to/after.png", width=700)
msg.send()
```

You can also combine formatted text, tags, and attachments in one message:

```py
msg = bec.messaging.scilog.new()
msg.add_text("Scan quality check failed.", bold=True, color="red")
msg.add_text(" See the attached plot for details.")
msg.add_tags(["quality-check", "scan"])
msg.add_attachment("/path/to/scan_summary.pdf")
msg.send()
```

## 5. Use SciLog wrapper helpers

BEC also provides wrapper methods for common SciLog use cases. These are convenient when you want to send structured content directly without building the message element by element.

### Log device positions as a table

Use `log_positions()` to capture the current state of devices in SciLog. It collects the same kind of position information you would inspect with `dev.wm(...)` and sends it as a formatted table.

For example, log all sample-positioning devices that match a wildcard:

```py
bec.messaging.scilog.log_positions(
    devices="sam*",
    title="Current sample positions",
    tags="snapshot",
)
```

This creates a SciLog entry with columns for:

- `device`
- `readback`
- `setpoint`
- `limits`

You can also pass other device selections accepted by `dev.wm(...)`, for example a list of device names or device objects.

### Log source code

Use `log_code()` to send source code to SciLog as a Python code block. This is useful for macros, helper functions, or other small snippets that should be recorded alongside a measurement.

Log the source of a function directly:

```py
def align_sample():
    samx.set(1.2)
    samy.set(-0.4)


bec.messaging.scilog.log_code(
    align_sample,
    title="Alignment macro used for this run",
    tags="code",
)
```

!!! success "Congratulations!"

    You can now send SciLog messages from the BEC IPython client, log device positions and source code, add tags, and attach files when needed.

## Common pitfalls

- `bec.messaging.scilog.new()` raises an error if SciLog messaging is not enabled for the current deployment or session.
- `add_attachment(...)` fails if the file does not exist or is larger than 5 MB.
- Default tags are added automatically. If you call `set_default_tags(...)`, those tags are used for later messages in the current client session.

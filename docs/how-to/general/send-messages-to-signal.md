---
related:
  - title: Core Services
    url: learn/system-architecture/overview/core-services.md
---

# Send messages to Signal

!!! Info "Overview"
    Send direct Signal messages from the BEC IPython client by addressing recipients with their phone numbers.

## Prerequisites

- You have a running BEC IPython client session.
- Signal messaging is enabled for your deployment or session.

!!! tip "Private phone numbers"

    Make sure to not commit source code with your private phone number to version control. If you want to share code that includes phone numbers, consider using environment variables or configuration files to keep the numbers private.

## 1. Create and send a simple message

Create a new Signal message object from the BEC client and send it to a phone number:

```py
msg = bec.messaging.signal.new()
msg.add_text("Beamline is ready for alignment.")
msg.send(scope="+41791234567")
```

You can also create and send a short message in one line:

```py
bec.messaging.signal.new("Beamline checks completed.").send(scope="+41791234567")
```

## 2. Send to phone numbers directly

For Signal, pass the recipient phone number to `send(scope=...)`.

```py
msg = bec.messaging.signal.new("Scan finished successfully.")
msg.send(scope="+41791234567")
```

BEC normalizes valid phone numbers before sending them to Signal.
For example, Swiss numbers such as `079 123 45 67` and `0041 79 123 45 67` are converted to `+41791234567`.

```py
msg = bec.messaging.signal.new("Direct message using a local number.")
msg.send(scope="079 123 45 67")
```

!!! warning "Country codes required"

    BEC always normalizes valid phone numbers without country codes to use the Swiss country code `+41` by default. If you want to send messages to phone numbers in other countries, make sure to include the correct country code in the recipient number.

You can also send the same message to more than one phone number:

```py
msg = bec.messaging.signal.new("Please confirm detector status.")
msg.send(scope=["+41791234567", "+41795554433"])
```

## 3. Attach a file

Add attachments from a local path before sending the message:

```py
msg = bec.messaging.signal.new("Attached: latest detector snapshot.")
msg.add_attachment("/path/to/snapshot.png")
msg.send(scope="+41791234567")
```

Attachments must exist on disk and must be smaller than 5 MB.

<!-- TODO: Uncomment once we have a better support for stickers -->
<!-- ## 4. Add a sticker

Signal messages can include stickers:

```py
msg = bec.messaging.signal.new("Alignment completed.")
msg.add_sticker("sticker_123")
msg.send(scope="+41791234567")
```

## 5. Combine text and stickers

You can also mix text and stickers in one message:

```py
msg = bec.messaging.signal.new()
msg.add_text("The scan queue is empty.")
msg.add_sticker("sticker_123")
msg.send(scope="+41791234567")
``` -->

!!! success "Congratulations!"

    You can now send direct Signal messages from the BEC IPython client, address recipients by phone number, and include attachments when needed.

## Common pitfalls

- `bec.messaging.signal.new()` raises an error if Signal messaging is not enabled for the current deployment or session.
- `send(scope=...)` is where you provide the recipient phone number.
- `add_attachment(...)` fails if the file does not exist or is larger than 5 MB.
- Valid phone numbers are normalized automatically before sending.

---
related:
  - title: Set Up Auto Notifications
    url: set-up-auto-notifications.md
  - title: Send Messages to SciLog
    url: send-messages-to-scilog.md
  - title: Send Messages to Signal
    url: send-messages-to-signal.md
  - title: Core Services
    url: ../../learn/system-architecture/overview/core-services.md
---

# Send a custom notification event

!!! Info "Overview"
    Publish a custom notification event from BEC code so it can be routed to messaging services such as SciLog, Signal, or Teams.

## Prerequisites

- You are working in custom BEC code such as a plugin, service extension, or beamline-specific helper.
- Your code has access to a BEC connector, for example `self.connector` or `client.connector`.
- The target messaging service is enabled for your deployment or session.
- If you want the event to be forwarded automatically, you have configured a matching route in [Set Up Auto Notifications](set-up-auto-notifications.md){ data-preview }.

## Notification publish interface

Publish a notification with:

```py
connector.notify(event, message)
```

- `event` is a string such as `"beamline_ready"` or `"sample_mount_failed"`
- `message` can be either a plain string or a `NotificationMessageObject`

## 1. Send a simple custom event

If plain text is enough, send the event name together with a string message:

```py
self.connector.notify(
    "beamline_ready",
    "Beamline checks passed and the station is ready for users.",
)
```

BEC wraps the string into a notification message object automatically before routing it.

## 2. Send a richer custom event

Use `NotificationMessageObject` when you want formatted text, tags, or attachments that can be adapted to the target messaging service:

```py
from bec_lib.messaging_services import NotificationMessageObject

msg = NotificationMessageObject()
msg.add_text("Sample mount failed", bold=True, color="red")
msg.add_text(" Please check the robot status before retrying.")
msg.add_tags(["sample-exchange", "robot"])

self.connector.notify("sample_mount_failed", msg)
```

This is useful when the same event should later be routed to services with richer formatting support, especially SciLog.

## 3. Route the event to a messaging service

Publishing a custom event does not send it anywhere by itself. To forward it automatically, configure a route for the same event name from the BEC client as described in [Set Up Auto Notifications](set-up-auto-notifications.md){ data-preview }:

```py
bec.messaging.scilog.set_auto_notifications(
    "beamline_ready",
    enabled=True,
    scopes="default",
)
```

After that, every `beamline_ready` notification published by your code is forwarded to the configured SciLog scope.

## 4. Use a stable event name

Choose one event string and keep it consistent between the publisher and the routing configuration:

```py
self.connector.notify("sample_mount_failed", "Robot reported a mount failure.")
```

```py
bec.messaging.signal.set_auto_notifications(
    "sample_mount_failed",
    enabled=True,
    scopes="beamline-ops",
)
```

If the event names do not match exactly, BEC will not route the notification.

!!! success "Congratulations!"

    You can now publish custom notification events from BEC code and connect them to the automatic notification routing system.

## Common pitfalls

- `connector.notify(...)` only publishes the event. It does not automatically choose a messaging service unless you configured a matching route.
- The event name in `notify(...)` and the event name in `set_auto_notifications(...)` must match exactly.
- Use `NotificationMessageObject` when you need tags, formatting, or attachments. Use a plain string when a simple text notification is enough.

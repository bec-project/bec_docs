---
related:
  - title: Send a Custom Notification Event
    url: send-a-custom-notification-event.md
  - title: Send Messages to SciLog
    url: send-messages-to-scilog.md
  - title: Send Messages to Signal
    url: send-messages-to-signal.md
  - title: Core Services
    url: ../../learn/system-architecture/overview/core-services.md
---

# Set up auto notifications

!!! Info "Overview"
    Configure BEC to send automatic notifications for scan and alarm events through a messaging service such as SciLog or Signal.

## Prerequisites

- You have a running BEC IPython client session.
- The messaging service you want to use is enabled for your deployment or session.
- You know which target scope to use for that service, for example a SciLog logbook or a Signal group scope.

## Notification interface and event types

Auto notifications are configured per messaging service from the BEC client with:

```py
bec.messaging.<service>.set_auto_notifications(event_type, enabled=True, scopes=...)
```

Supported event types are:

<table>
  <colgroup>
    <col style="width: 28%;">
    <col style="width: 72%;">
  </colgroup>
  <thead>
    <tr>
      <th>Event type</th>
      <th>Emitted when</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>"new_scan"</code></td>
      <td>A scan enters the <code>open</code> state, meaning BEC has started the scan.</td>
    </tr>
    <tr>
      <td><code>"scan_completed"</code></td>
      <td>A scan finishes with the status <code>closed</code> or <code>user_completed</code>.</td>
    </tr>
    <tr>
      <td><code>"alarm_warning"</code></td>
      <td>BEC raises an alarm with warning severity.</td>
    </tr>
    <tr>
      <td><code>"alarm_minor"</code></td>
      <td>BEC raises an alarm with minor severity.</td>
    </tr>
    <tr>
      <td><code>"alarm_major"</code></td>
      <td>BEC raises an alarm with major severity.</td>
    </tr>
    <tr>
      <td><code>"scan_interlock"</code></td>
      <td>The scan interlock is triggered because beamline states do not match, and again when that interlock is cleared.</td>
    </tr>
  </tbody>
</table>

!!! tip "Custom event names"

    You can also use custom event names. BEC supports any event string, as long as something in your deployment publishes notifications with the same event name.

    To learn how to publish one of these events from custom BEC code, see [Send a Custom Notification Event](send-a-custom-notification-event.md){ data-preview }.

    For example, if a custom service or plugin publishes a `beamline_ready` notification, you can route it like this:

    ```py
    bec.messaging.scilog.set_auto_notifications(
        "beamline_ready",
        enabled=True,
        scopes="default",
    )
    ```

## 1. Enable an automatic notification

Enable a notification by choosing the service, event, and target scope.

For example, route new scan notifications to SciLog:

```py
bec.messaging.scilog.set_auto_notifications(
    "new_scan",
    enabled=True,
    scopes="default",
)
```

This stores a routing rule for the `new_scan` event. When a new scan starts, BEC forwards the notification to the configured SciLog scope.

You can do the same for Signal when your deployment exposes a named Signal scope:

```py
bec.messaging.signal.set_auto_notifications(
    "alarm_major",
    enabled=True,
    scopes="beamline-ops",
)
```

## 2. Add more event routes

You can enable more than one event for the same service:

```py
bec.messaging.scilog.set_auto_notifications(
    "scan_completed",
    enabled=True,
    scopes="default",
)

bec.messaging.scilog.set_auto_notifications(
    "scan_interlock",
    enabled=True,
    scopes="default",
)
```

You can also route the same event to more than one service. For example, keep SciLog for the permanent record and send major alarms to Signal as well:

```py
bec.messaging.scilog.set_auto_notifications(
    "alarm_major",
    enabled=True,
    scopes="default",
)

bec.messaging.signal.set_auto_notifications(
    "alarm_major",
    enabled=True,
    scopes="beamline-ops",
)
```

## 3. Use the default scope

If your messaging service already has a suitable default scope, set it once and omit `scopes=` afterwards:

```py
bec.messaging.scilog.set_default_scope("default")

bec.messaging.scilog.set_auto_notifications(
    "new_scan",
    enabled=True,
)
```

This is useful when most notifications should go to the same logbook or group.

## 4. Disable an automatic notification

Disable a route by setting `enabled=False` for the same event and scope:

```py
bec.messaging.scilog.set_auto_notifications(
    "new_scan",
    enabled=False,
    scopes="default",
)
```

If that was the only route for this service and event, BEC removes it from the notification configuration.

!!! success "Congratulations!"

    You have configured automatic notifications in BEC. You can now route scan and alarm events to your messaging services without sending each message manually.

## Common pitfalls

- `set_auto_notifications(...)` raises an error if the messaging service is not enabled for the current deployment or session.
- Use the supported event strings exactly as shown above.
- For services with configured scopes such as SciLog, the scope must exist before you enable auto notifications.
- Signal auto notifications are typically routed to a configured Signal scope such as a group, not to an arbitrary phone number.

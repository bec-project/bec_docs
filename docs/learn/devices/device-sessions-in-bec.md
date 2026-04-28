---
related:
  - title: Device Configuration in BEC
    url: learn/devices/device-config-in-bec.md
  - title: Managing Device Configurations
    url: learn/devices/managing-device-configs.md
  - title: Load and Save a Device Session
    url: how-to/devices/load-and-save-a-device-session-from-the-bec-ipython-client.md
  - title: Inspect the Current Device Session
    url: how-to/devices/inspect-the-current-device-session-from-the-bec-ipython-client.md
---

# Device Sessions in BEC

In BEC, a device configuration file on disk and the currently active devices in the running system are closely related, but they are not the same thing.

Understanding that difference helps explain how BEC loads devices, how runtime changes behave, and why clients can use devices without direct access to the underlying ophyd objects.

## Device configuration and device session

It is useful to separate two ideas:

- The **device configuration** is the YAML description on disk.
- The **device session** is the currently active set of devices loaded into the running BEC system.

A device session usually starts from one or more YAML configuration files, but once loaded it becomes a shared runtime state across all BEC services and clients. This state may change at runtime, and therefore may differ from the original source file on disk. This is an important distinction to keep in mind when working with devices in BEC.

!!! learn "[Learn more about the fields available in a device configuration](device-config-in-bec.md){ data-preview }"

!!! learn "[Learn how multiple config files can be combined into one effective configuration](managing-device-configs.md){ data-preview }"

## From configuration files to a device session

BEC can load device definitions from a single YAML file or from several files composed together, for example with `!include`. 
Once the configuration is loaded, BEC will try to (1) initialized an ophyd object for each device based on the provide device config, (2) connect to all underlying signals of the device, and (3) publish the resulting device interface in Redis. 

### 1. Initialize ophyd objects
On the device server, the configuration turns into a list of device definitions, each specified by the device config provided in the config file (see (./device-config-in-bec.md) for details about the device config fields). 
For each device entry, BEC resolves the configured `deviceClass`, combines it with the device's `deviceConfig`, and constructs an ophyd object on the device server.

If a device declares dependencies through `needs`, BEC resolves those dependencies first such that the device specified in `needs` is initialized first. This allows the dependent device to reference the ophyd object of the needed device.

!!! warning "Device initialization fails""

    Once a single device fails to initialize, BEC treats that as a failure for the entire session and will flush all devices from the current sessions. This means that if one device fails to initialize, the whole session will be empty and no devices will be available from the client until a new configuration is loaded.

### 2. Try to establish a connection

Directly after initialization of the ophyd object, BEC tries to connect to the underlying signals of the device. This is where connection timeouts, unreachable IOCs, or other backend-specific connection problems appear. Per default, BEC waits up to 10 seconds for a successful connection before giving up and marking the device as failed. You can adjust this timeout with the `connectionTimeout` field in the device config.


!!! warning "Device connection fails""

    If a device fails to connect within the configured timeout, BEC will disable the device in the current session, but continue to load the rest of the devices. This means that if one device fails to connect, the other devices may still be available from the client, but the failed device will be marked as disabled. 

### 3. Read and publish the device interface

Once the ophyd objects are initialized and connected to, BEC inspects its interface and publishes the relevant device information through Redis.

This published interface includes information such as:

- signals
- methods
- metadata

BEC also publishes the `read()` and `read_configuration()` data for each device during the initial publishing step.

### 4. Device Interface from the client perspective

Every BEC service and client is connected to Redis and subscribes to the published device information. When a new device session is loaded, all clients receive the updated device information and can use these devices in runtime. The interface exposes a proxy representation of the device, which looks and feels like the original ophyd object, but is not the same object. Calling methods such as `read()` and `read_configuration()` from the client triggers a communication with the device server to execute these methods on the original ophyd object, and then returns the result back to the client. This allows clients to share the same device session and use the same devices without direct access to the original ophyd objects on the device server.


## Why this distinction matters in practice

Now that we have established the difference between a device configuration, the device session, and the client interface, we have a clearer picture of how BEC handles devices across its distributed architecture. Even with multiple clients and services, there is only one active device session at a time, which is shared across the system. This means that any change to the session, whether from loading a new config file or from runtime changes in the client, affects all clients and services that rely on that session.
It further explains why there can be differences between the original YAML file on disk and the current device session.

## What to learn next

- Continue with [Device Configuration in BEC](device-config-in-bec.md) to learn the individual fields in a device entry.
- Continue with [Managing Device Configurations](managing-device-configs.md) to learn how larger configurations are composed.

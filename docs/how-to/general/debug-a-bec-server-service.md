# Debug a BEC server service in VS Code

If you want to debug a BEC service with breakpoints, VS Code is usually the easiest option.

The basic idea is:

1. keep the rest of BEC running normally
2. stop only the service you want to inspect
3. launch that service from VS Code
4. reproduce the problem from a client

This gives you breakpoints, variable inspection, stack traces, and a regular terminal for logs.

## When this is useful

This workflow is helpful when:

- logs are not enough to explain the problem
- you want to inspect object state during execution
- a service is taking an unexpected code path
- you want to step through request handling callback by callback

## Before you start

You will usually need:

- the BEC repository open in VS Code
- the correct Python environment selected in VS Code
- the same BEC config that the rest of your running services use
- a running Redis server and the rest of the BEC stack

If you normally start the stack with:

```bash
bec-server start
```

then the services are usually running in tmux. You can inspect them with:

```bash
bec-server attach
```

## Step 1: identify the service you want to debug

Typical services are:

- `bec-scan-server`
- `bec-device-server`
- `bec-file-writer`
- `bec-scihub`
- `bec-scan-bundler`

Examples:

- queueing and scan execution issues: `bec-scan-server`
- motion, device communication, RPC issues: `bec-device-server`
- file writing issues: `bec-file-writer`

## Step 2: stop the already running copy of that service

This is important. BEC services are unique services, so you generally should not run a second copy of the same one while the original is still active.

If the stack is running in tmux:

1. run `bec-server attach`
2. move to the pane of the target service
3. stop it with `Ctrl+C`
4. leave the other services running

Now VS Code can launch that service instead.

## Step 3: open the service entry file

In the BEC repository, the service entry points are the CLI launch files:

- `bec_server/bec_server/scan_server/cli/launch.py`
- `bec_server/bec_server/device_server/cli/launch.py`
- `bec_server/bec_server/file_writer/cli/launch.py`
- `bec_server/bec_server/scihub/cli/launch.py`

Open the one that matches the service you want to debug.

## Step 4: add breakpoints

Set breakpoints in the code path you want to inspect.

Good first breakpoint locations are often:

- the `main()` function in the service `launch.py`
- the callback or handler that receives the request
- the method where you suspect state becomes wrong

If you are not yet sure where the issue is, start near the service entry point and move deeper once you see the flow.

## Step 5: start the service from VS Code

The sibling BEC repository already contains a basic VS Code Python launch configuration for debugging the current file.

That means a simple workflow is:

1. open the correct `launch.py`
2. select the VS Code Run and Debug view
3. choose `Python: Debug current file`
4. start debugging

If you need command-line arguments such as `--config`, add them in the VS Code debug configuration before launching.

For example, the service should receive the same config file you would use from the terminal:

```bash
--config path/to/your_config.yaml
```

You can also pass a Redis address directly:

```bash
--bec-server localhost:6379
```

## Step 6: reproduce the problem

Once the service is running under the debugger:

- start the scan, move, or workflow from your BEC client
- let execution hit your breakpoints
- inspect variables, object attributes, and the call stack
- step over or into the next methods as needed

This is usually the clearest way to answer questions like:

- what request actually arrived here?
- what metadata did this service receive?
- why did this branch execute?
- what internal state changed just before the failure?

## Logs still help

Even when you are using breakpoints, logs are still useful.

If you want more terminal output from the service, pass a more verbose log level in the debug arguments:

```bash
--log-level DEBUG
```

or, if really necessary:

```bash
--log-level TRACE
```

`DEBUG` is usually a better first choice than `TRACE`, because `TRACE` can become noisy quickly.

You can also use:

```bash
bec-log-monitor --filter "scan_server"
```

or another suitable filter string in a separate terminal.

## A minimal VS Code workflow

For most cases, this is enough:

1. start BEC normally with `bec-server start`
2. attach with `bec-server attach`
3. stop only the target service
4. open its `launch.py` in VS Code
5. add breakpoints
6. start `Python: Debug current file`
7. pass the same config arguments as the normal service
8. reproduce the issue from the client

## Common pitfalls

- Forgetting to stop the original service before starting the VS Code one.
- Running the service with a different config from the rest of the stack.
- Using the wrong Python interpreter in VS Code.
- Putting breakpoints too deep before first confirming the request path.
- Turning on `TRACE` immediately and making the output harder to read.


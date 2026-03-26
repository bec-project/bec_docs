# Open BEC outside of PSI

!!! Info "Goal"

     In this tutorial you will prepare a complete local BEC environment outside PSI and launch it end to end. By the end, you
     will have installed the required Python packages, started Redis and the BEC server, and opened the BEC IPython client
     against a running local stack.

## Before you start

This page describes a full local setup. That means you need more than the client alone: `bec` will not work unless a BEC
server and Redis are running as well.

## Requirements

Use the following components for the recommended local setup:

| Component                                      | Why it is needed                                               |
|------------------------------------------------|----------------------------------------------------------------|
| [Python](https://www.python.org) 3.11 or newer | Required for the BEC Python packages                           |
| [Redis](https://redis.io)                      | Message transport and shared runtime state                     |
| [tmux](https://github.com/tmux/tmux/wiki)      | Recommended way to launch and manage the BEC services together |

Without a running Redis instance and BEC server, starting only the `BECIPythonClient` will not give you a usable
session.

## 1. Create and activate a Python environment

There are several ways to create a Python environment. Choose the one that matches how you normally work.

/// tab | :material-language-python: pyenv

If you use [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv),
you can create a dedicated BEC environment like this:

```bash
pyenv install 3.11
pyenv virtualenv 3.11 bec
pyenv local bec
```

`pyenv local` writes a `.python-version` file in the current directory so the environment is activated automatically
when you enter it.
///
/// tab | :material-console: Python virtual environment

If you already have [Python](https://www.python.org) 3.11 or newer installed, you can create a standard virtual environment:

```bash
python -m venv ./bec_venv
source ./bec_venv/bin/activate
```

This activates the environment only in the current shell. Leave it again with `deactivate`.

///
/// tab | :material-anvil: Conda

If you use [Conda](https://docs.conda.io), create and activate an environment like this:

```bash
conda create -n bec python=3.11
conda activate bec
```

Any environment name is fine. The only requirement is that BEC is installed into the same active environment you will use to start it.

///

## 2. Install BEC

Make sure the Python environment is active before continuing.

/// tab | :material-package-down: Standard `pip` install

Use this if you want a working BEC environment but do not need to edit the source code directly.

Install the core BEC packages:

```bash
pip install bec_lib
pip install bec_ipython_client
pip install bec-server
pip install ophyd_devices
```

If you also want the GUI stack, install BEC Widgets:

```bash
pip install bec_widgets
```

This adds the PySide6-based GUI tools, including the companion DockArea workflow, `bec-app`, and `bec-designer`.
///

/// tab | :material-hammer-wrench: Editable developer install

Use this if you want to work on BEC code directly, add devices, develop widgets, or run a local development stack.

Clone the repositories you need:

```bash
git clone https://github.com/bec-project/ophyd_devices.git
git clone https://github.com/bec-project/bec.git
git clone https://github.com/bec-project/bec_widgets.git
```

Install the BEC core packages in editable mode:

```bash
pip install -e './bec/bec_lib[dev]'
pip install -e './bec/bec_ipython_client[dev]'
pip install -e './bec/bec_server[dev]'
pip install -e './ophyd_devices[dev]'
```

If you also want the GUI and widget development tools, install BEC Widgets in editable mode:

```bash
pip install -e './bec_widgets[dev]'
```
!!! note
    The development extras install additional tools that are useful when you work on the code base directly, such as test (`pytest`), formatting (`black`), and linting dependencies.
///

!!! note
    The GUI stack is optional. Install `bec_widgets` if you want the companion DockArea workflow, `bec-app`, or
    `bec-designer`. If you only need the command-line client, you can skip it.

## 3. Install and start Redis and tmux

Open a new terminal for the service side of the stack.

/// tab | :material-anvil: Conda

If you use `conda`, install Redis and tmux like this:

```bash
conda install redis-server tmux
redis-server
```
///
/// tab | :material-apple: macOS

On macOS, install Redis and tmux with [Homebrew](https://brew.sh):

```bash
brew install redis
brew install tmux
redis-server
```
///

Redis starts on port `6379` by default.

`tmux` is the recommended way to manage the BEC services together. If you do not use it, you must start each service
manually in a separate terminal.

!!! tip
    Redis writes a `dump.rdb` file to disk. Start it in a location where a few gigabytes of writable space are available.

## 4. Start the BEC server

Go back to the terminal where your Python environment is active.

Start the service stack with:

```bash
bec-server start
```

To attach to the running service session:

```bash
bec-server attach
```

Detach from the tmux session again with `CTRL+b d`.

!!! note
    You can also attach to the same tmux session with `tmux attach -t bec` and detach again with `CTRL+b d`.

If you do not use `tmux`, you must start the services individually, for example `bec-device-server start`,
`bec-scan-server start`, and the other required services in separate terminals. The recommended path remains
`bec-server start`.

!!! note
    Strictly speaking, `tmux` is not required. It is recommended because it starts and groups the BEC services in one
    managed session instead of forcing you to launch every service manually in its own terminal.

## 5. Start the client

Now start the command-line client in new terminal window after activating the same Python environment:

```bash
bec
```

If your setup uses a non-default configuration file, pass it explicitly both to the server and the client. For the
client side, that looks like:

```bash
bec --config /path/to/client-config.yaml
```

If you need the shell only, you can suppress the GUI:

```bash
bec --nogui
```

If BEC Widgets is installed and you do not use `--nogui`, BEC starts the CLI together with the companion DockArea
workflow.

!!! note
    If you start the server with a non-default configuration, pass the matching configuration to the client as well. Server
    and client must point to the same running deployment.

## 6. Verify the session

Once the prompt appears, confirm that the main objects are present:

```python
bec
dev
scans
```

If you started with the GUI enabled, also confirm:

```python
gui
```

## 7. Leave the client running

Keep this client session open. The remaining Quick start tutorials assume you continue from the same shell.

!!! success "What you have learned"

    You prepared the full local BEC stack outside PSI: Python environment, package installation, Redis, BEC services, and
    finally the client. You also saw the difference between a standard `pip` install and an editable development install,
    and how the optional BEC Widgets package adds the GUI tools on top of the same setup.

## Next step

Continue with [03 Load your first config](03-load-your-first-config.md), where you will load a known training
configuration for the rest of the sequence.

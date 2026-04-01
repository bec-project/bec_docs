---
title: 01 Open BEC
heading: Open BEC
---

!!! info "Goal"

    In this tutorial you will start BEC either from a PSI-managed workstation or from a local environment outside PSI.
    By the end, you will have a running BEC IPython client and know how to recognize that the session is ready for the
    rest of the Quick Start sequence.

Choose the startup path that matches your environment, then continue with the common startup checks in section 5.

/// tab | :material-office-building: PSI-managed Beamline Console

### 1. Open the BEC Launcher

Use a beamline workstation or PSI-managed machine where BEC is already prepared. You should see a BEC icon in the dock
that opens the BEC Launcher where you can choose the deployment and application mode. Start BEC by clicking the BEC
icon on the beamline workstation.

If you do not see the icon, ask your local support team to set up BEC for you.

### 2. Select the deployment

If your beamline has multiple deployments, choose the one you want to work with in the first step of the launcher.

Typical reasons for multiple deployments are:

1. production and test environments
2. multiple instrument or branch setups
3. development deployments alongside the main one

If there is only one deployment available, the launcher can skip this choice automatically.

### 3. Choose how you want to interact with BEC

After choosing the deployment, the launcher offers three application modes:

1. `Terminal`
   Starts the `BECIPythonClient` in a terminal without a graphical interface.
2. `Terminal + Dock`
   Starts the `BECIPythonClient` together with the companion Dock Area window for BEC Widgets.
3. `BEC App`
   Starts the full BEC desktop application environment.

You can mark both the deployment and the launch mode as default in the launcher. When both defaults are set, the
launcher can reopen BEC the same way the next time you start it.

If you have already set defaults but want to change them later, right-click the BEC icon in the dock and choose
`Open BEC Launcher`. This opens the launcher again so you can adjust the saved deployment and launch mode.

### 4. For this tutorial, start the terminal client

To keep the first steps simple, choose `Terminal`.

This opens the `BECIPythonClient` in a terminal, which is the best place to learn the basic session objects before
adding GUI workflows.

If you prefer to keep the companion Dock Area open as well, you can choose `Terminal + Dock`. The same CLI commands
from the rest of this tutorial still apply.

///
/// tab | :material-laptop: Local environment outside PSI

### 1. Prepare the required components

For a full local setup, you need more than the client alone. `bec` will not work unless a BEC server and Redis are
running as well.

Use the following components for the recommended local setup:

| Component                                      | Why it is needed                                               |
|------------------------------------------------|----------------------------------------------------------------|
| [Python](https://www.python.org) 3.11 or newer | Required for the BEC Python packages                           |
| [Redis](https://redis.io)                      | Message transport and shared runtime state                     |
| [tmux](https://github.com/tmux/tmux/wiki)      | Recommended way to launch and manage the BEC services together |

### 2. Create and activate a Python environment

Choose the environment style that matches how you normally work.

/// tab | :material-language-python: pyenv

If you use [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv),
you can create a dedicated BEC environment like this:

```bash
pyenv install 3.11
pyenv virtualenv 3.11 bec
pyenv local bec
```
///
/// tab | :material-console: Python virtual environment

If you already have [Python](https://www.python.org) 3.11 or newer installed, create a standard virtual environment:

```bash
python -m venv ./bec_venv
source ./bec_venv/bin/activate
```
///
/// tab | :material-anvil: Conda

If you use [Conda](https://docs.conda.io), create and activate an environment like this:

```bash
conda create -n bec python=3.11
conda activate bec
```
///

### 3. Install and start BEC

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
///

Start Redis in one terminal:

/// tab | :material-anvil: Conda

```bash
conda install redis-server tmux
redis-server
```
///
/// tab | :material-apple: macOS

```bash
brew install redis
brew install tmux
redis-server
```
///

Then start the BEC service stack from the terminal where your Python environment is active:

```bash
bec-server start
```

### 4. Start the client

Open a new terminal, activate the same Python environment, and start the client:

```bash
bec
```

If you need the shell only, you can suppress the GUI:

```bash
bec --nogui
```

If BEC Widgets is installed and you do not use `--nogui`, BEC starts the CLI together with the companion Dock Area
workflow.

///

## 5. Recognize a successful startup

After the terminal opens, look for three signs that the session is ready:

1. The prompt changes to the BEC prompt and shows your user, the session name, the current command number, and the next scan number.
2. The objects `bec`, `dev`, and `scans` are available in the shell.
3. If you launched with the GUI enabled, the `gui` object is available as well.

!!! tip "BECIPython Client prompt"

    The prompt is based on IPython. A prompt such as `default@bec [4/19]` means you are in the `default` session, you are currently on command
    number `4`, and the next scan submitted in that session will receive scan number `19`.

Try the following in the shell:

```python
bec
```


## 6. Keep this session open

Leave the BEC terminal running. The remaining Quick Start tutorials continue in this same client session.

!!! success "What you have learned"

    You started BEC through the path that matches your environment, either from the PSI launcher or from a local stack
    outside PSI. You also saw the core signs of a successful startup and confirmed that the main session objects are
    ready for the rest of the Quick Start sequence.

## Next step

Continue with [02 Load your first config](02-load-your-first-config.md).

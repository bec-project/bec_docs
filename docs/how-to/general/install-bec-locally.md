---
related:
  - title: Open BEC
    url: getting-started/quick-start/01-open-bec.md
  - title: Load your first config
    url: getting-started/quick-start/02-load-your-first-config.md
---

# Install BEC locally

!!! Info "Goal"
    Install BEC in a local Python environment, start the required services, and open a working BEC client session on
    your own machine.

## Pre-requisites
- You have Python 3.11 or newer available.
- You can install Python packages in a virtual environment or Conda environment.
- You can install and run `redis-server`.
- You can install and use `tmux`.
- You have network access to the repositories you want to install from.

## 1. Create and activate a Python environment

Choose the environment style that matches your usual workflow.

/// tab | `pyenv`

If you use `pyenv` together with `pyenv-virtualenv`, create a dedicated environment:

```bash
pyenv install 3.11
pyenv virtualenv 3.11 bec
pyenv local bec
```
///
/// tab | Python virtual environment

If you already have Python 3.11 or newer installed:

```bash
python -m venv ./bec_venv
source ./bec_venv/bin/activate
```
///
/// tab | Conda

If you use Conda:

```bash
conda create -n bec python=3.11
conda activate bec
```
///

## 2. Install the BEC packages

Make sure your Python environment is active before installing anything.

Choose the installation style that matches your goal.

/// tab | Standard install

Use this if you want a working local BEC environment and do not need to edit the source code directly.

```bash
pip install bec_lib
pip install bec_ipython_client
pip install bec-server
pip install ophyd_devices
```

If you also want the widget and GUI stack:

```bash
pip install bec_widgets
```
///
/// tab | Editable developer install

Use this if you want to work on the BEC source code, add devices, or develop widgets locally.

Clone the repositories you need:

```bash
git clone https://github.com/bec-project/ophyd_devices.git
git clone https://github.com/bec-project/bec.git
git clone https://github.com/bec-project/bec_widgets.git
```

Then install the packages in editable mode:

```bash
pip install -e './bec/bec_lib[dev]'
pip install -e './bec/bec_ipython_client[dev]'
pip install -e './bec/bec_server[dev]'
pip install -e './ophyd_devices[dev]'
```

If you also want widget development tools:

```bash
pip install -e './bec_widgets[dev]'
```
///

## 3. Install and start Redis

BEC requires a running Redis server for message transport and shared runtime state.

/// tab | Conda

```bash
conda install redis-server tmux
redis-server
```
///
/// tab | macOS

```bash
brew install redis
brew install tmux
redis-server
```
///

By default, Redis starts on port `6379`.

!!! tip
    Redis writes a `dump.rdb` file in the directory where it is started. Run it in a location with enough available
    disk space.

## 4. Start the BEC service stack

Open a terminal where the same Python environment is active and start the BEC services:

```bash
bec-server start
```

This typically launches the BEC services inside `tmux`.

If you want to inspect the running services:

```bash
bec-server attach
```

Detach from the `tmux` session again with `Ctrl+b d`.

## 5. Start the client

Open a new terminal, activate the same Python environment, and start the BEC client:

```bash
bec
```

If you only want the terminal client and not the GUI:

```bash
bec --nogui
```

When startup succeeds, the prompt changes to the BEC prompt and you can run commands such as:

```python
dev.show_all()
```

## 6. Continue with your local session

At this point, BEC is running locally and ready for configuration loading, device work, or further development.

!!! Success "Congratulations!"
    You have successfully installed BEC locally and started a working client session.

## Common pitfalls
- Installing the Python packages without first activating the intended environment.
- Starting the client before `redis-server` or the BEC services are running.
- Using different Python environments for `bec-server` and `bec`.
- Forgetting that `bec-server start` usually launches the stack in `tmux`.
- Running Redis in a directory without enough free disk space.

## Next Steps
- Continue with [Open BEC](../../getting-started/quick-start/01-open-bec.md) if you want the full startup context.
- Continue with [Load your first config](../../getting-started/quick-start/02-load-your-first-config.md) to begin working in the local session.

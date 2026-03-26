---
title: 01 Open BEC
heading: Open BEC
badge: psi
---

!!! Info "Goal"
    In this tutorial you will start BEC through the PSI beamline launcher and learn how to choose the right deployment and
    application mode. By the end, you will have a running BEC IPython client and know how the launcher remembers your
    preferred startup path.

If you are not on a PSI-managed machine, continue with [02 Open BEC outside of PSI](02-open-bec-outside-psi.md) instead,
which describes how to prepare and launch a local BEC environment.

## 1. Open the BEC Launcher

Use a beamline workstation or PSI-managed machine where BEC is already prepared. You should see a BEC icon in the dock
that opens the BEC Launcher where you can choose the deployment and application mode. Start BEC by clicking the BEC icon
on the beamline workstation.

If you don't see the icon, ask your local support team to set up BEC for you.

## 2. Select the deployment

If your beamline has multiple deployments, choose the one you want to work with
in the first step of the launcher.

Typical reasons for multiple deployments are:

1. production and test environments
2. multiple instrument or branch setups
3. development deployments alongside the main one

If there is only one deployment available, the launcher can skip this choice automatically.

## 3. Choose how you want to interact with BEC

After choosing the deployment, the launcher offers three application modes:

1. `Terminal`
   Starts the `BECIPythonClient` in a terminal without a graphical interface.
2. `Terminal + Dock`
   Starts the `BECIPythonClient` together with the companion DockArea window for BEC Widgets.
3. `BEC App`
   Starts the full BEC desktop application environment.

You can mark both the deployment and the launch mode as default in the launcher. When both defaults are set, the
launcher can reopen BEC the same way the next time you start it.

If you have already set defaults but want to change them later, right-click the BEC icon in the dock and choose
`Open BEC Launcher`. This opens the launcher again so you can adjust the saved deployment and launch mode.

## 4. For this tutorial, start the terminal client

To keep the first steps simple, choose `Terminal`.

This opens the `BECIPythonClient` in a terminal, which is the best place to learn the basic session objects before
adding GUI workflows.

If you prefer to keep the companion DockArea open as well, you can choose `Terminal + Dock`. The same CLI commands from
the rest of this tutorial still apply.

## 5. Recognize a successful startup

After the terminal opens, look for three signs that the session is ready:

1. The prompt changes to the BEC prompt and shows your user, the session name, the current command number, and the next scan number.
2. The objects `bec`, `dev`, and `scans` are available in the shell.
3. If you launched `Terminal + Dock`, the `gui` object is available as well.


!!! tip "BECIPython Client prompt"

    The prompt is based on IPython. A prompt such as `default@bec [4/19]` means you are in the `default` session, you are currently on command
    number `4`, and the next scan submitted in that session will receive scan number `19`.

Try the following in the shell:

```python
bec
dev
scans
```

If you launched with the companion DockArea, also check:

```python
gui
```

## 6. Keep this session open

Leave the BEC terminal running. The remaining Quick start tutorials continue in this same client session.

!!! success "What you have learned"

    You started BEC the PSI way: through the launcher, with an explicit deployment choice and a selectable application mode.
    You also saw that the launcher can remember both the deployment and the launch mode, while the terminal client remains
    the simplest entry point for learning the core `bec`, `dev`, and `scans` objects.

## Next step

If you usually work outside the PSI-managed environment, continue
with [02 Open BEC outside of PSI](02-open-bec-outside-psi.md) instead. Otherwise go straight
to [03 Load your first config](03-load-your-first-config.md).

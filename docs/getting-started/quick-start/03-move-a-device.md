# Move a Device

!!! Info "Goal"

    In this tutorial you will make your first controlled motor move and confirm the result from the CLI. By the end, you
    will know the difference between a blocking move for learning and a non-blocking move for more advanced workflows.

## Before you start

Continue in a session where the demo configuration is already loaded, so `dev.samx` is available.

## 1. Check the current position

Start by printing the current state of the motor:

--[]->[]--test_snippet--test_quickstart.py:test_samx_wm:Check the motor info

## 2. Make and confirm a blocking move

Use `umv` to issues a move command which waits until the device reaches the requested position:

--[]->[]--test_snippet--test_quickstart.py:test_samx_blocking_move:Make a move with umv

While the motor is moving, BEC shows a progress bar in the terminal so you can follow the motion until the requested
position is reached.

![Terminal recording of `umv(dev.samx, 10)` showing the motor progress bar during the move](../assets/umv.gif)

When the command returns, the move is complete or BEC has raised an error. The same output also shows the motor state
after the move, so you can confirm that the readback is close to the requested target position.

## 3. Move the motor back

Return to a neutral position:

```python
umv(dev.samx, 0)
```

!!! success "What you have learned"

    You checked a motor state, executed a safe blocking move, and confirmed the result from the shell.

## Next step

Continue with [04 Run your first scan](04-run-your-first-scan.md), where you will use the same training devices in your first
simple scan.

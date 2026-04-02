# Move a device

!!! Info "Goal"

    In this tutorial you will make your first controlled motor move and confirm the result from the CLI. By the end, you
    will know the difference between a blocking move for learning and a non-blocking move for more advanced workflows.

## Before you start

Continue in a session where the demo configuration is already loaded, so `dev.samx` is available.

## 1. Check the current position

Start by printing the current state of the motor:

--[]->[]--test_snippet--test_quickstart.py:test_samx_wm:Check the motor info

## 2. Make and confirm a blocking move

Use `umv` for a blocking move that waits until the device reaches the requested position:

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

## 4. Know the non-blocking alternative

For later work, BEC also offers `mv`, which submits the move but does not wait for completion:

```python
mv(dev.samx, 1)
```

For Quick start, prefer `umv` because it is easier to reason about while you are learning.

!!! success "What you have learned"

    You checked a motor state, executed a safe blocking move, and confirmed the result from the shell. You also saw that
    `mv` exists for non-blocking workflows, but that `umv` is the better teaching tool for a first session.

## Next step

Continue with [04 Run your first scan](04-run-your-first-scan.md), where you will use the same training devices in your first
simple scan.

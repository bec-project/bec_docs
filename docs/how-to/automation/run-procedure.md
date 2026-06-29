

# How to run a procedure

!!! Info "Goal"
    Learn how to submit a macro to be executed by the BEC server.

## Prerequisites
    - A macro which you want to run in the background.

## Execute the procedure

Any macro defined in a BEC plugin may be executed on the server by using the procedure interface to
call it. For example if you have a macro defined as follows:

```python
def my_macro(position, relative=True):
    my_device.long_running_move(position, relative=relative)
```

You can schedule it to execute on the server using:

```python
bec.proc.run_macro("my_macro", 10, relative=False)
```

Note that the first argument to `bec.proc.run_macro` is the macro name, and it is then followed by
whichever arguments and keyword arguments the macro function expects.

!!! Success "Congratulations!"
    You have can now run tasks in the background as procedures in BEC.

## Next Steps
Learn how to manage running procedures.
<!-- TODO: make manage running procedures page -->

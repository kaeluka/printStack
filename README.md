# printStack

An `lldb` command that prints the whole stack, all globals -- and all
memory reachable from them (including heap memory).

Also dumps all information to a csv file `stack.dump`.

![](./printStack.png?raw=true)

## Dependencies

 - `lldb`
 - `termcolor` (`pip install termcolor`)

## Usage

Add to your `~/.lldbinit`, or run each time you start `lldb`:

```
command script import PATH/TO/printStack.py
```

Then call `printStack` from within `lldb`.

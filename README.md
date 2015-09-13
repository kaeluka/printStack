# printStack

An `lldb` command that prints the whole stack and all values on it.

![](./printStack.png?raw=true)

## Dependencies

 - lldb
 - `termcolor` (`pip install termcolor`)

## Usage

Add to your `~/.lldbinit`, or run each time you start `lldb`:

```
command script import PATH/TO/printStack.py
```

Then call `printFrame` from within `lldb`.

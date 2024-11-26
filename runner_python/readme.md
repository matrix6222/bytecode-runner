# Example of use
```python3
from runner_python.WindowsRunner import WindowsRunner
import ctypes

# add_two_numbers
code = b''
code += b'\x48\x8B\xC1'  # MOV RAX, RCX
code += b'\x48\x03\xC2'  # ADD RAX, RDX
code += b'\xC3'          # RET

func = WindowsRunner(
    code,                             # code
    ctypes.c_uint64,                  # return type
    ctypes.c_uint64, ctypes.c_uint64  # argument types
)
result = func(10, 20)
print(result)  # 30
```
# Shellcode allocated memory protection
| Class         | Protection  |
|---------------|-------------|
| MacOSRunner   | `R` `-` `E` |
| WindowsRunner | `R` `W` `E` |
| LinuxRunner   | `R` `W` `E` |

# Argument passing (ctypes.CFUNCTYPE, python3)
## Windows x64
- Arguments in `RCX`, `RDX`, `R8`, `R9` and `stack`.
- Return in `RAX`. 
- You can pass max 1024 arguments.
- The table applies regardless of the number of declared/typed arguments.

  | Reg        | Arg    | Reg        | Arg    | Stack      | Arg    |
  |:-----------|:-------|:-----------|:-------|:-----------|:-------|
  | RAX        | -      | R8         | `arg3` | RSP + 0x00 | -      |
  | RBX        | -      | R9         | `arg4` | RSP + 0x08 | `arg1` |
  | RCX        | `arg1` | R10        | -      | RSP + 0x10 | `arg2` |
  | RDX        | `arg2` | R11        | -      | RSP + 0x18 | `arg3` |
  | RSI        | -      | R12        | -      | RSP + 0x20 | `arg4` |
  | RDI        | -      | R13        | -      | RSP + 0x28 | `arg5` |
  | RSP        | -      | R14        | -      | RSP + 0x30 | `arg6` |
  | RBP        | -      | R15        | -      | RSP + 0x38 | `arg7` |

- Stack is trash test (16 args passed)

  |             | 0 converted | 3 converted | 16 converted |
  |------------:|:------------|:------------|--------------|
  |  0 declared | works       | works       | works        |
  |  3 declared | works       | works       | works        |
  | 16 declared | works       | works       | works        |

- Registers fill (16 args passed)

  |             | 0 converted | 3 converted | 16 converted |
  |------------:|:------------|:------------|--------------|
  |  0 declared | full        | full        | full         |
  |  3 declared | full        | full        | full         |
  | 16 declared | full        | full        | full         |

## Linux x64
- Arguments in `RDI`, `RSI`, `RDX`, `RCX`, `R8`, `R9` and `stack`.
- Return in `RAX`.
- You can pass max 1024 arguments.
- The table applies regardless of the number of declared/typed arguments.

  | Reg        | Arg    | Reg        | Arg    | Stack      | Arg     |
  |:-----------|:-------|:-----------|:-------|:-----------|:--------|
  | RAX        | -      | R8         | `arg5` | RSP + 0x00 | -       |
  | RBX        | -      | R9         | `arg6` | RSP + 0x08 | `arg7`  |
  | RCX        | `arg4` | R10        | -      | RSP + 0x10 | `arg8`  |
  | RDX        | `arg3` | R11        | -      | RSP + 0x18 | `arg9`  |
  | RSI        | `arg2` | R12        | -      | RSP + 0x20 | `arg10` |
  | RDI        | `arg1` | R13        | -      | RSP + 0x28 | `arg11` |
  | RSP        | -      | R14        | -      | RSP + 0x30 | `arg12` |
  | RBP        | -      | R15        | -      | RSP + 0x38 | `arg13` |

- Stack is trash test (16 args passed)

  |             | 0 converted | 3 converted | 16 converted |
  |------------:|:------------|:------------|--------------|
  |  0 declared | error       | error       | works        |
  |  3 declared | error       | error       | works        |
  | 16 declared | works       | works       | works        |

- Registers fill (16 args passed)

  |             | 0 converted | 3 converted | 16 converted |
  |------------:|:------------|:------------|--------------|
  |  0 declared | full        | full        | full         |
  |  3 declared | full        | full        | full         |
  | 16 declared | full        | full        | full         |

## MacOS arm64
- Arguments in `X0`, `X1`, `X2`, `X3`, `X4`, `X5`, `X6`, `X7` and `stack`.
- Return in `X0`.
- Num of passed args in `X27`.
- You can pass max 1024 arguments.

- Declared 0 types, passed 16 ctypes args

  | Reg | Arg    | Stack     | Arg     |
  |:----|:-------|:----------|:--------|
  | X0  | `arg1` | SP + 0x00 | `arg9`  |
  | X1  | `arg2` | SP + 0x08 | `arg10` |
  | X2  | `arg3` | SP + 0x10 | `arg11` |
  | X3  | `arg4` | SP + 0x18 | `arg12` |
  | X4  | `arg5` | SP + 0x20 | `arg13` |
  | X5  | `arg6` | SP + 0x28 | `arg14` |
  | X6  | `arg7` | SP + 0x30 | `arg15` |
  | X7  | `arg8` | SP + 0x38 | `arg16` |

- Declared 3 types, passed 16 ctypes args

  | Reg | Arg    | Stack     | Arg     |
  |:----|:-------|:----------|:--------|
  | X0  | `arg1` | SP + 0x00 | `arg4`  |
  | X1  | `arg2` | SP + 0x08 | `arg5`  |
  | X2  | `arg3` | SP + 0x10 | `arg6`  |
  | X3  | -      | SP + 0x18 | `arg7`  |
  | X4  | -      | SP + 0x20 | `arg8`  |
  | X5  | -      | SP + 0x28 | `arg9`  |
  | X6  | -      | SP + 0x30 | `arg10` |
  | X7  | -      | SP + 0x38 | `arg11` |

- Declared 16 types, passed 16 ctypes args

  | Reg | Arg    | Stack     | Arg     |
  |:----|:-------|:----------|:--------|
  | X0  | `arg1` | SP + 0x00 | `arg9`  |
  | X1  | `arg2` | SP + 0x08 | `arg10` |
  | X2  | `arg3` | SP + 0x10 | `arg11` |
  | X3  | `arg4` | SP + 0x18 | `arg12` |
  | X4  | `arg5` | SP + 0x20 | `arg13` |
  | X5  | `arg6` | SP + 0x28 | `arg14` |
  | X6  | `arg7` | SP + 0x30 | `arg15` |
  | X7  | `arg8` | SP + 0x38 | `arg16` |

- Stack is trash test (16 args passed)

  |             | 0 converted | 3 converted | 16 converted |
  |------------:|:------------|:------------|--------------|
  |  0 declared | error       | error       | works        |
  |  3 declared | works       | works       | works        |
  | 16 declared | works       | works       | works        |

- Registers fill (16 args passed)

  |             | 0 converted | 3 converted | 16 converted |
  |------------:|:------------|:------------|--------------|
  |  0 declared | full        | full        | full         |
  |  3 declared | partial     | partial     | partial      |
  | 16 declared | full        | full        | full         |
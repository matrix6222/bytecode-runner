# Bytecode Runner
A cross-platform tool designed to execute bytecode/shellcode. The project includes classes for Windows, Linux, and MacOS.

## Features
- Support for executing bytecode/shellcode on **Windows**, **Linux**, and **MacOS**.
- Python-specific classes in the `runner_python` folder for simplified scripting.
- Pre-built examples in assembly for all supported operating systems in folder `asm_examples`.
- Comprehensive `readme.md` files in each folder to guide usage and explain parameter handling.
- **Kernel calls** explained in `asm_examples` folder for all supported systems.

## Simply usage
```python
from runner_python.WindowsRunner import WindowsRunner
import ctypes

# add_two_numbers.asm
code = b''
code += b'\x48\x8B\xC1'  # MOV RAX, RCX
code += b'\x48\x03\xC2'  # ADD RAX, RDX
code += b'\xC3'          # RET
func = WindowsRunner(code, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64)
result = func(10, 20)
print(f'result: {result}')  # prints "result: 30"
```

## Supported systems
 - Windows
 - Linux
 - MacOS

## Supported languages
 - Python3
# Windows x86_64
## Keynotes
- When writing shellcode, prefer using relative addressing such as `LEA RAX, label` and `MOV RAX, label`.
- Compiling without linking won't calculate any offsets, they must be calculated manually.
- Compiled without linking, data in `.DATA` or `.CODE`.
  - The compiler assumes `RIP + 0x0` for labels.
  - Calculate the offset from the start of the next instruction to the label.
  - Modify the instruction to use `RIP + offset`, replacing the last 4 bytes with the offset in little-endian format.
  - Use the relocation table `objdump -r` to identify address references.
- Compiled and linked, data in `.DATA`.
  - The linker will calculate the offsets to the labels in data.
  - Linker with parameter `/BASE:0x0` will place the code at address `0x1000` and the data at address `0x3000`.
  - The empty section between addresses `0x0000` and `0x0FFF` can be removed.
    This will result in the code starting at address `0x0000` and the data at `0x2000`. The offsets will still be correct.
  - To eliminate the gap between the end of the code (e.g., at address `0x0094`) and the beginning of the data (at `0x2000`), the data can be shifted downward by `0x1F68` to address `0x0098`.
    However, in this case, all relative addresses must also be adjusted by subtracting the same offset, i.e., `0x1F68`.
  - The data must start at an address divisible by 8, so 3 bytes of padding should be added to the code if length of code is `0x0095` and then the data at address `0x0098`.
- Compiled and linked, data in `.CODE`.
  - Add `ALIGN 8` before data.
  - The linker will calculate the offsets to the labels in data.
  - Data will be placed after the code (with padding).
  - The empty section between addresses `0x0000` and `0x0FFF` can be removed.
- When a structure contains a pointer to another structure, calculate the address of the target in the code to avoid static absolute addresses.
  ```asm
  UNICODE_STRING  DW 22       ; USHORT Length
                  DW 24       ; USHORT MaximumLength;
                  DD 0        ;        Padding
                  DQ filename ; PWSTR  Buffer

  filename        DW '\', '?', '?', '\', 'C', 'O', 'N', 'O', 'U', 'T', '$', 0
  ```
  ```asm
  LEA RAX, filename       ; address of filename
  LEA RBX, UNICODE_STRING ; address of UNICODE_STRING
  MOV [RBX + 8], RAX      ; UNICODE_STRING->Buffer = address of filename
  ```
- Compile locally rather than online.
### Compilation
- Online compilers:
  - https://defuse.ca/online-x86-assembler.htm
  - https://shell-storm.org/online/Online-Assembler-and-Disassembler/ (x86 (64))
- Compile locally without linking
  ```bash
  cd bytecode_examples
  ml64 /c /Fo temp/prog.obj x86_64_windows/prog.asm
  objdump -M intel --insn-width=16 -d temp/prog.obj  # Disassemble to see the instructions
  objdump -s temp/prog.obj                           # Display hex of .code and .data
  ```
- Compile locally with linking (to executable)
  ```bash
  cd bytecode_examples
  ml64 x86_64_windows/prog.asm /link /ENTRY:main /BASE:0x0 /OUT:temp/prog.exe
  objdump -M intel --insn-width=16 -d temp/prog.exe  # Disassemble to see the instructions
  objdump -s temp/prog.exe                           # Display hex of .code and .data
  ./temp/prog.exe                                    # Run the executable
  $LastExitCode                                      # Get exit code (RAX content)
  ```

## Kernel calls
- The `SYSCALL` number is placed in `RAX`.
- Arguments are passed in `R10`, `RDX`, `R8`, and `R9`.
- A 32-byte reservation on the stack is always required.
- Additional arguments are pushed onto the stack.
- Before the call, 8 bytes must be reserved on the stack.
- The return value is stored in `RAX`.
- Unofficial system calls: https://j00ru.vexillium.org/syscalls/nt/64/
  ```asm
  SUB RSP, 32 + 2 * 8             ; shadow space + 2 args on the stack
  LEA R10, arg_1                  ; pointer
  LEA RDX, arg_2                  ; pointer
  MOV R8,  arg_3                  ; value
  MOV R9,  arg_4                  ; value
  MOV QWORD PTR [rsp + 32], arg_5 ; value
  MOV QWORD PTR [rsp + 40], arg_6 ; value
  MOV RAX, 85                     ; SYSCALL NUMBER
  SUB RSP, 8                      ; Additional 8 bytes on the stack
  SYSCALL
  RSP, 32 + 2 * 8 + 8             ; shadow space + 2 args on the stack + 8 bytes
  ```
## ASM notes
- `RIP` offset always calculated in linking process
- Compiling provide `RIP` offset equals `0x0` (always)
- `RIP` points to begin of next instruction
  ```ASM
  ; label in .DATA
  MOV RAX, VAL_DATA    ; get QD value of label `VAL_DATA`
  MOV RAX, [VAL_DATA]  ; get QD value of label `VAL_DATA`
  
  ;LEA RAX, VAL_DATA   ; get address of label 'VAL_DATA'
  ;LEA RAX, [VAL_DATA] ; get address of label 'VAL_DATA'
  
  ; label in .CODE
  MOV RAX, VAL_CODE    ; get QD value of label `VAL_CODE`
  MOV RAX, [VAL_CODE]  ; get QD value of label `VAL_CODE`
  
  LEA RAX, VAL_CODE    ; get address of label 'VAL_CODE'
  LEA RAX, [VAL_CODE]  ; get address of label 'VAL_CODE'
  ```
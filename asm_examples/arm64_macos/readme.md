# MacOS arm64
## Key notes
- When writing shellcode, prefer using `ADR` instead of `ADRP + ADD`.
- With `ADRP + ADD`, the offset to the label must be calculated manually. To do this:
  - Use `ADRP X0, #0x0` to load the page containing the shellcode into `X0`. The compiler automatically provides this instruction, it is modified during the linking process. This gives you the base address of the shellcode.
  - Then, add the offset to the label. Since the label is placed right after the executable code in shellcode, this offset equals the length of the executable code. `ADD X0, X0, #28`
- The `ADR` instruction calculates the offset to the label automatically, but the label must be in the same section (do not place the label in the `.data` section if the instruction is in `.text`).
- Compile locally rather than online.
### Compilation
- Online compilers:
  - https://armconverter.com
  - https://shell-storm.org/online/Online-Assembler-and-Disassembler/ (AArch64)
- Compile locally without linking
  ```bash
  cd asm_examples
  clang -c arm64_macos/prog.asm -o temp/prog.o
  objdump -d temp/prog.o   # Disassemble to see the instructions
  objdump -t temp/prog.o   # Display the symbol table
  ```
- Compile locally with linking (to executable)
  ```bash
  cd asm_examples
  clang arm64_macos/prog.asm -o temp/prog
  ./temp/prog   # Run the executable
  ```

## Kernel calls
- The system call number is placed in `X16`.
- Arguments are passed in `X0`, `X1`, `X2`, `X3`, `X4`, `X5`, `X6` and `X7`.
Probably also `X8` but max number of arguments in syscalls.master is 8.
- There are no arguments on stack.
- Return is in `X0` and sometimes in `X0` and `X1` (e.g. fork).
- `SVC #1234` value is required but ignored, use `#0xFFFF` to avoid `0x00` bytes.
- System calls: https://github.com/opensource-apple/xnu/blob/master/bsd/kern/syscalls.master
  ```asm
  .align 4
  _main:
      MOV X0, #1   ; arg1 fd (stdout)
      ADR X1, msg  ; arg2 address of text
      MOV X2, #13  ; arg3 length of text
      MOV X16, #4  ; syscall number (write)
      SVC #0xFFFF
      RET
  msg: .ascii "Hello world\n"
  ```
## ASM notes
### Move value between registers
- Basic move
  - Max value of `imm` is 65535.
  ```ASM
  MOV X0, X1       ; X0 = X1
  MOV X0, #8       ; X0 = 8
  MOV X0, #0x1234  ; X0 = 0x1234
  ```
- Partial move
  - Max value of imm is 65535.
  - `LSL` must be 0, 16, 32, 48.
  ```ASM
  MOVK X0, #0xBBBB, LSL #32   ; keep ; 0xFEDC BA98 765 43210 -> 0xFEDC BBBB 7654 3210
  MOVZ X0, #0xBBBB, LSL #32   ; zero ; 0xFEDC BA98 765 43210 -> 0x0000 BBBB 0000 0000
  MOVN X0, #0xBBBB, LSL #32   ;  neg ; 0xFEDC BA98 765 43210 -> 0xFFFF 4444 FFFF FFFF
  ```
- Set 64-bit value.
  ```ASM
  MOVK X0, #0xFEDC, LSL #48   ; X0 = 0xFEDC 0000 0000 0000
  MOVK X0, #0xBA98, LSL #32   ; X0 = 0xFEDC BA98 0000 0000
  MOVK X0, #0x7654, LSL #16   ; X0 = 0xFEDC BA98 7654 0000
  MOVK X0, #0x3210, LSL #00   ; X0 = 0xFEDC BA98 7654 3210
  ```
### Load value from memory
- The `imm` value must be divisible by 1.
- `LSL`, `UXTW` must be `#0` or `#3` for `X` destination register and `#0` or `#2` for `W` destination register.
    ```ASM
    LDR X0, [X1]      ; normal     ; load from X1,      X1 = X1
    LDR X0, [X1, #8]  ; offset     ; load from X1 +  8, X1 = X1
    LDR X0, [X1, #8]! ; pre-index  ; load from X1 +  8, X1 = X1 + 8
    LDR X0, [X1], #8  ; post-index ; load from X1,      X1 = X1 + 8
    
    LDR X0, msg       ; normal     ; load from msg, label must be in the same segment
  
    LDR X0, [X1, X2]          ; offset         ; load from X1 + X2
    LDR X0, [X1, X2, LSL #3]  ; shifted-offset ; load from X1 + (X2 << 3)
    LDR X0, [X1, W0, UXTW #3] ; shifted-offset ; load from X1 + (W2 << 3)
    ```
### Load a pair of values from memory
- The `imm` value must be divisible by 8 for `X` registers and by 4 for `W` registers.
- There's no load from label or offset by register.
    ```ASM
    LDP X0, X1, [X2]       ; normal     ; X0 = [X2],      X1 = [X2 + 8],      X2 = X2
    LDP X0, X1, [X2, #16]  ; offset     ; X0 = [X2 + 16], X1 = [X2 + 16 + 8], X2 = X2
    LDP X0, X1, [X2, #16]! ; pre-index  ; X0 = [X2 + 16], X1 = [X2 + 16 + 8], X2 = X2 + 16
    LDP X0, X1, [X2], #16  ; post-index ; X0 = [X2],      X1 = [X2 + 8],      X2 = X2 + 16
    ```
### Get address
- Calculated during compilation.
  - The label must be placed in the same segment, e.g., `.text`.
  - The maximum value of `imm` is 2**20 - 1.
  - `PC` points to the beginning of the `ADR` instruction.
      ```ASM
      ADR X0, msg        ; X0 = PC + offset to label
      ADR X0, #7         ; X0 = PC + imm
      ```
- Calculated during linking.
  - The label can be placed in a different segment, e.g., `.data`.
    ```ASM
    ADRP X0, msg@PAGE
    ADD X0, X0, msg@PAGEOFF
    ```
### Automatic string length calculation
- Calculated during compilation.
- It can be used in `.data` and `.text` sections.
- It does not generate any additional code, it simply replaces `#msg_len` with `#13`.
  ```ASM
  MOV X2, #msg_len
  
  msg: .ascii "Hello world!\n"
  .equ msg_len, . -msg
  ```
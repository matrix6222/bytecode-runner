# Linux x86_64
## Keynotes
- When writing shellcode, use relative addressing such as `MOV RAX, [label_in_text]` and `LEA RAX, [label_in_text]`.
- Use `DEFAULT REL` at the beginning of the assembly file to ensure NASM uses relative addressing `RIP + offset`.
- The compiler will calculate the offset to the label automatically if the label will be in the `.text` section.
- If the label is in the `.data` section, the offset must be calculated manually.
- `RIP` points to begin of next instruction.
- Compile locally rather than online.
### Compilation
- Online compilers:
  - https://defuse.ca/online-x86-assembler.htm
  - https://shell-storm.org/online/Online-Assembler-and-Disassembler/ (x86 (64))
- Compile locally without linking
  ```bash
  cd asm_examples
  nasm -f elf64 -o temp/prog.o x86_64_linux/prog.asm
  objdump -M intel --insn-width=16 -d temp/prog.o    # Disassemble to see the instructions
  objdump -s temp/prog.o                             # Display hex of .text and .data
  ```
- Compile locally with linking (to executable)
  ```bash
  cd asm_examples
  nasm -f elf64 -o temp/prog.o x86_64_linux/prog.asm
  ld -o temp/prog temp/prog.o
  objdump -M intel --insn-width=16 -d temp/prog      # Disassemble to see the instructions
  objdump -s temp/prog.o                             # Display hex of .code and .data
  ./temp/prog                                        # Run the executable
  echo $?                                            # Get exit code (RAX content)
  ```

## Kernel calls
- Syscall number in `RAX`.
- Arguments in `RDI`, `RSI`, `RDX`, `R10`, `R8`, and `R9`.
- Return value in `RAX`.
- System calls https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86_64-64_bit
  ```asm
  MOV RAX, 1    ; syscall number (x86_64 write is 1)
  MOV RDI, 1    ; fd (1 is stdout)
  MOV RSI, msg  ; msg addr
  MOV RDX, 6    ; msg len
  SYSCALL
  ```

## ASM notes
- Addressing and Value Loading with `LEA` and `MOV`.
  ```asm
  ; label in .DATA                                       ; compilation result
  MOV RAX, VAL_DATA   ; get address of label `VAL_DATA`  ; 48 b8 00 00 00 00 00 00 00 00 movabs rax,0x0
  MOV RAX, [VAL_DATA] ; get QD value of label `VAL_DATA` ; 48 8b 05 00 00 00 00          mov rax,QWORD PTR [rip+0x0]
  LEA RAX, VAL_DATA   ; incorrect
  LEA RAX, [VAL_DATA] ; get address of label 'VAL_DATA'  ; 48 8d 05 00 00 00 00          lea rax,[rip+0x0]
  
  ; label in .CODE
  MOV RAX, VAL_CODE   ; get address of label `VAL_CODE`  ; 48 b8 00 00 00 00 00 00 00 00 movabs rax,0x0
  MOV RAX, [VAL_CODE] ; get QD value of label `VAL_CODE` ; 48 8b 05 01 00 00 00          mov rax,QWORD PTR [rip+0x1]
  LEA RAX, VAL_CODE   ; incorrect
  LEA RAX, [VAL_CODE] ; get address of label 'VAL_CODE'  ; 48 8d 05 01 00 00 00          lea rax,[rip+0x1]
  ```
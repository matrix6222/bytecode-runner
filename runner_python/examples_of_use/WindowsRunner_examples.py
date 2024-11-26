from runner_python.WindowsRunner import WindowsRunner
import ctypes
import numpy as np


# print_NtOpenFile_NtWriteFile_NtClose.asm
# code = b''
# code += b'\x48\x8D\x05\x39\x01\x00\x00'                                      # LEA    RAX,[RIP+0x139]             # 0x140
# code += b'\x48\x8D\x1D\x0A\x01\x00\x00'                                      # LEA    RBX,[RIP+0x10A]             # 0x118
# code += b'\x48\x89\x43\x08'                                                  # MOV    QWORD PTR [RBX+0x8],RAX
# code += b'\x48\x8D\x05\xCF\x00\x00\x00'                                      # LEA    RAX,[RIP+0xCF]              # 0xE8
# code += b'\x48\x89\x58\x10'                                                  # MOV    QWORD PTR [RAX+0x10],RBX
# code += b'\x48\x83\xEC\x30'                                                  # SUB    RSP,0x30
# code += b'\x4C\x8D\x15\x10\x01\x00\x00'                                      # LEA    R10,[RIP+0x110]             # 0x138
# code += b'\x48\xC7\xC2\x16\x01\x12\x00'                                      # MOV    RDX,0x120116
# code += b'\x4C\x8D\x05\xB2\x00\x00\x00'                                      # LEA    R8,[RIP+0xB2]               # 0xE8
# code += b'\x4C\x8D\x0D\xEB\x00\x00\x00'                                      # LEA    R9,[RIP+0xEB]               # 0x128
# code += b'\x48\xC7\x44\x24\x20\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x20],0x0
# code += b'\x48\xC7\x44\x24\x28\x20\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x28],0x20
# code += b'\x48\xC7\xC0\x33\x00\x00\x00'                                      # MOV    RAX,0x33
# code += b'\x48\x83\xEC\x08'                                                  # SUB    RSP,0x8
# code += b'\x0F\x05'                                                          # SYSCALL
# code += b'\x48\x83\xC4\x38'                                                  # ADD    RSP,0x38
# code += b'\x48\x83\xEC\x48'                                                  # SUB    RSP,0x48
# code += b'\x4C\x8B\x15\xCD\x00\x00\x00'                                      # MOV    R10,QWORD PTR [RIP+0xCD]    # 0x138
# code += b'\x48\xC7\xC2\x00\x00\x00\x00'                                      # MOV    RDX,0x0
# code += b'\x49\xC7\xC0\x00\x00\x00\x00'                                      # MOV    R8,0x0
# code += b'\x49\xC7\xC1\x00\x00\x00\x00'                                      # MOV    R9,0x0
# code += b'\x48\x8D\x05\xA1\x00\x00\x00'                                      # LEA    RAX,[RIP+0xA1]              # 0x128
# code += b'\x48\x89\x44\x24\x20'                                              # MOV    QWORD PTR [RSP+0x20],RAX
# code += b'\x48\x8D\x05\xC5\x00\x00\x00'                                      # LEA    RAX,[RIP+0xC5]              # 0x158
# code += b'\x48\x89\x44\x24\x28'                                              # MOV    QWORD PTR [RSP+0x28],RAX
# code += b'\x48\xC7\x44\x24\x30\x0D\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x30],0xD
# code += b'\x48\xC7\x44\x24\x38\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x38],0x0
# code += b'\x48\xC7\x44\x24\x40\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x40],0x0
# code += b'\x48\xC7\xC0\x08\x00\x00\x00'                                      # MOV    RAX,0x8
# code += b'\x48\x83\xEC\x08'                                                  # SUB    RSP,0x8
# code += b'\x0F\x05'                                                          # SYSCALL
# code += b'\x48\x83\xC4\x50'                                                  # ADD    RSP,0x50
# code += b'\x48\x83\xEC\x20'                                                  # SUB    RSP,0x20
# code += b'\x4C\x8B\x15\x69\x00\x00\x00'                                      # MOV    R10,QWORD PTR [RIP+0x69]    # 0x138
# code += b'\x48\xC7\xC0\x0F\x00\x00\x00'                                      # MOV    RAX,0xF
# code += b'\x48\x83\xEC\x08'                                                  # SUB    RSP,0x8
# code += b'\x0F\x05'                                                          # SYSCALL
# code += b'\x48\x83\xC4\x28'                                                  # ADD    RSP,0x28
# code += b'\xC3'                                                              # RET
# code += b'\x00\x00\x00\x00\x00\x00\x00'                                      # PADDING
# code += b'\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x0E8  0 . . . . . . . . . . . . . . .
# code += b'\x30\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x0F8  0 0 . . . . . . . . . . . . . .
# code += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x108  . . . . . . . . . . . . . . . .
# code += b'\x16\x00\x18\x00\x00\x00\x00\x00\x58\x30\x00\x00\x00\x00\x00\x00'  # 0x118  . . . . . . . . X 0 . . . . . .
# code += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x128  . . . . . . . . . . . . . . . .
# code += b'\x00\x00\x00\x00\x00\x00\x00\x00\x5C\x00\x3F\x00\x3F\x00\x5C\x00'  # 0x138  . . . . . . . . \ . ? . ? . \ .
# code += b'\x43\x00\x4F\x00\x4E\x00\x4F\x00\x55\x00\x54\x00\x24\x00\x00\x00'  # 0x148  C . O . N . O . U . T . $ . . .
# code += b'\x48\x65\x6C\x6C\x6F\x20\x77\x6F\x72\x6C\x64\x0A\x00'              # 0x158  H e l l o   w o r l d . .
# func = WindowsRunner(code)
# func()


# print_NtCreateFile_NtWriteFile_NtClose.asm
# code = b''
# code += b'\x48\x8D\x05\x61\x01\x00\x00'                                      # LEA    RAX,[RIP+0x161]             # 0x168
# code += b'\x48\x8D\x1D\x32\x01\x00\x00'                                      # LEA    RBX,[RIP+0x132]             # 0x140
# code += b'\x48\x89\x43\x08'                                                  # MOV    QWORD PTR [RBX+0x8],RAX
# code += b'\x48\x8D\x05\xF7\x00\x00\x00'                                      # LEA    RAX,[RIP+0xF7]              # 0x110
# code += b'\x48\x89\x58\x10'                                                  # MOV    QWORD PTR [RAX+0x10],RBX
# code += b'\x48\x83\xEC\x58'                                                  # SUB    RSP,0x58
# code += b'\x4C\x8D\x15\x38\x01\x00\x00'                                      # LEA    R10,[RIP+0x138]             # 0x160
# code += b'\x48\xC7\xC2\x16\x01\x12\x00'                                      # MOV    RDX,0x120116
# code += b'\x4C\x8D\x05\xDA\x00\x00\x00'                                      # LEA    R8,[RIP+0xDA]               # 0x110
# code += b'\x4C\x8D\x0D\x13\x01\x00\x00'                                      # LEA    R9,[RIP+0x113]              # 0x150
# code += b'\x48\xC7\x44\x24\x20\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x20],0x0
# code += b'\x48\xC7\x44\x24\x28\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x28],0x0
# code += b'\x48\xC7\x44\x24\x30\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x30],0x0
# code += b'\x48\xC7\x44\x24\x38\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x38],0x0
# code += b'\x48\xC7\x44\x24\x40\x20\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x40],0x20
# code += b'\x48\xC7\x44\x24\x48\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x48],0x0
# code += b'\x48\xC7\x44\x24\x50\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x50],0x0
# code += b'\x48\xC7\xC0\x55\x00\x00\x00'                                      # MOV    RAX,0x55
# code += b'\x48\x83\xEC\x08'                                                  # SUB    RSP,0x8
# code += b'\x0F\x05'                                                          # SYSCALL
# code += b'\x48\x83\xC4\x60'                                                  # ADD    RSP,0x60
# code += b'\x48\x83\xEC\x48'                                                  # SUB    RSP,0x48
# code += b'\x4C\x8B\x15\xC8\x00\x00\x00'                                      # MOV    R10,QWORD PTR [RIP+0xC8]    # 0x160
# code += b'\x48\xC7\xC2\x00\x00\x00\x00'                                      # MOV    RDX,0x0
# code += b'\x49\xC7\xC0\x00\x00\x00\x00'                                      # MOV    R8,0x0
# code += b'\x49\xC7\xC1\x00\x00\x00\x00'                                      # MOV    R9,0x0
# code += b'\x48\x8D\x05\x9C\x00\x00\x00'                                      # LEA    RAX,[RIP+0x9C]              # 0x150
# code += b'\x48\x89\x44\x24\x20'                                              # MOV    QWORD PTR [RSP+0x20],RAX
# code += b'\x48\x8D\x05\xC0\x00\x00\x00'                                      # LEA    RAX,[RIP+0xC0]              # 0x180
# code += b'\x48\x89\x44\x24\x28'                                              # MOV    QWORD PTR [RSP+0x28],RAX
# code += b'\x48\xC7\x44\x24\x30\x0D\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x30],0xD
# code += b'\x48\xC7\x44\x24\x38\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x38],0x0
# code += b'\x48\xC7\x44\x24\x40\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x40],0x0
# code += b'\x48\xC7\xC0\x08\x00\x00\x00'                                      # MOV    RAX,0x8
# code += b'\x48\x83\xEC\x08'                                                  # SUB    RSP,0x8
# code += b'\x0F\x05'                                                          # SYSCALL
# code += b'\x48\x83\xC4\x50'                                                  # ADD    RSP,0x50
# code += b'\x48\x83\xEC\x20'                                                  # SUB    RSP,0x20
# code += b'\x4C\x8B\x15\x64\x00\x00\x00'                                      # MOV    R10,QWORD PTR [RIP+0x64]    # 0x160
# code += b'\x48\xC7\xC0\x0F\x00\x00\x00'                                      # MOV    RAX,0xF
# code += b'\x48\x83\xEC\x08'                                                  # SUB    RSP,0x8
# code += b'\x0F\x05'                                                          # SYSCALL
# code += b'\x48\x83\xC4\x28'                                                  # ADD    RSP,0x28
# code += b'\xC3'                                                              # RET
# code += b'\x00\x00'                                                          # PADDING
# code += b'\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x110
# code += b'\x30\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x120
# code += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x130
# code += b'\x16\x00\x18\x00\x00\x00\x00\x00\x58\x30\x00\x00\x00\x00\x00\x00'  # 0x140
# code += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x150
# code += b'\x00\x00\x00\x00\x00\x00\x00\x00\x5C\x00\x3F\x00\x3F\x00\x5C\x00'  # 0x160
# code += b'\x43\x00\x4F\x00\x4E\x00\x4F\x00\x55\x00\x54\x00\x24\x00\x00\x00'  # 0x170
# code += b'\x48\x65\x6C\x6C\x6F\x20\x77\x6F\x72\x6C\x64\x0A\x00'              # 0x180
# func = WindowsRunner(code)
# func()


# print_by_args.asm
# code = b''
# code += b'\x4C\x8B\xE1'                                                      # MOV    R12,RCX
# code += b'\x4C\x8B\xEA'                                                      # MOV    R13,RDX
# code += b'\x48\x8D\x05\x2B\x01\x00\x00'                                      # LEA    RAX,[RIP+0x12B]             # 0x138
# code += b'\x48\x8D\x1D\xFC\x00\x00\x00'                                      # LEA    RBX,[RIP+0xFC]              # 0x110
# code += b'\x48\x89\x43\x08'                                                  # MOV    QWORD PTR [RBX+0x8],RAX
# code += b'\x48\x8D\x05\xC1\x00\x00\x00'                                      # LEA    RAX,[RIP+0xC1]              # 0xE0
# code += b'\x48\x89\x58\x10'                                                  # MOV    QWORD PTR [RAX+0x10],RBX
# code += b'\x48\x83\xEC\x30'                                                  # SUB    RSP,0x30
# code += b'\x4C\x8D\x15\x02\x01\x00\x00'                                      # LEA    R10,[RIP+0x102]             # 0x130
# code += b'\x48\xC7\xC2\x16\x01\x12\x00'                                      # MOV    RDX,0x120116
# code += b'\x4C\x8D\x05\xA4\x00\x00\x00'                                      # LEA    R8,[RIP+0xA4]               # 0xE0
# code += b'\x4C\x8D\x0D\xDD\x00\x00\x00'                                      # LEA    R9,[RIP+0xDD]               # 0x120
# code += b'\x48\xC7\x44\x24\x20\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x20],0x0
# code += b'\x48\xC7\x44\x24\x28\x20\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x28],0x20
# code += b'\x48\xC7\xC0\x33\x00\x00\x00'                                      # MOV    RAX,0x33
# code += b'\x48\x83\xEC\x08'                                                  # SUB    RSP,0x8
# code += b'\x0F\x05'                                                          # SYSCALL
# code += b'\x48\x83\xC4\x38'                                                  # ADD    RSP,0x38
# code += b'\x48\x83\xEC\x48'                                                  # SUB    RSP,0x48
# code += b'\x4C\x8B\x15\xBF\x00\x00\x00'                                      # MOV    R10,QWORD PTR [RIP+0xBF]    # 0x130
# code += b'\x48\xC7\xC2\x00\x00\x00\x00'                                      # MOV    RDX,0x0
# code += b'\x49\xC7\xC0\x00\x00\x00\x00'                                      # MOV    R8,0x0
# code += b'\x49\xC7\xC1\x00\x00\x00\x00'                                      # MOV    R9,0x0
# code += b'\x48\x8D\x05\x93\x00\x00\x00'                                      # LEA    RAX,[RIP+0x93]              # 0x120
# code += b'\x48\x89\x44\x24\x20'                                              # MOV    QWORD PTR [RSP+0x20],RAX
# code += b'\x4C\x89\x6C\x24\x28'                                              # MOV    QWORD PTR [RSP+0x28],R13
# code += b'\x4C\x89\x64\x24\x30'                                              # MOV    QWORD PTR [RSP+0x30],R12
# code += b'\x48\xC7\x44\x24\x38\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x38],0x0
# code += b'\x48\xC7\x44\x24\x40\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x40],0x0
# code += b'\x48\xC7\xC0\x08\x00\x00\x00'                                      # MOV    RAX,0x8
# code += b'\x48\x83\xEC\x08'                                                  # SUB    RSP,0x8
# code += b'\x0F\x05'                                                          # SYSCALL
# code += b'\x48\x83\xC4\x50'                                                  # ADD    RSP,0x50
# code += b'\x48\x83\xEC\x20'                                                  # SUB    RSP,0x20
# code += b'\x4C\x8B\x15\x66\x00\x00\x00'                                      # MOV    R10,QWORD PTR [RIP+0x66]    # 0x130
# code += b'\x48\xC7\xC0\x0F\x00\x00\x00'                                      # MOV    RAX,0xF
# code += b'\x48\x83\xEC\x08'                                                  # SUB    RSP,0x8
# code += b'\x0F\x05'                                                          # SYSCALL
# code += b'\x48\x83\xC4\x28'                                                  # ADD    RSP,0x28
# code += b'\xC3'                                                              # RET
# code += b'\x00\x00\x00\x00'                                                  # PADDING
# code += b'\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x0E0
# code += b'\x30\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x0F0
# code += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x100
# code += b'\x16\x00\x18\x00\x00\x00\x00\x00\x58\x30\x00\x00\x00\x00\x00\x00'  # 0x110
# code += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x120
# code += b'\x00\x00\x00\x00\x00\x00\x00\x00\x5C\x00\x3F\x00\x3F\x00\x5C\x00'  # 0x130
# code += b'\x43\x00\x4F\x00\x4E\x00\x4F\x00\x55\x00\x54\x00\x24\x00\x00\x00'  # 0x140
# string = b'Hello world from python\n'
# string_len = len(string)
# func = WindowsRunner(code, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_char_p)
# func(string_len, string)


# print_by_stack.asm
# code = b''
# code += b'\x4C\x8B\xE1'                                                      # MOV    R12,RCX
# code += b'\x4C\x8B\xEC'                                                      # MOV    R13,RSP
# code += b'\x49\x83\xC5\x10'                                                  # ADD    R13,0x10
# code += b'\x48\x8D\x05\x27\x01\x00\x00'                                      # LEA    RAX,[RIP+0x127]             # 0x138
# code += b'\x48\x8D\x1D\xF8\x00\x00\x00'                                      # LEA    RBX,[RIP+0xF8]              # 0x110
# code += b'\x48\x89\x43\x08'                                                  # MOV    QWORD PTR [RBX+0x8],RAX
# code += b'\x48\x8D\x05\xBD\x00\x00\x00'                                      # LEA    RAX,[RIP+0xBD]              # 0xE0
# code += b'\x48\x89\x58\x10'                                                  # MOV    QWORD PTR [RAX+0x10],RBX
# code += b'\x48\x83\xEC\x30'                                                  # SUB    RSP,0x30
# code += b'\x4C\x8D\x15\xFE\x00\x00\x00'                                      # LEA    R10,[RIP+0xFE]              # 0x130
# code += b'\x48\xC7\xC2\x16\x01\x12\x00'                                      # MOV    RDX,0x120116
# code += b'\x4C\x8D\x05\xA0\x00\x00\x00'                                      # LEA    R8,[RIP+0xA0]               # 0xE0
# code += b'\x4C\x8D\x0D\xD9\x00\x00\x00'                                      # LEA    R9,[RIP+0xD9]               # 0x120
# code += b'\x48\xC7\x44\x24\x20\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x20],0x0
# code += b'\x48\xC7\x44\x24\x28\x20\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x28],0x20
# code += b'\x48\xC7\xC0\x33\x00\x00\x00'                                      # MOV    RAX,0x33
# code += b'\x48\x83\xEC\x08'                                                  # SUB    RSP,0x8
# code += b'\x0F\x05'                                                          # SYSCALL
# code += b'\x48\x83\xC4\x38'                                                  # ADD    RSP,0x38
# code += b'\x48\x83\xEC\x48'                                                  # SUB    RSP,0x48
# code += b'\x4C\x8B\x15\xBB\x00\x00\x00'                                      # MOV    R10,QWORD PTR [RIP+0xBB]    # 0x130
# code += b'\x48\xC7\xC2\x00\x00\x00\x00'                                      # MOV    RDX,0x0
# code += b'\x49\xC7\xC0\x00\x00\x00\x00'                                      # MOV    R8,0x0
# code += b'\x49\xC7\xC1\x00\x00\x00\x00'                                      # MOV    R9,0x0
# code += b'\x48\x8D\x05\x8F\x00\x00\x00'                                      # LEA    RAX,[RIP+0x8F]              # 0x120
# code += b'\x48\x89\x44\x24\x20'                                              # MOV    QWORD PTR [RSP+0x20],RAX
# code += b'\x4C\x89\x6C\x24\x28'                                              # MOV    QWORD PTR [RSP+0x28],R13
# code += b'\x4C\x89\x64\x24\x30'                                              # MOV    QWORD PTR [RSP+0x30],R12
# code += b'\x48\xC7\x44\x24\x38\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x38],0x0
# code += b'\x48\xC7\x44\x24\x40\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x40],0x0
# code += b'\x48\xC7\xC0\x08\x00\x00\x00'                                      # MOV    RAX,0x8
# code += b'\x48\x83\xEC\x08'                                                  # SUB    RSP,0x8
# code += b'\x0F\x05'                                                          # SYSCALL
# code += b'\x48\x83\xC4\x50'                                                  # ADD    RSP,0x50
# code += b'\x48\x83\xEC\x20'                                                  # SUB    RSP,0x20
# code += b'\x4C\x8B\x15\x62\x00\x00\x00'                                      # MOV    R10,QWORD PTR [RIP+0x62]    # 0x130
# code += b'\x48\xC7\xC0\x0F\x00\x00\x00'                                      # MOV    RAX,0xF
# code += b'\x48\x83\xEC\x08'                                                  # SUB    RSP,0x8
# code += b'\x0F\x05'                                                          # SYSCALL
# code += b'\x48\x83\xC4\x28'                                                  # ADD    RSP,0x28
# code += b'\xC3'                                                              # RET
# code += b''                                                                  # PADDING
# code += b'\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x0E0
# code += b'\x30\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x0F0
# code += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x100
# code += b'\x16\x00\x18\x00\x00\x00\x00\x00\x58\x30\x00\x00\x00\x00\x00\x00'  # 0x110
# code += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x120
# code += b'\x00\x00\x00\x00\x00\x00\x00\x00\x5C\x00\x3F\x00\x3F\x00\x5C\x00'  # 0x130
# code += b'\x43\x00\x4F\x00\x4E\x00\x4F\x00\x55\x00\x54\x00\x24\x00\x00\x00'  # 0x140
# string = b'Hello world from python\n'
# string_len = len(string)
# chunks = [string[x: x + 8] for x in range(0, len(string), 8)]
# uint64_array = [int.from_bytes(chunk, 'little') for chunk in chunks]
# uint64_array = [ctypes.c_uint64(x) for x in uint64_array]
# func = WindowsRunner(code, ctypes.c_uint64, ctypes.c_uint64)
# func(string_len, *uint64_array)


# return_stack_by_index.asm
# code = b''
# code += b'\x48\x8B\x04\xCC'                                                  # MOV    RAX,QWORD PTR [RSP+RCX*8]
# code += b'\xC3'                                                              # RET
# func =  WindowsRunner(code, ctypes.c_uint64, ctypes.c_uint64)
# result = func(3, 1001, 1002, 1003, 1004)
# print(f'result: {result}')


# add_two_numbers.asm
# code = b''
# code += b'\x48\x8B\xC1'                                                      # MOV    RAX,RCX
# code += b'\x48\x03\xC2'                                                      # ADD    RAX,RDX
# code += b'\xC3'                                                              # RET
# func = WindowsRunner(code, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64)
# result = func(10, 20)
# print(f'result: {result}')


# add_4array_int32.asm
# code = b''
# code += b'\x8B\x01'                                                          # MOV    EAX,DWORD PTR [RCX]
# code += b'\x03\x41\x04'                                                      # ADD    EAX,DWORD PTR [RCX+0x4]
# code += b'\x03\x41\x08'                                                      # ADD    EAX,DWORD PTR [RCX+0x8]
# code += b'\x03\x41\x0C'                                                      # ADD    EAX,DWORD PTR [RCX+0xC]
# code += b'\xC3'                                                              # RET
# arr = np.array([2000, 100, 30, 7], dtype=np.int32)
# func = WindowsRunner(code, ctypes.c_int32, ctypes.c_void_p)
# result = func(arr.ctypes)
# print(f'result: {result}')


# add_4array_int32_SIMD.asm
# code = b''
# code += b'\x0F\x10\x01'                                                      # MOVUPS XMM0,XMMWORD PTR [RCX]
# code += b'\x66\x0F\x38\x02\xC0'                                              # PHADDD XMM0,XMM0
# code += b'\x66\x0F\x38\x02\xC0'                                              # PHADDD XMM0,XMM0
# code += b'\x66\x0F\x7E\xC0'                                                  # MOVD   EAX,XMM0
# code += b'\xC3'                                                              # RET
# arr = np.array([2000, 100, 30, 7], dtype=np.int32)
# func = WindowsRunner(code, ctypes.c_int32, ctypes.c_void_p)
# result = func(arr.ctypes)
# print(f'result: {result}')

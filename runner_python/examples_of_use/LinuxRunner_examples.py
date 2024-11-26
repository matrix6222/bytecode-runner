from runner_python.LinuxRunner import LinuxRunner
import ctypes
import numpy as np


# print_msg_in_code.asm
# code = b''
# code += b'\xB8\x01\x00\x00\x00'              # MOV EAX,0x1
# code += b'\xBF\x01\x00\x00\x00'              # MOV EDI,0x1
# code += b'\x48\x8D\x35\x08\x00\x00\x00'      # LEA RSI,[RIP+0x8] # 19 <msg>
# code += b'\xBA\x0D\x00\x00\x00'              # MOV EDX,0xD
# code += b'\x0F\x05'                          # SYSCALL
# code += b'\xC3'                              # RET
# code += b'\x48\x65\x6C\x6C\x6F\x20\x77\x6F'  # H e l l o   w o
# code += b'\x72\x6C\x64\x21\x0A\x00'          # r l d ! . .
# func = LinuxRunner(code)
# func()


# print_msg_in_code_exit.asm
# code = b''
# code += b'\xB8\x01\x00\x00\x00'              # MOV EAX,0x1
# code += b'\xBF\x01\x00\x00\x00'              # MOV EDI,0x1
# code += b'\x48\x8D\x35\x13\x00\x00\x00'      # LEA RSI,[RIP+0x13] # 24 <msg>
# code += b'\xBA\x0D\x00\x00\x00'              # MOV EDX,0xD
# code += b'\x0F\x05'                          # SYSCALL
# code += b'\xB8\x3C\x00\x00\x00'              # MOV EAX,0x3C
# code += b'\xBF\x00\x00\x00\x00'              # MOV EDI,0x0
# code += b'\x0F\x05'                          # SYSCALL
# code += b'\x48\x65\x6C\x6C\x6F\x20\x77\x6F'  # H e l l o   w o
# code += b'\x72\x6C\x64\x21\x0A\x00'          # r l d ! . .
# func = LinuxRunner(code)
# func()
# exit() causes an infinite loop


# print_msg_in_data.asm
# code = b''
# code += b'\xB8\x01\x00\x00\x00'              # MOV EAX,0x1
# code += b'\xBF\x01\x00\x00\x00'              # MOV EDI,0x1
# code += b'\x48\x8D\x35\x08\x00\x00\x00'      # LEA RSI,[RIP+0x8] # 0x19 <msg>
# code += b'\xBA\x0D\x00\x00\x00'              # MOV EDX,0xD
# code += b'\x0F\x05'                          # SYSCALL
# code += b'\xC3'                              # RET
# code += b'\x48\x65\x6C\x6C\x6F\x20\x77\x6F'  # H e l l o   w o
# code += b'\x72\x6C\x64\x21\x0A\x00'          # r l d ! . .
# func = LinuxRunner(code)
# func()


# add_two_numbers.asm
# code = b''
# code += b'\x48\x89\xF8'                      # MOV RAX,RDI
# code += b'\x48\x01\xF0'                      # ADD RAX,RSI
# code += b'\xC3'                              # RET
# func = LinuxRunner(code, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64)
# result = func(10, 20)
# print(f'result: {result}')


# print_by_args.asm
# code = b''
# code += b'\x48\x89\xFA'                      # MOV RDX,RDI
# code += b'\xBF\x01\x00\x00\x00'              # MOV EDI,0x1
# code += b'\xB8\x01\x00\x00\x00'              # MOV EAX,0x1
# code += b'\x0F\x05'                          # SYSCALL
# code += b'\xC3'                              # RET
# string = b'Hello world from python\n'
# string_len = len(string)
# func = LinuxRunner(code, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_char_p)
# func(string_len, string)


# print_by_stack.asm
# code = b''
# code += b'\x48\x89\xFA'                      # MOV RDX,RDI
# code += b'\x48\x8D\x74\x24\x08'              # LEA RSI,[RSP+0x8]
# code += b'\xBF\x01\x00\x00\x00'              # MOV EDI,0x1
# code += b'\xB8\x01\x00\x00\x00'              # MOV EAX,0x1
# code += b'\x0F\x05'                          # SYSCALL
# code += b'\xC3'                              # RET
# string = b'Hello world from python\n'
# string_len = len(string)
# chunks = [string[x: x + 8] for x in range(0, len(string), 8)]
# uint64_array = [int.from_bytes(chunk, 'little') for chunk in chunks]
# uint64_array = [ctypes.c_uint64(x) for x in uint64_array]
# func = LinuxRunner(code)
# func(ctypes.c_uint64(string_len), ctypes.c_uint64(0), ctypes.c_uint64(0), ctypes.c_uint64(0), ctypes.c_uint64(0), ctypes.c_uint64(0), *uint64_array)


# return_stack_by_index.asm
# code = b''
# code += b'\x48\x8B\x04\xFC'                  # MOV RAX,QWORD PTR [RSP+RDI*8]
# code += b'\xC3'                              # RET
# uint64_array = [ctypes.c_uint64(x) for x in [1001, 1002, 1003]]
# func = LinuxRunner(code, ctypes.c_uint64)
# result = func(1, ctypes.c_uint64(0), ctypes.c_uint64(0), ctypes.c_uint64(0), ctypes.c_uint64(0), ctypes.c_uint64(0), *uint64_array)
# print(f'result: {result}')


# add_4array_int32.asm
# code = b''
# code += b'\x8B\x07'                          # MOV EAX,DWORD PTR [RDI]
# code += b'\x03\x47\x04'                      # ADD EAX,DWORD PTR [RDI+0x4]
# code += b'\x03\x47\x08'                      # ADD EAX,DWORD PTR [RDI+0x8]
# code += b'\x03\x47\x0C'                      # ADD EAX,DWORD PTR [RDI+0xC]
# code += b'\xC3'                              # RET
# arr = np.array([2000, 100, 30, 7], dtype=np.int32)
# func = LinuxRunner(code, ctypes.c_int32, ctypes.c_void_p)
# result = func(arr.ctypes)
# print(f'result: {result}')


# add_4array_int32_SIMD.asm
# code = b''
# code += b'\x0F\x10\x07'                      # MOVUPS XMM0,XMMWORD PTR [RDI]
# code += b'\x66\x0F\x38\x02\xC0'              # PHADDD XMM0,XMM0
# code += b'\x66\x0F\x38\x02\xC0'              # PHADDD XMM0,XMM0
# code += b'\x66\x0F\x7E\xC0'                  # MOVD EAX,XMM0
# code += b'\xC3'                              # RET
# arr = np.array([2000, 100, 30, 7], dtype=np.int32)
# func = LinuxRunner(code, ctypes.c_int32, ctypes.c_void_p)
# result = func(arr.ctypes)
# print(f'result: {result}')

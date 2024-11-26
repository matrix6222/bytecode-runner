from runner_python.MacOSRunner import MacOSRunner
import numpy as np
import ctypes


# print_adr.asm / print_adr_autolen.asm
# code = b''
# code += b'\x20\x00\x80\xD2'  # MOV X0, #1
# code += b'\xA1\x00\x00\x10'  # ADR X1, #20
# code += b'\xA2\x01\x80\xD2'  # MOV X2, #13
# code += b'\x90\x00\x80\xD2'  # MOV X16, #4
# code += b'\xE1\xFF\x1F\xD4'  # SVC #0xFFFF
# code += b'\xC0\x03\x5F\xD6'  # RET
# code += b'\x48\x65\x6C\x6C'  # H e l l
# code += b'\x6F\x20\x77\x6F'  # o   w o
# code += b'\x72\x6C\x64\x21'  # r l d !
# code += b'\x0A'              # .
# func = MacOSRunner(code)
# func()


# print_adrp.asm / print_adrp_autolen.asm
# code = b''
# code += b'\x20\x00\x80\xD2'  # MOV X0, #1
# code += b'\x01\x00\x00\x90'  # ADRP X1, 0x0 <LTMP0+0x4>
# code += b'\x21\x70\x00\x91'  # ADD X1, X1, #28
# code += b'\xA2\x01\x80\xD2'  # MOV X2, #13
# code += b'\x90\x00\x80\xD2'  # MOV X16, #4
# code += b'\x01\x00\x00\xD4'  # SVC #0
# code += b'\xC0\x03\x5F\xD6'  # RET
# code += b'\x48\x65\x6C\x6C'  # H e l l
# code += b'\x6F\x20\x77\x6F'  # o   w o
# code += b'\x72\x6C\x64\x21'  # r l d !
# code += b'\x0A'              # .
# func = MacOSRunner(code)
# func()


# print_by_args.asm
# code = b''
# code += b'\xE2\x03\x00\xAA'  # MOV X2, X0
# code += b'\x20\x00\x80\xD2'  # MOV X0, #1
# code += b'\x90\x00\x80\xD2'  # MOV X16, #4
# code += b'\xE1\xFF\x1F\xD4'  # SVC #0xFFFF
# code += b'\xC0\x03\x5F\xD6'  # RET
# string = b'Hello world from python\n'
# string_len = len(string)
# func = MacOSRunner(code, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_char_p)
# func(string_len, string)


# print_by_stack.asm
# code = b''
# code += b'\xE2\x03\x00\xAA'  # MOV X2, X0
# code += b'\x20\x00\x80\xD2'  # MOV X0, #1
# code += b'\xE1\x03\x00\x91'  # MOV X1, SP
# code += b'\x90\x00\x80\xD2'  # MOV X16, #4
# code += b'\xE1\xFF\x1F\xD4'  # SVC #0xFFFF
# code += b'\xC0\x03\x5F\xD6'  # RET
# string = b'Hello world from python\n'
# string_len = len(string)
# chunks = [string[x: x + 8] for x in range(0, len(string), 8)]
# uint64_array = [int.from_bytes(chunk, 'little') for chunk in chunks]
# uint64_array = [ctypes.c_uint64(x) for x in uint64_array]
# func = MacOSRunner(code, ctypes.c_uint64, ctypes.c_uint64)
# func(string_len, *uint64_array)


# add_two_numbers.asm
# code = b''
# code += b'\x00\x00\x01\x8B'  # ADD X0, X0, X1
# code += b'\xC0\x03\x5F\xD6'  # RET
# func = MacOSRunner(code, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64)
# result = func(10, 20)
# print(f'result: {result}')


# add_4array_int32.asm
# code = b''
# code += b'\x01\x08\xC1\x28'  # LDP W1, W2, [X0], #8
# code += b'\x03\x10\x40\x29'  # LDP W3, W4, [X0]
# code += b'\x20\x00\x02\x0B'  # ADD W0, W1, W2
# code += b'\x00\x00\x03\x0B'  # ADD W0, W0, W3
# code += b'\x00\x00\x04\x0B'  # ADD W0, W0, W4
# code += b'\xC0\x03\x5F\xD6'  # RET
# arr = np.array([2000, 100, 30, 7], dtype=np.int32)
# func = MacOSRunner(code, ctypes.c_int32, ctypes.c_void_p)
# result = func(arr.ctypes)
# print(f'result: {result}')


# add_4array_int32_SIMD.asm
# code = b''
# code += b'\x00\x78\x40\x4C'  # LD1.4S { V0 }, [X0]
# code += b'\x00\xB8\xB1\x4E'  # ADDV.4S S0, V0
# code += b'\x00\x3C\x04\x0E'  # MOV.S W0, V0[0]
# code += b'\xC0\x03\x5F\xD6'  # RET
# arr = np.array([2000, 100, 30, 7], dtype=np.int32)
# func = MacOSRunner(code, ctypes.c_int32, ctypes.c_void_p)
# result = func(arr.ctypes)
# print(f'result: {result}')


# return_stack_by_index.asm
# code = b''
# code += b'\xE0\x7B\x60\xF8'  # LDR X0, [SP, X0, LSL #3]
# code += b'\xC0\x03\x5F\xD6'  # RET
# func = MacOSRunner(code, ctypes.c_uint64, ctypes.c_uint64)
# result = func(2, 1001, 1002, 1003, 1004)
# print(f'result: {result}')


# allocate_RW_page.asm
# code = b''
# code += b'\x00\x00\x80\xD2'  # MOV X0, #0
# code += b'\x01\x00\x88\xD2'  # MOV X1, #16384
# code += b'\x62\x00\x80\xD2'  # MOV X2, #3
# code += b'\x43\x00\x82\xD2'  # MOV X3, #4098
# code += b'\x04\x00\x80\x92'  # MOV X4, #-1
# code += b'\x05\x00\x80\xD2'  # MOV X5, #0
# code += b'\xB0\x18\x80\xD2'  # MOV X16, #197
# code += b'\xE1\xFF\x1F\xD4'  # SVC #0xFFFF
# code += b'\xE7\x03\x00\xAA'  # MOV X7, X0
# code += b'\xE0\x08\xE9\xF2'  # MOVK X0, #18503, LSL #48
# code += b'\xA0\xC8\xC8\xF2'  # MOVK X0, #17989, LSL #32
# code += b'\x60\x88\xA8\xF2'  # MOVK X0, #17475, LSL #16
# code += b'\x20\x48\x88\xF2'  # MOVK X0, #16961
# code += b'\xE0\x00\x00\xF9'  # STR X0, [X7]
# code += b'\x20\x00\x80\xD2'  # MOV X0, #1
# code += b'\xE1\x03\x07\xAA'  # MOV X1, X7
# code += b'\x02\x01\x80\xD2'  # MOV X2, #8
# code += b'\x90\x00\x80\xD2'  # MOV X16, #4
# code += b'\xE1\xFF\x1F\xD4'  # SVC #0xFFFF
# code += b'\xE0\x03\x07\xAA'  # MOV X0, X7
# code += b'\x01\x00\x88\xD2'  # MOV X1, #16384
# code += b'\x30\x09\x80\xD2'  # MOV X16, #73
# code += b'\xE1\xFF\x1F\xD4'  # SVC #0xFFFF
# code += b'\xC0\x03\x5F\xD6'  # RET
# func = MacOSRunner(code)
# func()

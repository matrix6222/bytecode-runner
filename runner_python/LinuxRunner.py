import ctypes


class LinuxRunner:
    def __init__(self, code, res_type=ctypes.c_int64, *arg_types):
        self._libc = ctypes.CDLL(None)
        self._PROT_READ = 1
        self._PROT_WRITE = 2
        self._PROT_EXEC = 4
        self._ptr = self._libc.valloc(len(code))
        if not self._ptr:
            raise MemoryError("Unable to allocate memory")
        if self._libc.mprotect(self._ptr, len(code), self._PROT_READ | self._PROT_WRITE | self._PROT_EXEC) != 0:
            raise PermissionError("Unable to set memory as executable")
        ctypes.memmove(self._ptr, code, len(code))
        func_type = ctypes.CFUNCTYPE(res_type, *arg_types)
        self._func_ptr = func_type(self._ptr)

    def __call__(self, *args):
        return self._func_ptr(*args)

    def __del__(self):
        self._libc.free(self._ptr)

    @staticmethod
    def show_regs_x86_64(ret_type, arg_types, args, all_reg=False, stack_len=16):
        codes = []
        if all_reg:
            codes.append({'name': 'RAX', 'code': b'\x48\x89\xC0\xC3'})  # MOV RAX, RAX; RET
            codes.append({'name': 'RBX', 'code': b'\x48\x89\xD8\xC3'})  # MOV RAX, RBX; RET
            codes.append({'name': 'RCX', 'code': b'\x48\x89\xC8\xC3'})  # MOV RAX, RCX; RET
            codes.append({'name': 'RDX', 'code': b'\x48\x89\xD0\xC3'})  # MOV RAX, RDX; RET
            codes.append({'name': 'RSI', 'code': b'\x48\x89\xF0\xC3'})  # MOV RAX, RSI; RET
            codes.append({'name': 'RDI', 'code': b'\x48\x89\xF8\xC3'})  # MOV RAX, RDI; RET
            codes.append({'name': 'RSP', 'code': b'\x48\x89\xE0\xC3'})  # MOV RAX, RSP; RET
            codes.append({'name': 'RBP', 'code': b'\x48\x89\xE8\xC3'})  # MOV RAX, RBP; RET
            codes.append({'name': 'R8', 'code': b'\x4C\x89\xC0\xC3'})  # MOV RAX, R8; RET
            codes.append({'name': 'R9', 'code': b'\x4C\x89\xC8\xC3'})  # MOV RAX, R9; RET
            codes.append({'name': 'R10', 'code': b'\x4C\x89\xD0\xC3'})  # MOV RAX, R10; RET
            codes.append({'name': 'R11', 'code': b'\x4C\x89\xD8\xC3'})  # MOV RAX, R11; RET
            codes.append({'name': 'R12', 'code': b'\x4C\x89\xE0\xC3'})  # MOV RAX, R12; RET
            codes.append({'name': 'R13', 'code': b'\x4C\x89\xE8\xC3'})  # MOV RAX, R13; RET
            codes.append({'name': 'R14', 'code': b'\x4C\x89\xF0\xC3'})  # MOV RAX, R14; RET
            codes.append({'name': 'R15', 'code': b'\x4C\x89\xF8\xC3'})  # MOV RAX, R15; RET
        else:
            codes.append({'name': 'RDI', 'code': b'\x48\x89\xF8\xC3'})  # MOV RAX, RDI; RET
            codes.append({'name': 'RSI', 'code': b'\x48\x89\xF0\xC3'})  # MOV RAX, RSI; RET
            codes.append({'name': 'RDX', 'code': b'\x48\x89\xD0\xC3'})  # MOV RAX, RDX; RET
            codes.append({'name': 'RCX', 'code': b'\x48\x89\xC8\xC3'})  # MOV RAX, RCX; RET
            codes.append({'name': 'R8', 'code': b'\x4C\x89\xC0\xC3'})  # MOV RAX, R8; RET
            codes.append({'name': 'R9', 'code': b'\x4C\x89\xC8\xC3'})  # MOV RAX, R9; RET
        for x in range(stack_len):
            offset = x * 8
            if offset == 0:
                temp = {'name': 'RSP + 0x00', 'code': b'\x48\x8B\x04\x24\xC3'}  # MOV RAX, [RSP + 0x00]; RET
                codes.append(temp)
            elif 0 < offset < 128:
                b = offset.to_bytes(1, 'little')
                a = '0x' + format(offset, '02X').upper()
                temp = {'name': f'RSP + {a}', 'code': b'\x48\x8B\x44\x24' + b + b'\xC3'}  # MOV RAX, [RSP + 0xXX]; RET
                codes.append(temp)
            elif 128 <= offset < 2147483648:
                b = offset.to_bytes(4, 'little')
                a = '0x' + format(offset, '08X').upper()
                temp = {'name': f'RSP + {a}',
                        'code': b'\x48\x8B\x84\x24' + b + b'\xC3'}  # MOV RAX, [RSP + 0xXXXXXXXX]; RET
                codes.append(temp)
        for code_entry in codes:
            name = code_entry['name']
            code = code_entry['code']
            func = LinuxRunner(code, ret_type, *arg_types)
            print(f'{name}: {func(*args)}')

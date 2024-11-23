import ctypes


class WindowsRunner:
	def __init__(self, code, res_type=ctypes.c_int64, *arg_types):
		virtual_alloc = ctypes.windll.kernel32.VirtualAlloc
		virtual_alloc.restype = ctypes.c_void_p

		page_execute_readwrite = 0x40
		mem_commit = 0x1000
		mem_reserve = 0x2000
		self._ptr = virtual_alloc(None, len(code), mem_commit | mem_reserve, page_execute_readwrite)
		if not self._ptr:
			raise MemoryError("Unable to allocate executable memory")
		ctypes.memmove(self._ptr, code, len(code))

		func_type = ctypes.CFUNCTYPE(res_type, *arg_types)
		self._func_ptr = func_type(self._ptr)

	def __call__(self, *args):
		return self._func_ptr(*args)

	def __del__(self):
		virtual_free = ctypes.windll.kernel32.VirtualFree
		virtual_free.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint]
		virtual_free.restype = ctypes.c_bool

		mem_release = 0x8000
		if not virtual_free(self._ptr, 0, mem_release):
			raise MemoryError("Unable to free allocated memory")

	@staticmethod
	def show_regs_x86_64(ret_type, arg_types, args, all_reg=False, stack_len=16):
		codes = []
		if all_reg:
			codes.append({'name': 'RAX', 'code': b'\x48\x8B\xC0\xC3'})  # MOV RAX, RAX; RET
			codes.append({'name': 'RBX', 'code': b'\x48\x8B\xC3\xC3'})  # MOV RAX, RBX; RET
			codes.append({'name': 'RCX', 'code': b'\x48\x8B\xC1\xC3'})  # MOV RAX, RCX; RET
			codes.append({'name': 'RDX', 'code': b'\x48\x8B\xC2\xC3'})  # MOV RAX, RDX; RET
			codes.append({'name': 'RSI', 'code': b'\x48\x8B\xC6\xC3'})  # MOV RAX, RSI; RET
			codes.append({'name': 'RDI', 'code': b'\x48\x8B\xC7\xC3'})  # MOV RAX, RDI; RET
			codes.append({'name': 'RSP', 'code': b'\x48\x8B\xC4\xC3'})  # MOV RAX, RSP; RET
			codes.append({'name': 'RBP', 'code': b'\x48\x8B\xC5\xC3'})  # MOV RAX, RBP; RET
			codes.append({'name': 'R8', 'code': b'\x49\x8B\xC0\xC3'})  # MOV RAX, R8; RET
			codes.append({'name': 'R9', 'code': b'\x49\x8B\xC1\xC3'})  # MOV RAX, R9; RET
			codes.append({'name': 'R10', 'code': b'\x49\x8B\xC2\xC3'})  # MOV RAX, R10; RET
			codes.append({'name': 'R11', 'code': b'\x49\x8B\xC3\xC3'})  # MOV RAX, R11; RET
			codes.append({'name': 'R12', 'code': b'\x49\x8B\xC4\xC3'})  # MOV RAX, R12; RET
			codes.append({'name': 'R13', 'code': b'\x49\x8B\xC5\xC3'})  # MOV RAX, R13; RET
			codes.append({'name': 'R14', 'code': b'\x49\x8B\xC6\xC3'})  # MOV RAX, R14; RET
			codes.append({'name': 'R15', 'code': b'\x49\x8B\xC7\xC3'})  # MOV RAX, R15; RET
		else:
			codes.append({'name': 'RCX', 'code': b'\x48\x8B\xC1\xC3'})  # MOV RAX, RCX; RET
			codes.append({'name': 'RDX', 'code': b'\x48\x8B\xC2\xC3'})  # MOV RAX, RDX; RET
			codes.append({'name': 'R8', 'code': b'\x49\x8B\xC0\xC3'})  # MOV RAX, R8; RET
			codes.append({'name': 'R9', 'code': b'\x49\x8B\xC1\xC3'})  # MOV RAX, R9; RET
		for x in range(stack_len):
			offset = x * 8
			if offset == 0:
				temp = {'name': 'RSP + 0x00', 'code': b'\x48\x8B\x04\x24\xC3'}  # MOV RAX, QWORD PTR [RSP + 0x00]; RET
				codes.append(temp)
			elif 0 < offset < 128:
				addr_bytes = offset.to_bytes(1, 'little')
				addr_str = '0x' + format(offset, '02X').upper()
				temp = {'name': f'RSP + {addr_str}', 'code': b'\x48\x8B\x44\x24' + addr_bytes + b'\xC3'}  # MOV RAX, QWORD PTR [RSP + 0xXX]; RET
				codes.append(temp)
			elif 128 <= offset < 2147483648:
				addr_bytes = offset.to_bytes(4, 'little')
				addr_str = '0x' + format(offset, '08X').upper()
				temp = {'name': f'RSP + {addr_str}', 'code': b'\x48\x8B\x84\x24' + addr_bytes + b'\xC3'}  # MOV RAX, QWORD PTR [RSP + 0xXXXXXXXX]; RET
				codes.append(temp)
		for code_entry in codes:
			name = code_entry['name']
			code = code_entry['code']
			func = WindowsRunner(code, ret_type, *arg_types)
			print(f'{name}: {func(*args)}')

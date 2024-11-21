import ctypes
import os


class MacOSRunner:
	def __init__(self, code, res_type=ctypes.c_int64, *arg_types):
		page_size = os.sysconf('SC_PAGESIZE')
		self._alloc_size = (len(code) + page_size - 1) & ~(page_size - 1)
		self._PROT_READ = 1
		self._PROT_WRITE = 2
		self._PROT_EXEC = 4
		self._libc = ctypes.CDLL(None)
		self._ptr = ctypes.c_void_p()
		if self._libc.posix_memalign(ctypes.byref(self._ptr), page_size, self._alloc_size) != 0:
			raise MemoryError("Unable to allocate memory")
		ctypes.memmove(self._ptr, code, len(code))
		if self._libc.mprotect(self._ptr, self._alloc_size, self._PROT_EXEC) != 0:
			raise PermissionError("Unable to set memory protection to EXEC")
		func_type = ctypes.CFUNCTYPE(res_type, *arg_types)
		self._func_ptr = func_type(self._ptr.value)

	def __call__(self, *args):
		return self._func_ptr(*args)

	def __del__(self):
		if self._libc.mprotect(self._ptr, self._alloc_size, self._PROT_WRITE) != 0:
			raise PermissionError("Unable to set memory protection to WRITE")
		self._libc.free(self._ptr)

	@staticmethod
	def show_regs_arm64(ret_type, arg_types, args, all_reg=False, stack_len=16):
		codes = []
		if all_reg:
			codes.append({'name': 'X0', 'code': b'\xE0\x03\x00\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X0; RET
			codes.append({'name': 'X1', 'code': b'\xE0\x03\x01\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X1; RET
			codes.append({'name': 'X2', 'code': b'\xE0\x03\x02\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X2; RET
			codes.append({'name': 'X3', 'code': b'\xE0\x03\x03\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X3; RET
			codes.append({'name': 'X4', 'code': b'\xE0\x03\x04\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X4; RET
			codes.append({'name': 'X5', 'code': b'\xE0\x03\x05\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X5; RET
			codes.append({'name': 'X6', 'code': b'\xE0\x03\x06\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X6; RET
			codes.append({'name': 'X7', 'code': b'\xE0\x03\x07\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X7; RET
			codes.append({'name': 'X8', 'code': b'\xE0\x03\x08\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X8; RET
			codes.append({'name': 'X9', 'code': b'\xE0\x03\x09\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X9; RET
			codes.append({'name': 'X10', 'code': b'\xE0\x03\x0A\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X10; RET
			codes.append({'name': 'X11', 'code': b'\xE0\x03\x0B\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X11; RET
			codes.append({'name': 'X12', 'code': b'\xE0\x03\x0C\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X12; RET
			codes.append({'name': 'X13', 'code': b'\xE0\x03\x0D\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X13; RET
			codes.append({'name': 'X14', 'code': b'\xE0\x03\x0E\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X14; RET
			codes.append({'name': 'X15', 'code': b'\xE0\x03\x0F\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X15; RET
			codes.append({'name': 'X16', 'code': b'\xE0\x03\x10\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X16; RET
			codes.append({'name': 'X17', 'code': b'\xE0\x03\x11\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X17; RET
			codes.append({'name': 'X18', 'code': b'\xE0\x03\x12\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X18; RET
			codes.append({'name': 'X19', 'code': b'\xE0\x03\x13\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X19; RET
			codes.append({'name': 'X20', 'code': b'\xE0\x03\x14\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X20; RET
			codes.append({'name': 'X21', 'code': b'\xE0\x03\x15\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X21; RET
			codes.append({'name': 'X22', 'code': b'\xE0\x03\x16\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X22; RET
			codes.append({'name': 'X23', 'code': b'\xE0\x03\x17\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X23; RET
			codes.append({'name': 'X24', 'code': b'\xE0\x03\x18\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X24; RET
			codes.append({'name': 'X25', 'code': b'\xE0\x03\x19\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X25; RET
			codes.append({'name': 'X26', 'code': b'\xE0\x03\x1A\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X26; RET
			codes.append({'name': 'X27', 'code': b'\xE0\x03\x1B\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X27; RET
			codes.append({'name': 'X28', 'code': b'\xE0\x03\x1C\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X28; RET
			codes.append({'name': 'X29', 'code': b'\xE0\x03\x1D\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X29; RET
			codes.append({'name': 'X30', 'code': b'\xE0\x03\x1E\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X30; RET
			codes.append({'name': 'XZR', 'code': b'\xE0\x03\x1F\xAA\xC0\x03\x5F\xD6'})  # MOV X0, XZR; RET
		else:
			codes.append({'name': 'X0', 'code': b'\xE0\x03\x00\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X0; RET
			codes.append({'name': 'X1', 'code': b'\xE0\x03\x01\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X1; RET
			codes.append({'name': 'X2', 'code': b'\xE0\x03\x02\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X2; RET
			codes.append({'name': 'X3', 'code': b'\xE0\x03\x03\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X3; RET
			codes.append({'name': 'X4', 'code': b'\xE0\x03\x04\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X4; RET
			codes.append({'name': 'X5', 'code': b'\xE0\x03\x05\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X5; RET
			codes.append({'name': 'X6', 'code': b'\xE0\x03\x06\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X6; RET
			codes.append({'name': 'X7', 'code': b'\xE0\x03\x07\xAA\xC0\x03\x5F\xD6'})  # MOV X0, X7; RET
		for x in range(stack_len):
			offset = x * 8
			if offset == 0:
				temp = {'name': 'SP + 0x00', 'code': b'\xE0\x03\x40\xF9\xC0\x03\x5F\xD6'}  # LDR X0, [SP]; RET
				codes.append(temp)
			elif 0 < offset < 4096:
				addr_str = '0x' + format(offset, '04X').upper()
				if offset < 256:
					addr_str = '0x' + format(offset, '02X').upper()
				temp = {'name': f'SP + {addr_str}', 'code': b'\xE0' + ((offset << 2) + 3).to_bytes(2, 'little') + b'\x91\x00\x00\x40\xF9\xC0\x03\x5F\xD6'}  # ADD X0, SP, #0xXX; LDR X0, [X0]; RET
				codes.append(temp)
		for code_entry in codes:
			name = code_entry['name']
			code = code_entry['code']
			func = MacOSRunner(code, ret_type, *arg_types)
			print(f'{name}: {func(*args)}')

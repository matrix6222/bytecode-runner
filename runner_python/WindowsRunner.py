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

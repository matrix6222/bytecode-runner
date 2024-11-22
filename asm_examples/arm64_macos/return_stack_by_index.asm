.align 4

// uint64 return_stack(uint64 index, ...);
return_stack:
	LDR X0, [SP, X0, LSL #3]
	RET


; code = b''
; code += b'\xE0\x7B\x60\xF8'  # LDR X0, [SP, X0, LSL #3]
; code += b'\xC0\x03\x5F\xD6'  # RET

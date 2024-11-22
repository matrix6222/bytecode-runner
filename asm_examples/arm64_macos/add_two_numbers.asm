.align 4

// uint64 add(uint64 a, uint64 b);
add:
	ADD X0, X0, X1
	RET


; code = b''
; code += b'\x00\x00\x01\x8B'  # ADD X0, X0, X1
; code += b'\xC0\x03\x5F\xD6'  # RET

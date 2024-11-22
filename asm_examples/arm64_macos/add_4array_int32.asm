.align 4

// int32 add4(int32* arr_ptr);
add4:
	LDP W1, W2, [X0], #8
	LDP W3, W4, [X0]
	ADD W0, W1, W2
	ADD W0, W0, W3
	ADD W0, W0, W4
	RET


; code = b''
; code += b'\x01\x08\xC1\x28'  # LDP W1, W2, [X0], #8
; code += b'\x03\x10\x40\x29'  # LDP W3, W4, [X0]
; code += b'\x20\x00\x02\x0B'  # ADD W0, W1, W2
; code += b'\x00\x00\x03\x0B'  # ADD W0, W0, W3
; code += b'\x00\x00\x04\x0B'  # ADD W0, W0, W4
; code += b'\xC0\x03\x5F\xD6'  # RET

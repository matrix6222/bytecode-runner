.align 4

// void print(uint64 size, uint8* bytes);
print:
	MOV X2, X0
	MOV X0, #1
	MOV X16, #4
	SVC #0xFFFF

	RET


; code = b''
; code += b'\xE2\x03\x00\xAA'  # MOV X2, X0
; code += b'\x20\x00\x80\xD2'  # MOV X0, #1
; code += b'\x90\x00\x80\xD2'  # MOV X16, #4
; code += b'\xE1\xFF\x1F\xD4'  # SVC #0xFFFF
; code += b'\xC0\x03\x5F\xD6'  # RET

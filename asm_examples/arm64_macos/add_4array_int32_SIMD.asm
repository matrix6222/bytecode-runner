.align 4

// int32 add4_simd(int32* arr_ptr);
add4_simd:
	LD1 {V0.4S}, [X0]
	ADDV S0, V0.4S
	MOV W0, V0.S[0]
	RET


; code = b''
; code += b'\x00\x78\x40\x4C'  # LD1.4S { V0 }, [X0]
; code += b'\x00\xB8\xB1\x4E'  # ADDV.4S S0, V0
; code += b'\x00\x3C\x04\x0E'  # MOV.S W0, V0[0]
; code += b'\xC0\x03\x5F\xD6'  # RET

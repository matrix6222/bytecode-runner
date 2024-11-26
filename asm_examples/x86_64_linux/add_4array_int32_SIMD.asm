DEFAULT REL

SECTION .text
	GLOBAL _start

; int32 add4(int32* arr_ptr);
_start:
    MOVUPS XMM0, [RDI]
    PHADDD XMM0, XMM0
    PHADDD XMM0, XMM0
    MOVD EAX, XMM0

	RET


; code = b''
; code += b'\x0F\x10\x07'                      # MOVUPS XMM0,XMMWORD PTR [RDI]
; code += b'\x66\x0F\x38\x02\xC0'              # PHADDD XMM0,XMM0
; code += b'\x66\x0F\x38\x02\xC0'              # PHADDD XMM0,XMM0
; code += b'\x66\x0F\x7E\xC0'                  # MOVD EAX,XMM0
; code += b'\xC3'                              # RET

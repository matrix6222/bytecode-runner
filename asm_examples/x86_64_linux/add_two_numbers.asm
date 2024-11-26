DEFAULT REL

SECTION .text
	GLOBAL _start

; uint64 add(uint64 a, uint64 b);
_start:
	MOV RAX, RDI
	ADD RAX, RSI
	RET


; code = b''
; code += b'\x48\x89\xF8'  # MOV RAX,RDI
; code += b'\x48\x01\xF0'  # ADD RAX,RSI
; code += b'\xC3'          # RET

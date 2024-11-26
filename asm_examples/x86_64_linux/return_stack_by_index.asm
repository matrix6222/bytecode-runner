DEFAULT REL

SECTION .text
	GLOBAL _start

; uint64 return_stack(uint64 index, ...);
_start:
	MOV RAX, [RSP + RDI * 8]
	RET


; code = b''
; code += b'\x48\x8B\x04\xFC'                  # MOV RAX,QWORD PTR [RSP+RDI*8]
; code += b'\xC3'                              # RET

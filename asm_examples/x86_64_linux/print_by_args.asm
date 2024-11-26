DEFAULT REL

SECTION .text
	GLOBAL _start

; void (uint64 size, uint8* bytes);
_start:
	MOV RDX, RDI
	MOV RDI, 1
	MOV RAX, 1
	SYSCALL

	RET


; code = b''
; code += b'\x48\x89\xFA'                      # MOV RDX,RDI
; code += b'\xBF\x01\x00\x00\x00'              # MOV EDI,0x1
; code += b'\xB8\x01\x00\x00\x00'              # MOV EAX,0x1
; code += b'\x0F\x05'                          # SYSCALL
; code += b'\xC3'                              # RET

DEFAULT REL

SECTION .text
	GLOBAL _start

; void (uint64 size, uint64 arg2, uint64 arg3, uint64 arg4, uint64 arg5, uint64 arg6, ...);
_start:
	MOV RDX, RDI
	LEA RSI, [RSP + 8]
	MOV RDI, 1
	MOV RAX, 1
	SYSCALL

	RET


; code = b''
; code += b'\x48\x89\xFA'                      # MOV RDX,RDI
; code += b'\x48\x8D\x74\x24\x08'              # LEA RSI,[RSP+0x8]
; code += b'\xBF\x01\x00\x00\x00'              # MOV EDI,0x1
; code += b'\xB8\x01\x00\x00\x00'              # MOV EAX,0x1
; code += b'\x0F\x05'                          # SYSCALL
; code += b'\xC3'                              # RET

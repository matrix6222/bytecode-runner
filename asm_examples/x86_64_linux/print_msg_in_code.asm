DEFAULT REL

SECTION .text
	GLOBAL _start

; void print();
_start:
	MOV RAX, 1
	MOV RDI, 1
	LEA RSI, [msg]
	MOV RDX, 13
	SYSCALL

	RET

msg DB "Hello world!", 0x0A, 0x00


; code = b''
; code += b'\xB8\x01\x00\x00\x00'              # MOV EAX,0x1
; code += b'\xBF\x01\x00\x00\x00'              # MOV EDI,0x1
; code += b'\x48\x8D\x35\x08\x00\x00\x00'      # LEA RSI,[RIP+0x8] # 19 <msg>  ; calculated by the compiler
; code += b'\xBA\x0D\x00\x00\x00'              # MOV EDX,0xD
; code += b'\x0F\x05'                          # SYSCALL
; code += b'\xC3'                              # RET
; code += b'\x48\x65\x6C\x6C\x6F\x20\x77\x6F'  # H e l l o   w o
; code += b'\x72\x6C\x64\x21\x0A\x00'          # r l d ! . .

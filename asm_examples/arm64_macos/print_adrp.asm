.global _main
.align 4
.text

_main: ; void print();
	MOV X0, #1
	ADRP X1, msg@PAGE
	ADD X1, X1, msg@PAGEOFF
	MOV X2, 13
	MOV X16, #4
	SVC #0

	RET

.data
	msg: .ascii "Hello world!\n"


; code = b''
; code += b'\x20\x00\x80\xD2'  # MOV X0, #1
; code += b'\x01\x00\x00\x90'  # ADRP X1, 0x0 <LTMP0+0x4> ; compiler provides this instruction
; code += b'\x21\x70\x00\x91'  # ADD X1, X1, #28          ; manually modified shellcode from ADD X1, X1, #0 to ADD X1, X1, #28
; code += b'\xA2\x01\x80\xD2'  # MOV X2, #13
; code += b'\x90\x00\x80\xD2'  # MOV X16, #4
; code += b'\x01\x00\x00\xD4'  # SVC #0
; code += b'\xC0\x03\x5F\xD6'  # RET
; code += b'\x48\x65\x6C\x6C'  # H e l l
; code += b'\x6F\x20\x77\x6F'  # o   w o
; code += b'\x72\x6C\x64\x21'  # r l d !
; code += b'\x0A'              # .

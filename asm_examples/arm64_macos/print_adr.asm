.align 4

print: ; void print();
	MOV X0, #1
	ADR X1, msg
	MOV X2, #13
	MOV X16, #4
	SVC #0xFFFF

	RET

msg: .ascii "Hello world!\n"


; code = b''
; code += b'\x20\x00\x80\xD2'  # MOV X0, #1
; code += b'\xA1\x00\x00\x10'  # ADR X1, #20
; code += b'\xA2\x01\x80\xD2'  # MOV X2, #13
; code += b'\x90\x00\x80\xD2'  # MOV X16, #4
; code += b'\xE1\xFF\x1F\xD4'  # SVC #0xFFFF
; code += b'\xC0\x03\x5F\xD6'  # RET
; code += b'\x48\x65\x6C\x6C'  # H e l l
; code += b'\x6F\x20\x77\x6F'  # o   w o
; code += b'\x72\x6C\x64\x21'  # r l d !
; code += b'\x0A'              # .

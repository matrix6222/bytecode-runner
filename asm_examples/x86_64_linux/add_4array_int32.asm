DEFAULT REL

SECTION .text
	GLOBAL _start

; int32 add4(int32* arr_ptr);
_start:
	MOV EAX, [RDI]
    ADD EAX, [RDI + 4]
    ADD EAX, [RDI + 8]
    ADD EAX, [RDI + 12]

	RET


code = b''
code += b'\x8B\x07'                          # MOV EAX,DWORD PTR [RDI]
code += b'\x03\x47\x04'                      # ADD EAX,DWORD PTR [RDI+0x4]
code += b'\x03\x47\x08'                      # ADD EAX,DWORD PTR [RDI+0x8]
code += b'\x03\x47\x0C'                      # ADD EAX,DWORD PTR [RDI+0xC]
code += b'\xC3'                              # RET

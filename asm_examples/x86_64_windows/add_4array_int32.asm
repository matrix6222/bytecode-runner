.CODE
; int32 add4(int32* arr_ptr);
main PROC
	MOV EAX, DWORD PTR [RCX]
    ADD EAX, DWORD PTR [RCX + 4]
    ADD EAX, DWORD PTR [RCX + 8]
    ADD EAX, DWORD PTR [RCX + 12]

	RET

main ENDP
END


; code = b''
; code += b'\x8B\x01'      # MOV    EAX,DWORD PTR [RCX]
; code += b'\x03\x41\x04'  # ADD    EAX,DWORD PTR [RCX+0x4]
; code += b'\x03\x41\x08'  # ADD    EAX,DWORD PTR [RCX+0x8]
; code += b'\x03\x41\x0C'  # ADD    EAX,DWORD PTR [RCX+0xC]
; code += b'\xC3'          # RET

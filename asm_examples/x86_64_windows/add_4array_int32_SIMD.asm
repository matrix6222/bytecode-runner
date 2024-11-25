.CODE
; int32 add4(int32* arr_ptr);
main PROC
    MOVUPS XMM0, XMMWORD PTR [RCX]
    PHADDD XMM0, XMM0
    PHADDD XMM0, XMM0
    MOVD EAX, XMM0

	RET

main ENDP
END


; code = b''
; code += b'\x0F\x10\x01'          # MOVUPS XMM0,XMMWORD PTR [RCX]
; code += b'\x66\x0F\x38\x02\xC0'  # PHADDD XMM0,XMM0
; code += b'\x66\x0F\x38\x02\xC0'  # PHADDD XMM0,XMM0
; code += b'\x66\x0F\x7E\xC0'      # MOVD   EAX,XMM0
; code += b'\xC3'                  # RET

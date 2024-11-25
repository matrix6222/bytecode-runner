.CODE
; uint64 add(uint64 a, uint64 b);
main PROC
	MOV RAX, RCX
	ADD RAX, RDX

	RET

main ENDP
END


; code = b''
; code += b'\x48\x8B\xC1'  # MOV    RAX,RCX
; code += b'\x48\x03\xC2'  # ADD    RAX,RDX
; code += b'\xC3'          # RET

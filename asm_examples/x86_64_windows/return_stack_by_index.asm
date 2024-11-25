.CODE
; uint64 return_stack(uint64 index, ...);
main PROC
	MOV RAX, QWORD PTR [RSP + RCX * 8]
	RET

main ENDP
END


code = b''
code += b'\x48\x8B\x04\xCC'  # MOV RAX, QWORD PTR [RSP + RCX * 8]
code += b'\xC3'              # RET

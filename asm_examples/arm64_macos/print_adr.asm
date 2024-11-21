.align 4

_main:
	MOV X0, #1
	ADR X1, msg
	MOV X2, #13
	MOV X16, #4
	SVC #0xFFFF

	RET

msg: .ascii "Hello world!\n"
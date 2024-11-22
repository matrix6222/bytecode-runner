.global _main
.align 4
.text

_main: ; void print();
	MOV X0, #1
	ADRP X1, msg@PAGE
	ADD X1, X1, msg@PAGEOFF
	MOV X2, #msg_len
	MOV X16, #4
	SVC #0

	RET

.data
	msg: .ascii "Hello world!\n"
	.equ msg_len, . -msg
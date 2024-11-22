.align 4

// void print(uint64 size, ...);
// Vararg - each argument is always packed onto the stack as an 8-byte number
print:
	MOV X2, X0
	MOV X0, #1
	MOV X1, SP
	MOV X16, #4
	SVC #0xFFFF

	RET


;;;

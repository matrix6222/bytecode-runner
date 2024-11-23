.align 4

_main:
	; allocate RW data section
    MOV X0, #0       ; addr: NULL (let kernel choose the address)
    MOV X1, #16384   ; length: one page (16KB)
    MOV X2, #3       ; PROT_READ | PROT_WRITE (1 | 2 = 3)
    MOV X3, #0x1002  ; MAP_PRIVATE | MAP_ANONYMOUS
    MOV X4, #-1      ; fd: -1 (not backed by a file)
    MOV X5, #0       ; offset: 0
    MOV X16, #197    ; Syscall number for mmap (macOS ARM64)
    SVC #0xFFFF
    MOV X7, X0       ; RW data pointer in X7

	; set X0 to "ABCDEFGH"
    MOVK X0, #0x4847, LSL #48  ; HG
	MOVK X0, #0x4645, LSL #32  ; FE
	MOVK X0, #0x4443, LSL #16  ; DC
	MOVK X0, #0x4241, LSL #00  ; BA

	; save X0 in RW data section
	STR X0, [X7]

    ; print [X7]
	MOV X0, #1
	MOV X1, X7
	MOV X2, #8
	MOV X16, #4
	SVC #0xFFFF

	; free RW data section
	MOV X0, X7      ; addr: ptr
    MOV X1, #16384  ; length: one page (16KB)
    MOV X16, #73    ; Syscall number for munmap (macOS ARM64)
    SVC #0xFFFF

	RET


; code = b''
; code += b'\x00\x00\x80\xD2'  # MOV X0, #0
; code += b'\x01\x00\x88\xD2'  # MOV X1, #16384
; code += b'\x62\x00\x80\xD2'  # MOV X2, #3
; code += b'\x43\x00\x82\xD2'  # MOV X3, #4098
; code += b'\x04\x00\x80\x92'  # MOV X4, #-1
; code += b'\x05\x00\x80\xD2'  # MOV X5, #0
; code += b'\xB0\x18\x80\xD2'  # MOV X16, #197
; code += b'\xE1\xFF\x1F\xD4'  # SVC #0xFFFF
; code += b'\xE7\x03\x00\xAA'  # MOV X7, X0
; code += b'\xE0\x08\xE9\xF2'  # MOVK X0, #18503, LSL #48
; code += b'\xA0\xC8\xC8\xF2'  # MOVK X0, #17989, LSL #32
; code += b'\x60\x88\xA8\xF2'  # MOVK X0, #17475, LSL #16
; code += b'\x20\x48\x88\xF2'  # MOVK X0, #16961
; code += b'\xE0\x00\x00\xF9'  # STR X0, [X7]
; code += b'\x20\x00\x80\xD2'  # MOV X0, #1
; code += b'\xE1\x03\x07\xAA'  # MOV X1, X7
; code += b'\x02\x01\x80\xD2'  # MOV X2, #8
; code += b'\x90\x00\x80\xD2'  # MOV X16, #4
; code += b'\xE1\xFF\x1F\xD4'  # SVC #0xFFFF
; code += b'\xE0\x03\x07\xAA'  # MOV X0, X7
; code += b'\x01\x00\x88\xD2'  # MOV X1, #16384
; code += b'\x30\x09\x80\xD2'  # MOV X16, #73
; code += b'\xE1\xFF\x1F\xD4'  # SVC #0xFFFF
; code += b'\xC0\x03\x5F\xD6'  # RET

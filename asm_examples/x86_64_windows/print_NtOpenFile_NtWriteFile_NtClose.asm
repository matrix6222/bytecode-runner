.DATA

	OBJECT_ATTRIBUTES	DQ 48				; ULONG           Length (size if structure)
						DQ 0				; HANDLE          RootDirectory
						DQ UNICODE_STRING	; PUNICODE_STRING ObjectName
						DQ 0				; ULONG           Attributes
						DQ 0				; PVOID           SecurityDescriptor
						DQ 0				; PVOID           SecurityQualityOfService

	UNICODE_STRING		DW 22				; USHORT Length
						DW 24				; USHORT MaximumLength;
						DD 0				;        Padding
						DQ filename			; PWSTR  Buffer

	IO_STATUS_BLOCK		DQ 0, 0

	hStdOut				DQ 0

	filename			DW '\', '?', '?', '\', 'C', 'O', 'N', 'O', 'U', 'T', '$', 0

	message				DB "Hello world", 0Ah, 0

.CODE
; void print();
main PROC

	; set pointers in data (for shellcode)
	LEA RAX, filename
	LEA RBX, UNICODE_STRING
	MOV [RBX + 8], RAX
	LEA RAX, OBJECT_ATTRIBUTES
	MOV [RAX + 16], RBX

	; NtOpenFile
	SUB RSP, 48
	LEA R10, hStdOut				; [out]          PHANDLE            FileHandle
	MOV RDX, 120116h				; [in]           ACCESS_MASK        DesiredAccess (FILE_GENERIC_WRITE)
	LEA R8, OBJECT_ATTRIBUTES		; [in]           POBJECT_ATTRIBUTES ObjectAttributes
	LEA R9, IO_STATUS_BLOCK			; [out]          PIO_STATUS_BLOCK   IoStatusBlock
	MOV QWORD PTR [rsp + 32], 0		; [in]           ULONG              ShareAccess
	MOV QWORD PTR [rsp + 40], 20h   ; [in]           ULONG              OpenOptions
	MOV RAX, 51  ; Windows 10 x64, 0x0033 NtOpenFile (can be different)
	SUB RSP, 8
	SYSCALL
	ADD RSP, 56

	; NtWriteFile
	SUB RSP, 72
	MOV R10, hStdOut
	MOV RDX, 0
	MOV R8, 0
	MOV R9, 0
	LEA RAX, IO_STATUS_BLOCK
	MOV QWORD PTR [RSP + 32], RAX
	LEA RAX, message
	MOV QWORD PTR [RSP + 40], RAX
	MOV QWORD PTR [RSP + 48], 13
	MOV QWORD PTR [RSP + 56], 0
	MOV QWORD PTR [RSP + 64], 0
	MOV RAX, 8  ; Windows 10 x64, 0x0008 NtWriteFile (can be different)
	SUB RSP, 8
	SYSCALL
	ADD RSP, 80

	; NtClose
	SUB RSP, 32
	MOV R10, hStdOut
	MOV RAX, 15  ; Windows 10 x64, 0x000f NtClose (can be different)
	SUB RSP, 8
	SYSCALL
	ADD RSP, 40

	RET

main ENDP
END


; code = b''
; code += b'\x48\x8D\x05\x39\x01\x00\x00'                                      # LEA    RAX,[RIP+0x139]             # 0x140  ; manually modified offset in shellcode
; code += b'\x48\x8D\x1D\x0A\x01\x00\x00'                                      # LEA    RBX,[RIP+0x10A]             # 0x118  ; manually modified offset in shellcode
; code += b'\x48\x89\x43\x08'                                                  # MOV    QWORD PTR [RBX+0x8],RAX
; code += b'\x48\x8D\x05\xCF\x00\x00\x00'                                      # LEA    RAX,[RIP+0xCF]              # 0xE8   ; manually modified offset in shellcode
; code += b'\x48\x89\x58\x10'                                                  # MOV    QWORD PTR [RAX+0x10],RBX
; code += b'\x48\x83\xEC\x30'                                                  # SUB    RSP,0x30
; code += b'\x4C\x8D\x15\x10\x01\x00\x00'                                      # LEA    R10,[RIP+0x110]             # 0x138  ; manually modified offset in shellcode
; code += b'\x48\xC7\xC2\x16\x01\x12\x00'                                      # MOV    RDX,0x120116
; code += b'\x4C\x8D\x05\xB2\x00\x00\x00'                                      # LEA    R8,[RIP+0xB2]               # 0xE8   ; manually modified offset in shellcode
; code += b'\x4C\x8D\x0D\xEB\x00\x00\x00'                                      # LEA    R9,[RIP+0xEB]               # 0x128  ; manually modified offset in shellcode
; code += b'\x48\xC7\x44\x24\x20\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x20],0x0
; code += b'\x48\xC7\x44\x24\x28\x20\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x28],0x20
; code += b'\x48\xC7\xC0\x33\x00\x00\x00'                                      # MOV    RAX,0x33
; code += b'\x48\x83\xEC\x08'                                                  # SUB    RSP,0x8
; code += b'\x0F\x05'                                                          # SYSCALL
; code += b'\x48\x83\xC4\x38'                                                  # ADD    RSP,0x38
; code += b'\x48\x83\xEC\x48'                                                  # SUB    RSP,0x48
; code += b'\x4C\x8B\x15\xCD\x00\x00\x00'                                      # MOV    R10,QWORD PTR [RIP+0xCD]    # 0x138  ; manually modified offset in shellcode
; code += b'\x48\xC7\xC2\x00\x00\x00\x00'                                      # MOV    RDX,0x0
; code += b'\x49\xC7\xC0\x00\x00\x00\x00'                                      # MOV    R8,0x0
; code += b'\x49\xC7\xC1\x00\x00\x00\x00'                                      # MOV    R9,0x0
; code += b'\x48\x8D\x05\xA1\x00\x00\x00'                                      # LEA    RAX,[RIP+0xA1]              # 0x128  ; manually modified offset in shellcode
; code += b'\x48\x89\x44\x24\x20'                                              # MOV    QWORD PTR [RSP+0x20],RAX
; code += b'\x48\x8D\x05\xC5\x00\x00\x00'                                      # LEA    RAX,[RIP+0xC5]              # 0x158  ; manually modified offset in shellcode
; code += b'\x48\x89\x44\x24\x28'                                              # MOV    QWORD PTR [RSP+0x28],RAX
; code += b'\x48\xC7\x44\x24\x30\x0D\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x30],0xD
; code += b'\x48\xC7\x44\x24\x38\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x38],0x0
; code += b'\x48\xC7\x44\x24\x40\x00\x00\x00\x00'                              # MOV    QWORD PTR [RSP+0x40],0x0
; code += b'\x48\xC7\xC0\x08\x00\x00\x00'                                      # MOV    RAX,0x8
; code += b'\x48\x83\xEC\x08'                                                  # SUB    RSP,0x8
; code += b'\x0F\x05'                                                          # SYSCALL
; code += b'\x48\x83\xC4\x50'                                                  # ADD    RSP,0x50
; code += b'\x48\x83\xEC\x20'                                                  # SUB    RSP,0x20
; code += b'\x4C\x8B\x15\x69\x00\x00\x00'                                      # MOV    R10,QWORD PTR [RIP+0x69]    # 0x138  ; manually modified offset in shellcode
; code += b'\x48\xC7\xC0\x0F\x00\x00\x00'                                      # MOV    RAX,0xF
; code += b'\x48\x83\xEC\x08'                                                  # SUB    RSP,0x8
; code += b'\x0F\x05'                                                          # SYSCALL
; code += b'\x48\x83\xC4\x28'                                                  # ADD    RSP,0x28
; code += b'\xC3'                                                              # RET
; code += b'\x00\x00\x00\x00\x00\x00\x00'                                      # PADDING
; code += b'\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x0E8  0 . . . . . . . . . . . . . . .
; code += b'\x30\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x0F8  0 0 . . . . . . . . . . . . . .
; code += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x108  . . . . . . . . . . . . . . . .
; code += b'\x16\x00\x18\x00\x00\x00\x00\x00\x58\x30\x00\x00\x00\x00\x00\x00'  # 0x118  . . . . . . . . X 0 . . . . . .
; code += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # 0x128  . . . . . . . . . . . . . . . .
; code += b'\x00\x00\x00\x00\x00\x00\x00\x00\x5C\x00\x3F\x00\x3F\x00\x5C\x00'  # 0x138  . . . . . . . . \ . ? . ? . \ .
; code += b'\x43\x00\x4F\x00\x4E\x00\x4F\x00\x55\x00\x54\x00\x24\x00\x00\x00'  # 0x148  C . O . N . O . U . T . $ . . .
; code += b'\x48\x65\x6C\x6C\x6F\x20\x77\x6F\x72\x6C\x64\x0A\x00'              # 0x158  H e l l o   w o r l d . .

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
main PROC

	; set addresses
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

	; MOV RAX, hStdOut
	RET

main ENDP
END
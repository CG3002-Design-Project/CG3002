$mod186
NAME EG0_COMP

;IO Setup for 80C188 
	UMCR    EQU    0FFA0H ; Upper Memory Control Register
	LMCR    EQU    0FFA2H ; Lower Memory control Register         
	PCSBA   EQU    0FFA4H ; Peripheral Chip Select Base Address
	MPCS    EQU    0FFA8H ; MMCS and PCS Alter Control Register
	IOPORT  EQU    00080H
	
; STACK SEGMENT
STACK_SEG		SEGMENT
	
STACK_SEG		ENDS
	
	
; DATA SEGMENT
DATA_SEG        SEGMENT 
DATA_SEG        ENDS

; RESET SEGMENT
Reset_Seg   SEGMENT
    MOV DX, UMCR
    MOV AX, 03E07H
    OUT DX, AX
	JMP far PTR start
	
Reset_Seg  ends
; MESSAGE SEGMENT
MESSAGE_SEG     SEGMENT
MESSAGE_SEG     ENDS
;CODE SEGMENT
CODE_SEG        SEGMENT
       
PUBLIC	START
ASSUME  CS:CODE_SEG, DS:DATA_SEG, SS:STACK_SEG
START:
; Initialize MPCS to MAP peripheral to IO address
	MOV DX, MPCS
	MOV AX, 0083H
	OUT DX, AX
; PCSBA initial, set the parallel port start from 00H
	MOV DX, PCSBA
	MOV AX, 0003H ; Peripheral starting address 00H no READY, No Waits
	OUT DX, AX
; Initialize LMCS 
    MOV DX, LMCR
    MOV AX, 01C4H  ; Starting address 1FFFH, 8K, No waits, last shoud be 5H for 1 waits      
    OUT DX, AX
	; YOUR CODE HERE ...
	; GOOD LUCK!
	
	mov ax, data_seg
	mov ds,ax
	mov es,ax
	PORTB EQU 00081h ; Port B
	PORTC EQU 00082h;  Port C
	CWR  EQU 00083h ; address
	
	;setting all ports to output on CWR
	mov dx,CWR
	mov al,80h
	out dx,al
	
	mov dx,PORTC
	mov al,00000110b ; RS - 0, R/W-1, E -1
	out dx,al
	
	;display 16
	mov dx,PORTB
	mov al,11101001b
	out dx,al
	
	;delay
	mov cx,0ffffh
	loopA:
	mov bx,3
	loopB:
	mov ax,[5000h]
	mov [5000h],ax
	mov ax,[5000h]
	dec bx
	jnz loopB
	loop loopA
	xor ax,ax
	
	;display 10
	mov dx,PORTB
	mov al,01101110b
	out dx,al
	
	;delay
	mov cx,0ffffh
	loopG:
	mov bx,3
	loopH:
	mov ax,[5000h]
	mov [5000h],ax
	mov ax,[5000h]
	dec bx
	jnz loopH
	loop loopG
	
	
	
CODE_SEG        ENDS
END
$MOD186
$EP
NAME TIMER
; Main program for uPD70208 microcomputer system
;
; Author: 	Dr Tay Teng Tiow
; Address:     	Department of Electrical Engineering 
;         	National University of Singapore
;		10, Kent Ridge Crescent
;		Singapore 0511.	
; Date:   	6th September 1991
;
; This file contains proprietory information and cannot be copied 
; or distributed without prior permission from the author.
; =========================================================================
public	serial_rec_action, timer2_action
extrn	print_char:far, print_2hex:far, iodefine:far
extrn   set_timer2:far
STACK_SEG	SEGMENT
		DB	256 DUP(?)
	TOS	LABEL	WORD
STACK_SEG	ENDS
DATA_SEG	SEGMENT
	TIMER0_MESS	DB	10,13,'TIMER2 INTERRUPT    '
	T_COUNT		DB	2FH
	T_COUNT_SET	DB	2FH
	REC_MESS	DB	10,13,'Period of timer0 =     '
	zerotoeleven    DB  '#','0','*','#','0','*','9','8','7','9','8','7'
	twelvetoend		DB	'6','5','4','6','5','4','3','2','1','3','2','1'
DATA_SEG	ENDS
$include(80188.inc)
CODE_SEG	SEGMENT
	PUBLIC		START
ASSUME	CS:CODE_SEG, SS:STACK_SEG, DS:DATA_SEG
START:
;initialize stack area
		MOV	AX,STACK_SEG		
		MOV	SS,AX
		MOV	SP,TOS
; Initialize the on-chip pheripherals
		CALL	FAR PTR	IODEFINE
; ^^^^^^^^^^^^^^^^^  Start of User Main Routine  ^^^^^^^^^^^^^^^^^^
    ;call set_timer2
    STI
MOV	BX,DATA_SEG		;initialize data segment register
	MOV	DS,BX
PORTA	EQU 	0080H
PORTB 	EQU 	0081H
PORTC 	EQU 	0082H
CWR 	EQU 	0083H
;set 8255 output
MOV AL, 89H       ;PA, PB output, PC input
MOV DX, CWR
OUT DX, AL        ;send the control word
NEXT:
	;test code turn on port A
;	MOV DX, PORTA
;	MOV AL, 11110000b
;	OUT DX, AL	
	;call far ptr simpletest
	call far ptr keypad
	;MOV AL, 'A'
	;CALL FAR PTR PRINT_CHAR
	JMP NEXT
; ^^^^^^^^^^^^^^^ End of User main routine ^^^^^^^^^^^^^^^^^^^^^^^^^
keypad proc far
	PUSH    DX
	PUSH	CX
	PUSH 	BX
	PUSH	AX

setup:	
	MOV CL, 11111110b ;Row output to ground from PB0
	MOV CH, 0H	;set row counter

startcycle:		
		;CL has the row grounding output
		MOV AL,CL
		MOV DX, PORTB	;port B address to DX; 
		OUT DX, AL	;ground one of the rows
		MOV DX, PORTC	;port B address to DX  
		IN  AL,DX		;read input port for key closure
		;input here should be 00xxxxx. checked to be correct
		;PC6 and PC7 are physically grounded- why is the input on them still 1?!
		XOR AL, 11111111b	;PC0 to PC5 masked. Whichever one is 0 will give a 1 output
		CMP AL,0H 	;checking for no key is pressed
	   	JE retpoint
		
		;ERROR CHECK
		CMP AL, 00000001B ;PC0 pressed
		JE column0
		CMP AL, 00000010B ;PC1 pressed
		JE column1
		CMP AL, 00000100B ;PC2 pressed
		JE column2
		CMP AL, 00001000B ;PC3 pressed
		JE column3
		CMP AL, 00010000B ;PC4 pressed
		JE column4
		CMP AL, 00100000B ;PC5 pressed
		JE column5
		JMP retpoint ;invalid keypress of some kind
resumekeypad:		
		;DL now has the column number
		;Logic: (Row number * 6) + col number 
		;gives us the so called button number being pressed, which can be stored as
		;an array starting at the top left of the keypad and ending at the bottom right
		mov AL,CH ; row number, previously saved
		MOV DH,06
		;multiply AL by DH, result stored in AX
		MUL DH ;row*6
		ADD AL, DL ;Add row*6 to col to get button number
		MOV BL,AL
		XOR BH,BH
		;BL now has the button number
		cmp BX, 12d
		jge greater_than_11
		MOV AL,DS:zerotoeleven[BX] ; Stores character in AL (?)
		jmp sendchar
greater_than_11:
		sub BL, 12d 
		MOV AL, DS:twelvetoend[BX]; Stores character in AL (?)
sendchar:
		XOR AH, AH
		CALL FAR PTR PRINT_CHAR
		CALL FAR PTR DELAY
		jmp retpoint
		
column0:
		MOV DL, 00000000b
		jmp resumekeypad
column1:
		MOV DL, 00000001b
		jmp resumekeypad
column2:
		MOV DL, 00000010b
		jmp resumekeypad
column3:
		MOV DL, 00000011b
		jmp resumekeypad
column4:
		MOV DL, 00000100b
		jmp resumekeypad
column5:
		MOV DL, 00000101b
		jmp resumekeypad	

retpoint: 
	INC CH
	CMP CH,04
	jz setup
	rol CL, 01H
	jmp startcycle
	
	POP AX
	POP BX
	POP CX
	POP DX
	ret
keypad endp
DELAY proc far
	PUSH    DX
	PUSH	CX
	PUSH 	BX
	PUSH	AX
	MOV AX, 04E20H
delay_loop:
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	dec AX
	cmp AX, 0H
	jne delay_loop
	POP AX
	POP BX
	POP CX
	POP DX
	ret
DELAY endp
SERIAL_REC_ACTION	PROC	FAR
		PUSH	CX
		PUSH 	BX
		PUSH	DS
		MOV	BX,DATA_SEG		;initialize data segment register
		MOV	DS,BX
		CMP	AL,'<'
		JNE	S_FAST
		INC	DS:T_COUNT_SET
		INC	DS:T_COUNT_SET
		JMP	S_NEXT0
S_FAST:
		CMP	AL,'>'
		JNE	S_RET
		DEC	DS:T_COUNT_SET
		DEC	DS:T_COUNT_SET
S_NEXT0:
		MOV	CX,22			;initialize counter for message
		MOV	BX,0
S_NEXT1:	MOV	AL,DS:REC_MESS[BX]	;print message
		call	FAR ptr print_char
		INC	BX
		LOOP	S_NEXT1
		MOV	AL,DS:T_COUNT_SET	;print current period of timer0
		CALL	FAR PTR PRINT_2HEX
S_RET:
		POP	DS
		POP	BX
		POP	CX
		RET
SERIAL_REC_ACTION	ENDP
TIMER2_ACTION	PROC	FAR
		PUSH	AX
		PUSH	DS
		PUSH	BX
		PUSH	CX
		MOV	AX,DATA_SEG
		MOV	DS,AX
		DEC	DS:T_COUNT
		JNZ	T_NEXT1
		MOV	AL,DS:T_COUNT_SET
		MOV	DS:T_COUNT,AL
		MOV	CX,20
		MOV	BX,0H
T_NEXT0:
		MOV	AL,DS:TIMER0_MESS[BX]
		INC	BX
		CALL 	FAR PTR PRINT_CHAR
		LOOP	T_NEXT0
T_NEXT1:	
		POP	CX
		POP	BX
		POP	DS
		POP 	AX
		RET
TIMER2_ACTION	ENDP
;generates a delay of about 560ms
CODE_SEG	ENDS
END
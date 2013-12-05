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
	ARRAY    	DB  '#','0','*','#','0','*','9','8','7','9','8','7'
	bottom2		DB	'6','5','4','6','5','4','3','2','1','3','2','1'
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
PORTA	EQU 	0080H
PORTB 	EQU 	0081H
PORTC 	EQU 	0082H
CWR 	EQU 	0083H

;set 8255 output
MOV AL, 89H       
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

keypad proc far

	PUSH    DX
	PUSH	CX
	PUSH 	BX
	PUSH	AX

	
	MOV	BX,DATA_SEG		;initialize data segment register
	MOV	DS,BX
	
SETUP:		

	MOV CL, 07FH ;01111111 Row output to ground from PB
	MOV CH, 0H	;set row counter



NEXTROW:		
		ROL CL, 01H  ;rotate CL to ground next row/ al HAS 8 BITS. so must JMP BACK TO WAIT

		MOV AL,CL
		MOV DX, PORTB	;port B address to DX; 
		OUT DX, AL	;ground one of the rows
                
		MOV DX, PORTC	;port B address to DX  
		IN  AL,DX		;read input port for key closure


		XOR AL, 11111111b	;PC0 to PC5 masked. Whichever one is 0 will give a 1 output
		
		CMP AL,0H 	;checking for no key is pressed
	   	JE RETPOINT
		
		;ERROR CHECK
		CMP AL, 00000001B ;PC0 pressed
		JE VALIDATED
		CMP AL, 00000010B ;PC1 pressed
		JE VALIDATED
		CMP AL, 00000100B ;PC2 pressed
		JE VALIDATED
		CMP AL, 00001000B ;PC3 pressed
		JE VALIDATED
		CMP AL, 00010000B ;PC4 pressed
		JE VALIDATED
		CMP AL, 00100000B ;PC5 pressed
		JE VALIDATED
		
		JMP RETPOINT ;invalid keypress of some kind

VALIDATED:		
		
		
		;AND AL, 07H; MASK OTHER BLOODY BITS OMGOMGOMG
		
		SHR AL,01 ; shifting right gives you the col number, the first col on the keypad being col 0
		MOV DL,AL ; this col number goes into DL

		;Logic: (Row number * 6) + col number 
		;gives us the so called button number being pressed, which can be stored as
		;an array starting at the top left of the keypad and ending at the bottom right
		
		mov AL,CH ; row number, previously saved
		MOV DH,06
		;multiply AL by DH, result stored in AX
		MUL DH

		
		ADD AL, DL ;Add row*6 to col to get button number
		
		
		MOV BL,AL
		XOR BH,BH
		;BL now has the button number
		
		; MOV BL,0H ; force array index to 0 for testing.
		
topnumbers:
		cmp BX, 12
		jge bottom_numbers
		MOV AL,DS:ARRAY[BX] ; Stores character in AL (?)
		jmp NUMBERS

bottom_numbers:
		sub BL, 12d 
		MOV AL, DS:bottom2[BX]; Stores character in AL (?)
		
NUMBERS:
		XOR AH, AH
		CALL FAR PTR PRINT_CHAR
		
		CALL FAR PTR DELAY
              		
RETPOINT:	
	INC CH
	CMP CH,04
	JNZ NEXTROW
	JMP SETUP


	POP AX
	POP BX
	POP CX
	POP DX
	ret

keypad endp

;generates a delay of about 560ms
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

CODE_SEG	ENDS
END

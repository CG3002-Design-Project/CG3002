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
	top2      	DB  10,13,'this is A'
	bottom2		DB	10,13,'this is B'
DATA_SEG	ENDS

$include(80188.inc)

CODE_SEG	SEGMENT

	PUBLIC		START

ASSUME	CS:CODE_SEG, SS:STACK_SEG

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
	;call far ptr keypad
	call far ptr lcd
	
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

topnumbers:
		cmp BX, 12
		jge bottom_numbers
		MOV AL, DS:top2[BX]; Stores character in AL (?)
		jmp NUMBERS

bottom_numbers:
		sub BL, 12d 
		MOV AL, DS:bottom2[BX]; Stores character in AL (?)
		
NUMBERS:
		XOR AH,AH
		CALL FAR PTR PRINT_CHAR
		;CALL FAR PTR PRINT_2HEX
              		
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

lcd proc far

	PUSH    DX
	PUSH	CX
	PUSH 	BX
	PUSH	AX


FRONT:		

	mov ax, DATA_SEG
	mov ds,ax
	mov es,ax

	
	;The following sends all the necessary commands to the LCD
	MOV AL, 38H ;initialize LCD for 2 lines & 5*7 matrix
	CALL COMNDWRT ;write the command to LCD	
	CALL DELAY ;wait before issuing the next command
	CALL DELAY 
	;this command needs lots of delay
	CALL DELAY
	MOV AL, 0EH ;send command for LCD on, cursor on 0000 1110b 
	CALL COMNDWRT
	CALL DELAY
	MOV AL, 01 	 ;clear LCD
	CALL COMNDWRT
	CALL DELAY
	MOV AL, 06 	 ;command for shifting cursor right
	CALL COMNDWRT
	CALL DELAY

	COMNDWRT PROC ;this procedure writes commands to LCD
		PUSH DX ;save DX
		MOV DX, PORTB
		OUT DX, AL 	 ;send the code to Port A
		MOV DX, PORTC
		MOV AL, 00000100B ;RS=0,R/W=0,E=1 for H-To-L pulse
		OUT DX, AL
		NOP
		NOP
		MOV AL, 00000000B ;RS=0,R/W=0,E=0 for H-To-L pulse
		OUT DX, AL
		POP DX
		RET
	COMNDWRT ENDP
	
	MOV AL, 1 ;display ‘1’ letter
	CALL DATWRIT ;issue it to LCD
	CALL DELAY ;wait before issuing the next character
	MOV AL, 2 ;display ‘2’ letter
	CALL DATWRIT ;issue it to LCD
	CALL DELAY ;wait before issuing the next character
	MOV AL, 5 ;display ‘5’ letter
	CALL DATWRIT ;issue it to LCD
	CALL DELAY ;wait
	;data write to LCD without checking the busy flag
	;AL = char sent to LCD
	
	DATWRIT PROC
		PUSH DX  ;save DX
		MOV DX, PORTB  ;DX=port B address
		OUT DX, AL ;issue the char to LCD
		MOV AL, 00000101B ;RS=1,R/W=0, E=1 for H-to-L pulse
		MOV DX, PORTC ;port B address
		OUT DX, AL  ;make enable high
		MOV AL, 00000001B ;RS=1,R/W=0 and E=0 for H-to-L pulse
		OUT DX, AL
		POP DX
		RET
	DATWRIT ENDP
	
	DELAY PROC
		MOV CX, 1325  ;1325*15.085 usec = 20 msec
		PUSH AX
		W1: IN AL, 61H
		AND AL, 00010000B
		CMP AL, AH
		JE W1
		MOV AH, AL
		LOOP W1
		POP AX
		RET
	DELAY ENDP

	JMP FRONT
	POP AX
	POP BX
	POP CX
	POP DX
	ret	
	
lcd endp


CODE_SEG	ENDS
END

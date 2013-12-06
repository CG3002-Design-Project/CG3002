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
extrn	print_char:far, print_2hex:far, iodefine:far,delay:far
extrn   set_timer2:far

STACK_SEG	SEGMENT
		DB	256 DUP(?)
	TOS	LABEL	WORD
STACK_SEG	ENDS


DATA_SEG	SEGMENT
	TIMER0_MESS	DB	10,13,'TIMER1 INTERRUPT    '
	T_COUNT		DB	2FH
	T_COUNT_SET	DB	2FH
	REC_MESS	DB	''
	COUNTER     DW 0H
	FLAG        DB 0H
	DFLAG       DB 0H
	DISPLAY_BUFF DB	100 DUP(?)
	D1			DB	'Barcode :'
	D2			DB	'123456'  
	D3			DB	'Price   :$'  
	D4			DB	'225.5'   
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
		call set_timer2
        STI
	
		MOV CX, 9H
		MOV BX, DATA_SEG
		MOV DS, BX
		MOV BX, 0H
			
		
NEXT:     JMP NEXT

; ^^^^^^^^^^^^^^^ End of User main routine ^^^^^^^^^^^^^^^^^^^^^^^^^


SERIAL_REC_ACTION	PROC	FAR
		PUSH	CX
		PUSH 	BX
		PUSH	DS

		MOV	BX,DATA_SEG		;initialize data segment register
		MOV	DS,BX
		
	    CALL  FAR PTR print_char
					
		MOV CX, 1H
		MOV BX, DATA_SEG
		MOV DS, BX
		MOV BX, 0H
		
	
		;CMP  AL,'!'
		;JE SET_FLAG
		
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
		
		; PUSH AX
		; MOV AL, 18H ;set entry mode register
		; CALL FAR PTR CMD_WRITE
		; CALL FAR PTR DELAY
		; POP AX
		;MOV DX, 180H
		;OUT DX, 0FFH
		
		;MOV DX, 200H
		;OUT DX, 0FFH
		
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


CODE_SEG	ENDS
END

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
extrn	print_char:far, print_2hex:far, iodefine:far, CMD_WRITE:far,delay:far, DATA_WRITE: far
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
	DISPLAY_BUFF DB	''
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
		;START OF LCD ROUTINE
		MOV DX, 83H
		MOV AX, 080H
		OUT DX, AX
		CALL FAR PTR DELAY
		
		MOV AL, 38H ; Set function set
		CALL FAR PTR CMD_WRITE
		CALL FAR PTR DELAY
		CALL FAR PTR DELAY
		CALL FAR PTR DELAY
		
		MOV AL, 08H ;Switch off display
		CALL FAR PTR CMD_WRITE
		CALL FAR PTR DELAY
		
		MOV AL, 01H ;Clear lcd
		CALL FAR PTR CMD_WRITE
		CALL FAR PTR DELAY
		
		MOV AL, 06H ;Set entry mode register
		CALL FAR PTR CMD_WRITE
		CALL FAR PTR DELAY
		
		MOV AL, 0FH ;Set display on, cursor on, and blinking
		CALL FAR PTR CMD_WRITE
		CALL FAR PTR DELAY
			
		
		MOV CX, 9H
		MOV BX, DATA_SEG
		MOV DS, BX
		MOV BX, 0H
		
; PRINTMSG:
		; MOV AL, DS:D1[BX]
		; CALL FAR PTR DATA_WRITE
		; CALL FAR PTR DELAY
		; INC BX
		; LOOP PRINTMSG
		
		; MOV CX, 6H
		; MOV BX, 0H
		
; PRINTBARCODE:
		; MOV AL, DS:D2[BX]
		; CALL FAR PTR DATA_WRITE
		; CALL FAR PTR DELAY
		; INC BX
		; LOOP PRINTBARCODE		
	
		; MOV AL, 0C0H ;Set DDRAM Address to Next Line
		; CALL FAR PTR CMD_WRITE
		; CALL FAR PTR DELAY
		
		; MOV CX, 0AH
		; MOV BX, DATA_SEG
		; MOV DS, BX
		; MOV BX, 0H
; PRINTNEXTLINE:
		; MOV AL, DS:D3[BX]
		; CALL FAR PTR DATA_WRITE
		; CALL FAR PTR DELAY
		; INC BX
		; LOOP PRINTNEXTLINE
		
		; MOV CX, 6H
		; MOV BX, 0H
		
; PRINTPRICE:
		; MOV AL, DS:D4[BX]
		; CALL FAR PTR DATA_WRITE
		; CALL FAR PTR DELAY
		; INC BX
		; LOOP PRINTPRICE	
		

		
		MOV AL, 01H ;Clear lcd
		CALL FAR PTR CMD_WRITE
		CALL FAR PTR DELAY
		
		
NEXT:     JMP NEXT

; ^^^^^^^^^^^^^^^ End of User main routine ^^^^^^^^^^^^^^^^^^^^^^^^^


SERIAL_REC_ACTION	PROC	FAR
		PUSH	CX
		PUSH 	BX
		PUSH	DS

		MOV	BX,DATA_SEG		;initialize data segment register
		MOV	DS,BX
				
		MOV DS:REC_MESS, AL
	    CALL  FAR PTR print_char
		
		;START OF LCD ROUTINE
		MOV DX, 83H
		MOV AX, 080H
		OUT DX, AX
		CALL FAR PTR DELAY
		
		MOV AL, 06H ;Set entry mode register
		CALL FAR PTR CMD_WRITE
		CALL FAR PTR DELAY
		
		MOV AL, 0FH ;Set display on, cursor on, and blinking
		CALL FAR PTR CMD_WRITE
		CALL FAR PTR DELAY
			
		
		MOV CX, 1H
		MOV BX, DATA_SEG
		MOV DS, BX
		MOV BX, 0H
		
    	MOV AL, DS:REC_MESS[BX]
		CMP AL, '#'
		JE CHECK_DISPLAY
		JNE PRINT

PRINT: 		
       CALL FAR PTR PRINT_CHAR
	   JMP S_RET
		
CHECK_DISPLAY:
		INC BX
		MOV AL, DS:REC_MESS[BX]
		CALL  FAR PTR print_char
		MOV DS:DISPLAY_BUFF, AL
		CMP AL, 'X'
		JE DONE_DISPLAY
        LOOP CHECK_DISPLAY
		
DONE_DISPLAY:
        PUSH BX
		XOR BX, BX
		MOV AL, DS:DISPLAY_BUFF[BX]
		CMP AL,1
		JNE DONT_DISPLAY
		INC BX
		MOV AL, DS:DISPLAY_BUFF[BX]
		CMP AL,1
		JNE DONT_DISPLAY
		INC BX
		MOV AL, DS:DISPLAY_BUFF[BX]
		CMP AL,1
		JNE DONT_DISPLAY
		INC BX
		MOV AL, DS:DISPLAY_BUFF[BX]
		CMP AL,1
		JNE DONT_DISPLAY
		INC BX
		MOV AL, DS:DISPLAY_BUFF[BX]
		CMP AL,'*'
		
		POP BX
		JNE DONT_DISPLAY
		JMP DISPLAY

DISPLAY:
		CMP AL, ':'
		JE MOV_NEXT_LINE
		JNE PRINTMSG1	
		
DONT_DISPLAY:
		JMP S_RET
       			
	
MOV_NEXT_LINE:
		
		MOV AL, 0C0H ;Set DDRAM Address to Next Line
		CALL FAR PTR CMD_WRITE
		CALL FAR PTR DELAY
		
		
PRINTMSG1:
		MOV AL, DS:REC_MESS[BX]
		CALL FAR PTR DATA_WRITE
		CALL FAR PTR DELAY
		INC BX
		LOOP PRINTMSG1
		
		MOV CX, 6H
		MOV BX, 0H
		
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

$MOD186
$EP
NAME TIMER
; Main program for uPD70208 microcomputer system
;
; Author:         Dr Tay Teng Tiow
; Address:             Department of Electrical Engineering 
;                 National University of Singapore
;                10, Kent Ridge Crescent
;                Singapore 0511.        
; Date:           6th September 1991
;
; This file contains proprietory information and cannot be copied 
; or distributed without prior permission from the author.
; =========================================================================

public        serial_rec_action, timer2_action
extrn        print_char:far, print_2hex:far, iodefine:far
extrn   set_timer2:far



STACK_SEG        SEGMENT
                DB        256 DUP(?)
        TOS        LABEL        WORD
STACK_SEG        ENDS

DATA_SEG        SEGMENT
        TIMER0_MESS        	DB      10,13,'TIMER2 INTERRUPT    '
        T_COUNT             DB      2FH
        T_COUNT_SET       	DB      2FH
        REC_MESS        	DB      10,13,'Period of timer0 =     '
        DISPLAY_DIGIT    	DB      3FH,06H,5BH,4FH,66H,6DH,7DH,07H,7FH,06FH ;from 0-9, the display digits for BCD
        DISPLAY_NUM      	DB      1H, 2H, 3H, 4H, 5H, 6H  ;numbers to be displayed
DATA_SEG        ENDS


$include(80188.inc)

CODE_SEG        SEGMENT

        PUBLIC                START

ASSUME        CS:CODE_SEG, SS:STACK_SEG

START:
	
	;Chip select configurations
	PCS3_select   EQU   0180H
	PCS2_select   EQU   0183H 
				
	MOV        AX,STACK_SEG                
	MOV        SS,AX
	MOV        SP,TOS

; Initialize the on-chip pheripherals
	CALL        FAR PTR        IODEFINE

; ^^^^^^^^^^^^^^^^^  Start of User Main Routine  ^^^^^^^^^^^^^^^^^^
    ;call set_timer2
     ;STI
	 
NEXT:
	 call FAR PTR LED
	 jmp NEXT
    
; ^^^^^^^^^^^^^^^ End of User main routine ^^^^^^^^^^^^^^^^^^^^^^^^^

LED PROC FAR
		PUSH AX
        PUSH BX
        PUSH CX
        PUSH DX
		
		MOV AX, PCS3_select
		MOV DX, 
		
		
		POP DX
        POP CX
        POP BX
        POP AX
        RET
LED       ENDP

DISPLAY_BCD        PROC        FAR
        PUSH AX
        PUSH BX
        PUSH CX
        PUSH DX
        
        CALL FAR PTR BIN_CONV_DISPLAY
        
        MOV DX,CHIP_SELECT
        OUT DX,AL
    
        POP DX
        POP CX
        POP BX
        POP AX
        RET
DISPLAY_BCD        ENDP


;CONVERTS 4 BIT BINARY INTO CORRESPONDING DIGITS      
BIN_CONV_DISPLAY PROC FAR
		PUSH BX
		
        MOV BL,AL
		MOV BH, 0H
        MOV AL,DS:DISPLAY_DIGIT[BX]
        POP BX
        RET
BIN_CONV_DISPLAY ENDP  


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




CODE_SEG	ENDS
END

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
        TIMER0_MESS        DB        10,13,'TIMER2 INTERRUPT    '
        T_COUNT                DB        2FH
        T_COUNT_SET        DB        2FH
        REC_MESS        DB        10,13,'Period of timer0 =     '
		
		LED0 DB 00H
		LED1 DB 01H
		LED2 DB 02H
		LED3 DB 03H
		LED4 DB 04H
		LED5 DB 05H
		LED_COUNT DB 06H
		
		;for LED
		;d0- cathode A
		;d1- cathode F
		;d2- cathode E
		;d3- cathode D
		;d4- cathode C
		;d5- cathode G
		;d6- cathode B
		;d7- cathode DP
		
		;d|B|G|C|D|E|F|A
		
		;ground cathode to turn off
		; 0 - 01011111b - 5FH
		; 1 - 01010000b - 50H
		; 2 - 01101101b - 6DH
		; 3 - 01111001b - 79H
		; 4 - 01110010b - 72H
		; 5 - 00111011b - 3BH
		; 6 - 00111111b - 3FH
		; 7 - 01010001b - 51H
		; 8 - 01111111b - 7FH
		; 9 - 01111011b - 7BH
		; d - 10000000b - 80H
		
        ;BCD                DB        7EH,30H,6DH,79H,33H,5BH,5FH,70H,7FH,7BH
        CATHODES            DB         5FH,	50H, 6DH, 79H, 72H, 3BH, 3FH, 51H, 7FH, 7BH, 80H
        DISPLAY_NUM        DW        1234H
DATA_SEG        ENDS

$include(80188.inc)
CODE_SEG        SEGMENT

        PUBLIC                START

ASSUME        CS:CODE_SEG, SS:STACK_SEG

START:
;initialize stack area
                   
	MOV        AX,STACK_SEG                
	MOV        SS,AX
	MOV        SP,TOS

;initialize DS
	MOV BX, DATA_SEG
	MOV DS,BX
	
; Initialize the on-chip pheripherals
	CALL        FAR PTR        IODEFINE
                
;set register values
	LED_SELECT        EQU        0100H ;PCS2
	LED_OUTPUT        EQU        0180H ;PCS3
				
; ^^^^^^^^^^^^^^^^^  Start of User Main Routine  ^^^^^^^^^^^^^^^^^^
    call far ptr set_timer2
    STI
	
; INIT:
    ; MOV BX, DATA_SEG
	; MOV DS,BX

; first:	
	; mov cx, 00H
	; mov bx, 01H
	; mov al, 01111111b
	

NEXT:

	; rol AL, 01
	; mov dx, LED_SELECT
	; out dx, al
	
	; MOV AL, DS:CATHODES[BX]
	; MOV DX, LED_OUTPUT
    ; OUT DX,AL
	
	; mov AL, 11111111b
	; mov dx, LED_SELECT
	; out dx, AL
	
	; MOV AL, 0H
	; MOV DX, LED_OUTPUT
    ; OUT DX,AL
	
	;inc CX
	;inc BX
	;cmp CX, 05H
	;je first
	
JMP NEXT

; ^^^^^^^^^^^^^^^ End of User main routine ^^^^^^^^^^^^^^^^^^^^^^^^^

;; EXPECTS 16 BIT BCD ENCODED NUMBER IN AX.  
DISPLAY_BCD        PROC        FAR
	PUSH AX
	PUSH BX
	PUSH CX
	PUSH DX
	;; NUMBER STORED IN CX
	MOV CX, AX
	MOV BH, 0FEH;1111 1110
	MOV BL, 04H
LOOP_START:
        ;; SET LCD_SELECT
        MOV AL, BH
        MOV DX, LED_SELECT
        OUT DX, AL
        
        ROL BH,01 ;1111 1101 -> 1111 1011 -> 1111 0111
        
        MOV AX, CX
        
        AND AL, 0FH
        ;5557 : 0101 0101 0101 0111 ->000 0111
        CALL FAR PTR BCD_TO_7SEG
        
        ;RESULT IN AL
        MOV DX, LED_OUTPUT
        OUT DX,AL
        MOV AL,0H
        OUT DX,AL
        
        DEC BL
        SHR CX,04H
        ;0000 0101 0101 0101
        ; 0000 0000 0101 0101
        ;BL IS NOW 2
        ;0000 0000 0000 0101
        
        CMP BL, 0
        JNZ LOOP_START

        
        POP DX
        POP CX
        POP BX
        POP AX
        RET
DISPLAY_BCD        ENDP
;; EXPECTS A 16 BIT NUMBER IN AX. DISPLAYS IT ON THE 7 SEGMENT 
;; NOTE: 16 BITS MEANS 4 BCD DIGITS. THIS THIS ROUTINE ONLY USES 4 LEDS. 

CONVERT_TO_BCD        PROC        FAR


        PUSH BX
        MOV BL,AL
        CMP BL,10
        JGE GREATER_THAN_10
        JMP RETURN_BCD
;; IF BL(AL) > = 10 WE ADD 6. AH -> 10H 
GREATER_THAN_10:
        ADD AL,06
        
RETURN_BCD:
        
        POP BX
        RET
CONVERT_TO_BCD        ENDP
;; 
;EXPECTS A 4BIT BCD DIGIT IN AL. RETURNS THE 7SEG CODE IN AL FOR THAT DIGIT        
BCD_TO_7SEG        PROC        FAR
        PUSH BX

        ;; STORE AL TEMPORARILY IN BL
        MOV BL,AL
        
        XOR BH,BH
        ;; GET THE BLTH INDEX OF THE BCD ARRAY IN DATA_SEG
        MOV AL,DS:CATHODES[BX]
        POP BX
        RET
BCD_TO_7SEG        ENDP        


SERIAL_REC_ACTION        PROC        FAR
                PUSH        CX
                PUSH         BX
                PUSH        DS

                MOV        BX,DATA_SEG                ;initialize data segment register
                MOV        DS,BX

                CMP        AL,'<'
                JNE        S_FAST

                INC        DS:T_COUNT_SET
                INC        DS:T_COUNT_SET

                JMP        S_NEXT0
S_FAST:
                CMP        AL,'>'
                JNE        S_RET

                DEC        DS:T_COUNT_SET
                DEC        DS:T_COUNT_SET

S_NEXT0:
                MOV        CX,22                        ;initialize counter for message
                MOV        BX,0

S_NEXT1:        MOV        AL,DS:REC_MESS[BX]        ;print message
                call        FAR ptr print_char
                INC        BX
                LOOP        S_NEXT1

                MOV        AL,DS:T_COUNT_SET        ;print current period of timer0
                CALL        FAR PTR PRINT_2HEX
S_RET:
                POP        DS
                POP        BX
                POP        CX
                RET
SERIAL_REC_ACTION        ENDP



TIMER2_ACTION PROC FAR

	PUSH        AX
	PUSH        BX
	PUSH        CX
	PUSH        DX
	
	;init data segment
	MOV BX, DATA_SEG
	MOV DS,BX
	
	mov bx, 0H
	;check which LEDs turn it is
	xor ax, ax
	xor cx, cx
	mov cl, DS:LED_COUNT
	
	;cl has the led count
	cmp cl, 01H
	je led_0
	cmp cl, 02H
	je led_1
	cmp cl, 03H
	je led_2
	cmp cl, 04H
	je led_3
	cmp cl, 05H
	je led_4
	cmp cl, 06H
	je led_5
	
led_0:
	mov al, 11111110b
	mov dx, LED_SELECT
	out dx, al
	mov al, DS:LED0
	jmp decided
	
led_1:
	mov al, 11111101b
	mov dx, LED_SELECT
	out dx, al
	mov al, DS:LED1
	jmp decided
	
led_2:
	mov al, 11111011b
	mov dx, LED_SELECT
	out dx, al
	mov al, DS:LED2	
	jmp decided
	
led_3:
	mov al, 11110111b
	mov dx, LED_SELECT
	out dx, al
	mov al, DS:LED3	
	jmp decided
	
led_4:
	mov al, 11101111b
	mov dx, LED_SELECT
	out dx, al
	mov al, DS:LED4
	jmp decided
	
led_5:
	mov al, 11011111b
	mov dx, LED_SELECT
	out dx, al
	mov al, DS:LED5
	jmp decided

decided:
	xor bx, bx
	mov bl, al
	mov al, DS:CATHODES[BX]
	mov dx, LED_OUTPUT
	out dx, al
	
	;now to cycle the LED count
	cmp cl, 06H
	je reset_led_count
	jmp continue_led_count

reset_led_count:
	mov cl, 00H
	mov DS:LED_COUNT, 01H
	mov AX, 01H
	mov [SI], AX
	jmp exit_timer

continue_led_count:
	inc DS:LED_COUNT

exit_timer:	
	POP        DX
	POP        CX
	POP        BX
	POP        AX
	RET
TIMER2_ACTION        ENDP	
	
	; first:
	; MOV BX, DATA_SEG
	; MOV DS,BX
	; xor cx, cx
	; mov cl, 01111111b
	; mov bx, 00H
	
	; mov AL, '1'
	; xor AH, AH
	; CALL FAR PTR PRINT_CHAR
	
	; mov AL, 11111110b
	; mov dx, LED_SELECT
	; out dx, al
	
	; MOV AL, 11111111b
	; MOV DX, LED_OUTPUT
    ; OUT DX,AL

	
	
; cycle:
	
	; rol cl, 01
	
	; mov AL, CL
	; mov dx, LED_SELECT
	; out dx, al
	
	; MOV AL, DS:CATHODES[BX]
	; MOV DX, LED_OUTPUT
    ; OUT DX,AL
	
	; mov AL, 11111111b
	; mov dx, LED_SELECT
	; out dx, AL
	
	; MOV AL, 0H
	; MOV DX, LED_OUTPUT
    ; OUT DX,AL
	

	; cmp cl, 11011111b
	; je exit_timer
	
	; inc BX
	; jmp cycle			
				
                ; MOV        AX,DATA_SEG
                ; MOV        DS,AX
        
                ; DEC        DS:T_COUNT
                ; JNZ        T_NEXT1
                ; MOV        AL,DS:T_COUNT_SET
                ; MOV        DS:T_COUNT,AL

                ; MOV        CX,20
                ; MOV        BX,0H
; T_NEXT0:
                ; MOV        AL,DS:TIMER0_MESS[BX]
                ; INC        BX
                ; CALL         FAR PTR PRINT_CHAR
                ; LOOP        T_NEXT0

; T_NEXT1:



CODE_SEG        ENDS
END
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
		
		LED_displays DB 00H,00H,00H,00H,00H,00H
		
		LED0 DB 00H
		LED1 DB 01H
		LED2 DB 02H
		LED3 DB 03H
		LED4 DB 04H
		LED5 DB 05H
		LED_COUNT DB 00H
		
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
		; 2 - 01101101b - 6CH
		; 3 - 01111001b - 79H
		; 4 - 01110010b - 72H
		; 5 - 00111011b - 3BH
		; 6 - 00111111b - 3FH
		; 7 - 01010001b - 51H
		; 8 - 01111111b - 7FH
		; 9 - 01111011b - 7BH
		; d - 10000000b - 80H
		
        ;BCD                DB        7EH,30H,6DH,79H,33H,5BH,5FH,70H,7FH,7BH
        CATHODES            DB         5FH,	50H, 6CH, 79H, 72H, 3BH, 3FH, 51H, 7FH, 7BH, 80H
        DISPLAY_NUM        DW        1234H
		
		;need to be careful here to avoid ASCII characters that map to 0-9
		zerotoeleven    DB  '#',0H,'*','>','0','*',09H,08H,07H,'9','8','7'
		twelvetoend		DB	06H,05H,04H,'6','5','4',03H,02H,01H,'3','2','1'
		
		LED_NUMBER_STORAGE DB 0H,0H,0H,0H,0H,0H,0H
		LED_storage_count
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
	cmp cl, 00H
	je led_0
	cmp cl, 01H
	je led_1
	cmp cl, 02H
	je led_2
	cmp cl, 03H
	je led_3
	cmp cl, 04H
	je led_4
	cmp cl, 05H
	je led_5
	
led_0:
	mov al, 11111110b
	mov dx, LED_SELECT
	
	
	out dx, al
	mov al, DS:LED_displays[cx]
	jmp decided
	
led_1:
	mov al, 11111101b
	jmp decided
led_2:
	mov al, 11111011b
	jmp decided
led_3:
	mov al, 11110111b
	jmp decided
led_4:
	mov al, 11101111b
	jmp decided
led_5:
	mov al, 11011111b
	jmp decided
	
	
decided:
	mov dx, LED_SELECT
	out dx, al
	mov al, DS:LED_displays[cx]
	jmp decided
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
	mov DS:LED_COUNT, 00H
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
		
		;we now need to know what to do with this keypress, the character for which is stored in AL
		;CALL FAR PTR PRINT_CHAR
		call far ptr analyze_key
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

;character for keypress is in AL
analyze_key proc far
push bx
push cx
push dx

;ASCII char 0 is dec  48
;char 9 is dec 57

cmp al, 09H
jg action_key

;if not, then it's a number
mov cx, DS:LED_storage_count
cmp cx, 00H
jne switch_LEDs
;count is 0, then-
mov bx, 03H
mov DS:LED_displays[bx], AL ;mov that number into led3
inc DS:LED_storage_count
jmp exit_analyze_key

switch LEDs:
xor cx, cx

;other LEDs shifted
mov bx, 01H 
mov cl, DS:LED_displays[BX]
mov bx, 00H
mov DS:LED_displays[BX], cl

mov bx, 02H 
mov cl, DS:LED_displays[BX]
mov bx, 01H
mov DS:LED_displays[BX], cl

mov bx, 03H 
mov cl, DS:LED_displays[BX]
mov bx, 02H
mov DS:LED_displays[BX], cl

;new number added to led3
mov bx, 03H
mov DS:LED_displays[bx], AL ;mov that number into led3
inc DS:LED_storage_count

exit_analyze_key:

pop dx
pop cx
pop bx
ret


analyze_key endp


CODE_SEG        ENDS
END
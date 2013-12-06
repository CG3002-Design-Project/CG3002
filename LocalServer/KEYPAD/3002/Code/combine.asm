$MOD186
$EP
NAME combine
; =========================================================================

public        serial_rec_action, timer2_action
extrn        print_char:far, print_2hex:far, iodefine:far
extrn   set_timer2:far, keypad:far

STACK_SEG        SEGMENT
    DB        256 DUP(?)
    TOS        LABEL        WORD
STACK_SEG        ENDS

DATA_SEG        SEGMENT
	TIMER0_MESS	DB	10,13,'TIMER2 INTERRUPT    '
	T_COUNT		DB	2FH
	T_COUNT_SET	DB	2FH
	REC_MESS	DB	10,13,'Period of timer0 =     '
	LED_displays DB 00H,00H,00H,00H,00H,00H
	
	LED0 DB 00H
	LED1 DB 01H
	LED2 DB 02H
	LED3 DB 03H
	LED4 DB 04H
	LED5 DB 05H
	LED_COUNT DB 00H
	
	;BCD                DB        7EH,30H,6DH,79H,33H,5BH,5FH,70H,7FH,7BH
	CATHODES            DB         5FH,	50H, 6CH, 79H, 72H, 3BH, 3FH, 51H, 7FH, 7BH, 80H
	DISPLAY_NUM        DW        1234H
	
	LED_NUMBER_STORAGE DB 0H,0H,0H,0H,0H,0H,0H
	LED_storage_count DB 0H
DATA_SEG        ENDS

$include(80188.inc)
CODE_SEG        SEGMENT
PUBLIC  START
ASSUME  CS:CODE_SEG, SS:STACK_SEG, DS:DATA_SEG

START:
;initialize stack area
                   
	MOV        AX,STACK_SEG                
	MOV        SS,AX
	MOV        SP,TOS

;initialize DS
	MOV BX, DATA_SEG
	MOV DS, BX
	
; Initialize the on-chip pheripherals
	CALL FAR PTR IODEFINE
                
;set register values
	LED_SELECT  EQU 0100H ;PCS2
	LED_OUTPUT  EQU 0180H ;PCS3
				
; ^^^^^^^^^^^^^^^^^  Start of User Main Routine  ^^^^^^^^^^^^^^^^^^
    call far ptr set_timer2
    STI

NEXT:
	call far ptr keypad
	
JMP NEXT

; ^^^^^^^^^^^^^^^ End of User main routine ^^^^^^^^^^^^^^^^^^^^^^^^^

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

S_NEXT1:       
	MOV        AL,DS:REC_MESS[BX]        ;print message
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
	mov bx, cx
	mov al, DS:LED_displays[bx]
	
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

CODE_SEG        ENDS
END
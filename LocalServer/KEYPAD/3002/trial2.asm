$MOD186
$EP
NAME trial2
; =========================================================================

public        serial_rec_action, timer2_action, analyze_key
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
	LED_displays DB 80H,80H,80H,80H,80H,80H
	
	
	LED_COUNT DB 00H
	
	;BCD                DB        7EH,30H,6DH,79H,33H,5BH,5FH,70H,7FH,7BH
	CATHODES            DB         5FH,	50H, 6DH, 79H, 72H, 3BH, 3FH, 51H, 7FH, 7BH, 80H
	DISPLAY_NUM        DW        1234H
	
	empty_led_counter DB 06H
	
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
	;call far ptr keypad
	
JMP NEXT

; ^^^^^^^^^^^^^^^ End of User main routine ^^^^^^^^^^^^^^^^^^^^^^^^^

SERIAL_REC_ACTION        PROC        FAR
	PUSH        CX
	PUSH         BX
	PUSH        DS

	MOV        BX,DATA_SEG                ;initialize data segment register
	MOV        DS,BX

	CMP  AL,'/'
	JE	error_show

	exit_serial:
	POP        DS
	POP        BX
	POP        CX
	RET
	
error_show:	
	mov BX, 0H
	mov DS:LED_DISPLAYS[BX], 2FH
	inc BX
	mov DS:LED_DISPLAYS[BX], 24H
	inc BX
	mov DS:LED_DISPLAYS[BX], 24H
	inc BX
	mov DS:LED_DISPLAYS[BX], 3CH
	inc BX
	mov DS:LED_DISPLAYS[BX], 24H
	inc BX
	mov DS:LED_DISPLAYS[BX], 00H
	jmp exit_serial

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
	
	; xor bx, bx
	; mov bl, al
	; mov al, DS:CATHODES[BX]
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


;character/number for keypress is in AL
analyze_key proc far
push bx
push cx
push dx



;need to access data_segment
mov bx, data_seg
mov ds, bx

;check if number has been pressed
cmp al, 09H
jg action_key ;if not number, it is an action key

;if it's a number-
;call far ptr print_char
xor bx, bx
mov bl, al ;bl now has the number
mov al, DS:CATHODES[BX] ;now AL has the BCD version of the number

mov cl, DS:empty_led_counter ;this keeps track of how many empty leds (hence how many successive buttons pressed)
cmp cl, 0H ;no free leds
je exit_analyze_key

cmp cl, 06H ;all leds empty, no buttons pressed yet
jne shift_LEDs ;not empty, we need to shift 

;if equal to 0, first number press
mov bx, 05H ;access the right most LED
mov DS:LED_displays[bx], AL ;mov that number into led5
dec DS:empty_led_counter ; decrement empty LEDs
jmp exit_analyze_key

shift_LEDs:
;cl has the number_counter
xor bx, bx
mov bl, cl 

xor dx, dx
mov dl, DS:LED_displays[bx]
dec bl
mov DS:LED_displays[bx], dl

inc cl
cmp cl, 06H
jne shift_LEDs

;latest number to right most LED
mov bx, 05H
mov DS:LED_displays[bx], al
dec DS:empty_led_counter ; decrement empty LEDs
jmp exit_analyze_key

action_key:
cmp al, '>'
je clearleds
cmp al, '.'
je decimal
jmp exit_analyze_key

;if it is >
clearleds:

mov BX, 0H
mov DS:LED_displays[BX], 0H
inc BX
mov DS:LED_displays[BX], 0H
inc BX
mov DS:LED_displays[BX], 0H
inc BX
mov DS:LED_displays[BX], 0H
inc BX
mov DS:LED_displays[BX], 0H
inc BX
mov DS:LED_displays[BX], 0H
mov DS:empty_led_counter, 06H
jmp exit_analyze_key

decimal:

mov bx,  05H
mov cl, DS:LED_displays[BX]
or cl, 80H ;mask to make the dp place 1
mov DS:LED_displays[BX], cl
jmp exit_analyze_key



exit_analyze_key:
;mov al, 'E'
;call far ptr print_char

pop dx
pop cx
pop bx
ret


analyze_key endp

CODE_SEG        ENDS
END
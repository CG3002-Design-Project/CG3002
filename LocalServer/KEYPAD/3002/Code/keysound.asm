$MOD186
$ep
$include(80188.inc)
NAME keysound
;combines keypad and sound
;use with keycomb.asm
; =========================================================================

public	serial_rec_action, timer2_action , timer1_action
extrn	print_char:far, print_2hex:far, iodefine:far
extrn   set_timer1:far, set_timer2:far, keypad:far

STACK_SEG	SEGMENT
		DB	256 DUP(?)
	TOS	LABEL	WORD
STACK_SEG	ENDS


DATA_SEG	SEGMENT
	TIMER0_MESS	DB	10,13,'TIMER0 INTERRUPT    '
	TIMER1_MESS	DB	10,13,'TIMER1 INTERRUPT    '
	TIMER2_MESS	DB	10,13,'TIMER2 INTERRUPT    '
	T_COUNT		DB	2FH
	T_COUNT_SET	DB	2FH
	REC_MESS	DB	10,13,'Period of timer0 =     '
 
  ;===========LED stuff
 LED_displays DB 80H,80H,80H,80H,80H,80H
	
	
	LED_COUNT DB 00H
	
	;BCD                DB        7EH,30H,6DH,79H,33H,5BH,5FH,70H,7FH,7BH
	CATHODES            DB         5FH,	50H, 6DH, 79H, 72H, 3BH, 3FH, 51H, 7FH, 7BH, 80H
	DISPLAY_NUM        DW        1234H
	
	empty_led_counter DB 06H
;================LED stuff ends
  
  ;============= New Sound Start
	sound_q_head	DW 0H
	sound_q_end		DW 0H
	
	sound_start_1 	DW 0, 0, 0, 0, 0
	sound_end_1 	DW 0F6BH, 0F6BH, 0F6BH, 0F6BH, 0F6BH
	
	;=============New sound end
	sound_queue_head DW 0d
	sound_queue_tail DW 255d
	
	
	SOUND_REM			DW	0
	SOUND_SIZE dw 00h
	;my_current_sound dd 00h
	
	my_sound_index	dw 0 ; specifies index ( i.e can be 0,1,2,3,4,5,6,7,8,9,10) , till sound "ten"
	
	;starting address of sounds till "ten" 
	my_sound_word_start DW	0, 4713, 8481, 11945, 15315, 18317, 21615, 26121, 30013, 31809,36107
	
	; number of words for souund till "ten"
	;count starting from 0
	my_sound_word_size dw 4713, 3768, 3464, 3371, 3002, 3297, 4506, 3893, 1796, 4298,3003
	
	CURRENT_SOUND DW 0H
  
  ;============= Sound End
  
DATA_SEG	ENDS

EXTRA_SEG SEGMENT
EXTRA_SEG ENDS



CODE_SEG	SEGMENT
PUBLIC		START

ASSUME	CS:CODE_SEG, SS:STACK_SEG, DS:DATA_SEG , ES:EXTRA_SEG

START:
	CLI
;initialize stack area
	MOV	AX,STACK_SEG		
	MOV	SS,AX
	MOV	SP,TOS

	MOV BX, DATA_SEG
	MOV DS, BX
	
	
; Initialize the on-chip pheripherals
	CALL	FAR PTR	IODEFINE
	
;Initialisation for Sound done in 80188.inc file
	
; ^^^^^^^^^^^^^^^^^  Start of User Main Routine  ^^^^^^^^^^^^^^^^^^
	
; Initialize MPCS to MAP peripheral to IO address
         MOV DX, MPCS
         MOV AX, 2083H ; ;0010 0000 1000 0110; MMCS block size is 20H or 256KB, PCS programmed for I/O operation 
         OUT DX, AL
		 
; Initialize Middle Memory chip select
		MOV 	DX, MMCS	; 
		MOV 	AX, 4003H	;0100 0000 0000 0110 ;no ready, 2 waits		
		OUT 	DX, AX
	
	;call far ptr set_timer2
	call far ptr set_timer1
	STI
	
	;set the value of sound_q_head and sound_q_end to some test values and run code

NEXT: 	
	call far ptr keypad	
		
JMP NEXT

; ^^^^^^^^^^^^^^^ End of User main routine ^^^^^^^^^^^^^^^^^^^^^^^^^

	
;------------------------------------------------------------------------------	
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
		
		
		POP	CX
		POP	BX
		POP	DS
		POP AX
		RET
TIMER2_ACTION	ENDP

TIMER1_ACTION	PROC	FAR
		PUSH	AX
		PUSH	DS
		PUSH	BX
		PUSH	CX
		
		
		MOV	AX,DATA_SEG
		MOV	DS,AX
	
		MOV AX, DS:sound_q_head
		MOV CX, DS:sound_q_end
		CMP AX, CX
		JE reset_pointers
		
		
		XOR AX, AX
		xor bx,bx
		mov ax, 5000h ;address of Middle Memory active? This should activate only middle memory block 1
		mov es, ax
		mov di, DS:sound_q_head
			
		mov al, es:[di]
		
		;call far ptr print_2hex
		
		;mov al, es:[di]
		mov dx, 0200h ;address of PCS4
		out dx,al

		inc DS:sound_q_head
		jmp exit_timer1

reset_pointers:
	mov ax, 0d
	mov ds:sound_q_head, ax	
		
		
exit_timer1:	
		POP	CX
		POP	BX
		POP	DS
		POP AX
		RET
		
TIMER1_ACTION	ENDP


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
xor bx, bx
mov bl, al ;bl now has the number


;AUDIO PART
;currently al has the number
mov AX, DS:sound_start_1[BX]
mov DS:sound_q_head, AX

mov AX, DS:sound_end_1[BX]
mov DS:sound_q_end, AX


;LED PART
;call far ptr print_char
;xor bx, bx
;mov bl, al ;bl now has the number

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



CODE_SEG	ENDS
END

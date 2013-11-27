$MOD186
$EP
NAME LCDANKHH

public	serial_rec_action, timer2_action, topLine ; can be called by external referencs
extrn	print_char:far, print_2hex:far, iodefine:far
extrn   set_timer2:far
STACK_SEG	SEGMENT
		DB	256 DUP(?)
	TOS	LABEL	WORD
STACK_SEG	ENDS

DATA_SEG	SEGMENT
	TIMER0_MESS	DB	10,13,'TIMER2 INTERRUPT    '
	T_COUNT		DB	2FH ; 47 decimal
	T_COUNT_SET	DB	2FH ;47 decimal
	REC_MESS	DB	10,13,'Period of timer0 =     '
	zerotoeleven    DB  '#','0','*','#','0','*','9','8','7','9','8','7'
	twelvetoend		DB	'6','5','4','6','5','4','3','2','1','3','2','1'
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
    call set_timer2
    STI
MOV	BX,DATA_SEG		;initialize data segment register
	MOV	DS,BX

	
	PORTA	EQU 	0080H
	PORTB 	EQU 	0081H
	PORTC 	EQU 	0082H
	CWR 	EQU 	0083H
	
	MOV AL, 80H  ; PORT A, B, C - output       
	MOV DX, CWR
	OUT DX, AL 
	

	
	call far ptr initLCD
	
	; xor bh, bh
	; mov bl, '1'
	; call FAR PTR topLine
	; mov bl, '2'
	; call FAR PTR topLine
	; mov bl, '3'
	; call FAR PTR topLine
	; mov bl, '4'
	; call FAR PTR topLine
	; mov bl, '5'
	; call FAR PTR topLine
	
	;stay: loop stay 
	;jmp next
	
waiting:
		jmp waiting
; ^^^^^^^^^^^^^^^ End of User main routine ^^^^^^^^^^^^^^^^^^^^^^^^^


initLCD PROC FAR

	;Store and set up registers
	push	ax 						;10cyc
	push    bx
	push	cx 						;10cyc
	push	dx 						;10cyc
	
;Time Waste 15ms - need 24*10^4 cycles 
	xor cx, cx
	mov cx, 13F5h
Time15ms: 
	nop ;3cycles each
	nop
	nop
	nop
	nop ;3cycles each
	nop
	nop
	nop
	nop ;3cycles each
	nop
	
	dec cx ;3 cycles
	cmp cx, 0h ;10 cycles
	jne Time15ms ;13 when taken, 4 not taken
;delay ends	

	call FAR PTR ENABLE
	xor al, al
	mov al, 00111000b   ;00111100b(original) what it is now: 8 bit bus, 2 line display
	mov dx, PORTB
	out dx, al ;---------------------first function set, before need > 40ms
	call FAR PTR DISABLE
	
	xor cx, cx
	mov cx, 6A7h
Time5ms: 
	nop ;3cycles each
	nop
	nop
	nop
	nop ;3cycles each
	nop
	nop
	nop
	nop ;3cycles each
	nop
	
	dec cx ;3 cycles
	cmp cx, 0h ;10 cycles
	jne Time5ms ;13 when taken, 4 not taken
;delay ends		

	call FAR PTR ENABLE
	;F Function Set
	xor al, al
	mov al, 00111000b
	mov dx, PORTB
	out dx, al ;---------------------first function set, before need > 4.1ms
	call FAR PTR DISABLE

	xor cx, cx
	mov cx, 22h
Time100us: 
	nop ;3cycles each
	nop
	nop
	nop
	nop ;3cycles each
	nop
	nop
	nop
	nop ;3cycles each
	nop
	
	dec cx ;3 cycles
	cmp cx, 0h ;10 cycles
	jne Time100us ;13 when taken, 4 not taken
;delay ends			
	
	;function set
	call FAR PTR ENABLE
	;F Function Set
	xor al, al
	mov al, 00111000b
	mov dx, PORTB
	out dx, al ;---------------------first function set, before need > 100us
	call FAR PTR DISABLE
	
	call FAR PTR ENABLE
	;F Function Set -- FINAL ONE
	xor al, al
	mov al, 00111000b
	mov dx, PORTB
	out dx, al ;
	call FAR PTR DISABLE
	
	;DISPLAY OFF
	call FAR PTR ENABLE
	;D Display Off
	xor al, al
	mov al, 00001000b
	mov dx, PORTB
	out dx, al
	call FAR PTR DISABLE
	
	;DISPLAY CLEAR
	call FAR PTR ENABLE
	xor al, al
	mov al, 00000001b
	mov dx, PORTB
	out dx, al
	call FAR PTR DISABLE
	
	;ENTRY MODE SET
	call FAR PTR ENABLE
	xor al, al
	mov al, 00000110b
	mov dx, PORTB ; Shifts to the right, whole data does not shift
	out dx, al
	call FAR PTR DISABLE
	
	;SET DISPLAY ON CURSOR ON AND BLINK ON
	call FAR PTR ENABLE
	xor al, al
	mov al, 00001111b
	mov dx, PORTB ; Shifts to the right, whole data does not shift
	out dx, al
	call FAR PTR DISABLE
	
	
	;H set DDRAM addr-- makes DDRAM data available from CPU
	call FAR PTR ENABLE
	mov al, 00H ; 40H --we only display on line2 first
	mov dx, PORTB
	out dx, al	
	NOP
	NOP
	call FAR PTR DISABLE
		
	;INITIALIZATION ENDS HERE	
	pop	dx 						;10cyc
	pop	cx 						;10cyc
	pop bx
	pop	ax 						;10cyc
	ret
initLCD	ENDP


;character expected in bl
topLine proc far
	
	
	push	ax 						;10cyc
	push    bx
	push	cx 						;10cyc
	push	dx 	

	mov 	bl, al   ; because topLine is defined for bl
	;call far ptr initLCD

	; WRITE DATA TO RAM --------------------------------------------------------
	; RS high R/W low, -- writing data to RAM
	xor al, al
	mov al, 00000101b ;enable and R/S high
	mov dx, PORTC
	out dx, al
	
	;J Write to Ram
	xor al, al
	mov al, BL
	mov dx, PORTB
	out dx, al
	
	xor al,al
	mov al, 00000001b ;enable low R/S high
	mov dx, PortC
	out dx, al
	
	call FAR PTR DELAY
	;;stay: loop stay
	pop	dx 						;10cyc
	pop	cx 						;10cyc
	pop bx
	pop	ax 						;10cyc
	ret
topLine	ENDP


bottomLine proc far
	
	push	ax 						;10cyc
	push    bx
	push	cx 						;10cyc
	push	dx 	

	mov 	bl, al   ; because topLine is defined for bl
	
	
	;############################################################
	
	xor al,al
	mov al, 00000110b ;enable high
	mov dx, PortC
	out dx, al
	
	mov al, 11000000b ; busy flag set, line2
	mov dx, PORTB
	out dx, al	
	NOP
	NOP
	;call FAR PTR DISABLE
	xor al,al
	mov al, 00000010b ;disable high
	mov dx, PortC
	out dx, al
	
	call FAR PTR DELAY
	;H set DDRAM addr-- makes DDRAM data available from CPU
	call FAR PTR ENABLE
	mov al, 0C0H ; 0C0H --we only display on line2 first
	mov dx, PORTB
	out dx, al	
	NOP
	NOP
	call FAR PTR DISABLE
	
	;busy set
	xor al,al
	mov al, 00000110b ;enable high
	mov dx, PortC
	out dx, al
	
	mov al, 11000000b ; busy falg set, line2
	mov dx, PORTB
	out dx, al	
	NOP
	NOP
	;call FAR PTR DISABLE
	xor al,al
	mov al, 00000010b ;enable high
	mov dx, PortC
	out dx, al

	;######################################################################
	
	; WRITE DATA TO RAM --------------------------------------------------------
	; RS high R/W low, -- writing data to RAM
	xor al, al
	mov al, 00000101b ;enable and R/S high
	mov dx, PORTC
	out dx, al
	
	;J Write to Ram
	xor al, al
	mov al, BL
	mov dx, PORTB
	out dx, al
	
	xor al,al
	mov al, 00000001b ;enable low R/S high
	mov dx, PortC
	out dx, al
	
	call FAR PTR DELAY
	;;stay: loop stay
	pop	dx 						;10cyc
	pop	cx 						;10cyc
	pop bx
	pop	ax 						;10cyc
	ret
bottomLine	ENDP



; bottomLine proc far

	; push	ax 						;10cyc
	; push	cx 						;10cyc
	; push	dx 	
	; ;SET DDRAM ADDRESS ------------------------------------------
	; call FAR PTR ENABLE
	
	; ;H set DDRAM addr-- makes DDRAM data available from CPU
	; mov al, 1100000b ; 40H --we only display on line2 first
	; mov dx, PORTB
	; out dx, al	
	; call FAR PTR DISABLE
	
	; ; WRITE DATA TO RAM --------------------------------------------------------
	
	; ; RS high R/W low, -- writing data to RAM
	; xor al, al
	; mov al, 00000101b ;enable and R/S high
	; mov dx, PORTC
	; out dx, al
	
	; ;J Write to Ram
	; xor al, al
	; mov al, BL
	; mov dx, PORTB
	; out dx, al
	
	; xor al,al
	; mov al, 00000001b ;enable low R/S high
	; mov dx, PortC
	; out dx, al
	
	; ;----print E-----

	; ;----print G----- 
	
	
	; ; READ DATA FROM RAM ----------------------------------------------------------
	
	; xor al,al
	; mov al, 00000111b ;enable, RS and R/W high
	; mov dx, PortC
	; out dx, al
	
	; ; DISPLAY DATA -----------------------------------------------------------------

	; ;mov al, 00000100b ;enable high
	; ;mov dx, PORTC
	; ;out dx, al
	
	; ;D Display On
	; mov al, 00001100b
	; mov dx, PORTB
	; out dx, al
	
	; mov al, 00000011b ;enable low
	; mov dx, PORTC
	; out dx, al	;------------------------------------------------------------------------------
	

	; pop	dx 						;10cyc
	; pop	cx 						;10cyc
	; pop	ax 						;10cyc
	; ret
; bottomLine	ENDP


ENABLE PROC FAR

push AX
push BX
push CX
push DX

xor al,al
	mov al, 00000100b ;enable high
	mov dx, PortC
	out dx, al


pop	dx 						;10cyc
pop	cx 						;10cyc
pop	bx 						;10cyc
pop	ax 						;10cyc

ENABLE ENDP

DISABLE PROC FAR

push AX
push BX
push CX
push DX

xor al,al
	mov al, 00000000b ;enable high
	mov dx, PortC
	out dx, al


pop	dx 						;10cyc
pop	cx 						;10cyc
pop	bx 						;10cyc
pop	ax 						;10cyc

DISABLE ENDP


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

SERIAL_REC_ACTION	PROC	FAR  ; keyboard interfacing happening here
		PUSH	CX
		PUSH 	BX
		PUSH	DS
		
		MOV	BX,DATA_SEG		;initialize data segment register
		MOV	DS,BX ; DS points to data segment
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

;generates a delay of about 560ms
CODE_SEG	ENDS
END
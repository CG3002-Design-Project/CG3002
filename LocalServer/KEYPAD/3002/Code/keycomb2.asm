$mod186
$EP
NAME KEYCOMB2
;---------------------------------------------------------------------------

public	keypad
extrn print_char:far, print_2hex:far

$include(80188.inc)

KEYPAD_SEG SEGMENT

	zerotoeleven    DB  '#',0H,'*','>','0','*',09H,08H,07H,'9','8','7'
	twelvetoend		DB	06H,05H,04H,'6','5','4',03H,02H,01H,'3','2','1'
KEYPAD_SEG ENDS

KEYPAD_ROUTINE	SEGMENT
ASSUME CS:KEYPAD_ROUTINE

PORTA	EQU 	0080H
PORTB 	EQU 	0081H
PORTC 	EQU 	0082H
CWR 	EQU 	0083H

keypad proc far
	PUSH    DX
	PUSH	CX
	PUSH 	BX
	PUSH	AX
	
;set 8255 mode
	MOV AL, 89H       ;PA, PB output, PC input
	MOV DX, CWR
	OUT DX, AL        ;send the control word
;map to keypad segment
	mov bx, KEYPAD_SEG
	mov ds, bx

;ground row 0 to start with	
	MOV CL, 11111110b ;Row output to ground from PB0
	MOV CH, 0H	;set row counter
	
startcycle:		
	;CL has the row grounding output
	MOV AL,CL
	MOV DX, PORTB	;port B address to DX; 
	OUT DX, AL	;ground one of the rows
	MOV DX, PORTC	;port C address to DX  
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
	CALL FAR PTR PRINT_CHAR
	;call far ptr analyze_key
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
	je cycle_done
	
	rol CL, 01H
	jmp startcycle
	
cycle_done:
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


; ;character/number for keypress is in AL
; analyze_key proc far
; push bx
; push cx
; push dx

; ;need to access data_segment
; mov 

; ;check if number has been pressed
; cmp al, 09H
; jg action_key ;if not number, it is an action key

; ;if it's a number-
; mov cl, DS:LED_storage_count
; cmp cl, 00H
; jne switch_LEDs
; ;count is 0, then-
; mov bx, 03H
; mov DS:LED_displays[bx], AL ;mov that number into led3
; inc DS:LED_storage_count
; jmp exit_analyze_key

; switch_LEDs:
; xor cx, cx

; ;other LEDs shifted
; mov bx, 01H 
; mov cl, DS:LED_displays[BX]
; mov bx, 00H
; mov DS:LED_displays[BX], cl

; mov bx, 02H 
; mov cl, DS:LED_displays[BX]
; mov bx, 01H
; mov DS:LED_displays[BX], cl

; mov bx, 03H 
; mov cl, DS:LED_displays[BX]
; mov bx, 02H
; mov DS:LED_displays[BX], cl

; ;new number added to led3
; mov bx, 03H
; mov DS:LED_displays[bx], AL ;mov that number into led3
; inc DS:LED_storage_count
; jmp exit_analyze_key

; action_key:


; exit_analyze_key:

; pop dx
; pop cx
; pop bx
; ret


; analyze_key endp



KEYPAD_ROUTINE	ENDS

END

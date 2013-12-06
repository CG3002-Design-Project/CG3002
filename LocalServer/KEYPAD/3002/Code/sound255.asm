$MOD186
$ep
$include(80188.inc)
NAME soundtry
; =========================================================================

public	serial_rec_action, timer2_action , timer1_action
extrn	print_char:far, print_2hex:far, iodefine:far
extrn   set_timer1:far, set_timer2:far

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
 
 
  
  ;============= Sound Start
  
	sound_queue_head DW 0d
	sound_queue_tail DW 255d
	
	
	sound_q_head	DW 0d
	sound_q_end	DW 12981H
	
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
		mov ax, 4000h ;address of Middle Memory active? This should activate only middle memory block 1
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



;Sound code starts here
PUT_ONE_SOUND PROC FAR
	PUSH DS
	PUSH BX
	PUSH CX
	PUSH AX
	; insert which sound here in my_sound_index
	; MOV AX,5
	; MOV DS:CURRENT_SOUND,AX
	 MOV AX,DS:CURRENT_SOUND
	 MOV DS:my_sound_index, AX
		

	CMP AX,3
	JE threes	
	cmp AX, 8
	JE eight
	cmp AX, 6
	JE sixs
	cmp AX, 9
	JE nine
	cmp AX, 7
	JE Seven
	
	jmp normal_fetch
	threes:
	jmp three
	sixs:
	jmp six
	
	normal_fetch:
	 ;set head
		XOR AX,AX
		 XOR BX, BX
		 XOR CX,CX
		 MOV BX,offset my_sound_word_start
		 MOV AX,DS:my_sound_index
		 ADD DS:my_sound_index , AX
		 ADD BX,DS:my_sound_index
		 MOV AX ,[BX]
		MOV WORD PTR DS:SOUND_QUEUE_HEAD ,AX
	
	;set tail
		 XOR AX,AX
		 XOR BX, BX
		 XOR CX,CX
	
		 MOV BX,offset my_sound_word_size
		 MOV AX,DS:my_sound_index
		 ADD DS:my_sound_index , AX
		 ADD BX,DS:my_sound_index
		 MOV AX, [BX]
		 MOV WORD PTR DS:SOUND_SIZE , AX
		 MOV AX , DS:SOUND_SIZE
		ADD AX, DS:SOUND_QUEUE_HEAD
		 MOV word ptr DS:SOUND_QUEUE_TAIL , AX
		 
		 JMP endd
	seven :	 

		MOV WORD PTR DS:SOUND_QUEUE_HEAD ,6609h
		MOV AX,0f35h
		ADD AX, DS:SOUND_QUEUE_HEAD
		 MOV word ptr DS:SOUND_QUEUE_TAIL , AX
	jmp endd
	
	eight:
		MOV WORD PTR DS:SOUND_QUEUE_HEAD ,753eh
		MOV AX,0703h
		ADD AX, DS:SOUND_QUEUE_HEAD
		 MOV word ptr DS:SOUND_QUEUE_TAIL , AX
	jmp endd
	
	nine:
		MOV WORD PTR DS:SOUND_QUEUE_HEAD ,7c41h
		MOV AX,10cAh
		ADD AX, DS:SOUND_QUEUE_HEAD
		 MOV word ptr DS:SOUND_QUEUE_TAIL , AX
	jmp endd
	
	six:
		MOV WORD PTR DS:SOUND_QUEUE_HEAD ,21615
		MOV AX,4506
		ADD AX, DS:SOUND_QUEUE_HEAD
		 MOV word ptr DS:SOUND_QUEUE_TAIL , AX
	jmp endd

	three:	 
		MOV WORD PTR DS:SOUND_QUEUE_HEAD ,2ea9h	
		MOV AX,0d2ah
		ADD AX, DS:SOUND_QUEUE_HEAD
		 MOV word ptr DS:SOUND_QUEUE_TAIL , AX	
	endd:
	POP AX
	POP CX
	POP BX
	POP DS
	RET
PUT_ONE_SOUND ENDP

CODE_SEG	ENDS
END

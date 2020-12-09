	.data
	.balign 4
Intro: .asciz "Raspberry Pi wiringPi blink test\n"
ErrMsg: .asciz "Setup didn't work... Aborting...\n"
pin: .int 7
i: .int 0
delayMs: .int 250
OUTPUT = 1

	.text
	.global main
	.extern printf
	.extern wiringPiSetup
	.extern delay
	.extern digitalWrite
	.extern pinMode

main: PUSH {ip, lr}

	BL wiringPiSetup
	MOV R1, #-1
	CMP R0, R1
	BNE init


@ pinMode(pin, OUTPUT);
init:
	LDR R0, =pin
	LDR R0, [R0]
	MOV R1, #OUTPUT
	BL pinMode

@	digitalWrite( pin, 1);
	LDR R0, =pin
	LDR R0, [R0]
	MOV R1, #1
	BL digitalWrite

done:
	POP {ip, pc}

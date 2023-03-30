.data

newline: .asciiz "\n"
buffer: .space 22
comma: .asciiz ","

.text

returnfunc:
	jr $ra

str_to_int:
	lb $a0, 0($t7)
	beq $a0, 10, returnfunc
	andi $a0, $a0, 0x0F

	multu $t1, $a1
	mflo $t1
	mfhi $t3
	multu $t0, $a1
	mflo $t2
	add $t0, $t2, $t3

	move $t2, $t1
	addu $t1, $t1, $a0
	nor $a0, $a0, $zero
	sltu $a0, $a0, $t2
	add $t0, $t0, $a0

	addi $t7, $t7, 1
	j str_to_int

int_to_str:
	or $t7, $t0, $t1
	beqz $t7, returnfunc

	divu $t1, $a1
	mflo $t1
	mfhi $s0

	divu $t0, $a1
	mflo $t0
	mfhi $s1

	mult $s1, $a2
	mflo $s4

	add $s4, $s4, $s0
	div $s4, $a1
	mflo $s4
	mfhi $s5
	addu $t1, $t1, $s4

	addiu $sp, $sp, -1
	addi $s5, $s5, 0x30
	sb $s5, 0($sp)

	multu $s1, $a3
	mflo $s0
	mfhi $s1
	addu $t0, $t0, $s1

	move $t2, $t1
	addu $t1, $t1, $s0
	nor $s0, $s0, $zero
	sltu $s0, $s0, $t2
	add $t0, $t0, $s0

	j int_to_str

lpa:
	srl $s1, $s1, 1
	andi $t7, $s0, 1
	sll $t7, $t7, 31
	srl $s0, $s0, 1
	addu $s1, $s1, $t7
	addi $t6, $t6, 1
loopa:
	andi $t7, $s1, 1
	beq $t7, 0, lpa
	sw $t6, ($sp)
	jr $ra

lpm:
	srl $s3, $s3, 1
	andi $t7, $s2, 1
	sll $t7, $t7, 31
	srl $s2, $s2, 1
	addu $s3, $s3, $t7
	addi $t6, $t6, 1
loopm:
	andi $t7, $s3, 1
	beq $t7, 0, lpm
	sw $t6, 4($sp)
	jr $ra

base1:						#a is 1
	bne $s0, 0, basereturn1
	li $s4, 0
	li $s5, 1
	li $s6, 0
	li $s7, 0
	j casesdone

base2:						#m is 1
	bne $s2, 0, basereturn2
	li $s4, 0
	li $s5, 1
	seq $a0, $s1, 0 		#a-1
	addiu $s7, $s1, -1
	subu $s6, $s0, $a0
	j casesdone

loop:
	addi $sp, $sp, -28
	sw $ra, 24($sp)			#previous ra
	li $t6, 0
	jal loopm				#for even m
	li $t6, 0
	jal loopa				#for even a

	sw $s2, 8($sp)			#m (upper bits)
	sw $s3, 12($sp)			#m (lower bits)
	sw $s0, 16($sp)			#a (upper bits)
	sw $s1, 20($sp)			#a (lower bits)
	beq $s1, 1, base1
basereturn1:
	beq $s3, 1, base2
basereturn2:				
	sltu $a0, $s0, $s2
	sltu $a1, $s1, $s3
	sll $a3, $a0, 1
	sltu $a2, $s2, $s0
	add $a3, $a3, $a1
	srl $a3, $a3, $a2
	bne $a3, 0, case2
case1:						#a>m
	subu $s0, $s0, $s2
	subu $s1, $s1, $s3
	subu $s0, $s0, $a1
	jal loop

	nor $a0, $s5, $zero
	addu $s6, $s6, $s4
	sltu $a0, $a0, $s7
	addu $s7, $s7, $s5
	addu $s6, $s6, $a0

	j casesdone
case2:						#a<m
	sltu $a1, $s3, $s1
	subu $s2, $s2, $s0
	subu $s3, $s3, $s1
	subu $s2, $s2, $a1
	jal loop
	addu $s0, $s0, $s1

	nor $a0, $s7, $zero
	addu $s4, $s4, $s6
	sltu $a0, $a0, $s5
	addu $s5, $s5, $s7
	addu $s4, $s4, $a0

casesdone:
	lw $s2, 8($sp)			#m (upper bits)
	lw $s3, 12($sp)			#m (lower bits)
	lw $s0, 16($sp)			#a (upper bits)
	lw $s1, 20($sp)			#a (lower bits)

	lw $t7, 4($sp)
	bne $t7, 0, sublp2
	lw $t7, ($sp)
	beq $t7, 0, continue
sublp1:
	srl $s3, $s3, 1
	andi $a0, $s2, 1
	sll $a0, $a0, 31
	srl $s2, $s2, 1
	addu $s3, $s3, $a0
	seq $a0, $s3, -1
	addiu $s3, $s3, 1
	addu $s2, $s2, $a0
subloop1:					#When a was even
	addi $t7, $t7, -1
	andi $t6, $s5, 1

	srl $s5, $s5, 1
	andi $a0, $s4, 1
	sll $a0, $a0, 31
	srl $s4, $s4, 1
	addu $s5, $s5, $a0

	beq $t6, 0, subloop1case2
subloop1case1:
	nor $a0, $s1, $zero		#addu $s1, $s1, $a0
	sltu $a0, $a0, $s7
	addu $s6, $s6, $s0
	addu $s7, $s7, $s1
	addu $s6, $s6, $a0
	
	nor $a0, $s3, $zero		#addu $s0, $s0, $a1
	sltu $a0, $a0, $s5
	addu $s4, $s4, $s2
	addu $s5, $s5, $s3
	addu $s4, $s4, $a0

	sll $s0, $s0, 1
	srl $a0, $s1, 31
	sll $s1, $s1, 1
	addu $s0, $s0, $a0

	bne $t7, 0, subloop1
	j continue
subloop1case2:
	sll $s0, $s0, 1
	srl $a0, $s1, 31
	sll $s1, $s1, 1
	addu $s0, $s0, $a0

	bne $t7, 0, subloop1
	j continue

sublp2:
	srl $s1, $s1, 1
	andi $a0, $s0, 1
	sll $a0, $a0, 31
	srl $s0, $s0, 1
	addu $s1, $s1, $a0
	seq $a0, $s1, -1
	addiu $s1, $s1, 1
	addu $s0, $s0, $a0
subloop2:					#When m was even
	addi $t7, $t7, -1
	andi $t6, $s7, 1

	srl $s7, $s7, 1
	andi $a0, $s6, 1
	sll $a0, $a0, 31
	srl $s6, $s6, 1
	addu $s7, $s7, $a0

	beq $t6, 0, subloop2case2
subloop2case1:
	nor $a0, $s1, $zero		#addu $s1, $s1, $a0
	sltu $a0, $a0, $s7
	addu $s6, $s6, $s0
	addu $s7, $s7, $s1
	addu $s6, $s6, $a0
	
	nor $a0, $s3, $zero		#addu $s0, $s0, $a1
	sltu $a0, $a0, $s5
	addu $s4, $s4, $s2
	addu $s5, $s5, $s3
	addu $s4, $s4, $a0

	sll $s2, $s2, 1
	srl $a0, $s3, 31
	sll $s3, $s3, 1
	addu $s2, $s2, $a0

	bne $t7, 0, subloop2
	j continue
subloop2case2:
	sll $s2, $s2, 1
	srl $a0, $s3, 31
	sll $s3, $s3, 1
	addu $s2, $s2, $a0
	
	bne $t7, 0, subloop2
continue:
	lw $ra, 24($sp)
	addi $sp, $sp, 28
	jr $ra
	
main:
	li $v0, 8
	la $a0, buffer
	li $a1, 22
	syscall
	li $t0, 0
	li $t1, 0
	la $t7, buffer
	li $a1, 10				#For I/O
	jal str_to_int
	move $s0, $t0			#a (upper 32 bits)
	move $s1, $t1			#a (lower 32 bits)

	li $v0, 8
	la $a0, buffer
	li $a1, 22
	syscall
	li $t0, 0
	li $t1, 0
	la $t7, buffer
	li $a1, 10				#For I/O
	jal str_to_int
	move $s2, $t0			#m (upper 32 bits)
	move $s3, $t1			#m (lower 32 bits)

	jal loop

	move $t0, $s4
	move $t1, $s5

	li $a1, 10				#For I/O
	li $a2, 6				#For O
	li $a3, 0x1999
	sll $a3, $a3, 8
	addi $a3, $a3, 0x99
	sll $a3, $a3, 8
	addi $a3, $a3, 0x99

	la $t7, buffer
	addi $sp, $sp, 0
	sb $zero, 0($sp)
	jal int_to_str

	li $v0, 4
	move $a0, $sp
	syscall

	li $v0, 4
	la $a0, newline
	syscall

	li $v0, 10
    syscall

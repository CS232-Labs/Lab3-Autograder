.data 

aprompt:
    .asciiz "Enter a:​ "

mprompt:
    .asciiz "Enter m:​ "

cprompt:
    .asciiz "Wish to continue?:​ "

star:
    .asciiz "*"

mod:
    .asciiz " = 1 (mod "

ending:
    .asciiz ")\n"

nline:
    .asciiz "\n"

Y:
    .byte 'Y'

.text

invMod:
    addi $sp,$sp,-12
    sw $ra,8($sp) # ra to stack
    sw $a1,4($sp) # a to stack
    sw $a2,0($sp)  # m to stack

    jal gcdEx
    
    lw $ra,8($sp) # ra to stack
    lw $a1,4($sp) # a to stack
    lw $a2,0($sp)  # m to stack
    
    slt $t1,$0,$t0
    bne $t1,$0,Ret
    div $t0,$a2
    mfhi $v0
    add $v0,$v0,$a2
    div $v0,$a2
    mfhi $v0
    jr $ra

Ret:
    div $t0,$a2
    mfhi $v0
    jr $ra
    


gcdEx:
    addi $sp,$sp,-20
    sw $ra,16($sp) # ra to stack
    sw $a1,12($sp) # a to stack
    sw $a2,8($sp)  # m to stack
    sw $t0,4($sp)  # x to stack
    sw $t1,0($sp)  # y to stack
    
    bne $a1,$0,L2
    
    li $t0,0
    li $t1,1
    move $v0,$a2
    
    addi $sp,$sp,20
    jr $ra

L2:
    
    div $a2,$a1
    move $a2,$a1 # b = a
    mfhi $a1 #a = b%a

    jal gcdEx
    
    lw $ra,16($sp)
    lw $a1,12($sp)
    lw $a2,8($sp)
    
    div $a2,$a1
    mflo $t2
    mul $t2,$t2,$t0
    move $t3,$t0
    sub $t0,$t1,$t2
    
    move $t1,$t3
    
    addi $sp,$sp,20
    jr $ra

main:

    # li $v0, 4
    # la $a0, aprompt
    # syscall

    li $v0, 5
    syscall
    move $a1, $v0

    # li $v0, 4
    # la $a0, mprompt
    # syscall

    li $v0, 5
    syscall
    move $a2,$v0

    jal invMod
    move $a3,$v0

    # li $v0, 1
    # move $a0, $a1
    # syscall
    
    # li $v0, 4
    # la $a0, star
    # syscall

    li $v0, 1
    move $a0, $a3
    syscall

    # li $v0, 4
    # la $a0, mod
    # syscall

    # li $v0, 1
    # move $a0, $a2
    # syscall
    
    # li $v0, 4
    # la $a0, ending
    # syscall

    # li $v0, 4
    # la $a0, cprompt
    # syscall

    # li $v0, 12
    # syscall
    # move $t0,$v0

    # lb $t1, Y
    # bne $t0,$t1,exit
    
    li $v0, 4
    la $a0, nline
    syscall

exit:

    li $v0 10 # exit
    syscall

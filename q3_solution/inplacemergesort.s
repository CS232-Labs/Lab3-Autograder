.data

arr: .space 204 # 50*4+4

newline: .asciiz "\n"
# sizestring: .asciiz "Enter size of array to sort: "
# arraystring: .asciiz "Enter the array elements: "
outputstring: .asciiz "The sorted array is: "

.text

merge:
    lw $a1, 4($sp)                      # Restore left
    lw $a2, 8($sp)                      # Restore right 

    add $a3, $a1, $a2                   # a3 = mid+1
    sra $a3, $a3, 1
    addi $a3, $a3, 1

    addi $t0, $a2, 1                    # Right bound= right+1

    move $t1, $a1                       # idx1 = left
    move $t2, $a3                       # idx2 = mid+1
    move $t3, $a1                       # idx3 = left

checkbounds:
    slt $t4, $t1, $a3                   # t4 == 1 if idx1 < mid+1
    slt $t5, $t2, $t0                   # t5 == 1 if idx2 < right+1

    add $t6, $t4, $t5                   

    beq $t6, 2, whilewithtwo            # If both are true, compare
    beq $t4, 1, addfirsthalf            # If first one true, go to first part
    beq $t5, 1, addsecondhalf           # If second one true, go to second part

    move $s6, $a1
    beq $zero, $zero, copyback          # copyback the values to original array

copyback:
    beq $s6, $t0, copydone

    sll $s6, $s6, 2
    lw $t8, arr($s6)
    div $t8, $s7
    mflo $t8
    sw $t8, arr($s6)                    # copy back to arr from out
    sra $s6, $s6, 2

    addi $s6, $s6, 1
    j copyback

copydone:
    jr $ra

whilewithtwo:
    # Compare arr($t1), arr($t2)
    sll $t1, $t1, 2
    lw $s1, arr($t1)
    div $s1, $s7
    mfhi $s1                            # takes original arr(t1) value
    sra $t1, $t1, 2

    sll $t2, $t2, 2
    lw $s2, arr($t2)
    div $s2, $s7
    mfhi $s2                            # takes original arr(t2) value
    sra $t2, $t2, 2

    slt $s3, $s1, $s2                   # arr(idx1) < arr(idx2)

    beq $s3, 0, addsecondhalf
    beq $s3, 1, addfirsthalf

addfirsthalf:
    sll $t1, $t1, 2
    lw $s1, arr($t1)
    div $s1, $s7
    mfhi $s1                            # takes original arr(t1) value
    sra $t1, $t1, 2

    sll $t3, $t3, 2
    lw $s4, arr($t3)
    mul $s5, $s1, $s7 
    add $s4, $s4, $s5
    sw $s4, arr($t3)                    # store arr(t3)=arr(t3) + $s7*arr(t1)
    sra $t3, $t3, 2

    addi $t1, $t1, 1
    addi $t3, $t3, 1

    beq $zero, $zero, checkbounds

addsecondhalf:
    sll $t2, $t2, 2
    lw $s2, arr($t2)
    div $s2, $s7
    mfhi $s2                            # takes original arr(t2) value
    sra $t2, $t2, 2

    sll $t3, $t3, 2
    lw $s4, arr($t3)
    mul $s5, $s2, $s7 
    add $s4, $s4, $s5
    sw $s4, arr($t3)                    # store arr(t3)=arr(t3) + $s7*arr(t2)
    sra $t3, $t3, 2

    addi $t2, $t2, 1
    addi $t3, $t3, 1

    beq $zero, $zero, checkbounds

sort:
    # Assume $a1 has left, $a2 has right
    addi $sp, $sp, -12

    sw $ra, 0($sp)                      # Store ra
    sw $a1, 4($sp)                      # Store left
    sw $a2, 8($sp)                      # Store right

    # check if left == right?
    beq $a1, $a2, basecase

    # call for left
    add $a2, $a1, $a2                   # compute mid
    sra $a2, $a2, 1

    jal sort

    # call for right
    lw $ra, 0($sp)                      # Restore ra
    lw $a1, 4($sp)                      # Restore left
    lw $a2, 8($sp)                      # Restore right

    add $a1, $a1, $a2                   # compute mid+1
    sra $a1, $a1, 1
    addi $a1, $a1, 1

    jal sort

    # merge both
    jal merge

    lw $ra, 0($sp)                      # Restore ra
    lw $a1, 4($sp)                      # Restore left
    lw $a2, 8($sp)                      # Restore right

    addi $sp, $sp, 12

    jr $ra

basecase:
    # Left == right. So, return to previous caller
    lw $ra, 0($sp)                      # Restore ra
    lw $a1, 4($sp)                      # Restore left
    lw $a2, 8($sp)                      # Restore right

    addi $sp, $sp, 12
    jr $ra

main:
    addi $s7, $zero, 10001
    # Print "Enter size of array to sort: "
    # li $v0, 4                           # Syscall for printing sizestring 
    # la $a0, sizestring                  
    # syscall 

    # Get the array size
    li $v0, 5                           # Syscall to input the size of array
    syscall

    move $s0, $v0                       # Move the size into $s0

    # Store the left and right pointers
    move $a1, $zero                     # Stores left
    addi $a2, $s0, -1                   # Stores right

    sll $s0, $s0, 2                     # Make size*4 for storing ints(4 bytes!)

    # Get the array elements
    # li $v0, 4                   
    # la $a0, arraystring                 # print the message for getting array
    # syscall

    move $t0, $zero                     # represents the index

getarray:
    beq $s0, $t0, getdone               # If index i == n, start sorting procedure
    # i < n, so, get arr(i) input
    li $v0, 5                           # Get arr(i)
    syscall

    sw $v0, arr($t0)                    # Store the value in arr(i)

    addiu $t0, $t0, 4                   # i = i + 4
    j getarray

getdone:
    # Array input done, start sort
    jal sort

    lw $ra, 0($sp)                      # Restore ra
    lw $a1, 4($sp)                      # Restore left
    lw $a2, 8($sp)                      # Restore right

    # li $v0, 4                   
    # la $a0, outputstring                 # print the message for getting array
    # syscall

    # li $v0, 4
    # la $a0, newline
    # syscall

    move $t0, $zero

printarray:
    beq $t0, $s0, printdone

    lw $a0, arr($t0)                    # Store the value in arr(i)
    li $v0, 1                           # Get arr(i)
    syscall

    li $v0 11  # syscall 11: print a character based on its ASCII value
    li $a0 10  # ASCII value of a newline is "10"
    syscall

    addiu $t0, $t0, 4                   # i = i + 4
    j printarray

printdone:
    li $v0, 10
    syscall
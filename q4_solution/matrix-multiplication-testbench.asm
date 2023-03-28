        global main

        extern exit
        extern matrix_mult, read_64, write_64

        section .text

matrix_init:
        push rax
        push rdx
        push rcx
        push r10

        mov rcx, [r3]
        mov rax, [c3]
        mul rcx
        mov rcx, rax
        shl rcx, 3
        mov rdx, [a3]
        add rcx, rdx
mat3_init_loop:
        xor rax, rax
        mov [rdx], rax
        add rdx, 8
        cmp rdx, rcx
        jne mat3_init_loop

        pop r10
        pop rcx
        pop rdx
        pop rax
        ret

main:
        push rbp

; INPUT - r1\nc1\nr2\nc2\n
; Matrices are 0-indiced !!

        call read_64
        mov [r1], rax
        call read_64
        mov [c1], rax                  ; rax = c1
        mov rcx, [r1]                  ; rcx = r1

; ; TODO - Fill code for allocating the matrix into memory, you may use either the stack or heap for this purpose
; ; Start of your code
; ; End of your code

        call read_64
        mov [r2], rax
        call read_64
        mov [c2], rax                  ; rax = c2
        mov rcx, [r2]                  ; rcx = r2

; ; TODO - Fill code for allocating the matrix into memory, you may use either the stack or heap for this purpose
; ; Start of your code
; ; End of your code

        mov rax, [c1]                  ; Validity check if matrices can be multiplied
        cmp rax, [r2]
        jne end

        mov rax, [r1]
        mov [r3], rax                  ; rax = r3
        mov rcx, [c2]
        mov [c3], rcx                  ; rcx = c3

; ; TODO - Fill code for allocating the matrix into memory, you may use either the stack or heap for this purpose
; ; Start of your code
; ; End of your code

; Matrix Input format - row major one number at a time for mat1 followed by mat2 !!
; Use the testcase_gen.py script to generate testcases to validate your code

        mov rcx, [r1]
        mov rax, [c1]
        mul rcx
        mov rcx, rax
        shl rcx, 3
        mov rdx, [a1]
        add rcx, rdx
mat1_read_loop:
        push rdx
        push rdx
        call read_64
        pop rdx
        pop rdx
        mov [rdx], rax
        add rdx, 8
        cmp rdx, rcx
        jne mat1_read_loop

        mov rcx, [r2]
        mov rax, [c2]
        mul rcx
        mov rcx, rax
        shl rcx, 3
        mov rdx, [a2]
        add rcx, rdx
mat2_read_loop:
        push rdx
        push rdx
        call read_64
        pop rdx
        pop rdx
        mov [rdx], rax
        add rdx, 8
        cmp rdx, rcx
        jne mat2_read_loop

processing_code:

        lfence
        rdtsc
        shl rdx, 32
        or rdx, rax
        mov r12, rdx
        lfence

        mov rdi, [a1]
        mov rsi, [r1]
        mov rcx, [a2]
        mov r8, [r2]
        mov r9, [c2]
        mov r10, [a3]
        mov rdx, [c1]
        mov r11, 0
test_loop:
        call matrix_init
        call matrix_mult
        add r11, 1
        cmp r11, 10
        jne test_loop

        lfence
        rdtsc
        shl rdx, 32
        or rdx, rax
        sub rdx, r12
        mov rax, rdx
        xor rdx, rdx
        mov rcx, 10
        div rcx
        call write_64
        lfence

        mov rcx, [r3]
        mov rax, [c3]
        mul rcx
        mov rcx, rax
        shl rcx, 3
        mov rdx, [a3]
        add rcx, rdx
mat3_print_loop:
        mov rax, [rdx]
        push rdx
        push rcx
        call write_64
        pop rcx
        pop rdx
        add rdx, 8
        cmp rdx, rcx
        jne mat3_print_loop

code_end:
        jmp end

end:
        xor rdi, rdi
        call exit

        section .bss

        wordsize equ 8
        tempsize equ 10

r1:
        resb wordsize                  ; row count of mat1
c1:
        resb wordsize                  ; col count of mat1
a1:
        resb wordsize                  ; pointer to mat1

r2:
        resb wordsize                  ; row count of mat2
c2:
        resb wordsize                  ; col count of mat2
a2:
        resb wordsize                  ; pointer to mat2

r3:
        resb wordsize                  ; row count of res
c3:
        resb wordsize                  ; col count of res
a3:
        resb wordsize                  ; pointer to mat 3

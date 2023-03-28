; ; Do not modify this file - provided for I/O operations on stdin and stdout

        global read_64, write_64
        extern printf, scanf, malloc
        section .text
read_64:
; stores 64-bit number read into rax register
; no registers modified
        push rdi
        push rsi
        push rcx

        mov rax, [first_read_flag]
        cmp rax, 0
        jne not_first_read

        mov rax, 1
        mov [first_read_flag], rax

        mov rdi, 16
        call malloc

not_first_read:
        mov rdi, read_format_64
        mov rsi, tmp
        xor rax, rax

        call scanf
        mov rax, [tmp]
        pop rcx
        pop rsi
        pop rdi
        ret

write_64:
; writes 64-bit number stored in rax register onto stdout
; no registers modified
        push rdi
        push rax
        push rsi

        mov rax, [first_write_flag]
        cmp rax, 0
        jne not_first_write

        mov rax, 1
        mov [first_write_flag], rax

        xor r14, r14
overwrite_loop_sifsiafuherbguye:

        mov rdi, 100000
        call malloc
        mov rcx, rsi
        xor rdx, rdx
brk_overwrite_loop_dshfncuyefgc:
        mov [rax], rdx
        add rax, 8
        cmp rax, rcx
        jne brk_overwrite_loop_dshfncuyefgc

        inc r14
        cmp r14, 1000
        jne overwrite_loop_sifsiafuherbguye

not_first_write:
        pop rsi
        pop rax
        push rax
        push rsi

        mov rdi, write_format_64
        mov rsi, rax
        xor rax, rax

        call printf

        pop rsi
        pop rax
        pop rdi
        ret

        section .bss
        wordsize equ 8
        tempsize equ 10

tmp:
        resb wordsize                  ; placeholder for int input
first_write_flag: resb 8
first_read_flag: resb 8

        section .data
read_format_64:
        db "%ld", 0
write_format_64:
        db `%ld\n`, 0
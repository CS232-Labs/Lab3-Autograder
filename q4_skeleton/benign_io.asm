; ; Do not modify this file - provided for I/O operations on stdin and stdout

        global read_64, write_64
        extern printf, scanf
        section .text
read_64:
; stores 64-bit number read into rax register
; no registers modified
        push rdi
        push rsi
        push rcx

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

        section .data
read_format_64:
        db "%ld", 0
write_format_64:
        db `%ld\n`, 0

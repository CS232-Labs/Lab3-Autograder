        section .text
        global matrix_mult

matrix_mult:
        push rdi                       ; pointer to mat1
        push rsi                       ; row count of mat1
        push rdx                       ; column count of mat1
        push rcx                       ; pointer to mat2
        push r8                        ; row count of mat2
        push r9                        ; column count of mat2
        push r10                       ; pointer to mat3
        push r11
        push r12
        push r13

; ; 0-indexing on all matrices
; ; mat1[i][j] = rdi+(rdx*i+j)*8
; ; assume rdx = r8
; ; Code used to set mat3[1][1] = 1

        xor rax, rax
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, 5
        shl rax, 3
        mov r11, 490
        mov rax[r10], r11
        xor rax, rax
        add rax, 7
        shl rax, 3
        mov r11, 224
        mov rax[r10], r11
        xor rax, rax
        add rax, r9
        add rax, r9
        add rax, 2
        shl rax, 3
        mov r11, 880
        mov rax[r10], r11
        xor rax, rax
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, 3
        shl rax, 3
        mov r11, 233
        mov rax[r10], r11
        xor rax, rax
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, 8
        shl rax, 3
        mov r11, 544
        mov rax[r10], r11
        xor rax, rax
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, 0
        shl rax, 3
        mov r11, 728
        mov rax[r10], r11
        xor rax, rax
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, 4
        shl rax, 3
        mov r11, 705
        mov rax[r10], r11
        xor rax, rax
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, 4
        shl rax, 3
        mov r11, 661
        mov rax[r10], r11
        xor rax, rax
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, 2
        shl rax, 3
        mov r11, 783
        mov rax[r10], r11
        xor rax, rax
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, 4
        shl rax, 3
        mov r11, 505
        mov rax[r10], r11
        xor rax, rax
        add rax, 8
        shl rax, 3
        mov r11, 414
        mov rax[r10], r11
        xor rax, rax
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, 2
        shl rax, 3
        mov r11, 103
        mov rax[r10], r11
        xor rax, rax
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, 4
        shl rax, 3
        mov r11, 876
        mov rax[r10], r11
        xor rax, rax
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, 8
        shl rax, 3
        mov r11, 206
        mov rax[r10], r11
        xor rax, rax
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, 9
        shl rax, 3
        mov r11, 525
        mov rax[r10], r11
        xor rax, rax
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, 2
        shl rax, 3
        mov r11, 450
        mov rax[r10], r11
        xor rax, rax
        add rax, 3
        shl rax, 3
        mov r11, 0
        mov rax[r10], r11
        xor rax, rax
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, 3
        shl rax, 3
        mov r11, 111
        mov rax[r10], r11
        xor rax, rax
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, r9
        add rax, 5
        shl rax, 3
        mov r11, 942
        mov rax[r10], r11
        xor rax, rax
        add rax, r9
        add rax, 7
        shl rax, 3
        mov r11, 52
        mov rax[r10], r11

        pop r13
        pop r12
        pop r11
        pop r10
        pop r9
        pop r8
        pop rcx
        pop rdx
        pop rsi
        pop rdi
        ret
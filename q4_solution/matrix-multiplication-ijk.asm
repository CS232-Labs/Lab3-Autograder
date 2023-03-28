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
; ; GOAL - Perform matrix multiplication of mat1, mat2 and save result in mat3

; ; TODO - Fill your code here performing the matrix multiplication in the following order
; ; for i in range(r1) { for j in range(c2) { for k in range(c1) { mat3[i][j] += mat1[i][k]*mat2[k][j] } } }

; ; End of code to be filled

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

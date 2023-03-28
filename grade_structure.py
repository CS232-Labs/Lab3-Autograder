newline_char = "\n"
newline_replaced = "\\n"

def clean(str_obj : str):
    return str_obj.replace(newline_char,newline_replaced)

class Grade:
    roll_no = ""
    q1_a = 0
    q1_b = 0
    q1_c = 0
    q1_viva = 0
    q1_message = ""
    q2_correctness = 0
    q2_bonus = 0
    q2_message = ""
    q3_correctness = 0
    q3_speed = 0
    q3_complexity_doubt = ""
    q3_complexity_help = ""
    q3_memory = 0
    q3_memory_doubt = ""
    q3_memory_help = ""
    q3_viva = 0
    q3_message = ""
    q4_code_valid = 0
    q4_memory = 0 # done fully
    q4_correctness = 0 # done fully - need testcases
    q4_speed_ijk = 0
    q4_speed_ikj = 0
    q4_speed_jik = 0
    q4_speed_jki = 0
    q4_speed_kij = 0
    q4_speed_kji = 0
    q4_speed = 0 
    q4_viva = 0 # purely by report (or if q4_message flags brk check)
    q4_bonus = 0 # purely by report
    q4_message = ""
    format_message = ""


    def my_view(self) -> str:

        # list1 = [self.roll_no, self.q1_a, self.q1_b, self.q1_c, self.q1_viva]

        prologue = f'{self.roll_no},'
        q1_view = f'{self.q1_a},{self.q1_b},{self.q1_c},{self.q1_viva},"{clean(self.q1_message)}",'
        q2_view = f'{self.q2_correctness},{self.q2_bonus},"{clean(self.q2_message)}",'
        q3_view = f'{self.q3_correctness},{self.q3_speed},"{clean(self.q3_complexity_doubt)}","{clean(self.q3_complexity_help)}",{self.q3_memory},"{clean(self.q3_memory_doubt)}","{clean(self.q3_memory_help)}",{self.q3_viva},"{clean(self.q3_message)}",'
        q4_view = f'{self.q4_code_valid},{self.q4_memory},{self.q4_correctness},{self.q4_speed_ijk},{self.q4_speed_ikj},{self.q4_speed_jik},{self.q4_speed_jki},{self.q4_speed_kij},{self.q4_speed_kji},{self.q4_speed},{self.q4_viva},{self.q4_bonus},"{clean(self.q4_message)}",'
        epilogue = f'{self.format_message}'
        
        return prologue + q1_view + q2_view + q3_view + q4_view + epilogue 
        # return f'{self.roll_no},{self.q1_a},{self.q1_b},{self.q1_c},{self.q1_viva},"{self.q1_message}",{self.q2_correctness},{self.q2_bonus},"{self.q2_message}",{self.q4_speed_ijk},{self.q4_speed_ikj},{self.q4_speed_jik},{self.q4_speed_jki},{self.q4_speed_kij},{self.q4_speed_kji},{self.q3_correctness},{self.q3_speed},{self.q3_complexity_doubt},{self.q3_complexity_help},{self.q3_memory},{self.q3_memory_doubt},{self.q3_memory_help},{self.q3_viva},"{self.q3_message}",{self.q4_code_valid},{self.q4_memory},{self.q4_correctness},{self.q4_speed},{self.q4_viva},{self.q4_message},{self.format_message}'

    def __repr__(self) -> str:
        return self.my_view()
    
    def __str__(self) -> str:
        return self.my_view()
    
    def __format__(self, __format_spec: str) -> str:
        return self.my_view()
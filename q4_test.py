import os
import subprocess
import re
import resource
import difflib
import time
from log import *
from tqdm import tqdm

"""
Utility functions for part d) and e) checking
"""
def memory_resource_unbound():
        # passed as preexec_fn to remove resource limits on memory
        resource.setrlimit(resource.RLIMIT_DATA,(resource.RLIM_INFINITY,resource.RLIM_INFINITY))
        resource.setrlimit(resource.RLIMIT_STACK,(resource.RLIM_INFINITY,resource.RLIM_INFINITY))
        resource.setrlimit(resource.RLIMIT_RSS,(resource.RLIM_INFINITY,resource.RLIM_INFINITY))
        resource.setrlimit(resource.RLIMIT_FSIZE,(resource.RLIM_INFINITY,resource.RLIM_INFINITY))
        resource.setrlimit(resource.RLIMIT_AS,(resource.RLIM_INFINITY,resource.RLIM_INFINITY))

def memory_resource_bound():
    resource.setrlimit(resource.RLIMIT_STACK, (1024 * 1024,1024 * 1024))


def compare_matmul_outs(actual, expected, debug=False):
    # Ignore row to measure timing to compare correctness
    with open(actual, "r") as actual_fd, open(expected,"r") as expected_fd:
        actual_lines, expected_lines = actual_fd.readlines(), expected_fd.readlines()
        # print(len(actual_lines),len(expected_lines))
        if len(actual_lines) < 1:
            return  True
        
        if len(actual_lines) != len(expected_lines):
            return True
        
        actual_lines, expected_lines = actual_lines[1:], expected_lines[1:]

        for actual_line, expected_line in zip(actual_lines, expected_lines):
            # print(actual_line, expected_line)
            if (actual_line != expected_line):
                return True
            
        return False


"""
Q4 Part compilation checking
"""
def check_q4_compile():
    make_proc = subprocess.Popen(["make",f"NASM={nasm_path}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    make_stdout, make_stderr = make_proc.communicate()
    make_proc.wait()
    return (make_proc.returncode !=0, make_stderr)

"""
Q4 Part d) checking
"""
def run_memtest(input_dir, expected_output_dir, actual_output_dir, binary_dir, mem_func=memory_resource_unbound, debug=False):
    # Note that this needs inputfile = "3" and outputfile="memory_test","3"    
    memory_test_input = os.path.join(input_dir,"101")
    expected_memory_test_output = os.path.join(expected_output_dir,"memory_test")
    actual_memory_test_output = os.path.join(actual_output_dir,"memory_test")
    try:
        with open(memory_test_input,"r") as input_fd, open(actual_memory_test_output,"w") as output_fd:
            ps = subprocess.Popen(os.path.join(binary_dir, "memtest.o"), preexec_fn=mem_func, stdin=input_fd, stdout=output_fd, stderr=subprocess.PIPE, shell=False)
            stderr = ps.communicate()
            ps.wait()
            if ps.returncode != 0:
                error(f"[ERROR] Program fails to run with error = {stderr}")
                return False
        # with open(actual_memory_test_output,"r") as actual_fd, open(expected_memory_test_output,"r") as expected_fd:
        nlinesdiff = compare_matmul_outs(actual_memory_test_output, expected_memory_test_output, debug=debug)
        if nlinesdiff:
            error(f"[ERROR] Testcase mismatch on {memory_test_input}")
            return  False
    except Exception as err:
        error(f"[ERROR] Subprocess error = {err} with type = {type(err)}")
        return False
    return True


def check_q4_d(input_dir, expected_output_dir, actual_output_dir, binary_dir):
    # Note that this needs inputfile = "3" and outputfile="memory_test","3"  
    import shutil
    shutil.copyfile(os.path.join(os.path.join(basedir, "q4_skeleton"), "memory-test.asm"), os.path.join(binary_dir,"memory-test.asm"))
    shutil.copyfile(os.path.join(os.path.join(basedir, "q4_skeleton"), "benign_io.asm"), os.path.join(binary_dir,"io.asm"))
    compile_fail, compile_error =  check_q4_compile()
    if compile_fail:
        error(f"[ERROR] unexpected error {compile_error} - tampered memory-test/io.asm")
        return False
    
    unbound_mem_run = run_memtest(input_dir, expected_output_dir, actual_output_dir, binary_dir)
    if not unbound_mem_run:
        error("[ERROR] Memory test fails with unbound memory")
        return False

    bound_mem_run = run_memtest(input_dir, expected_output_dir, actual_output_dir, binary_dir, mem_func=memory_resource_bound)
    if not bound_mem_run:
        info("[INFO] Used stack for memory allocation - partial")
        grade.q4_memory = 0.5
        return True
    
    info("[INFO] Heap used for memory allocation")
    shutil.copyfile(os.path.join(os.path.join(basedir, "q4_skeleton"), "brk_io.asm"), os.path.join(binary_dir,"io.asm"))
    compile_fail, compile_error =  check_q4_compile()
    if compile_fail:
        grade.q4_message += f"unexpected error {compile_error} - manually check for brk"
        error(f"[ERROR] unexpected error {compile_error} - manually check for brk")
        return True
    # /home/girish/iitb22/ca_ta/lab3/Lab3-evaluation/testcases/Q4/input/3
     
    brk_poisoned_run = run_memtest(input_dir, expected_output_dir, actual_output_dir, binary_dir, mem_func=memory_resource_unbound, debug=True)
    if not brk_poisoned_run:
        info("[INFO] Used brk for memory allocation - partial")
        grade.q4_memory = 0.7
    else:
        info("[INFO] Used mmap for memory allocation - full")
        grade.q4_memory = 1.0

    shutil.copyfile(os.path.join(os.path.join(basedir, "q4_skeleton"), "benign_io.asm"), os.path.join(binary_dir,"io.asm"))
    compile_fail, compile_error =  check_q4_compile()
    if compile_fail:
        assert(False)
    return True
    

def read_timestamp(actual_outfile):
    with open(actual_outfile,"r") as actual_fd:
        line = actual_fd.readlines()[0]
        return int(line.strip())

"""
Q4 Part e) checking
"""
def check_q4_e(input_dir, expected_output_dir, actual_output_dir, binary_dir):
    n_pass, n_total = 0, 0
    ts = [0, 0, 0, 0, 0, 0]
    ns = [0, 0, 0, 0, 0, 0]
    input_files = sorted(list(os.listdir(input_dir)))
    Len = len(input_files)
    # Len = 3 
    for i in tqdm(range(Len)):
        inputfile = input_files[i]
        expected_outfile = os.path.join(expected_output_dir,os.path.basename(inputfile))
        for loop_idx, matrix_loop_order in enumerate(["ijk","ikj","jik","jki","kij","kji"]):
            actual_outfile = os.path.join(actual_output_dir,os.path.basename(inputfile)+f"_{matrix_loop_order}")
            try:
                with open(os.path.join(input_dir,inputfile),"r") as input_fd, open(actual_outfile,"w") as output_fd:
                    ps = subprocess.Popen(os.path.join(binary_dir,f"matrix-{matrix_loop_order}.o"), preexec_fn=memory_resource_unbound, stdin=input_fd, stdout=output_fd, stderr=subprocess.PIPE, shell=False)
                    stderr = ps.communicate()
                    ps.wait()
                    if ps.returncode != 0:
                        error(f"[ERROR] Program fails to run with error = {stderr}")
                        continue
                # with open(actual_outfile,"r") as actual_fd, open(expected_outfile,"r") as expected_fd:
                nlinesdiff = compare_matmul_outs(actual_outfile, expected_outfile)
                if nlinesdiff:
                    error(f"[ERROR] Testcase mismatch on {os.path.join(input_dir,inputfile)} for loop order {matrix_loop_order}")
                else:
                    n_pass+=1
                    ts[loop_idx] += read_timestamp(actual_outfile=actual_outfile)
                    ns[loop_idx] += 1
            except Exception as err:
                error(f"[ERROR] Subprocess error = {err} with type = {type(err)} on file = {inputfile} and loop order = {matrix_loop_order}")
            n_total+=1
    return n_pass, n_total, list(zip(ns,ts))

"""
    Check if the student has filled code only in the space between TODO and END
    Otherwise, give 0

    file1 - actual given file
    file2 - student's submission

    Returns True if there is a difference; Else, returns False
"""
def check_diff(file1, file2, isTestbench = False):
    # print("checking diff...")
    with open(file1, "r") as f1, open(file2, "r") as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

        isIgnored = False

        cur1 = cur2 = 0     # Pointers to traverse over the two files
        
        while cur1 < len(lines1):

            if cur2 >= len(lines2):
                grade.q4_message += "Tampered file\n"
                return True

            # print(f"cur1 = {cur1}, cur2 = {cur2}")

            line1 = lines1[cur1].strip()
            line2 = lines2[cur2].strip()

            # print(f"line1 = '{line1}' \nline2 = '{line2}', isIgnored = {isIgnored}")

            if not isIgnored and line1 == "":
                cur1 += 1
                continue

            if line2 == "":
                cur2 += 1
                continue

            if not isIgnored:
                # print("not ignored...", (line1 == line2))
                if (line1 != line2):
                    error(f"""
                        Mismatch in {file1}!
                        Line #{cur1 + 1} of solution : {line1}\n
                        Line #{cur2 + 1} of submission file : {line2}\n
                    """)
                    return True
                else:
                    cur1 += 1
                    cur2 += 1
            else:
                cur2 += 1
                if isTestbench and (line2.startswith("call")):
                    grade.q4_message += "Used call instruction in testbench\n"
                    return True

            # print(cur1, cur2, len(lines1))

            if line2.startswith("; ; for") or line2.startswith("; ; Start of"): 
                isIgnored = True
                cur1 += 1 
            if line2.startswith("; ; End of"):
                isIgnored = False
                cur1 += 1
            
    return False
"""
    
"""
def check_code(expected_submission_path, actual_folder_path):
    info("checking code...")
    loop_combinations = ["ijk", "ikj", "jik", "jki", "kij", "kji"]
    folder_path = os.path.join(expected_submission_path,f"Q4")

    # print(folder_path)

    for comb in loop_combinations:
        filename = f"matrix-multiplication-{comb}.asm"
        file_path = os.path.join(folder_path, filename)
        info(f"checking {filename}")
        actual_file_path = os.path.join(os.path.join(basedir,"q4_solution"), filename)

        isSame = check_diff(actual_file_path, file_path, (comb == "testbench"))
        if isSame:
            # print("Not same files...")
            error(f"[ERROR] {filename} has been tampered...")
            grade.q4_code_valid = 0
            grade.q4_message += f"{filename} has been tampered...\n"
        else:
            grade.q4_code_valid = 1
        
    info(f"[INFO] All code files ok...")

"""
Testing for Q4
"""
def check_q4(expected_submission_path):
    # NOTE that we will be using our own matrix-multiplication-testbench.asm for part e) and our own memory-test.asm for d) and our Makefile, io.asm for both parts
    is_q4_compile_error, q4_compile_error = check_q4_compile()

    if is_q4_compile_error:
        error(f"[ERROR] Make command fails - {q4_compile_error}")    
        grade.q4_message += f"Make command fails - {q4_compile_error}"
        test_fail(f"{fail_char} Q4 Compilation failed")
        return
    else:
        test_pass(f"{pass_char} Q4 compilation pass")

    # Construct required directory paths
    testcasedir = os.path.join(os.path.join(basedir,"testcases"),"Q4")
    inputdir = os.path.join(testcasedir,"input")
    expected_outputdir = os.path.join(testcasedir,"output")
    actual_outputdir = os.path.join(expected_submission_path,"Q4")
    binarydir = os.path.join(expected_submission_path,"Q4")

    check_code(expected_submission_path, "q4_solution")

    # Memory test check
    q4_memory_testcase_passed = check_q4_d(input_dir=inputdir, expected_output_dir=expected_outputdir, actual_output_dir=actual_outputdir, binary_dir=binarydir)

    if not q4_memory_testcase_passed:
        test_fail(f"{fail_char} Q4 d) testcase match fail")
        return
    else:
        test_pass(f"{pass_char} Q4 d) testcase match pass")

    # For each input iterate over all binaries and validate with expected output returning on first failure
    q4_testcase_passed, q4_testcase_total, q4_speed_res = check_q4_e(input_dir=inputdir, expected_output_dir=expected_outputdir, actual_output_dir=actual_outputdir, binary_dir=binarydir)

    grade.q4_correctness = (q4_testcase_passed * 1.0) / q4_testcase_total

    if q4_testcase_passed < q4_testcase_total:
        test_fail(f"{fail_char} Q4 e) testcases [{q4_testcase_passed}/{q4_testcase_total}] passed")
        return
    else:
        test_pass(f"{pass_char} Q4 e) testcase [{q4_testcase_passed}/{q4_testcase_total}] passed")

    # ["ijk", "ikj", "jik", "jki", "kij", "kji"]
    grade.q4_speed_ijk = q4_speed_res[0][1] / q4_speed_res[0][0]
    grade.q4_speed_ikj = q4_speed_res[1][1] / q4_speed_res[1][0]
    grade.q4_speed_jik = q4_speed_res[2][1] / q4_speed_res[2][0]
    grade.q4_speed_jki = q4_speed_res[3][1] / q4_speed_res[3][0]
    grade.q4_speed_kij = q4_speed_res[4][1] / q4_speed_res[4][0]
    grade.q4_speed_kji = q4_speed_res[5][1] / q4_speed_res[5][0]

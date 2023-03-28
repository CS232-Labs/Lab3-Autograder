import os
import subprocess
from log import *
import time
from tqdm import tqdm

testcasedir = os.path.join(os.path.join(basedir,"testcases"),"Q3")
inputdir = os.path.join(testcasedir,"input")
expected_outputdir = os.path.join(testcasedir,"output")

def run_spim(program_file, input_fd, output_fd, timeout=1, my_spim_path=spim_path, flags = []):
    """
    Returns True if runs with no exception else returns False after printing non-critical error message
    """
    try:
        ps = subprocess.Popen([my_spim_path,"-exception_file",exceptions_path,*flags,"-f",program_file], stdin=input_fd, stdout=output_fd, stderr=subprocess.PIPE, shell=False)
        try:
            stderr = ps.communicate(timeout)
            ps.wait()
        except subprocess.TimeoutExpired as exc:
            ps.kill()
            return 1
        if ps.returncode != 0:
            error(f"[ERROR] Process returns error = {stderr}")
            return 0
    except Exception as err:
        error(f"[ERROR] Subprocess error = {err} with type = {type(err)}")
        return 0
    return 2

"""
    first, 1 runs:
        Heap  - 131072 + 40150 = x1 - spim_for_recursion
        Heap  - 131072 + 150  , stack -> unbound = x2 - regular_spim
    if x1 - > full
    if not x1:
        if x2:
            used_stack -> flag !
        else:
            used_recursion -> 0 !
    
    # Ideally, exactly one of them should pass
"""
def check_q3_memory(expected_submission_path):
    binarydir = os.path.join(expected_submission_path,"Q3")
    executablefile = os.path.join(binarydir,"inplacemergesort.s")

    with open(os.path.join(inputdir,"1"),"r") as input_fd, open("/dev/null", "w") as output_fd:
        x1 = run_spim(program_file=executablefile,input_fd=input_fd, output_fd=output_fd, my_spim_path=modified_spim_path, flags=["-ldata",f"{131072 + 40150}"])
    # subprocess.Popen(["gnome-terminal","--","sh"])
    # time.sleep(60)
    with open(os.path.join(inputdir,"1"),"r") as input_fd, open("/dev/null", "w") as output_fd:
        x2 = run_spim(program_file=executablefile,input_fd=input_fd, output_fd=output_fd, my_spim_path=instructions_spim_path, flags=["-ldata",f"{131072+150}"])
        
    with open(os.path.join(inputdir,"1"),"r") as input_fd, open("/dev/null", "w") as output_fd:
        x3 = run_spim(program_file=executablefile,input_fd=input_fd, output_fd=output_fd, my_spim_path=spim_path, flags=[])

    if x1:
        grade.q3_memory = 1
        grade.q3_memory_help += "Has used heap + iteration\n"
    else:
        if x2:
            grade.q3_memory = 0.0
            grade.q3_memory_doubt += "Has used stack\n"
            grade.q3_memory_help += "Suspected stack usage or heap usage with .space - need to check\n"
        else:
            if x3:
                grade.q3_memory = 0.75
                grade.q3_memory_help += "Has used heap + recursion\n"
            else:
                grade.q3_memory = 0.0
                grade.q3_memory_help += "Failed all runs\n"
                return False
    
    return True


def compare_spim_output(actual_outfile, expected_outfile):
    with open(actual_outfile, "r") as actual_fd, open(expected_outfile, "r") as expected_fd:
        actual_output = actual_fd.readlines()
        expected_output = expected_fd.readlines()

        if len(actual_output) == 0:
            return False
        
        if len(expected_output) == 0:
            return False
        
        if actual_output[-1] == "\n":
            actual_output = actual_output[:-1]

        if expected_output[-1] == "\n":
            expected_output = expected_output[:-1]

        if (len(actual_output) < 5) or (len(expected_output) < 5):
            return False
        elif len(actual_output) != len(expected_output):
            return False
        else:
            actual_output = actual_output[5:]
            expected_output = expected_output[5:]
            for actual_line, expected_line in zip(actual_output, expected_output):
                actual_line = actual_line.strip()
                expected_line = expected_line.strip()
                if actual_line != expected_line:
                    return False
            return True

def get_num_instructions(filename):
    with open(filename, "r") as fd:
        lines = fd.readlines()

        for line in lines:
            temp = line.strip()
            if temp.startswith("Steps:"):
                return int(temp.split()[1])

    return -1


"""
    Get time for 10000-sized output
    Get time for 10-sized output

    If O(nlogn), then, ratio ~ 4000 (upto 6000)
    If O(nlogn^2), then ration > 6000 (expected) < 60,000 - flag for manual checks
    If >= O(n^2), then ratio = 1,000,000 (definitely > 100,000)
"""
def check_q3_speed(expected_submission_path):
    binarydir = os.path.join(expected_submission_path,"Q3")
    filename = os.path.join(expected_submission_path,"temp_file_q3_speed")
    executablefile = os.path.join(binarydir,"inplacemergesort.s")
    steps_10000 = 1
    steps_10 = 1

    ratio = (steps_10000 / steps_10)

    # make sure testcase 1 is 10000-sized
    with open(os.path.join(inputdir,"1"),"r") as input_fd, open(filename, "w+") as output_fd:
        spim_result = run_spim(executablefile, input_fd, output_fd, timeout=30, my_spim_path=instructions_spim_path, flags = [])
        if spim_result == 2:
            steps_10000 = get_num_instructions(filename)
        elif spim_result == 1:
            steps_10000 = 1000000 * 1000000
        else:
            grade.q3_speed = 0
            grade.q3_complexity_help += "Error for q3 10000 case\n"
            return False

    # make sure testcase 2 is 10-sized
    with open(os.path.join(inputdir,"2"),"r") as input_fd, open(filename, "w+") as output_fd:
        run_spim(executablefile, input_fd, output_fd, timeout=30, my_spim_path=instructions_spim_path, flags = [])
        if spim_result == 2:
            steps_10 = get_num_instructions(filename)
        else:
            grade.q3_speed = 0
            grade.q3_complexity_help += "Error for q3\n"
            return False

    ratio = (steps_10000 * 1.0) / steps_10 

    info(f"Ratio = {ratio}")

    if ratio <= 6000:
        grade.q3_speed = 1.0
    elif ratio <= 60000:
        grade.q3_speed = 0.75
        grade.q3_complexity_doubt = "Is O(NlogNlogN) ?"
        grade.q3_complexity_help += f"ratio = {ratio}\n"
    else:
        grade.q3_speed = 0.25
        grade.q3_complexity_help += f"ratio = {ratio}; >= O(n^2)\n"
        
    return True


def check_q3_correctness(expected_submission_path):
    actual_outputdir = os.path.join(expected_submission_path,"Q3")
    binarydir = os.path.join(expected_submission_path,"Q3")
    executablefile = os.path.join(binarydir,"inplacemergesort.s")
    q3_testcase_passed, q3_testcase_total = 0, 0
    messageFlag = False
    file_list = os.listdir(inputdir)
    Len = len(file_list)
    # Len = 3
    for i in tqdm(range(Len)):
        inputfile = file_list[i]
        q3_testcase_total += 1
        expected_outfile = os.path.join(expected_outputdir,os.path.basename(inputfile))
        actual_outfile = os.path.join(actual_outputdir,os.path.basename(inputfile))
        # print(inputfile, actual_outfile, expected_outfile, os.path.exists(inputfile), os.path.exists(actual_outfile), os.path.exists(expected_outfile))

        # spim_result: 0 -> compilation/runtime error, 1 -> timeout, 2 -> correct
        with open(os.path.join(inputdir,inputfile),"r") as input_fd, open(actual_outfile, "w") as output_fd:
            spim_result = run_spim(executablefile, input_fd, output_fd, timeout=5)
            if spim_result == 1:
                messageFlag = True
            if spim_result != 2:
                continue
        is_same = compare_spim_output(actual_outfile, expected_outfile)

        if is_same:
            q3_testcase_passed += 1

    grade.q3_correctness = (q3_testcase_passed * 1.0)/ q3_testcase_total

    if messageFlag:
        grade.q3_message = f"timeout error\n"
    
    grade.q3_message += f"testcases [{q3_testcase_passed}/{q3_testcase_total}] passed"

    if q3_testcase_passed < q3_testcase_total:
        test_fail(f"{fail_char} Q3 testcases [{q3_testcase_passed}/{q3_testcase_total}] passed")
        return
    else:
        test_pass(f"{pass_char} Q3 testcases [{q3_testcase_passed}/{q3_testcase_total}] passed")


def check_q3(expected_submission_path):
    if check_q3_memory(expected_submission_path):
        test_pass(f"{pass_char} Q3 memory testcase match pass")
    else:
        test_fail(f"{fail_char} Q3 memory testcase match fail")

    if check_q3_speed(expected_submission_path):
        test_pass(f"{pass_char} Q3 speed testcase match pass")
    else:
        test_fail(f"{fail_char} Q3 speed testcase match fail")

    check_q3_correctness(expected_submission_path)


    
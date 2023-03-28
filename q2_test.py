import os
import subprocess
from log import *

def run_spim(program_file, input_fd, output_fd, timeout=1):
    """
    Returns True if runs with no exception else returns False after printing non-critical error message
    """
    try:
        ps = subprocess.Popen([spim_path,"-exception_file",exceptions_path,"-f",program_file], stdin=input_fd, stdout=output_fd, stderr=subprocess.PIPE, shell=False)
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
Q2 Part compilation checking
"""
def check_q2_compile():
    make_proc = subprocess.Popen(["spim",f"NASM={spim_path}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    make_stdout, make_stderr = make_proc.communicate()
    make_proc.wait()
    return (make_proc.returncode !=0, make_stderr)

def compare_spim_output(actual_outfile, expected_outfile):
    # print("Called")
    with open(actual_outfile, "r") as actual_fd, open(expected_outfile, "r") as expected_fd:
        actual_output = actual_fd.readlines()
        expected_output = expected_fd.readlines()

        if len(actual_output) == 0 or len(expected_output) == 0:
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

                # print(actual_line, expected_line)

                if actual_line != expected_line:
                    return False
            return True

def check_q2(expected_submission_path):
    testcasedir = os.path.join(os.path.join(basedir,"testcases"),"Q2")
    inputdir = os.path.join(testcasedir,"input")
    expected_outputdir = os.path.join(testcasedir,"output")
    actual_outputdir = os.path.join(expected_submission_path,"Q2")
    binarydir = os.path.join(expected_submission_path,"Q2")
    executablefile = os.path.join(binarydir,"inverse.s")
    q2_testcase_passed, q2_testcase_total = 0, 0
    messageFlag = False
    for inputfile in os.listdir(inputdir):
        q2_testcase_total += 1
        expected_outfile = os.path.join(expected_outputdir,os.path.basename(inputfile))
        actual_outfile = os.path.join(actual_outputdir,os.path.basename(inputfile))
        # print(inputfile, actual_outfile, expected_outfile, os.path.exists(inputfile), os.path.exists(actual_outfile), os.path.exists(expected_outfile))

        # spim_result: 0 -> compilation/runtime error, 1 -> timeout, 2 -> correct
        with open(os.path.join(inputdir,inputfile),"r") as input_fd, open(actual_outfile, "w") as output_fd:
            spim_result = run_spim(executablefile, input_fd, output_fd)
            if spim_result == 1:
                messageFlag = True
            if spim_result != 2:
                continue
        is_same = compare_spim_output(actual_outfile, expected_outfile)

        if is_same:
            q2_testcase_passed += 1

    grade.q2_correctness = (q2_testcase_passed * 1.0)/ q2_testcase_total

    if messageFlag:
        grade.q2_message = f"timeout error\n"
    
    grade.q2_message += f"testcases [{q2_testcase_passed}/{q2_testcase_total}] passed"

    if q2_testcase_passed < q2_testcase_total:
        test_fail(f"{fail_char} Q2 testcases [{q2_testcase_passed}/{q2_testcase_total}] passed")
        return
    else:
        test_pass(f"{pass_char} Q2 testcases [{q2_testcase_passed}/{q2_testcase_total}] passed")
        
    


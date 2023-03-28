import os
import argparse
import tempfile
import tarfile

from log import *
import q4_test
import q3_test
import q2_test

gradefile = "grades.csv"

"""
Print grades
"""
def print_grade():
    with open(os.path.join(basedir,gradefile),"a") as gradefd:
        gradefd.write(f"{grade}\n")

"""
Enter the temporary directory
"""
def enter_temporary_dir(tmpdirname):
    info(f"[INFO] creating tmpdir = {tmpdirname}")
    os.chdir(tmpdirname)
    info(f"[INFO] entered {tmpdirname}")


"""
Extract the tar file into the temporary directory
"""
def extract_tar(tmpdirname, submission):
    try:
        tar_file = tarfile.open(submission)
        tar_file.extractall(tmpdirname)
        tar_file.close()
        info(f"[INFO] submission extracted")
    except:
        grade.format_message = f"Submission file in invalid format"
        print_grade()
        critical_error(f"[ERROR] Submission file in invalid format")


"""
Check topmost folder name; Exits if wrong
"""
def check_folder_name(tmpdirname, submission_file_name):
    expected_submission_path = os.path.join(tmpdirname,submission_file_name[:-7])
    print(expected_submission_path)
    if not os.path.isdir(expected_submission_path):
        grade.format_message = f"Invalid submission folder name"
        print_grade()
        critical_error(f"[ERROR] Invalid submission folder name")

    return expected_submission_path


"""
Enter the submission folder
"""
def enter_submission_folder(expected_submission_path):
    os.chdir(expected_submission_path)
    info(f"[INFO] entering submission folder")


"""
Get all the folders and files in the submission
"""
def get_root_folders_and_files(expected_submission_path):
    root_folders = set()
    root_files = set()

    for root_file in os.listdir(expected_submission_path):
        if os.path.isdir(root_file):
            # Make sure it is not hidden (this will ignore .git and .gitignore)
            if root_file[0] != '.':
                root_folders.add(os.path.basename(root_file))
        else:
            if root_file[0] != '.':
                root_files.add(os.path.basename(root_file))

    return root_folders, root_files


"""
Check if there is a report file; Exit if there are extra files/missing files
"""
def check_root_files(root_files, valid_root_files):
    # print(f"root_files = {root_files}, valid_root_files = {valid_root_files}")
    if len(root_files.difference(valid_root_files)) != 0:
        grade.format_message = f"Extra files in root folder ({list(root_files.difference(valid_root_files))})"
        print_grade()
        critical_error(f"[ERROR] Extra files in root folder ({list(root_files.difference(valid_root_files))}) - Grading halted")
    
    if len(valid_root_files.difference(root_files)) != 0:
        grade.format_message = f"Missing files in root folder ({list(valid_root_files.difference(root_files))})"
        print_grade()
        critical_error(f"[ERROR] Missing files in root folder ({list(valid_root_files.difference(root_files))}) - Grading halted")


"""
Check the internal file structure of the folder Q{question_num}, given a valid_files_list
Exit if all the files in valid_files_list are not present
"""
def check_internal_files(expected_submission_path, question_num, valid_files_list):
    # print(question_num)
    temp_list = [file for file in valid_files_list]
    for q_file in os.listdir(os.path.join(expected_submission_path,f"Q{question_num}")):
        if os.path.isdir(q_file):
            if os.path.basename(q_file)[0] != ".":
                error(f"[ERROR] Q{question_num} submission format mismatch (unkown folder {os.path.basename(q_file)}) - Ending Q{question_num} grading")
                return False
        elif os.path.basename(q_file) in valid_files_list:
            temp_list.remove(q_file)
            continue
        else:
            if os.path.basename(q_file)[0] != ".":
                error(f"[ERROR] Q{question_num} submission format mismatch (unkown file {os.path.basename(q_file)}) - Ending Q{question_num} grading")
                return False

    if len(temp_list) > 0:
        grade.format_message = f"Missing the following files: ({', '.join(temp_list)})"
        print_grade()
        critical_error(f"[ERROR] Missing the following files: ({', '.join(temp_list)}) - Grading halted")

    info(f"[INFO] Q{question_num} submission format match")
    return True


"""
* Top wrapper to check the folder structure and internal files
* Exit if there is any extra folder
"""
def check_structure(root_files, root_folders, expected_submission_path, submission_file_name):
    # valid_root_folders = set(["Q2","Q3","Q4"])
    # valid_root_files = set([f"{submission_file_name[:-18]}-report.pdf"])
    # valid_root_files = set()

    # check_root_files(root_files, valid_root_files)

    is_q2_valid = False
    is_q3_valid = False
    is_q4_valid = False

    for folder in root_folders:
        if folder == "Q2":
            is_q2_valid = True
        elif folder == "Q3":
            is_q3_valid = True
        elif folder == "Q4":
            is_q4_valid = True
        else:
            grade.format_message = f"Extra folder in root ({folder})"
            print_grade()
            critical_error(f"[ERROR] Extra folder in root ({folder}) - Grading halted")

    if not (is_q2_valid and is_q3_valid and is_q4_valid):
        grade.format_message = f"Missing folders in root ({list(root_folders.difference(folder))})"
        print_grade()
        critical_error(f"[ERROR] Missing folders in root ({list(root_folders.difference(folder))})")

    if is_q2_valid:
        valid_q2_files = ["inverse.s"]
        is_q2_valid = check_internal_files(expected_submission_path, 2, valid_q2_files)

    if is_q3_valid:
        valid_q3_files = ["inplacemergesort.s"]
        is_q3_valid = check_internal_files(expected_submission_path, 3, valid_q3_files)

    if is_q4_valid:
        valid_q4_files = ["io.asm","Makefile","matrix-multiplication-ijk.asm","matrix-multiplication-ikj.asm",
                          "matrix-multiplication-jik.asm","matrix-multiplication-jki.asm","matrix-multiplication-kij.asm",
                          "matrix-multiplication-kji.asm","matrix-multiplication-testbench.asm","memory-test.asm"]
        is_q4_valid = check_internal_files(expected_submission_path, 4, valid_q4_files)
        
    return is_q2_valid, is_q3_valid, is_q4_valid

def main():
    # Argument parsing and help method
    parser = argparse.ArgumentParser(description="""Autograder for Lab3 - note that if a test fails, further tests that depend on it might not be performed. Ex. if compilation fails, program will not be run. 
                                                    Furthermore only some of the required tests are performed in this code and it is not exhaustive, you are required to perform your own testing.
                                                    """)
    parser.add_argument("path", help="relative/absolute path of .tar.gz submission", type=str)
    parser.add_argument("-v", "--verbose", help="control log output - if not present only success/failure of test shown. If -v then error info shown. If -vv then debug messages shown.", action="count", default=0)
    parser.add_argument("-q2", "--ignore_q2", help="ingore q2 testing", action="store_true")
    parser.add_argument("-q3", "--ignore_q3", help="ingore q3 testing", action="store_true")
    parser.add_argument("-q4", "--ignore_q4", help="ingore q4 testing", action="store_true")
    args = parser.parse_args()

    set_verbosity(args.verbose)

    # Submission file path
    submission = os.path.abspath(args.path)
    submission_file_name = os.path.basename(submission)

    # Argument sanity check
    if not os.path.isfile(submission):
        critical_error(f"[ERROR] Submission file at {submission} does not exist")

    if "_cs232_lab3.tar.gz" != submission_file_name[-18:]:
        critical_error(f"[ERROR] Submission file name {submission_file_name} invalid")

    grade.roll_no = submission_file_name[:-18]
    grade.roll_no.replace('D', '5')
    grade.roll_no.replace('B', '4')

    with tempfile.TemporaryDirectory() as tmpdirname:
        enter_temporary_dir(tmpdirname)
        extract_tar(tmpdirname, submission)
        expected_submission_path = check_folder_name(tmpdirname, submission_file_name)
        enter_submission_folder(expected_submission_path)    
        root_folders, root_files = get_root_folders_and_files(expected_submission_path)
        is_q2_valid, is_q3_valid, is_q4_valid = check_structure(root_files, root_folders, expected_submission_path, submission_file_name)
        
        if is_q2_valid and is_q3_valid and is_q4_valid:
            test_pass(f"{pass_char} Format validation passed")
        else:
            test_fail(f"{fail_char} Format validation failed")

        if (not args.ignore_q2) and is_q2_valid:
            os.chdir(os.path.join(expected_submission_path,"Q2"))
            # Testing code for Q2
            q2_test.check_q2(expected_submission_path)

        if (not args.ignore_q3) and is_q3_valid:
            os.chdir(os.path.join(expected_submission_path,"Q3"))
            # Testing code for Q3
            q3_test.check_q3(expected_submission_path)

        if (not args.ignore_q4) and is_q4_valid:
            os.chdir(os.path.join(expected_submission_path,"Q4"))
            # Testing code for Q4
            q4_test.check_q4(expected_submission_path)

        # import time
        # time.sleep(60)

        print_grade()

        os.chdir(basedir)
        info(f"[INFO] exited and cleaned {tmpdirname}")


if __name__ == '__main__':
    main()

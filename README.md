# Lab3-Autograder

Autograder used for Lab3. Prepared by Girish Srivatsa and Prajeeth.S

## Instructions for Usage:

```
    python3 autograder.py -vvv <path-to-your-tar-gz-file>
```

On running, a file named `grades.csv` is created, which shows various parameters as given in `grade_structure.py`

For Q2 bonus, there is a folder named bonus inside `testcases/Q2`. Place your inverse.s file inside the `testcases/Q2/bonus/submission` folder and run `./generate_answers.sh` to check for correctness. For generating results only for a particular question you can ignore testing other parts by the flags `-q2,-q3,-q4` where `-q2` results in no testing for Q2 being performed.

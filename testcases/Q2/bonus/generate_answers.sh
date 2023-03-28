#! /bin/bash

for i in {1..1000}
do
    echo "testcase #${i}"
   python3 "compute_inverse.py" < "input/${i}" > "expected_output/${i}"
   spim -f "submission/inverse.s" < "input/${i}" > "output/${i}"

   if cmp -s "expected_output/${i}" "output/${i}"; then 
    # echo "same..."
    echo "same..."
   else 
    echo "different..."
   fi

done
#!/bin/sh
M=( 1 2 3 4 5 6 7 8 9 10 11 12 13 14)

for m in ${M[@]}
do
    mpirun -n $m /bin/python3 /home/tr0fin0/Documents/git_repositories/OS202_2023_examen/ExamenOS202_21Mars2023/automate_cellulaire_1d.py
done
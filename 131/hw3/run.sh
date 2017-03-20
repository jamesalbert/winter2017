#!/usr/bin/bash
set -e

g++ -std=c++11 -fopenmp Implementation.cpp -o imp
OMP_NUM_THREADS=$2 ./imp aniketsh_tc2.pgm aniketsh_tc2.out.pgm $3 $1

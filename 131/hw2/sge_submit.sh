#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -pe openmpi 16
#$ -o output_b2_16.out
#
#
# Use modules to setup the runtime environment
#
module load sge
module load openmpi
#
# Execute the run
#
mpirun -np $NSLOTS partb input.txt the b2

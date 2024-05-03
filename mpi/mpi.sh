#!/bin/bash -l
# The -l above is required to get the full environment with modules

# The name of the script is myjob
#SBATCH -J mpi
# Only 1 hour wall-clock time will be given to this job
#SBATCH -t 0:10:00
#SBATCH -A edu24.DD2356
# Number of nodes
#SBATCH -p main
#SBATCH --ntasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --nodes=2
#SBATCH -e error_file.e

# Run the executable file 
# and write the output into my_output_file
perf stat srun -n 256 ./finitedifference_mpi.out > mpi_perf_256.txt 2>&1
# srun -n 1 ./finitedifference_mpi.out

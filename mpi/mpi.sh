#!/bin/bash -l
# The -l above is required to get the full environment with modules

# The name of the script is myjob
#SBATCH -J mpi
# Only 1 hour wall-clock time will be given to this job
#SBATCH -t 0:10:00
#SBATCH -A edu24.DD2356
# Number of nodes
#SBATCH -p main
#SBATCH --ntasks-per-node=64
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH -e error_file.e

# Run the executable file 
# and write the output into my_output_file
srun -n 64 ./finitedifference_mpi.out
# srun -n 1 ./finitedifference_mpi.out

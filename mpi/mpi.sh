#!/bin/bash -l
# The -l above is required to get the full environment with modules

# The name of the script is mpi
#SBATCH -J mpi
# Only 10 mins wall-clock time will be given to this job
#SBATCH -t 0:10:00
#SBATCH -A edu24.DD2356
# Number of nodes
#SBATCH -p main
#SBATCH --ntasks-per-node=64
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH -e error_file.e

# Run the executable file 
srun -n 32 ./finitedifference_mpi.out
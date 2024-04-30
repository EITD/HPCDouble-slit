#!/bin/bash -l
# The -l above is required to get the full environment with modules

# The name of the script is myjob
#SBATCH -J openmp
# Only 1 hour wall-clock time will be given to this job
#SBATCH -t 0:10:00
#SBATCH -A edu24.DD2356
# Number of nodes
#SBATCH -p shared
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=256
#SBATCH --nodes=1
#SBATCH -e error_file.e

# Run the executable file 
# and write the output into my_output_file
export OMP_NUM_THREADS=256 &&
OMP_PLACES=cores &&
srun -n 1 perf stat ./finitedifference_openmp.out > openmp_perf.txt 2>&1
# srun -n 1 ./finitedifference_openmp.out

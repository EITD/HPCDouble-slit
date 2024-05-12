# HPCDouble-slit

## How to run

There are 3 versions code of the double-slit experiment.

### Serial

Simply submit the batch job.

```bash
sbatch ./serial.sh
```

### OpenMp

Assign different numbers of threads before running the code. In `openmp.sh`, change the following line.

```bash
export OMP_NUM_THREADS=<number of threads>
```

Then submit the batch job.

```bash
sbatch ./openmp.sh
```

### MPI

Assign different numbers of processes when running the code. In `mpi.sh`, change the following line.

```bash
srun -n <number of processes> ./finitedifference_mpi.out
```

Then submit the batch job.

```bash
sbatch ./mpi.sh
```

## Plot outputs
Use the plot script to visualize the wave propagation. Change to serial/openmp/mpi directory for required output.

```bash
cd <target output directory>
python3 plot.py
```

## Check outputs

In `validate.py`, change the path of `dir2` to the result output directory. Then run the script.

```bash
dir2 = "mpi/output"
```

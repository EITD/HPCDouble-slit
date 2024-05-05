#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <string.h>
#include <mpi.h>

#define N 256 // resolution
#define BOXSIZE 1.0
#define C 1.0
#define TEND 2.0

void initialize_arrays(double U[N][N], bool mask[N][N], int start_row, int end_row)
{
    double dx = BOXSIZE / N;
    for (int i = start_row; i < end_row; i++)
    {
        for (int j = 0; j < N; j++)
        {
            U[i][j] = 0.0;
            mask[i][j] = false;
            if (i == 0 || i == N - 1 || j == 0 || j == N - 1)
            {
                mask[i][j] = true;
            }
        }
    }

    for (int i = start_row; i < end_row; i++)
    {
        for (int j = 0; j < N - 1; j++)
        {
            if (i >= N / 4 && i < N * 9 / 32)
            {
                mask[i][j] = true;
            }
        }

        if (i >= 1 && i < N - 1)
        {
            for (int j = N * 5 / 16; j < N * 3 / 8; j++)
            {
                mask[i][j] = false;
            }
            for (int j = N * 5 / 8; j < N * 11 / 16; j++)
            {
                mask[i][j] = false;
            }
        }
    }
}

void transpose(double src[N][N], double dest[N][N])
{
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            dest[j][i] = src[i][j];
        }
    }
}

void output_to_file(double U[N][N], FILE *file)
{
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            fprintf(file, "%lf ", U[i][j]);
        }
        fprintf(file, "\n");
    }
    fflush(file);
}

void update_wave_equation(double U[N][N], double Uprev[N][N], bool mask[N][N], double xlin[N], int start_row, int end_row, int rank, int size)
{
    double dx = BOXSIZE / N;
    double dt = (sqrt(2) / 2) * dx / C;
    double fac = dt * dt * C * C / (dx * dx);
    // printf("rank: %d, start: %d, end: %d\n", rank, start_row, end_row);
    double t = 0;
    while (t < TEND)
    {
        // Compute new state
        double Unew[N][N];
        if (size > 1)
        {
            MPI_Status status;
            if (rank == 0)
            {
                MPI_Sendrecv(&U[start_row][0], N, MPI_DOUBLE, size - 1, 0,
                             &U[end_row][0], N, MPI_DOUBLE, rank + 1, 0,
                             MPI_COMM_WORLD, &status);
            }
            else if (rank == size - 1)
            {
                MPI_Sendrecv(&U[start_row][0], N, MPI_DOUBLE, rank - 1, 0,
                             &U[0][0], N, MPI_DOUBLE, 0, 0,
                             MPI_COMM_WORLD, &status);
            }
            else
            {
                MPI_Sendrecv(&U[start_row][0], N, MPI_DOUBLE, rank - 1, 0,
                             &U[end_row][0], N, MPI_DOUBLE, rank + 1, 0,
                             MPI_COMM_WORLD, &status);
            }

            if (rank == 0)
            {
                MPI_Sendrecv(&U[end_row - 1][0], N, MPI_DOUBLE, rank + 1, 0,
                             &U[N - 1][0], N, MPI_DOUBLE, size - 1, 0,
                             MPI_COMM_WORLD, &status);
            }
            else if (rank == size - 1)
            {
                MPI_Sendrecv(&U[end_row - 1][0], N, MPI_DOUBLE, 0, 0,
                             &U[start_row - 1][0], N, MPI_DOUBLE, rank - 1, 0,
                             MPI_COMM_WORLD, &status);
            }
            else
            {
                MPI_Sendrecv(&U[end_row - 1][0], N, MPI_DOUBLE, rank + 1, 0,
                             &U[start_row - 1][0], N, MPI_DOUBLE, rank - 1, 0,
                             MPI_COMM_WORLD, &status);
            }
        }

        for (int i = start_row; i < end_row; i++)
        {
            for (int j = 0; j < N; j++)
            {
                double laplacian = (U[(i == 0 ? N - 1 : i - 1)][j] + U[i][(j == 0 ? N - 1 : j - 1)] - 4 * U[i][j] + U[(i == N - 1 ? 0 : i + 1)][j] + U[i][(j == N - 1 ? 0 : j + 1)]);
                Unew[i][j] = 2 * U[i][j] - Uprev[i][j] + fac * laplacian;
            }
        }
        // Apply boundary conditions
        for (int i = start_row; i < end_row; i++)
        {
            for (int j = 0; j < N; j++)
            {
                if (mask[i][j])
                {
                    Unew[i][j] = 0;
                }
                if (i == 0)
                {
                    Unew[0][j] = sin(20 * M_PI * t) * pow(sin(M_PI * xlin[j]), 2);
                }
            }
        }

        // Swap arrays
        memcpy(Uprev, U, sizeof(double) * N * N);
        memcpy(U, Unew, sizeof(double) * N * N);

        for (int i = start_row; i < end_row; i++)
        {
            for (int j = 0; j < N; j++)
            {
                if (mask[i][j])
                {
                    Unew[i][j] = HUGE_VAL; // 使用HUGE_VAL来模拟NaN
                }
            }
        }

        if (rank == 0)
        {
            for (int r = 1; r < size; r++)
            {
                MPI_Recv(&Unew[r * N / size][0], N / size * N, MPI_DOUBLE, r, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            }
            double UT[N][N];
            transpose(Unew, UT);

            // char filename[50];
            // sprintf(filename, "output/uplot_data_%lf.txt", t); // 格式化文件名
            // FILE *file = fopen(filename, "w");
            // output_to_file(UT, file);
            // fclose(file);
        }
        else
        {
            MPI_Send(&Unew[start_row][0], N / size * N, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
        }

        t += dt;
    }
}

int main(int argc, char **argv)
{
    int rank, size, provided;
    MPI_Init_thread(&argc, &argv, MPI_THREAD_SINGLE, &provided);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    double start_time, stop_time, elapsed_time, total_time;
    start_time = MPI_Wtime();

    double xlin[N];
    double U[N][N];
    double Uprev[N][N];
    bool mask[N][N];

    int start_row = rank * N / size;
    int end_row = (rank + 1) * N / size;

    if (rank == 0)
    {
        double dx = BOXSIZE / N;
        for (int i = 0; i < N; i++)
        {
            xlin[i] = (0.5 + i) * dx;
        }
    }
    initialize_arrays(U, mask, start_row, end_row);

    update_wave_equation(U, Uprev, mask, xlin, start_row, end_row, rank, size);

    stop_time = MPI_Wtime();
    elapsed_time = stop_time - start_time;

    MPI_Reduce(&elapsed_time, &total_time, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0)
    {
        printf("Average execution time: %f\n", total_time / size);
    }

    return 0;
}

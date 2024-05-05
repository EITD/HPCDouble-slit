#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <string.h>
#include <omp.h>

#define N 256 // resolution
#define BOXSIZE 1.0
#define C 1.0
#define TEND 2.0

void initialize_arrays(double U[N][N], bool mask[N][N], double xlin[N])
{
    double dx = BOXSIZE / N;
#pragma omp parallel for collapse(2)
    for (int i = 0; i < N; i++)
    {
        xlin[i] = (0.5 + i) * dx;
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

#pragma omp parallel for collapse(2)
    for (int i = N / 4; i < N * 9 / 32; i++)
    {
        for (int j = 0; j < N - 1; j++)
        {
            mask[i][j] = true;
        }
    }
#pragma omp parallel for
    for (int i = 1; i < N - 1; i++)
    {
#pragma omp parallel for
        for (int j = N * 5 / 16; j < N * 3 / 8; j++)
        {
            mask[i][j] = false;
        }
#pragma omp parallel for
        for (int j = N * 5 / 8; j < N * 11 / 16; j++)
        {
            mask[i][j] = false;
        }
    }
}

void transpose(double src[N][N], double dest[N][N])
{
#pragma omp parallel for collapse(2)
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

void update_wave_equation(double U[N][N], double Uprev[N][N], bool mask[N][N], double xlin[N])
{
    double dx = BOXSIZE / N;
    double dt = (sqrt(2) / 2) * dx / C;
    double fac = dt * dt * C * C / (dx * dx);
    double t = 0;
    while (t < TEND)
    {
        // Compute new state
        double Unew[N][N];
#pragma omp parallel for collapse(2)
        for (int i = 0; i < N; i++)
        {
            for (int j = 0; j < N; j++)
            {
                double laplacian = (U[(i == 0 ? N - 1 : i - 1)][j] + U[i][(j == 0 ? N - 1 : j - 1)] - 4 * U[i][j] + U[(i == N - 1 ? 0 : i + 1)][j] + U[i][(j == N - 1 ? 0 : j + 1)]);
                Unew[i][j] = 2 * U[i][j] - Uprev[i][j] + fac * laplacian;
                if (mask[i][j])
                {
                    Unew[i][j] = 0;
                }
            }
        }
        // Apply boundary conditions
#pragma omp parallel for
        for (int j = 0; j < N; j++)
        {
            Unew[0][j] = sin(20 * M_PI * t) * pow(sin(M_PI * xlin[j]), 2);
        }

        // Swap arrays
        memcpy(Uprev, U, sizeof(double) * N * N);
        memcpy(U, Unew, sizeof(double) * N * N);

#pragma omp parallel for collapse(2)
        for (int i = 0; i < N; i++)
        {
            for (int j = 0; j < N; j++)
            {
                if (mask[i][j])
                {
                    Unew[i][j] = HUGE_VAL; // 使用HUGE_VAL来模拟NaN
                }
            }
        }

        double UT[N][N];
        transpose(Unew, UT);

        // char filename[50];
        // sprintf(filename, "output/uplot_data_%lf.txt", t); // 格式化文件名
        // FILE *file = fopen(filename, "w");
        // output_to_file(UT, file);
        // fclose(file);

        t += dt;
    }
}

int main()
{
    double xlin[N];
    double U[N][N];
    double Uprev[N][N];
    bool mask[N][N];

    initialize_arrays(U, mask, xlin);
    update_wave_equation(U, Uprev, mask, xlin);

    return 0;
}
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

#define N 256 // resolution
#define BOXSIZE 1.0
#define C 1.0
#define TEND 2.0

void initialize_arrays(double **U, bool **mask, double *xlin)
{
    double dx = BOXSIZE / N;
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

    for (int i = N / 4; i < N * 9 / 32; i++)
    {
        for (int j = 0; j < N - 1; j++)
        {
            mask[i][j] = true;
        }
    }
    for (int i = 1; i < N - 1; i++)
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

void update_wave_equation(double **U, double **Uprev, bool **mask, double *xlin)
{
    double dx = BOXSIZE / N;
    double dt = (sqrt(2) / 2) * dx / C;
    double fac = dt * dt * C * C / (dx * dx);
    double t = 0;
    while (t < TEND)
    {
        // Compute new state
        double **Unew = (double **)malloc(N * sizeof(double *));
        for (int i = 0; i < N; i++)
        {
            Unew[i] = (double *)malloc(N * sizeof(double));
            for (int j = 0; j < N; j++)
            {
                double laplacian = (U[(i == 0 ? N - 1 : i - 1)][j] + U[i][(j == 0 ? N - 1 : j - 1)] - 4 * U[i][j] + U[(i == N - 1 ? 0 : i + 1)][j] + U[i][(j == N - 1 ? 0 : j + 1)]);
                Unew[i][j] = 2 * U[i][j] - Uprev[i][j] + fac * laplacian;
            }
        }
        // Apply boundary conditions
        for (int i = 0; i < N; i++)
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
        free(Uprev);
        Uprev = U;
        U = Unew;

        t += dt;

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

        double **UT = (double **)malloc(N * sizeof(double *));
        for (int i = 0; i < N; i++)
        {
            UT[i] = (double *)malloc(N * sizeof(double));
        }
        transpose(Unew, UT);

        
    }

    // Free the last used arrays
    free(Uprev);
    for (int i = 0; i < N; i++)
    {
        free(U[i]);
    }
    free(U);
}

void transpose(double **src, double **dest)
{
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            dest[j][i] = src[i][j];
        }
    }
}

void output_array_to_file(double array[N][N], const char *filename)
{
    FILE *file = fopen(filename, "w");
    if (file == NULL)
    {
        perror("Failed to open file");
        exit(1);
    }

    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            fprintf(file, "%lf ", array[i][j]);
        }
        fprintf(file, "\n");
    }

    fclose(file);
}

int main()
{
    double *xlin = (double *)malloc(N * sizeof(double));
    double **U = (double **)malloc(N * sizeof(double *));
    double **Uprev = (double **)malloc(N * sizeof(double *));
    bool **mask = (bool **)malloc(N * sizeof(bool *));
    for (int i = 0; i < N; i++)
    {
        U[i] = (double *)malloc(N * sizeof(double));
        Uprev[i] = (double *)malloc(N * sizeof(double));
        mask[i] = (bool *)malloc(N * sizeof(bool));
    }

    initialize_arrays(U, mask, xlin);
    update_wave_equation(U, Uprev, mask, xlin);

    free(xlin);
    for (int i = 0; i < N; i++)
    {
        free(mask[i]);
    }
    free(mask);

    return 0;
}

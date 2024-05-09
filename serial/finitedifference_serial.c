#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <string.h>

#define N 256 // resolution
#define BOXSIZE 1.0
#define C 1.0
#define TEND 2.0

/**
 * @brief Initial arrays.
 * 
 * @param U Wave state array.
 * @param mask Boundary mask array.
 * @param xlin X-lin array for simulate the wave start.
 */
void initialize_arrays(double U[N][N], bool mask[N][N], double xlin[N])
{
    double dx = BOXSIZE / N;
    // Initialize along x-axis
    for (int i = 0; i < N; i++)
    {
        xlin[i] = (0.5 + i) * dx;
        // Initialize wave and boundary mask
        for (int j = 0; j < N; j++)
        {
            U[i][j] = 0.0;
            mask[i][j] = false;
            if (i == 0 || i == N - 1 || j == 0 || j == N - 1)
            {
                mask[i][j] = true; // Boundary -> true
            }
        }
    }

    // Additional boundary, the double-slit
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

/**
 * @brief Transpose matrix.
 * 
 * @param src Source matrix.
 * @param dest Destination matrix.
 */
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

/**
 * @brief Output wave state to file.
 * 
 * @param U Wave state array.
 * @param file Output file pointer.
 */
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

/**
 * @brief Update wave array over time.
 * 
 * @param U Current wave state array.
 * @param Uprev Previous wave state array.
 * @param mask Boundary mask array.
 * @param xlin X-lin array for simulate the wave start.
 */
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
        for (int i = 0; i < N; i++)
        {
            for (int j = 0; j < N; j++)
            {
                double laplacian = (U[(i == 0 ? N - 1 : i - 1)][j] + U[i][(j == 0 ? N - 1 : j - 1)] - 4 * U[i][j] + U[(i == N - 1 ? 0 : i + 1)][j] + U[i][(j == N - 1 ? 0 : j + 1)]);
                Unew[i][j] = 2 * U[i][j] - Uprev[i][j] + fac * laplacian;
            }
        }
        // Apply boundary and initial conditions
        for (int i = 0; i < N; i++)
        {
            for (int j = 0; j < N; j++)
            {
                if (mask[i][j])
                {
                    Unew[i][j] = 0; // Boundary -> 0
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

        for (int i = 0; i < N; i++)
        {
            for (int j = 0; j < N; j++)
            {
                if (mask[i][j])
                {
                    Unew[i][j] = HUGE_VAL; // use HUGE_VAL to simulate NaN
                }
            }
        }

        double UT[N][N];
        transpose(Unew, UT);

        // char filename[50];
        // sprintf(filename, "output/uplot_data_%lf.txt", t); // Format file name
        // FILE *file = fopen(filename, "w");
        // output_to_file(UT, file);
        // fclose(file);

        // Increase time
        t += dt;
    }
}

/**
 * @brief Main.
 * 
 * @return 0.
 */
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

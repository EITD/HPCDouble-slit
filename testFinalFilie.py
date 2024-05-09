import numpy as np

file1 = "./1.txt"
file2 = "./2.txt"

file1_data = np.loadtxt(file1, dtype=float)
file1_data = np.where(np.isnan(file1_data) | np.isinf(file1_data), 0.0, file1_data)
file1_data = np.around(file1_data, decimals=6)

file2_data = np.loadtxt(file2, dtype=float)
file2_data = np.where(np.isnan(file2_data) | np.isinf(file2_data), 0.0, file2_data)
file2_data = np.around(file2_data, decimals=6)

if np.array_equal(file1_data, file2_data):
        print("Same")
else:
        print("Not same")


import os
import numpy as np

def compare_files(file1, file2):
        file1_data = np.loadtxt(file1, dtype=float)
        file1_data = np.where(np.isnan(file1_data) | np.isinf(file1_data), 0.0, file1_data)
        file1_data = np.around(file1_data, decimals=6)

        file2_data = np.loadtxt(file2, dtype=float)
        file2_data = np.where(np.isnan(file2_data) | np.isinf(file2_data), 0.0, file2_data)
        file2_data = np.around(file2_data, decimals=6)

        if np.array_equal(file1_data, file2_data):
               return True
        else:
               return False

def compare_directories(dir1, dir2):
    files1 = sorted(os.listdir(dir1))
    files2 = sorted(os.listdir(dir2))
    
    if len(files1) != len(files2):
        print("Different size!")
        return False
    
    for file1, file2 in zip(files1, files2):
        path1 = os.path.join(dir1, file1)
        path2 = os.path.join(dir2, file2)
                
        if not compare_files(path1, path2):
            print(f"Different file: {file1} 和 {file2}")
            return False
    
    print("All same.")
    return True

dir1 = "output"
dir2 = "mpi/output"
compare_directories(dir1, dir2)
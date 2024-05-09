import os
import re
from math import isclose

float_regex = re.compile(r'([-+]?\d*\.\d+([eE][-+]?\d+)?|[-+]?\d+[eE][-+]?\d+|[-+]?\d+)')

def parse_and_compare_floats(line1, line2):
    def get_floats(line):
        for num in float_regex.findall(line):
             print(num)
        return [float(num) for num in float_regex.findall(line)]
    
    floats1 = get_floats(line1)
    floats2 = get_floats(line2)
    
    if len(floats1) != len(floats2):
        return False
    
    for num1, num2 in zip(floats1, floats2):
        if not isclose(round(num1, 6), round(num2, 6), rel_tol=1e-6, abs_tol=1e-6):
            print(num1, num2)
            return False
    return True

def compare_files(file1, file2):
        with open(file1, "r") as f1, open(file2, "r") as f2:
                for line1, line2 in zip(f1, f2):
                        if not parse_and_compare_floats(line1.strip(), line2.strip()):
                                return False
                if any(f1) or any(f2):
                        return False
        return True

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
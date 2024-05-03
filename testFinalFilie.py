def compare_files(file1, file2):
        with open(file1, "r") as f1, open(file2, "r") as f2:
                for line1, line2 in zip(f1, f2):
                        if line1 != line2:
                                return False
                if any(f1) or any(f2):
                        return False
        return True


file1 = "./uplot_data_1.999786_mpi.txt"
file2 = "./uplot_data_1.999786_openmp.txt"

if compare_files(file1, file2):
        print("same.")
else:
        print("not same.")

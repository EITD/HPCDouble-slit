import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

sizes = np.array([1, 2, 4, 8, 16, 32, 64, 128, 256]) 
times = np.array([19.371616717, 18.403196836, 16.083139587, 15.866991874, 15.927508032, 15.984533610, 16.177270197, 20.782886575, 23.394011481])

def performance_model(p, a, b, c):
    return a/p + b*p**c

params, params_covariance = curve_fit(performance_model, sizes, times)

plt.figure(figsize=(10, 7))
plt.plot(sizes, times, marker='o', linestyle='-', label='Measured Data')
plt.plot(sizes, performance_model(sizes, *params), color='red', label='Fitted function: a/p + b*p^c')
plt.xlabel('Number of Processes')
plt.ylabel('Execution Time (seconds)')
plt.title('Performance Modeling of Distributed Matrix Multiplication')
plt.xticks(sizes)
plt.legend()
plt.savefig('model.png')

print("Fitted parameters: a =", params[0], ", b =", params[1], ", c =", params[2])
